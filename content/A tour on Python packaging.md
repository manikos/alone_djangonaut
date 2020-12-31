Title: A tour on Python Packaging
Date: 2018-11-8
Modified: 2019-5-7
Category: packaging
Tags: python, package, PyPI
Summary: The current state of packaging a Python library (not a Python application).
Description: This post tries to decipher common questions about python packaging and also give an understanding around this concept.
Author: Nick Mavrakis
Status: published


If you're new to Python or a mature one and want to share your code with other developers
or you have build a library to be used by end users and you're struggle with the packaging,
then this tutorial/post/explanatory guide is (possibly) for you.


[TOC]


# [Prerequisites](#prerequisites)

First of all, you **must** understand some basics around Python packaging
terminology or else this (useful) post will turn into an incomprehensible one!

Your first stop is [packaging glossary](https://packaging.python.org/glossary/).
In there, you'll find the terminology around python packaging.
Some things I would like to highlight:

1. `artifact` (not listed): fancy word for file
2. `source distribution (sdist)`: simple, source only `.tar.gz` archive. **Only** for pure Python modules/packages
(ones that do not contain any C/C++ code).
3. The institution set up to deal with distribution in Python is called the [Python Packaging Authority][PyPA].
So, to a programmer, a `distribution` looks like a *directory containing a bunch of Python code* next to a `setup.py` which describes
that code and adds some metadata to it like the name, version, author etc.


# [Assumptions](#assumptions)

This post assumes that python 3.6 is used and you're comfortable with virtualenvs:

- Python 3.6 is used
- [virtualenv](https://virtualenv.pypa.io/en/stable/) is used
  - and more preferably [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/stable/) is used

If neither `virtualenv` or `virtualenvwrapper` are used then, the built-in
`python3 -m venv path/to/virtualenv` command may be used as well but you have
to take care (each time) of the `activate` script and that `pip`, `setuptools` and
`wheel` are installed (things that the above tools do automatically).

When the status of the [PEP 582 - Python local packages directory](https://www.python.org/dev/peps/pep-0582/)
becomes *Final* then we (might) get rid of the 3rd party virtualenv tools.


# [Packaging in Python](#packaging_in_python)

[It has been written](https://packaging.python.org/overview/) and it's quite self-explanatory. Nothing to add here.

> As a general-purpose programming language, Python is designed to be used in many ways.
You can build web sites or industrial robots or a game for your friends to play, and much more, all using the same core technology.

The term *python packaging* is quite broad and depending on the scenario and purpose of the code written, it applies accordingly.
That said, in this post we will focus on [packaging Python source distributions](https://packaging.python.org/overview/#python-source-distributions).
This means to package a [Python package](https://docs.python.org/3/glossary.html#term-package) (for distribution) that contains
pure Python code.


## [Modularity](#modularity)

###  [PyPI](#mod_pypi)
The [PyPI][PyPI] is the one and only deposit area/space where all Python packages are stored
(just like [npmjs](https://www.npmjs.com/) where all Javascript packages are stored).
Of course, you may have a locally Python package which you don't plan to upload to PyPI.
That's OK. But if you want to share your code with others, then PyPI is the answer.

Imagine this deposit area like a warehouse (fun fact: that's the alternate name for PyPI).
The main objective of a warehouse is [the storage of goods](https://en.wikipedia.org/wiki/Warehouse).
Each good is stored inside a container (a box). This container takes its place somewhere inside the warehouse.
Probably, stacked with other goodies.

### [setuptools](#mod_setuptools)
[`setuptools`][setuptools] is a Python library (just like hundreds of thousands ones)
which purpose is to take your Python package (directory) as input
and convert it to an archive in order to be placed in the PyPI index.
It's the recommended tool by the [PyPA][PyPA].

`setuptools`is the tool to wrap your good inside a container and, eventually,
this container be placed inside the warehouse. The insertion into the warehouse is not performed
by `setuptools`, but by another Python package called [`twine`][twine].

### [wheel](#mod_wheel)
[`wheel`][wheel] is a Python library which provides a `bdist_wheel` command for `setuptools`.
A wheel file (`file.whl`) is a ZIP-format archive with a specially formatted filename and
the `.whl` extension.

A `wheel` archive may be considered as a container with specifications (like specific
dimensions, weight, labels etc). All wheels will have the same format and, thus, can be
easily unpacked and introspected. [Skip the rest and read about wheels](#wheels).

### [twine](#mod_twine)
[`twine`][twine] is a Python library which given an OS path to your previously converted
archive files (i.e `path/to/packaged/archive`), it uploads them on the PyPI.
It's the recommended package by the PyPA to publish Python packages on PyPI in a secure manner
(that is over https).

Consider `twine` as the machine that takes your well-wrapped package and inserts it,
with extreme caution, into the warehouse. Now, your package is stored safely amongst other packages!

### [pip](#mod_pip)
[`pip`][pip] is another Python library that acts as a package manager.
It's main role is to download/install/update/downgrade/uninstall packages from/to your system.
When you `pip install` something then what `pip` does is this: it goes to the PyPI index
(unless told to go somewhere else - [even look in local directories](https://pip.pypa.io/en/stable/user_guide/#installing-from-local-packages)
and fetches and install the requested package.

In the warehouse analogy, `pip` is the machine (make it a forklift, if you like)
that enters the warehouse, picks the appropriate container, unpacks it and delivers it to you
(the position of `you` is outside of the warehouse, waiting for your package to come!).

<br><figure style="display: flex; flex-direction: column; justify-content: center; align-items: center;">
  <a name="warehouse_img"></a>
	<img id="pypi-warehouse" src="/images/pypi_warehouse.jpg" alt="Python Package Index Warehouse representation">
	<figcaption>Representation of the PyPI and the relevant tools (image source: <a href="https://www.crown.com/en-us/warehouse-solutions-products.html">www.crown.com</a>)</figcaption>
</figure><br>

So, there you have it, a warehouse (PyPI) to store Python codes (libraries, #3),
a tool to wrap your code (`setuptools`, #1) in specific formats (`sdist` and `wheel`, #3),
a tool to put Python code into the warehouse (`twine`, #2) and a tool to fetch and
install Python code from the warehouse into your machine (`pip`, #4).
This is the backbone knowledge in order to proceed into more on Python packaging.
Once these concepts are clear to your head, then you have everything you need in your arsenal
to package a Python package with ease, reliability and security.
Also, others will be able to download your package and install it without any issues.


## [Difference between `sdist` and `bdist_wheel`](#sdist_wheel_diff)

[PyPUG (Python Package User Guide) has already covered this difference][wheel_sdist_diff]
but I would like to clarify some things.

The command to convert your local directory (which is meant to be a Python library)
into a distributable one is `python setup.py sdist bdist_wheel`.
This command will read your `setup.py` along with other ones (`MANIFEST.in`, `setup.cfg` etc)
and will generate two archives: a `.tar.gz` (`sdist` aka source distribution) and a `.whl`
(`bdist_wheel` aka binary distribution wheel or just `wheel`) one.
You may inspect both of them by double-click on each.

The main difference between the two is that:

1. The `sdist` archive contains a single directory which consists of your source files
   (your actual code which may be either a Python module or a Python package) along with
   the `setup.py`, `setup.cfg`, `MANIFEST.in`etc files (and optionally along with your
   `tests/`, `docs/` directories depending on your `MANIFEST.in` file).
2. The `wheel` contains **only** two directories, the directory that holds your source
   files **only** (without the `setup.py` files etc) and a `.dist-info` directory which
   contains metadata of your package. If you like to learn more on this extra directory,
   read the [PEP 427 -- The Wheel Binary Package Format 1.0][pep_427] and the upcoming
   [PEP 491 -- The Wheel Binary Package Format 1.9][pep_491] which is still in `draft` status.

Another difference is that installing from `wheel` is as simple as copy-paste the two
directories as-is inside the `site-packages` directory of your environment (that's it)
while installing from `sdist` requires this extra step of reading the `setup.py` do any
potential compilation, convert to `wheel` and then add the directories inside the `site-packages` dir.
I am not saying it's bad to install from source but since the author of a package is able to
produce a `wheel` as well, then why not upload that too?
Besides, since [pip prefers wheel][pip_prefers_whl], having both kind of distributions uploaded,
allows one to convert `sidst` to `wheel`, store it (cache it) and next time it will
use the cached one (saving bandwidth).
The other way around, convert `wheel` into `sdist` is not feasible. Put it that way,
`wheel` is a distribution format much more minimal that `sdist`, thus there is no way
for `wheel`s to generate `sdist`s.

If your question is why to have both generated and uploaded to PyPI, the answer is
the edge case of some users which do not have the [`wheel`][wheel] package installed
or have an old version of [`pip`][pip] which does not support installation from `wheel` packages.
On the other hand, having only source distributions uploaded (`sdist`) you enforce users
to compile your package each time they download it.
This may not sound too time-consuming but if your package consists of Python extensions
(i.e C, C++ etc) then compiling those may take a long time comparing with `wheel`.

So, upload both and keep everybody happy!



# [The basics](#thebasics)

By now, you either have a clear image about what is happening or you're completely
lost, regarding, of course, Python packaging. In this chapter we will play with an
imaginable Python package and try to distribute it to other Pythonistas.


## [Name](#name)

The first thing you'll want to consider when your aim is to create a redistributable
Python package (either to use is locally or distribute it via PyPI) is the name of it.
Once the package has been created and begins to grow, if you decide to change the name
of the package in the middle of the road, then it'll be hard to spot and change
references to this name across your project.
Think first, act last. Of course, IDEs will help you do that in an easy manner, but that means
that you had made a frivolous choice.

Nevertheless, assuming that you're going to build something that is related with *flowers*
you'll have to go to [PyPI][PyPI] and search for this term. If it's occupied then see if you
can attach a hyphen (`-`) and add another word into it. Do not name your package with more than two
words and make it possible so others will simply `pip install package` and then in their code do
`import package` or `from package import func`.
Sometimes, of course, this will not be feasible, but please try! It's clean, elegant and lazy (for the others).

Older methods that required to *register* the name of the package before uploading it,
[are gone](https://packaging.python.org/guides/migrating-to-pypi-org/#registering-package-names-metadata).
You, now, proceed directly to uploading artifacts.

We have decided that we would like to build a Python library which will add some more
capabilities (methods) for Python strings and lists.
An idea taken from [lodash](https://lodash.com/) (a famous JS library extending built-in capabilities).
The name of it would be `booster`. I think it's concise, short and right to the point.
Plus, [it's not reserved in PyPI (until this post is written)](https://pypi.org/search/?q=booster)
nor it would be since we'll not upload it. Maybe, a nice choice/idea for the next developer!


## [Cookiecutter](#cookicutter)

We will make our life easier and rely on a cookiecutter to build our package rather than build it from scratch.
That's the reason of a cookiecutter. To make your/our lives as developers easier.

There is one dominant cookiecutter for Python packages: [the cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)
and several other popular forks like [Nekroze](https://github.com/Nekroze/cookiecutter-pypackage),
[ardydedase](https://github.com/ardydedase/cookiecutter-pypackage), [samastur](https://github.com/samastur/cookiecutter-pypackage)
and [thousands more](https://github.com/audreyr/cookiecutter-pypackage/network/members)!
Pardon me if I have missed a *multi-starred* cookiecutter. If so, let me know in the comments below and I'll update this section.

The logic behind a cookiecutter is pretty simple. A project structure has already been written by the author leaving
*placeholders* (usually with `{{ name }}`) to be filled through CLI questions by the developer.

Thus, you `pip install cookiecutter` into your virtualenv (or `pip install --user cookiecutter` to install it under the `~/.local/` directory)
and now you have the `cookiecutter` command available. Note that `cookiecutter` is a CLI command, not a project template. You use this command
along with a project template URL in order to create a project. Thus, you run `cookiecutter <github_repo_url>`,
a series of questions is initiated and at the end you'll have a pre-configured Python package ready to be
developed (not deployed, since there is no source code written by you, yet).
For more info, read the installation guide for the cookiecutter of your choice.
There is [a ton of templates](https://github.com/audreyr/cookiecutter#a-pantry-full-of-cookiecutters) to choose from (from pure Python packages
to Django, Flask, Pyramid, C++, Java, JS, Tornado etc).

In this post, we'll use audreyr's cookiecutter [template for pure Python packages](https://github.com/audreyr/cookiecutter-pypackage).


## [Structure](#structure)

Using the above cookiecutter, the following questions showed up...:

```bash
(distvenv) nick ~/t/boo> cookiecutter https://github.com/audreyr/cookiecutter-pypackage.git
full_name [Audrey Roy Greenfeld]: Nick Mavrakis
email [audreyr@example.com]: web@web.gr
github_username [audreyr]: manikos
project_name [Python Boilerplate]: booster
project_slug [booster]: booster
project_short_description [Python Boilerplate ... a Python package]: Extra functionality for Python strings!
pypi_username [test_user]: test_user
version [0.1.0]:
use_pytest [n]: y
use_pypi_deployment_with_travis [y]: y
add_pyup_badge [n]: n
Select command_line_interface:
1 - Click
2 - No command-line interface
Choose from 1, 2 [1]: 1
create_author_file [y]: y
Select open_source_license:
1 - MIT license
2 - BSD license
3 - ISC license
4 - Apache Software License 2.0
5 - GNU General Public License v3
6 - Not open source
Choose from 1, 2, 3, 4, 5, 6 [1]: 1
(distvenv) nick ~/t/boo>
```

...creating the following project structure:

```bash
(distvenv) nick ~/t/boo>ls
booster

(distvenv) nick ~/t/boo>tree booster/
booster
├── AUTHORS.rst
├── booster
│   ├── booster.py
│   ├── cli.py
│   └── __init__.py
├── CONTRIBUTING.rst
├── docs
│   ├── authors.rst
│   ├── conf.py
│   ├── contributing.rst
│   ├── history.rst
│   ├── index.rst
│   ├── installation.rst
│   ├── make.bat
│   ├── Makefile
│   ├── readme.rst
│   └── usage.rst
├── HISTORY.rst
├── LICENSE
├── Makefile
├── MANIFEST.in
├── README.rst
├── requirements_dev.txt
├── setup.cfg
├── setup.py
├── tests
│   └── test_booster.py
└── tox.ini

3 directories, 25 files
```

Depending on your given answers to the questions the structure may be different,
but some files not, since they are mandatory in order to call this directory a *re-distributable Python package*.

You may have seen in other Python libraries that the source code is inside a directory called `src/`.
I will not advice you to put your code inside the `src/` directory or not.
[There is an open issue on PyPA user guide on github](https://github.com/pypa/python-packaging-user-guide/issues/320)
and if you're brave enough, go read it. After all, it's a great discussion exchanging different thoughts.
That's the spirit of a healthy community!
[There is also a great post that enforces you to use the `src/` dir](https://blog.ionelmc.ro/2014/05/25/python-packaging/).
Decision is yours. Whichever you take, make sure that your package, at the end, is installable and usable without any errors.

Now back to the above, generated, file structure. Do not freak out seeing all these files! Most of them are there to *support* your project.
You may ask if all these are mandatory in order to upload your simple Python package.
No, they are not. If you had, only, the `booster` dir (containing `booster.py` file which is actually your code)
and the `setup.py` file you would be good to go. A single dir and a file. But that would not be too helpful because it lacks:

1. license
2. documentation
3. tests
4. continuous integration (CI)
5. version control

and other goodies which make your package more mature and complete.

Be patient. Do not rush yourself. Spend some time and [write documentation](https://blog.digitalocean.com/documentation-as-an-open-source-practice/)
and tests. Many other developers (including yourself tomorrow) will thank you. Personally, if I see a package with no docs, I skip it.
Short story. Not because it's not useful or I want to penaltize it, but because I don't know how to install and use it.
What do I `import`? What arguments a function takes? How about tests? Is it tested thoroughly? Why do I have to read the source code in order to use it?
All these questions are vital to every developer before using a package (not just a Python one).

How satisfied/confident are you when you see a package with decent documentation and over 80% test coverage? Someone, wrote all these.
Someone that took the writing of his/her Python package, seriously. Maybe it's not a single person but a group of contributors.
It does not matter. Time has been spent in order to write docs and tests. That's what makes a package *beautiful* and *elegant*.

**Lesson learned**: Do not hurry to finish your package. PyPI is not going away. Be fussy not only for coding but to support it as well
(support means *docs* **and** *tests*).


### [requirements_dev.txt](#requirements_dev.txt)

You may have noticed the file `requirements_dev.txt` which contains the requirements (aka dependencies) of your project in case
another developer (or even you, the author) wants to reproduce it. By `pip install`ing the package, these requirements
will **not** be honored. These are just for development cases. [The official docs say][requirements_vs_install_requires]:

> Whereas `install_requires` defines the dependencies for a single project,
Requirements Files are often used to define the requirements for a complete Python environment.

We have not seen `install_requires` [yet](#install_requires), but keep the above statement in mind. Also, note that this file may be named
any name you like. It's just a convention to name it that way.

Suppose, for example, that you and me are working on the `booster` package. We, both, must have the same development environment
which means the same versions of dependencies and, of course, the same Python version. `requirements_dev.txt` ensures scenarios
like this and if I change (or format) my computer then I will be able to reproduce this environment by `pip install -r requirements_dev.txt`
under my virtualenv and will be back to tracks.

You may, also, want to switch `requirements_dev.txt` with `Pipfile` (and its auto-generated brother `Pipfile.lock`).
No changes here. The same logic applies. Instead of `pip install -r requirements_dev.txt` you would do `pipenv install`.


### [Makefile](#makefile)

This is a usual [Make](ftp://ftp.gnu.org/old-gnu/Manuals/make-3.79.1/html_chapter/make_2.html) file which provides some useful
CLI commands to facilitate your development flow.
It's a cookiecutter-specific file and you may alter it at your own needs. Other cookiecutters may have similar `Make` file.
You can view it, in order to see each function details or just write `make` (under the root package directory,
`booster` in our case) and have an overview of the available commands.


### [LICENSE](#license)

The official packaging docs [cover this file](https://packaging.python.org/tutorials/packaging-projects/?highlight=license#creating-a-license)
but I would like to add to it a little more.

This is a mandatory file that **must not be empty**. If it's omitted then the default LICENCE applied to the
project/package is *all rights reserved* which basically means *I, the owner of the package, am the only one allowed
to use this package*. Thus, why bother uploading to PyPI? Just keep it in your local directory. PyPI means sharing and
adding a non-empty `LICENSE` file, respects this.

There is a myriad type of licenses out there and digging into them brings a lot of confusion, resulting in omitting the
file, altogether. Play safe and adopt the MIT or BSD licence. I am not promoting these kind of licenses but it's the
most commonly used for open source projects. The user's limitation, by using a package under one of the above licenses,
is *to keep the name and the copyright declaration intact*. A useful website that might be help you to pick a license
is the [choosealicense.com][choosealicense].

Congratulations, you now have a package ready to be shared!


### [docs/, AUTHORS.rst, CONTRIBUTING.rst, HISTORY.rst and README.rst](#doc_files)

As you might have guessed, these files are documentation files. Each file is pre-filled with content
(thank you cookiecutter) and the tweaks you might do, the first time, are minor. Each file is quite
self-explanatory. Open each file to read the contents and alter it if you like.

These files are written using the [reStructuredText](http://docutils.sourceforge.net/rst.html) file format.
You may use the Markdown format but be aware that `.rst` files are by far more rich and extensible.
They play perfect together with Sphinx. Learning this kind of language may take some time but the benefits you gain are huge.
Did we mention to not rush yourself to finish your beloved Python package?
If you do change the format, however, [you must use a special keyword](https://packaging.python.org/specifications/core-metadata/#description-content-type-optional)
inside the `setup` function, the `long_description_content_type=text/markdown`.
We have not seen this function, yet. [I am keeping the desert for last :)](#setuppy)

Fun fact: The reStructuredText file format may be applied to any kind of text. Not just documentation for you code.
After all, documentation is just text (code-agnostic). You could write a novel too.

Another part of the documentation procedure is [Sphinx][sphinx]. Sphinx is a documentation generator. What this means is that
you write a bunch of `.rst` files, you run `make html` and voila. The HTML look of your ugly-looking files have been
generated. A PDF version is also available. There is list of HTML templates available to choose and also Sphinx can
be customized through the `docs/conf.py` file. The cookiecutter tool, also, provides another `Makefile`, exclusive for
doc facilitation. I think there is no reason, now, not to write docs.

Bonus tip #1: Once docs have been written, you may upload them on [readthedocs.org][readthedocs] (RTD for short).
Just link your github repo to the RTD and you're good to go (you need an account before that).

Bonus tip #2: If your Python package is small enough and writing a bunch of docs would be considered overkill
because there is not much to say about it (that is, *it can all fit in a single file*) then it is perfectly fine
to include just a `README` file. You may then upload it to [readthedocs.org][readthedocs]. Remember that if
you use Markdown, you should change the `long_description_content_type` value inside the `setup()` function.
Beware though, that the skeleton of this file stays the same with the *full version* of the documentation,
which is a *contributing*, a *history* (or *changelog*), an *installation*, a *usage* section etc.


### [tests/ and tox.ini](#tests)

Code without tests is unreliable. Simple as that. It's like having a "friend" on facebook
without actually ever interact with this person. In what context is this person your friend?
Friends, in a general meaning, are people we can count on them. They are reliable. So are
the tests of your code. No more to add here.

Whether you use [pytest][pytest], [unittest][unittest], [nose][nose] or something else, all your
test files should live inside the `test/` directory.

In addition, [tox][tox] is a Python library which helps you to test your code under different
Python versions and contexts in general. It's extremely powerful, quick and easy to use (although,
there is a slight learning curve, at start, in order to understand how to write the `tox.ini` file).


# [setup.py](#setup.py)

After the description of all the aside helper files and folders (excluding the `booster` sub-directory which is actually your
source code), created by the cookiecutter, we are now ready to dive in to the beast called `setup.py`.

I will not go through the evolution of Python packaging because
[Nick Coghlan has already posted about it](http://python-notes.curiousefficiency.org/en/latest/pep_ideas/core_packaging_api.html).
A lot have changed and there is more to come.

Briefly, this file is just a regular Python file which, at top, contains a very important `import` statement:

`from setuptools import setup`

The [setup](https://github.com/pypa/setuptools/blob/master/setuptools/__init__.py#L140) function is the *beast* we mentioned above. It serves two roles:

1. Describes the package (name, author, requirements, scripts etc)
2. It's the tool you run to convert a package (full of source code) into an installable & distributable unit.

Using the electronic engineering terminology, you may say that this component is both active and passive,
depending on how you use it. More on this in a little bit.

After the `import` statement, a simple call to the `setup` function is all you need. An example, using
our `booster` package is shown below.

```python
from setuptools import setup, find_packages


with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

setup(
    # Project information
    name="booster",
    version="0.1.0",
    author="Nick Mavrakis",
    author_email="nick@nick.gr",
    url="https://github.com/manikos/booster/",  # 404, just an example
    license="MIT license",

    # Description
    description="Extra functionality for Python strings.",
    long_description=f"{readme}\n\n{history}",
    long_description_content_type='text/x-rst',

    # Requirements
    python_requires='>=3.6',
    install_requires=[],
    extras_require={
        'test': [  # install these with: pip install booster[test]
            "pytest>=3.8",
            "coverage>=4.5",
            "pytest-cov>=2.6",
            "tox>=3.3",
            "codecov>=2.0",
        ],
    },

    # Packaging
    packages=find_packages(include=["booster", "booster.*"]),
    include_package_data=True,
    zip_safe=False,

    # Tests
    test_suite="tests",

    # CLI
    entry_points={
        "console_scripts": ["transform=booster.cli:string_transform"]
    },

    # Metadata
    keywords="string strings accent beautify",
    project_urls={
        'Documentation': 'https://booster.readthedocs.io/en/latest/',
        'Tracker': 'https://github.com/manikos/booster/issues/',
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
```

Again, do not freak out. This is the present state of packaging in Python and believe it or not
it's better than ever. Also, if you think that this `setup.py` file is confusing, have a look
at other Python libraries and then you may freak out!

The `setup` function is called using keyword arguments (not positional ones). The whole list of these parameters
can be found in the [setuptools docs](https://setuptools.readthedocs.io/en/latest/setuptools.html#new-and-changed-setup-keywords).

Recalling the first role of `setup.py` file above, calling this function, allows us to describe the package metadata, dependencies etc.
Recalling the second role of `setup.py` file above, executing (through the shell) `python setup.py <command>` allows us to
do things (build artifacts, wheels etc) with the package. The artifacts that may be generated using the CLI command,
contain (as text in specific dirs/files) the metadata, dependencies etc written inside the `setup` function. So, these two
roles are, somehow, interconnected.

You may now visit [PyPI][PyPI] and pick a package which has both formats available for download (in the `Downloads` section, on the left).
Download both archives (`.whl` and `.tar.gz`). Open the `.whl` and inspect the `.dist-info/` dir.
Open, also, the `setup.py` file inside the `.tar.gz` and see the call to the `setup()` function.
You will find all the `setup()` keyword-value items inside the `.dist-info/METADATA` file.
I hope, by now, the two roles of `setup.py` are now distinguished and understood.

When you run `python setup.py sdist` in order to create a source distribution ([we will talk about that](#source-distribution-aka-sdist))
and your `setup()` is empty, then the script will run with no errors but your source distribution will be named `UNKNOWN`
and you will get some nice warnings:

```bash
warning: check: missing required meta-data: name, url
warning: check: missing meta-data: either (author and author_email) or (maintainer and maintainer_email) must be supplied
```

which are quite self-explanatory: at least pass the `name`, `url`, `author` and `author_email` as arguments to `setup` function.
But, please, do not supply only these! This is just for demonstration purposes. You should be explicit about your package.

Now, lets take a deep breath and dive in to the `setup` basics.


## [Metadata](#metadata)

This section is named *Metadata* but it's a kind of **grouping**, of `setup` function, in my head. No official docs call it
this way. Because, `setup` contains a lot of keyword arguments I want to organize them into logical groups. Thus,
I give it the name of *Metadata* to distinguish it from the other keywords. After all, it's the easy part.

In this section, `setup(**kwargs)`, the - pretty straightforward - keyword arguments contain the:

- `name`: name of the package (what other users will `pip install`)
- `author`: your name (after all you're the author)
- `author_email`: a contact email of yours
- `url`: project's URL (usually a VCS url)
- `license`: a string declaring the license title (the full body is written in the `LICENSE` file)
- `description`: a string containing a short/brief description of the package
- `long_description`: a string with more details (usually the same as the `README` file)
- `long_description_content_type`: one of `'text/plain'`, `'text/x-rst'` (default) or `'text/markdown'`
- `keywords`: just a list of strings (not used anywhere practically for the moment)
- `project_urls`: dictionary of `title: url` key-value pairs.
- `classifiers`: [a list of predefined strings](https://pypi.org/classifiers/) to be used for
  filtering/searching when searching via the [PyPI][PyPI] website

Again, all of the above might be too much, but the cookiecutter has already pre-filled most of them for us with
sane defaults (actually the defaults are the [answers you gave through the console](#structure)).
You may edit them, add new ones, delete some etc. These were, more or less, the easy-to-understand ones.


## [Requirements](#kwarg_requirements)

### install_requires
We discussed earlier about environment reproduction using `requirements_dev.txt` or `Pipfile` or any other tool
you might use to resolve dependencies. But how about the dependencies of the project itself?
These are declared through the `install_requires` keyword argument. It's a list of strings and contains all
the 3rd party libraries (if any) your project/library depends on. If your library depends on `foo` Python
library, then inside the `install_requires` list, the `'foo'` string must be included, otherwise when the end-user
will `pip install <library_name>` then the `foo` library will not be installed resulting in an error when running
you package.

Remember, the `requirements_dev.txt` is used for `pip install -r requirements_dev.txt` only (for development
purposes), while `install_requires` is used only during the installation of the library (`pip install <library_name>`).

You are allowed not to have a `requirements_dev.txt` file at all. Also, if your project does not depend on other
libraries, the `install_requires` may be omitted as well. But, if your project is dependent on other libraries
you must have the `install_requires` inside the `setup` function.

The best practice when you list dependencies is not to pin them (i.e `library==x.y`) to a specific version.
Just specify the minimum major version and you're to go (i.e `"library>=x.y"`). The reason for this practice
may be found [here](https://blog.miguelgrinberg.com/post/the-package-dependency-blues).


### [python_requires](#kwarg_python_requires)
The `python_requires` [argument](https://packaging.python.org/guides/distributing-packages-using-setuptools/#python-requires)
specifies to the installer tool ([pip][pip], [poetry][poetry] etc) under which Python
version this package may run. If, for example, you're working in a virtualenv with Python 3.6 interpreter and you want
to install a package named `foo` which has declared `python_requires==2.7`, then `pip` will exit with an error message:

```bash
(py_36_venv) $ pip install foo  # foo is Python 2.7 compatible only
Could not find a version that satisfies the requirement foo (from versions: )
No matching distribution found for foo
```

You should fill this one since it prevents early running errors regarding Python versions.


### [extras_require](#kwarg_extras_require)
This is a handy way of installing additional packages by simply *enabling flags*. Based on the [above](#setuppy) `setup`,
if I want to download this package and install *test*-related packages only, then I would run `pip install booster[test]`,
where `test` (the name inside the brackets) is a key of the dictionary. This key maps to a list of dependencies and thus
by executing this command the test-related packages will be installed. You may have a ton of other *aside* packages
grouped together under a single name (all these under this dictionary), i.e `"security": [...]`.
A reminder though, do not confuse this requirement setting with the `install_requires` one.
The former is (usually) for other developers while the latter is for the end user which will simply do `pip install booster`.


## [Entry points](#kwarg_entry_points)

This is a handy feature of `setuptools` which allows us to define CLI commands which when executed, certain
Python functions will run.

For example suppose that inside the `booster/cli.py` file, we have written the following:

```python
# booster/cli.py

def string_transform():
    print('string transformed!')
```

and, recalling the `setup` function [above](#setuppy):

```python
from setuptools import setup

setup(
    entry_points={
        "console_scripts": ["transform=booster.cli:string_transform"]
    },
)
```

Now, once the package has been installed, opening a console we can simply write
`transform` and the message `string transformed!` will get printed on screen.

What is happening, behind the scenes, is that `setuptools` create an executable file
inside the `bin/` directory of the `virtualenv` dir (just like `pip`, `wheel` and other commands that
are available through the command line) which maps to the function(s) declared in the value of the
key `console_scripts`, under the `entry_points` dictionary.

The string is composed of `"<cli_command_name>`=`<python_dottted_path_to_module>`:`<function_name>"`.
Of course, the above function instead of printing something it can return something, accept parameters
(`transform <a string here> <another one>`) etc. If you plan to have cli support then [Click][click]
is a must-have library to do this kind of things.


## [Packaging](#packaging_general)

This will be the most hard-to-explain section, but I will do my best. You know, there are several
things in life where while you're trying to explain a single thing, another thing needs to be explained first and
then you realise that another thing needs to be explained first etc and at the end you forget what
you were trying to explain at the first place! Same rule applies here but I'll try to be consistent and not get lost.

First of all, before talking about packaging, we must understand the available forms of packaging. Referring to the
[image at the beginning](#warehouse_img), Python packages come in two forms: wheels and source distributions (#3 on image).
It can also be seen from the image below:

<br><figure style="display: flex; flex-direction: column; justify-content: center; align-items: center;">
  <a name="packaging_formats_img"></a>
	<img id="packaging-formats" src="/images/packaging_whl_tar.png" alt="Python Packaging Formats (sdist and wheel)">
	<figcaption>Python packaging formats: built distribution and source (wheel and sdist, respectively)</figcaption>
</figure><br>


### [Wheels (aka built distribution)](#wheel)

[The wheel binary package format](https://www.python.org/dev/peps/pep-0427/) or *built distribution*
or just *wheel* is a way to package code into a redistributable way. The abstract of it's PEP, is quite comprehensive:

> A wheel is a ZIP-format archive with a specially formatted file name and the `.whl` extension.
It contains a single distribution nearly as it would be installed according to PEP 376 with a particular installation scheme.
Although a specialized installer is recommended, a wheel file may be installed by simply unpacking into site-packages
with the standard 'unzip' tool while preserving enough information to spread its contents out onto their final paths at any later time.

In other words, instead of having a source distribution file that pip downloads, unpacks and runs "setup.py install",
the wheel format has things, effectively, in the format that they need to be when they are installed on the system.
So pip can just unpack the zip file (.whl) in a very specific way, but you don't actually have to run any code to do installs.
This means that installs are much faster and safer since you don't execute arbitrary code from the internet.

[Wheels come in three flavors](https://packaging.python.org/guides/distributing-packages-using-setuptools/#wheels):
universal, pure Python and platform. Because of its compiled extensions (C extensions), Numpy comes in platform wheels.
Take a minute and choose the appropriate distribution wheel. Simple rule of thumb: Does your package contains pure
Python code? If yes, choose either pure Python (does not support both Python 2 and 3) or universal (your package
does support both Python 2 and 3). If no, then you must go with platform wheel. No worries, though. The command
is the same in all options: `python setup.py bdist_wheel`. The onle point of difference is inside the `setup.cfg` file.
[We will get to that](#setupcfg).

Furthermore, wheel formats have another advantage. Their filename says a lot about the package. Have a minute and visit the
[numpy downloadble file list](https://pypi.org/project/numpy/#files). There is a whole list of different wheels
(the source distribution is at the bottom). Luckily, you don't have to choose one, download and install. `pip`
will do it for you automatically, depending on your OS system, Python version etc. My point here is that the author
of the package has the ability to make the package installable on different platforms, Python versions etc, using
the wheel format. No chance with the source dist one.

Visiting PyPI and examining some packages, you may see that not all packages have a wheel format. However, all of them
have a source distribution one. A good practice is to **always generate both wheel and source distributions** each time
you upload a new version of your package.

Now that we have explained what a wheel is, theoretically, lets build one for our booster package.
The command that builds a wheel is `python setup.py bdist_wheel`. If you like, run `python setup.py bdist_wheel --help`
to get a list of options applied to this command (most popular is `--universal`).
If you get an error running this command, then your working Python environment has not the [wheel][wheel]
library installed (which is installed automatically every time you create a virtualenv using the [virtualenv][virtualenv] library).
You can see that using `setup.py` this way, it acts as the 2nd role we described earlier (tool for handling packages etc).
Note that no code has been written yet inside the `booster/booster.py` file.
It doesnt matter because at this point we're focusing on the package rather the contents of each file.

```bash
$ cd path/to/booster/
$ python setup.py bdist_wheel
running bdist_wheel
running build
...
```

If you examine the root `booster` directory, you will see that three new directories have been created:
`booster.egg-info/`, `build/` and `dist/`. Leave the first two folders intact and focus on the `dist` one.
This would be the directory (although it's name may be changed, `-d` option) where you'll place your wheels
and your source distributions as well. These two go together. Always. Remember that. wheel + sdist = BFF
like we wrote in the 90's.
The contents of the `.whl` file are two folders: `booster/` and `booster-0.1.0.dist-info/`. If you paste
the `booster/` folder into your virtualenv `site-packages` folder, then `booster` would be available in your
Python path (i.e you can do `import booster`).

- Aside fact #1: there is another way to build a wheel for your package (although, the above method
  should always be used). Once inside the root directory of the package run `pip wheel -w dist --no-deps .`
  (this will create only a `dist/` dir which includes the `.whl` file).

- Aside fact #2: We have mentioned the [wheel][wheel] library but we have not used it yet. In fact you never
  have to play with it but you may install wheels through this library also. Again, this is not the recommended
  way. Once you have a wheel of your library, you may install it with `wheel install dist/booster-0.1.0-py2.py3-none-any.whl`.
  Verify that by doing: `pip freeze | grep booster`. There it is! But `wheel` command has no uninstall procedure
  which signifies that this method is unsuitable for installing/uninstalling packages. To uninstall it run
  `pip uninstall booster`. Press `y` (for yes) and it's gone.

- Aside fact #3: Since `pip` can install wheels, let's take a look of a manual way of doing that. Again, this is
  not the recommended way. Inside the root package run `pip install --no-index --find-links=. dist/booster-0.1.0-py2.py3-none-any.whl`.
  Because the default behavior of `pip` is to look for package in the PyPI index we tell it to not look at any (`--no-index`)
  and advise it to look for packages in the current dir (`--find-links=.`). Next follows the path of the wheel file.
  This works brilliantly but it's overkill to write all these every time!

- Aside fact #4: Enter developer mode. Or else `editable` mode. When you develop your package, instead of
  `pip install` it every time you make a change (or you want to examine a `print` statement somewhere) you may
  symlink it and then all changes will be applied automatically. You can either do `python setup.py develop`
  (which shows a verbose output) or `pip install -e .` (where the dot at the end specifies the current working
  directory which is the project root one) which gives a suppressed output but pay close attention at it.
  It says `Running setup.py develop for booster`. So, the same command is used.
  Anyhow, I prefer to use the latter (`pip install -e .`) and I'm good to go.

- Aside fact #5: You may notice that wheels include only what's under your source code directory. Anything else
  outside will not be included (because, simply, it's not needed in order for your library to run). So, if your
  `MANIFEST.in` file (we'll look at it [below](#manifestin)) includes other dirs/files outside the `booster/`
  root source directory, running `python setup.py bdist_wheel`, the produced `.whl` archive will not include those.
  However, it will include any dirs/files (written in the manifest) that are inside the `booster/` root source dir.
  On the other hand, all the above are not valid for the `sdist` distribution. In this format, almost everything
  are included in the `.tar.gz` archive.

- Aside fact #6: You may produce a wheel artifact out from an `sdist`, but not the other way around.

- Aside fact #7: You might have heard of Python `.egg` files. These kind of archives are considered obsolete.
  The official packaging docs state that [wheels are now considered the standard](https://packaging.python.org/discussions/wheel-vs-egg/).
  So, there is no need to worry about them. Consider `wheel` the upgraded version of `egg`.


### [Sdist (aka source distribution)](#sdist)

Source distribution (sdist for short) is actually a `.tar.gz` file which contains not only the directory
where your code lives but also the other files (depending of the contents of `MANIFEST.in` file)
inside the root directory of the package (such as `setup.py`, `setup.cfg` etc).
Some packages on PyPI either have only `sdist`s, `wheel`s or both. `pip` will always prefer a `wheel`
because it's faster and requires no compilation at all. In contrast, if `wheel` file is missing,
`pip` will download the sdist, run `python setup.py install` and finally install the lib. Sdist
has all the information needed to build a wheel, install the library etc. That's why it's called
*source* distribution.

To build a sdist simply `python setup.py sdist`. Note that this command will not create a `build/` dir
like `bdist_wheel` did earlier. It creates a `booster.egg-info/` and a `dist/` folder. Inside the `dist/`
folder you can see the `.tar.gz` archive which contains your package with all the accompanying dirs and
files.

Of course, running `python setup.py sdist --help` will show you the available options for the sdist argument.
There are other formats you can archive your package. `python setup.py sdist --help-formats` to see the list.

Usually, we do not run `python setup.py bdist_wheel` and `python setup.py sdist` individually. We combine
these commands into a single one `python setup.py bdist_wheel sdist` (`bdist_wheel` comes first in case you forget ;)
and any options on each argument (if any) are included in the `setup.cfg` file. What? How `setup.py` file gets the
options from the `setup.cfg` file? We will look [at it in a moment](#setupcfg) when we will talk about `setup.cfg`.

In order to facilitate this process, the `Makefile` (created by the cookiecutter) has a command called `dist` which
first deletes the `build/` dir, the `dist/` dir, any hidden `.eggs/` dir, any `.pyc` files and other stuff and finally
runs `python setup.py bdist_wheel sdist` in order to generate the new distribution pair of artifacts. Run it as
`make dist`.

Reminder: Until now, we have talked about how to wrap your package into a format that can be uploaded to PyPI and
be distributed to the Python world. We have not talked about how to upload a package to PyPI or once uploaded
how to install it in your machine. We have talked about the number 3 referring to [the image on top](#warehouse_img). Although,
we have used `pip` (#4) and `setuptools` (#1).


### [Packages](#kwarg_packages)

The `packages` keyword argument to `setup()` function tells `setuptools` where to look to find Python code.
It takes a list of strings declaring Python package names. We could, in our example, not used the
`find_packages` function at all and instead write `setup(packages=["booster"])` or use the `find_packages`
without any parameters, `setup(packages=find_packages())`. It would be exactly the same.
This argument (`packages`), however, is important because if you got it wrong then your actual code will not be included inside
the distributable package (both the wheel and the sdist)!

The handy function `find_packages` is given some parameters and it looks for Python modules.
[setuptools docs for find_packages function](https://setuptools.readthedocs.io/en/latest/setuptools.html#using-find-packages)
explain it very well:

> Anyway, `find_packages()` walks the target directory, filtering by inclusion patterns
and finds Python packages (any directory). Packages are only recognized if they include an `__init__.py` file.
Finally, exclusion patterns are applied to remove matching packages.

In our case, we have a single dir called `booster/` and under it three Python modules
(`booster.py`, `cli.py` and `__init__.py`). The `find_packages` function is called without any arguments resulting
in including this dir into the distributable one. If, however, this dir was not a Python package (without the
`__init__.py` module) then it will not be included by this function.

Fire up a Python console and import `find_packages` from `setuptools`:

```python
from setuptools import find_packages

find_packages()
# ['booster']
```

Now, delete the `booster/__init__.py` and run `find_packages` again:

```python
from setuptools import find_packages

find_packages()
# []
```

It doesnt matter how many subpackages your main package have. The `find_packages` function
will work recursively and find them all. However, if you have, say, a file named `config.json`
or `config.yml` or anything that does not have a `.py` suffix and you want to include it, because
somewhere you parse it and use it, then `find_packages` will not help you there.

These kind of files are not Python ones and thus they are called *data files*. There are many
scenarios on including those files and once again
[setuptools docs for data files](https://setuptools.readthedocs.io/en/latest/setuptools.html#including-data-files)
have all these covered in an explicit fashion.


### [zip_safe](#kwarg_zip_safe)

To be really honest I don't quite comprehend this setting and to always play safe I set it on `False`.

As per the [PEAK docs say about setuptools](http://peak.telecommunity.com/DevCenter/setuptools#setting-the-zip-safe-flag):

> For maximum performance, Python packages are best installed as zip files.
Not all packages, however, are capable of running in compressed form, because they may expect
to be able to access either source code or data files as normal operating system files.
So, setuptools can install your project as a zipfile or a directory
and its default choice is determined by the project's zip_safe flag.

Also [a post on medium](https://medium.com/@madumalt/python-setuptools-adding-non-code-files-to-a-package-804f9e914807)
tries to explain `zip_safe` option. Last but not least read this
[answer on StackOverflow about `zip_safe`](https://stackoverflow.com/questions/15869473/what-is-the-advantage-of-setting-zip-safe-to-true-when-packaging-a-python-projec).

As I understand it, unless you know what you're doing keep `zip_safe=False`. Most Python packages (small and big ones) have it `False`.


### [test_suite](#kwarg_test_suite)

This option, once again is covered by the [setuptools docs](https://setuptools.readthedocs.io/en/latest/setuptools.html#test-build-package-and-run-a-unittest-suite).
When set, then you'll be able to run `python setup.py test` and the test suite will get initiated.

In our example, the `test_suite` keyword is set to the `tests/` directory. That's it. Try to run `python setup.py test` and
see the already written by the cookiecutter test run and succeed. Since we are using `pytest` we can also run tests using
`pytest` or `py.test` or `python setup.py pytest`.
If you get the error `E   ModuleNotFoundError: No module named 'booster'` then you have not installed `booster` in your virtualenv.
Do that first (`pip install -e .`) and then rerun `pytest`.


### [setup.cfg](#setup.cfg)

This file is not mandatory but most of the times comes in handy due to repetition of `setup.py` command options.
It's an `ini` file and describes how the `setup.py` is going to run. Instead of doing `python setup.py bdist_wheel --universal`,
you set this option inside the `setup.cfg` as follows:

```ini
# apply to the "setup.py bdist_wheel" command
# the universal option with a value of 1 (that is, set it to true)
[bdist_wheel]
universal=1

[aliases]
test=pytest
```

A general practice is to list the available `setup.py` commands with `python setup.py --help-commands`
and for each command, list it's available options, i.e `python setup.py --help sdist`. Then, if
you want an option to persist while you create `sdist` formats, you write it down to `setup.cfg` along
with it's corresponding value.

However, this is not true for the `alias` command. Although, the command is `python setup.py alias <alias_name> <alias_command>`
the corresponding entry in the `setup.cfg` is `[aliases]`. Delete this section and save `setup.cfg`.
Then run `python setup.py alias test pytest`. This will write to the `setup.cfg` the lines that you previously deleted.
The `[aliases]` was added.

There are other Python libraries, such as [bump2version][bump2version] (a library to manage your package's version) that
are *compatible* with `setup.cfg` and allow you to define their command options inside this file. Then, whenever
you run `bumpversion minor` the file `setup.cfg` will be read under the hood for any options defined.

Another technique that gains popularity is to make the `setup.cfg` fat and keep `setup.py` thin. What is meant
by this is to put all the metadata inside the `setup.cfg` so that the `setup.py` will, eventually, consist of
the following:

```python
from setuptools import setup

setup()
```

It can't be any simpler! It's a matter of choice. I prefer to keep my balances and have them both
in a sane size.

Nevertheless, it's a good idea to have `setup.cfg` in place, in order not to forget certain options, since this file provides
defaults for the `setup.py` script (in other words it describes how the `setup.py` script behaves).

A good read on this is the [official python docs on distributing python modules (legacy version)](https://docs.python.org/3/distutils/configfile.html)


### [MANIFEST.in](#manifest.in)

This file defines everything else that needs to be included in your source distribution (not the wheel)
that isn't actually necessary for the code to run itself. In contrast to `setup.py` file which defines
the code that's going to be executed, which code do I need to include, the requirements of the
project etc (where all these are for functional purposes), `MANIFEST.in` file describes other
files/dirs you need to include in your source distribution (such as docs, tests, images, html files, examples etc).

[As mentioned earlier](#packages), data files (anything other than `.py` files) are not included by default
in your distributable package. To do so you must use the `include_package_data=True` keyword argument
of the `setup()` function and the script will read the `MANIFEST.in` file and include all dirs/files
listed into the sdist one (and to the wheel if they are under the source root directory).

So, the keyword arguments of `setup()`: `include_package_data`, `package_data` and `exclude_package_data` work together
with the `MANIFEST.in` file in a combination fashion in order to determine what *other files* are to be included in the `sdist`
package format. In fact, any files that match `exclude_package_data` patterns will be included in the `sdist` format but
when the package gets installed on the system (`pip install package`) they will be excluded from the installation.

You may read more on the `MANIFEST.in` file on the [official Python docs about MANIFEST.in](https://docs.python.org/3/distutils/sourcedist.html#specifying-the-files-to-distribute).

If you find yourself lost with this kind of file (as I did in the beginning), [check-manifest][check-manifest]
is very good tool that kind of *syncs* version controlled dirs/files with the `sdist` one.
It also recommends which files should be added to the `MANIFEST.in` file.


# [Upload](#upload)

Once you have your Python package wrapped in a distributable form (remember, **both wheel and sdist**) then it's
time to share it. Your distributable ones, conventionally, live under the `dist/` dir, in the same level as
`setup.py` is. The place where all Python packages are stored is called [PyPI][PyPI].
Since, an image worth a thousand words, here you are:

<br><figure style="display: flex; flex-direction: column; justify-content: center; align-items: center;">
  <a name="packaging_upload_img"></a>
	<img id="packaging-upload" src="/images/packaging_upload_twine.png" alt="Python Packaging upload on PyPI via twine">
	<figcaption>Python packaging upload on PyPI via twine</figcaption>
</figure><br>

The way to upload your goodies on PyPI is called [twine][twine]. However, in order to be absolutely sure
that your package can be installed and run correctly without errors, the [testing PyPI server][PyPI_test] exists
to host (temporarily) packages and expose such errors (uploading, installation etc).

So, before you upload you package to the official live PyPI server (the default one), test it first and then
upload it *officially*. You'll need two different accounts; one for the testing and one for the default one.

Both uploads use the same command and it's pretty straightforward:

```bash
# for the testing PyPI server
twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# for the default PyPI server
twine upload dist/*
```

After each new version release of your package, it's a good idea to empty the `dist/` directory
from previous ones. Also delete the `build/` dir as well. As already been said above, the cookiecutter
has a command to help you with this, `make dist`.

Important note #1: PyPI does not allow to upload an artifact with the same version. That is, if your uploaded
package version is `0.1.0` and you discovered a minor bug (say a typo to a string, a minor one) and fix it
without change the version and try to upload it again, PyPI will complain with the following error:

```bash
Uploading booster-0.1.0-py2.py3-none-any.whl
100%|███████████████████████████████████████████████████████████████████████████████████| 8.94k/8.94k [00:01<00:00, 5.84kB/s]
HTTPError: 400 Client Error: File already exists. See https://test.pypi.org/help/#file-name-reuse for url: https://test.pypi.org/legacy/
```

Fix that by increment the patch version part to `0.1.1` and then upload it. Or wait for some feedback
from the users, gather some bugs and then update it. It depends on the scenario and how big these
bugs are.

Important note #2: Every time you change a version you should log it inside the `HISTORY.rst`
or the `CHANGELOG.rst` file (if you have it). That's a good practice not only for documentation
tracking purposes but also for the end users who need to know what has changed since the previous
version.


## [keyring](#keyring)

After running the above command(s), `twine` will ask your username and password. Instead of providing them
through the console each time, there is another way, the lazy one.

Under your virtualenv install [keyring][keyring] (once again, you're using a virtualenv, don't you?),
`pip install keyring`. Read the installation docs carefully because at some platforms, additional platform-specific
libraries might be needed. As it's docs say:

> `keyring` provides an easy way to access the system keyring service
from Python. It can be used in any application that needs safe password storage.

Before, `keyring`, the [recommended practice was to create a `.pypirc` file](https://docs.python.org/3/distutils/packageindex.html#the-pypirc-file)
under your home directory and inside there write in plain text the username and password for
each index (test and default).

Those days are gone and we may now be much more safe and cryptic.
Back to `keyring`, run the following two commands (one at a time):

```bash
keyring set https://test.pypi.org/legacy/ <your_testing_PyPI_username_here>
keyring set https://upload.pypi.org/legacy/ <your_default_PyPI_username_here>
```

Each command will prompt you for your password. Enter it and you're good to go.


## [Installing your uploaded package](#installing-your-uploaded-package)

Once the package has been uploaded to the testing server, you may install it from there,
in a new and clean virtualenv. Create your testing virtualenv and then:

```bash
pip install --index-url https://test.pypi.org/simple/ <package_name>
```

Confirm that installation produced no errors and that you can run your package
without any difficulties. In general, confirm that your package works as expected.

Once done, you may upload it to the default PyPI server and then simply use the
famous simple command:

```bash
pip install <package_name>
```

Congratulations! If you have made it so far that means you are in position to
share your ideas with others and make the world a better place to live!

Extra tip: Recall the keyword argument of the `setup` function, `extras_require`,
you may install additional packages/dependencies by just `pip install booster[test]`,
where `test` is a key of the dictionary.


# [Sum up](#sum-up)

If you're confused with all the above, which I admit, are a lot to learn (but easy ones)
in the first place, here are some advices in order to make your life easier:

1. Create a virtualenv.
2. Try to separate the concerns. First focus on your package and make sure it works. Forget about packaging.
3. Write documentation. No, docstrings are not enough! [We talked about it above](#docs-authorsrst-contributingrst-historyrst-and-readmerst).
4. Write tests. No more here to say. [We talked about it above](#tests-and-toxini).
5. Now it's time to think about wrapping your library to a package. Again, separation of concerns.
6. Using a cookiecutter of your choice, try to fill/edit/delete each file produced. One at a time.
7. Docs work with Sphinx? Tests pass? Package can be installed locally in developer mode? Works as expected?
8. Create the archives (wheel and sdist)
9. Upload first to testing PyPI and then to the default PyPI
10. Enjoy and tell others what you have built.

I am repeating myself here (against the [DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) discipline)
but it's for good:

> Do not rush. One step at a time. Complete each step and then go to the next.
Maybe you create your own *steps*, that's OK. But please try not to do things
simultaneously. The error lies in asynchronous human tasks. Be synchronous!

I am not saying that I succeeded the first time I try to build a Python package. I failed.
That's why I created this *kind of guide*. You may fail too. But do not give up.
Enough with the advices and lessons learned.

Now dive in and share your ideas with the Python community!


# [Resources](#resources)

## [Python packaging-related videos](#py_packaging_videos)

If you are a video-person then the following list contains (maybe all) english-spoken
video conferences, since 2012, related to Python packaging.
They are listed from recent to older without making older videos stale
(except those talking about the `distutils` package).
As a bonus, there is a small comment on each, by me, highlighting some points (if any) about the video.

- [What does PEP 517 mean for packaging](https://www.youtube.com/watch?v=s5lJsFzv_iI)
    - [Thomas Kluyver](https://github.com/takluyver)
	  - PyCon UK 2019 (Cardiff, UK)
      - A brief history on Python packaging. Talks about PEP 517, pyproject.toml and
	    distinguish between frontend and backend of packaging.<br><br>
- [Shipping your first Python package and automating future publishing](https://www.youtube.com/watch?v=P3dY3uDmnkU)
    - [Chris Wilcox](https://github.com/crwilcox)
	  - PyCon 2019 (Cleveland, Ohio)
	  - Not something new in comparison to other talks in the past.
	    Ends with the automation of package deployment which is quite handy!<br><br>
- [The Black Magic of Python Wheels](https://www.youtube.com/watch?v=02aAZ8u3wEQ)
    - [Elana Hashman](https://github.com/ehashman)
	  - PyCon 2019 (Cleveland, Ohio)
	  - Focuses on building extension wheels (ones that include C code, not only Python),
	    explains what [manylinux](https://github.com/pypa/manylinux), [auditwheel](https://github.com/pypa/auditwheel)
		and symbol version (C specific) are.<br><br>
- [Dependency hell: a library author's guide](https://www.youtube.com/watch?v=OaBhcueqNqw)
    - Yanhui Li & [Brian Quinlan](https://github.com/brianquinlan)
	  - PyCon 2019 (Cleveland, Ohio)
	  - Describes the problem of "dependecy hell" (diamond dependency) and recommends on using
	    semantic versioning ([semver](https://semver.org/))<br><br>
- [Packaging Django apps for distribution on PyPI](https://www.youtube.com/watch?v=RQrZRFcbYM0)
    - [Laura Hampton](https://github.com/lgh2)
	  - North Bay Python 2018 (Petaluma, California)
	  - Despite the Django-specific parts at the beginning,
	    not something new to learn in comparison with the other talks<br><br>
- [Can packaging improve Django deployments?](https://www.youtube.com/watch?v=Gt3Pkgsd0Tk)
    - [Markus Zapke-Gründemann](https://github.com/keimlink)
	  - DjangoCon Europe 2018 (Heidelberg, Germany)
	  - `pip-tools`, different Django project structure, `contraints.txt`, `setup.cfg`<br><br>
- [How to publish a package on PyPI](https://www.youtube.com/watch?v=QgZ7qv4Cd0Y)
    - [Mark Smith](https://github.com/judy2k)
    - PyCon Australia 2018
    - [gitignore.io](https://gitignore.io), [choosealicense.com][choosealicense],
      [check-manifest](https://github.com/mgedmin/check-manifest), [pipenv](https://github.com/pypa/pipenv)<br><br>
- [Inside the Cheeseshop: How Python Packaging Works](https://www.youtube.com/watch?v=AQsZsgJ30AE)
    - [Dustin Ingram](https://github.com/di)
    - PyCon 2018 (Cleveland, Ohio)
    - Focus on packaging history and not on how to package your Python code. Good references, though.<br><br>
- [Packaging Let’s Encrypt Lessons learned shipping Python code to hundreds of thousands of users](https://www.youtube.com/watch?v=WdhYa--Cahk)
    - [Noah Swartz](https://github.com/SwartzCr)
    - PyCon 2017 (Portland, Oregon)
    - Focuses on Python Applications ([certbot](https://certbot.eff.org/)) and problems encountered during
      development and production. Not a talk for Python libraries.<br><br>
- [Share your code! Python Packaging Without Complication](https://www.youtube.com/watch?v=qOH-h-EKKac)
    - [Dave Forgac](https://github.com/tylerdave)
    - PyCon 2017 (Portland, Oregon)
    - Not something new in comparison to the 2016 talks<br><br>
- [The trends in choosing licenses in Python ecosystem](https://www.youtube.com/watch?v=ikT2i4I2LYY)
    - [Anwesha Das](https://github.com/anweshadas)
    - PyCon 2017 (Portland, Oregon)
    - Learn about different types of licenses and best practices to license your project.<br><br>
- [Python Packaging - current state and overview](https://www.youtube.com/watch?v=xSbezLCJ87E)
    - [Jakub Wasielak](https://github.com/Gandi24)
    - EuroPython 2017 (Rimini, Italy)
    - Learn a lot about `setup.py` like [setuptools_scm](https://github.com/pypa/setuptools_scm), `extras_require`, `setup.cfg`
      `python setup.py install/develop`, [devpi.net](https://www.devpi.net/)
      and [PEP 440 -- Version Identification and Dependency Specification](https://www.python.org/dev/peps/pep-0440/)<br><br>
- [The Packaging Gradient](https://www.youtube.com/watch?v=iLVNWfPWAC8)
    - [Mahmoud Hashemi](https://github.com/mahmoud)
    - PyBay 2017 (San Francisco, California)
    - Focuses more on packaging Python applications instead of Python libraries. Refers to [pex][pex],
      [anaconda][anaconda], [freezers][py_freezer] and other methods.
      Obsolete, regarding the command for upload to PyPI (uses `setup.py upload`)<br><br>
- [Confessions of a Python packaging noo](https://www.youtube.com/watch?v=Ai2l9V2Y5Kw)
    - [Steven Saporta](https://github.com/ssaporta)
    - PyGotham 2017 (New York City)
    - Learn about the different wheel types<br><br>
- [Shipping Software To Users With Python](https://www.youtube.com/watch?v=5BqAeN-F9Qs)
    - [Glyph Lefkowitz](https://github.com/glyph)
    - PyCon 2016 (Portland, Oregon)
    - Talks more on distributing Python applications and not Python libraries.
      Learn about not to install globally using `sudo ` and instead use `pip install --user package`<br><br>
- [Publish your code so others can use it in 5 easy steps](https://www.youtube.com/watch?v=nFozViwDWvY)
    - [Marko Samastur](https://github.com/samastur)
    - PyCon 2016 (Portland, Oregon)
    - It's the same talk as of EuroPython 2016 so, more or less the same.<br><br>
- [Warehouse - the future of PyPI](https://www.youtube.com/watch?v=v_wFF2wEG_A)
    - [Nicole Harris](https://github.com/nlhkabu)
    - PyConFR 2016
    - Focuses more on the *old* PyPI and the birth of the new one (warehouse),
      learn about the [bus factor](https://en.wikipedia.org/wiki/Bus_factor), [PyPA][PyPA],
      [PyPUG](https://packaging.python.org/), [PSF Packaging WG](https://wiki.python.org/psf/PackagingWG)<br><br>
- [Publish your code so others can use it in 4 easy steps](https://www.youtube.com/watch?v=gc9dkktg1gU)
    - [Marko Samastur](https://github.com/samastur)
    - EuroPython 2016 (Bilbao, Spain)
    - It's kind of stale (uses `setup.py sdist upload` instead of [twine][twine])<br><br>
- [What Python can learn from Haskell packaging](https://www.youtube.com/watch?v=osCJgs5UetU)
    - [Domen Kožar](https://github.com/domenkozar)
    - EuroPython 2016 (Bilbao, Spain)
    - Talks about Haskell with a few referrals to Python<br><br>
- [Reinventing the `whl`: New Developments in Upstream Python Packaging Ecosystem](https://www.youtube.com/watch?v=oE5iePv8nD8)
    - [Nathaniel Smith](https://github.com/njsmith/)
    - SciPy 2016 (Austin, Texas)
    - Speaks about packaging Python applications, mostly, not Python libraries.
      Talks about the [pip install --pre <package>](https://pip.pypa.io/en/stable/reference/pip_install/#cmdoption-pre)
      and the upcoming `pyproject.toml` configuration file.<br><br>
- [Rethinking packaging, development and deployment](https://www.youtube.com/watch?v=W8A2bOKPtJU)
    - [Domen Kožar](https://github.com/domenkozar)
    - PyCon 2015 (Montréal, Canada)
    - Talks about the [nix](https://nixos.org/nixpkgs/manual/#python) project<br><br>
- [Grug make fire! Grug make wheel!](https://www.youtube.com/watch?v=UtFHIpNPMPA)
    - [Russell Keith-Magee](https://github.com/freakboy3742)
    - PyCon Australia 2014
    - A little stale but you may learn about `setup.cfg`, `MANIFEST` and  `LICENCE`<br><br>
- [Python packaging simplified, for end users, app developers](https://www.youtube.com/watch?v=eLPiPHr6TVI)
    - [Asheesh Laroia](https://github.com/paulproteus)
    - PyCon 2014 (Montréal, Canada)
    - A bit of stale too, but you learn that `pip install -e .` is the alias
      of `python setup.py develop`<br><br>
- [What is coming in Python packaging](https://www.youtube.com/watch?v=jOiAp3wtx18)
    - [Noah Kantrowitz](https://github.com/coderanger)
    - PyCon 2014 (Montréal, Canada)
    - Learn about the [warehouse JSON API](https://warehouse.pypa.io/api-reference/json/),
      [ensurepip](https://docs.python.org/3/library/ensurepip.html),
      [PEP 453 -- Explicit bootstrapping of pip in Python installations](https://www.python.org/dev/peps/pep-0453/)
      and `wheel`s<br><br>
- [Nobody Expects the Python Packaging Authority](https://www.youtube.com/watch?v=8Xrdt3-YVz4)
    - [Nick Coghlan](https://github.com/ncoghlan)
    - PyCon Australia 2013
    - Talks about the pre-PyPA era and packaging issues that prevent Python packaging from evolving.
      Great talk for historical reasons.<br><br>
- [Sharing is Caring: Posting to the Python Package Index](https://www.youtube.com/watch?v=bwwf_HbEJQM)
    - [Luke Sneeringer](https://github.com/lukesneeringer)
    - PyConUS 2012 (Santa Clara, California)
    - Very good video but a bit of stale since he uses `distutils`


## [Python packaging-related podcasts](#py_packaging_podcasts)

If you want to put on your headphones and enjoy the listening about Python
packaging, then this list is for you:

- [52: pyproject.toml : the future of Python packaging](https://testandcode.com/52)
    - [Brett Cannon](https://github.com/brettcannon)
    - 5 November 2018<br><br>


## [Python packaging-related articles](#py_packaging_articles)

Searching for "python packaging" will give you a ton of results. I tried to minimize
this list of results and end up with the following articles. They are in chronological
order. This does not mean that older posts are obsolete.

- [Python's new package landscape](http://andrewsforge.com/article/python-new-package-landscape/)
    - [Andrew Pinkham](https://github.com/jambonrose)
    - 11 May 2018<br><br>
- [A tutorial on packaging up your Python code for PyPI](https://snarky.ca/a-tutorial-on-python-package-building/)
    - [Brett Cannon](https://github.com/brettcannon)
    - 28 October 2017<br><br>
- [Sharing your labor of love: PyPI quick and dirty](https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/)
    - [Hynek Schlawack](https://github.com/hynek)
    - 29 July 2013 (updated on 23 October 2017)<br><br>
- [Alice in Python projectland](https://veekaybee.github.io/2017/09/26/python-packaging/)
    - [Vicki Boykis](https://github.com/veekaybee)
    - 26 September 2017<br><br>
- [Publish your Python packages easily using flit](http://brunorocha.org/python/publish-your-python-packages-easily-using-flit.html)
    - [Bruno Rocha](https://github.com/rochacbruno)
    - 22 August 2017<br><br>
- [Conda: Myths and misconceptions](https://jakevdp.github.io/blog/2016/08/25/conda-myths-and-misconceptions/)
    - [Jake VanderPlas](https://github.com/jakevdp)
    - 25 Aug 2016<br><br>
- [Python packaging is good now](https://glyph.twistedmatrix.com/2016/08/python-packaging.html)
    - [Glyph Lefkowitz](https://github.com/glyph)
    - 14 August 2016<br><br>
- [Testing & Packaging](https://hynek.me/articles/testing-packaging/)
    - [Hynek Schlawack](https://github.com/hynek)
    - 19 October 2015<br><br>
- [Python packaging pitfalls](https://blog.ionelmc.ro/2014/06/25/python-packaging-pitfalls/)
    - [Ionel Cristian Mărieș](https://github.com/ionelmc)
    - 25 June 2014<br><br>
- [The package dependency blues](https://blog.miguelgrinberg.com/post/the-package-dependency-blues)
    - [Miguel Grinberg](https://github.com/miguelgrinberg)
    - 2 Sep 2013<br><br>
- [setup.py vs requirements.txt](https://caremad.io/posts/2013/07/setup-vs-requirement/)
    - [Donald Stuff](https://github.com/dstufft)
    - 22 Jul 2013<br><br>
- [Incremental plans to improve Python packaging](http://python-notes.curiousefficiency.org/en/latest/pep_ideas/core_packaging_api.html)
    - [Nick Coghlan](https://github.com/ncoghlan)<br><br>
- [6 things I learned about setuptools](https://justin.abrah.ms/python/setuptools_lessons.html)
    - [Justin Abrahms](https://github.com/justinabrahms)<br><br>
- [PyPA tutorials](https://packaging.python.org/tutorials/)
- [PyPA guides](https://packaging.python.org/guides/)
- [setuptools official docs](https://setuptools.readthedocs.io/en/latest/)


[anaconda]: https://www.anaconda.com/
[bump2version]: https://github.com/c4urself/bump2version
[check-manifest]: https://github.com/mgedmin/check-manifest
[choosealicense]: https://choosealicense.com
[click]: https://click.palletsprojects.com/en/master/
[keyring]: https://pypi.org/project/keyring/
[nose]: https://nose.readthedocs.io/en/latest/
[pep_427]: https://www.python.org/dev/peps/pep-0427/
[pep_491]: https://www.python.org/dev/peps/pep-0491/
[pex]: https://github.com/pantsbuild/pex
[pip]: https://pypi.org/project/pip/
[pip_prefers_whl]: https://pip.pypa.io/en/stable/user_guide/#installing-from-wheels
[poetry]: https://pypi.org/project/poetry/
[pytest]: https://docs.pytest.org/en/latest/
[py_freezer]: https://docs.python-guide.org/shipping/freezing/
[readthedocs]: https://readthedocs.org/
[requirements_vs_install_requires]: https://packaging.python.org/discussions/install-requires-vs-requirements/?highlight=requirements#requirements-files
[setuptools]: https://pypi.org/project/setuptools/
[sphinx]: http://www.sphinx-doc.org/en/master/
[tox]: https://tox.readthedocs.io/en/latest/
[twine]: https://pypi.org/project/twine/
[unittest]: https://docs.python.org/3/library/unittest.html
[virtualenv]: https://virtualenv.pypa.io/en/latest/
[wheel]: https://pypi.org/project/wheel/
[wheel_sdist_diff]: https://packaging.python.org/tutorials/installing-packages/#source-distributions-vs-wheels
[PyPA]: https://www.pypa.io/en/latest/
[PyPI]: https://pypi.org/
[PyPI_test]: https://test.pypi.org/
