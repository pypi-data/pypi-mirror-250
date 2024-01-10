import json
from pathlib import Path

# Omitting country for now, focus on NZ
# https://service.unece.org/trade/locode/nz.htm

locations_filepath = Path(Path(__file__).parent, 'locations.json')
with open(locations_filepath, 'r') as locations_file:
    LOCATIONS = json.load(locations_file)

nz_ids_filepath = Path(Path(__file__).parent, 'nz_ids.json')
with open(nz_ids_filepath, 'r') as nz_ids_file:
    NZ_IDS = json.load(nz_ids_file)

LOCATIONS_BY_ID = {location["id"]: location for location in LOCATIONS}


LOCATION_LISTS = {
    "HB": {
        "id": "HB",
        "name": "Hawk's Bay high res grid with vs30",
        "locations": [loc["id"] for loc in LOCATIONS if "hb_" in loc["id"]],
    },
    "NZ": {"id": "NZ", "name": "Default NZ locations", "locations": NZ_IDS},
    "NZ2": {
        "id": "NZ2",
        "name": "Main Cities NZ",
        "locations": ["WLG", "CHC", "DUD", "NPL", "AKL", "ROT", "HLZ"],
    },
    "SRWG214": {
        "id": "SRWG214",
        "name": "Seismic Risk Working Group NZ code locations",
        # "locations": list(map(lambda idn: f"srg_{idn}", range(214))),
        "locations": [loc["id"] for loc in LOCATIONS if "srg_" in loc["id"]],
    },
    "ALL": {
        "id": "ALL",
        "name": "Seismic Risk Working Group NZ code locations",
        "locations": list(map(lambda loc: loc["id"], LOCATIONS)),
    },
}


def location_by_id(location_code):
    return LOCATIONS_BY_ID.get(location_code)


if __name__ == "__main__":
    """Print all locations."""
    print("custom_site_id,lon,lat")
    for loc in LOCATIONS:
        print(f"{loc['id']},{loc['longitude']},{loc['latitude']}")
