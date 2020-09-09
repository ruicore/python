from __future__ import annotations

from enum import Enum
from pydantic import BaseModel
from typing import Optional, NewType, List, Text
UID = NewType("UID", str)
ID = NewType("ID", int)


class MaterialType(str, Enum):
    RAW = "RAW"


class Tree(BaseModel):

    uid: Optional[UID]
    procedure: Optional[ID]
    madeOf: Optional[List[Tree]] = None
    type: Optional[MaterialType]
    name: Optional[Text]


Tree.update_forward_refs()
