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
def update_predictions(sports = 'all'):
    print("Updating Predictions")
    if not os.path.isdir(USER_DATA_PATH):
        os.makedirs(USER_DATA_PATH)
    urls = {'nfl': 'https://projects.fivethirtyeight.com/data-webpage-data/datasets/nfl-elo.zip', 'nba': 'https://projects.fivethirtyeight.com/data-webpage-data/datasets/nba-forecasts.zip',
            'soccer': 'https://projects.fivethirtyeight.com/data-webpage-data/datasets/soccer-spi.zip', 'nhl': 'https://projects.fivethirtyeight.com/data-webpage-data/datasets/nhl-forecasts.zip'}
    if sports == 'all':
        for url in urls.values():
            current_url = url
            filename = current_url.split('/')[-1]
            print(f"Download Starting for {filename}") 
            try:
                req=requests.get(current_url)
            except: 
                print(f"{filename} failed to download, continuing")
                continue   
            zipped_predictions = zipfile.ZipFile(BytesIO(req.content))
            zipped_predictions.extractall(USER_DATA_PATH)
    print("Succesfully Updated Predictions")
    print("Please support https://fivethirtyeight.com/ if possible as they provide this data.")


@app.command()
def configure(the_odds_API_key: str, betmaker: str, bankroll:int,  predictions = ['all'], staking_strategy = 'kelly-criterion'):
    """
    
    """
    configuration.ensure_config_directories()
    
    print(betmaker)
    print(the_odds_API_key)

@app.command()
def determine_upcoming_bets():
    '''
    Handles the automated bet selection process.
    '''

    

if __name__ == "__main__":
    app()