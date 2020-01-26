import unittest

from selenium import webdriver

from pages.home_page import HomePage
from pages.main_page import MainPage

global browser

class WikipediaCommon(unittest.TestCase):

	def setUp(self):
		global browser
		if browser == 'firefox':
			self.driver = webdriver.Firefox(executable_path='/selenium_browser_drivers/geckodriver')
		elif browser == 'ie':
			self.driver = webdriver.Ie()
		elif browser == 'chrome':
			self.driver = webdriver.Chrome()  # use driver in system path /usr/local/bin on Unix
			#self.driver = webdriver.Chrome(executable_path='/path_to/chromedriver')
		elif browser == 'safari':
			self.driver = webdriver.Safari()
			self.driver.set_window_position(20,20)
			self.driver.set_window_size(1200,800)
		else:
			print('Browser parameter not recognized')
		# The implicit wait is not normally necessary
		#self.driver.implicitly_wait(5)

	def tearDown(self):
		self.driver.quit()

	# Open the home page
	# returns
	#   HomePage object
	def open_home_page(self):
		home = HomePage(self.driver)
		home.open_home_page()
		return home

	# Open the main page (English)
	# returns
	#   MainPage object
	def open_main_page(self):
		main = MainPage(self.driver)
		main.open_main_page()
		return main
