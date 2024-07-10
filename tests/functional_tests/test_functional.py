# import pytest
# from flask_testing import LiveServerTestCase
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from flask import url_for, Flask


# @pytest.fixture
# def driver():
#     driver = webdriver.Chrome()
#     yield driver
#     driver.quit()


# class MyTest(LiveServerTestCase):

#     def create_app(self):
#         app = Flask(__name__)
#         app.config["TESTING"] = True
#         # Default port is 5000
#         app.config["LIVESERVER_PORT"] = 8943
#         # Default timeout is 5 seconds
#         app.config["LIVESERVER_TIMEOUT"] = 10
#         return app

#     def test_index_page(driver, live_server):
#         driver.get(live_server + url_for("index"))
#         assert "Welcome" in driver.page_source


# def test_login_and_show_summary(driver, live_server):
#     driver.get(live_server + url_for("index"))

#     # Find the email input and submit button
#     email_input = driver.find_element(By.NAME, "email")
#     email_input.send_keys("test@example.com")
#     email_input.send_keys(Keys.RETURN)

#     # Wait for the next page to load
#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Welcome')]")))

#     assert "Welcome, test@example.com" in driver.page_source


# def test_book_places(driver, live_server):
#     driver.get(live_server + url_for("showSummary", email="test@example.com"))

#     # Find and click the book button for the first competition
#     book_button = driver.find_element(By.LINK_TEXT, "Book Places")
#     book_button.click()

#     # Wait for the booking page to load
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Booking for')]"))
#     )

#     places_input = driver.find_element(By.NAME, "places")
#     places_input.send_keys("2")
#     places_input.send_keys(Keys.RETURN)

#     # Check the success message
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located(
#             (By.XPATH, "//div[contains(@class, 'flash') and contains(text(), 'Great-booking complete!')]")
#         )
#     )

#     assert "Great-booking complete!" in driver.page_source


# def test_logout(driver, live_server):
#     driver.get(live_server + url_for("showSummary", email="test@example.com"))

#     # Find and click the logout button
#     logout_button = driver.find_element(By.LINK_TEXT, "Logout")
#     logout_button.click()

#     # Wait for the index page to load
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located(
#             (By.XPATH, "//h1[contains(text(), 'Welcome to the GUDLFT Registration portal!')]")
#         )
#     )

#     assert "Welcome to the GUDLFT Registration portal!" in driver.page_source
