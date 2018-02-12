# Verifies that the traces generated in part 1 are consistent with the specified topology
# i.e. tcp packets are only considered as received at nodes that are endpoints of
# one of two tcp connections
# This is the architecture with two tcp flows across one common UDP link with varying CBR

import os
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent
BASE_LOC = os.path.join(BASE_DIR, "out", "tr")

print(BASE_LOC)
