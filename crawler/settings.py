from pathlib import Path

from .helpers import required_env

PROJECT_ROOT = Path(__file__).parent.parent

TWITTER_CLIENT_ID = required_env("TWITTER_CLIENT_ID")

TWITTER_CLIENT_SECRET = required_env("TWITTER_CLIENT_SECRET")
