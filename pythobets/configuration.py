import typer
from pathlib import Path
import os

APP_NAME = "pythobets"
APP_DIR = typer.get_app_dir(APP_NAME)

def configure_config():
    config_path: Path = Path(APP_DIR) / "config.json"
    if not config_path.is_file():
        print(f"Config file doesn't exist yet, try running configure")


def ensure_config_directories():
    if not os.path.exists(os.path.dirname(APP_DIR)):
        os.makedirs(os.path.dirname(APP_DIR))  
        print(f"Your config directory didn't exist, so we created it for you at {APP_DIR}")

def main():
    # recursively create directories if necessary
    config_path: Path = Path(APP_DIR) / "config.json"
    if not config_path.is_file():
        print(f"Config file doesn't exist yet, try running configure")


if __name__ == "__main__":
    typer.run(main)