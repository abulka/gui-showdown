from dataclasses import dataclass
from typing import List, Any

@dataclass
class NestedDictAccess:
    data: dict
    keys: List

    # dynamically access or set nested dictionary keys in model

    @property
    def val(self) -> str:
        data = self.data
        for k in self.keys:
            data = data[k]
        return data

    @val.setter
    def val(self, v: str) -> None:
        data = self.data
        lastkey = self.keys[-1]
        for k in self.keys[:-1]:  # when assigning drill down to *second* last key
            data = data[k]
        data[lastkey] = v


class DynamicAccessNestedDict:
    """Dynamically get/set nested dictionary keys of 'data' dict"""

    def __init__(self, data: dict):
        self.data = data

    def getval(self, keys: List):
        data = self.data
        for k in keys:
            data = data[k]
        return data

    def setval(self, keys: List, val) -> None:
        data = self.data
        lastkey = keys[-1]
        for k in keys[:-1]:  # when assigning drill down to *second* last key
            data = data[k]
        data[lastkey] = val


if __name__ == "__main__":
    # Quick test of ModelRef

    model = {
        "welcomemsg": "Welcome", 
        "user": {
            "firstname": "Sam", 
            "surname": "Smith"
        }
    }

    m = NestedDictAccess(model, ["user", "firstname"])
    assert m.val == "Sam"
    m.val = "Mary"
    assert m.val == "Mary"

    model = {
        "welcomemsg": "Welcome", 
        "user": {
            "firstname": "Sam", 
            "surname": "Smith"
        }
    }

    m = DynamicAccessNestedDict(model)
    assert m.getval(["user", "firstname"]) == "Sam"
    m.setval(["user", "firstname"], "Mary")
    assert m.getval(["user", "firstname"]) == "Mary"


    # My Stack Overflow answer example - https://stackoverflow.com/questions/39818669/python-dynamically-accessing-nested-dictionary-keys

    dct = {'label': 'A', 'config': {'value': 'val1'}}

    d = DynamicAccessNestedDict(dct)
    assert d.getval(["label"]) == "A"
    assert d.getval(["config", "value"]) == "val1"

    # Set some values
    d.setval(["label"], "B")
    d.setval(["config", "value"], "val2")

    assert d.getval(["label"]) == "B"
    assert d.getval(["config", "value"]) == "val2"

    print("OK")