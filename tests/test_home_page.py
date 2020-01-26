import unittest

from pages.main_page import MainPage
from pages.article_page import ArticlePage

from tests.wikipedia_common import WikipediaCommon

class TestHomePage(WikipediaCommon):

	#@unittest.skip('')
	def test_homepage_title(self):
		home_page = self.open_home_page()
		self.verify_home_page_title(home_page)

	#@unittest.skip('')
	# Safari doesn't display a tab unless multiple tabs are open.
	def test_homepage_article_search(self):
		search_term = "Buster Keaton"
		home_page = self.open_home_page()
		article = self.submit_search(home_page, search_term)
		self.verify_article_page(article, search_term)

	#@unittest.skip('')
	def test_homepage_autosuggest(self):
		home_page = self.open_home_page()
		self.type_search(home_page, "bust")
		self.verify_suggestions_start_with(home_page, "bust")
		self.type_search(home_page, "er")
		self.verify_suggestions_start_with(home_page, "buster")

	#@unittest.skip('')
	def test_homepage_english_link(self):
#		if browser == "safari":
#			self.skipTest('Safari does not click on home page language link as expected')

		home_page = self.open_home_page()
		main_page = self.click_language_link(home_page, 'English')
		self.verify_main_page_text(
			main_page,
			title_text="Wikipedia, the free encyclopedia",
			body_text="the free encyclopedia that anyone can edit")

	#@unittest.skip('')
	def test_homepage_french_link(self):
#		if browser == "safari":
#			self.skipTest('Safari does not click on home page language link as expected')

		home_page = self.open_home_page()
		main_page = self.click_language_link(home_page, 'Français')
		self.verify_main_page_text(
			main_page,
			title_text="Wikipédia, l'encyclopédie libre",
			body_text="L'encyclopédie libre que chacun peut améliorer")

	#@unittest.skip('')
	def test_homepage_german_link(self):
#		if browser == "safari":
#			self.skipTest('Safari does not click on home page language link as expected')

		home_page = self.open_home_page()
		main_page = self.click_language_link(home_page, 'Deutsch')
		self.verify_main_page_text(
			main_page,
			title_text="Wikipedia – Die freie Enzyklopädie",
			body_text="Wikipedia ist ein Projekt zum Aufbau einer Enzyklopädie aus freien Inhalten")

	#@unittest.skip('')
	def test_homepage_spanish_link(self):
#		if browser == "safari":
#			self.skipTest('Safari does not click on home page language link as expected')

		home_page = self.open_home_page()
		main_page = self.click_language_link(home_page, 'Español')
		self.verify_main_page_text(
			main_page,
			title_text="Wikipedia, la enciclopedia libre",
			body_text="la enciclopedia de contenido libreque todos pueden editar")

	####################
	# Helper functions
	####################

	# Verify the home page title
	# parameter
	#   home_page - HomePage object
	def verify_home_page_title(self, home_page):
		self.assertEqual(home_page.get_page_title(), "Wikipedia")

	# Submit a search
	# parameters
	#   home_page - HomePage object
	#   search_term - string, text to enter and submit
	# returns
	#   ArticlePage object
	def submit_search(self, home_page, search_term):
		home_page.enter_search_term(search_term)
		home_page.submit_search()
		return ArticlePage(self.driver)

	# Type text into search term, but not submit
	# parameters
	#   home_page - HomePage object
	#   search_term - string, text to enter
	def type_search(self, home_page, search_term):
		home_page.enter_search_term(search_term)

	# Click a language link
	# parameters
	#   home_page - HomePage object
	#   lang - string, two character language code
	# returns
	#   MainPage object
	def click_language_link(self, home_page, lang):
		home_page.click_language_link(lang)
		return MainPage(self.driver)

	# Verify article page title, URL and header
	# parameters
	#   article - ArticlePage object
	#   search_term - string, text to expect in elements of article page
	def verify_article_page(self, article, search_term):
		# check the resulting page has the correct header & title
		title_regex = "^{}.*".format(search_term)
		encoded_search_term = search_term.replace(" ", "_")
		url_regex   = ".*{}$".format(encoded_search_term)

		s = article.get_page_title()
		self.assertRegex(s, title_regex)
		s = article.get_current_url()
		self.assertRegex(s, url_regex)
		self.assertEqual(article.get_article_header(), search_term)

	# Verify the suggestions displayed with search file
	# parameters
	#   home_page - HomePage object
	#   search_term - string, expected text in suggestions
	def verify_suggestions_start_with(self, home_page, search_term):
		regex = "^{}.*".format(search_term.lower())
		for suggestion in home_page.get_search_suggestions():
			title = suggestion['title'].lower()
			self.assertRegex(title, regex)

	# Verify text on the main page
	# Parameters
	#   main_page - MainPage object
	#   title_text - expected text in the title (browser tab)
	#   body_text - expected text somewhere in body
	#
	# asserts the title/tab is the expected text
	# asserts the page body contains the expected text
	def verify_main_page_text(self, main_page, title_text, body_text):
		self.assertEqual(title_text, main_page.get_page_title())
		self.assertIn(body_text, main_page.get_body_text().replace("\n", ''))
