# Generates traces files for part 1 of the assignment

import sys, os
import argparse

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
def generate_two_flow_traces():
    for p1, p2 in protocol_pairs:
        for cbr in range(1, 101, 5):
            # print("ns general.tcl {} {} {}".format(p1, p2, cbr/10))
            os.system("ns two_flow.tcl {} {} {}".format(p1, p2, cbr/10))

single_protocols = ["Reno", "Newreno", "Vegas"]

def generate_single_flow_traces():
    for protocol in single_protocols:
        for cbr in range(1, 101, 5):
            # print("ns general.tcl {} {} {}".format(p1, p2, cbr/10))
            os.system("ns single_flow.tcl {} {}".format(protocol, cbr/10))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate trace files for part 1")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--single", action="store_true")
    group.add_argument("--double", action="store_true")

    args = parser.parse_args()

    if args.single:
        generate_single_flow_traces()
    else:
        generate_two_flow_traces()
