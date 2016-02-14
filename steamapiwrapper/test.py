class A():


	def __init__(self):
		self.a = 10


class B(A):
	def change(self):
		self.a = 100

a  = A()
b = B()
print b.a
b.change()
print b.a