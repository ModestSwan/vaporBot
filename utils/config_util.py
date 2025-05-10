# \vaporBot\utils\config_util.py
import json
import time


def get_art_url(art_id):
    with open('./art_details.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for art in data.get("ARTS", []):
        if art.get("id") == art_id:
            return art.get("url")

    raise ValueError(f"No artwork found for art_id '{art_id}'")


def get_patch_details(patch_number):
    with open('./patch_details.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for patch_details in data.get("PATCH_DETAILS", []):
        if patch_details.get("patch_number") == patch_number:
            return patch_details
    return None


def get_next_patch_number():
    currentTS = int(time.time())
    with open('./patch_details.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for patch_details in data.get("PATCH_DETAILS", []):
        if patch_details.get("timestamp") >= currentTS:
            return patch_details.get("patch_number")
    return None


def get_stream_details():
    try:
        with open('./stream_details.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def get_testing_servers():
    try:
        with open('./config.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("testing_servers", [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []
