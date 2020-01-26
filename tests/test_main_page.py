import unittest

from pages.article_page import ArticlePage

from tests.wikipedia_common import WikipediaCommon

class TestMainPage(WikipediaCommon):

	#@unittest.skip('')
	def test_mainpage_article_search(self):
		search_term = "Disneyland"

		main_page = self.open_main_page()
		article = self.search_for_article(main_page, search_term)

		# check the resulting page has the correct header & title
		s = article.get_page_title()
		self.assertRegex(s, "^{}.*".format(search_term))
		s = article.get_current_url()
		self.assertRegex(s, ".*{}$".format(search_term))
		self.assertEqual(article.get_article_header(), search_term)

	#@unittest.skip('')
	def test_mainpage_autosuggest(self):
#		if browser == "safari":
#			self.skipTest('main page search does not return autosuggest on Safari')

		main_page = self.open_main_page()
		self.type_search(main_page, "dou")
		self.verify_suggestions_start_with(main_page, "dou")
		self.type_search(main_page, "glas") # extend search term
		self.verify_suggestions_start_with(main_page, "douglas")

	####################
	# Helper functions
	####################

	def search_for_article(self, main_page, search_term):
		main_page.open_article_by_search(search_term)
		return ArticlePage(self.driver)

	# Type a search term without submitting search
	# parameters
	#   main_page - MainPage object
	#   search_term - string, text for search
	def type_search(self, main_page, search_term):
		main_page.enter_header_search_term(search_term)

	# Verify the suggestions from the search field
	# parameters
	#   main_page - MainPage object
	#   search_term - string, text expected in suggestions
	def verify_suggestions_start_with(self, main_page, search_term):
		regex = "^{}.*".format(search_term.lower())
		for suggestion in main_page.get_header_search_suggestions():
			title = suggestion['title'].lower()
			self.assertRegex(title, regex)
