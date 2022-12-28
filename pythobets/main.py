"""An amazing betting analysis!"""

__version__ = "0.1"

import typer
import requests, zipfile
import os, os.path
from io import BytesIO
import configuration

USER_DATA_PATH = os.path.join(os.getenv("HOME"), ".pythobets")

app = typer.Typer()


@app.command()
def update_clubsoccer_predictions():
    print("Updating Club Soccer Predictions")
    url = "https://projects.fivethirtyeight.com/data-webpage-data/datasets/soccer-spi.zip"
    if not os.path.isdir(USER_DATA_PATH):
        os.makedirs(USER_DATA_PATH)
    print("Downloading Started")    
    req = requests.get(url)
    print("Downloading Completed")
    filename = url.split('/')[-1]
    zipped_predictions = zipfile.ZipFile(BytesIO(req.content))
    zipped_predictions.extractall(USER_DATA_PATH)
    print("Succesfully Updated Club Soccer Predictions")
    print("Please support https://fivethirtyeight.com/ if possible as they provide this data.")


@app.command()
def configure(api_key: str, betmaker: str, bankroll:int,  predictions = ['all'], staking_strategy = 'kelly-criterion'):
    """
    
    """
    configuration.ensure_config_directories
    
    print(betmaker)
    print(api_key)
    


if __name__ == "__main__":
    app()