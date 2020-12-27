from aztec_circle import aztec
from draw_ascii import draw_ascii_reactor
from repeatable_random import repeatable_random

seed = 7
az = aztec(0, repeatable_random(seed), draw_ascii_reactor())
for i in range(0, 6):
    az.grow()
    print('')
    print('')

