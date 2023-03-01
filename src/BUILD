python_sources(
    name="src",
    dependencies=[
        "//:requirements",
    ],
)

pex_binary(
    name="linear",
    entry_point="main.py",
    dependencies=[
        ":src",
    ],
)
