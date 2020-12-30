from recording_reactor import recording_player
from reactor import debug_reactor

reactor = debug_reactor()
player = recording_player(reactor)
while True:
    player.step()
