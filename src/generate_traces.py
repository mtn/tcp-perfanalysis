import sys, os

if not os.path.isdir("out"):
    os.mkdir("out")
if not os.path.isdir("out/tr"):
    os.mkdir("out/tr")
if not os.path.isdir("out/nam"):
    os.mkdir("out/nam")

protocol_pairs = [("Reno", "Reno"),
                  ("Newreno", "Reno"),
                  ("Vegas", "Vegas"),
                  ("Newreno", "Vegas")]

# For each protocol pair, generate traces for each CBR from 0 to 10 with steps of 0.5
for p1, p2 in protocol_pairs:
    for cbr in range(0, 101, 5):
        # print("ns general.tcl {} {} {}".format(p1, p2, cbr/10))
        os.system("ns general.tcl {} {} {}".format(p1, p2, cbr/10))
