#! /usr/bin/env python

import sys
from optparse import OptionParser
import config
import dna
import svgfig

def main():
	usage = "usage: %prog [options] inputfile outputfile"
	parser = OptionParser(usage=usage)
	parser.add_option("-v", "--verbose", 	dest="verbose", default=True, help="make lots of noise [default]")

	(options, args) = parser.parse_args()
	if len(args) != 2:
		parser.error("incorrect number of arguments")
	
	input_file = open(args[0], "r")
	dna_drawer = dna.DNADrawer(input_file)
	dnasvg = dna_drawer.get_svg()
	input_file.close()
	
	canvas_width = "%dpx" % config.CANVAS_VIEWPORT[0]
	canvas_height = "%dpx" % config.CANVAS_VIEWPORT[1]
	canvas_viewbox = "0 0 %d %d" % (config.CANVAS_VIEWPORT[0], config.CANVAS_VIEWPORT[1])
	
	svgcanvas = svgfig.canvas(dnasvg, width=canvas_width, height=canvas_height, viewBox=canvas_viewbox, style="stroke:white; fill:none; stroke-width:0.%dpt; stroke-linejoin:round; text-anchor:middle" % config.STROKE)
	svgcanvas.save(args[1])


if __name__ == "__main__":
	main()