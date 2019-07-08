from dataclasses import dataclass
from typing import List, Any

@dataclass
class ModelRef:
    model: dict
    keys: List
    finalstr: str = ""

    # dynamically access or set nested dictionary keys in model

    @property
    def val(self) -> str:
        data = self.model
        for k in self.keys:
            data = data[k]
        return data

    @val.setter
    def val(self, v: str) -> None:
        data = self.model
        lastkey = self.keys[-1]
        for k in self.keys[:-1]:  # when assigning drill down to *second* last key
            data = data[k]
        data[lastkey] = v


@dataclass
class DynamicAccessNestedDict:
    """Dynamically access or set nested dictionary keys in model"""
    data: dict

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

    m = ModelRef(model, ["user", "firstname"])
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