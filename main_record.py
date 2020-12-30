from aztec_circle import aztec
from aztec_circle import sequence_tile_generator
from reactor import recording_reactor

import sys

grow_to  = int(sys.argv[1]) if len(sys.argv) > 1 else 3
sequence = str(sys.argv[2]) if len(sys.argv) > 2 else 'r'
seed     = int(sys.argv[3]) if len(sys.argv) > 3 else 712451

az = aztec(grow_to, sequence_tile_generator(seed, sequence), recording_reactor())
