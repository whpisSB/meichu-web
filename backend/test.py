import requests

url = "http://140.112.251.50:5000/user_info"

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
    "email": "aaa"
}
#/user_rewards?line_id=Ua0e4d2058f68cfb9c16953c29bac8399
#                      Ua0e4d2058f68cfb9c16953c29bac8399
response = requests.get(url,json=payload)
# response = requests.get("http://140.112.251.50:5000/ping")
response.raise_for_status()
print(response.json())

