
The project demonstrates Selenium with Python used in a page-object model to verify web elements on the Wikipedia.org site. Test cases are defined with the unittest framework.

Project organization
* test_wikipedia.py - test cases are defined in the test_* methods in the Test* classes. Also defined in the Test* classes are supporting methods which are intermediaries between the tests case and page class methods.
* pages.py - \*Page classes contain web element locators and methods to interact with them.


# Prerequisites #
* Python3
* Python bindings for Selenium
* Selenium browser drivers are in the directory referenced in test_wikipedia.py setup() method.

Installation for supporting Selenium components can be found at 

https://selenium-python.readthedocs.io/installation.html

# Usage
In terminal window
1. navigate to folder with test scripts
2. enter command: ```python3 test_wikipedia <browser>```

	where _browser_ is one of chrome, safari, firefox or ie


# Coding examples

**Decorator**
* Defined in new_url_and_title in wait_for.py. 
* Used with click_link(), submit_search() and others in pages.py

**Stale Element Reference exception**
* get_search_suggestions() and get_header_search_suggestions() in pages.py

**Dynamic element** - Suggestions dropdown on input field
* get_search_suggestions() and get_header_search_suggestions() in pages.py

