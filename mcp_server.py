from mcp.server import FastMCP
import requests
from config import *

mcp = FastMCP("crm-tools")
@mcp.tool()
def crm_connector(payload: dict):
    print("Forwarding to pyConnectorApi:", payload)
    try:
        response = requests.post(
            PY_CONNECTOR_API,
            json=payload,
            timeout=15
        )

        if response.status_code != 200:
            return {
                "status": "error",
                "stage": "connector_api_response",
                "http_status": response.status_code,
                "response_text": response.text
            }

        return response.json()

    except Exception as e:
        return {
            "status": "error",
            "stage": "connector_api_call",
            "exception_type": type(e).__name__,
            "exception_message": str(e)
        }
if __name__ == "__main__":
    mcp.run()
'''
def hubspot_list_tables(payload: dict):
    access_token = payload.get("accessToken")

    if not access_token:
        return {
            "status": "error",
            "message": "Missing accessToken"
        }

    try:
        response = requests.get(
            "https://api.hubapi.com/crm/v3/schemas",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            },
            timeout=10
        )

        if response.status_code != 200:
            return {
                "status": "error",
                "http_status": response.status_code,
                "error": response.text
            }

        data = response.json()

        tables = [obj["name"] for obj in data.get("results", [])]

        return {
            "status": "success",
            "tables": tables
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

'''



'''
@mcp.tool()
def crm_connector(payload: dict):
    try:
        response = requests.post(
            PY_CONNECTOR_API,
            json=payload,
            timeout=15
        )

        if response.status_code != 200:
            return {
                "status": "error",
                "stage": "connector_api_response",
                "http_status": response.status_code,
                "response_text": response.text
            }

        return response.json()

    except Exception as e:
        return {
            "status": "error",
            "stage": "connector_api_call",
            "exception_type": type(e).__name__,
            "exception_message": str(e)
        }
@mcp.tool()
def hubspot(payload: dict):
    """
    Calls INTERNAL HubSpot connector API
    """

    required = ["hubId", "accessToken"]
    for k in required:
        if not payload.get(k):
            return {
                "status": "error",
                "message": "Missing credentials"
            }

    try:
        response = requests.post(
            HUBSPOT_URL,
            json=payload,  
            headers={
                "Content-Type": "application/json"
            },
            timeout=10
        )

        if response.status_code != 200:
            return {
                "status": "error",
                "http_status": response.status_code,
                "error": response.text
            }

        return response.json()

    except Exception as e:
        return {
            "status": "error",
            "error": f"Internal API unreachable: {str(e)}"
        }





@mcp.tool()
def salesforce(payload: dict):
    """
    Calls INTERNAL Salesforce connector API
    """

    required = ["username", "password", "securityToken"]
    for k in required:
        if not payload.get(k):
            return {"status": "error", "message": "Missing credentials"}


    try:

        response = requests.post(
            INTERNAL_SF_URL,
            json=payload,
            timeout=10
        )

        return response.json()

    except Exception as e:
        return {
            "status": "error",
            "error": f"Internal API unreachable: {str(e)}"
        }

if __name__ == "__main__":
    mcp.run()
'''