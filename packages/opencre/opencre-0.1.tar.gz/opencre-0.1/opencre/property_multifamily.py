from dataclasses import dataclass
from typing import Optional
from .property_generic import PropertyGeneric

@dataclass
class PropertyMultifamily(PropertyGeneric):
    units: Optional[int] = None