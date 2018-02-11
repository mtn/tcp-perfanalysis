import sys, os

protocol_pairs = [("Reno", "Reno"),
                  ("Newreno", "Reno"),
                  ("Vegas", "Vegas"),
                  ("Newreno", "Vegas")
                 ]

for p1, p2 in protocol_pairs:
    # for cbr in range(1,10,0.1):
    os.system("ns general.tcl {} {} 1".format(p1,p2))
    # print("ns general.tcl {} {} 1".format(p1,p2))
