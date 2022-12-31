import requests
import zipfile
import os
import os.path
from io import BytesIO
import configparser
import json

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

def update_betmaker_odds(api_key):
    SPORT = 'upcoming'  # use the sport_key from the /sports endpoint below, or use 'upcoming' to see the next 8 games across all sports

    REGIONS = 'us'  # uk | us | eu | au. Multiple can be specified if comma delimited

    # h2h | spreads | totals. Multiple can be specified if comma delimited
    MARKETS = 'h2h,spreads'

    ODDS_FORMAT = 'decimal'  # decimal | american

    DATE_FORMAT = 'iso'  # iso | unix

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    # First get a list of in-season sports
    #   The sport 'key' from the response can be used to get odds in the next request
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    sports_response = requests.get(
        'https://api.the-odds-api.com/v4/sports',
        params={
            'api_key': api_key
        }
    )

    if sports_response.status_code != 200:
        print(
            f'Failed to get sports: status_code {sports_response.status_code}, response body {sports_response.text}')

    else:
        print('List of in season sports:', sports_response.json())


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    # Now get a list of live & upcoming games for the sport you want, along with odds for different bookmakers
    # This will deduct from the usage quota
    # The usage quota cost = [number of markets specified] x [number of regions specified]
    # For examples of usage quota costs, see https://the-odds-api.com/liveapi/guides/v4/#usage-quota-costs
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    odds_response = requests.get(
        f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds',
        params={
            'api_key': api_key,
            'regions': REGIONS,
            'markets': MARKETS,
            'oddsFormat': ODDS_FORMAT,
            'dateFormat': DATE_FORMAT,
        }
    )

    if odds_response.status_code != 200:
        print(
            f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')

    else:
        odds_json = odds_response.json()
        json_odds = json.dumps(odds_json, indent=4)
        with open (os.path.join(USER_DATA_PATH, 'odds.json'), 'w') as json_odds:
            json_odds.write(json_odds)
            
        # Check the usage quota
        print('Remaining requests', odds_response.headers['x-requests-remaining'])
        print('Used requests', odds_response.headers['x-requests-used'])



def main():
    if not os.path.isdir(USER_DATA_PATH):
        os.makedirs(USER_DATA_PATH)
        update_predictions()
    if not os.path.isfile(USER_CONFIG_PATH):
        initiate_config()
    # Turn on when you actually want to update_predictions
    # TODO add logic to automatically only do this if 8hrs has passed since last run
    # Add a last updated entry to the users config file
    # update_predictions()
    # Begins reading config file
    config = configparser.ConfigParser()
    config.read(USER_CONFIG_PATH)
    update_betmaker_odds(config['the-odds-api.com']['api-key'])


if __name__ == "__main__":
    main()
