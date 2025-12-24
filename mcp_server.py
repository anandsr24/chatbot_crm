from mcp.server import FastMCP
import requests
from config import *
mcp = FastMCP("crm-tools")


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
