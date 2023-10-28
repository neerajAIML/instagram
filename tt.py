from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

# Specify the path to geckodriver executable
firefox_service = Service('geckodriver')

# Specify the path to the new Firefox profile directory
new_profile_directory = '/'

# Configure Firefox options
firefox_options = Options()
firefox_options.add_argument("-headless")  # Run Firefox in headless mode
firefox_options.set_preference("profile", new_profile_directory)

# Set the service and options when creating the Firefox webdriver
driver = webdriver.Firefox(service=firefox_service, options=firefox_options)

# Example usage: navigate to a website
driver.get("https://www.aajtak.in/")

# Close the webdriver
driver.quit()

