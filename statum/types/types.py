from pydantic import BaseModel, Field

class Metadata(BaseModel):
    token_count: int = Field(default=0, alias="token_count")
    action_count: int = Field(default=0, alias="action_count")
    latest_action: str = Field(default=None, alias="latest_action")
