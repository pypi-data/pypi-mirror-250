import unittest
import json
from json import JSONDecodeError


class TestContractCompliance(unittest.TestCase):

    def setUp(self) -> None:
        self.python_contract = 'm3_python_sdk_contract.json'
        self.java_contract = 'm3_java_sdk_contract.json'

    def compare_dicts(self, d1, d2, path=""):

        problems = []
        if type(d1) is dict and type(d2) is dict:
            for k in d1:
                if k not in d2:
                    problems.append(f"Key {k} does not exist in second JSON")
                else:
                    self.compare_dicts(d1[k], d2[k], path=f"{path}.{k}")
        elif type(d1) is list and type(d2) is list:
            min_len = min(len(d1), len(d2))
            for i in range(min_len):
                self.compare_dicts(d1[i], d2[i], path=f"{path}[{i}]")
            if len(d1) != len(d2):
                problems.append(
                    f"{path}: List length mismatch. {len(d1)} != {len(d2)}")
        else:
            if d1 != d2:
                problems.append(f"{path}: Value mismatch. {d1} != {d2}")

        if problems:
            return {
                "result": "There is differences between two json files",
                "differences": problems
            }

        return True

    def compare_json(self, python_contract, java_contract):
        try:
            with open(python_contract, 'r') as f:
                python_data = json.load(f)
        except FileNotFoundError as e:
            raise Exception({"error": e})
        except JSONDecodeError as e:
            raise Exception({"error": f"{e}, seems like json is empty"})

        try:
            with open(java_contract, 'r') as f:
                java_data = json.load(f)
        except FileNotFoundError as e:
            raise Exception({"error": e})
        except JSONDecodeError as e:
            raise Exception({"error": f"{e}, seems like json is empty"})

        python_data = json.loads(json.dumps(python_data, sort_keys=True))
        java_data = json.loads(json.dumps(java_data, sort_keys=True))

        return self.compare_dicts(python_data, java_data)

    def test_contracts(self):

        result = self.compare_json(
            python_contract=self.python_contract,
            java_contract=self.java_contract
        )

        self.assertEqual(
            result,
            True,
            f"Test failed with result: {result}"
        )

