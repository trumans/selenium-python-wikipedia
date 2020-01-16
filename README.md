
The project uses Selenium WebDriver with Python and a page-object model structure to verify web elements on Wikipedia.org. Test cases are defined with the PyUnit/unittest framework.

Project organization
* **test_wikipedia.py** - defines test cases using the PyUnit convention of method names beginning with "test_" in the class names beginning with "Test". Test case methods call helper functions defined in the same class which create page object instances and call related methods. This aids readability by allowing tests definitions to have a concise sequence of function calls.
* **pages.py** - defines classes for each page containing web element locators and methods to interact with the elements.


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

