import requests

url = "http://140.112.251.50:5000/icon"

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
    "prompt": "good"
}
#/user_rewards?line_id=Ua0e4d2058f68cfb9c16953c29bac8399
#                      Ua0e4d2058f68cfb9c16953c29bac8399
response = requests.post(url,json=payload)
# response = requests.get("http://140.112.251.50:5000/ping")
response.raise_for_status()
print(response.json())

