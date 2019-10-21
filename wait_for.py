# wait_for module
#   decorators that wait for conditions/changes around an action
#   intended to be imported into page classes

# wait for the page url and title to change around a navigation
#   parameter: func - a web navigation method, such as a click 
def new_url_and_title(func):

	def wrapper(self, *args):
		before_url = self.get_current_url()
		before_title = self.get_page_title()

		if len(args) == 0:
			func(self)
		else:
			func(self, *args)

		while True:
			after_url = self.get_current_url()
			after_title = self.get_page_title()
			if before_url != after_url and before_title != after_title:
				break

	return wrapper
