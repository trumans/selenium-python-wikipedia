from datetime import datetime
import unittest
import random

from pages.main_page import MainPage
from pages.current_events_page import CurrentEventsPage

from tests.wikipedia_common import WikipediaCommon

class TestCurrentEventsPage(WikipediaCommon):

	#@unittest.skip('')
	def test_main_current_events_page(self):
		ce_page = self.navigate_to_current_events_page()
		now = datetime.now()
		self.verify_date_headers(ce_page,
			now.strftime('%B'), now.strftime('%Y'), days_ascending=False)

	#@unittest.skip('')
	def test_main_archived_current_events_page(self):
#		if browser == "safari":
#			self.skipTest('Safari does not locate month_year link')

		ce_page = self.navigate_to_current_events_page()
		month, year = self.select_random_month_year(ce_page)
		self.verify_date_headers(ce_page, month, year, days_ascending=True)

	def test_archived_months_link_text(self):
		ce_page = self.navigate_to_current_events_page()
		self.verify_archives_link_text(ce_page)

	####################
	# Helper functions
	####################

	# Click link to Current Events on left panel
	#   returns an CurrentEvents page object
	def navigate_to_current_events_page(self):
		self.main = MainPage(self.driver)
		self.main.open_main_page()
		self.main.click_left_panel_link("Current events")
		return CurrentEventsPage(self.driver)

	# Return the expected first and last month of an archived year
	#   parameter
	#     ce - CurrentEventsPage object
	#     year - integer in the range of first archived and current year
	#   returns
	#     tuple of integers (first_month, last_month)
	def get_month_range(self, ce, year):
		current_year = datetime.now().year

		# raise exception if year is out of range
		if year < ce.first_archived_year or year > current_year:
			msg = "Year must be between {} and {}, value is {}."
			raise ValueError(msg.format(ce.first_archived_year, current_year, year))

		first_month = 1
		last_month = 12
		# adjust month range, as necessary
		if year == ce.first_archived_year:
			first_month = ce.first_archived_month
		elif year == current_year:
			last_month = datetime.now().month

		return (first_month, last_month)

	# Randomly select a month from the archives at the bottom of the page
	#   Earliest expected archive is July 1994
	#   Latest expected archive is the current month
	# parameter
	#   ce_page - CurrentEvents page object
	# returns
	#   the tuple (month, year) which was selected
	def select_random_month_year(self, ce_page):
		year = random.randint(ce_page.first_archived_year, datetime.now().year)

		first_month, last_month = self.get_month_range(ce_page, year)
		month = ce_page.month_name(random.randint(first_month, last_month))

		print("Verifying {} {}".format(month, year))
		ce_page.click_link_archived_month(month, year)
		return (month, year)

	# Verify link text on the archived months
	# parameter
	#   ce_page - CurrentEventsPage object
	# Expects groups of links from the current year to the first archived year
	#   each group has one link for the year and links for each month
	def verify_archives_link_text(self, ce_page):
		current_year = datetime.now().year

		years = ce_page.get_archive_links_by_year()
		for yr in years:

			links = ce_page.parse_archive_links(yr)

			# verify the first link is the year
			yr_str = str(current_year)
			self.assertEqual(links[0]["text"], yr_str)
			self.assertEqual(links[0]["title"], yr_str)
			self.assertRegex(links[0]["href"], ".*/wiki/" + yr_str)

			# verify the remaining links are months
			#   while most years will be months# 1-12
			#   the first archived and current year will be fewer months
			first_month, last_month = self.get_month_range(ce_page, current_year)
			current_month = first_month

			for i in range(1, len(links)):
				month_name = ce_page.month_name(current_month)

				self.assertEqual(links[i]["text"], month_name)
				regex = ".*{} {}$".format(month_name, yr_str)
				self.assertRegex(links[i]["title"], regex)
				regex = ".*/{}_{}$".format(month_name, yr_str)
				self.assertRegex(links[i]["href"], regex)

				current_month += 1

			current_year -= 1


	# Verify the headers for dates
	#   verify headers are the expected format (ex: Janurary 1, 1999 (Monday))
	#   verify dates are in sequence
	# Parameters
	#   ce_page - CurrentEventsPage object
	#   month - string, full spelling of a month
	#   year - string, YYYY format
	#   days_ascending - boolean, dates should be in ascending order if True
	#                    in descending order if False
	def verify_date_headers(self, ce_page, month, year, days_ascending=True):
		dates = ce_page.get_date_headers()

		days = []
		for date in dates:
			self.assertRegex(date, ce_page.long_date_regex)  # header is expected format
			date_parsed = ce_page.parse_date_header(date)
			self.assertEqual(month, date_parsed[0])     # expected month
			self.assertEqual(year, date_parsed[2])      # expected year
			days.append( (int(date_parsed[2]),
				          ce_page.month_index(date_parsed[0]),
				          int(date_parsed[1])) )	
		# days are in expected sequence
		self.assertEqual(days, sorted(days, reverse=(not days_ascending)))
