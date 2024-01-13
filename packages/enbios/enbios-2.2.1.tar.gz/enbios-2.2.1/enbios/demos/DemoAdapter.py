from typing import Any, Optional

from enbios.base.adapters_aggregators.adapter import EnbiosAdapter
from enbios.base.scenario import Scenario
from enbios.generic.unit_util import get_output_in_unit
from enbios.models.experiment_models import (
    ActivityOutput,
    ResultValue,
)


class DemoAdapter(EnbiosAdapter):
    def __init__(self):
        super().__init__()
        self._config = None
        self.activities: list[str] = []
        self.activityMap: dict[str, float] = {}

    def validate_config(self, config: dict[str, Any]):
        pass

    def validate_methods(self, methods: Optional[dict[str, Any]]) -> list[str]:
        return ["unspecified impact method"]

    def validate_activity_output(
        self, node_name: str, target_output: ActivityOutput
    ) -> float:
        return get_output_in_unit(target_output, self.get_activity_output_unit(node_name))

    def validate_activity(
        self,
        node_name: str,
        activity_config: Any,
        output: ActivityOutput,
        required_output: bool = False,
    ):
        self.activities.append(node_name)

        if output:
            self.activityMap[node_name] = self.validate_activity_output(node_name, output)

    def get_activity_output_unit(self, activity_name: str) -> str:
        return "kilowatt_hour"

    def get_method_unit(self, method_name: str) -> str:
        return "unspecified impact unit"

    def get_default_output_value(self, activity_name: str) -> float:
        return self.activityMap[activity_name]

    def run(self):
        pass

    def run_scenario(self, scenario: Scenario) -> dict[str, dict[str, ResultValue]]:
        return {
            activity: {
                "some impact": ResultValue(unit=self.get_method_unit(""), magnitude=10)
            }
            for activity in self.activities
        }

    @property
    def node_indicator(self) -> str:
        """
        this is the string to which activities should refer in the hierarchy, when they should be assigned to this adapter
        :return:
        """
        return "demo-adapter"

    @property
    def name(self) -> str:
        """
        The name of the adapter
        :return:
        """
        return "Demo Adapter"
