import csv
from svgfig import *
import config
import math


class SNP(object):
	"""
	Single Nucleotide Polymorphism
	Basically this is a row in the genome CSV
	"""
	def __init__(self, name, variation, chromosome, strand, code):
		self.name = name
		self.variation = variation
		self.code = code
		self.strand = strand
		self.chromosome = chromosome

	def get_strand(self):
		return (self.strand == '+')

	def colour(self, index):
		if self.trait:
			return config.COLOURS.get('TRAIT')
		c = config.COLOURS.get(self.code[index])
		if index == self.get_strand():
			c = [v*1.5 for v in c]
		return c


class SNPFactory(object):
	
	def __init__(self, snp_file, trait_file):
		self.reader = csv.reader(snp_file, delimiter=',')
		# set over the header lables.
		self.reader.next()
		self.chromosome = None	
		trait_reader = csv.reader(trait_file, delimiter=',')
		# skip labels
		trait_reader.next()
		self.traits = {}
		while True:
			try:
				trait = trait_reader.next()
				self.traits[trait[2]] = trait
			except StopIteration:
				break

	def trait_for_snp(self, snp):
		if self.chromosome != snp.chromosome:
			print 'Chromosome', snp.chromosome
			self.chromosome = snp.chromosome
		return self.traits[snp.name]

	def get_SNP(self):
		data = self.reader.next()
		snp = SNP(data[0], data[1], data[2], data[4], data[5])
		try:
			snp.trait = self.trait_for_snp(snp)
			print snp.trait
		except KeyError:
			snp.trait = None
		return snp


class DNADrawer(object):
	"""
	Turns a deCODEme csv file handle into
	an SVG representation.
	"""
	_current_x = 0
	_current_y = 0	
	_trigon_point_bottom_left = True
		
	def __init__(self, deCODEme_scan_file, deCODEme_trait_file, limit, offset, width, height):
		self.snp_factory = SNPFactory(deCODEme_scan_file, deCODEme_trait_file)
		self.limit = limit
		self.offset = offset
		self.shape_size = math.sqrt((width*height)/limit)
		self.grid_width = int(width/self.shape_size)
		self.grid_height = int(math.floor(height/self.shape_size)) 

	def get_filters(self):
		"""
		    <filter id="HueRotate90" filterUnits="objectBoundingBox" x="0%" y="0%" width="100%" height="100%">
			     <feColorMatrix type="hueRotate" in="SourceGraphic" values="190"/>
			</filter>
		"""
		defs = SVG('defs')
		for c in range(22):
			c=c+1
			filter = SVG('filter', id='F%d' % c, filterUnits="objectBoundingBox", x="0%", y="0%", width="100%", height="100%")
			filter.append(SVG('feColorMatrix', type="hueRotate", values="%d0" % (int(c)*3)))
			defs.append(filter)
		return defs

	def get_svg(self):
		return self._render()
		
	def _render(self):
		"""
		renders the SVG representation and wraps it in a group.
		"""
		#self.svg_group = SVG('g')
		shape_count = 0
		base_group = SVG('g', id='base_group')
		chromosome = None
		while True:
			try:
				while True:
					snp = self.snp_factory.get_SNP()
					if snp.code!='--':
						break
			except StopIteration:                                                    
				break
			if shape_count < self.offset: 
				shape_count=shape_count+1
				continue
			# create a group for chromosome
			if chromosome != snp.chromosome:
				chromo_group = SVG('g', id=snp.chromosome, filter="url(#F%s)" % snp.chromosome)
				base_group.append(chromo_group)
				chromosome=snp.chromosome
			svg = self.svg_shape(snp)
			chromo_group.append(svg)
			self._calculate_new_pos()
			shape_count=shape_count+1
			if shape_count==self.limit: break
			if self._current_y==self.grid_height: break
		return base_group

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
		if snp.trait:
			group.append(SVG("text", SVG("tspan", snp.trait[0]), x=self.x(), y=self.y()-2, fill="black", font_size="10pt"))
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
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
