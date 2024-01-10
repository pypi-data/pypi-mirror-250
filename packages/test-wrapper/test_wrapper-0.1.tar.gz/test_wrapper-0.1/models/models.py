import datetime
from dataclasses import dataclass
from enum import Enum

from pydantic import BaseModel


@dataclass
class LambdaDescriptor:
    app_name: str
    # Class name implementing
    class_name: str
    # Module name containing lambda implementation
    module: str

class Role(Enum):
    """The role of actor who added a message to a session."""

    USER = 1
    AI = 2

class SessionEvent(BaseModel):
    """A session event is a message from a user or an AI agent that took place in a session context."""

    # TODO maybe add a sequence number here?
    # TODO it is so loserish that this is float.
    timestamp: float
    role: Role
    content: str

    @classmethod
    def create(cls, role: Role, content: str):
        return cls(timestamp=datetime.datetime.now().timestamp(), role=role, content=content)

class Session(BaseModel):
    """A session history is a collection of session events that took place in a session context."""

    # TODO - eventually we will need to add an int sequencer here.
    session_id: str

    # Application which this session is associated with
    app_name: str

    # a list of events that took place in this session
    events: list[SessionEvent]

    # chatMemory: "agent_foo internal state is 7"
    app_metadata: dict[str, str]

    def add_event(self, event: SessionEvent):
        self.events.append(event)
