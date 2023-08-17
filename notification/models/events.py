import orjson
from pydantic import BaseModel
import json
from json import JSONEncoder


class Event(BaseModel):
    id: str
    title: str
    description: str
    recipient_name: str
    recipient_email: str
    deferred: bool

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson.dumps


class EventEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__
