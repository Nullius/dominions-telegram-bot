import configparser
import json

def gamelist():
    config = configparser.ConfigParser()
    config.read('config.ini')
    with open(config['DEFAULT']['gameData'], 'r') as data:
        games = json.load(data)
    games = [game['name'] for game in games]
    return games
