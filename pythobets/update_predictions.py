import os
import csv
from datetime import datetime

USER_DATA_PATH = os.path.join(os.getenv("HOME"), ".pythobets")
USER_CONFIG_PATH = os.path.join(USER_DATA_PATH, 'config.ini')
JSON_ODDS = os.path.join(USER_DATA_PATH, 'odds.json')

#TODO add a sport variable that is passed to this function
# Predictions that are run should depend on which sport was passed
def load_predictions():
    odds = []
    todays_odds = []
    SOCCER_ODDS = os.path.join(
        USER_DATA_PATH, 'soccer-spi', 'spi_matches_latest.csv')
    with open(SOCCER_ODDS, newline='') as csvfile:
        prediction_reader = csv.reader(csvfile, delimiter=',')
        for row in prediction_reader:
            odds.append(datetime.strptime(row[1],"%Y-%m-%d") )
            # odds.append(row[1])
    # print(datetime.strptime(odds[1], "%Y-%m-%d"))
    print(odds)


def main():
    load_predictions()


if __name__ == "__main__":
    main()
