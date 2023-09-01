"""Clean-up script for a deleted branch.

Delete GitHub Actions workflow runs of a branch that has been deleted.
"""

import os
import sys

from github import Auth, Github


DELETED_BRANCH = sys.argv[1]

GITHUB_ACCESS_TOKEN = os.environ["GITHUB_ACCESS_TOKEN"]


def main():
    g = Github(auth=Auth.Token(GITHUB_ACCESS_TOKEN))
    repository = g.get_repo("fenya123/acih-backend")
    workflow_runs = repository.get_workflow_runs(branch=DELETED_BRANCH)
    for run in workflow_runs:
        run.delete()


if __name__ == "__main__":
    main()
