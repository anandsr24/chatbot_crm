import json
from mcp_server import *

def _parse_input_to_dict(input_text):
    if not input_text:
        return {}

    parts = {}
    for item in input_text.strip().split():
        if "=" not in item:
            continue
        key, value = item.split("=", 1)
        parts[key.strip().lower()] = value.strip().strip('"')

    return parts


# ---------------- HUBSPOT ----------------
def hubspot_tables(input_text: str):
    parts = _parse_input_to_dict(input_text)
    try:
        if not all(k in parts for k in ("hubid", "accesstoken")):
            return {
                "status": "error",
                "message": "Expected: hubId=<value> accessToken=<value>"
            }

        payload = {
            "hubId": parts["hubid"],
            "accessToken": parts["accesstoken"],
            "connectorId": 45,
            "connectorName": "hubspot",
            "pyMethod": "tablesMethodName"
        }

        # ---- Call backend ----
        result = crm_connector(payload)

            # ---- Handle response ----
        if result.get("status") in (True, "success"):
            return result

        return f"{result.get('message')}"

    except Exception as e:
        return f"Error while processing Salesforce input:\n{e}"


def hubspot_columns(input_text: str):
    parts = _parse_input_to_dict(input_text)
    try:
        if not all(k in parts for k in ("hubid", "accesstoken", "table")):
            return {
                "status": "error",
                "message": "Expected: hubId=<value> accessToken=<value> table=<contacts|companies|deals|tickets>"
            }

        payload = {
            "hubId": parts["hubid"],
            "accessToken": parts["accesstoken"],
            "connectorId": 45,
            "connectorName": "hubspot",
            "table": parts["table"],
            "pyMethod": "columnsMethodName"
        }

        result=crm_connector(payload)
        if result.get("status") in (True, "success"):
            return result

        return f"{result.get('message')}"

    except Exception as e:
        return f"Error while processing Salesforce input:\n{e}"


# ---------------- SALESFORCE ----------------

def salesforce_tables(input_text: str) -> str:
    """
    Expected chat input (case-insensitive):
    username=<value> password=<value> securityToken=<value>
    """

    try:
        parts = _parse_input_to_dict(input_text)

        # ---- Validate required fields ----
        if not all(k in parts for k in ("username", "password", "securitytoken")):
            return (
                "Invalid input format.\n"
                "Expected:\n"
                "username=<value> password=<value> securityToken=<value>"
            )

        # ---- Build payload ----
        connector_payload = {
        "username": parts["username"],
        "password": parts["password"],
        "securityToken": parts["securitytoken"],  
        "connectorId": 5,
        "connectorName": "salesforce",
        "pyMethod": "tablesMethodName"
        }

        # ---- Call backend ----
        result = crm_connector(connector_payload)

        # ---- Handle response ----
        if result.get("status") in (True, "success"):
            return result


        return f"{result.get('message')}"

    except Exception as e:
        return f"Error while processing Salesforce input:\n{e}"





def salesforce_columns(input_text: str) -> str:
    """
    Expected chat input (case-insensitive):
    username=<value> password=<value> securityToken=<value>
    """

    try:
        parts = _parse_input_to_dict(input_text)

        # ---- Validate required fields ----
        if not all(k in parts for k in ("username", "password", "securitytoken")):
            return (
                "Invalid input format.\n"
                "Expected:\n"
                "username=<value> password=<value> securityToken=<value>"
            )

        # ---- Build payload ----
        connector_payload = {
        "username": parts["username"],
        "password": parts["password"],
        "securityToken": parts["securitytoken"],  
        "connectorId": 5,
        "connectorName": "salesforce",
        "pyMethod": "columnsMethodName"
    }

        # ---- Call backend ----
        result = crm_connector(connector_payload)

        # ---- Handle response ----
        if result.get("status") in (True, "success"):
            return result

        return f"{result.get('message')}"

    except Exception as e:
        return f"Error while processing Salesforce input:\n{e}"




'''
def salesforce_tables(input_text: str):
    parts = _parse_input_to_dict(input_text)

    if not all(k in parts for k in ("username", "password", "securitytoken")):
        return {
            "status": "error",
            "message": "Expected: username=<value> password=<value> securityToken=<value>"
        }

    payload = {
        "username": parts["username"],
        "password": parts["password"],
        "securityToken": parts["securitytoken"],  # lowercase key
        "connectorId": 5,
        "connectorName": "salesforce",
        "pyMethod": "tablesMethodName"
    }

    return crm_connector(payload)

def _base_payload(parts: dict) -> dict:
    return {
        "username": parts.get("username"),
        "password": parts.get("password"),
        "securityToken": parts.get("securitytoken"),
        "connectorName": "salesforce",    
        "friendlyName": "chat_session",
        "friendlyName": parts.get("friendlyname", "chat_session")
    }

def salesforce_connect(input_text):
    parts = _parse_input_to_dict(input_text)

    if not all(k in parts for k in ("username", "password", "securitytoken")):
        return {
            "status": "error",
            "message": "Missing required fields: username, password, securityToken"
        }

    payload = {
        "username": parts["username"],
        "password": parts["password"],
        "securityToken": parts["securitytoken"],
        "connectorId": 5,
        "connectorName": "salesforce",
        "friendlyName": "chat_session",
        "pyMethod": "connectionMethodName"
    }

    result = crm_connector(payload)

    if result.get("status") == "error":
        return {
            "status": "error",
            "stage": "salesforce_connect",
            "backend_error": result
        }

    return result

def salesforce_list_tables(input_text: str):
    parts = _parse_input_to_dict(input_text)

    payload = _base_payload(parts)
    payload["pyMethod"] = "tablesMethodName"

    return crm_connector(payload)

def salesforce_list_columns(input_text: str):
    parts = _parse_input_to_dict(input_text)

    if "table" not in parts:
        return "Please specify table=<TableName>"

    payload = _base_payload(parts)
    payload["table"] = parts["table"]
    payload["pyMethod"] = "columnsMethodName"

    return crm_connector(payload)
def hubspot_connect(input_text: str):
    parts = _parse_input_to_dict(input_text)

    payload = {
        "hubId": parts.get("hubid"),
        "accessToken": parts.get("accesstoken"),
        "connectorId": int(parts.get("connectorid", 45)),
        "connectorName": "hubspot",
        "friendlyName": "hub_chat",
        "pyMethod": "connectionMethodName"
    }
    result = crm_connector(payload)
    if result.get("status") == "error":
        return {
            "status": "error",
            "stage": "salesforce_connect",
            "backend_error": result
        }

    return result

def hubspot_list_tables(input_text: str):
    parts = _parse_input_to_dict(input_text)

    payload = {
        "hubId": parts.get("hubid"),
        "accessToken": parts.get("accesstoken"),
        "connectorId": 45,
        "connectorName": "hubspot",
        "pyMethod": "tablesMethodName"
    }

    return crm_connector(payload)
def hubspot_list_columns(input_text: str):
    parts = _parse_input_to_dict(input_text)

    if "table" not in parts:
        return "Please provide table=<table_name>"

    payload = {
        "hubId": parts.get("hubid"),
        "accessToken": parts.get("accesstoken"),
        "connectorId": 45,
        "connectorName": "hubspot",
        "table": parts["table"],
        "pyMethod": "columnsMethodName"
    }

    return crm_connector(payload)

# =========================================================
# SALESFORCE
# =========================================================
def validate_salesforce_from_chat(input_text: str) -> str:
    """
    Expected chat input (case-insensitive):
    username=<value> password=<value> securityToken=<value>
    """

    try:
        parts = _parse_input_to_dict(input_text)

        # ---- Validate required fields ----
        if not all(k in parts for k in ("username", "password", "securitytoken")):
            return (
                "Invalid input format.\n"
                "Expected:\n"
                "username=<value> password=<value> securityToken=<value>"
            )

        # ---- Build payload ----
        connector_payload = {
            "username": parts["username"],
            "password": parts["password"],
            "securityToken": parts["securitytoken"],
            "connectorName": "Salesforce",
            "friendlyName": "test",
            "connectorId": 5
        }

        # ---- Call backend ----
        result = salesforce(connector_payload)

        # ---- Handle response ----
        if result.get("status") is True or result.get("code") == 200:
           return f"{result.get('message')}"

        return f"{result.get('message')}"

    except Exception as e:
        return f"Error while processing Salesforce input:\n{e}"

def validate_hubspot_from_chat(input_text: str) -> str:
    """
    Expected chat input (case-insensitive):
    hubId=<value> accessToken=<value>
    """

    try:
        parts = _parse_input_to_dict(input_text)

        # ---- Validate required fields ----
        if not all(k in parts for k in ("hubid", "accesstoken")):
            return (
                "Invalid input format.\n"
                "Expected:\n"
                "hubId=<value> accessToken=<value>"
            )

        # ---- Build payload ----
        connector_payload = {
            "hubId": parts["hubid"],
            "accessToken": parts["accesstoken"],
            "connectorName": "HubSpot",
            "friendlyName": "test",
            "connectorId": 45
        }

        # ---- Call backend ----
        result = hubspot(connector_payload)

        # ---- Handle response ----
        if result.get("status") is True or result.get("code") == 200:
            return f"{result.get('message')}"

        return f"{result.get('message')}"

    except Exception as e:
        return f"Error while processing HubSpot input:\n{e}"
'''