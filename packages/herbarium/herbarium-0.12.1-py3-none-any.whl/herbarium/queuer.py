import re
from dataclasses import dataclass
from typing import Protocol

from .git_utils import StagingMigrater
from .issue_service import Issue
from .subprocess_utils import interactive_cmd


@dataclass(frozen=True)
class ParsedIssue:
    prefix: str
    description: str


def sanitise_text_for_bash(input_string: str) -> str:
    char_to_remove = ["`"]
    for character in char_to_remove:
        input_string = input_string.replace(character, "")
    return input_string


def sanitise_text_for_git(input_string: str) -> str:
    char2replacement = {
        " ": "-",
        ":": "/",
        ",": "",
        "'": "",
        '"': "",
        "(": "",
        ")": "",
        "[": "",
        "": "",
        "`": "",
        ">": "",
        "<": "",
        "=": "",
    }

    for character, replacement in char2replacement.items():
        input_string = input_string.replace(character, replacement)

    return input_string.replace("--", "-")


def parse_issue_title(issue_title: str) -> ParsedIssue:
    # Get all string between start and first ":"
    prefix = re.findall(r"^(.*?):", issue_title)[0]
    description = re.findall(r": (.*)$", issue_title)[0]

    return ParsedIssue(
        prefix=sanitise_text_for_git(input_string=prefix),
        description=sanitise_text_for_git(input_string=description),
    )


class Queuer(Protocol):
    def sync(self):
        ...

    def create_queue_from_trunk(self, issue: Issue):
        ...

    def add_to_beginning_of_queue(self, issue: Issue):
        ...

    def add_to_end_of_queue(self, issue: Issue):
        ...

    def submit_queue(self, automerge: bool):
        ...

    def status(self):
        ...


class Graphite(Queuer):
    def sync(self):
        interactive_cmd("gt sync --force")

    def create_queue_from_trunk(self, issue: Issue):
        with StagingMigrater():
            interactive_cmd("gt trunk")
        self.add_to_end_of_queue(issue)

    def add_to_beginning_of_queue(self, issue: Issue):
        first_commit_str = self._get_first_commit_str(issue)
        branch_title = self._get_branch_title(issue=issue)

        with StagingMigrater():
            interactive_cmd("gt bottom")

        interactive_cmd("gt trunk")
        interactive_cmd(f'gt create {branch_title} --all --insert -m "{first_commit_str}"')
        interactive_cmd(f'git commit --allow-empty -m "{first_commit_str}"')

    def add_to_end_of_queue(self, issue: Issue):
        first_commit_str = self._get_first_commit_str(issue)
        branch_title = self._get_branch_title(issue=issue)

        interactive_cmd(f'gt create {branch_title} --all -m "{first_commit_str}"')
        interactive_cmd(f'git commit --allow-empty -m "{first_commit_str}"')

    def _get_first_commit_str(self, issue: Issue) -> str:
        first_commit_str = f"{issue.title}"
        if issue.entity_id is not None:
            first_commit_str += f""" (issue #{issue.entity_id})

Fixes #{issue.entity_id}"""

        return sanitise_text_for_bash(first_commit_str)

    def _get_branch_title(self, issue: Issue) -> str:
        parsed_issue = parse_issue_title(issue.title)
        entity_id_section = "" if issue.entity_id is None else f"/{issue.entity_id}"
        return f"{parsed_issue.prefix}{entity_id_section}/{parsed_issue.description}"

    def submit_queue(self, automerge: bool):
        submit_command = "gt submit --no-edit --publish"

        if automerge:
            submit_command += " --merge-when-ready"

        interactive_cmd(submit_command)

    def status(self):
        interactive_cmd("gt log short --reverse")
