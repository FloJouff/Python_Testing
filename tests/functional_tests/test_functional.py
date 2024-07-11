import pytest
from flask_testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import url_for, Flask


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def test_index_page(driver, live_server):
    driver.get("http://127.0.0.1:5000")
    assert "Welcome" in driver.page_source


def test_login_and_show_summary(driver, live_server):
    driver.get("http://127.0.0.1:5000")

    # Find the email input and submit button
    email_input = driver.find_element(By.NAME, "email")
    email_input.send_keys("john@simplylift.co")
    email_input.send_keys(Keys.RETURN)

    # Wait for the next page to load
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Welcome')]")))

    assert "Welcome, john@simplylift.co" in driver.page_source


def test_book_places(driver, live_server):
    driver.get("http://127.0.0.1:5000")

    # Find the email input and submit button
    email_input = driver.find_element(By.NAME, "email")
    email_input.send_keys("john@simplylift.co")
    email_input.send_keys(Keys.RETURN)

    # Wait for the next page to load
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Welcome')]")))

    # Find and click the book button for the first competition
    book_button = driver.find_element(By.LINK_TEXT, "Book Places")
    book_button.click()

    # Wait for the booking page to load
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Spring Festival')]"))
    )

    places_input = driver.find_element(By.NAME, "places")
    places_input.send_keys("2")
    places_input.send_keys(Keys.RETURN)

    # Check the success message
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//ul[contains(@class, 'flashes')]")))

    assert "Great-booking complete!" in driver.page_source


def test_logout(driver, live_server):
    driver.get("http://127.0.0.1:5000")

    # Find the email input and submit button
    email_input = driver.find_element(By.NAME, "email")
    email_input.send_keys("john@simplylift.co")
    email_input.send_keys(Keys.RETURN)

    # Wait for the welcome page to load
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Welcome')]")))

    # Find and click the logout button
    logout_button = driver.find_element(By.LINK_TEXT, "Logout")
    logout_button.click()

    # Wait for the index page to load
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.XPATH, "//h1[contains(text(), 'Welcome to the GUDLFT Registration Portal!')]")
        )
    )

    assert "Welcome to the GUDLFT Registration Portal!" in driver.page_source
