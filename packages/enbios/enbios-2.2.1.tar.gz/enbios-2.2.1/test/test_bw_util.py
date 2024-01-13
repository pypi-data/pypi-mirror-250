import bw2data
import pytest
from bw2data.errors import UnknownObject

from enbios.bw2.util import full_duplicate, clean_delete
from test.enbios.test_project_fixture import TEST_BW_PROJECT

@pytest.fixture
def test_db():
    return "ecoinvent_391_cutoff"

@pytest.fixture
def clean_test_copy(test_db: str):
    yield None
    bw2data.projects.set_current(TEST_BW_PROJECT)
    db = bw2data.Database(test_db)
    try:
        test_copy_act = db.get_node("test-copy")
        clean_delete(test_copy_act)
    except UnknownObject:
        pass


def test_copy(clean_test_copy, test_db: str):
    bw2data.projects.set_current(TEST_BW_PROJECT)
    db = bw2data.Database(test_db)
    try:
        test_copy_act = db.get_node("test-copy")
        clean_delete(test_copy_act)
    except UnknownObject:
        pass

    activity_ = {
        "name": "heat and power co-generation, wood chips, 6667 kW, state-of-the-art 2014",
        "unit": "kilowatt hour",
        "code": '8b6b33ff681a7b18918e2c9dff030000',
        "location": "DK"}
    search_results = db.search(activity_["name"], filter={"location": activity_["location"]})
    search_results = list(
        filter(lambda a: a["unit"] == activity_["unit"], search_results)
    )

    exact_activity = None
    if len(search_results) == 1:
        exact_activity = search_results[0]
    else:
        for act in search_results:
            print(act)
            if act["code"] != activity_["code"]:
                act.delete()
            else:
                exact_activity = act

    if exact_activity:
        full_duplicate(exact_activity, "test-copy")
