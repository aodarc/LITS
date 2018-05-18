
def html_tag(tag='div'):

	def decorator(func):
		def wrapper(*args, **kwargs):
			return '<{0}>{1}</{0}>'.format(tag, func())
		return wrapper

	return decorator



@html_tag(tag='p')
def get_some_text():
	return "hello world"



print(get_some_text())  # '<h1>hello world</h1>'


def decorator(func):
	def wrapper(*args, **kwargs):
		# ... 
		return '<{0}>{1}</{0}>'.format('div', func())
	return wrapper


# same way
@decorator
def get_some_text():
	return "hello world"
# same way
get_some_text = decorator(get_some_text)



class ClassDecorator:
	"""html_tag decorator"""
	def __init__(self, tag):
		self.tag = tag
	
	def __call__(self, func):
		"""Our decorator"""

		def wrapper(*args, **kwargs):
			return '<{0}>{1}</{0}>'.format(self.tag, func())
		return wrapper


@ClassDecorator(tag='span')
def get_some_text():
	return "hello world"

print(get_some_text())  # '<span>hello world</span>'

