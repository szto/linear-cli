# linear cli

## Pre-requisites
- set linear api key
```shell
zsh
echo 'export LINEAR_API_KEY=set your api key here' >> ~/.zshenv
```
- install pants
```shell
curl --proto '=https' --tlsv1.2 -fsSL https://static.pantsbuild.org/setup/get-pants.sh

or 

brew install pantsbuild/tap/pants
```
- install python 3.9

## Installation

```zsh
pants package ::
sodo mv dist/src/linear.pex /usr/local/bin/linear
```

## Run
```zsh
linear --help
linear branch -- choose linear issue to create branch
linear open -- open linear application
linear issue {issue_number} -- open issue in browser
```

## Donwload
[0.0.1 download](https://github.com/szto/linear-cli/releases/tag/0.0.1)
