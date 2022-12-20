#!/usr/bin/env python3

import json
import pandas as pd

exports = []

with open("twitter_stream.txt") as f:
    for line in f.readlines():
        data = json.loads(line)
        if "data" not in data:
            continue
        user_id = data["data"]["author_id"]
        user = next(
            (u for u in data.get("includes", {}).get("users", []) if u["id"] == user_id),
            {"name": "", "verified": False},
        )
        rule = next((r for r in data["matching_rules"]), {"tag": ""})
        exports.append(
            [
                data["data"]["id"],
                data["data"]["created_at"],
                data["data"]["text"],
                data["data"]["possibly_sensitive"],
                user["name"],
                user["verified"],
                rule["tag"],
            ]
        )

tweets = pd.DataFrame(
    exports,
    columns=["id", "created", "text", "possibly_sensitive", "user", "verified", "rule"],
)
tweets.to_csv("twitter_stream.csv")
# {
#     "data": {
#         "author_id": "1550169084934950913",
#         "created_at": "2022-12-10T18:29:58.000Z",
#         "edit_history_tweet_ids": ["1601645413505077248"],
#         "id": "1601645413505077248",
#         "possibly_sensitive": false,
#         "public_metrics": {
#             "retweet_count": 0,
#             "reply_count": 0,
#             "like_count": 0,
#             "quote_count": 0,
#         },
#         "text": "@ecssxq \u00d6zlemi\u015fim\ud83e\udd79",
#     },
#     "includes": {
#         "users": [
#             {
#                 "id": "1550169084934950913",
#                 "name": "z' bet\u00fcl \ud83c\udf2a\ufe0f",
#                 "protected": false,
#                 "username": "tacsizperilice",
#                 "verified": false,
#             },
#             {
#                 "id": "1550608603727503365",
#                 "name": "ece\ud83e\udd18\ud83c\udffb",
#                 "protected": false,
#                 "username": "ecssxq",
#                 "verified": false,
#             },
#         ]
#     },
#     "matching_rules": [{"id": "1601645394219376648", "tag": "Players"}],
# }
