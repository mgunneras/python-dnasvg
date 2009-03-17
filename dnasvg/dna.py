import csv
from svgfig import *
import config
from math import sqrt


class SNP(object):
	"""
	Single Nucleotide Polymorphism
	Basically this is a row in the genome CSV
	"""
	def __init__(self, name, variation, strand, code):
		self.name = name
		self.variation = variation
		self.code = code
		self.strand = strand
	
	def get_strand(self):
		return (self.strand == '+')
		
	def colour(self, index):
		c = config.COLOURS.get(self.code[index])
		if index == self.get_strand():
			c = [v*1.5 for v in c]
		return c


class SNPFactory(object):
	
	def __init__(self, file):
		self.reader = csv.reader(file, delimiter=',')
		# set over the header lables.
		self.reader.next()
	
	def get_SNP(self):
		data = self.reader.next()
		return SNP(data[0], data[1], data[4], data[5])


class DNADrawer(object):
	"""
	Turns a deCODEme csv file handle into
	an SVG representation.
	"""
	_current_x = 0
	_current_y = 0	
	_trigon_point_bottom_left = True
		
	def __init__(self, deCODEme_scan_file, limit, offset, width, height):
		self.snp_factory = SNPFactory(deCODEme_scan_file)
		self.limit = limit
		self.offset = offset
		self.shape_size = sqrt((width*height)/limit)
		self.grid_width = int(width/self.shape_size)
	
	def get_svg(self):
		return self._render()
		
	def _render(self):
		"""
		renders the SVG representation and wraps it in a group.
		"""
		self.svg_group = SVG('g')
		shape_count = 0
		while True:
			try:
				snp = self.snp_factory.get_SNP()
			except StopIteration:                                                    
				break
			if shape_count < self.offset: 
				shape_count=shape_count+1
				continue
			svg = self.svg_shape(snp)
			self.svg_group.append(svg)
			self._calculate_new_pos()
			shape_count=shape_count+1
			if shape_count==self.limit: break
			
		return self.svg_group

	def svg_shape(self, snp):
		"""
		Returns the SVG object for given SNP
		"""
		# <polygon points="0,0 10,0 0,10" fill="#00FF00"/>
		# group for the shapes
		group = SVG('g')
		double_points = self.trigon_points(self.trigon_point_bottom_left())	
		for index in range(2):
			p = double_points[index]
			points_string = "%d,%d %d,%d %d,%d" % (p[0][0], p[0][1], p[1][0], p[1][1], p[2][0], p[2][1])
			colour = snp.colour(index)
			group.append(SVG("polygon", points=points_string, fill=rgb(colour[0], colour[1], colour[2], 255)))

		return group
	
	def trigon_points(self, point_left):
		tl = (self.x(), self.y())
		tr = (self.x()+self.shape_size, self.y())
		bl = (self.x(), self.y()+self.shape_size)
		br = (self.x()+self.shape_size, self.y()+self.shape_size)
		if point_left:
			return ([tl, br, bl], [tl, tr, br])
		else: 
			return ([bl, tr, br], [tl, tr, bl])
	
	def trigon_point_bottom_left(self):
		self._trigon_point_bottom_left = not self._trigon_point_bottom_left
		# if new row set the start values
		if self.x() == 0:
			self._trigon_point_bottom_left = self._current_y % 2
		
		return self._trigon_point_bottom_left
	
	def x(self):
		return self._current_x * self.shape_size
	
	def y(self):
		return self._current_y * self.shape_size
	
	def _calculate_new_pos(self):
		# if not full row
		if self._current_x == self.grid_width-1:
			# starting place for next shape
			self._current_x = 0
			self._current_y = self._current_y + 1
		else:
			self._current_x = self._current_x + 1	
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			