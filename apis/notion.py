import os
import notion_client
from datetime import datetime

notion_api_key = os.getenv("NOTION_API_KEY")
database_id = os.getenv("NOTION_DATABASE_ID")

def get_notion_client():
    """Initializes and returns the Notion client using the API key from environment variables."""
    if not notion_api_key:
        raise ValueError("NOTION_API_KEY environment variable not set.")
    
    return notion_client.Client(auth=notion_api_key)

def create_notion_page(title: str, content: str):
    """
    Creates a new page in a Notion database with the given title and content.
    Handles content that exceeds Notion's 100-block limit per request.

    Args:
        title (str): The title of the Notion page.
        content (str): The content of the Notion page in Markdown format.
    """
    notion = get_notion_client()
    if not database_id:
        raise ValueError("NOTION_DATABASE_ID environment variable not set.")

    # Convert Markdown content to Notion blocks
    blocks = []
    for line in content.split('\n'):
        if line.startswith('# '):
            blocks.append({
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": line.replace('# ', '')}}]
                }
            })
        elif line.startswith('## '):
            blocks.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": line.replace('## ', '')}}]
                }
            })
        elif line.startswith('### '):
            blocks.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": line.replace('### ', '')}}]
                }
            })
        elif line.strip(): # Non-empty line
            # Simple check for bullet points
            if line.strip().startswith('- '):
                text_content = line.strip().replace('- ', '', 1)
                blocks.append({
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [{"type": "text", "text": {"content": text_content}}]
                    }
                })
            else:
                blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": line}}]
                    }
                })

    # Dynamically find the title property
    try:
        db_info = notion.databases.retrieve(database_id=database_id)
        title_property_name = None
        for name, prop in db_info['properties'].items():
            if prop['type'] == 'title':
                title_property_name = name
                break
        
        if not title_property_name:
            raise ValueError("Could not find a 'title' property in the database.")

        # Create the page in Notion with the first batch of blocks
        page_children = blocks[:100]
        
        new_page_data = {
            "parent": {"database_id": database_id},
            "properties": {
                title_property_name: {
                    "title": [
                        {
                            "type": "text",
                            "text": {
                                "content": f"{title} ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})"
                            }
                        }
                    ]
                }
            },
            "children": page_children
        }
        
        created_page = notion.pages.create(**new_page_data)
        page_id = created_page['id']
        
        # Append remaining blocks in chunks of 100
        remaining_blocks = blocks[100:]
        for i in range(0, len(remaining_blocks), 100):
            chunk = remaining_blocks[i:i+100]
            notion.blocks.children.append(
                block_id=page_id,
                children=chunk
            )

        print(f"Successfully created Notion page: {created_page.get('url')}")
        return created_page
    except Exception as e:
        print(f"Error creating Notion page: {e}")
        raise

if __name__ == '__main__':
    # Example usage (for testing)
    # Make sure to set NOTION_API_KEY and NOTION_DATABASE_ID in your environment
    from dotenv import load_dotenv
    load_dotenv()

    sample_title = "Sample Analysis Report"
    sample_content = """
# Stock Analysis: AAPL

## Fundamental Analysis
- **P/E Ratio**: 25.0
- **Debt-to-Equity**: 0.8

### Analyst Recommendations
- **Buy**: 15
- **Hold**: 5
- **Sell**: 2

## Technical Analysis
- **RSI**: 55 (Neutral)
- **MACD**: Bullish crossover

## News Sentiment
- Overall sentiment is positive based on recent news.
"""
    
    # To run this test, you need a .env file with your Notion credentials
    # create_notion_page(sample_title, sample_content)
    pass
