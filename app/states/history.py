import reflex as rx
import json
import time
from typing import Optional
import logging


class HistoryItem(rx.Base):
    """Model for a single history item."""

    id: str
    type: str
    title: str
    content: str
    timestamp: float
    formatted_date: str = ""
    metadata: dict[str, str] = {}


class HistoryState(rx.State):
    """State for managing local history."""

    history_json: str = rx.LocalStorage("[]", name="prompt_history")

    @rx.var
    def history(self) -> list[HistoryItem]:
        """Parse history from JSON."""
        try:
            data = json.loads(self.history_json)
            items = []
            for item_data in data:
                if "formatted_date" not in item_data and "timestamp" in item_data:
                    item_data["formatted_date"] = time.strftime(
                        "%Y-%m-%d %H:%M", time.localtime(item_data["timestamp"])
                    )
                items.append(HistoryItem(**item_data))
            return items
        except Exception as e:
            logging.exception(f"Error parsing history JSON: {e}")
            return []

    @rx.var
    def recent_history(self) -> list[HistoryItem]:
        """Get most recent items first."""
        return sorted(self.history, key=lambda x: x.timestamp, reverse=True)

    @rx.var
    def has_history(self) -> bool:
        """Check if history is not empty."""
        return len(self.history) > 0

    def _save_history(self, items: list[HistoryItem]):
        """Save list to JSON string."""
        if len(items) > 50:
            items = sorted(items, key=lambda x: x.timestamp, reverse=True)[:50]
        self.history_json = json.dumps(
            [
                {
                    "id": item.id,
                    "type": item.type,
                    "title": item.title,
                    "content": item.content,
                    "timestamp": item.timestamp,
                    "formatted_date": item.formatted_date,
                    "metadata": item.metadata,
                }
                for item in items
            ]
        )

    @rx.event
    def add_item(self, type: str, title: str, content: str, metadata: dict[str, str]):
        """Add a new item to history."""
        import uuid

        ts = time.time()
        formatted = time.strftime("%Y-%m-%d %H:%M", time.localtime(ts))
        new_item = HistoryItem(
            id=str(uuid.uuid4()),
            type=type,
            title=title,
            content=content,
            timestamp=ts,
            formatted_date=formatted,
            metadata=metadata,
        )
        current = self.history
        current.append(new_item)
        self._save_history(current)

    @rx.event
    def delete_item(self, item_id: str):
        """Delete a specific item."""
        current = [item for item in self.history if item.id != item_id]
        self._save_history(current)
        yield rx.toast("Item removed from history", position="bottom-right")

    @rx.event
    def clear_history(self):
        """Clear all history."""
        self.history_json = "[]"
        yield rx.toast("History cleared", position="bottom-right")