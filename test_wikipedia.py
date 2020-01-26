import sys

import unittest

from tests.test_home_page import TestHomePage
from tests.test_main_page import TestMainPage
from tests.test_article_page import TestArticlePage
from tests.test_current_events_page import TestCurrentEventsPage
import tests.wikipedia_common

if __name__ == '__main__':
	supported_browsers = ['firefox', 'ie', 'chrome', 'safari']
	if (len(sys.argv) == 2) and (sys.argv[1] in supported_browsers):
		browser = sys.argv[1]
		tests.wikipedia_common.browser = browser
		del sys.argv[1]  # remove so that unittest doesn't attempt to process argument

		# Gather one test suite
		#tests = unittest.TestLoader().loadTestsFromTestCase(TestCurrentEventsPage)

		# Gather set of test suites
		suite_list = [
			TestHomePage,
			TestMainPage,
			TestArticlePage,
			TestCurrentEventsPage,
		]
		suites = map(unittest.TestLoader().loadTestsFromTestCase, suite_list)
		tests = unittest.TestSuite(suites)

		# Run gathered tests
		unittest.TextTestRunner(verbosity=2).run(tests)

	else:
		print("Argument missing or invalid. Expected one of",str(supported_browsers)[1:-1])

