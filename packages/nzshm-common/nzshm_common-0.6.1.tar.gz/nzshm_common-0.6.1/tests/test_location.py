from nzshm_common import location
from nzshm_common.location.code_location import CodedLocation


def test_location_keys_unique():
    assert len(location.LOCATIONS) == len(set(loc['id'] for loc in location.LOCATIONS))


def test_location_lists():
    assert len(location.LOCATION_LISTS["NZ"]["locations"]) == 36
    assert len(location.LOCATION_LISTS["SRWG214"]["locations"]) == 214
    assert len(location.LOCATION_LISTS["ALL"]["locations"]) == 214 + 36 + 19480
    assert len(location.LOCATION_LISTS["HB"]["locations"]) == 19480


def test_vs30():
    for id in location.LOCATION_LISTS["HB"]["locations"]:
        assert location.LOCATIONS_BY_ID[id].get("vs30")
    assert location.LOCATIONS_BY_ID[f"hb_{2603-2}"]["vs30"] == 150


def test_location_rot():
    rot = location.LOCATIONS_BY_ID['ROT']
    assert rot['name'] == 'Rotorua'


def test_location_pauanui():
    rot = location.LOCATIONS_BY_ID['srg_34']
    assert rot['name'] == 'Pauanui'


def test_hawks_bay():
    hb0 = location.LOCATIONS_BY_ID['hb_0']
    assert hb0['latitude'] == -39.28856686
    assert hb0['longitude'] == 176.1209845
    assert hb0['vs30'] == 1000

    hb19479 = location.LOCATIONS_BY_ID['hb_19479']
    assert hb19479['latitude'] == -38.15959922
    assert hb19479['longitude'] == 178.2035461
    assert hb19479['vs30'] == 1000


def test_rounded_locations():
    def get_lat_lon(id):
        return (location.location_by_id(id)['latitude'], location.location_by_id(id)['longitude'])

    id = 'srg_142'
    assert CodedLocation(*get_lat_lon(id), 0.001).code == "-41.520~173.948"

    id = 'srg_186'
    assert CodedLocation(*get_lat_lon(id), 0.001).code == "-44.379~171.230"
