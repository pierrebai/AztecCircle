from aztec_circle import aztec
from draw_ascii import draw_ascii_reactor
from reactor import reactor
from repeatable_random import repeatable_random

seed = 7
az = aztec(10, repeatable_random(seed), draw_ascii_reactor())
