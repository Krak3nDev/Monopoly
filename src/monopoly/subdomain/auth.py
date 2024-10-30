from dataclasses import dataclass
from typing import NewType

UserId = NewType("UserId", int)


@dataclass
class Username(kw_only=True, slots=True, frozen=True):
    value: str


### Create auth subdomain


### Add to user check if username is unique before creating, move it to subdomain
@dataclass
class User(kw_only=True, slots=True):
    identity: UserId
    username: Username
    email: str
