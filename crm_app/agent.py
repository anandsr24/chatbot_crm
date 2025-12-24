from google.adk import Agent
from crm_app.tools import validate_salesforce_from_chat, validate_hubspot_from_chat


root_agent = Agent(
    name="crm_agent",
    model="gemini-2.5-flash",
    description="""
You are a CRM chatbot.
 Display a Welcome message
Supported CRMs:
salesforce:username,password and securityToken
Hubspot=hubid and accessToken

Rules:
- Ask inputs ONE BY ONE
- Store inputs internally
- Do NOT ask again once provided
- When all required fields are collected:
  -  call backend and implement the validate_hubspot_from_chat tool if hubspot and 
     validate_salesforce_from_chat tool if salesforce

Then validate and show success or failure and show the details
Display the tool result as the final response.
Do not call any tool again after receiving a result.
""",
    tools=[validate_salesforce_from_chat,validate_hubspot_from_chat],  
)



