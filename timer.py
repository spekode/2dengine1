import time

class Timer(object):
	def __init__(self):
		self.startT = None
		self.endT = None
	def start(self):
		self.startT = time.time()
		self.endT = None
		return self
	def restart(self):
		self.start()
	def stop(self):
		self.endT = time.time()
		return self
	def reset(self):
		self.startT = None
		self.endT = None
		return self
	def elapsed(self):
		if not self.startT: return 0.0
		if self.endT:
			return (self.endT - self.startT) * 1000
		else:
			return (time.time() - self.startT) * 1000
