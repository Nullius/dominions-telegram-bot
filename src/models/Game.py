"""
Game creation, storing, loading and running

game itself is just a json dictionary where game name is a key and list of options is a value
"""

import json
import shlex
import subprocess

from helpers import config

GameListType = dict[str, str]
defaultArgs = '-ST --nosteam --statusdump --noclientstart'

def load() -> GameListType: 
    with open(config.gameData, 'r') as dataFile:
        gameList = json.load(dataFile)
    return gameList

def create(name: str, args: str) -> None:
    gameList = load()
    gameList[name] = args
    with open(config.gameData, 'w') as dataFile:
        gameList = json.dump(gameList, dataFile)

def remove(name: str) -> None:
    gameList = load()
    del gameList[name]
    with open(config.gameData, 'w') as dataFile:
        gameList = json.dump(gameList, dataFile)

def run(name: str, args: str) -> None:
    cmd = ' '.join([
        config.binPath,
        defaultArgs,
        '--ipadr {}'.format(config.ip),
        args,
        name,
    ])

    subprocess.run(shlex.split(cmd))
