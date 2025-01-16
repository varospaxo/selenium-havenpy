# Selenium Havenpy

This document outlines the usage of various commands to interact with web elements effectively using Selenium Havenpy. Below are the detailed instructions and formats for the commands.

---

## Input Fields

- **Help**: Shows instructions to use the tool.
- **Select a Browser**: Choose a browser from the supported list. Supported browsers include **Chrome** and **Firefox**.
- **URL**: Add the source URL.
- **Main Actions**: Add actions to perform.
- **Prefix Actions**: Add actions to execute before every main action.
- **Suffix Actions**: Add actions to execute after every main action.
- **Folder Name**: Specify the folder name to save the script.
- **Script Name**: Specify the script name.


## API Requests

Add an API call to the Selenium script.
- **Format**: `request|<Base64 encoded cURL>`
- **Example**: `request|Y3VybCAtLWxvY2F0aW9u...`

To generate the Base64 cURL:
1. Click on the "Add API" button.
2. Enter the cURL command (Postman format) and click "Parse cURL."
3. Select the request method and make changes to headers/data.
4. Click "Convert to Action Format" and then "Copy Action."
5. Paste the result into the "Main Actions" field.
## Command Formats

### 0. **Log Statements**
Logs a message or variable into the logger.
- **Format**: `log|type|str(string)/var(variable)|output content`
- **Example**:  
  `log|info|str|Hello World`  
  `log|debug|var|response.text`

---

### 1. **Add Comment**
Add a comment to the script.
- **Format**: `<blank>/#/comment|Comment Text`
- **Example**: `#/comment|This is a test comment`

---

### 2. **Click**
Perform a click action on the specified element.
- **Format**: `click|XPath|coordinates(optional)|resolution(optional)`
- **Example**: `click|//button[@id=submit]|100,200|1920x1080`

---

### 3. **Input Text**
Enter text into an input field.
- **Format**: `input|XPath|text|type|encoding/None`
- **Examples**:  
  Single line: `input|//input[@name=username]|test_user|text|None`  
  Multi-line (Base64): `input|//textarea[@id=description]|U29tZSBtdWx0aS1saW5lIHRleHQ=|textarea|encoded`

---

### 4. **Submit Form**
Submit a form element.
- **Format**: `submit|XPath(form)`
- **Example**: `submit|//form[@id=loginForm]`

---

### 5. **Sleep**
Pause execution for a specified duration.
- **Format**: `sleep|seconds`
- **Example**: `sleep|5`

---

### 6. **Wait**
Wait for a specific condition to be met on an element.
- **Format**: `wait|XPath|until/until_not|mode|timeout`
- **Modes**:  
  - **visible**: Wait until the element is visible.  
  - **invisible**: Wait until the element is not visible.  
  - **clickable**: Wait until the element is clickable.  
  - **presence**: Wait until the element is present in the DOM.  
  - **staleness**: Wait until the element becomes stale (is no longer attached to the DOM).  
  - **selected**: Wait until the element is selected.  
  - **deselected**: Wait until the element is deselected.  
  - **text_to_be_present**: Wait until the specified text is present in the element.  
  - **text_to_be_present_in_value**: Wait until the specified text is present in the element's value.  
  - **frame_to_be_available**: Wait until the frame is available and switch to it.  
  - **alert_is_present**: Wait until an alert is present.  
  - **title_contains**: Wait until the title contains the specified text.  
  - **title_is**: Wait until the title is exactly the specified text.  
  - **url_contains**: Wait until the URL contains the specified text.  
  - **url_matches**: Wait until the URL matches the specified pattern.  
  - **url_to_be**: Wait until the URL is exactly the specified URL.  
  - **url_changes**: Wait until the URL changes.  
  - **number_of_windows_to_be**: Wait until the number of open windows matches the specified count.  
  - **new_window_is_opened**: Wait until a new window is opened.  
  - **element_located_to_be_selected**: Wait until the located element is selected.  
  - **element_selection_state_to_be**: Wait until the element's selection state matches the specified state.  
  - **element_located_selection_state_to_be**: Wait until the located element's selection state matches the specified state.  


- **Examples**:  
  
      wait|//div[@id='example']|until|visible|7|
      wait|//div[@id='example']|until|invisible|7|
      wait|//button[@id='submit']|until|clickable|7|
      wait|//span[@class='status']|until|presence|7|
      wait|//div[@id='staleElement']|until|staleness|7|
      wait|//input[@id='checkbox']|until|selected|7|
      wait|//input[@id='checkbox']|until|deselected|7|
      wait|//div[@id='message']|until|text_to_be_present|7|Hello World
      wait|//input[@id='textbox']|until|text_to_be_present_in_value|7|Example Value
      wait|//iframe[@id='frame']|until|frame_to_be_available|7|
      wait||until|alert_is_present|7|
      wait||until|title_contains|7|Page Title
      wait||until_not|title_is|7|Exact Page Title
      wait||until|url_contains|7|example.com
      wait||until|url_matches|7|https://example.com
      wait||until|url_to_be|7|https://example.com/home
      wait||until|url_changes|7|
      wait||until_not|number_of_windows_to_be|7|2
      wait||until|new_window_is_opened|7|
      wait|//input[@id='checkbox']|until|element_located_to_be_selected|7|
      wait|//input[@id='checkbox']|until|element_selection_state_to_be|7|True
      wait|//input[@id='checkbox']|until|element_located_selection_state_to_be|7|False

---

### 7. **Scroll**
Scroll to the bottom of the page.
- **Format**: `scroll`
- **Example**: `scroll`

---

### 8. **Scroll Up**
Scroll to the top of the page.
- **Format**: `scroll_up`
- **Example**: `scroll_up`

---

### 9. **Scroll to Element**
Scroll to make an element visible.
- **Format**: `scroll_to|XPath`
- **Example**: `scroll_to|//div[@id=content]`

---

### 10. **Scroll by Offset**
Scroll by specific x and y axes.
- **Format**: `scroll_by|x-axis|y-axis|resolution`
- **Example**: `scroll_by|0|500|1920x1080`

---

### 11. **Hover**
Hover over an element.
- **Format**: `hover|XPath`
- **Example**: `hover|//button[@class=menu]`

---

### 12. **Right Click**
Perform a right-click on an element.
- **Format**: `right_click|XPath`
- **Example**: `right_click|//div[@id=context-menu]`

---

### 13. **Double Click**
Perform a double-click on an element.
- **Format**: `double_click|XPath`
- **Example**: `double_click|//button[@class=edit]`

---

### 14. **Drag and Drop**
Drag and drop an element to a target location.
- **Format**: `drag_and_drop|sourceXPath|targetXPath`
- **Example**: `drag_and_drop|//div[@id=item]|//div[@id=target]`

---

### 15. **Drag by Offset**
Drag an element by a specific offset.
- **Format**: `drag_and_drop_by|XPath|x|y`
- **Example**: `drag_and_drop_by|//div[@id=item]|100|200`

---

### 16. **Accept Alert**
Accept a browser alert.
- **Format**: `accept_alert`
- **Example**: `accept_alert`

---

### 17. **Dismiss Alert**
Dismiss a browser alert.
- **Format**: `dismiss_alert`
- **Example**: `dismiss_alert`

---

### 18. **Send Keys to Alert**
Send keys to an alert input box.
- **Format**: `send_keys_alert|text`
- **Example**: `send_keys_alert|username123`

---

### 19. **Get Alert Text**
Retrieve the text of an alert.
- **Format**: `get_alert_text`
- **Example**: `get_alert_text`

---

### 20. **Set Alert Text**
Create a custom alert with a message.
- **Format**: `set_alert_text|text`
- **Example**: `set_alert_text|Hello World`

---

### 21. **Get Attribute**
Get a specified attribute of an element.
- **Format**: `get_attribute|XPath|attributeName`
- **Example**: `get_attribute|//input[@id=username]|value`

---

### 22. **Get CSS Value**
Retrieve the CSS value of a property for an element.
- **Format**: `get_css_value|XPath|property`
- **Example**: `get_css_value|//div[@id=box]|color`

---

### 23. **Get Property**
Retrieve a property of an element.
- **Format**: `get_property|XPath|propertyName`
- **Example**: `get_property|//input[@id=checkbox]|checked`

---

### 24. **Get Text**
Retrieve the text content of an element.
- **Format**: `get_text|XPath`
- **Example**: `get_text|//p[@id=message]`

---

### 25. **Get Title**
Retrieve the page title.
- **Format**: `get_title`
- **Example**: `get_title`

---

### 26. **Get URL**
Retrieve the current page URL.
- **Format**: `get_url`
- **Example**: `get_url`

---

### 27. **Get Page Source**
Retrieve the HTML source of the current page.
- **Format**: `get_page_source`
- **Example**: `get_page_source`

---

### 28. **Get Cookies**
Retrieve all browser cookies.
- **Format**: `get_cookies`
- **Example**: `get_cookies`

---

### 29. **Add Cookie**
Add a new browser cookie.
- **Format**: `add_cookie|cookieData`
- **Example**: `add_cookie|{name: session, value: 12345}`

---

### 30. **Delete Cookie**
Delete a specific browser cookie.
- **Format**: `delete_cookie|cookieName`
- **Example**: `delete_cookie|session`

---

### 31. **Delete All Cookies**
Delete all browser cookies.
- **Format**: `delete_all_cookies`
- **Example**: `delete_all_cookies`

---

### 32. **Capture Screenshot**
Capture a screenshot of the browser viewport.
- **Format**: `ss/screenshot|filename(optional)`
- **Examples**:  
  `ss`  
  `screenshot|test`

---

**Note**: Avoid using XPaths and inputs with single quotes `'`.
