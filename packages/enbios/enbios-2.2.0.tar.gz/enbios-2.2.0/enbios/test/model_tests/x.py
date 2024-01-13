from pydantic import BaseModel, Field


class X(BaseModel):
    name: str = Field("", description="Name of the X")


class Y(BaseModel):
    name: str = Field(None, description="Name of the X")


print(Y.model_json_schema())


print(Y())
