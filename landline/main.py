import sys
sys.path.insert(0, '.')

import argparse
import logging
import whisper

from landline.config import Config
from landline.notion import NotionController
from landline.process import Processor


def main():
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(prog="landline")
    parser.add_argument("--preload-only", action="store_true", help="Download Whisper model and exit")
    args = parser.parse_args()

    cfg = Config.new()
    logging.info(f"loading Whisper model: {cfg.whisper.model} (language = {cfg.whisper.language})")
    model = whisper.load_model(cfg.whisper.model)

    if args.preload_only:
        return

    if not cfg.notion.database_id:
        # TODO: suggest initial setup & exit
        print("TODO: database not set up")
        exit(1)

    notion = NotionController(cfg)
    processor = Processor(cfg, notion, model)
    processor.run()


if __name__ == '__main__':
    main()
