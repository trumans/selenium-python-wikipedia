import unittest

from pages.article_page import ArticlePage

from tests.wikipedia_common import WikipediaCommon

class TestArticlePage(WikipediaCommon):

	def test_infobox_for_country(self):
		self.infobox_test(
			"Peru", (('Currency', "Sol"), ('Capital', "Lima")))

	def test_infobox_for_chemistry(self):
		self.infobox_test(
			"Oxygen", (('atomic weight', "15.999"), ('Phase at STP', "gas")))

	def test_infobox_for_person(self):
		self.infobox_test(
			"Charlie Chaplin", (('Born', '1889'), ('Relatives', 'Chaplin')))

	def test_infobox_for_movie(self):
		self.infobox_test(
			"north by northwest",
			(('Directed', 'Alfred Hitchcock'), ('Starring', 'Cary Grant')))

	def test_infobox_for_holiday(self):
		self.infobox_test(
			"april fool's day",
			(('Significance', 'pranks'), ('Frequency', 'Annual')))

	def test_infobox_for_song(self):
		self.infobox_test(
			"rocky raccoon",
			(('Recorded', '1968'), ('Songwriter(s)', 'Lennon')))

	def test_compare_toc_and_headlines(self):
		main = self.open_main_page()
		article = self.open_article_by_search(main, "Douglas Adams")
		self.verify_article_toc_and_headers(article)

	####################
	# Helper functions
	####################

	# Template for testing info box contents
	# parameters
	#   search_term - string, search text to open an article.
	#     assumes search does not open a disambiguration page
	#   expected_values - list of (label, value) tuples where
	#     label is a string contained in the left side of a row in info box
	#     value is a string contained in value on the right side
	def infobox_test(self, search_term, expected_values):
		main_page = self.open_main_page()
		article = self.open_article_by_search(main_page, search_term)
		infobox = article.get_infobox_contents()

		# check expected values are in info box
		for (label, expected_value) in expected_values:
			found_value = article.get_value_from_infobox_contents(infobox, label)
			self.assertIn(expected_value, found_value)

	# Submits a search from the main page
	# parameter
	#   main_page - MainPage object
	#   search_term - string, text to enter for search
	def open_article_by_search(self, main_page, search_term):
		main_page.open_article_by_search(search_term)
		return ArticlePage(self.driver)

	def verify_article_toc_and_headers(self, article):
		toc = article.get_toc_items_text()
		self.assertTrue(len(toc) > 0, "TOC is empty")
		headlines = article.get_headlines_text()
		self.assertTrue(len(headlines) > 0, "No headlines found")
		self.assertEqual(toc, headlines)
