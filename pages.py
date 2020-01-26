import sys
import time
from datetime import datetime
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions as SelExc
from selenium.webdriver.common.action_chains import ActionChains

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


class ArticlePage(BasePage):

	article_header = (By.ID, 'firstHeading')
	infobox = (By.CSS_SELECTOR, 'table.infobox')
	toc_box = (By.ID, 'toc')
	toc_item = (By.CLASS_NAME, 'toctext')
	headline = (By.CLASS_NAME, 'mw-headline')

	# Get the text from the article header
	def get_article_header(self):
		return self.driver.find_element(*ArticlePage.article_header).text

	# Get the text in the infobox
	def get_infobox_text(self):
		return self.driver.find_element(*ArticlePage.infobox).text

	# Parse the contents of the infobox
	# Returns list of two-item tuples containing text from th and td elements
	def get_infobox_contents(self):
		i = self.driver.find_element(*ArticlePage.infobox)
		return self.table_to_list_of_tuples(i)

	# Get from the infobox the value related to a label
	# Parameter
	#   header_text - label to search for
	# Returns text related to the label
	def get_value_from_infobox(self, header_text):
		i = self.driver.find_element(*ArticlePage.infobox)
		return self.get_value_in_table(i, header_text)

	# Get a value from a list of tuples
	# Parameters
	#   infobox_contents: list of two-item tuples, presumably from an infobox 
	#   header_text: text to find the first item of each tuple (i.e. table header) 
	# Returns
	#     second item from the tuple containing the matching header text
	#     None if a matching value is not found
	def get_value_from_infobox_contents(self, infobox_contents, header_text):
		for item in infobox_contents:
			if item[0] != None and header_text in item[0]:
				return item[1]
		return None

	# Get the Table of Contents text
	# Returns list of strings from ToC box
	def get_toc_items_text(self):
		toc = self.driver.find_element(*ArticlePage.toc_box)
		toc_items = toc.find_elements(*ArticlePage.toc_item)
		return [ item.text for item in toc_items ]

	# Get the headlines text
	# Returns list of strings from headers in the article
	def get_headlines_text(self):
		headlines = self.driver.find_elements(*ArticlePage.headline)
		return [ headline.text for headline in headlines ]

class CurrentEventsPage(BasePage):

	first_archived_year = 1994
	first_archived_month = 7
	date_header = (By.CSS_SELECTOR, "[role='heading'] [class='summary']")
	events_by_month_box = (By.CSS_SELECTOR, "[aria-labelledby='Events_by_month']")
	year_archives = (By.CSS_SELECTOR, "[aria-labelledby='Events_by_month'] .hlist dl")

	# Get archive links by year for all years
	# return: list of elements containing each year
	def get_archive_links_by_year(self):
		return self.driver.find_elements(*self.year_archives)

	# Create a list of link attributes
	# parameter:
	#   links_parent - web element containing <a> nodes
	# return: list of dictionaries containing the href, title and text
	#   from <a> node
	def parse_archive_links(self, links_parent):

		links = links_parent.find_elements(By.CSS_SELECTOR, "a")

		def get_attributes(el):
			hr = el.get_attribute("href")
			ti = el.get_attribute("title")
			tx = el.text
			return { "href": hr, "title": ti, "text": tx }

		yr = map(get_attributes, links)
		return list(yr)

	# Open the page for current events archive for a month and year
	#   using links at the bottom of current events page
	# Parameters
	#   month - month name, full spelling
	#   year - 4 digit year
	def click_link_archived_month(self, month, year):
		link_css = "a[href*='{}_{}']".format(month, year)
		box = self.driver.find_element(*self.events_by_month_box)
		lnk = box.find_element(By.CSS_SELECTOR, link_css)
		ActionChains(self.driver).move_to_element(lnk).perform()
		self.click_link(lnk)

	# Return the headers for each date on the page
	def get_date_headers(self):
		hdrs = self.driver.find_elements(*self.date_header)
		date_headers = []
		for header in hdrs:
			date_headers.append(header.text)
		return date_headers

	# Parse a date text into month, day, year, day-of-week
	# Parameter
	#   header_text - text to parse date components from
	# Returns a tuple of the four strings
	def parse_date_header(self, header_text):
		m = re.search(self.long_date_regex, header_text)
		return (m[1], m[2], m[3], m[4])


class MainPage(BasePage):

	main_page_url = "https://en.wikipedia.org/wiki/Main_Page"
	top_banner = (By.ID, 'mp-topbanner')
	left_panel = (By.ID, 'mw-panel')

	# Open the Main page
	def open_main_page(self):
		self.driver.get(self.main_page_url)

	# Open an article for a search term using the header search
	#   should open the article page that's the first search suggestion
	# Parameters
	#   search_term - string entered in the header search field
	def open_article_by_search(self, search_term):
		self.enter_header_search_term(search_term)
		self.submit_header_search()

	# Click a link on the left side panel
	# Parameters
	#   link_text - the text on the link to click
	def click_left_panel_link(self, link_text):
		lnk_loc = (By.PARTIAL_LINK_TEXT, link_text)
		lnk = self.driver.find_element(*self.left_panel).find_element(*lnk_loc)
		self.click_link(lnk)

	# Get the text from the banner at the top of the page
	def get_topbanner_text(self):
		return self.driver.find_element(*self.top_banner).text
