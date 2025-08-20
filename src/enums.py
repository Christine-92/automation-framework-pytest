from enum import Enum

class MessageType(int, Enum):
    OUTGOING = 1 #"outgoing"
    INCOMING = 0 #"incoming"

class ContentType(str, Enum):
    TEXT = "text"
