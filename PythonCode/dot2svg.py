### This module converts dot file into image format for easy visualization

import sys
import os

def to_graph(fileName, target = ""):
        if target == "" :
            target = filename.replace('.dot','')+".png"
        command = "dot -Tpng " + fileName + " -o "+ target #Tsvg can be changed to Tjpg, Tpng, Tgif etc (see dot man pages)
        os.system(command)
if __name__=="__main__":
    if len(sys.argv) != 2:
        print ("\nUsage: python dot2svg.py mygraph.dot")
        exit ()
    filename=sys.argv[1]
    to_graph(filename)