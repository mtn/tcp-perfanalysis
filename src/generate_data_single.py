"""
Generate output data files for plotting in gnuplot
"""

import argparse
import pathlib
import glob
import sys
import os


def increment(key, dictionary, amount=1):
    if key not in dictionary:
        dictionary[key] = 0
    dictionary[key] += 1

def compute_loss_rate(drops, recvs, key):
    if not key in drops:
        return 0
    elif not key in recvs:
        return 1

    return drops[key]/(recvs[key] + drops[key])

def compute_avg_bandwidth(sent, elapsed_time, key):
    if not key in sent:
        return 0

    return sent[key] / elapsed_time

def get_loss_rates_part1(opened):
    drops = {}
    recvs = {}

    for line in opened:
        split = line.split(" ")

        # Increment recvs for a 'r' at any tcp endpoint
        if split[0] == "r":

            if split[7] == "1" and split[3] == "0" or split[3] == "3":
                increment("tcp14", recvs)

            if split[7] == "2" and split[3] == "4" or split[3] == "5":
                increment("tcp56", recvs)

            if split[7] == "3":
                increment("udp", recvs)

        elif line[0] == "d":

            if split[7] == "1":
                increment("tcp14", drops)

            if split[7] == "2":
                increment("tcp56", drops)

            if split[7] == "3":
                increment("udp", drops)

    tcp_14_loss_rate = compute_loss_rate(drops, recvs, "tcp14")
    tcp_56_loss_rate = compute_loss_rate(drops, recvs, "tcp56")
    udp_loss_rate = compute_loss_rate(drops, recvs, "udp")

    return tcp_14_loss_rate, tcp_56_loss_rate, udp_loss_rate

def get_avg_bandwidth_part1(opened):
    ELAPSED_TIME = 3
    sent = {}

    for line in opened:
        split = line.split(" ")

        # Increment recvs for a 'r' at any tcp endpoint
        if split[0] == "r":
            # Packet size will always be integral
            pkt_size = int(split[5])

            if split[7] == "1" and split[3] == "0" or split[3] == "3":
                increment("tcp14", sent, pkt_size)

            if split[7] == "2" and split[3] == "4" or split[3] == "5":
                increment("tcp56", sent, pkt_size)

            if split[7] == "3":
                increment("udp", sent, pkt_size)

    tcp_14_avg_bandwidth = compute_avg_bandwidth(sent, ELAPSED_TIME, "tcp14")
    tcp_56_avg_bandwidth = compute_avg_bandwidth(sent, ELAPSED_TIME, "tcp56")
    udp_avg_bandwidth = compute_avg_bandwidth(sent, ELAPSED_TIME, "udp")

    return tcp_14_avg_bandwidth, tcp_56_avg_bandwidth, udp_avg_bandwidth

# Files is an iterator over names of matching files
def gen_data(files, args):
    filepath = pathlib.Path(__file__).resolve().parent
    outfiles = [None, None, None]

    if args.cbr_drops:
        analysis_kind = "drops"
    elif args.cbr_bandwidth:
        analysis_kind = "bandwidth"

    for i, stream in enumerate(["tcp14", "tcp56", "cbr"]):
        if args.rr:
            outfiles[i] = open(os.path.join(filepath, "dat",
                               "rr_{}_{}_part1.dat".format(stream, analysis_kind)), "w")
        elif args.nrr:
            outfiles[i] = open(os.path.join(filepath, "dat",
                               "nrr_{}_{}_part1.dat".format(stream, analysis_kind)),
                               "w")
        elif args.vv:
            outfiles[i] = open(os.path.join(filepath, "dat",
                               "vv_{}_{}_part1.dat".format(stream, analysis_kind)),
                               "w")
        elif args.nrv:
            outfiles[i] = open(os.path.join(filepath, "dat",
                               "nrv_{}_{}_part1.dat".format(stream, analysis_kind)),
                               "w")

    for f in files:
        last_ind = f.rfind("/")
        if last_ind != -1:
            filename = f[last_ind+1:]
        else:
            filename = f

        # Extract the CBR from the filename
        cbr = int(''.join(c for c in filename if c.isdigit()))/10

        with open(f) as opened:
            if args.cbr_drops:
                tcp_14, tcp_56, udp = get_loss_rates_part1(opened)

                outfiles[0].write("{}\t{}\n".format(cbr, tcp_14))
                outfiles[1].write("{}\t{}\n".format(cbr, tcp_56))
                outfiles[2].write("{}\t{}\n".format(cbr, udp))
            elif args.cbr_bandwidth:
                tcp_14, tcp_56, udp = get_avg_bandwidth_part1(opened)

                outfiles[0].write("{}\t{}\n".format(cbr, tcp_14))
                outfiles[1].write("{}\t{}\n".format(cbr, tcp_56))
                outfiles[2].write("{}\t{}\n".format(cbr, udp))


def generate_datfile(pattern, args):
    filepath = pathlib.Path(__file__).resolve().parent

    gglob = "{}/out/tr/{}".format(filepath, pattern)
    file_matches = glob.iglob(gglob)

    gen_data(file_matches, args)

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Generate input data for gnuplot.")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--r", action="store_true")
    group.add_argument("--nr", action="store_true")
    group.add_argument("--v", action="store_true")
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
