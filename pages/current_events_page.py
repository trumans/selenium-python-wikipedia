import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from pages.base_page import BasePage

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
