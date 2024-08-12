import datetime
import attrs
import typed_settings as ts


@attrs.frozen
class NotionConfig:
    # Integragration token for Notion API.
    token: str = ""
    
    # ID of the page, containing main database for recordings.
    # TODO: document initial setup
    database_id: str = ""

    # Notion API version to use.
    version: str = "2022-06-28"

    # Base URL for all requests.
    base_url: str = "https://api.notion.com/v1"


@attrs.frozen
class WhisperConfig:
    # Whisper model name, e.g. "tiny" or "large". Consult whisper docs for options.
    model: str = "large"

    # Recording language. Seems irrelevant for "large" model.
    language: str = "Russian"


@attrs.frozen
class PathsConfig:
    # Path to the folder with voice memos.
    voice_memos_root: str = "/Recordings"


@attrs.frozen
class ServiceConfig:
    # Delay between two consecutive processing attempts.
    sleep_interval: datetime.timedelta = datetime.timedelta(minutes=5)


@attrs.frozen
class Config:
    notion: NotionConfig
    paths: PathsConfig
    service: ServiceConfig
    whisper: WhisperConfig

    @classmethod
    def new(cls) -> 'Config':
        return ts.load(
            cls=cls,
            appname="landline",
            config_files=(
                ts.find("config.toml"),
            ),
        )
