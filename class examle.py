class A1:
	"""docstring for ClassName"""
	atr = "A1 attr"

	def __init__(self, atr1):
		self.atr1 = atr1

a = A1("some atr")

class A2:
	"""docstring for ClassName"""
	__atr2 = 42
	atr = "A2 attr"

	def __init__(self, atr1):
		self.atr1 = atr1

	def say_hello(self):
		print("")
		self.atr3 = "atr3"

a2 = A2()

A.__atr2  # 

a2.__atr2

a2.atr3 # atr Error
a2.say_hello()

a2.atr3
A2.say_hello(a2)

########################################################
class B(A2, A):
	"""docstring for B"""
	# atr = "B atr"
	pass

B.atr


#########
from abc import ABCMeta, abstractmethod
class Foo(metaclass=ABCMeta):
	@abstractmethod
	def name_of_method(self):
		pass


class  Bar(Foo):

	def name_of_method(self):
		print("implemented")
		
		





