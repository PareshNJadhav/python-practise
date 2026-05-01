import json
from urllib.request import urlopen
import requests


def learn_json_with_string():
    data = """
    {
        "people": [
                {
                    "name": "John Smith",
                    "phone": "615-555-7164",
                    "emails": ["johnsmith@bogusemail.com", "john.smith@work-place.com"],
                    "has_license": false
                },
                {
                    "name": "Jane Doe",
                    "phone": "560-555-5153" ,
                    "emails": null,
                    "has_license": true
                }
        ]
    }
    """

    """converts the json string to python object"""
    people = json.loads(data)
    print(type(people))
    print(type(people["people"]))

    for person in people["people"]:
        print(person)
        del person["phone"]

    """converts the python object to json"""

    data = json.dumps(people, indent=2, sort_keys=True)

    print(type(data))
    print(data)

def learn_json_with_file():
    with open("./input/states.json") as file:
        """load the json file and convert it to python object"""
        states = json.load(file)

    print(type(states))
    for state in states["states"]:
        #print(state["name"], state["abbreviation"])
        del state["area_codes"]

    with open("./output/states.json", "w") as file:
        json.dump(states, file, indent=2)

def learn_json_with_api():
    url = "https://api.exchangerate-api.com/v4/latest/USD"

    response = requests.get(url)

    print(type(response))
    print(response.text)

    """load the responce text into the python object"""
    data = json.loads(response.text)
    print(json.dumps(data, indent=2))
    #
    usd_rates = dict()
    """another way to get final data"""
    usd_rates1 = data["rates"].copy()

    """iterating and creating new dict"""
    for item in data['rates']:
        usd_rates[item] = data['rates'][item]
    #
    print(usd_rates)
    """directly loading the dict from the json file"""
    # json.dump(data['rates'], open("./output/rates.json", "w"), indent=2)
    json.dump(usd_rates1, open("./output/rates.json", "w"), indent=2)

if __name__ == "__main__":
    #learn_json_with_string()
    #learn_json_with_file()
    learn_json_with_api()

