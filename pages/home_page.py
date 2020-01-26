import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import exceptions as SelExc

from pages.base_page import BasePage

class HomePage(BasePage):

	import wait_for

	homePageUrl = "https://wikipedia.org"
	
	search_input = (By.ID, 'searchInput')
	submit_search_button = (By.XPATH, "//button[@type='submit']")
	search_input_suggestions = (By.CSS_SELECTOR, '#typeahead-suggestions a')

	# Open the home page
	def open_home_page(self):
		self.driver.get(self.homePageUrl)

	# Enter search term into search field
	#   search is not submited
	# Parameter
	#   search_str - string to enter into search field
	def enter_search_term(self, search_str):
		max_wait = 2 # maximum time to wait for search suggestions to change
		before_list = self.get_search_suggestions()
		before_time = time.time()		
		self.driver.find_element(*HomePage.search_input).send_keys(search_str)
		# wait for sooner of: the autosuggestion list to change, or 1 second
		while True:
			after_list = self.get_search_suggestions()
			after_time = time.time()
			if (after_list != before_list) or ((after_time-before_time) > max_wait):
				break

	# Submit the search already entered in the header
	#   waits for page title and URL to change
	@wait_for.new_url_and_title
	def submit_search(self):
		self.driver.find_element(*HomePage.submit_search_button).submit()

	# Get the suggestions from the search input
	# Returns a list of suggestions represented by dictionaries containing
	#   'title' of the suggestion
	#   'summary' with any additional text
	#   'link' containing the href in the suggestion
	def get_search_suggestions(self):
		suggestions = []
		start_time = time.time()

		while True:
			try:
				for element in self.driver.find_elements(
						*HomePage.search_input_suggestions):
					text = element.text.split("\n")
					suggestion = {
						'title'  : text[0],
						'summary': text[1] if len(text) == 2 else '',
						'link'   : element.get_attribute('href')}
					suggestions.append(suggestion)
				break
			except (SelExc.StaleElementReferenceException, SelExc.NoSuchElementException) as e:
				# When Stale Element or No Such Element (often for href) is thrown
				#   reset suggestions list, find and parse elements again
				#   throw exception if too much time spent attempting it
				if time.time() - start_time < 1: #  limit attempts to 1 second
					suggestions = []
					pass
				else:
					raise Exception(e)
		return suggestions

	def find_element_language_link(self, language):
		css = "[data-el-section='primary links'] a[title *= '{}']".format(language)
		return self.driver.find_element(By.CSS_SELECTOR, css)

		'''
		Alternate locators attempted to work correctly with Safari
		xpath = "//a//*[contains(text(), '{}')]".format(language)
		return self.driver.find_element(By.XPATH, xpath)

		ln = "en"
		if language == "Deutsch":
			ln = "de"
		elif language == "Français":
			ln = "fr"
		elif language == "Español":
			ln = "es"

		css = "a[href='//{}.wikipedia.org/']".format(ln)
		css = "[lang='{}'] a".format(ln) 
		return self.driver.find_element(By.CSS_SELECTOR, css)
		'''

	# Click a specified language link
	#   waits for page title and URL to change
	# Parameter
	#   language_code: 2 letter language code in link for lanaguage's main page
	@wait_for.new_url_and_title
	def click_language_link(self, language):
		self.find_element_language_link(language).click()
