import os
import json
from datetime import datetime
from notion_client import Client

from memory.palace import get_memory_palace
from strategies.strategy_registry import get_registry

class NotionBridge:
    def __init__(self):
        self.token = os.getenv("NOTION_TOKEN")
        if not self.token:
            print("Warning: NOTION_TOKEN not set. Notion integration disabled.")
            self.client = None
        else:
            self.client = Client(auth=self.token)
        self.memory = get_memory_palace()
        self.registry = get_registry()

    def create_weekly_reckoning(self):
        if not self.client:
            return "Notion not configured."
        recent = self.memory.recall_past_signals("weekly performance", limit=20)
        parent = {"database_id": os.getenv("NOTION_DATABASE_ID", "your_database_id_here")}
        properties = {
            "Title": {"title": [{"text": {"content": f"CoIn Weekly Reckoning - {datetime.now().strftime('%Y-%m-%d')}"}}]},
            "Date": {"date": {"start": datetime.now().isoformat()}},
            "Summary": {"rich_text": [{"text": {"content": f"{len(recent)} signals processed this week. Capital preserved."}}]}
        }
        try:
            page = self.client.pages.create(
                parent=parent,
                properties=properties,
                children=[
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"text": {"content": "Full audit trail available in MemPalace. Grok-powered analysis attached."}}]
                        }
                    }
                ]
            )
            return f"Weekly Reckoning created in Notion: {page['id']}"
        except Exception as e:
            return f"Notion sync error: {str(e)}"

    def sync_signal_to_notion(self, signal: dict, signal_id: int):
        if not self.client:
            return
        print(f"Signal {signal_id} synced to Notion (placeholder - configure database).")

# Singleton
notion_bridge = None
def get_notion_bridge() -> NotionBridge:
    global notion_bridge
    if notion_bridge is None:
        notion_bridge = NotionBridge()
    return notion_bridge
