from pydantic import BaseModel, ConfigDict, Field


class Parent(BaseModel):
    model_config = ConfigDict(extra="allow")
    name: str


Parent(name="s", a=5)


class Parent(BaseModel):
    model_config = ConfigDict(extra="allow")
    name: str
    sup: int = Field(None)


Parent(name="s")


class C(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=False)
    name: str


c = C(name="s")

MyConfigDict = ConfigDict(extra="forbid", validate_assignment=True, strict=True)


class CS(BaseModel):
    model_config = MyConfigDict
    name: str


c = C(name="s")
c.name = {"3", 1}
print(type(c.name))
