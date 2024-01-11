import os as _os
from pydantic import BaseModel, Field
import asyncio
import json
import requests
from langchain.tools import BaseTool


api_key: str | None = _os.environ.get("SPOOKY_API_KEY")

agent_id: str | None = _os.environ.get("SPOOKY_AGENT_ID")

agent_name: str | None = _os.environ.get("SPOOKY_AGENT_NAME")

SPOOKY_URL = "https://cerebrus-prod-eastus.azurewebsites.net/"


def query_human(query: str, metadata: str = "") -> str:
    
    data = {
        "apiKey": api_key,
        "query": query,
        "agentID": agent_id,
        "agentName": agent_name,
        "metadata": metadata,
    }

    # Headers for the request (if needed, like authentication tokens)
    headers = {
        "Content-Type": "application/json",
        # Add other headers here if needed
    }

    print("data: ", data)
    # Making the POST request with an infinite timeout
    # response = requests.post(CEREBRUS_URL + "queryHuman", data=json.dumps(data), headers=headers, timeout=None)
    # response = requests.post("http://localhost:7001/queryHuman", data=json.dumps(data), headers=headers)
    
    # loop = asyncio.get_event_loop()
    # response = await loop.run_in_executor(
    #     executor,
    #     proxy_post,
    #     CEREBRUS_URL + 'queryHuman',
    #     data
    # )

    # print("response: ", response.json())

    # # Checking the response
    # if response.status_code == 200:
    #     return jsonify({ "success": True, 'message': 'Callback received', 'data': response.json()})
    # else:
    #     print("Error:", response.status_code, response.text)
    #     return jsonify({ "success": False, 'message': 'Callback received', 'data': response.json()})
    
    #make the request to the n8n server
    url = SPOOKY_URL + "queryHuman"
    print(url)
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=None)
        if response.status_code == 200:
            print("Success:", response.json())
            return response.json()
        else:
            print("Error:", response.json())
            return response.json()
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return e
        

def human_approval(query: str) -> str:
    pass

class _HumanQueryInput(BaseModel):
    query: str = Field()
    metadata: str = Field() #In Markdown: All relevant information about the query, including the context in which it is being asked, and the consequences of the answer. This is what the user will see when they are asked for their consent.

class _HumanQuery(BaseTool):
    name = "QueryHuman"
    description = "useful for when you need to ask your human a question- for permission, to get personal info you can't find elsewhere, and much more. Use sparingly. Arguments: query: the question you want to ask your human. metadata: All relevant information about the query, including the context in which it is being asked, and the consequences of the answer. This is what the user will see when they are asked for their consent. This is optional, but highly recommended. It is in Markdown."
    args_schema: type[BaseModel] = _HumanQueryInput

    def _run(
        self, query: str, metadata: str, run_manager: None
    ) -> str:
        """Use the tool."""
        return query_human(query, metadata)
            

    async def _arun(
        self, query: str, metadata: str, run_manager: None
    ) -> str:
        return self._run(query, metadata, run_manager)
        
        
#Agent Consent Tool: sends a notification to the user asking for consent to use their data
class _HumanApprovalInput(BaseModel):
    query: str = Field()
    
class _HumanApproval(BaseTool):
    name = "HumanApproval"
    description = "useful for when you need to ask your human for confirmation before doing something - for example, using a important tool, or sending a message to someone"
    args_schema: type[BaseModel] = _HumanApprovalInput

    def _run(
        self, query: str, run_manager: None
    ) -> str:
        """Use the tool."""
        return human_approval(query)
            

    async def _arun(
        self, query: str, run_manager: None
    ) -> str:
        return self._run(query, run_manager)



#Agent Stuck in a Loop : sends time sensitive notification to user


#human consent tool: sends a notification to the user asking for consent to use their data    
    
    
HumanQuery = _HumanQuery()
HumanApproval = _HumanApproval()