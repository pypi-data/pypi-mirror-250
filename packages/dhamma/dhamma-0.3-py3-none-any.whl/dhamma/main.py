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
import re
import pypandoc
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


def remove_prefix_from_title(title: str) -> str:
    """'3. Some Title' -> 'Some Title'"""
    # remove everything up to and including the file number
    return title.split(". ")[1]


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
    output = []

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

        percentage = 100.0 * (float(i) / float(total))
        print(f"{log_label} correction {percentage:.2f}% completed")

    return "".join(output)


def mp3_to_title(filename: str) -> str:
    filename = os.path.basename(filename)
    # mp3 file has metadata within braces, other files do not
    pattern = re.compile(r".*(\[.*?\] ).*")
    match = pattern.match(filename)
    base_name = filename
    if match:
        base_name = filename.replace(match.group(1), "")
    return base_name.replace(".mp3", "")


def metadata_from_mp3(filename: str) -> dict[str, str]:
    pattern = re.compile(r".*(\[.*?\]).*")
    match = pattern.match(filename)
    meta = match.group(1).split(" - ")
    teacher = meta[0]
    date = meta[1]
    return {
        "teacher": teacher,
        "date": date,
    }


def metadata_from_readme(
    readme_contents: str, directory: str = ""
) -> dict[str, dict[str, str]]:
    metadata: dict[str, dict[str, str]] = {}

    bullet_pattern = re.compile(r"^\s+- (.*?)$")
    current_title: str = None
    for line in readme_contents.split("\n"):
        # replace links to mp3 file to markdown file
        if ".md" in line:
            link_pattern = re.compile(r".*\[(.*?)\]\((.*?)\)$")
            match = link_pattern.match(line)

            title = match.group(1)
            current_title = title

            metadata[current_title] = {
                "markdown": os.path.join(directory, f"{title}.md"),
            }
        elif ".mp3" in line:
            link_pattern = re.compile(r".*\[(.*?)\]\((.*?)\)$")
            match = link_pattern.match(line)

            title = match.group(1)
            current_title = title

            raw_link = match.group(2)

            mp3_link = raw_link.replace("%20", " ")
            mdfile = mp3_to_title(mp3_link) + ".md"
            mdlink = mdfile.replace(" ", "%20")

            metadata[current_title] = {
                "mp3": mp3_link,
                "markdown": os.path.join(directory, mdfile),
            }

            line = line.replace(raw_link, mdlink)
        elif "Teacher:" in line:
            match = bullet_pattern.match(line)
            meta = match.group(1)
            teacher = meta.replace("Teacher: ", "")
            info = metadata[current_title]
            info["teacher"] = teacher
            metadata[current_title] = info
        elif "Date:" in line:
            match = bullet_pattern.match(line)
            meta = match.group(1)
            date = meta.replace("Date: ", "")
            info = metadata[current_title]
            info["date"] = date
            metadata[current_title] = info
    return metadata


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
    readme_file: str = None

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
        # set index file to be updated
        readme_file = os.path.join(input_directory, "README.md")
        if not os.path.exists(readme_file):
            readme_file = None

        files: dict[str, str] = {}
        for entry in os.listdir(input_directory):
            # skip file types we don't care about
            if not ".mp3" in entry and not ".txt" in entry and not ".md" in entry:
                continue

            file_path = os.path.join(input_directory, entry)
            if os.path.isfile(file_path):
                files[entry] = file_path

        # don't re-process files we've already transcribed as indicated by
        # the associated markdown file being present
        skip_files = set()
        for entry, file_path in files.items():
            if "README" in entry:
                skip_files.add(entry)
            elif ".mp3" in entry or ".md" in entry:
                base_name = ""
                if ".mp3" in entry:
                    base_name = mp3_to_title(entry)
                elif ".md" in entry:
                    base_name = os.path.basename(entry)
                    base_name = base_name.replace(".md", "")
                txtfile = f"{base_name}.txt"
                mdfile = f"{base_name}.md"

                # prefer text file instead of mp3
                if files.get(txtfile):
                    skip_files.add(entry)
                # we have already transcribed it (md file present) - skip
                if files.get(mdfile):
                    skip_files.add(mdfile)
                    skip_files.add(txtfile)
                    skip_files.add(entry)

        for entry, file_path in files.items():
            if entry in skip_files:
                # if filename in files:
                if "README" not in entry:
                    print(
                        f"skipping file '{entry}' because it has already been transcribed"
                    )
                continue
            # add file to be processed
            input_files.append(file_path)

    metadata: dict[str, dict[str, str]] = {}

    if readme_file:
        # read readme file
        readme_contents: str = None
        with open(readme_file, "r") as file:
            readme_contents = file.read()

        mdlines = []

        bullet_pattern = re.compile(r"^\s+- (.*?)$")
        current_title: str = None
        for line in readme_contents.split("\n"):
            # replace links to mp3 file to markdown file
            if ".md" in line:
                link_pattern = re.compile(r".*\[(.*?)\]\((.*?)\)$")
                match = link_pattern.match(line)

                title = match.group(1)
                current_title = title
                label = make_log_label(title)

                metadata[current_title] = {
                    "markdown": os.path.join(input_directory, f"{title}.md"),
                    "text": os.path.join(input_directory, f"{title}.txt"),
                    "label": label,
                }
            elif ".mp3" in line:
                link_pattern = re.compile(r".*\[(.*?)\]\((.*?)\)$")
                match = link_pattern.match(line)

                title = match.group(1)
                current_title = title
                label = make_log_label(title)

                raw_link = match.group(2)

                mp3_link = raw_link.replace("%20", " ")
                mdfile = mp3_to_title(mp3_link) + ".md"
                mdlink = mdfile.replace(" ", "%20")

                metadata[current_title] = {
                    "mp3": mp3_link,
                    "markdown": os.path.join(input_directory, mdfile),
                    "text": os.path.join(input_directory, f"{title}.txt"),
                    "label": label,
                }

                line = line.replace(raw_link, mdlink)
            elif "Teacher:" in line:
                match = bullet_pattern.match(line)
                meta = match.group(1)
                teacher = meta.replace("Teacher: ", "")
                info = metadata[current_title]
                info["teacher"] = teacher
                metadata[current_title] = info
            elif "Date:" in line:
                match = bullet_pattern.match(line)
                meta = match.group(1)
                date = meta.replace("Date: ", "")
                info = metadata[current_title]
                info["date"] = date
                metadata[current_title] = info
            mdlines.append(line)

        readme_contents = "\n".join(mdlines)
        # rewrite
        with open(readme_file, "w") as file:
            file.write(readme_contents)
    elif ".mp3" in input_file:
        title = mp3_to_title(input_file)
        meta = metadata_from_mp3(input_file)
        dirname = os.path.dirname(input_file)
        meta["markdown"] = os.path.join(dirname, f"{title}.md")
        metadata[title] = meta

    print(json.dumps(metadata, indent=4))

    if len(input_files) == 0:
        print("no files to transcribe")
        exit(1)

    # transcribe and correct text concurrently
    transcribe_executor = ThreadPoolExecutor(max_workers=10)
    transcribe_futures: dict[Future, str] = {}
    correct_executor = ThreadPoolExecutor(max_workers=10)
    correct_futures: dict[Future, str] = {}

    # process files in the expected order
    input_files = list(sorted(input_files, key=extract_prefix_from_file))

    for input_path in input_files:
        title = os.path.basename(input_path)
        title, _ = os.path.splitext(title)
        log_label = f"[{title}]"

        # set outputs and assume that outputs should be placed next to
        # their inputs
        txtfile: str = None
        is_txt = False
        if ".mp3" in input_path:
            txtfile = input_path.replace(".mp3", ".txt")
        elif ".txt" in input_path:
            is_txt = True
            txtfile = input_path
        else:
            print(f"{log_label} unsupported file given {input_path}")
            exit(1)

        # get raw transcription
        transcription: str = None
        if is_txt:
            # restore previously prepared transcription
            print(f"{log_label} reading text file {input_path}")
            future = transcribe_executor.submit(
                read_file,
                input_path,
            )
            transcribe_futures[future] = title
        else:
            # create new transcription usind whisper
            print(f"{log_label} transcribing audio file")
            future = transcribe_executor.submit(
                transcribe_audio,
                client,
                input_path=input_path,
            )
            transcribe_futures[future] = title

    for future in as_completed(transcribe_futures):
        title = transcribe_futures[future]
        meta = metadata[title]
        log_label = make_log_label(title)
        try:
            meta = metadata[title]
            txtfile = meta.get("text")
            transcription = future.result()
            try:
                # write text file
                print(f"{log_label} writing text transcription to {txtfile}")
                with open(txtfile, "w") as file:
                    file.write(transcription)
            except Exception as we:
                print(f"transcription write error: {we}")

            # prepare corrected markdown file
            future = correct_executor.submit(
                correct_transcript, client, log_label, transcription, model
            )
            correct_futures[future] = title
        except Exception as e:
            title = meta.get("title")
            print(f"failed to create transcription '{title}': {e}")

    for future in as_completed(correct_futures):
        title = correct_futures[future]
        try:
            meta = metadata[title]
            mdfile = meta.get("markdown")
            text = future.result()
            try:
                # write corrected markdown transcription
                print(f"{log_label} writing markdown transcription to {mdfile}")
                write_markdown(text, title, meta, mdfile)
            except Exception as we:
                print(f"transcription write error: {we}")
        except Exception as e:
            title = meta.get("title")
            print(f"failed to correct transcription '{title}': {e}")


def make_log_label(filepath: str) -> str:
    file_num = extract_prefix_from_file(filepath)
    title = extract_title_from_file(filepath)
    return f"[{file_num}. {title}]"


def read_file(filename: str) -> str:
    with open(filename) as file:
        return file.read()


def write_markdown(text: str, title: str, metadata: dict[str, str], filename: str):
    teacher = metadata["teacher"]
    date = metadata["date"]

    md = [f"# {title}\n\n"]
    md.append(f"*{teacher} - {date}*\n\n\n")
    md.append(text)
    content = "".join(md)

    with open(filename, "w") as file:
        file.write(content)


def download_mp3(url: str, output_file: str):
    print(f"downloading mp3 from {url}")
    response = requests.get(url)
    if response.status_code == 200:
        with open(output_file, "wb") as file:
            file.write(response.content)
        print(f"Download complete. The MP3 file has been saved as '{output_file}'.")
    else:
        print(f"Failed to download the file. HTTP status code: {response.status_code}")


def parse_retreat_metadata(base_url: str, page_url: str) -> dict[str, str]:
    response = requests.get(page_url)
    response.raise_for_status()  # Will raise an exception if the HTTP request
    soup = BeautifulSoup(response.text, "html.parser")
    table_data = soup.find_all("td", attrs={"colspan": "2"})

    date_pattern = re.compile(r"\b(19|20)\d{2}-([0-1][0-9])-([0-3][0-9])\b")
    date_info_pattern = re.compile(r"(.*) \((.*?)\)")

    title: str = None
    date: str = None
    duration: str = None
    location: str = None
    for data in table_data:
        if title and date and location:
            break

        contents = data.text.strip()
        if contents != "" and date_pattern.search(contents):
            # retreat info is in the first <td> containing a date after
            # the title
            info = contents.split("\n")
            if len(info) > 0:
                match = date_info_pattern.search(info[0].strip())
                if match:
                    date = match.group(1)
                    duration = match.group(2)
                location = info[-1].strip()

        for child in data.children:
            if getattr(child, "name", None) == "h2":
                title = child.text.strip()

    return {
        "title": title,
        "date": date,
        "duration": duration,
        "location": location,
    }


def parse_retreat_talks(
    base_url: str, page_url: str, talk_counter: int = 1
) -> dict[str, str]:
    response = requests.get(page_url)
    response.raise_for_status()  # Will raise an exception if the HTTP request returned an unsuccessful status code
    soup = BeautifulSoup(response.text, "html.parser")
    anchors = soup.find_all("a")
    raw_page_url = urlparse(page_url)
    base_page_url = f"{raw_page_url.scheme}://{raw_page_url.netloc}{raw_page_url.path}"

    talks: dict[str, dict[str, str]] = {}

    talk_title: str = None
    talk_teacher: str = None
    talk_mp3: str = None
    talk_date: str = None

    next_counter = 0
    next_url: str = None

    for anchor in anchors:
        a_class = anchor.get("class")
        link = anchor.get("href")
        link_text = anchor.text.strip()

        if a_class and ("talkteacher" in a_class and "/teacher" in link):
            talk_teacher = link_text
        if a_class and ("talkteacher" in a_class and "/talks" in link):
            talk_date = anchor.parent.text.strip().split("\n")[0].strip()
            talk_title = f"{talk_counter}. {link_text}"
        if ".mp3" in link:
            talk_mp3 = base_url + link
        if talk_title and talk_teacher and talk_mp3 and talk_date:
            talks[talk_title] = {
                "teacher": talk_teacher,
                "date": talk_date,
                "mp3": talk_mp3,
            }
            talk_title = None
            talk_teacher = None
            talk_mp3 = None
            talk_counter += 1
        if "next ››" in link_text:
            if next_counter > 0:
                next_url = base_page_url + link
            next_counter += 1

    if next_url:
        next_talks = parse_retreat_talks(
            base_url=base_url, page_url=next_url, talk_counter=talk_counter
        )
        talks = {**next_talks, **talks}
        return talks

    return talks


def pad_prefix(talks: dict[str, dict[str, str]]) -> dict[str, str]:
    new_talks: dict[str, str] = {}

    # sort first
    talks = {
        key: talks[key] for key in sorted(talks.keys(), key=extract_prefix_from_title)
    }
    # find the last talk
    max_key = list(talks)[-1]
    max_prefix_len = len(str(extract_prefix_from_title(max_key)))
    for title in talks:
        new_title = remove_prefix_from_title(title)
        prefix = str(extract_prefix_from_title(title))
        padding = max_prefix_len - len(prefix)
        # left pad with zeroes
        if padding > 0:
            prefix = (padding * "0") + prefix
        new_title = f"{prefix}. {new_title}"
        new_talks[new_title] = talks[title]
    return new_talks


def download_retreat(retreat_url: str, output_dir: str):
    url = urlparse(retreat_url)
    page_url = url.geturl()
    base_url = f"{url.scheme}://{url.netloc}"

    metadata = parse_retreat_metadata(base_url, page_url)
    title = metadata["title"]

    index_file = [f"# {title}\n\n"]
    index_file.append(f"- **Retreat Page**: [Link]({page_url})\n")
    for k, v in metadata.items():
        if k == "title":
            continue
        index_file.append(f"- **{k.capitalize()}**: {v}\n")
    index_file.append("\n")

    talks = parse_retreat_talks(base_url, page_url)
    talks = pad_prefix(talks)

    index_file.append("## Talks\n\n")
    mp3s: dict[str, str] = {}
    for title, info in talks.items():
        teacher = info["teacher"]
        date = info["date"]

        # prepare mp3 metadata for download
        file_name = title.replace(". ", f". [{teacher} - {date}] ") + ".mp3"
        file_path = os.path.join(output_dir, file_name)
        mp3s[file_path] = info["mp3"]

        # update index file
        file_link = file_name.replace(" ", "%20")
        index_file.append(f"- [{title}](./{file_link})\n")
        index_file.append(f"  - Teacher: {teacher}\n")
        index_file.append(f"  - Date: {date}\n")
    index_contents = "".join(index_file)

    executor = ThreadPoolExecutor(max_workers=4)
    futures: dict[Future, dict[str, str]] = {}
    for file_path, mp3_url in mp3s.items():
        if os.path.exists(file_path):
            print(f"skipping file {file_path} because it has already been downloaded")
            continue
        future = executor.submit(download_mp3, mp3_url, file_path)
        futures[future] = {
            "url": mp3_url,
            "file": file_path,
        }

    for future in as_completed(futures):
        args = futures[future]
        try:
            future.result()
        except Exception as e:
            url = args.get("url")
            print(f"could not download audio file {url}: {e}")

    # write index file
    mdfile = os.path.join(output_dir, "README.md")
    with open(mdfile, "w") as file:
        file.write(index_contents)


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


def extract_readme_title(contents: str) -> str:
    lines = contents.split("\n")
    return lines[0].replace("#", "").strip()


def extract_readme_metadata(contents: str) -> dict[str, str]:
    lines = contents.split("\n")
    lines = lines[1:]

    end = 0
    for i, line in enumerate(lines):
        if line.startswith("#"):
            break
        end = i

    lines = lines[:end]
    lines = [line for line in lines if len(line) > 0]

    metadata: dict[str, str] = {}
    for line in lines:
        meta = line.split(": ")
        metadata[meta[0].replace("*", "").replace("- ", "").lower()] = meta[1]

    return metadata


def extract_markdown_link(string: str) -> dict[str, str]:
    link_pattern = re.compile(r".*\[(.*?)\]\((.*?)\)$")
    match = link_pattern.match(string)
    if not match:
        return None

    return {
        "title": match.group(1),
        "link": match.group(2),
    }


# TODO: remove
def extract_readme_talks(contents: str, output_dir: str) -> dict[str, str]:
    contents = contents.split("## Talks")[1]
    talks = contents.split("\n")
    talks = [talk for talk in talks if len(talk) > 0]
    talks = [re.sub("^- ", "", talk) for talk in talks]
    link_pattern = re.compile(r".*\[(.*?)\]\((.*?)\)$")

    files: dict[str, str] = {}
    for talk in talks:
        if not ".md" in talk:
            continue
        match = link_pattern.match(talk)
        title = match.group(1)
        file_path = match.group(2).replace("%20", " ").replace("./", "")
        file_path = os.path.join(output_dir, file_path)
        files[title] = file_path
    return files


def pdf(args: argparse.Namespace):
    directory = args.directory
    if not os.path.exists(directory):
        print(f"{directory} does not exist")
        exit(1)

    mdfile = os.path.join(directory, "README.md")
    if not os.path.exists(mdfile):
        print(f"required {mdfile} file does not exist")
        exit(1)

    mdcontents: str = None
    with open(mdfile, "r") as file:
        mdcontents = file.read()

    retreat_title = extract_readme_title(mdcontents)
    metadata = extract_readme_metadata(mdcontents)

    talks = metadata_from_readme(mdcontents, directory)

    date = metadata["date"]
    location = metadata["location"]
    duration = metadata["duration"]

    retreat_page = extract_markdown_link(metadata["retreat page"])
    retreat_page_link = retreat_page.get("link")

    teachers = set()
    for _, meta in talks.items():
        teacher = meta["teacher"]
        teachers.add(teacher)
    teachers_str = ", ".join(teachers)

    combined_md = f"""
---
title: "{retreat_title}"
author: "{teachers_str}"
date: "{date}"
---

\\begin{{center}}
\\href{{{retreat_page_link}}}{{{location} ({duration})}}
\\end{{center}}

\\newpage

\\tableofcontents

\\newpage
"""

    for _, meta in talks.items():
        file_path = meta["markdown"]
        with open(file_path, "r") as file:
            combined_md += file.read() + "\\newpage\n\n"

    output_pdf = os.path.join(directory, f"{retreat_title}.pdf")
    pypandoc.convert_text(
        source=combined_md,
        outputfile=output_pdf,
        to="pdf",
        format="md",
        extra_args=[
            "--pdf-engine=xelatex",  # use latex engine
            "-V",
            "fontsize=12pt",
        ],
    )


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

    #
    # book
    #
    make_parser = subparsers.add_parser(
        "make", help="use the transcriptions for some other output"
    )
    make_parser = make_parser.add_subparsers(dest="subcommand", help="sub-command help")
    pdf_parser = make_parser.add_parser(
        "pdf", help="convert markdown transcriptions to a pdf"
    )
    pdf_parser.add_argument(
        "directory",
        type=str,
        help="The directory containing the markdown transcripts",
    )
    pdf_parser.set_defaults(func=pdf)

    # execute the function associated with the chosen subcommand
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
