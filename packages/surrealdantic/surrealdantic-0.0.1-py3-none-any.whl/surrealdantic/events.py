import asyncio
from typing import Generic, Literal, TypeAlias, TypeVar

from fastapi import APIRouter
from pydantic import BaseModel, Field
from sse_starlette import EventSourceResponse

from .utils import robust

EventType: TypeAlias = Literal["message", "created", "updated", "deleted"]


T = TypeVar("T")


class Event(BaseModel, Generic[T]):
    """
    Represents a Server-Sent Event (SSE) payload.
    It witll handle the events that ocurr in the database and react to them accordingly passing the new state to the client.
    """

    event: EventType = Field(default="message")
    data: T


class EventSource(Generic[T], APIRouter):
    """
    Represents a Server-Sent Event (SSE) endpoint.

    It will have the role of the main controller for the given namespace and key.
    """

    subscribers: dict[str, dict[str, asyncio.Queue[T]]] = {}

    async def sub(self, *, namespace: str, key: str):
        """
        Subscribes to a namespace and key.
        """

        if namespace not in self.subscribers:
            self.subscribers[namespace] = {}
            self.subscribers[namespace][key] = asyncio.Queue()
        elif key not in self.subscribers[namespace]:
            self.subscribers[namespace][key] = asyncio.Queue()
        queue = self.subscribers[namespace][key]
        while True:
            try:
                yield await queue.get()
            except asyncio.CancelledError:
                break

    @robust
    async def pub(self, *, namespace: str, key: str, data: T):
        """
        Publishes to a namespace and key.
        """
        if namespace not in self.subscribers:
            self.subscribers[namespace] = {}
            self.subscribers[namespace][key] = asyncio.Queue()
        elif key not in self.subscribers[namespace]:
            self.subscribers[namespace][key] = asyncio.Queue()
        queue = self.subscribers[namespace][key]
        await queue.put(data)

    async def event_source(
        self, *, namespace: str, key: str, event: EventType = "message"
    ):
        """
        Generates an event source for a namespace and key.
        """

        async def generator():
            async for item in self.sub(namespace=namespace, key=key):
                yield Event(event=event, data=item).model_dump()

        return EventSourceResponse(generator())
