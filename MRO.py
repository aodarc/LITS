class X: 
	pass 
class Y: 
	pass 
class Z:
	 pass 
class A(X,Y):
    pass 
class B(Y,Z):
    pass 
class M(B,A,Z):
    pass 
print(M.__mro__, sep='\n')


class Robot:
	name = 'Bander'
	x = 0
	y = 0
	rotation = 'front'

class MoveUpMixin:
	def move(self):
		self.y += 1		

class RotationMixin:
	def turn_left(self):
		self.rotation = 'left'

	def turn_right(self):
		self.rotation = 'right'



class CasanovaRobot(
	Robot, 
	MoveUpMixin):
	pass
		

