# Repo Fetcher
The Repo Fetcher is a versatile tool designed to extract the essential contents from GitHub repository. <br>
It seamlessly retrieves files, excluding specified patterns, to offer a concise overview of the repository's key components.<br> This tool proves invaluable for developers, project managers, and contributors seeking a quick glance at the project structure without the noise of unnecessary files <br>

If you find any noice contents getting printed, please [mail](alfareedss472@gmail.com) me.
## Example
from FetchRepo.RepoFetcher import harvest_github_repo <br>
repo_link = "https://your/github-repo/link" <br>
access_token = "your access token" #(requireed if the repository is private) <br>
code = harvest_github_repo(repo_link,branch="branch_name",access_token="access_token") <br>
print(code)

- If you don't know the branch name to be fetched from, you can also leave it empty, {branch="} it will list (display) all the branches from the repo and prompts you to enter the required feature brnach to be fetched.
- If the repo is public let the value for the  access_token be empty ; <br>
harvest_github_repo(repo_link,branch="",access_token="")