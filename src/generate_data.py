"""
Generate output data files for plotting in gnuplot
"""

import argparse
import pathlib
import glob
import sys
import os


# Files is an iterator over names of matching files
def drops_vs_cbr(files, args):
    filepath = pathlib.Path(__file__).resolve().parent
    if args.outfile:
        out = open(args.outfile, "w")
    elif args.rr:
        out = open(os.path.join(filepath, "dat", "rr_part1.dat"), "w")
    elif args.nrr:
        out = open(os.path.join(filepath, "dat", "nrr_part1.dat"), "w")
    elif args.vv:
        out = open(os.path.join(filepath, "dat", "vv_part1.dat"), "w")
    elif args.nrv:
        out = open(os.path.join(filepath, "dat", "nrv_part1.dat"), "w")

    for f in files:
        loss_rate = 0

        last_ind = f.rfind("/")
        if last_ind != -1:
            filename = f[last_ind+1:]
        else:
            filename = f

        # Extract the CBR from the filename
        cbr = int(''.join(c for c in filename if c.isdigit()))

        with open(f) as opened:
            drops = 0
            recvs = 0

            for line in opened:
                if line[0] == "r":
                    recvs += 1
                elif line[0] == "d":
                    drops += 1

            loss_rate = drops/(recvs + drops)

        out.write("{}\t{}\n".format(cbr, loss_rate))

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Generate input data for gnuplot.")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--rr", action="store_true")
    group.add_argument("--nrr", action="store_true")
    group.add_argument("--vv", action="store_true")
    group.add_argument("--nrv", action="store_true")

    parser.add_argument("--outfile")

    args = parser.parse_args()

    if args.rr:
        file_pattern = "Reno_Reno_*.tr"
    elif args.nrr:
        file_pattern = "Newreno_Reno_*.tr"
    elif args.vv:
        file_pattern = "Vegas_Vegas_*.tr"
    elif args.nrv:
        file_pattern = "Newreno_Vegas_*.tr"

    filepath = pathlib.Path(__file__).resolve().parent
    gglob = "{}/out/tr/{}".format(filepath, file_pattern)

    file_matches = glob.iglob(gglob)
    drops_vs_cbr(file_matches, args)
