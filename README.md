# linear cli

## Pre-requisites
- set linear api key
```shell
LINEAR_API_KEY="set your api key here"
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
mv dist/src/linear.pex ~/.local/bin/linear.pex

in .zshrc
alias linear="LINEAR_API_KEY="your api key" ~/.local/bin/linear.pex"
```

## Run
```zsh
linear --help
linear branch -- choose linear issue to create branch
linear open -- open linear application
linear issue {issue_number} -- open issue in browser
```
