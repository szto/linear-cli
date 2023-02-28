import os

import inquirer
import typer
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from graphql import DocumentNode

app = typer.Typer()


@app.callback()
def callback():
    """
    Awesome Linear
    """

@app.command()
def branch():
    """
    Create a branch from lienar issue
    """
    client = _get_gql_client()
    query = _compose_gql_to_get_linear_issues()

    # Get format
    data = client.execute(query)
    team_key = data.get("teams").get("nodes")[0].get("key")

    features = _get_features()
    issues = _get_issues(data=data, team_key=team_key)


    questions = [
        inquirer.List("feature", message="Choose feature.", choices=features),
        inquirer.List("issue", message="What task are you working on?", choices=issues)
    ]

    answers = inquirer.prompt(questions)
    feature_selected = answers.get("feature")
    issue_selected = answers.get("issue")

    # Create this branch
    typer.echo(f"git checkout -b {feature_selected}/{issue_selected}")

    # Sync with gh
    typer.echo(f"gh pr create {feature_selected}/{issue_selected}")


def _get_features() -> None:
    return ["feat", "fix", "chore", "docs", "refactor", "test", "style", "ci", "perf"]


def _get_issues(data, team_key) -> list[str]:
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


def _get_gql_client() -> Client:
    return Client(
        transport=AIOHTTPTransport(
        url="https://api.linear.app/graphql",
        headers={
            "Content-type": "application/json",
            "Authorization": os.getenv("LINEAR_API_KEY"),
            },
        )
    )
