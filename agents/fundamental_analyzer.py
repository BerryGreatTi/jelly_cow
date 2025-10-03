from google.adk.agents import Agent


agent = Agent(
    name="FundamentalAnalyzer",
    model="gemini-2.5-flash",
    
    description="Specialist of stock fundamental analysis.",
    
    instruction=(
"You are a specialist in fundamental analysis. "
"Analyze the given company's financial health, valuation, and competitive advantages. "
"The tools for this are not yet implemented."
    ),
    
    tools=[] # Tools to be added later
)