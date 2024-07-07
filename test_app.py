from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchWindowException

@pytest.fixture
def setup():
    driver = webdriver.Chrome()  # Ensure you have chromedriver installed and in PATH
    driver.get("file:///C:/Harsh_Personal/Automation/multipletab_testing_selenium_pytest/index.html")  # Use 'file://' for local files
    yield driver
    driver.quit()

def test_text_transfer(setup):
    driver = setup

    # Find the text field and enter some text
    text_field = driver.find_element(By.ID, 'textField')
    text_field.send_keys('Hello, World!')

    # Click the button to open a new tab
    button = driver.find_element(By.XPATH, '//button')
    button.click()
    print(driver.window_handles)
    try:
        # Wait for the new tab to open and then switch to it
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[1])
        
        # Wait until the element with id 'displayText' is present in the new tab
        wait = WebDriverWait(driver, 10)
        display_text = wait.until(EC.visibility_of_element_located((By.XPATH, "//p[@id='displayText']")))
        
        # Print the page source for debugging
        print(driver.page_source)

        # Verify the text is present in the new tab
        assert display_text.text == 'Hello, World!'
    
    except NoSuchWindowException:
        print("Window not found")
        assert False
    
    except TimeoutException:
        print("Element not found within the timeout period")
        # Print the page source for debugging
        print(driver.page_source)
        assert False

if __name__ == "__main__":
    pytest.main()
