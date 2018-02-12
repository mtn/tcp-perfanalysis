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
    if args.rr:
        out = open(os.path.join(filepath, "dat", "rr_drops_part1.dat"), "w")
    elif args.nrr:
        out = open(os.path.join(filepath, "dat", "nrr_drops_part1.dat"), "w")
    elif args.vv:
        out = open(os.path.join(filepath, "dat", "vv_drops_part1.dat"), "w")
    elif args.nrv:
        out = open(os.path.join(filepath, "dat", "nrv_drops_part1.dat"), "w")

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

# Files is an iterator over names of matching files
def bandwidth_vs_cbr(files, args):
    filepath = pathlib.Path(__file__).resolve().parent
    if args.rr:
        out = open(os.path.join(filepath, "dat", "rr_bandwidth_part1.dat"), "w")
    elif args.nrr:
        out = open(os.path.join(filepath, "dat", "nrr_bandwidth_part1.dat"), "w")
    elif args.vv:
        out = open(os.path.join(filepath, "dat", "vv_bandwidth_part1.dat"), "w")
    elif args.nrv:
        out = open(os.path.join(filepath, "dat", "nrv_bandwidth_part1.dat"), "w")

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

def generate_datfile(pattern, args):
    filepath = pathlib.Path(__file__).resolve().parent

    gglob = "{}/out/tr/{}".format(filepath, pattern)
    file_matches = glob.iglob(gglob)
    if args.cbr_drops:
        drops_vs_cbr(file_matches, args)
    else:
        bandwidth_vs_cbr(file_matches, args)

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Generate input data for gnuplot.")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--rr", action="store_true")
    group.add_argument("--nrr", action="store_true")
    group.add_argument("--vv", action="store_true")
    group.add_argument("--nrv", action="store_true")
    group.add_argument("--all", action="store_true")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--cbr_drops", action="store_true",
                       help="plot average number of drops against cbr")
    group.add_argument("--cbr_bandwidth", action="store_true",
                       help="plot average bandwidth against cbr")

    args = parser.parse_args()

    BASE_PATH = pathlib.Path(__file__).resolve().parent
    DAT_PATH = os.path.join(BASE_PATH, "dat")
    if not os.path.isdir(DAT_PATH):
        os.mkdir(DAT_PATH)

    if args.all:
        for i, pattern in enumerate(["Reno_Reno_*.tr", "Newreno_Reno_*.tr",
                                     "Vegas_Vegas_*.tr", "Newreno_Vegas_*.tr"]):

            args.rr = True if i == 0 else False
            args.nrr = True if i == 1 else False
            args.vv = True if i == 2 else False
            args.nrv = True if i == 3 else False

            generate_datfile(pattern, args)
    else:
        if args.rr:
            file_pattern = "Reno_Reno_*.tr"
        elif args.nrr:
            file_pattern = "Newreno_Reno_*.tr"
        elif args.vv:
            file_pattern = "Vegas_Vegas_*.tr"
        elif args.nrv:
            file_pattern = "Newreno_Vegas_*.tr"

        generate_datfile(file_pattern, args)
