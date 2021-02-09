from typing import List, Optional

from pydantic import BaseModel


class Tree(BaseModel):
    """ for dgraph"""

    uid: Optional[str]
    procedure: Optional[int]
    madeOf: Optional[List['Tree']] = None
