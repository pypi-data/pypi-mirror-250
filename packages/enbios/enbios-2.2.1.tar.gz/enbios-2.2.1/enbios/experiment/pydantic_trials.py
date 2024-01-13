# from enbios.models.experiment_models import ExperimentHierarchyNodeData, ExperimentData
#
# full_data = {'hierarchy': {'name': 'root',
#                                 'aggregator': 'sum',
#                                 'children': [{'name': 'electricity production, wind, >3MW turbine, onshore',
#                                               'id': {'name': 'electricity production, wind, >3MW turbine, onshore',
#                                                      'code': '0d48975a3766c13e68cedeb6c24f6f74'},
#                                               'adapter': 'bw',
#                                               'output': ['kilowatt_hour', 10]},
#                                              {'name': 'electricity production, wind, 1-3MW turbine, onshore',
#                                               'id': {'name': 'electricity production, wind, 1-3MW turbine, onshore',
#                                                      'code': 'ed3da88fc23311ee183e9ffd376de89b'},
#                                               'adapter': 'bw',
#                                               'output': ['kilowatt_hour', 10]}]},
#                   'adapters': [{'module_path': '/home/ra/projects/enbios/enbios/bw2/brightway_experiment_adapter.py',
#                                 'config': {'bw_project': 'ecoinvent_391'},
#                                 'methods': {'GWP1000': {'id': ('ReCiPe 2016 v1.03, midpoint (H)',
#                                                                'climate change',
#                                                                'global warming potential (GWP1000)')},
#                                             'FETP': {'id': ('ReCiPe 2016 v1.03, midpoint (H)',
#                                                             'ecotoxicity: freshwater',
#                                                             'freshwater ecotoxicity potential (FETP)')}}},
#                                {'module_path': '/home/ra/projects/enbios/enbios/demos/DemoAdapter.py'}]}
#
# a = ExperimentHierarchyNodeData(**full_data["hierarchy"])
#
# print(a.model_dump())
#
# xx = ExperimentData(**full_data)
#
# print(xx.model_dump())
# print(xx.hierarchy.model_dump())
from typing import Any, Optional

from pydantic import BaseModel, field_validator, Field, model_validator, ConfigDict
from pydantic_core.core_schema import ValidationInfo


###

class FF(BaseModel):
    name: str


# class X(BaseModel):
#     activity: str
# #     output_unit: str
# #     default_output: Optional[FF] = Field(..., description="The default output of the activity")
# #
#     @field_validator("default_output")
#     @classmethod
#     def validate_default_output(cls, v: Any, values: ValidationInfo) -> FF:
#         print(v)
#         # if not v:
#         #     return FF(name=values.data["output_unit"])
#         return FF(name="sweet")


# X(**{"activity": "test", "output_unit": "kg"})


class UserModel(BaseModel):
    id: int
    name: str
    defo: str

    @model_validator(mode='before')
    @classmethod
    def check_card_number_omitted(cls, data: Any) -> Any:
        if "defo" not in data:
            data["defo"] = None
        return data

    @field_validator('defo', mode='before')
    @classmethod
    def name_must_contain_space(cls, v: Any, values: ValidationInfo):
        if ' ' not in v:
            raise ValueError('must contain a space')
        return v.title()


    # @field_validator('defo')
    # @classmethod
    # def validate_default_output(cls, v: Any) -> FF:
    #     if not v:
    #         raise ValueError("no v")
    #     return v

# print(UserModel(id=1, name='John Doe'))
StrictInputConfig = ConfigDict(extra='forbid', validate_assignment=True, strict=True)

class B(BaseModel):
    a: int

class A(BaseModel):
    model_config: ConfigDict = StrictInputConfig

    a: int
    x: B
    y: Optional[str] = Field(None, description='dd', title="blaa")

dd = A(a=4,x = B(a=1))
# dd.a = "5"

print(dd.model_dump())
A.model_fields