from dataclasses import dataclass

@dataclass(frozen = True)
class Team:
    name: str
    ID: int
    totale: float

    def __hash__(self):
        # Hash basato su identificativo univoco
        return hash(self.ID)

    def __str__(self):
        return f"{self.name} - {self.ID} - {self.totale}"
