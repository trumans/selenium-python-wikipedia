from selenium import webdriver
from selenium.webdriver.common.by import By

from pages.base_page import BasePage

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
