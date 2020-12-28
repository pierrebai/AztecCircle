from aztec_circle import aztec
from draw_ascii import draw_ascii_reactor
from reactor import reactor
from tile_generator import sequence_tile_generator

seed = 7
az = aztec(10, sequence_tile_generator(seed, None), draw_ascii_reactor())
