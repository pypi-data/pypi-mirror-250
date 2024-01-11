import json
import logging
from datetime import date

_LOGGER = logging.getLogger(__name__)


def generate_json_nld(json_data, add_date=False):
    """Generating a JSON NLD formatted string from JSON data.

    :param list json_data: A list of dicts.
    :param bool add_date: Whether or not to add a field "upload_date" to each row
        containing today's date (may be useful for partitioning data in BQ).
        Defaults to ``False``.
    :return str: The data in JSON NLD format.
    """
    _LOGGER.info("Generating JSON NLD...")
    json_nld = ""
    if isinstance(json_data, dict):
        json_data = [json_data]
    for item in json_data:
        if add_date:
            item["upload_date"] = date.today().isoformat()
        json_nld += f"{json.dumps(item)}\n"
    _LOGGER.info("Generated.")
    return json_nld


def parse_json_nld(nld_json_data):
    """Parse JSON NLD formatted string into a list of dicts.

    :param str nld_json_data: A string of data in JSON NLD format.
    :return list: A list of dicts.
    """
    _LOGGER.info("Parsing JSON NLD data...")
    json_list = "[" + nld_json_data.replace("\n", ",").rstrip(",") + "]"
    return json.loads(json_list)
