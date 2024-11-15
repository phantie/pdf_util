from typing import TypeVar
from pydantic import NonNegativeInt


PageIndex = TypeVar("PageIndex", bound=NonNegativeInt)
