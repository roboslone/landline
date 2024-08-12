import datetime
import functools
import logging
import os
import pathlib
import time
import whisper

from landline.config import Config
from landline.notion import NotionController


class Processor:
    logger = logging.getLogger("processor")

    def __init__(self, cfg: Config, notion: NotionController, whisper: whisper.Whisper) -> None:
        self.cfg = cfg
        self.notion = notion
        self.whisper = whisper

    @functools.cached_property
    def voice_memos_root(self) -> pathlib.Path:
        return pathlib.Path(self.cfg.paths.voice_memos_root)

    def run_once(self):
        self.logger.info("fetching existing recordings from Notion...")
        existing = set()
        for r in self.notion.records():
            existing.add(r['properties']['File']['rich_text'][0]['text']['content'])
        self.logger.info(f"got {len(existing)} existing recordings, processing new ones...")

        # Next, iterate over recordings in iCloud and process new ones.
        self.logger.info("processing records:")
        count = 0
        for f in sorted(self.voice_memos_root.glob("*.m4a")):
            if f.name in existing:
                self.logger.info(f"\t{f.name}: already processed")
                continue

            self.logger.info(f"\t{f.name}: processing")
            
            result = self.whisper.transcribe(str(f), fp16=False, language=self.cfg.whisper.language)
            page = self.notion.insert(f.name, datetime.datetime.fromtimestamp(f.stat().st_mtime), f, result["text"])
            self.logger.info(f"\t{f.name}: successfully uploaded: {page["id"]}")
            count += 1

        if count:
            self.logger.info(f"uploaded {count} new recording(s)")

    def run(self):
        self.logger.info("starting processor...")

        while True:
            try:
                self.run_once()
            except (KeyboardInterrupt, SystemExit):
                self.logger.info("exiting...")
                break

            try:
                time.sleep(self.cfg.service.sleep_interval.total_seconds())
            except (KeyboardInterrupt, SystemExit):
                self.logger.info("exiting...")
                break

# voiceMemoFolder = f"/Users/{username}"
# print("reading voice memos from", voiceMemoFolder)

# outputFolder = f"/Users/{username}/Library/Mobile Documents/com~apple~CloudDocs/Recordings"
# print("loading model")
# model = whisper.load_model("large")
# print("model loaded")

# files = list(filter(lambda x: x.endswith(('.m4a')), sorted(os.listdir(voiceMemoFolder))))
# masterTranscription = ""

# for index, file in enumerate(files):
#     inputFile = os.path.join(voiceMemoFolder, file)
#     print(f"[{index+1}/{len(files)}] {inputFile}: processing")

#     fileName = os.path.splitext(file)[0];
#     outputFile = os.path.join(outputFolder, f"{fileName}.json")
#     if os.path.isfile(outputFile):
#         print(f"[{index+1}/{len(files)}] transcription exists, grabbing text")
#         with open(outputFile) as textfile:
#             masterTranscription += processTranscript(textfile.read())
#         continue

#     print(f"[{index+1}/{len(files)}] {inputFile}: transcribing")
#     result = model.transcribe(inputFile, fp16=False, language='Russian')
#     masterTranscription += processTranscript(result["text"])

#     print(f"[{index+1}/{len(files)}] {inputFile}: writing: {outputFile}")
#     with open(outputFile, 'w') as f:
#         json.dump(result, f)

#     print(f"[{index+1}/{len(files)}] {inputFile}: complete")

# print("all files complete, outputting master transcription")
# masterFile = os.path.join(outputFolder, 'master_transcription.txt')
# with open(masterFile, 'w') as f:
#     f.write(masterTranscription)
