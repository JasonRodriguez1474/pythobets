import requests
import zipfile
import os
import os.path
from io import BytesIO
import configparser

USER_DATA_PATH = os.path.join(os.getenv("HOME"), ".pythobets")
USER_CONFIG_PATH = os.path.join(USER_DATA_PATH, 'config.ini')

def update_predictions(sports='all'):
    print("Updating Predictions")
    urls = {'nfl': 'https://projects.fivethirtyeight.com/data-webpage-data/datasets/nfl-elo.zip', 'nba': 'https://projects.fivethirtyeight.com/data-webpage-data/datasets/nba-forecasts.zip',
            'soccer': 'https://projects.fivethirtyeight.com/data-webpage-data/datasets/soccer-spi.zip', 'nhl': 'https://projects.fivethirtyeight.com/data-webpage-data/datasets/nhl-forecasts.zip'}
    if sports == 'all':
        for url in urls.values():
            current_url = url
            filename = current_url.split('/')[-1]
            print(f"Download Starting for {filename}")
            try:
                req = requests.get(current_url)
            except:
                print(f"{filename} failed to download, continuing")
                continue
            zipped_predictions = zipfile.ZipFile(BytesIO(req.content))
            zipped_predictions.extractall(USER_DATA_PATH)
    print("Succesfully Updated Predictions")
    print("Please support https://fivethirtyeight.com/ if possible as they provide this data.")


def initiate_config():
    config = configparser.ConfigParser()
    config['DEFAULT']= {'Sports': 'All'}
    config['the-odds-api.com'] = {'api-key':''}
    with open (USER_CONFIG_PATH, 'w') as config_file:
        config.write(config_file)

def main():
    if not os.path.isdir(USER_DATA_PATH):
        os.makedirs(USER_DATA_PATH)
    if not os.path.isfile(USER_CONFIG_PATH):
        initiate_config()
    # Turn on when you actually want to update_predictions
    # TODO add logic to automatically only do this if 8hrs has passed since last run
    # Add a last updated entry to the users config file
    # update_predictions()
    initiate_config()


if __name__ == "__main__":
    main()
