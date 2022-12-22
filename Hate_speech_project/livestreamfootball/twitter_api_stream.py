#!/usr/bin/env python3

# filtered stream from: https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Filtered-Stream/filtered_stream.py
# documentation here: https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/introduction
import requests
import os
import json
import time

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = "XXXX"  # os.environ.get("BEARER_TOKEN")


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r


def get_rules():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))
    return response.json()


def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print(json.dumps(response.json()))


def set_rules(delete):
    # You can adjust the rules if needed
    sample_rules = [
        {
            "value": "England OR ThreeLions OR France OR LesBleus OR FRAANG OR ENGFRA OR FrenchTeam -is:retweet lang:en",
            "tag": "England France",
        },
        {"value": "FIFAWorldcup OR worldcup -is:retweet lang:en", "tag": "Worldcup"},
        {
            "value": "Mbappe OR Mbappé OR Giroud OR Kounde OR Koundé OR Upamecano OR Tchouameni OR Tchouaméni OR Thuram OR Dembele OR Dembélé OR Kane OR Southgate OR Bellingham OR Walker OR Maddison OR Maguire OR Alexander-Arnold OR Bukayo OR Saka OR Pickford OR Grealish OR Shaw OR Mason OR Mount OR Bowen OR Mendy OR Rashford OR Walker OR Pope OR Raheem OR Sterling OR Trippier OR Dier OR Sancho OR Toney OR Hennessey -is:retweet lang:en",
            "tag": "Players",
        },
    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))


def get_stream(set):
    with open("twitter_stream.txt", "a") as file:
        response = requests.get(
            "https://api.twitter.com/2/tweets/search/stream",
            auth=bearer_oauth,
            stream=True,
            params={
                "tweet.fields": "created_at,organic_metrics,possibly_sensitive,promoted_metrics,public_metrics",
                "user.fields": "protected,verified",
                "expansions": "author_id",
            },
        )
        print(response.status_code)
        if response.status_code != 200:
            raise Exception(
                "Cannot get stream (HTTP {}): {}".format(
                    response.status_code, response.text
                )
            )
        for response_line in response.iter_lines():
            if response_line:
                json_response = json.loads(response_line)
                # json_response["timestamp"] = time.time()
                print(json.dumps(json_response, indent=4, sort_keys=True))
                file.write(json.dumps(json_response) + "\n")


def main():
    rules = get_rules()
    delete = delete_all_rules(rules)
    set = set_rules(delete)
    get_stream(set)


if __name__ == "__main__":
    main()
