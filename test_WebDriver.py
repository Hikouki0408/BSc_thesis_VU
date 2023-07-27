from selenium import webdriver
from selenium.common.exceptions import JavascriptException

# Set Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run Chrome in headless mode (optional)

# Create a new instance of the Chrome browser
driver = webdriver.Chrome(options=options)

# JavaScript code to execute
script_code = '''
// JavaScript code generating dynamic content 3
        const dynamicContent3 = "This content was dynamically generated with JavaScript (content 3).";
        const dynamicContent4 = "And this is a separate dynamic content.";
        document.write(`<p>${dynamicContent3}</p>`);
        document.write(`<p>${dynamicContent4}</p>`);
'''

# Load a blank HTML page to execute the script
driver.get('data:text/html;charset=utf-8,<!DOCTYPE html><html><head></head><body></body></html>')

try:
    # Execute the JavaScript code
    driver.execute_script(script_code)

    # Extract the dynamically generated text displayed on the browser
    script_extract_text = '''
        var elements = document.querySelectorAll('body > *');
        var texts = "";
        elements.forEach(function(element) {
            texts += element.textContent + " ";
        });
        return texts.trim();
    '''
    extracted_text = driver.execute_script(script_extract_text)

    print(extracted_text)

except JavascriptException:
    # If there's a JavaScript exception, return an empty string
    extracted_text = ''

finally:
    # Close the browser
    driver.quit()



