# Generates tex graphs using gnuplot and stores them in tex_src dir
#
# Script must be kept in the same directory as .gpi input files
# and one level about tex_src dir

import subprocess
import pathlib
import os


if __name__=="__main__":
    dirpath = pathlib.Path(__file__).resolve().parent
    directory = os.fsencode(dirpath)

    if not os.path.isdir(os.path.join(dirpath, "tex_src")):
        os.mkdir(os.path.join(dirpath, "tex_src"))

    for filename in os.listdir(directory):
        filename = os.fsdecode(filename)
        if filename.endswith(".gpi"):
            with open(os.path.join("tex_src", "{}.tex".format(filename[:-4])), "w") as outfile:
                subprocess.call("gnuplot \"{}\"".format(filename), stdout=outfile, shell=True)
