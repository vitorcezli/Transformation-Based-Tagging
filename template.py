#!/usr/bin/python

class Template:
	"This class is used as a transformation rule template"
	INVALID = -1


	def __init__( self, fi, fpos, li, lpos, from_pos, to_pos ):
		self.fi = fi
		self.fpos = fpos
		self.li = li
		self.lpos = lpos
		self.from_pos = from_pos
		self.to_pos = to_pos


	def get_rule( self ):
		return ( self.fi, self.fpos, self.li, self.lpos, \
			self.from_pos, self.to_pos )


	def first_index( self, index ):
		if index - self.fi < 0:
			return Template.INVALID
		else:
			return index - self.fi


	def last_index( self, index, size ):
		if index + self.li >= size:
			return Template.INVALID
		else:
			return index + self.li


	def make_transformation( self, array ):
		size = len( array )
		
		for index in range( size ):
			index_first = self.first_index( index )
			index_last = self.last_index( index, size )
			if ( index_first == Template.INVALID ) or \
			   ( index_last == Template.INVALID ):
				continue
			else:
				if ( array[ index_first ] == self.fpos ) and \
				   ( array[ index_last ] == self.lpos ) and \
				   ( array[ index ] == self.from_pos ):
					array[ index ] = self.to_pos