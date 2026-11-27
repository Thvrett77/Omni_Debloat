import json
from tuilb import *
import time
import subprocess
def is_xm(filename: str) -> bool:
    return filename.endswith(".xm")


def read_xm(filename: str):
    if not is_xm(filename):
        raise ValueError("Input file must have be .xm")

    with open(filename, "r", encoding="UTF-8") as file:
        # strips + only appends non-empty lines
        lines: list[str] = [line.strip() for line in file if line.strip()]
        return lines


def extract_second_group(lines: list[str]):
    group_contents: list[str] = []
    found: bool = False

    # finds <SecondGroup> in the file
    for line in lines:
        if line == "<SecondGroup>":
            found = True
            continue

        # appends all lines that are below <SecondGroup>
        if found:
            group_contents.append(line)

    return group_contents


def xm_to_json(input_file: str, output_file: str, key="items"):
    """Convert a .xm file to a .json file. Default key: 'items'"""
    lines: list[str] = read_xm(input_file)
    json_data: dict[str, list[str]] = {key: lines}

    # dumps the data into a file
    with open(output_file, "w", encoding="UTF-8") as file:
        json.dump(json_data, file, indent=2, ensure_ascii=False)


def xm_second_group_to_json(input_file: str, output_file: str, key="SecondGroup"):
    """Extract everything after <SecondGroup> into a json file. Default key: 'SecondGroup'"""
    lines: list[str] = read_xm(input_file)
    second_group: list[str] = extract_second_group(lines)
    json_data: dict[str, list[str]] = {key: second_group}

    # dumps the data into a file
    with open(output_file, "w", encoding="UTF-8") as file:
        json.dump(json_data, file, indent=2, ensure_ascii=False)


def extract_groups(lines: list[str]) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = {
        "FirstGroup": [],
        "SecondGroup": [],
    }

    current_group: str | None = None

    for line in lines:
        if line == "<FirstGroup>":
            current_group = "FirstGroup"
            continue

        if line == "<SecondGroup>":
            current_group = "SecondGroup"
            continue

        if current_group:
            groups[current_group].append(line)

    return groups


def xm_groups_to_json(input_file: str, output_file: str) -> None:
    lines: list[str] = read_xm(input_file)
    groups: dict[str, list[str]] = extract_groups(lines)
    
    with open(output_file, "w", encoding="UTF-8") as file:
        json.dump(groups, file, indent=2, ensure_ascii=False)




def CheckSecondGroupHasHttpsValidDownloads(filename):
    invalid_cnt = 0
    with open(filename,'r') as fl:
        data = json.load(fl)
        for p in range(len(data["SecondGroup"])):
            if data["SecondGroup"][p].startswith("https://"):
                pass
            else:
                invalid_cnt +=1


        if len(data["SecondGroup"]) == invalid_cnt:
            prt(text="Every Link is Invalid to download Please Fix it!!!! ✗",color="red",bold=True)
            

            
        if invalid_cnt == 0:
            prt(text="The Links passed as valid links ✔",color="blue",bold="True")
            return 0
#            print(data["SecondGroup"][p])


xm_groups_to_json(input_file="test.xm", output_file="groups.json")
CheckSecondGroupHasHttpsValidDownloads("groups.json")


