from pydantic import BaseModel


class DecisionResponse(BaseModel):
    contact_user: bool
    reasoning: str