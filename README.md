# Requirements-based testing of MATLAB Simulink models
This example demonstrates how to perform requirements-based testing of a MATLAB Simulink model using the BTC EmbeddedPlatform (BTC). The example includes a Simulink model for a seat heating controller, which is tested against a set of requirements.

### CI Status & Test Report
![CI](https://github.com/btc-embedded/requirements-based-testing/actions/workflows/pipeline.yml/badge.svg)

[BTC Test Report](https://btc-embedded.github.io/requirements-based-testing/report.html)

## Developer testing: Interactive Walk-through
**Preparation**
- Create a new branch for your changes
- Open the `seat_heating_controller.slx` model in MATLAB Simulink.
- Click "Activate" in the BTC EmbeddedPlatform ribbon bar

**First test**
- Create a test case that cycles through the heating stages (button pressed 4 times) and link it to the relevant requirements
- Run the test case and observe the results in the BTC Test Manager

**Debugging**
- Activate the Debug-mode, then add a break in the `convert_to_stage` subsystem
- Debug the test case and identify the issue
- Fix the issue in the model and re-run the test case

**Hierarchical test case**
- In order to test requirement '0 - CondCheck', convert the `activation_condition_check` subsystem to a referenced subsystem
- Navigate into the subsystem and click "New" in the BTC EmbeddedPlatform ribbon bar, then click "Add" to create a test case
- Check that the correct combination of inputs activates the system
- Save the test case

**Triggering Automated Tests**
- Commit your changes to the branch and publish it to GitHub
- Create a pull request
- Navigate to the PR on github.com and check the status of the GitHub Actions pipeline

## Automated Tests 
The GitHub Actions [pipeline](.github/workflows/pipeline.yml) is triggered on pull requests and pushes. It performs the following steps:
- Checkout files: Uses the `actions/checkout@v4` action to check out the repository files.
- Run tests:
    1. Run MIL tests, only continue if all tests pass
    2. Run SIL tests
    3. Publish test results to Polarion
    4. Create HTML report with
        - MIL + SIL test results
        - Code coverage
        - traceability information
- Publish test results to GitHub Pages: Uses the `peaceiris/actions-gh-pages@v4` action to publish test results to GitHub Pages.
- Publish results: Uses the `dorny/test-reporter@v1` action to publish test results, regardless of success or failure.
- Add test report link to PR: Adds a comment to the pull request with a link to the test report


## Model files
The `model` directory contains all files relevant to the Simulink model:
- `seat_heating_controller.slx` (main model)
- `init.m`


## Test files
The `test` directory contains the test projects (interactive MIL project for developer testing + MIL/SIL project with full testing capabilities, code coverage, etc.) and a python script to automate the test execution
