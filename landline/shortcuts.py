from landline.config import *
from landline.notion import *
from landline.transcribe import *

cfg = Config.new()
notion = NotionController(cfg)
transcriber = Processor(cfg, notion)
