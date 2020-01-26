
The project uses Python and Selenium WebDriver with a page-object model structure to verify Wikipedia.org. Test cases use the PyUnit/unittest framework.

# Code organization #
## test_wikipedia.py ## 
**Test Cases**
* Test cases are methods with names beginning with "test_" in the class names that begin with "Test".
* Test cases begin with calling an open_some_page method to receive a page object which it passes to helper functions that interact or verify with the page.
* Whenever a test case calls a method that triggers a new page, it expects to receive a page object from the method for the new page.

**Helper Functions**
* Defined in the class with test cases they support
* When called their first parameter is generally a page object needed to call the methods that call Selenium. Generally they do not directly call Selenium
* Handle verification logic and assertions about a page
* Helper methods that trigger the need for a new page object (e.g. click which opens an new page) returns the appropriate page object for the destination page
## pages.py ##
* Defines classes for each web page 
* Defines web element locators and methods that call Selenium.
* Limited to interacting or retrieving elements, attributes or text from the web page. Does not evaluate or verify the page.
## wait_for.py ##
* Decorator to wait for a web element to be present before continuing.


# Prerequisites #
* Python3
* Selenium for Python
* Selenium browser drivers are in the directory referenced in test_wikipedia.py - WikipediaCommon class - setUp method.

Installation for supporting Selenium components can be found at 

https://selenium-python.readthedocs.io/installation.html

# Execution
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

