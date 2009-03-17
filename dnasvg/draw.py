#! /usr/bin/env python

import sys
from optparse import OptionParser
import config
import dna
import svgfig

def main():
	usage = "usage: %prog [options] inputfile outputfile"
	parser = OptionParser(usage=usage)
	parser.add_option("-l", "--limit", 		default=config.LIMIT, help="Max limit of SNPs to draw")
	parser.add_option("-o", "--offset", 	default=config.OFFSET, help="Offset of SNPs to skip")
	parser.add_option("-v", "--viewport",	default=config.CANVAS_VIEWPORT, help="Viewport to draw", metavar="WIDTHxHEIGHT")
	parser.add_option("-s", "--stroke",		default=config.STROKE, help="Stroke width", metavar="X.Xpt")

	(options, args) = parser.parse_args()

	if len(args) != 2:
		parser.error("incorrect number of arguments")
	
	# options
	limit 		= int(options.limit)
	offset 		= int(options.offset)
	viewport 	= options.viewport
	stroke 		= options.stroke
	
	if type(viewport) == str:
		viewport = [int(d) for d in viewport.split('x')]

	input_file = open(args[0], "r")
	dna_drawer = dna.DNADrawer(input_file, limit, offset, viewport[0], viewport[1])
	dnasvg = dna_drawer.get_svg()
	input_file.close()

	canvas_width = "%dpx" % viewport[0]
	canvas_height = "%dpx" % viewport[1]
	canvas_viewbox = "0 0 %d %d" % (viewport[0], viewport[1])
	
	svgcanvas = svgfig.canvas(dnasvg, width=canvas_width, height=canvas_height, viewBox=canvas_viewbox, style="stroke:white; fill:cornsilk; stroke-width:%s; stroke-linejoin:round; text-anchor:middle" % stroke)
	svgcanvas.save(args[1])


if __name__ == "__main__":
	main()