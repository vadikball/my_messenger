from pydantic import BaseModel, ConfigDict


class BaseFromAttrs(BaseModel):
    model_config = ConfigDict(from_attributes=True)
