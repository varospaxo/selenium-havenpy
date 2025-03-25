import base64
import json
import re
import os

class RobotFrameworkScriptGenerator:
    def generate_script(self, url, actions, csv_name):
        """
        Generate a comprehensive Robot Framework script based on the provided actions
        
        :param url: Starting URL of the web application
        :param actions: List of actions to perform
        :param csv_name: CSV file containing input values
        """
        # Start building the script
        script = self._generate_settings()
        script += self._generate_variables(csv_name)
        script += self._generate_keywords()
        script += self._generate_test_cases(url, actions)
        
        return script

    def _generate_settings(self):
        """Generate the comprehensive settings section of the Robot Framework script"""
        return (
            "*** Settings ***\n"
            "Documentation    Comprehensive Automated Web Test Script\n"
            "Library    SeleniumLibrary\n"
            "Library    OperatingSystem\n"
            "Library    Collections\n"
            "Library    DateTime\n"
            "Library    RequestsLibrary\n"
            "Library    String\n\n"
        )

    def _generate_variables(self, csv_name):
        """Generate variables section, including CSV input processing"""
        return (
            "*** Variables ***\n"
            f"${{{csv_name}}}\n"
            "@{INPUT_VALUES}    Read CSV File    ${csv_name}\n"
            "${STEP_COUNTER}    Set Variable    0\n\n"
        )

    def _generate_keywords(self):
        """Define comprehensive custom keywords for the script"""
        return (
            "*** Keywords ***\n"
            "Read CSV File\n"
            "    [Arguments]    ${file_path}\n"
            "    ${data}=    Read CSV File With Headers    ${file_path}\n"
            "    [Return]    ${data}\n\n"
            
            "Safe Click\n"
            "    [Arguments]    ${locator}\n"
            "    Wait Until Element Is Visible    ${locator}    timeout=10s\n"
            "    Click Element    ${locator}\n\n"
            
            "Safe Input\n"
            "    [Arguments]    ${locator}    ${text}\n"
            "    Wait Until Element Is Visible    ${locator}    timeout=10s\n"
            "    Clear Element Text    ${locator}\n"
            "    Input Text    ${locator}    ${text}\n\n"
            
            "Scroll To Element\n"
            "    [Arguments]    ${locator}\n"
            "    Scroll Element Into View    ${locator}\n\n"
            
            "Capture Timestamped Screenshot\n"
            "    [Arguments]    ${filename}=NONE\n"
            "    ${timestamp}=    Get Current Date    result_format=%Y%m%d_%H%M%S\n"
            "    Run Keyword If    '${filename}' == 'NONE'    Capture Page Screenshot    screenshot_${timestamp}.png\n"
            "    Run Keyword Unless    '${filename}' == 'NONE'    Capture Page Screenshot    ${filename}\n\n"
            
            "Increment Step Counter\n"
            "    ${STEP_COUNTER}=    Evaluate    ${STEP_COUNTER} + 1\n"
            "    Log    Step ${STEP_COUNTER}\n\n"
            
            "Perform Right Click\n"
            "    [Arguments]    ${locator}\n"
            "    Open Context Menu    ${locator}\n\n"
            
            "Perform Double Click\n"
            "    [Arguments]    ${locator}\n"
            "    Double Click Element    ${locator}\n\n"
            
            "Drag And Drop Elements\n"
            "    [Arguments]    ${source_locator}    ${target_locator}\n"
            "    Drag And Drop    ${source_locator}    ${target_locator}\n\n"
            
            "Handle Browser Alert\n"
            "    [Arguments]    ${action}    ${text}=NONE\n"
            "    Run Keyword If    '${action}' == 'accept'    Alert Should Be Present\n"
            "    Run Keyword If    '${action}' == 'accept'    Handle Alert\n"
            "    Run Keyword If    '${action}' == 'dismiss'    Handle Alert    DISMISS\n"
            "    Run Keyword If    '${action}' == 'send_keys' and '${text}' != 'NONE'    Input Text Into Alert    ${text}\n\n"
            
            "Get Element Attribute\n"
            "    [Arguments]    ${locator}    ${attribute}\n"
            "    ${value}=    Get Element Attribute    ${locator}    ${attribute}\n"
            "    [Return]    ${value}\n\n"
            
            "Get Element CSS Value\n"
            "    [Arguments]    ${locator}    ${property}\n"
            "    ${value}=    Get Element Attribute    ${locator}    css=${property}\n"
            "    [Return]    ${value}\n\n"
        )

    def _generate_test_cases(self, url, actions):
        """Generate test cases based on provided actions"""
        script = "*** Test Cases ***\n"
        script += "Web Automation Test\n"
        script += f"    Open Browser    {url}    browser=chrome\n"
        script += "    Maximize Browser Window\n"
        
        for index, action in enumerate(actions):
            script += self._generate_action(index, action)
        
        script += "    Close Browser\n"
        return script

    def _generate_action(self, index, action):
        """Convert individual actions to Robot Framework steps"""
        action_type, xpath, coords, viewport, timeout, text = action
        action_script = ""

        if action_type == "click":
            # Handle coordinate-based clicks if needed
            action_script += f"    Safe Click    {xpath}\n"
        
        elif action_type in ["type", "input"]:
            # Handle both single and multi-line inputs
            if timeout == "encoded":
                # action_script += f"    ${decoded_value}=    Decode Base64    ${{INPUT_VALUES}}[input_value_{index}]\n"
                action_script += f"    Safe Input    {xpath}    ${{decoded_value}}\n"
            else:
                action_script += f"    Safe Input    {xpath}    ${{INPUT_VALUES}}[input_value_{index}]\n"
        
        elif action_type == "paste":
            # Simulate paste action
            action_script += f"    Press Keys    {xpath}    CTRL+v\n"
        
        elif action_type == "submit":
            action_script += f"    Submit Form    {xpath}\n"
        
        elif action_type == "hover":
            action_script += f"    Mouse Over    {xpath}\n"
        
        elif action_type == "right_click":
            action_script += f"    Perform Right Click    {xpath}\n"
        
        elif action_type == "double_click":
            action_script += f"    Perform Double Click    {xpath}\n"
        
        elif action_type == "drag_and_drop":
            action_script += f"    Drag And Drop Elements    {xpath}    {coords}\n"
        
        elif action_type == "drag_and_drop_by":
            # Note: Robot Framework doesn't have direct support for drag by offset
            action_script += f"    Execute JavaScript    var elem = document.evaluate('{xpath}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;\n"
            action_script += f"    ...    elem.style.transform = 'translate({coords}px, {viewport}px)';\n"
        
        elif action_type == "wait":
            condition_map = {
                "visible": "Wait Until Element Is Visible",
                "invisible": "Wait Until Element Is Not Visible",
                "clickable": "Wait Until Element Is Enabled",
                "presence": "Wait Until Page Contains Element",
                "staleness": "Wait Until Page Does Not Contain Element",
                "selected": "Checkbox Should Be Selected",
                "text_to_be_present": "Page Should Contain"
            }
            
            if viewport in condition_map:
                action_script += f"    {condition_map[viewport]}    {xpath}    timeout={timeout}s\n"
        
        elif action_type == "scroll":
            action_script += "    Scroll To Bottom\n"
        
        elif action_type == "scroll_up":
            action_script += "    Scroll To Top\n"
        
        elif action_type == "scroll_to":
            action_script += f"    Scroll To Element    {xpath}\n"
        
        elif action_type == "scroll_by":
            # Use JavaScript for precise scrolling
            action_script += f"    Execute JavaScript    window.scrollBy({xpath}, {coords})\n"
        
        elif action_type == "accept_alert":
            action_script += "    Handle Browser Alert    accept\n"
        
        elif action_type == "dismiss_alert":
            action_script += "    Handle Browser Alert    dismiss\n"
        
        elif action_type == "send_keys_alert":
            action_script += f"    Handle Browser Alert    send_keys    {xpath}\n"
        
        elif action_type == "get_alert_text":
            action_script += "    ${alert_text}=    Get Alert Message\n"
        
        elif action_type == "set_alert_text":
            action_script += f"    Execute JavaScript    window.alert('{xpath}')\n"
        
        elif action_type == "get_attribute":
            action_script += f"    ${{{coords}_value}}=    Get Element Attribute    {xpath}    {coords}\n"
        
        elif action_type == "get_css_value":
            action_script += f"    ${{{coords}_value}}=    Get Element CSS Value    {xpath}    {coords}\n"
        
        # elif action_type == "get_text":
        #     action_script += f"    ${text_value}=    Get Text    {xpath}\n"
        
        elif action_type == "get_title":
            action_script += "    ${page_title}=    Get Title\n"
        
        elif action_type == "get_url":
            action_script += "    ${current_url}=    Get Location\n"
        
        elif action_type == "get_page_source":
            action_script += "    ${page_source}=    Get Source\n"
        
        elif action_type == "get_cookies":
            action_script += "    ${cookies}=    Get Cookies\n"
        
        elif action_type == "add_cookie":
            action_script += f"    Add Cookie    {xpath}\n"
        
        elif action_type == "delete_cookie":
            action_script += f"    Delete Cookie    {xpath}\n"
        
        elif action_type == "delete_all_cookies":
            action_script += "    Delete All Cookies\n"
        
        elif action_type == "request":
            # Convert curl to Robot Framework request
            curl_command = base64.b64decode(xpath).decode('utf-8')
            url_match = re.search(r"curl --location '(.*?)'", curl_command)
            url = url_match.group(1) if url_match else None
            
            # Extract headers and method
            headers = {}
            for header_match in re.finditer(r"--header '(.*?): (.*?)'", curl_command):
                headers[header_match.group(1)] = header_match.group(2)
            
            method_match = re.search(r"-X\s+['\"](\w+)['\"]", curl_command)
            method = method_match.group(1) if method_match else "GET"
            
            action_script += f"    Create Session    req    {url}\n"
            
            # Add headers if present
            if headers:
                headers_str = " ".join([f"&{{HEADERS}}[{k}]={v}" for k, v in headers.items()])
                action_script += f"    &{{HEADERS}}    {headers_str}\n"
                action_script += f"    ${{response}}=    {method} On Session    req    /    headers=${{HEADERS}}\n"
            else:
                action_script += f"    ${{response}}=    {method} On Session    req    /\n"
            
            action_script += "    Log    ${response.text}\n"
        
        elif action_type == "step":
            action_script += "    Increment Step Counter\n"
        
        elif action_type in ["ss", "screenshot"]:
            if xpath:
                action_script += f"    Capture Timestamped Screenshot    {xpath}\n"
            else:
                action_script += "    Capture Timestamped Screenshot\n"
        
        elif action_type == "log":
            log_levels = {
                "info": "Log",
                "warning": "Log Warning",
                "error": "Log Error",
                "debug": "Log Debug",
                "critical": "Log Critical"
            }
            
            if xpath in log_levels:
                if coords == "var":
                    action_script += f"    {log_levels[xpath]}    {viewport}\n"
                else:
                    action_script += f"    {log_levels[xpath]}    '{viewport}'\n"
        
        return action_script

# Example usage comment
# generator = RobotFrameworkScriptGenerator()
# script = generator.generate_script(url, actions, csv_name)
# print(script)