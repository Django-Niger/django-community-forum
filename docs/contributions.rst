Contributions
=============

How to Contribute to the Development of Django-community-forum
--------------------------------------------------------------

Thank you for your interest in contributing to Django-community-forum! Here are some guidelines to help you get started.

Setting Up Your Development Environment
---------------------------------------

1. **Clone the repository**:
   
   Begin by cloning the repository to your local machine:

   .. code-block:: bash

       git clone https://github.com/yourusername/django-community-forum.git
       cd django-community-forum

2. **Create a virtual environment**:

   It's recommended to create a virtual environment to keep dependencies required by different projects separate. If you are using Python 3, you can create a virtual environment by running:

   .. code-block:: bash

       python -m venv venv
       source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install dependencies**:

   Install all the required packages using the provided `requirements.txt`:

   .. code-block:: bash

       pip install -r requirements.txt

4. **Set up the database**:

   Run the following command to set up your local database:

   .. code-block:: bash

       python manage.py migrate

5. **Run the development server**:

   Start the development server to see your changes:

   .. code-block:: bash

       python manage.py runserver

Code Style and Formatting
-------------------------

To ensure consistency throughout the source code, we enforce a coding standard and formatting guidelines. Please ensure your contributions adhere to these standards:

- We use `Black` for code formatting. Make sure to run Black on your code before submitting a pull request:
  
  .. code-block:: bash

      black .

- Follow PEP 8 guidelines for writing idiomatic Python code.

Testing
-------

Before submitting your changes, make sure all the tests pass:

.. code-block:: bash

    python manage.py test

Additionally, add tests for any new functionality or bug fixes. Comprehensive tests help ensure that the codebase remains reliable and maintainable.

Submitting Changes
------------------

Once your changes are ready:

1. Push your changes to a branch in your fork of the repository.
2. Submit a pull request to the `develop` branch of the original repository.
3. Ensure your pull request describes the changes you are making and any relevant context.
4. Engage in the code review process to get your changes accepted into the project.



Pre-commit Configuration
------------------------

To ensure that the codebase remains clean and consistent, we use pre-commit hooks. These hooks check for formatting issues and run tests automatically before each commit is made. Here’s how you can set up pre-commit in your local development environment.

1. **Install pre-commit**:

   Install the pre-commit tool if it isn't already installed:

   .. code-block:: bash

       pip install pre-commit

2. **Configure pre-commit**:

   The pre-commit configuration is defined in a file called `.pre-commit-config.yaml` at the root of the repository. This file contains definitions for the hooks that will be run before each commit. Here's a breakdown of our configuration:

   - **Black**:
     We use Black to format our Python code. The specific version of Black we use is locked to ensure consistency across all setups.
   - **Django Tests**:
     Runs Django unit tests to ensure that changes do not break the application.

   Here is the content of our `.pre-commit-config.yaml`:

   .. code-block:: yaml

       repos:
         - repo: https://github.com/psf/black
           rev: 24.4.2  # Utiliser la version de Black que tu as installée
           hooks:
             - id: black
               language_version: python3.11.6  # Assure-toi que cela correspond à ta version de Python
         - repo: local
           hooks:
             - id: django-tests
               name: Run Django Tests
               entry: python manage.py test
               language: system
               pass_filenames: false

3. **Install Hooks**:

   To install the pre-commit hooks into your Git hooks, run the following command in the repository root:

   .. code-block:: bash

       pre-commit install

   This command will set up the hooks to run automatically before each commit.

4. **Run Hooks Manually**:

   If you wish to manually run the hooks on all files, perhaps to ensure everything is formatted before making a large commit, you can do so with:

   .. code-block:: bash

       pre-commit run --all-files


Pull Request Guidelines
-----------------------

When submitting a pull request, please adhere to the following guidelines:

- **Base Branch**: Target the `develop` branch for your pull requests.
- **Description**: Provide a detailed description of what your changes do and why you have made them. Include any relevant issue numbers.
- **Conflict Resolution**: Before submitting your pull request, rebase your branch on the latest `develop` to make sure your changes are up to date and resolve any conflicts that arise.

Communication
-------------

Contributing to Django-community-forum is not just about submitting code. We encourage you to participate in discussions and decision-making:

- **Issues**: Feel free to open issues for bugs, feature requests, or improvements.

