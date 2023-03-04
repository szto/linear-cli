# linear cli

## Pre-requisites
- set linear api key [link](https://github.com/szto/linear-cli/blob/main/src/main.py)
```shell
for zsh
echo 'export LINEAR_API_KEY=set your api key here' >> ~/.zshenv
echo 'export LINEAR_ORGANIZATION=set your organization name for web' >> ~/.zshenv
```
- You may need to install python 3.9 or above.

## Installation

```zsh
download [linear.zip](https://github.com/szto/linear-cli/releases/download/0.0.1/linear.zip)
unzip linear.zip
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
[0.0.1 download](https://github.com/szto/linear-cli/releases/tag/0.0.1) - download linear.zip

## Development
- install pants
```shell
curl --proto '=https' --tlsv1.2 -fsSL https://static.pantsbuild.org/setup/get-pants.sh

or 

brew install pantsbuild/tap/pants
```
- install python 3.9
