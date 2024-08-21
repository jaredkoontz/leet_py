import json
import pprint
from pathlib import Path

"""
This is used to compare your solved problems for a session in leet code, to what is currently in this directory.

To use:
    get json from your web browser by running `extract_problems.json` in the dev console
    run this script, it will tell you what you are missing from this local dir, and what submissions you are missing
"""

PATH_TO_JSON = "my_leet.json"


def _get_leet_code():
    """
    reads the json on disk and returns a dict in the form of:
    '0-padded-num':
                title: ''
                full_url: ''
    """

    def _pre_process(lc_list: list[dict[str]]) -> dict[str, dict[str, str]]:
        processed = {}
        for entry in lc_list:
            if entry["title"]:
                number, title = entry["title"].split(". ", 1)
                key = f"{int(number):04d}"
                processed[key] = {
                    "title": title,
                    "url": f'https://leetcode.com{entry["url"]}',
                }
        return processed

    leet_code = json.load(Path(PATH_TO_JSON).open())
    return _pre_process(leet_code)


def _get_local_dirs() -> dict[str, dict[str, str]]:
    """
    reads the dirs on disk and returns a dict in the form of:
    '0-padded-num':
                title: ''
                full_path: ''
    """
    local_dirs = {}
    source_root = Path("..")
    for directory in source_root.glob(r"[0-9]*"):
        key, name = directory.name.split("_", 1)
        py_paths = [file for file in directory.rglob("test_*.py")]
        py_path = "" if len(py_paths) != 1 else py_paths[0]
        local_dirs[key] = {
            "title": name,
            "path": directory.absolute(),
            "py_path": py_path,
        }
    return local_dirs


def _compare_dicts(
    from_leet: dict[str, dict[str, str]], from_local: dict[str, dict[str, str]]
):
    # known_missing_local = {'0271', '0000'}

    missing_local = (set(from_leet.keys())) - set(from_local.keys())
    missing_leet = set(from_local.keys()) - set(from_leet.keys())

    missing_local_info = "missing_leet\n"
    missing_leet_info = "missing_leet\n"
    for x in missing_leet:
        entry = from_local[x]
        missing_local_info += f"{pprint.pformat(entry)}\n"
    for x in missing_local:
        entry = from_leet[x]
        missing_leet_info += f"{pprint.pformat(entry)}\n"

    print(
        f"missing_local\n{missing_local}\n{missing_leet_info}\n\n{missing_leet}\n{missing_local_info}"
    )


def _update_url(
    from_leet: dict[str, dict[str, str]], from_local: dict[str, dict[str, str]]
):
    for x in from_local:
        local_path = from_local[x]["py_path"]
        if from_leet.get(x):
            url = from_leet[x]["url"]
            file_path = Path(local_path)
            try:
                if file_path:
                    # Read the current content of the file
                    text_to_prepend = f"# {url}"
                    current_content = file_path.read_text()
                    # todo search for first line being the url, if not add the comment

                    # Combine the new text with the existing content
                    new_content = f"{text_to_prepend}\n{current_content}"
                    file_path.write_text(new_content)
            except Exception as e:
                print(f"failed on {x=}\n{e=}\n{url=}\n{file_path=}\n")


def main():
    from_leet = _get_leet_code()
    from_local = _get_local_dirs()
    _compare_dicts(from_leet, from_local)
    # do not uncomment, all files are currently commented.
    # _update_url(from_leet, from_local)


if __name__ == "__main__":
    main()
