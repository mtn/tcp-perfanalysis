"""
Generate output data files for plotting in gnuplot
"""

import argparse
import pathlib
import glob
import sys

RELATIVE_PATH = sys.argv[0]


# Files is an iterator over names of matching files
def drops_vs_cbr(files):
    for f in files:
        loss_rate = 0
        cbr = int(''.join(c for c in f if c.isdigit()))

        with open(f) as o:
            drops = 0
            recvs = 0

            for line in o:
                if line[0] == "r":
                    recvs += 1
                elif line[0] == "d":
                    drops += 1

            loss_rate = drops/(recvs + drops)

        print("cbr: {}, loss_rate: {}".format(cbr, loss_rate))

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Generate input data for gnuplot.")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--rr", action="store_true")
    group.add_argument("--nrr", action="store_true")
    group.add_argument("--vv", action="store_true")
    group.add_argument("--nrv", action="store_true")

    args = parser.parse_args()

    if args.rr:
        file_pattern = "Reno_Reno_*.tr"
        # with open("out/tr/Reno_Reno_13.tr") as f:
        #     for line in f:
        #         print(line)
        #         print("hi")

    elif args.nrr:
        file_pattern = "Newreno_Reno_*.tr"
    elif args.vv:
        file_pattern = "Vegas_Vegas_*.tr"
    elif args.nrv:
        file_pattern = "Newreno_Vegas_*.tr"

    filepath = pathlib.Path(__file__).resolve().parent
    gglob = "{}/out/tr/{}".format(filepath, file_pattern)

    file_matches = glob.iglob(gglob)
    drops_vs_cbr(file_matches)


