"""The main package file"""
import json
import subprocess
import sys


def get_execution_counts(file_content: str) -> list[int]:
    return [
        cell["execution_count"]
        for cell in json.loads(file_content)["cells"]
        if cell["cell_type"] == "code" and cell.get("source", []) != []
    ]


def executioncounts_inorder(execution_counts: list[int]) -> bool:
    return execution_counts == list(range(1, 1 + len(execution_counts)))


def get_gitaddnb_status(file_content: str) -> bool:
    return json.loads(file_content)["metadata"].get("gitaddnb", False) is True


def create_stage_content(file_content: str, sort_keys: bool = True) -> str:
    j2 = json.loads(file_content)
    for cell in j2["cells"]:
        cell["outputs"] = []
        cell["execution_count"] = None
    j2["metadata"]["gitaddnb"] = True

    return json.dumps(obj=j2, sort_keys=sort_keys)


def main(args: list[str] = sys.argv[1:]) -> int:
    """run the cli"""
    file_paths = [arg for arg in args if not arg.startswith("-") and arg.endswith(".ipynb")]
    for file_path in file_paths:
        with open(file_path, encoding="utf-8") as f:
            file_content = f.read()
        execution_counts = get_execution_counts(file_content=file_content)
        can_skip = get_gitaddnb_status(file_content=file_content)
        assert can_skip or executioncounts_inorder(
            execution_counts
        ), f"Not executed consecutively: {execution_counts}. Restart and Run All on {file_path}"
        stage_content = create_stage_content(file_content=file_content)
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        with open(file=file_path, mode="w", encoding="utf-8") as f:
            f.write(stage_content)
        subprocess.run(["git", "add", file_path], check=False)
        with open(file=file_path, mode="w", encoding="utf-8") as f:
            f.write(file_content)
    return 0
