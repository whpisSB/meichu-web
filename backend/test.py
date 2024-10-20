import requests

url = "http://140.112.251.50:5000/exchange_reward"

# payload = {
#     "user_account": "ycy.yo@gmail.com",
#     "user_password": "test"
# }

# payload ={
#     "RepositoryID": "repo4",
#     "GithubID": "ycy.yo444",
#     "CommitCount": 10,
#     "Additions": 10,
#     "Deletions": 10,
#     "Total": 10,
#     "Summary": "summary",
#     "Reviewers": "reviewers"
# }

payload = {
    "line_id": "U6d7b420fec2d8fc88fdc073603990788",
    "reward_id": 1
}
#/user_rewards?line_id=Ua0e4d2058f68cfb9c16953c29bac8399
#                      Ua0e4d2058f68cfb9c16953c29bac8399
response = requests.post(url,json=payload)
# response = requests.get("http://140.112.251.50:5000/ping")
response.raise_for_status()
print(response.json())

