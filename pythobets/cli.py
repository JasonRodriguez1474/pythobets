import click
import os
import configparser

APP_NAME = "pythobets"
APP_DIR = click.get_app_dir(APP_NAME)

@click.group()
def cli():
  pass

@cli.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo(f"Hello {name}!")


@cli.command()
@click.option('--sports', '-s', default=['all'], help="Which sports you'd like to update, defaults to all, but can be limited to nba, nfl, soccer, or nhl", multiple=True)
def update_predictions(sports):
    """Command to update the latest sports analysts predictions."""
    print(sports)
    for i in sports:
        print(i)

if __name__ == '__main__':
    cli()