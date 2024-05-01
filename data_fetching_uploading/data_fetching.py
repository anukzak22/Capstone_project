
# import time 
# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException
# from selenium.common.exceptions import TimeoutException, NoAlertPresentException





# def slow_type(element, text):
#     # Loop through each character in the text
#     for char in text:
#         # Send the current character to the element
#         element.send_keys(char)
#         # Wait for a short delay (e.g., 10 milliseconds)
#         time.sleep(0.03)

# def handle_cookie_consent(driver):
#     try:
#         # Check if the cookie consent banner is present
#         cookie_banner = driver.find_element(By.ID, "onetrust-banner-sdk")
#         if cookie_banner.is_displayed():
#             # Accept all cookies

#             accept_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
#             accept_button.click()
#             print("Accepted all cookies.")
#     except:
#         pass  # No cookie consent banner found or encountered an error

# def login_to_stackoverflow(email, password):
#     # Start a Selenium WebDriver session
#     driver = webdriver.Safari()

#     try:
#         # Open the Stack Overflow login page
#         driver.get("https://stackoverflow.com/users/login?returnurl=https%3a%2f%2fstackoverflow.com%2foauth%3fclient_id%3d18243%26scope%3d%26redirect_uri%3dhttps%253a%252f%252fdata.stackexchange.com%252fuser%252foauth%252fstackapps%26state%3d%257b%2522ses%2522%253a%2522d00917da5d2b4ba18c8269a31f9db63d%2522%252c%2522sid%2522%253a0%252c%2522hash%2522%253a%252290b6cf52611f8d32e3b06301de141555%2522%257d")

#         # Handle cookie consent banner
#         time.sleep(5)
#         handle_cookie_consent(driver)
#         time.sleep(5)

#         # Wait for the email input field to be visible
#         email_input = driver.find_element(By.ID, "email")
#         slow_type(email_input, email)

#         # Wait for a moment
#         time.sleep(2)

#         # Find the password input field and enter the password
#         password_input = driver.find_element(By.ID, "password")
#         password_input.send_keys(password)

#         # Wait for a moment
#         time.sleep(2)

#         # Submit the login form
#         login_button = driver.find_element(By.ID, "submit-button")
#         login_button.click()

#         print("Successfully logged in to Stack Overflow!")

#         # Wait for 3 minutes
#         print("Waiting for minutes...")
#         time.sleep(10)
#     except Exception as e:
#         print("An error occurred during login:", str(e))
#         raise e

#     return driver



# def execute_query(driver, query):
#     try:
#         driver.get("https://data.stackexchange.com/stackoverflow/query/new")

#         # Wait for the CodeMirror element to be clickable
#         code_mirror_element = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.CLASS_NAME, "CodeMirror"))
#         )
#         code_mirror_element.click()

#         # Write the provided query into the CodeMirror element
#         code_mirror_element.send_keys(query)

#         # Click the submit button
#         submit_button = driver.find_element(By.ID, "submit-query")  # Adjust the ID accordingly
#         submit_button.click()
#         print("Query executed successfully!")

#         # Wait for the download button to be clickable
#         download_button = WebDriverWait(driver, 60).until(
#             EC.element_to_be_clickable((By.ID, "resultSetsButton"))
#         )
#         print("Download button appeared. Results are ready.")

#         # Click the download button
#         download_button.click()
#         print("Downloaded CSV file successfully!")

#         # Wait for the specific <li> element to appear
#         try:
#             specific_li_element = WebDriverWait(driver, 60).until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, "li.selected.last"))
#             )
#             print("Specific <li> element appeared. Waiting for 1 minute...")
#             time.sleep(60)
#             print("Download is completed.")
#         except TimeoutException:
#             print("Timed out waiting for the specific <li> element to appear.")

#         # Accept download alert if present
#         try:
#             alert = driver.switch_to.alert
#             alert.accept()
#             print("Download alert accepted.")
#         except NoAlertPresentException:
#             print("No download alert present.")

#     except TimeoutException:
#         print("Timed out waiting for elements to appear.")
#     except Exception as e:
#         print("An error occurred while executing the query:", str(e))
#         raise e


# # Example usage:
# email = "anahit_zakaryan@edu.aua.am"
# password = "200322Anuk"
# driver = login_to_stackoverflow(email, password)
# query = """
# SELECT 
#     p.Id AS [Post ID],
#     p.Title,
#     p.Body AS [Post Body],
#     p.Tags,
#     c.Text AS [Comment],
#     c.Score AS [Comment Score],
#     p.CreationDate AS [Post Creation Time]
# FROM 
#     Posts p
# LEFT JOIN 
#     Comments c ON p.Id = c.PostId
# WHERE 
#     (p.Tags LIKE '%python%'
#     OR p.Tags LIKE '%javascript%'
#     OR p.Tags LIKE '%java%'
#     OR p.Tags LIKE '%php%'
#     OR p.Tags LIKE '%programming-language%')
#     AND p.CreationDate >= DATEADD(week, -1, GETDATE())
# ORDER BY 
#     p.CreationDate DESC;
# """
# execute_query(driver, query)


# # <div id="execution-stats">5171 rows returned in 56016 ms</div>


import sys
import time 
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException, NoAlertPresentException

def slow_type(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(0.03)

def handle_cookie_consent(driver):
    try:
        cookie_banner = driver.find_element(By.ID, "onetrust-banner-sdk")
        if cookie_banner.is_displayed():
            accept_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
            accept_button.click()
            print("Accepted all cookies.")
    except:
        pass
# def handle_cookie_consent(driver):
#     try:
#         cookie_banner = driver.find_element(By.ID, "onetrust-banner-sdk")
#         if cookie_banner.is_displayed():
#             banner_actions_container = driver.find_element(By.CLASS_NAME, "banner-actions-container")
#             accept_button = None
#             try:
#                 accept_button = banner_actions_container.find_element(By.ID, "onetrust-accept-btn-handler")
#             except NoSuchElementException:
#                 pass
#             if not accept_button:
#                 try:
#                     accept_button = banner_actions_container.find_element(By.XPATH, "//button[contains(text(), 'Accept all cookies')]")
#                 except NoSuchElementException:
#                     pass
#             if not accept_button:
#                 try:
#                     accept_button = banner_actions_container.find_element(By.ID, "onetrust-reject-all-handler")
#                 except NoSuchElementException:
#                     pass
#             if accept_button:
#                 accept_button.click()
#                 print("Handled cookie consent.")
#     except NoSuchElementException:
#         pass


def login_to_stackoverflow(email, password):
    driver = webdriver.Safari()

    try:
        driver.get("https://stackoverflow.com/users/login?returnurl=https%3a%2f%2fstackoverflow.com%2foauth%3fclient_id%3d18243%26scope%3d%26redirect_uri%3dhttps%253a%252f%252fdata.stackexchange.com%252fuser%252foauth%252fstackapps%26state%3d%257b%2522ses%2522%253a%2522d00917da5d2b4ba18c8269a31f9db63d%2522%252c%2522sid%2522%253a0%252c%2522hash%2522%253a%252290b6cf52611f8d32e3b06301de141555%2522%257d")

        time.sleep(10)
        handle_cookie_consent(driver)
        time.sleep(1)
        # handle_credential_picker(driver)
        time.sleep(1)
        email_input = driver.find_element(By.ID, "email")
        slow_type(email_input, email)

        time.sleep(2)

        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys(password)

        time.sleep(5)

        login_button = driver.find_element(By.ID, "submit-button")
        login_button.click()

        print("Successfully logged in to Stack Overflow!")

        print("Waiting for minutes...")
        time.sleep(10)
    except Exception as e:
        print("An error occurred during login:", str(e))
        raise e

    return driver
    
def handle_credential_picker(driver):
    try:
        iframe_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[src*="accounts.google.com/gsi/iframe/select"]'))
        )
        print("Google credential picker iframe found.")
        # Switch to the iframe
        driver.switch_to.frame(iframe_element)
        # Click on the close button
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'close'))
        )
        close_button.click()
        print("Clicked on the close button.")
    except TimeoutException:
        print("Timed out waiting for the Google credential picker iframe.")
    except Exception as e:
        print("An error occurred while handling Google credential picker:", str(e))



# def login_to_stackoverflow(email, password):
#     driver = webdriver.Safari()

#     try:
#         driver.get("https://stackoverflow.com/users/login?returnurl=https%3a%2f%2fstackoverflow.com%2foauth%3fclient_id%3d18243%26scope%3d%26redirect_uri%3dhttps%253a%252f%252fdata.stackexchange.com%252fuser%252foauth%252fstackapps%26state%3d%257b%2522ses%2522%253a%2522d00917da5d2b4ba18c8269a31f9db63d%2522%252c%2522sid%2522%253a0%252c%2522hash%2522%253a%252290b6cf52611f8d32e3b06301de141555%2522%257d")

#         time.sleep(10)
#         handle_cookie_consent(driver)
#         time.sleep(5)

#         # Handle Google credential picker
#         handle_credential_picker(driver)
#         time.sleep(10)

#         email_input = driver.find_element(By.ID, "email")
#         slow_type(email_input, email)

#         time.sleep(2)

#         password_input = driver.find_element(By.ID, "password")
#         password_input.send_keys(password)

#         time.sleep(5)

#         login_button = driver.find_element(By.ID, "submit-button")
#         login_button.click()

#         print("Successfully logged in to Stack Overflow!")


#         print("Waiting for minutes...")
#         time.sleep(10)
#     except Exception as e:
#         print("An error occurred during login:", str(e))
#         raise e

#     return driver


def execute_query(driver, query):
    try:
        driver.get("https://data.stackexchange.com/stackoverflow/query/new")

        code_mirror_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "CodeMirror"))
        )
        time.sleep(4)
        code_mirror_element.click()

        code_mirror_element.send_keys(query)

        submit_button = driver.find_element(By.ID, "submit-query")
        submit_button.click()
        print("Query clicked!")

        download_button = WebDriverWait(driver, 50).until(
            EC.element_to_be_clickable((By.ID, "resultSetsButton"))
        )
        print("Download button appeared. Results are ready.")

        download_button.click()
        print("Downloaded CSV file successfully!")

        try:
            specific_li_element = WebDriverWait(driver, 120).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "li.selected.last"))
            )
            print("Specific <li> element appeared. Waiting for 1 minute...")
            time.sleep(90)
            print("Download is completed.")
        except TimeoutException:
            print("Timed out waiting for the specific <li> element to appear.")

        try:
            alert = driver.switch_to.alert
            alert.accept()
            print("Download alert accepted.")
        except NoAlertPresentException:
            print("No download alert present.")

    except TimeoutException:
        print("Timed out waiting for elements to appear.")
    except Exception as e:
        print("An error occurred while executing the query:", str(e))
        raise e

# def main():
#     email = "anahit_zakaryan@edu.aua.am"
#     password = "200322Anuk"
#     driver = login_to_stackoverflow(email, password)

#     # Check if the query file argument is provided
#     if len(sys.argv) < 2:
#         print("Usage: python main_script.py <query_file>")
#         driver.quit()
#         return

#     # Extract the query file argument
#     query_file = sys.argv[1]

#     # Read the contents of the query file
#     with open(query_file, 'r') as file:
#         query = file.read()

#     # Execute the query
#     execute_query(driver, query)

#     driver.quit()

# if __name__ == "__main__":


#     main()


def main():
    # email = "anahit_zakaryan@edu.aua.am"
    # password = "200322Anuk"
    credential_file_path = 'credentials.txt'  # Update with your file path

    # Read email and password from the specified credential file
    with open(credential_file_path, 'r') as file:
        lines = file.readlines()
        email = lines[0].strip()  # First line contains the email
        password = lines[1].strip() 

    driver = login_to_stackoverflow(email, password)

    # Retrieve the query file name from command-line arguments
    if len(sys.argv) != 2:
        print("Usage: python fetch_data.py <query_file>")
        sys.exit(1)

    query_file = sys.argv[1]

    # Read the contents of the query file
    with open(query_file, 'r') as file:
        query = file.read()

    # Execute the query
    execute_query(driver, query)

    driver.quit()

if __name__ == "__main__":
    main()