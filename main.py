import os

import inquirer
import typer
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

app = typer.Typer()


@app.callback()
def callback():
    """
    Awesome Linear
    """

@app.command()
def branch(feat: str = typer.Argument("feat", help="feat, fix, chore, etc")):
    """
    linear 로 branch 를 생성합니다.
    """
    client = _get_gql_client()

    query = gql(
        """
        query {
            teams { nodes { key } }
            organization { gitBranchFormat }
            viewer {
                id
                name
                email
                assignedIssues (first: 10) { nodes { title number previousIdentifiers } }
            }
        }
    """
    )

    # Get format
    data = client.execute(query)
    branch_format = data.get("organization").get("gitBranchFormat")
    team_key = data.get("teams").get("nodes")[0].get("key")

    # Build issueIdentifier
    issues = []
    for issue in data.get("viewer").get("assignedIssues").get("nodes"):
        title = issue.get("title").replace(" ", "-").replace("/", "")
        number = issue.get("number")
        issues.append(f"{team_key}-{number}-{title}".lower())

    features = ["feat", "fix", "chore", "docs", "refactor", "test", "style", "ci", "perf"]

    questions = [
        inquirer.List("feature", message="Choose features", choices=features),
        inquirer.List("issue", message="What task are you working on?", choices=issues)
    ]

    answers = inquirer.prompt(questions)
    feature_selected = answers.get("feature")
    issue_selected = answers.get("issue")

    # Create this branch
    typer.echo(f"git checkout -b {feature_selected}/{issue_selected}")

    # Sync with gh
    typer.echo(f"gh pr create {feature_selected}/{issue_selected}")


def _get_gql_client():
    return Client(
        transport=AIOHTTPTransport(
        url="https://api.linear.app/graphql",
        headers={
            "Content-type": "application/json",
            "Authorization": os.getenv("LINEAR_API_KEY"),
            },
        )
    )
