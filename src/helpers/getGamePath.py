from pathlib import Path

'''TODO path from config'''
def getGamePath(name: str) -> Path:
  savesDir = Path('/home/nullius/dominions5/savedgames')
  return savesDir / name