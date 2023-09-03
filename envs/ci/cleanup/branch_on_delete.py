"""Clean-up script for a deleted branch.

Delete GitHub Actions workflow runs of a branch that has been deleted.
"""

import os

from github import Auth, Github


DELETED_BRANCH_NAME = os.environ["DELETED_BRANCH_NAME"]
GITHUB_ACCESS_TOKEN = os.environ["GITHUB_ACCESS_TOKEN"]
GITHUB_REPOSITORY = os.environ["GITHUB_REPOSITORY"]


def main():
    g = Github(auth=Auth.Token(GITHUB_ACCESS_TOKEN))
    repository = g.get_repo(GITHUB_REPOSITORY)
    workflow_runs = repository.get_workflow_runs(branch=DELETED_BRANCH_NAME)
    for run in workflow_runs:
        run.delete()


if __name__ == "__main__":
    main()
