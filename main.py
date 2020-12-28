from aztec_circle import aztec
from draw_ascii import draw_ascii_reactor
from reactor import reactor, debug_reactor
from tile_generator import sequence_tile_generator

seed = 7
az = aztec(200, sequence_tile_generator(seed, None), reactor())

#draw_ascii_reactor().end_grow(az)

print("Origin:     " + str(az._origin))
print("Allocated:  " + str(len(az._squares)))
print("Tile count: " + str(az.count_tiles()))
