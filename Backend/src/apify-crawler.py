import json
import pandas as pd
from utils import xstr

from apify_client import ApifyClient


def main():
    formatted_csv = {}
    with open("../data/apify_result.json", 'rb') as file:
        dataset = json.load(file)

    new_dataset = {}
    for key, item in dataset.items():
        if "city" not in item:
            continue
        new_dataset[key.encode('ascii', 'ignore').decode('ascii')] = item
        formatted_csv[item['title']] = ("The name is " + xstr(item["title"]) + "which is a "  + xstr(item["categoryName"]) + " in the city of " + xstr(item["city"]))

    apify_df = pd.DataFrame(formatted_csv.items())
    apify_df.columns = ["title", "content"]
    for c in apify_df.columns:
        apify_df[c] = apify_df[c].str.encode('ascii', 'ignore').str.decode('ascii')
    apify_df.index = apify_df["title"]
    apify_df.to_csv("../data/apify_result.csv")
    with open("../data/apify_result.json", 'w') as file:
        json.dump(new_dataset, file)



if __name__ == "__main__":
    main()
