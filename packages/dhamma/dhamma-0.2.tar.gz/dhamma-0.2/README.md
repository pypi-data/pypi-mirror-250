# Dhamma

[Dharma Seed](https://dharmaseed.org/) is an indespensible resource for those on the Buddhist path. However, sometimes it can be challenging to commit to sitting and listening to many hours of talks when reading the content would be preferred. The `dhamma` ("dharma" in Pāḷi) tool in this project enables you to do exactly that.

The tool works by scraping a retreat page ([dharmaseed.org/retreats/3972](https://dharmaseed.org/retreats/3972) for example), downloading the mp3 files hosted there, and then using the OpenAI Whisper and Chat APIs to transcribe, cleanup, and prepare markdown documents for easy reading anywhere. Facilities for converting these markdown documents into pdfs or epub documents are also included with this tool.

## Installation

```sh
pip install dhamma
```

## Example Usage

```sh
$ dhamma download retreat 3972 -o ./Soulmaking
$ dhamma transcribe ./Soulmaking
```
