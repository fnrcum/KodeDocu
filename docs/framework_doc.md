# Automation Setup
## Code setup

### Local environment
1. Download and install [Python 3.9.10](https://www.python.org/downloads/release/python-3910/) 
    1. During the installation check the following checkboxes. 
    > Note: The screenshot is for python 3.9.9 but the link above is for the recommended 3.9.10
     
    <img src="/static/resources/py39install.png" width="100%" height="100%">

2. Download [PyCharm](https://www.jetbrains.com/pycharm/download) community edition
3. Download and install git for your OS flavor: [Git](https://git-scm.com/downloads)
4. Clone the [tests repository](https://bondprotfs.visualstudio.com/NextGen/_git/bp_qa_auto) by running the following command in the terminal: `git clone https://bondprotfs.visualstudio.com/NextGen/_git/bp_qa_auto`
    1. For more information on terminal based git commands, please reference this [Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
5. Open PyCharm and open the cloned folder as a project
6. Open PyCharm terminal and install the python dependencies:  `pip install -r requirements.txt` and `pip install -r requirements-local.txt` in this exact order!
    1. Follow the prompts to authenticate to Azure for the dependencies. The prompts will give you a code and a link where to put the code in.
7. Install the playwright browser bindings:  `playwright install`
8. Install [Docker Desktop](https://docs.docker.com/desktop/)
    1. This is not immediately necessary but is a must-have to be able to confirm tests will run well under linux

### Local environment - Run your tests
#### Run tests using Pycharm IDE
1. Open Run/Debug configuration window and click the *Edit configuration templates* link
2. Select Python tests and then pytest.
3. Add the environment variable into the Environment Variables input, e.g. `ENVIRONMENT=surety-dev`
4. Make sure the python interpreter (python 3.9) and workspace (tests project root folder) are correctly set
<img src="/static/resources/run_configs.png" width="100%" height="100%">
5. Now you can run any test by right-clicking on it and hit run (similar for test classes).
#### Run tests from terminal
1.  In the terminal, navigate to the project location
2.  Run the following command to add the environment variable to the current terminal session e.g.  `export ENVIRONMENT="surety-dev"`
3.  Run the tests in the following ways:
    1. To run ALL tests, run the following terminal command:  `pytest`
    2. To run tests in a specific file:  `pytest tests/test_login_page.py`
    3. To run a specific test from a file without using tags:  `pytest tests/test_playground.py::Tests::test_input`  where “Tests” is the class and “test_input” is the specific test
    4. To run tests in headed mode:  `pytest -m playground --headed`
    5. To run tests on a specific browser (default is chromium):  `pytest -m playground --browser firefox`
        1. To run tests on multiple browsers: `pytest -m playground --browser firefox --browser chromium --browser webkit`
        2. Playwright supports Chrome (chromium), Firefox and Safari/Mobile (webkit)
    6. To run a specific tag, run the following command:  `pytest -m playground --template html1/index.html` where “playground” is the tag name
    7. To run tests by filters with logical operators:
        1.  `pytest -m "not playground"`  Will run all tests that do not have the tag  `login`
        2.  `pytest -m "playground and api"`  Will run all tests that have both tags at the same time
        3.  `pytest -m "playground or api"`  Will run all tests that have at least 1 of the 2 tags
    8. To run tests and get a list of the slowest tests run the tests in the following way:  `pytest -m playground --durations=2 --durations-min=0.1`  where  `--durations=2`  are the number of tests to be displayed and  `--durations-min=0.1`  is the minimum duration above which to collect the info in seconds
    9. To run tests with coverage: `pytest -v --cov PAF --cov-report html -m playground --template html1/index.html`
  
4.  After test execution, a *reports* folder will be created containing a  `report.html`  file and folders with the screenshots and video recordings of the failing tests.
    1.  The report will display the screenshots and the videos of the failing tests as embedded so even if  `report.html`  is moved or sent through an email, it should still contain them

### Docker environment runs

1.  Open your terminal (make sure you have docker installed on your machine)
2.  Navigate to the project folder and create the docker image:  `docker build -t bp_qa_auto .`
    1.  `-t bp_qa_auto`  tells docker the name of the newly created docker image
4.  After the image is created, make sure you have a folder called  `reports`  in your current path
5.  To run all tests from the docker image:  `docker run -d -e ENVIRONMENT="<some env>" --rm -v ${PWD}/reports:/bp_qa_auto/reports --name bp_tests bp_qa_auto --template=html1/index.html`
    1. `-d`  tells docker to run in detached mode
    2. `-e ENVIRONMENT="<some env>"`  tells docker to add an environment variable called  `ENVIRONMENT`  with the value  `<some env>`
    3. `--rm`  tells docker to remove the container after it finished
    4. `-v ${PWD}/reports:/bp_qa_auto/reports`  tells docker to attach your current path to the  `reports`  folder to the  `/bp_qa_auto/reports`  folder inside docker to have access to the reports after completion
        1.  `${PWD}`  will print your current working directory and will work on all linux and Mac systems
        2.  For Windows PowerShell use:  `-v $pwd\reports:/bp_qa_auto/reports`
        3.  For Windows Command prompt use:  `-v (@echo %cd%\reports):/bp_qa_auto/reports`
    5. `--name bp_tests`  tells docker to name the started container  `bp_tests`
    6. `bp_qa_auto`  is the docker image we are executing which we named at step 3.
    7. `--template=html1/index.html`  specifies the to use as a global template from the python packages
    8. The docker version runs pytest with coverage by default
    9. To run tests with the rerun module: `docker run -d -e ENVIRONMENT="<some env>" --rm -v ${PWD}/reports:/bp_qa_auto/reports --name bp_tests bp_qa_auto --template=html1/index.html --reruns=5` where `5` is the number of times the tests will be retried before the result is final
        1. You can also add a delay (in seconds) between the reruns: `--reruns-delay=1`
        2. You can also specify to only rerun the tests on specific errors: `--only-rerun=AssertionError --only-rerun=ValueError`
           1. Note that the errors come from python and any Python based error is supported
        3. Tests cal also be marked as flaky and reran individually 
        ```python 
        @pytest.mark.flaky(reruns=5, reruns_delay=2)
        ```
        4. Tests can also be marked for reruns based on conditions such as running platform
        ```python 
        @pytest.mark.flaky(reruns=5, condition=sys.platform.startswith("win32"))
        ```
6.  The docker container can take all the filters and flags from the normal pytest run for its execution such as:
    1.  `docker run -d -e ENVIRONMENT="<some env>" --rm -v ${PWD}/reports:/bp_qa_auto/reports --name bp_tests bp_qa_auto --template=html1/index.html -m=playground`  will run all the tests marked with the  `playground`  tag
        1.  Caveat, all flags must use the  `=`  operator to assign the values
    2.  `docker run -d -e ENVIRONMENT="<some env>" --rm -v ${PWD}/reports:/bp_qa_auto/reports --name bp_tests bp_qa_auto --template=html1/index.html -m="not playground"`  will execute exactly as the local version
    3.  `docker run -d -e ENVIRONMENT="<some env>" --rm -v ${PWD}/reports:/bp_qa_auto/reports --name bp_tests bp_qa_auto --template=html1/index.html --browser firefox --browser chromium --browser webkit`  will run exactly as the local version
7.  While docker runs in detached mode, you will not have access to the console output. to get it, you must follow the logs:
    1.  `docker run -d -e ENVIRONMENT="<some env>" --rm -v ${PWD}/reports:/bp_qa_auto/reports --name bp_tests bp_qa_auto --template=html1/index.html ;docker logs -f pff`
        1.  Caveat is that the colouring of the logs will not be done

### Running playwright in interactive browser mode with code generation

After the above local setup has been completed
1.  Run the following command to start the playwright interactive codegen browser:  `playwright codegen`
2.  The above browser and interactive code console will be displayed
    1.  Please note that this tool is best suited to formulate selectors and strategies to approach pages or to experiment potential scripts to interact with the page before transforming the code into the normal framework standard
3.  While the record button is running, all interactions on the page and all page navigations will be recorded in the form of code that can be executed to replicate those interactions.

### Project structure (modules and setup files)

####Modules:
1. `api_tests`  module for automated api tests
2. `ui_tests`  module for automated UI tests
3. `data`  module for test data such as data enums or users information
4. `endpoints`  module containing the AOM (Api Object Model) which is essentially identical to the POM but is designed to be used for API endpoints and interactions
5. `page`  module for the page objects
6. `reports`  is the folder that will be populated with reports when tests complete execution
    1.  Note that this is for local test runs, this folder will be different for Jenkins docker runs. Please see the docker section of the code setup
7. `report_template` is the folder that holds the reporter extensions
8. `resources` is the folder that holds resource files for project documentation

####Setup files:
8. `.dockerignore`  is the file that contains the list of items that will be ignored when performing a docker build
9. `.gitignore`  is the file that contains the list of items to be ignored by git when committing work
9. `__init__.py`  is the file that denotes a package in Python
10. `conftest.py`  is the most important file which contains the bulk of the framework interaction as per the PyTest standard.
11. `Dockerfile`  is the file that defines how the docker image will be built
12. `pytest.ini`  is the PyTest standard configuration file
13. `requirements.txt`  is the file that defines the Python packages that need to be installed for the project to work
    1.  Note that the python package installation requires PyPi access unless all required packages are hosted locally in a manager such as Artifactory
14. `sources.list`  is a linux sources file that defines what sources to be added to the package repository.

For more information about PyTest, please visit:  [https://docs.pytest.org/en/latest/contents.html](https://docs.pytest.org/en/latest/contents.html)

### Coding standards

The coding style standards followed by this project will be in line with the python PEP-8 standards.  [https://www.python.org/dev/peps/pep-0008/](https://www.python.org/dev/peps/pep-0008/)

For more information about the PlayWright please follow:  [https://playwright.dev/python/docs/intro/](https://playwright.dev/python/docs/intro/)

## Contributing

### Branching
Work will be exclusively done in git branches and 
>NOTE: No work shall be done directly in the main branch
- To create a branch: `git checkout -b <branch name>`
   - branch naming convention will be: "initials/ticket number or change name" eg: `nf/doc_changes`
- Pull Requests will include Nicu and Catalin and will not be completeable or margeable without both approvals
   - <img src="/static/resources/gitflow2.png" width="100%" height="100%">
   - 

- All changes will contain a branch, and we do not require a PR for any branches outside of main.
   - <img src="/static/resources/gitflow1.png" width="100%" height="100%">

### Workflow
1. Create a new branch
2. At the start of every day, update your local branch with the changes merged to main: `git pull --rebase origin main`
   1. This step implies fixing any conflicts that appear: [Tutorial](https://www.simplilearn.com/tutorials/git-tutorial/merge-conflicts-in-git)
3. At the end of the day, if your changes are not yet ready for a PR (pull request), push them to the remote in your branch
   1. `git add .` or `git add -A`
   2. `git commit -m "Commit message which must be descriptive"`
   3. `git push origin <branch name>` please refer to the branch naming convention in the #Branching section above
      1. This is to ensure that no changes are lost in the event of any local system failure
4. If the changes are ready, a [PR](https://bondprotfs.visualstudio.com/NextGen/_git/bp_qa_auto/pullrequestcreate?targetRef=main) will be created
   1. Choose the source branch which in this case is your own branch and create the PR

We also suggest Git crash courses like [This](https://www.udemy.com/course/git-going-fast/) or any such lecture to get more accustomed to using a source control like git        

## Custom report example (self-contained)

The following is an example report generated by the tests with some intentional failures to display the screenshot and video capture capabilities of the test framework.

NOTE: The  `playground`  tests are just example tests for general playwright use cases

<img src="/static/resources/report_img.png" width="100%" height="100%">

##[Allure sanity test report dashboard](http://chubb-stg.westus2.cloudapp.azure.com:5050/allure-docker-service/projects/sanity/reports/latest/index.html#)