import sys
import time
import datetime
import unittest
import re
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

import pages

class WikipediaCommon(unittest.TestCase):

	def setUp(self):
		if browser == 'firefox':
			self.driver = webdriver.Firefox(executable_path='/selenium_browser_drivers/geckodriver')
		elif browser == 'ie':
			self.driver = webdriver.Ie()
		elif browser == 'chrome':
			self.driver = webdriver.Chrome(executable_path='/selenium_browser_drivers/chromedriver')
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

@unittest.skip('')
class TestHomePage(WikipediaCommon):

	@unittest.skip('')
	def test_homepage_title(self):
		self.open_home_page()
		self.verify_home_page_title()

	@unittest.skip('')
	# Safari doesn't display a tab unless multiple tabs are open.
	def test_homepage_article_search(self):
		search_term = "Buster Keaton"
		self.open_home_page()
		self.submit_search(search_term)
		self.verify_article_page(search_term)

	@unittest.skip('')
	def test_homepage_autosuggest(self):
		self.open_home_page()
		self.type_search("bust")
		self.verify_suggestions_contain("Busta Rhymes")
		self.verify_suggestions_contain("Buster Posey")
		self.type_search("er")
		self.verify_suggestions_contain("Buster Keaton")
		self.verify_suggestions_do_not_contain("Busta Rhymes")

	#@unittest.skip('')
	def test_homepage_english_link(self):
		self.open_home_page()
		self.click_language_link('English')
		self.verify_main_page_text(
			title_text="Wikipedia, the free encyclopedia",
			body_text="the free encyclopedia that anyone can edit")

	#@unittest.skip('')
	def test_homepage_french_link(self):
		self.open_home_page()
		self.click_language_link('Français')
		self.verify_main_page_text(
			title_text="Wikipédia, l'encyclopédie libre",
			body_text="L'encyclopédie libre que chacun peut améliorer")

	#@unittest.skip('')
	def test_homepage_german_link(self):
		self.open_home_page()
		self.click_language_link('Deutsch')
		self.verify_main_page_text(
			title_text="Wikipedia – Die freie Enzyklopädie",
			body_text="Wikipedia ist ein Projekt zum Aufbau einer Enzyklopädie aus freien Inhalten")

	#@unittest.skip('')
	def test_homepage_spanish_link(self):
		self.open_home_page()
		self.click_language_link('Español')
		self.verify_main_page_text(
			title_text="Wikipedia, la enciclopedia libre",
			body_text="la enciclopedia de contenido libreque todos pueden editar")

	###############################
	# Home page support functions
	###############################

	# create the home page object and open the page
	def open_home_page(self):
		self.home = pages.HomePage(self.driver)
		self.home.open_home_page()

	def verify_home_page_title(self):
		self.assertEqual(self.home.get_page_title(), "Wikipedia")

	def submit_search(self, search_term):
		self.open_home_page()
		self.home.enter_search_term(search_term)
		self.home.submit_search()

	def click_language_link(self, lang):
		self.home.click_language_link(lang)

	def verify_article_page(self, search_term):
		# check the resulting page has the correct header & title
		title_regex = "^{0}.*".format(search_term)
		encoded_search_term = search_term.replace(" ", "_")
		url_regex   = ".*{0}$".format(encoded_search_term)

		article = pages.ArticlePage(self.driver)
		s = article.get_page_title()
		self.assertTrue(re.search(title_regex, s), 
			"Page title '{}' does not start with search term '{}'".format(s, search_term))
		s = article.get_current_url()
		self.assertTrue(re.search(url_regex, s), 
			"URL '{}' does not end with search term '{}'".format(s, encoded_search_term))
		self.assertEqual(article.get_article_header(), search_term)

	# type text into search term, but not submit
	def type_search(self, search_term):
		self.home.enter_search_term(search_term)

	def verify_suggestions_contain(self, search_str):
		suggestions = self.home.get_search_suggestions()
		titles = [suggestion['title'] for suggestion in suggestions]
		error_msg = "'{}' not found in titles {}"
		matching = [title for title in titles if title.startswith(search_str)]
		self.assertNotEqual(matching, [], error_msg.format(search_str, titles))
		
	def verify_suggestions_do_not_contain(self, search_str):
		suggestions = self.home.get_search_suggestions()
		titles = [suggestion['title'] for suggestion in suggestions]
		error_msg = "'{}' found in titles {}"
		matching = [title for title in titles if title.startswith(search_str)]
		self.assertEqual(matching, [], error_msg.format(search_str, titles))
	
	# Verify text on the main page
	# Parameters
	#   title_text - expected text in the title (browser tab)
	#   body_text - expected text somewhere in body
	#
	# declare a main-page object
	# asserts the title/tab is the expected text
	# asserts the page body contains the expected text
	def verify_main_page_text(self, title_text, body_text):
		self.main = pages.MainPage(self.driver)
		self.assertEqual(title_text, self.main.get_page_title())
		self.assertIn(body_text, self.main.get_body_text().replace("\n", ''))

@unittest.skip('')
class TestMainPage(WikipediaCommon):

	#@unittest.skip('')
	def test_mainpage_article_search(self):
		self.open_main_page()
		self.search_for_article("Disneyland")

		# check the resulting page has the correct header & title
		article = pages.ArticlePage(self.driver)
		s = article.get_page_title()
		self.assertTrue(re.search("^Disneyland.*", s), 
			"Page title '{}' is unexpected".format(s))
		s = article.get_current_url()
		self.assertTrue(re.search(".*Disneyland$", s), 
			"URL '{}'  is unexpected".format(s))
		self.assertEqual(article.get_article_header(), "Disneyland")

	#@unittest.skip('')
	def test_mainpage_autosuggest(self):
		if browser == "safari":
			self.skipTest('main page search does not return autosuggest on Safari')

		self.open_main_page()
		self.type_search("dou")
		self.verify_suggestions_start_with("dou")
		self.type_search("glas") # extend search term
		self.verify_suggestions_start_with("douglas")

	def open_main_page(self):
		self.main = pages.MainPage(self.driver)
		self.main.open_main_page()

	def search_for_article(self, search_term):
		self.main.open_article_by_search(search_term)

	# Type a search term without submitting search
	def type_search(self, search_term):
		self.main.enter_header_search_term(search_term)

	def verify_suggestions_start_with(self, search_term):
		prefix = search_term.lower()
		for suggestion in self.main.get_header_search_suggestions():
			title = suggestion['title'].lower()
			self.assertTrue(title.startswith(prefix), 
				"Suggestion '{}' expected to start with '{}'".format(title, prefix))

	def verify_suggestions_contain(self, expected_suggestion):
		titles = []
		for suggestion in self.main.get_header_search_suggestions():
			titles.append(suggestion['title'])
		self.assertIn(expected_suggestion, titles)

	def verify_suggestions_do_not_contain(self, omitted_suggestion):
		titles = []
		for suggestion in self.main.get_header_search_suggestions():
			titles.append(suggestion['title'])
		self.assertNotIn(omitted_suggestion, titles)



class TestArticlePage(WikipediaCommon):

	# Template for testing info box contents
	# Parameters:
	#   search_term: search text to open an article. 
	#     assumes search does not open a disambiguration page
	#   expected_value: list of (label, value) tuples where 
	#     label is a string contained in the left side of a row in info box
	#     value is a string contained in value on the right side.
	#       if value is None then label is not expected in info box
	def infobox_test(self, search_term, expected_values):
		main = pages.MainPage(self.driver)
		main.open_main_page()
		main.open_article_by_search(search_term)

		article = pages.ArticlePage(self.driver)
		info = article.get_infobox_contents()
		for (label, expected_value) in expected_values:
			found_value = article.get_value_from_infobox_contents(info, label)
			if expected_value == None:
				self.assertEqual(None, found_value)
			else:
				self.assertIn(expected_value, found_value)

	# Return the list of labels, value pairs for testing info box
	# The expected value for each label is None (not present in infox) by default, 
	# but is overriden by the tuples passed through args parameter.
	def create_expected_values(self, *args):
		return_list = [
			('Directed', None), ('Starring', None),            # movies
			('Born', None), ('Relatives', None),               # people
			('atomic weight', None), ('Phase at STP', None),   # chemical element
			('Currency', None), ('Capital', None),             # countries
			('Significance', None), ('Frequency', None),       # holidays
			('Songwriter(s)', None), ('Recorded', None)        # song
		]
		new_pairs = list(args)
		for idx in range(0, len(return_list)):
			for pair in new_pairs:
				if return_list[idx][0] == pair[0]: 
					return_list[idx] = pair 
					new_pairs.remove(pair)  # remove after it's inserted into return list
					break
			if not new_pairs:  # break main loop if no args left to insert
				break

		# insert any remaining args into return list
		for pair in new_pairs:
			return_list.append(pair)
		
		return return_list

	#@unittest.skip('')
	def test_infobox_for_country(self):
		expected_values = self.create_expected_values(
			('Currency', "Sol"), ('Capital', "Lima"))
		self.infobox_test("Peru", expected_values)

	#@unittest.skip('')
	def test_infobox_for_chemistry(self):
		expected_values = self.create_expected_values(
			('atomic weight', "15.999"), ('Phase at STP', "gas"))
		self.infobox_test("Oxygen", expected_values)

	#@unittest.skip('')
	def test_infobox_for_person(self):
		expected_values = self.create_expected_values(
			('Born', '1889'), ('Relatives', 'Chaplin'))
		self.infobox_test("Charlie Chaplin", expected_values)

	#@unittest.skip('')
	def test_infobox_for_movie(self):
		expected_values = self.create_expected_values(
			('Directed', 'Alfred Hitchcock'), ('Starring', 'Cary Grant'))
		self.infobox_test("north by northwest", expected_values)

	#@unittest.skip('')
	def test_infobox_for_holiday(self):
		expected_values = self.create_expected_values(
			('Significance', 'pranks'), ('Frequency', 'Annual'))
		self.infobox_test("april fool's day", expected_values)

	#@unittest.skip('')
	def test_infobox_for_song(self):
		expected_values = self.create_expected_values(
			('Recorded', '1968'), ('Songwriter(s)', 'Lennon'))
		self.infobox_test("rocky raccoon", expected_values)

	@unittest.skip('')
	def test_compare_toc_to_headlines(self):
		main = pages.MainPage(self.driver)
		main.open_main_page()
		main.open_article_by_search("Douglas Adams")

		article = pages.ArticlePage(self.driver)
		toc = article.get_toc_items_text()
		headlines = article.get_headlines_text()
		self.assertEqual(toc, headlines)

class TestCurrentEventsPage(WikipediaCommon):

	# Verify the contents of the current 'current events' page
	def verify_current_events_page(self, month, year, days_ascending=True):
		ce = pages.CurrentEventsPage(self.driver)
		dates = ce.get_date_headers()

		days = []
		for date in dates:
			self.assertRegex(date, ce.simple_date_regex)  # header is expected format
			date_parsed = ce.parse_date_header(date)
			self.assertEqual(month, date_parsed[0])  # current month
			self.assertEqual(year, date_parsed[2])  # current year
			days.append( (int(date_parsed[2]), 
				          ce.month_index(date_parsed[0]), 
				          int(date_parsed[1])) )	
		# days are in descending order
		self.assertEqual(days, sorted(days, reverse=(not days_ascending)))

	@unittest.skip('')
	def test_main_current_events_page(self):
		main = pages.MainPage(self.driver)
		main.open_main_page()
		main.click_left_panel_link("Current events")
		now = datetime.datetime.now()
		ascending = False
		self.verify_current_events_page(
			now.strftime('%B'), now.strftime('%Y'), ascending)

	@unittest.skip('')
	def test_main_archive_current_events_page(self):
		main = pages.MainPage(self.driver)
		main.open_main_page()
		main.click_left_panel_link("Current events")
		# Randomly select month and year from full years. TO-DO select from entire archive
		year = str(random.randint(1995, 2018)) 
		month = main.month_name(random.randint(1,12))
		print("Verifying {} {}".format(month, year))
		ascending = True
		ce = pages.CurrentEventsPage(self.driver)
		ce.click_link_archived_month(month, year)
		self.verify_current_events_page(month, year, ascending)


if __name__ == '__main__':
	supported_browsers = ['firefox', 'ie', 'chrome', 'safari']
	if (len(sys.argv) == 2) and (sys.argv[1] in supported_browsers):
		global browser 
		browser = sys.argv[1]
		del sys.argv[1]  # remove so that unittest doesn't attempt to process argument
		unittest.main(verbosity=2)
	else:
		print("Argument missing or invalid. Expected one of",str(supported_browsers)[1:-1])

