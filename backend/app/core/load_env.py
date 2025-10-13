from pathlib import Path
from dotenv import load_dotenv

def load():
    env_path = Path(__file__).resolve().parents[2] / "backend" / ".env"
    load_dotenv(dotenv_path=env_path, encoding="utf-8")
