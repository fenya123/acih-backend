"""Clean-up script for cleanup workflow's previous runs/

Delete previous workflow runs of cleanup.yml.
"""

import os
from pathlib import Path

from github import Auth, Github


GITHUB_ACCESS_TOKEN = os.environ["GITHUB_ACCESS_TOKEN"]
GITHUB_CLEANUP_WORKFLOW = "cleanup.yml"
GITHUB_REPOSITORY = os.environ["GITHUB_REPOSITORY"]


ROOT_DIR = Path(__file__).parents[3]
if not (ROOT_DIR / ".github" / "workflows" / GITHUB_CLEANUP_WORKFLOW).exists():
    raise FileNotFoundError("Workflow file does not exist!")


def main():
    g = Github(auth=Auth.Token(GITHUB_ACCESS_TOKEN))
    repository = g.get_repo(GITHUB_REPOSITORY)
    workflow = repository.get_workflow(GITHUB_CLEANUP_WORKFLOW)
    workflow_runs = workflow.get_runs()
    for run in workflow_runs:
        run.delete()


if __name__ == "__main__":
    main()
