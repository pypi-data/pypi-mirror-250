**********
Link Medic
**********

.. image:: https://img.shields.io/pypi/v/linkmedic
   :name: PyPI
   :target: https://pypi.org/project/linkmedic/

.. image:: https://img.shields.io/badge/License-BSD_3--Clause-blue.svg
   :name: License: 3-Clause BSD
   :target: https://opensource.org/licenses/BSD-3-Clause

.. image:: https://img.shields.io/badge/python-%3E=3.7-blue
   :name: Minimum required python version: 3.7

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :name: Coding style: Black
   :target: https://github.com/psf/black

A python script for checking links and resources used in local static webpages (``.htm``, ``.html``), OpenDocument files (``.odt``, ``.odp``, ``.ods``), and single OpenDocument XML files (``.fodt``, ``.fodp``, ``.fods``).

``linkmedic`` starts a test webserver, requests entry page from the test webserver and crawls all the local pages. All the links in the tags (``<a>`` ``<img>`` ``<script>`` ``<link>`` ``<iframe>`` ``<event-listener>``) are checked and the dead links are reported. If a link is present in multiple pages, only once it will be tested. By default, links to the external websites are ignored. If there is a ``.linkignore`` file in the website's root, the links listed in that file will be ignored during the tests (one link per line, see below for examples). After checking all the links if any dead links are discovered, ``linkmedic`` exits with a non-zero code.

For testing links in dynamic html content e.g. using JS template engines, or other document formats, you must first convert your files [with a thirdparty tool] to static html and then run ``linkmedic``.

Quick start
###########

prerequisites
*************
Depending on your operating system, you may have multiple options for installing them:

* `python <https://www.python.org/downloads/>`__: ``linkmedic`` is only tested on `officially supported python versions <https://devguide.python.org/versions/>`__.
* ``python`` package installer: For example, `pip <https://pip.pypa.io/en/stable/installation/>`__

Install linkmedic
*****************
You can install the ``linkmedic`` using your favorite python package installer. For example using ``pip`` you can download it from `PyPI <https://pypi.org/project/linkmedic/>`__:

.. code-block:: shell

  pip install linkmedic --user


Run
***
To start a test webserver with files at ``/var/www`` and crawl the pages and test all the links starting from ``/var/www/index.html`` page, run:

.. code-block:: shell

  linkmedic --root=/var/www


Usage & Options
###############

Mirror package repository
*************************

You can also install ``linkmedic`` from MPCDF GitLab package repository:

.. code-block:: shell

  pip install linkmedic --user --index-url https://gitlab.mpcdf.mpg.de/api/v4/projects/5763/packages/pypi/simple


Container
*********
You can use one of the container images with required libraries (and `linkmedkit <https://gitlab.mpcdf.mpg.de/tbz/linkmedkit>`_ tools) already installed in:

.. code-block:: shell

  quay.io/meisam/linkmedic:latest

.. code-block:: shell

  gitlab-registry.mpcdf.mpg.de/tbz/linkmedic:latest

You can access a specific version on ``linkmedic`` using container tags e.g. ``linkmedic:v0.7.4`` instead of ``linkmedic:latest``. See all available container tags `here <https://quay.io/repository/meisam/linkmedic?tab=tags>`_.

Using a container image, ``linkmedic``'s test webserver needs to have access to the files for your website pages from inside the container. Depending on your container engine, you may need to mount the path to your files inside the container. For example, using `podman <https://podman.io>`_:

.. code-block:: shell

  podman run --volume /www/public:/test quay.io/meisam/linkmedic:latest linkmedic --root=/test

Here, ``--volume /www/public:/test`` flag mounts ``/www/public`` inside the container at ``/test`` path.

.. _ci-cd:

CI/CD
*****
You can also use the container image in your CI/CD pipelines. For example, for GitLab CI in ``.gitlab-ci.yml``:

.. code-block:: yaml

  test_internal_links:
    image: quay.io/meisam/linkmedic:latest
    script:
      - linkmedic --root=/var/www/ --entry=index.html --warn-http --with-badge
    after_script:
      - gitlab_badge_sticker.sh


or for Woodpecker CI in ``.woodpecker.yml``:

.. code-block:: yaml

  test_internal_links:
    image: quay.io/meisam/linkmedic:latest
    commands:
      - linkmedic --root=/var/www/ --entry=index.html --warn-http

If you want to check the external links of your website in CI, you must avoid running multiple tests in a short period of time, e.g. on each commit of the development branches. Otherwise, the IP of your CI runners may get banned by external web servers. For example, in GitLab CI you can limit the external link checks only to the default branch of your git repository:

.. code-block:: yaml

  test_external_links:
    image: quay.io/meisam/linkmedic:latest
    rules:
      - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    script:
      - linkmedic --root=/var/www/ --ignore-local --with-badge
    after_script:
      - gitlab_badge_sticker.sh
    allow_failure: true  

Please note that ``gitlab_badge_sticker.sh`` script used in these examples requires an API access token with maintainer permission ``CI_API_TOKEN`` to modify the badges. See `linkmedkit documentation <https://gitlab.mpcdf.mpg.de/tabriz/linkmedkit>`_ for more details.

CLI reference
*************

* Display help. Will show all the command line options and their default values.

.. code-block:: shell

  linkmedic -h

* Start the webserver with the current directory as the root path of the server. Starting from ``index.html`` crawl the pages and test all the links.

.. code-block:: shell

  linkmedic

* Start the webserver with ``./tests/public1/`` as the root path of the server. Starting from ``index.html`` crawl the pages and test all the links.

.. code-block:: shell

  linkmedic --root=./tests/public1/

* Start the webserver with ``./tests/public1/`` as the root path of the server. Starting from ``index2.html`` crawl the pages and test all the links. Entry point should be relative to the server root. (in the example below, ``index2.html`` should be accessible at ``./tests/public1/index2.html``)

.. code-block:: shell

  linkmedic --root=./tests/public1/ --entry=index2.html

* Configure test webserver not to redirect missing pages (``/directory/page`` to ``/directory/page.html``).

.. code-block:: shell

  linkmedic --no-redirect

* Check links to external websites.
  
  [**IMPORTANT**: You must avoid running the link checker on external links multiple times in a short period of time, e.g. on each commit of the develop branch. Otherwise, IP of your machine (or CI runners) may get banned by the CDN or the DoS mitigation solution of the external webservers. See `CI/CD section <ci-cd_>`_ for a solution.]

.. code-block:: shell

  linkmedic --check-external

* Ignore local dead links [and activates external link checking].

.. code-block:: shell

  linkmedic --ignore-local

* Do not consider the external links which return HTTP status codes 403 and 503 as dead links.

.. code-block:: shell

  linkmedic --ignore-status 403 503

* Check links in an OpenDocument file (``.odt``, ``.odp``, ``.ods``), or a single OpenDocument XML file (``.fodt``, ``.fodp``, ``.fods``).

.. code-block:: shell

  linkmedic --entry=./presentation.odp

* Show warning for HTTP links.

.. code-block:: shell

  linkmedic --warn-http

* If any link to ``mydomain.com`` is encountered, treat them as internal links and resolve locally.

.. code-block:: shell

  linkmedic --domain=mydomain.com

* Start the webserver on port 3000. If the webserver could not be started on the requested port, the initializer will automatically try the next ports.

.. code-block:: shell

  linkmedic --port=3000

* Generate badge information file. Depending on the type of diagnosis, this file will be named ``badge.dead_internal_links.json``, ``badge.dead_external_links.json``, or ``badge.dead_links.json``. if ``--warn-http`` flag is used, a badge file for the number of discovered HTTP links will be also written to ``badge.http_links.json`` file. These files can be used to generate badges (see `linkmedkit`_ scripts) or to serve for `shields.io endpoint <https://shields.io/endpoint>`_ response.

.. code-block:: shell

  linkmedic --with-badge

* Check the links but always exit with code 0.

.. code-block:: shell

  linkmedic --exit-zero

* Log the output in a different level of verbosity. If more than one of these flags are defined, the most restrictive one will be in effect.

  -  ``--verbose`` : log debug information
  -  ``--quiet`` : only log errors
  -  ``--silent`` : completely silence the output logs

Example .linkignore
*******************

.. code-block:: shell

  invalidfile.tar.gz
  will_add/later.html
  https://not.accessible.com


Development
###########
This project is using `PDM <https://pdm.fming.dev/latest/>`_ for packaging and dependency management, `vermin <https://pypi.org/project/vermin/>`_ and `bandit <https://pypi.org/project/bandit/>`_ for validation, `black <https://pypi.org/project/black/>`_ and `isort <https://pypi.org/project/isort/>`_ for styling, and `jsonschema <https://pypi.org/project/jsonschema/>`_ and `jq <https://jqlang.github.io/jq/>`_ for testing. See `developers guide <DEVELOPERS.rst>`_ for more details.

History
#######
The original idea of this project is from Dr. Klaus Reuter (MPCDF). Fruitful discussions with Dr. Sebastian Kehl (MPCDF) facilitated this project’s packaging and release.

Accompanying tools for the ``linkmedic`` have been moved to a separate repository (`linkmedkit`_) in version 0.7.

License
#######
* Copyright 2021-2023 M. Farzalipour Tabriz, Max Planck Computing and Data Facility (MPCDF)
* Copyright 2023-2024 M. Farzalipour Tabriz, Max Planck Institute for Physics (MPP)

All rights reserved.

This software may be modified and distributed under the terms of the 3-Clause BSD License. See the LICENSE file for details.
