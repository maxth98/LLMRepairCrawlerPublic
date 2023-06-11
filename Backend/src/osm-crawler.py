import json
import osmium
import pandas as pd
import requests


class RepairHandler(osmium.SimpleHandler):
    def __init__(self, tag_key, word_key):
        osmium.SimpleHandler.__init__(self)
        self.repairs = []
        self.tag_key = tag_key
        self.word_key = word_key

    def string_contains_word(self, string, word):
        return word.lower() in string.lower()

    def node(self, n):
        if self.tag_key in n.tags or self.string_contains_word(n.tags.get('name', ''), self.word_key):
            repair = {
                'id': n.id,
                'type': 'node',
                'name': n.tags.get('name', ''),
                'latitude': n.location.lat,
                'longitude': n.location.lon
            }
            self.repairs.append(repair)

    def way(self, w):
        if self.tag_key in w.tags or self.string_contains_word(w.tags.get('name', ''), self.word_key):
            repair = {
                'id': w.id,
                'type': 'way',
                'name': w.tags.get('name', ''),
                'center': {
                    'latitude': w.center().lat,
                    'longitude': w.center().lon
                }
            }
            self.repairs.append(repair)

    def relation(self, r):
        if self.tag_key in r.tags or self.string_contains_word(r.tags.get('name', ''), self.word_key):
            repair = {
                'id': r.id,
                'type': 'relation',
                'name': r.tags.get('name', '')
            }
            self.repairs.append(repair)


def query_repairs(osm_file):
    handler = RepairHandler(tag_key="repair", word_key="reparatur")
    handler.apply_file(osm_file)

    return handler.repairs


def main():
    with open('../data/styria.json', 'r') as file:
        styria_json = json.load(file)

    with open('../data/tokens.json', 'r') as file:
        tokens = json.load(file)

    features = styria_json['features']
    node_dict = {}
    for node in features:
        props = node['properties']

        if "name" in props:
            new_node = {}
            new_node['location'] = node['geometry']['coordinates']
            geo_url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{new_node['location'][0]},{new_node['location'][1]}.json?access_token={tokens['mapbox']}"

            try:
                mb_result = requests.get(geo_url)
                place_name = json.loads(mb_result.text)['features'][0]['place_name']
            except:
                place_name = ""
            props['address'] = place_name
            del props['@id']
            new_node['props'] = props
            new_node['content'] = json.dumps(props)
            new_node['name'] = props['name']
            node_dict[props['name']] = new_node

    with open('../data/styria_proc.json', 'w') as file:
        json.dump(node_dict, file)

    trans_df = pd.DataFrame(node_dict).T[["content", "name"]]
    trans_df.to_csv("../data/styria_proc.csv")


if __name__ == "__main__":
    main()
