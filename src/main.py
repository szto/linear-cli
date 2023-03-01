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
def branch(api_key: str = typer.Argument(..., envvar="LINEAR_API_KEY", show_envvar=False)) -> None:
    """
    Create a branch from lienar issue
    """
    client = _get_gql_client(api_key=api_key)
    query = _compose_gql_to_get_linear_issues()

    # Get format
    data = client.execute(query)
    team_key = data.get("teams").get("nodes")[0].get("key")  # type: ignore[union-attr]

    features = _get_features()
    issues = _get_issues(data=data, team_key=team_key)

    questions = [
        inquirer.List("issue", message="What task are you working on?", choices=issues),
        inquirer.List("feature", message="Choose feature.", choices=features),
    ]

    answers = inquirer.prompt(questions)
    feature_selected = answers.get("feature")
    issue_selected = answers.get("issue")

    # Create this branch
    typer.echo(f"git checkout -b {feature_selected}/{issue_selected}")

    # Sync with gh
    typer.echo(f"gh pr create {feature_selected}/{issue_selected}")


def _get_features() -> list[str]:
    return ["feat", "fix", "chore", "docs", "refactor", "test"]


def _get_issues(data: Any, team_key: str) -> list[str]:
    issues = []
    for issue in data.get("viewer").get("assignedIssues").get("nodes"):
        title = issue.get("title").replace(" ", "-").replace("/", "")
        number = issue.get("number")
        issues.append(f"{team_key}-{number}-{title}".lower())
    return issues


def _compose_gql_to_get_linear_issues() -> DocumentNode:
    return gql(
        """
        query {
            teams { nodes { key } }
            organization { gitBranchFormat }
            viewer {
                id
                name
                email
                assignedIssues (first: 20) { nodes { title number previousIdentifiers } }
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
