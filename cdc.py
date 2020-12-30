import requests
import os
import xml.etree.ElementTree as ET

def parseXML(root):
            for child in root:
                if child.tag == "c":
                    key_len = len(child.keys())
                    if key_len == 2:
                        key = child.keys()[0]
                        global year
                        year = child.attrib[key]
                        years[year] = {}
                    else:
                        key = child.keys()[0]
                        value = child.attrib[key]
                        if "years" in value or "year" in value or "not" in value:
                            global count
                            count = 0
                            global age_group
                            age_group = value.replace(" years", "")
                            age_group = age_group.replace(" year", "")
                            age_group = age_group.replace(" ", "_")
                            years[year][age_group] = {'deaths': 0, 'population': 0, 'crude_rate' : 0}
                            global age_keys
                            age_keys = list(years[year][age_group].keys())
                        else:
                            years[year][age_group][age_keys[count]] = value
                            count = count + 1
                            if count >= 3:
                                count = 0
                parseXML(child)

            return years

def createParameterElement(parameter):
            parameter_string = ""
            for key in parameter:
                parameter_string += "<parameter>\n"
                parameter_string += "<name>" + key + "</name>\n"

                if isinstance(parameter[key], list):
                    for value in parameter[key]:
                        parameter_string += "<value>" + value + "</value>\n"
                else:
                    parameter_string += "<value>" + parameter[key] + "</value>\n"

                parameter_string += "</parameter>\n"

            return parameter_string

def getWonderData(ICD10):
        parameters = [
            {
                "B_1": "D76.V1-level1",
                "B_2": "D76.V5",
                "B_3": "*None*",
                "B_4": "*None*",
                "B_5": "*None*"
            },
            {
                "M_1": "D76.M1",
                "M_2": "D76.M2",
                "M_3": "D76.M3",
                "M_41": "D76.M41",
                "M_42": "D76.M42"
            },
            {
                "F_D76.V1": ["*All*"],
                "F_D76.V10": ["*All*"],
                "F_D76.V2": ["J09-J18"],
                "F_D76.V27": ["*All*"],
                "F_D76.V9": ["*All*"]
            },
            {
                "I_D76.V1": "*All* (All Dates)",
                "I_D76.V10": "*All* (The United States)",
                "I_D76.V2": ICD10, # ICD-10 Codes J09-J18 (Influenza and pneumonia)
                "I_D76.V27": "*All* (The United States)",
                "I_D76.V9": "*All* (The United States)"
            },
            {
                "V_D76.V1": "",
                "V_D76.V10": "",
                "V_D76.V11": "*All*",
                "V_D76.V12": "*All*",
                "V_D76.V17": "*All*",
                "V_D76.V19": "*All*",
                "V_D76.V2": "",
                "V_D76.V20": "*All*",
                "V_D76.V21": "*All*",
                "V_D76.V22": "*All*",
                "V_D76.V23": "*All*",
                "V_D76.V24": "*All*",
                "V_D76.V25": "*All*",
                "V_D76.V27": "",
                "V_D76.V4": "*All*",
                "V_D76.V5": "*All*",
                "V_D76.V51": "*All*",
                "V_D76.V52": "*All*",
                "V_D76.V6": "00",
                "V_D76.V7": "*All*",
                "V_D76.V8": "*All*",
                "V_D76.V9": ""
            },
            {
                "O_V10_fmode": "freg",
                "O_V1_fmode": "freg",
                "O_V27_fmode": "freg",
                "O_V2_fmode": "freg",
                "O_V9_fmode": "freg",
                "O_aar": "aar_none",
                "O_aar_pop": "0000",
                "O_age": "D76.V5",
                "O_javascript": "on",
                "O_location": "D76.V9",
                "O_precision": "1",
                "O_rate_per": "100000",
                "O_show_totals": "true",
                "O_timeout": "600",
                "O_title": "",
                "O_ucd": "D76.V2",
                "O_urban": "D76.V19"
            },
            {
                "VM_D76.M6_D76.V10": "",
                "VM_D76.M6_D76.V17": "*All*",
                "VM_D76.M6_D76.V1_S": "*All*",
                "VM_D76.M6_D76.V7": "*All*",
                "VM_D76.M6_D76.V8": "*All*"
            },
            {
                "action-Send": "Send",
                "finder-stage-D76.V1": "codeset",
                "finder-stage-D76.V2": "codeset",
                "finder-stage-D76.V27": "codeset",
                "finder-stage-D76.V9": "codeset",
                "stage": "request"
            }
        ]

        xml_request = "<request-parameters>\n"
        for parameter in parameters:
            xml_request += createParameterElement(parameter)
        xml_request += "</request-parameters>"

        url = "https://wonder.cdc.gov/controller/datarequest/D76"
        response = requests.post(url, data={"request_xml": xml_request, "accept_datause_restrictions": "true"})

        if response.status_code == 200:
            data = response.text
            path = "data.xml"
            with open(path, "w") as f:
                f.write(data)

        tree = ET.parse("data.xml")
        root = tree.getroot()

        global years
        years = {}
        years = parseXML(root)
        return years


result = getWonderData("X60-X84 (Intentional self-harm)")
print(result)
