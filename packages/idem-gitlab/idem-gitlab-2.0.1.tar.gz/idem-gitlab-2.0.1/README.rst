===========
idem-gitlab
===========

.. image:: https://img.shields.io/badge/made%20with-pop-teal
   :alt: Made with pop, a Python implementation of Plugin Oriented Programming
   :target: https://pop.readthedocs.io/

.. image:: https://img.shields.io/badge/made%20with-python-yellow
   :alt: Made with Python
   :target: https://www.python.org/

Gitlab provider for idem.

About
=====

Manage Gitlab with ``idem``.

What is POP?
------------

This project is built with `pop <https://pop.readthedocs.io/>`__, a Python-based
implementation of *Plugin Oriented Programming (POP)*. POP seeks to bring
together concepts and wisdom from the history of computing in new ways to solve
modern computing problems.

For more information:

* `Intro to Plugin Oriented Programming (POP) <https://pop-book.readthedocs.io/en/latest/>`__
* `pop-awesome <https://gitlab.com/vmware/pop/pop-awesome>`__
* `pop-create <https://gitlab.com/vmware/pop/pop-create/>`__

Getting Started
===============

Prerequisites
-------------

* Python 3.9+
* git *(if installing from source, or contributing to the project)*

Installation
------------

.. note::

   If wanting to contribute to the project, and setup your local development
   environment, see the ``CONTRIBUTING.rst`` document in the source repository
   for this project.

If wanting to use ``idem-gitlab``, you can do so by either
installing from PyPI or from source.

Install from PyPI
+++++++++++++++++

.. code-block:: bash

   pip install idem-gitlab

Install from source
+++++++++++++++++++

.. code-block:: bash

   # clone repo
   git clone git@gitlab.com/vmware/idem/idem-gitlab.git
   cd idem-gitlab

   # Setup venv
   python3 -m venv .venv
   source .venv/bin/activate
   pip install pip==21 -e .


Usage
=====

credentials
-----------

The preferred authentication method to idem-gitlab is with a personal access token.
To create a personal access token, see the `Gitlab documentation <https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html>`__.
Create an acct_file with the following format:

.. code-block:: yaml

   gitlab:
      default:
         token: <personal_access_token>
         # Optional parameters
         endpoint_url: https://gitlab.com
         api_version: v4
         sudo: <user>
         owned: True

Encrypt the acct_file with:

.. code-block:: bash

   idem encrypt /path/to/acct_file

The first time this command is run, it will output an ACCT_KEY that can be used to decrypt the file.
Put the ACCT_KEY and the ACCT_FILE in the environment variables and idem will find and use your gitlab profile automatically.

.. code-block:: bash

   export ACCT_KEY="<acct_key>"
   export ACCT_FILE=/path/to/acct_file

Once your credentials are in place, you can test them by running any of the following commands:

.. code-block:: bash

   idem exec gitlab.version.get
   idem exec gitlab.metadata.get
   idem exec gitlab.avatar.get email="gitlab_user@example.com"
   idem exec gitlab.namespace.get
   idem exec gitlab.project.commit.get "<commit_sha/branch/tag/null>" project_id="<project_id>"

Supported Resources
-------------------

The following are REFs for resources that are currently supported by idem-gitlab.

- gitlab.group
- gitlab.group.member
- gitlab.group.variable
- gitlab.impersonation_token
- gitlab.personal_access_token
- gitlab.project
- gitlab.project.branch
- gitlab.project.member
- gitlab.project.protected_branch
- gitlab.project.protected_tag
- gitlab.project.tag
- gitlab.project.variable
- gitlab.runner
- gitlab.user


For each ref, there are functions for create, list, get, update, and delete operations.

Idem-gitlab uses the "auto_state" contract to combine these CRUD operations into present and absent states.

Examples
--------

Run CRUD operations using the idem exec commands:

.. code-block:: bash

   idem exec gitlab.project.create path=new_project
   idem exec gitlab.project.list
   idem exec gitlab.project.get "<new_project_id>"
   idem exec gitlab.project.update "<new_project_id>" repository_access_level=private
   idem exec gitlab.project.delete "<new_project_id>"

Create an SLS files based on existing resource:

.. code-block:: bash

   idem describe gitlab.group > /srv/idem/gitlab/group.sls
   idem describe gitlab.group.member > /srv/idem/gitlab/group_member.sls
   idem describe gitlab.group.variable > /srv/idem/gitlab/group_variable.sls
   idem describe gitlab.project > /srv/idem/gitlab/project.sls
   idem describe gitlab.project.branch > /srv/idem/gitlab/branch.sls
   idem describe gitlab.project.member > /srv/idem/gitlab/project_member.sls
   idem describe gitlab.project.protected_branch > /srv/idem/gitlab/protected_branch.sls
   idem describe gitlab.project.protected_tag > /srv/idem/gitlab/protected_tag.sls
   idem describe gitlab.project.tag > /srv/idem/gitlab/tag.sls
   idem describe gitlab.project.variable > /srv/idem/gitlab/project_variable.sls
   idem describe gitlab.runner > /srv/idem/gitlab/runner.sls
   idem describe gitlab.user > /srv/idem/gitlab/user.sls

Create a top-level SLS file that sources all the others:

.. code-block:: yaml

   # /srv/idem/gitlab/init.sls
   include:
     - group
     - group_member
     - group_variable
     - project_member
     - project
     - branch
     - protected_branch
     - protected_tag
     - tag
     - project_variable
     - runner
     - user

Run "idem state" to idempotently enforce changes to the any of the files created:

.. code-block:: bash

   idem state /srv/idem/gitlab

And that's it! You are now using idem-gitlab to manage your gitlab resources.

Testing
=======

To run the tests using a gitlab docker image, first run:

.. code-block:: bash

   docker run -d -p 80:80 --env GITLAB_ROOT_PASSWORD=not_secure gitlab/gitlab-ce

For testing you can use the sample credentials file for tests:

.. code-block:: bash

   export ACCT_FILE=$PWD/example/credentials.yaml

Run the test suite with nox:

.. code-block:: bash

   pip3 install nox
   nox -p 3.11

Autogeneration
==============

Autogeneration utilizes ``pop-create`` to parse the gitlab api and generate modules for new resources.
To perform the autogeneration, first you need to install idem-gitlab with the ``autogen`` extras:

.. code-block:: bash

   pip3 install idem-gitlab[autogen]

Next, run  pop-create to generate the modules in the current directory:

.. code-block:: bash

   pop-create gitlab --directory $PWD --create-plugin auto_state
   pop-create gitlab --directory $PWD --create-plugin tests

These modules won't work out-of-the-box, they will likely need manual changes
to conform them to the rest of idem-gitlab and make them functional.
Once you have fully implemented a new resource, submit a PR and we will review it and hopefully
add it to idem-gitlab's functionality!

Roadmap
=======

Reference the `open issues <https://gitlab.com/vmware/idem/idem-gitlab/issues>`__ for a list of
proposed features (and known issues).

Acknowledgements
================

* `Img Shields <https://shields.io>`__ for making repository badges easy.
