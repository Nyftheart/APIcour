from pydantic import BaseModel

class LivreCreate(BaseModel):
    nom: str
    type: str
    langue: str
    description: str
    note: float
    prix: str
    features: list

class Livre(LivreCreate):
    id: int

class LivreUpdate(BaseModel):
    note: float
    prix: str
