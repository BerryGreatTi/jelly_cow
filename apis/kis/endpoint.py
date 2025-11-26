from dataclasses import dataclass

@dataclass
class Endpoint:
    method: str
    url: str
    domain: str
    tr_id: str