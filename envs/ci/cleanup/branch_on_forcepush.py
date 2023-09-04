"""Clean-up script for commits that no longer exist.

Delete GitHub Actions workflow runs for commits that no longer exist
(i.e. commits that are lost after squashing and force pushing).
"""

import os

from github import Auth, Github


REBASED_BRANCH_NAME = os.environ["REBASED_BRANCH_NAME"]
GITHUB_ACCESS_TOKEN = os.environ["GITHUB_ACCESS_TOKEN"]
GITHUB_REPOSITORY = os.environ["GITHUB_REPOSITORY"]


def main():
    g = Github(auth=Auth.Token(GITHUB_ACCESS_TOKEN))
    repository = g.get_repo(GITHUB_REPOSITORY)

    branch_commit_shas = []
    for commit in repository.compare(repository.default_branch, REBASED_BRANCH_NAME).commits:
        branch_commit_shas.append(commit)

    workflow_runs = repository.get_workflow_runs(branch=REBASED_BRANCH_NAME)
    for run in workflow_runs:
        if run.head_sha not in branch_commit_shas:
            run.delete()


if __name__ == "__main__":
    main()
