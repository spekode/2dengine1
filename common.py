import math

# These Vec classes should be rewritten to make an N-dimension base class and work from there.
# This'll work for now :D

class Vec(object):
	def __init__(self, v1=0.0):
		self.v1 = v1
	def _calcMag(self):
		return self.v1
	def __getattr__(self, name):
		if name == 'mag':
			return self._calcMag()
		elif name == 'x' or name == 'y':
			return self.v1
		raise AttributeError, "%s object has no attribute '%s'" % (type(self), name)
	def __mul__(self, other):
		if isinstance(other, Vec2):
			return Vec2.__mul__(other, self)
		elif isinstance(other, Vec):
			return Vec(self.v1 * other.v1)
		else:
			return Vec(self.v1 * other)
	def __sub__(self, other):
		if isinstance(other, Vec):
			v1 = self.v1 - other.v1
		else:
			v1 = self.v1 - other
		return Vec(v1)
	def __add__(self, other):
		return Vec(self.v1 + other.v1)
	def __int__(self):
		return int(self.v1)
	def __float__(self):
		return float(self.v1)
	def __neg__(self):
		return self.v1 * -1
	def __pos__(self):
		return self._calcMag()
	def __str__(self):
		return "<%f>" % self.v1

class Vec2(Vec):
	def __init__(self, v1=0.0, v2=0.0):
		self.v1 = v1
		self.v2 = v2
	def _calcMag(self):
		return math.sqrt((self.v1*self.v1) + (self.v2*self.v2))
	def __getattr__(self, name):
		if name == 'mag':
			return self._calcMag()
		elif name == 'x':
			return self.v1
		elif name == 'y':
			return self.v2
		raise AttributeError, "%s object has no attribute '%s'" % (type(self), name)

	def __mul__(self, other):
#		if isinstance(other, Vec2):
#			v1 = self.v1 * other.v1
#			v2 = self.v2 * other.v2
		if isinstance(other, Vec):
			v1 = self.v1 * other.v1
			v2 = self.v2 * other.v1
		elif isinstance(other, tuple) and len(other) == 2:
			v1 = self.v1 * other[0]
			v2 = self.v2 * other[1]
		else:
			v1 = self.v1 * other
			v2 = self.v2 * other
		return Vec2(v1, v2)
	def __sub__(self, other):
		if isinstance(other, Vec2):
			v1 = self.v1 - other.v1
			v2 = self.v2 - other.v2
		elif isinstance(other, Vec):
			v1 = self.v1 - other.v1
			v2 = self.v2 - other.v1
		elif isinstance(other, tuple) and len(other) == 2:
			v1 = self.v1 + other[0]
			v2 = self.v2 + other[1]
		else:
			v1 = self.v1 - other
			v2 = self.v2 - other
		return Vec2(v1, v2)
	def __add__(self, other):
		if isinstance(other, Vec2):
			v1 = self.v1 + other.v1
			v2 = self.v2 + other.v2
		elif isinstance(other, Vec):
			v1 = self.v1 + other.v1
			v2 = self.v2 + other.v1
		elif isinstance(other, tuple) and len(other) == 2:
			v1 = self.v1 + other[0]
			v2 = self.v2 + other[1]
		else:
			#try:
			v1 = self.v1 + other
			v2 = self.v2 + other
			#except Exception as e: raise e
		return Vec2(v1, v2)
	def __int__(self):
		return int(self._calcMag())
	def __float__(self):
		return float(self._calcMag())
	def __neg__(self):
		return self * -1
	def __str__(self):
		return "<%f, %f>" % (self.v1, self.v2)