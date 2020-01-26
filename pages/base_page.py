import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions as SelExc

class BasePage(object):

	import wait_for

	search_input = (By.ID, 'searchInput')
	submit_search_button = (By.CSS_SELECTOR, '#searchButton')
	search_input_suggestions = (By.CSS_SELECTOR, '.suggestions-results > a')

	def __init__(self, driver):
		self.driver = driver

	# Return the page title
	def get_page_title(self):
		return self.driver.title

	# Return the current page URL
	def get_current_url(self):
		return self.driver.current_url	

	# Return the current page text
	def get_body_text(self):
		return self.driver.find_element(By.TAG_NAME, 'body').text.replace("\xa0"," ")

	# Get rows from a table and return as a list
	# Parameter
	#   table_element - table web element to parse
	# Returns tuples (label, value) for each row in the table
	#   label is text from th element
	#   value is text from td element
	#   missing th or td element is assigned None
	def table_to_list_of_tuples(self, table_element):
		vals = []
		row_elements = table_element.find_elements(By.TAG_NAME, "tr")
		for row in row_elements:
			try:
				h = row.find_element(By.TAG_NAME, "th").text.strip().replace("\xa0"," ")
			except SelExc.NoSuchElementException:
				h = None

			try:
				d = row.find_element(By.TAG_NAME, "td").text.strip().replace("\xa0"," ")
			except SelExc.NoSuchElementException:
				d = None
			
			vals.append((h, d))

		return vals

	# Return a value from a table
	# Parameters
	#   table_element: web object expected to contain table rows elements (tr)
	#   header_text: text to find in a row header (th). 
	# Returns
	#     table data (td) text if a matching row header if found
	#     None if a matching row header is not found
	def get_value_in_table(self, table_element, header_text):
		row_elements = table_element.find_elements(By.TAG_NAME, "tr")
		for row in row_elements:
			try:
				h = row.find_element(By.TAG_NAME, "th").text.strip()
			except SelExc.NoSuchElementException:
				h = ''

			if header_text in h:
				try:
					d = row.find_element(By.TAG_NAME, "td").text.strip()
				except SelExc.NoSuchElementException:
					d = None
				return d

		return None  # header text was not found

	# Click on a link
	#   parameter: link_obj is a selenium object which can be clicked on.
	#     assumes link opens another page. waits for page title and URL to change
	@wait_for.new_url_and_title
	def click_link(self, link_obj):
		link_obj.click()

	# Enter the search term in the header
	#   function does not submit the search
	# Parameter
	#   search_string - text to enter into search field
	def enter_header_search_term(self, search_string):
		before_list = self.get_header_search_suggestions()
		before_time = time.time()
		self.driver.find_element(
			*BasePage.search_input).send_keys(search_string)
		# wait for autosuggest list to update
		while True:
			after_list = self.get_header_search_suggestions()
			after_time = time.time()
			if (before_list != after_list) or ((after_time-before_time) > 1):
				break

	# Submit the search in the header search
	#   assumes the search term is already entered. waits for page title and URL to change
	@wait_for.new_url_and_title
	def submit_header_search(self):
		self.driver.find_element(*BasePage.submit_search_button).send_keys(Keys.RETURN)

	# Get the list of suggestions from the header search field
	#   Returns list of suggestions represented as a dictionary with items
	#     'title' contain text of suggestion and 'link' containing href.
	#
	#   Note: method does not attempt to wait for list to "settle" although
	#     it does recover from selenium Stale Element exception
	def get_header_search_suggestions(self):
		while True:
			try:
				suggestions = [ 
					{'title': element.text, 
					 'link' : element.get_attribute('href') }
					for element in self.driver.find_elements(
						*BasePage.search_input_suggestions)
				]
				break
			except SelExc.StaleElementReferenceException:
				pass

		return suggestions

	# regex to match dates formatted "June 20, 2019 (Thursday)"
	#   allowing for text between date and day-of-week
	long_date_regex = r'(January|February|March|April|May|June|July|August|September|October|November|December)\s([1-9][0-9]?),\s(\d{4}).*\((Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\)'

	def month_index(self, month_name):
		months = {
			"January":   1,
			"February":  2,
			"March":     3,
			"April":     4,
			"May":       5, 
			"June":      6,
			"July":      7,
			"August":    8,
			"September": 9,
			"October":   10,
			"November":  11,
			"December":  12
		}
		return months.get(month_name, "invalid month name")

	def month_name(self, month_number):
		months = {
			1: "January",
			2: "February",
			3: "March",
			4: "April",
			5: "May", 
			6: "June",
			7: "July",
			8: "August",
			9: "September",
			10: "October",
			11: "November",
			12: "December"
		}
		return months.get(month_number, "invalid month#")

