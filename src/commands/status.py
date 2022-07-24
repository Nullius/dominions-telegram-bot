import re
import configparser
import subprocess
import shlex

from helpers.games import load 
from helpers.getGamePath import getGamePath

def status(name: str):
  gamePath = getGamePath(name)

  if not gamePath.exists():
    return {
      'status': 'Не создана',
      'undone': '',
      'timer': '',
    }

  ''' Get undone'''
  statusDump = gamePath / 'statusdump.txt'

  if not statusDump.exists():
      raise ValueError('Статусдамп отсутствует')
        
  with open(statusDump) as handler:
      lines = handler.readlines()
 
  title = lines.pop(0)
  turnInfo = lines.pop(0).split(',')
  turn = turnInfo[0]

  undone = lines = [parseUndone(line) for line in lines]
  undone= [line for line in lines if line != None]
  undone.insert(0, turn)

  '''Get timer'''
  game = load(name)
  port = game['port']
  timer = getTimer(port)

  return {
    'status': 'STARTED',
    'undone': undone,
    'timer': timer,
  }


def parseUndone(line: str) -> str:
    line = re.split(r'\s+', line)
    player = line[3]
    status = line[5]
    nation = line[7]

    print(line)
    print(player)
    print(status) 

    if player == '1':
      if status == '0':
          return '{} has not played its turn'.format(nation)

      if status == '1':
          return '{} unfinished'.format(nation)

    return None

def getTimer(port):
    config = configparser.ConfigParser()
    config.read('config.ini')
    bin_path = config['DEFAULT']['bin_path']
    ip = config['DEFAULT']['ip']

    cmd = '{bin} --tcpquery --nosteam --ipadr {ip} --port {port}'.format(
        bin = bin_path,
        ip = ip,
        port = port,
    )
    args = shlex.split(cmd)
    mask = r'Time left: (\d+) ms'

    try:
        result = subprocess.run(args, stdout=subprocess.PIPE)
        time = re.search(mask, str(result)).group(1)
        timeMinutes = int(int(time)/(1000*60))
        timeHours = int(int(time)/(1000*60*60))
        if (timeHours < 0):
            return 'Осталось {} минутов'.format(timeMinutes)
        else:
            return 'Осталось {} часов'.format(timeHours)
    except ValueError as e:
      return e
