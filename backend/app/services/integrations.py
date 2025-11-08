"""Placeholder integration layer for Gmail, Notion, and related services."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List


@dataclass
class IntegrationStatus:
    name: str
    ready: bool
    message: str


class GmailCalendarIntegration:
    """Minimal stub that fakes the Google Calendar interface."""

    def __init__(self) -> None:
        self._connected = False

    def connect(self) -> None:
        self._connected = True

    def status(self) -> IntegrationStatus:
        return IntegrationStatus(
            name="gmail_calendar",
            ready=self._connected,
            message="Connected" if self._connected else "Authentication required",
        )

    def next_events(self, horizon: int = 5) -> List[Dict[str, str]]:
        now = datetime.utcnow()
        return [
            {
                "id": f"event-{index}",
                "title": f"Sample event {index + 1}",
                "start": (now + timedelta(hours=index + 1)).isoformat(),
                "location": "Virtual",
            }
            for index in range(horizon)
        ]


class NotionIntegration:
    """Placeholder for Notion dashboards and databases."""

    def __init__(self) -> None:
        self._connected = False

    def connect(self) -> None:
        self._connected = True

    def status(self) -> IntegrationStatus:
        return IntegrationStatus(
            name="notion",
            ready=self._connected,
            message="Connected" if self._connected else "API token missing",
        )

    def available_dashboards(self) -> List[Dict[str, str]]:
        return [
            {"id": "notion-weekly-review", "title": "Weekly Reflection"},
            {"id": "notion-goals", "title": "Personal Growth Goals"},
        ]


class IntegrationManager:
    """Coordinates integration connectivity and reporting."""

    def __init__(self) -> None:
        self.calendar = GmailCalendarIntegration()
        self.notion = NotionIntegration()

    def connect_all(self) -> None:
        self.calendar.connect()
        self.notion.connect()

    def status_report(self) -> Dict[str, Dict[str, str]]:
        statuses = [self.calendar.status(), self.notion.status()]
        return {
            status.name: {"ready": str(status.ready).lower(), "message": status.message}
            for status in statuses
        }


__all__ = ["IntegrationManager", "GmailCalendarIntegration", "NotionIntegration"]
