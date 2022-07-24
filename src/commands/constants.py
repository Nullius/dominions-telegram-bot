# lookup https://www.illwinter.com/dom5/techmanual.html

NEWGAME_DEFAULT = (
  '-ST', # Start TCP server, text only
  '--nosteam', # Do not connect to steam
  '--statusdump', # Continuously create info on players in a parsable format
  '--noclientstart', # Clients cannot start the game during Choose Participants
)

NEW_GAME_REQUIRED = (
  ('port', ''),
  ('mapfile', ''),
  ('masterpass', ''),

  ('era', '2'),
  ('uploadmaxp', '8'), # Game is created if this many players join
  ('hours', '24'),
  ('thrones', '0 0 8'),
  ('requiredap', '20'),
)

OPTIONAL = (
  ('--norandres', True),
  ('--eventrarity', '1')
)