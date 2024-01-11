from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Optional, Union

from LOGS.Entity.SerializeableContent import SerializeableClass
from LOGS.Interfaces.IPaginationRequest import IPaginationRequest


class DefaultOrder(Enum):
    id: Any = "id"
    name: Any = "name"


@dataclass
class EntityRequestParameter(SerializeableClass, IPaginationRequest):
    _noSerialize = ["asString"]
    excludeIds: Optional[Union[List[int], List[str]]] = None
    searchTerm: Optional[str] = None
    ids: Optional[Union[List[int], List[str]]] = None
    includeCount: Optional[bool] = None
    includeRelations: Optional[bool] = True
    orderby: Any = None
