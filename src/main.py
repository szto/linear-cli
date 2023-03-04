import os
from typing import Any

import inquirer
import typer
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from graphql import DocumentNode

app = typer.Typer(pretty_exceptions_show_locals=False)


@app.callback()
def callback() -> None:
    """
    Awesome Linear
    """


@app.command()
def branch(
    api_key: str = typer.Argument(..., envvar="LINEAR_API_KEY", show_envvar=False),
) -> None:
    """
    create linear branch
    """
    try:
        client = _get_gql_client(api_key=api_key)
        query = _compose_gql_to_get_linear_issues()

        # Get format
        data = client.execute(query)

        features = _get_features()
        issues = _get_issues(data=data)

        questions = [
            inquirer.List("issue", message="What task are you working on?", choices=issues),
            inquirer.List("feature", message="Choose feature.", choices=features),
        ]

        answers = inquirer.prompt(questions)
        feature_selected = answers.get("feature")
        issue_selected = answers.get("issue")

        # Create this branch
        command = f"git checkout -b {feature_selected}/{issue_selected}"
        copy_to_clipboard(text=command)
        typer.echo(f"copy to clipboard: {command}")
    except Exception:
        typer.echo("Something went wrong!")


@app.command()
def open() -> None:
    """
    open linear app
    """
    os.system("open /Applications/Linear.app")


@app.command()
def issue(
    issue_number: str,
    organization: str = typer.Argument(..., envvar="LINEAR_ORGANIZATION", show_envvar=False),
) -> None:
    """
    open linear issue
    """
    os.system(f'open "" https://linear.app/{organization}/issue/{issue_number}')


def copy_to_clipboard(text: str) -> None:
    command = "echo " + text.strip() + "| pbcopy"
    os.system(command)


def _get_features() -> list[str]:
    return ["feat", "fix", "chore", "docs", "refactor", "test"]


def _get_issues(data: Any) -> list[str]:
    issues = []
    for issue in data.get("issues").get("nodes"):
        title = issue.get("title").replace(" ", "-").replace("/", "")
        identifier = issue.get("identifier")
        issues.append(f"{identifier}-{title}".lower())
    return issues


def _compose_gql_to_get_linear_issues() -> DocumentNode:
    return gql(
        """
        query {
          issues(first: 20, filter: {assignee: {isMe: {eq: true}}}) {
            nodes {
              title
              number
              identifier
            }
          }
        }
        """
    )


def _get_gql_client(api_key: str) -> Client:
    return Client(
        transport=RequestsHTTPTransport(
            url="https://api.linear.app/graphql",
            use_json=True,
            headers={
                "Content-type": "application/json",
                "Authorization": api_key,
            },
        ),
    )


if __name__ == "__main__":
    app()
