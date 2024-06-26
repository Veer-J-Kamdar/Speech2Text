from typing import Final
import os

# Service Configuration
CLASS_MODEL: Final[str] = "Speech-to-Text"
ENGINE: Final[str] = "speech_recognition"
LANGUAGE: Final[str] = "th"

# File Paths
BASE_DIR: Final[str] = os.path.dirname(os.path.abspath(__file__))
PATH_MP3: Final[str] = os.path.join(BASE_DIR, "temp", "sound")
PATH_JSON: Final[str] = os.path.join(BASE_DIR, "temp", "json")

# Server Configuration
HOST: Final[str] = "localhost"
PORT: Final[int] = 3000
BASE_URL: Final[str] = f"http://{HOST}:{PORT}/static/"

# Ensure directories exist
for path in [PATH_MP3, PATH_JSON]:
    os.makedirs(path, exist_ok=True)

# Optional: Environment variable overrides
ENGINE = os.environ.get("STT_ENGINE", ENGINE)
LANGUAGE = os.environ.get("STT_LANGUAGE", LANGUAGE)
HOST = os.environ.get("STT_HOST", HOST)
PORT = int(os.environ.get("STT_PORT", PORT))

# Validate configuration
assert ENGINE in ["speech_recognition"], f"Unsupported engine: {ENGINE}"
assert LANGUAGE, "Language must be specified"
assert 1 <= PORT <= 65535, f"Invalid port number: {PORT}"