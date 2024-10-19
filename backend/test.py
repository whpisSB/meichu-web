import requests

url = "http://140.112.251.50:5000/reward"

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

response = requests.get(url)
# response = requests.get("http://140.112.251.50:5000/ping")
response.raise_for_status()
print(response.json())

