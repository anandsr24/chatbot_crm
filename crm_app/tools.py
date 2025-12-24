import json
from mcp_server import salesforce, hubspot

def _parse_input_to_dict(input_text: str) -> dict:
    """
    Helper function:
    - Parses key=value pairs from chat input
    - Makes keys CASE-INSENSITIVE
    """
    parts = {}

    for item in input_text.strip().split():
        if "=" not in item:
            continue

        key, value = item.split("=", 1)
        parts[key.strip().lower()] = value.strip().strip('"')

    return parts


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
            return (
                "Salesforce connection SUCCESSFUL\n\n"
                "Backend Response:\n"
                f"{json.dumps(result, indent=2)}"
            )

        return (
            "Salesforce connection FAILED\n\n"
            "Backend Response:\n"
            f"{json.dumps(result, indent=2)}"
        )

    except Exception as e:
        return f"Error while processing Salesforce input:\n{e}"


# =========================================================
# HUBSPOT
# =========================================================
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
            return (
                "HubSpot connection SUCCESSFUL\n\n"
                "Backend Response:\n"
                f"{json.dumps(result, indent=2)}"
            )

        return (
            "HubSpot connection FAILED\n\n"
            "Backend Response:\n"
            f"{json.dumps(result, indent=2)}"
        )

    except Exception as e:
        return f"Error while processing HubSpot input:\n{e}"
