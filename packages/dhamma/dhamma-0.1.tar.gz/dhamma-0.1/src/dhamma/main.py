from openai import OpenAI
from pydub import AudioSegment
import os
from io import BytesIO
import argparse
import tiktoken
import json
import itertools
import sys
import time
import threading
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed, Future


MODEL = "gpt-4-1106-preview"
TOKEN_LIMIT = 1000  # 2048 for gpt-4
TOKENS_PER_MESSAGE = 3
TOKENS_PER_NAME = 1
ENCODER = tiktoken.encoding_for_model(MODEL)

SEGMENT_DURATION = 10 * 60 * 1000  # ten minutes
WHISPER_TIMEOUT_SEC = 300  # 5 minutes
CHAT_TIMEOUT_SEC = 60  # 3 minutes

DEBUG = os.getenv("DEBUG")


def debug(msg: str):
    if DEBUG:
        print(msg)


def extract_title_from_file(filename: str) -> str:
    """'./out/3. Some Title' -> 'Some Title'"""
    # remove everything up to and including the file number
    title_part = filename.split(". ")[1]
    # remove extension
    return os.path.splitext(title_part)[0]


def extract_prefix_from_title(title: str) -> int:
    """'3. Some Title' -> 3"""
    number_part = title.split(".")[0]
    return int(number_part)


def extract_prefix_from_file(filename: str) -> int:
    """'./out/3. Some Title' -> 3"""
    filename = os.path.basename(filename)
    number_part = filename.split(".")[0]
    return int(number_part)


class Spinner(threading.Thread):
    def __init__(self, message="Loading..."):
        super().__init__()
        self.message = message
        self.percentage: float = None
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.is_set():
            for char in itertools.cycle("|/-\\"):
                if self._stop_event.is_set():
                    break
                status = f"\r{self.message} {char}"
                if self.percentage:
                    status = f"\r{self.message} {self.percentage:.2f}% {char}"
                sys.stdout.write(status)
                sys.stdout.flush()
                time.sleep(0.1)

    def update_progress(self, percentage: float):
        self.percentage = percentage

    def stop(self):
        print()  # newline
        self._stop_event.set()


def count_tokens_in(text: str) -> int:
    num_tokens = TOKENS_PER_MESSAGE
    num_tokens += len(ENCODER.encode(text))
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens


def count_tokens(messages: list[dict[str, str]]) -> int:
    # adapted from https://github.com/openai/openai-cookbook
    num_tokens = 0
    for message in messages:
        num_tokens += TOKENS_PER_MESSAGE
        for key, value in message.items():
            num_tokens += len(ENCODER.encode(value))
            if key == "name":
                num_tokens += TOKENS_PER_NAME
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens


def transcribe_audio(client: OpenAI, input_path: str) -> str:
    segments = []
    audio_file = AudioSegment.from_mp3(input_path)
    for i in range(0, len(audio_file), SEGMENT_DURATION):
        end_time = min(i + SEGMENT_DURATION, len(audio_file))
        segment = audio_file[i:end_time]

        buffer = BytesIO()
        buffer.name = input_path
        segment.export(buffer, format="mp3")

        buffer.seek(0)
        segments.append(buffer)

    raw_transcript = ""
    for segment in segments:
        transcript = client.audio.transcriptions.create(
            model="whisper-1", file=segment, timeout=WHISPER_TIMEOUT_SEC
        )
        raw_transcript += transcript.text
    return raw_transcript


def create_chunks(full_text: str, max_tokens: int) -> list[str]:
    words = full_text.split()
    chunks = []
    current_chunk = []

    for word in words:
        current_tokens = count_tokens_in(" ".join(current_chunk))
        current_tokens += count_tokens_in(word)
        if current_tokens > max_tokens:
            # Finalize the current chunk and start a new one
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
        else:
            # Add the current word to the existing chunk
            current_chunk.append(word)

    # Add the last chunk if it contains any words
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def overlap_prompts(chunks: list[str], overlap_tokens: int = 30) -> list[str]:
    init_msg = "This is the first part of the transcription\n---\n:"
    continuation_msg = "Continue cleaning up the transcription considering the above overlap for context:\n---\n"

    overlap_tokens -= count_tokens_in(continuation_msg)
    if overlap_tokens < 0:
        raise Exception(f"overlap token overflow: {overlap_tokens}")

    overlapped_prompts: list[str] = []
    for i, _ in enumerate(chunks):
        overlap_text = ""
        if i > 0:
            prev_chunk_words = chunks[i - 1].split(" ")
            overlap = overlap_tokens
            prev = []

            # try to find the right length of overlap to fall
            # within the given number of overlap tokens
            while True:
                num_tokens = count_tokens_in(" ".join(prev))
                # lop off 25% of the overlap until we find an overlap that works
                overlap = int(overlap - (overlap / 4))
                prev = prev_chunk_words[-overlap:]
                if num_tokens < overlap_tokens:
                    break

            overlap_text = " ".join(prev)
            prompt = f"{overlap_text}\n{continuation_msg}{chunks[i]}\n"
        else:
            prompt = f"{init_msg}{chunks[i]}\n"
        overlapped_prompts.append(prompt.strip())

    return overlapped_prompts


def correct_transcript(
    client: OpenAI,
    log_label: str,
    transcription: str,
    title: str,
    model: str = MODEL,
) -> str:
    print(f"{log_label} formatting and correcting transcript using {model}")

    system_prompt = """You are a helpful transcription assistant. You have the following tasks, given in priority order:

     1. Break up the text into readable paragraphs. Aim for around 5 sentences per paragraph, but very this as appropriate for the content.
     2. Correct any spelling discrepancies in the transcribed text
     3. Add necessary punctuation such as periods, commas, and capitalization

     Do this using only the context provided. The document you prepare will be read as part of a book, do not surround the transcription with quotes. The goal is readability. Whatever you respond with will be in the book so do not return anything except for the edited transcript."""

    system_tokens = count_tokens([{"role": "system", "content": system_prompt}])
    transcript_tokens = count_tokens([{"role": "user", "content": transcription}])
    max_tokens = TOKEN_LIMIT - system_tokens

    prompts = []
    if TOKEN_LIMIT - (system_tokens + transcript_tokens) > 0:
        # under the limit so we don't need to chunk
        prompts = [transcription]
    else:
        # over the limit so we need to chunk queries
        overlap_tokens = 30
        chunk_size = max_tokens - overlap_tokens
        chunks = create_chunks(transcription, chunk_size)
        prompts = overlap_prompts(chunks, overlap_tokens)

    # validate all messages before making any API requests
    all_messages: list[list[dict[str, str]]] = []
    for prompt in prompts:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]
        num_tokens = count_tokens(messages)
        if num_tokens > TOKEN_LIMIT:
            raise Exception(
                f"prompt has {num_tokens} tokens which is more than {TOKEN_LIMIT}: {json.dumps(messages, indent=4)}"
            )
        all_messages.append(messages)

    # execute all api requests
    total = len(prompts)
    output = [f"# {title}\n\n"]
    for i, messages in enumerate(all_messages):
        debug(f"sending messages: {json.dumps(messages, indent=4)}")

        response = client.chat.completions.create(
            timeout=CHAT_TIMEOUT_SEC,
            model=model,
            temperature=0,
            messages=messages,
        )
        content = response.choices[0].message.content
        output.append(content + " ")

        percentage = float(i) / float(total)
        print(f"{log_label} correction {percentage:.2f%}% completed")

    return "".join(output)


def transcribe(args: argparse.Namespace):
    # inputs
    file_or_dir: str = args.file_or_directory
    if not file_or_dir:
        print("Must provide either an input file or directory")
        exit(1)
    input_file: str = None
    input_directory: str = None
    if not os.path.exists(file_or_dir):
        print(f"'{file_or_dir} 'does not exist")
        exit(1)
    if os.path.isdir(file_or_dir):
        input_directory = file_or_dir
    elif os.path.isfile(file_or_dir):
        input_file = file_or_dir
    else:
        print("Must provide either an input file or directory")
        exit(1)
    input_files: list[str] = []

    # openai settings
    model = args.model
    client = OpenAI()

    # accept single mp3 or raw txt transcript file
    if input_file:
        input_directory = os.curdir
        file_path = os.path.join(os.curdir, input_file)
        if os.path.isfile(file_path):
            if not ".mp3" in file_path and not ".txt" in file_path:
                print("only mp3 or text files are supported")
                exit(0)
            input_files.append(file_path)
    # accept a directory containing mp3s,
    elif input_directory:
        entries = os.listdir(input_directory)
        files: dict[str, str] = {}
        for entry in entries:
            if not ".mp3" in entry and not ".txt" in entry and not ".md" in entry:
                continue

            file_path = os.path.join(input_directory, entry)
            if os.path.isfile(file_path):
                files[entry] = file_path

        # don't re-process files we've already transcribed as indicated by
        # the associated markdown file being present
        delete_files = []
        for entry, file_path in files.items():
            if ".md" in entry:
                print(
                    f"skipping file '{entry}' because it has already been transcribed"
                )
                delete_files.append(entry)
                delete_files.append(entry.replace(".md", ".mp3"))
                delete_files.append(entry.replace(".md", ".txt"))
        for filename in delete_files:
            del files[filename]

        # avoid re-transcribing files if possible
        for entry, file_path in files.items():
            if ".mp3" in entry:
                # prefer text files if present
                txt_entry = entry.replace(".mp3", ".txt")
                if txt_path := files.get(txt_entry):
                    input_files.append(txt_path)
                else:
                    input_files.append(file_path)

    if len(input_files) == 0:
        print("something went wrong when parsing input files")
        exit(1)

    correct_executor = ThreadPoolExecutor(max_workers=4)
    correct_futures: dict[Future, dict[str, str]] = {}
    # TODO: do all of this concurrently:
    # - transcribe_audio

    # process files in the expected order
    input_files = list(sorted(input_files, key=extract_prefix_from_file))
    for input_path in input_files:
        file_num = extract_prefix_from_file(input_path)
        title = extract_title_from_file(input_path)
        log_label = f"[{file_num}. {title}]"

        # set outputs and assume that outputs should be placed next to
        # their inputs
        mdfile: str = None
        txtfile: str = None
        is_txt = False
        if ".mp3" in input_path:
            mdfile = input_path.replace(".mp3", ".md")
            txtfile = input_path.replace(".mp3", ".txt")
        elif ".txt" in input_path:
            is_txt = True
            mdfile = input_path.replace(".txt", ".md")
            txtfile = input_path
        else:
            print(f"{log_label} unsupported file given {input_path}")
            exit(1)

        # get raw transcription
        transcription: str = None
        if is_txt:
            # restore previously prepared transcription
            print(f"{log_label} reading text file {input_path}")
            with open(input_path) as file:
                transcription = file.read()
        else:
            # create new transcription usind whisper
            spinner = Spinner(f"{log_label} transcribing audio file")
            spinner.start()
            transcription = transcribe_audio(client, input_path=input_path)
            spinner.stop()
            spinner.join()

            # write text file
            print(f"{log_label} writing text transcription to {txtfile}")
            with open(txtfile, "w") as file:
                file.write(transcription)

        # prepare corrected markdown file
        future = correct_executor.submit(
            correct_transcript, client, log_label, transcription, title, model
        )
        correct_futures[future] = {
            "input_path": input_path,
            "title": title,
            "mdfile": mdfile,
        }

    for future in as_completed(correct_futures):
        args = correct_futures[future]
        try:
            corrected = future.result()
            try:
                # write corrected markdown transcription
                print(f"{log_label} writing markdown transcription to {mdfile}")
                with open(mdfile, "w") as file:
                    file.write(corrected)
            except Exception as we:
                print(f"transcription write error: {we}")
        except Exception as e:
            title = args.get("title")
            print(f"failed to correct transcription '{title}': {e}")


def download_mp3(url: str, name: str, output_dir: str):
    print(f"downloading mp3 from {url}")

    response = requests.get(url)
    if response.status_code == 200:
        output_file = f"{output_dir}/{name}.mp3"
        with open(output_file, "wb") as file:
            file.write(response.content)
        print(f"Download complete. The MP3 file has been saved as '{output_file}'.")
    else:
        print(f"Failed to download the file. HTTP status code: {response.status_code}")


def parse_retreat_page(
    base_url: str, page_url: str, talk_counter: int = 1
) -> dict[str, str]:
    print(page_url)
    response = requests.get(page_url)
    response.raise_for_status()  # Will raise an exception if the HTTP request returned an unsuccessful status code
    soup = BeautifulSoup(response.text, "html.parser")
    anchors = soup.find_all("a")
    raw_page_url = urlparse(page_url)
    base_page_url = f"{raw_page_url.scheme}://{raw_page_url.netloc}{raw_page_url.path}"

    talks: dict[str, str] = {}
    next_counter = 0
    current_title: str = None
    next_url: str = None

    for anchor in anchors:
        a_class = anchor.get("class")
        link = anchor.get("href")
        link_text = anchor.text.strip()

        if a_class and ("talkteacher" in a_class and "/talks" in link):
            current_title = f"{talk_counter}. {link_text}"
        if ".mp3" in link:
            if current_title:
                talks[current_title] = base_url + link
            current_title = None
            talk_counter += 1
        if "next ››" in link_text:
            if next_counter > 0:
                next_url = base_page_url + link
            next_counter += 1

    if next_url:
        next_talks = parse_retreat_page(
            base_url=base_url, page_url=next_url, talk_counter=talk_counter
        )
        talks = {**next_talks, **talks}
        return talks

    return talks


def download_retreat(retreat_url: str, output_dir: str):
    url = urlparse(retreat_url)
    page_url = url.geturl()
    base_url = f"{url.scheme}://{url.netloc}"

    # TODO: prepare a simple markdown index file with the information
    # gathered from the retreat page:
    # - Title
    # - Date and duration
    talks = parse_retreat_page(base_url, page_url)
    talks = {
        key: talks[key] for key in sorted(talks.keys(), key=extract_prefix_from_title)
    }
    print(json.dumps(talks, indent=4))

    # TODO: download these in reverse order so that we know what the max
    # number is and then can pad lower numbers with the right number of
    # leading zeros. This way alphabetic sorting works as expected.

    # TODO: add date to downloaded file names
    executor = ThreadPoolExecutor(max_workers=4)
    futures: dict[Future, dict[str, str]] = {}
    for name, mp3_url in talks.items():
        future = executor.submit(download_mp3, mp3_url, name, output_dir)
        futures[future] = {
            "url": mp3_url,
            "name": name,
            "output_dir": output_dir,
        }

    for future in as_completed(futures):
        args = futures[future]
        try:
            future.result()
        except Exception as e:
            url = args.get("url")
            print(f"could not download audio file {url}: {e}")


def download(args: argparse.Namespace):
    retreat_id = args.retreat_id
    if not retreat_id:
        print("must provide a retreat ID")
        exit(1)
    if not retreat_id.isdigit():
        print(f"must provide a valid retreat ID. you provided: {retreat_id}")
        exit(1)

    output_dir = args.out
    if not output_dir:
        print("must provide the output directory to use")
        exit(1)

    if not os.path.exists(output_dir):
        print(f"the directory {output_dir} does not exist")
        exit(1)

    retreat_url = f"https://dharmaseed.org/retreats/{retreat_id}"
    download_retreat(retreat_url, output_dir)


def main():
    # command line arguments
    parser = argparse.ArgumentParser(
        prog="dhamma", description="Transcribe audio from Dharma Seed retreat talks."
    )
    subparsers = parser.add_subparsers(dest="subcommand", help="sub-command help")

    #
    # transcribe
    #
    transcribe_parser = subparsers.add_parser(
        "transcribe", help="transcribe mp3s from a retreat posted on Dharma Seed"
    )
    transcribe_parser.set_defaults(func=transcribe)
    transcribe_parser.add_argument(
        "file_or_directory",
        type=str,
        help="The input mp3 or txt file or directory containing the desired files",
    )
    transcribe_parser.add_argument(
        "-m", "--model", type=str, help="The GPT model to use", default=MODEL
    )

    #
    # download
    #
    download_parser = subparsers.add_parser(
        "download", help="download mp3s from Dharma Seed"
    )
    download_subparsers = download_parser.add_subparsers(
        dest="subcommand", help="sub-command help"
    )
    retreat_parser = download_subparsers.add_parser(
        "retreat", help="transcribe mp3s from a retreat posted on Dharma Seed"
    )
    retreat_parser.set_defaults(func=download)
    retreat_parser.add_argument(
        "retreat_id",
        type=str,
        help="The retreat ID (e.g. dharmaseed.org/retreats/3972 -> 3972)",
    )
    retreat_parser.add_argument(
        "-o", "--out", type=str, help="The output directory to place mp3 files"
    )

    # execute the function associated with the chosen subcommand
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
