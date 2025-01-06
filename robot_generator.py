import base64
import json
import re

class ScriptGenerator:
    DEFAULT_BROWSER = "Chrome"

    def _generate_settings_section(self):
        return (
            "*** Settings ***\n"
            "Library    SeleniumLibrary\n"
            "Library    Collections\n"
            "Library    OperatingSystem\n"
            "Library    RequestsLibrary\n"
            "Library    String\n\n"
        )

    def _generate_variables_section(self, csv_name):
        return (
            "*** Variables ***\n"
            "${TIMEOUT}    5\n"
            f"${{CSV_FILE}}    {csv_name}\n\n"
        )

    def _generate_keywords_section(self):
        return (
            "*** Keywords ***\n"
            "Load CSV Variables\n"
            "    ${csv_data}=    Get File    ${CSV_FILE}\n"
            "    @{lines}=    Split To Lines    ${csv_data}\n"
            "    &{variables}=    Create Dictionary\n"
            "    FOR    ${line}    IN    @{lines}[1:]\n"
            "        ${parts}=    Split String    ${line}    ,\n"
            "        Set To Dictionary    ${variables}    ${parts}[0]=${parts}[1]\n"
            "    END\n"
            "    [Return]    ${variables}\n\n"
            "Set Viewport Size\n"
            "    [Arguments]    ${width}    ${height}\n"
            "    ${js}=    Set Variable    return [window.outerWidth - window.innerWidth + arguments[0], window.outerHeight - window.innerHeight + arguments[1]]\n"
            "    ${window_size}=    Execute Javascript    ${js}    ${width}    ${height}\n"
            "    Set Window Size    ${window_size}[0]    ${window_size}[1]\n\n"
        )

    def generate_script(self, browser, url, actions, csv_name):
        script = self._generate_settings_section()
        script += self._generate_variables_section(csv_name)
        script += self._generate_keywords_section()
        script += "*** Test Cases ***\n"
        script += "Main Test\n"
        script += f"    Open Browser    {url}    {browser}\n"
        script += "    ${variables}=    Load CSV Variables\n"
        script += self._generate_actions(actions)
        script += "    Sleep    5s\n"
        script += "    Close Browser\n"
        return script

    def _generate_actions(self, actions):
        action_script = ""
        for i, action in enumerate(actions):
            action_script += self._generate_action(i, action)
        return action_script

    def _generate_action(self, index, action):
        action_type, xpath, coords, viewport, timeout = action
        variable_name = f"input_value_{index}"
        script = "    "

        if action_type == "click":
            script += (
                "Sleep    2s\n"
                "    Wait Until Element Is Not Visible    xpath=//ion-spinner[@id='spinner']    timeout=${TIMEOUT}\n"
                f"    Wait Until Element Is Enabled    xpath={xpath}    timeout=${{TIMEOUT}}\n"
                f"    Click Element    xpath={xpath}\n"
            )
            if viewport and 'x' in viewport.lower():
                width, height = viewport.lower().split('x')
                script += f"    Set Viewport Size    {width}    {height}\n"

            if coords and ',' in coords:
                x, y = coords.split(',')
                script += f"    Click Element At Coordinates    None    {x}    {y}\n"

        elif action_type in ["type", "input"]:
            if timeout == "encoded":
                script += (
                    f"    Wait Until Element Is Visible    xpath={xpath}    timeout=${{TIMEOUT}}\n"
                    f"    ${{decoded_value}}=    Evaluate    base64.b64decode(${{variables}}['{variable_name}']).decode('utf-8')    modules=base64\n"
                    f"    Input Text    xpath={xpath}    ${{decoded_value}}\n"
                )
            else:
                script += (
                    f"    Wait Until Element Is Visible    xpath={xpath}    timeout=${{TIMEOUT}}\n"
                    f"    Input Text    xpath={xpath}    ${{variables}}['{variable_name}']\n"
                )

        elif action_type == "submit":
            script += f"    Submit Form    xpath={xpath}\n"

        elif action_type in ["#", "comment", ""]:
            script += f"# {xpath}\n"

        elif action_type == "sleep":
            script += f"    Sleep    {xpath}s\n"

        elif action_type == "wait":
            timeout = timeout if timeout else "${TIMEOUT}"
            condition_map = {
                "visible": "Wait Until Element Is Visible",
                "invisible": "Wait Until Element Is Not Visible",
                "clickable": "Wait Until Element Is Enabled",
                "presence": "Wait Until Page Contains Element",
                "staleness": "Wait Until Element Is Not Visible",
                "selected": "Wait Until Element Is Selected",
                "deselected": "Wait Until Element Is Not Selected",
            }
            if viewport in condition_map:
                condition = condition_map[viewport]
                script += f"    {condition}    xpath={xpath}    timeout={timeout}\n"

        elif action_type == "request":
            curl_command = base64.b64decode(xpath).decode('utf-8')
            method_match = re.search(r"-X\s+(\w+)", curl_command)
            method = method_match.group(1) if method_match else "GET"
            
            url_match = re.search(r"curl --location '(.*?)'", curl_command)
            url = url_match.group(1) if url_match else None

            headers = {}
            for header_match in re.finditer(r"--header '(.*?): (.*?)'", curl_command):
                headers[header_match.group(1)] = header_match.group(2)

            payload_match = re.search(r"--data '(.*?)'", curl_command, re.DOTALL)
            payload = payload_match.group(1) if payload_match else None

            script += "    Create Session    API    ${EMPTY}\n"
            if headers:
                script += f"    &{{headers_dict}}=    Create Dictionary"
                for key, value in headers.items():
                    script += f"    {key}={value}"
                script += "\n"
            
            request_args = f"    url={url}"
            if headers:
                request_args += "    headers=${headers_dict}"
            if payload:
                request_args += f"    data={payload}"
            
            script += f"    ${{response}}=    {method.title()} On Session    API    {request_args}\n"
            script += "    Log    ${response.text}\n"

        elif action_type == "scroll":
            script += "    Execute JavaScript    window.scrollTo(0, document.body.scrollHeight)\n"

        elif action_type == "scroll_up":
            script += "    Execute JavaScript    window.scrollTo(0, 0)\n"

        elif action_type == "scroll_to":
            script += f"    Scroll Element Into View    xpath={xpath}\n"

        elif action_type == "scroll_by":
            script += f"    Execute JavaScript    window.scrollBy({xpath}, {coords})\n"

        elif action_type == "hover":
            script += f"    Mouse Over    xpath={xpath}\n"

        elif action_type == "right_click":
            script += f"    Open Context Menu    xpath={xpath}\n"

        elif action_type == "double_click":
            script += f"    Double Click Element    xpath={xpath}\n"

        elif action_type == "drag_and_drop":
            script += f"    Drag And Drop    xpath={xpath}    xpath={coords}\n"

        elif action_type == "drag_and_drop_by":
            script += f"    Drag And Drop By Offset    xpath={xpath}    {coords}    {viewport}\n"

        elif action_type == "accept_alert":
            script += "    Handle Alert    accept\n"

        elif action_type == "dismiss_alert":
            script += "    Handle Alert    dismiss\n"

        elif action_type == "send_keys_alert":
            script += f"    Input Text Into Alert    {xpath}\n"

        elif action_type == "get_alert_text":
            script += "    ${alert_text}=    Handle Alert    NONE\n"

        elif action_type == "get_attribute":
            script += f"    ${{attribute}}=    Get Element Attribute    xpath={xpath}    {coords}\n"

        elif action_type == "get_text":
            script += f"    ${{text}}=    Get Text    xpath={xpath}\n"

        elif action_type == "get_title":
            script += "    ${title}=    Get Title\n"

        elif action_type == "get_location":
            script += "    ${url}=    Get Location\n"

        return script