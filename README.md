# linear cli for Payhere

## Pre-requisites
```zsh
LINEAR_API_KEY="set your api key here"
```

## Installation

```zsh
pants pacakge src/linear:linear
mv dist/src/linear.pex ~/.local/bin/linear.pex

in .zshrc
alias linear="LINEAR_API_KEY="your api key" ~/.local/bin/linear.pex"
```
