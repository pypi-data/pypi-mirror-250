# import sys
import json
import unittest

import gitaddnb  # type:ignore
import gitaddnb.add  # type:ignore


class TestStringMethods(unittest.TestCase):
    def test_get_execution_counts(self) -> None:
        with open(file="tests/True123.ipynb") as f:
            self.assertEqual(gitaddnb.add.get_execution_counts(f.read()), [1, 2, 3])

    def test_executioncounts_inorder(self) -> None:
        self.assertTrue(gitaddnb.add.executioncounts_inorder([1, 2, 3]))
        self.assertFalse(gitaddnb.add.executioncounts_inorder([4, 2, 3]))

    def test_get_gitaddnb_status(self) -> None:
        with open(file="tests/True123.ipynb") as f:
            self.assertFalse(gitaddnb.add.get_gitaddnb_status(f.read()))
        self.assertTrue(gitaddnb.add.get_gitaddnb_status('{"metadata":{"gitaddnb":true}}'))

    def test_create_stage_content(self) -> None:
        with open(file="tests/True123.ipynb") as f:
            file_content = f.read()
        stage_content = gitaddnb.add.create_stage_content(file_content=file_content)
        stage_json_content = json.loads(stage_content)
        for cell in stage_json_content["cells"]:
            self.assertListEqual(cell["outputs"], [])
            self.assertIsNone(cell["execution_count"])
        self.assertTrue(stage_json_content["metadata"]["gitaddnb"])


if __name__ == "__main__":
    unittest.main()
