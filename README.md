# Sporty WAP Tests
<h1 align="center">Web Automation with Pytest and Selenium</h1>

## Links

- [Repo](https://github.com/marmiou/sporty-tests "Automation with Selenium framework")

## Prerequisites

Before you begin, ensure you have met the following requirements:
- You have installed Python 3.8 or higher on your machine. You can check by using 
```bash
python3 -V
```
- You have installed Poetry for dependency management. If you haven't, follow the installation instructions below.

### Installing Poetry

Poetry is a tool for dependency management and packaging in Python. To install Poetry, run the following command:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```
For other installation methods, visit the [official Poetry documentation](https://python-poetry.org/docs/).

NOTE: Don't forget to add Poetry in the path (in your .bashrc or .zshrc file)

- You have installed Allure, which will be our Reporting tool

### Installing Allure
```bash
brew install allure
```

## Installation

After installing Poetry, clone the project repository and navigate to the project directory:

```bash
git clone git@github.com:marmiou/sporty-tests.git
cd sporty-tests
```
Install the project dependencies by running:
```bash
poetry install
```

## Available Commands
To activate the project's virtual environment and run tests:
```bash
poetry shell
pytest
```

Alternatively, you can run commands within the virtual environment without activating it by using poetry run. 
For example, to run a specific test file:
```bash
poetry run pytest tests/test_strreamer_loaded.py
```

Or, to run all e2e tests:
```bash
poetry run pytest
```

Reports of the run can be found under the directory:
```bash
allure/reports
```

To open reports execute:

```bash
allure serve reports/allure-results
```

## Built With

- Pytest
- Selenium
- Poetry
- Allure reporter
- isort
- black

## Screen Recording of the implemented test uploaded in github repo twitch-test-gif:
![Alt Text](https://github.com/marmiou/twitch-test-gif/blob/main/mytest-bigger.gif)

## Repo Structure explained:
The structure of the repo is the following:
![Alt Text](https://github.com/marmiou/twitch-test-gif/blob/main/repo-structure.png)

- .github: Contains github actions so that we can run the tests on CI. This is WIP and is still failing
  - auto trigger of tests on push
  - manual trigger of tests from github Actions
In general, github contains any configuration related to github (example we could have an issue template here)
- configuration: Contains anything related with the configuration of the repo. Just a small note, we used config.ini file,
but we did not use the configuration in our project after all
- pageObjects: Used Page Object Pattern, so the two Page Objects (Twitch & Streamer), which contain all the
interactions with these pages are placed here (elements + functionality).
- tests: directory with the test & the conftest file
- utilities: this was not used after all, but we can place here any code not related to the previous directories
- reports: Not a repo dir, it is produced after test execution. 
It contains produced allure-results + produced screenshot

## Known issues:
- [Issue #1 Handle muted videos](https://github.com/marmiou/twitch-tests/issues/1)
- [Issue #2 Handle categories](https://github.com/marmiou/twitch-tests/issues/2)

## Author

**Markella Efthymiou**
- [GitHub Profile](https://github.com/marmiou/ "Markella Efthymiou")
- [Email](mailto:efthymioumarkella@gmail.com?subject=Hi "Hi!")

## 🤝 Support

Contributions and issues are welcome!

Give a ⭐️ if you like this project!
