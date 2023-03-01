from setuptools import setup

setup(
    name="linear-cli",
    version="0.1",
    py_modules=["linear"],
    include_package_data=True,
    install_requires=[
        "typer",
        "rich",
        "gql",
    ],
    entry_points="""
        [console_scripts]
        linear=src/main:app
    """,
)
