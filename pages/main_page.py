from selenium import webdriver
from selenium.webdriver.common.by import By

from pages.base_page import BasePage

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
