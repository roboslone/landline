import datetime
import functools
import logging
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

    def fetch_existing(self) -> set:
        self.logger.info("fetching existing recordings from Notion...")
        existing = set()
        for r in self.notion.records():
            existing.add(r['properties']['File']['rich_text'][0]['text']['content'])
        self.logger.info(f"got {len(existing)} existing recordings")
        return existing

    """
    Returns a set of newly uploaded records IDs.
    """
    def run_once(self, existing: set):
        # Next, iterate over recordings in iCloud and process new ones.
        for f in sorted(self.voice_memos_root.glob("*.m4a")):
            if f.name in existing:
                self.logger.debug(f"\t{f.name}: already processed")
                continue

            self.logger.info(f"\t{f.name}: processing")
            
            result = self.whisper.transcribe(str(f), fp16=False, language=self.cfg.whisper.language)
            id = self.notion.insert(f.name, datetime.datetime.fromtimestamp(f.stat().st_mtime), f, result["text"])
            self.logger.info(f"\t{f.name}: successfully uploaded: {id}")
            yield id

    def run(self):
        self.logger.info("starting processor...")
        existing = self.fetch_existing()

        while True:
            try:
                count = 0
                for id in self.run_once(existing):
                    count += 1
                    existing.add(id)
                if count:
                    self.logger.info(f"processed {count} new recording(s)")

            except (KeyboardInterrupt, SystemExit):
                self.logger.info("exiting...")
                break

            try:
                time.sleep(self.cfg.service.sleep_interval.total_seconds())
            except (KeyboardInterrupt, SystemExit):
                self.logger.info("exiting...")
                break
