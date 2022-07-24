from helpers.getGamePath import getGamePath

def settimer(game_name, turnTimer):
    gamePath = getGamePath(game_name)
    if not gamePath.exists():
        raise ValueError('Игры не существует')

    if turnTimer <= 0:
        raise ValueError('Таймер должен быть больше нуля')

    domcmd = gamePath / 'domcmd'
    with open(domcmd, 'w') as handler:
        handler.write("settimeleft {}".format(str(60*60*turnTimer)))