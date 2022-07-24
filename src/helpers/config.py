import configparser

config = configparser.ConfigParser()
config.read('config.ini')

ip: str = config['DEFAULT']['ip']
gamePath: str = config['DEFAULT']['gamePath']
gameData: str = config['DEFAULT']['gameData']
binPath: str = config['DEFAULT']['bin_path']
