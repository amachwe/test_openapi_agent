import json
import os
from pathlib import Path

# Load OpenAPI specification from JSON file
def load_openapi_spec():
    spec_file = Path(__file__).parent / "account_api_spec.json"
    with open(spec_file, 'r', encoding='utf-8') as f:
        return json.load(f)

open_api_spec = load_openapi_spec()

from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset

toolset = OpenAPIToolset(spec_dict=open_api_spec)

async def async_main():
  tools = [tool for tool in await(toolset.get_tools())]

  for tool in tools:
    with open(tool.name + ".json", "w", encoding="utf-8") as f:
      f.write(tool.operation.json())

    print(f"Generated tools: {tool.name} - {tool.description} - \n Parameters {[p.name for p in tool.operation.parameters]} \n {tool.operation.json()}\n")



from google.adk.agents import LlmAgent

root_agent = LlmAgent(
    name="api_interacting_agent",
    model="gemini-2.5-flash", # Or your preferred model
    tools=[toolset], # Pass the toolset
    # ... other agent config ...
)

# Uncomment to extract generated tools.
# if __name__ == "__main__":
#   import asyncio
#   asyncio.run(async_main())