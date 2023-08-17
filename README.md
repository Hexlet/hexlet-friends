# Hexlet Friends

[![](https://github.com/Hexlet/hexlet-friends/workflows/CI/badge.svg)](https://github.com/Hexlet/hexlet-friends/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/dedb9f8ad241a9152fd0/maintainability)](https://codeclimate.com/github/Hexlet/hexlet-friends/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/dedb9f8ad241a9152fd0/test_coverage)](https://codeclimate.com/github/Hexlet/hexlet-friends/test_coverage)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

A service to track contributions from members of the Hexlet community to the Hexlet open-source projects on GitHub.

Contribution &mdash; issues, pull requests, commits, comments.

## Setup

_[Instructions for installing and running the app](INSTALLATION.md)_

_[Instructions for deploying app on Render](DEPLOYMENT.md)_

## Contributing

See [contribution guidelines](./CONTRIBUTING.md)

## Text localization

Install **gettext** (when working with Poetry).

1. Run `make transprepare` &mdash; prepare files ***.po** in directory **locale/ru/LC_MESSAGES**.
2. Make changes in these files.
3. Run `make transcompile`.

### **Please do not do localization in your PR , if you do not have the appropriate issue.**

--

[![Hexlet Ltd. logo](https://raw.githubusercontent.com/Hexlet/assets/master/images/hexlet_logo128.png)](https://hexlet.io/pages/about?utm_source=github&utm_medium=link&utm_campaign=hexlet-friends)

This repository is created and maintained by the team and the community of Hexlet, an educational project. [Read more about Hexlet](https://hexlet.io/pages/about?utm_source=github&utm_medium=link&utm_campaign=hexlet-friends).

See most active contributors on [hexlet-friends](https://friends.hexlet.io/).
