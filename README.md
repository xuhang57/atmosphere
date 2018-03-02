# atmosphere :cloud:

[![Build Status](https://travis-ci.org/CCI-MOC/giji-backend.svg?branch=giji-v29-changes)](https://travis-ci.org/CCI-MOC/giji-backend)
[![Coverage Status](https://coveralls.io/repos/github/CCI-MOC/giji-backend/badge.svg)](https://coveralls.io/github/CCI-MOC/giji-backend)
[![Code Health](https://landscape.io/github/CCI-MOC/giji-backend/giji-v29-changes/landscape.svg?style=flat)](https://landscape.io/github/CCI-MOC/giji-backend/giji-v29-changes)


Atmosphere addresses the growing needs for highly configurable and customized computational resources to support research efforts in plant sciences. Atmosphere is an integrative, private, self-service cloud computing platform designed to provide easy access to preconfigured, frequently used analysis routines, relevant algorithms, and data sets in an available-on-demand environment designed to accommodate computationally and data-intensive bioinformatics tasks.

## Installation

Install the required python packages
```
pip install -r requirements.txt
```

A separate environment is provided for developers
```
pip install -r dev_requirements.txt
```

The `*requirements.txt` files are generated using
[pip-tools](https://github.com/jazzband/pip-tools). See
[REQUIREMENTS.md](REQUIREMENTS.md) for instructions on using pip-tools and
upgrading packages in Atmosphere.

## Some Features

+ A powerful web client for management and administration of virtual machines
+ A fully RESTful API service for integrating with existing infrastructure components
+ Virtual machine images preconfigured for computational science and iPlant's infrastructure

## Running scripts

There are several utility scripts in `./scripts`. To run these:
```
cd <path to atmosphere>
export DJANGO_SETTINGS_MODULE='atmosphere.settings'
export PYTHONPATH="$PWD:$PYTHONPATH"
python scripts/<name of script>
```

## Contributing

See [HACKING.md](./HACKING.md).

### Coding Style
- Use 4 space indentation
- Limit lines to 79 characters
- Remove unused imports
- Remove trailing whitespace
- See [PEP8 - Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)

It is recommended that you use the git `pre-commit` hook to ensure your code
is compliant with our style guide.

```bash
ln -s $(pwd)/contrib/pre-commit.hook $(pwd)/.git/hooks/pre-commit
```

To automate running tests before a push use the git `pre-push` hook to ensure
your code passes all the tests.

```bash
ln -s $(pwd)/contrib/pre-push.hook $(pwd).git/hooks/pre-push
```

When master is pulled, it's helpful to know if a `pip install` or a `manage.py
migrate` is necessary. To get other helpful warnings:
```bash
ln -s $(pwd)/contrib/post-merge.hook $(pwd)/.git/hooks/post-merge
```

### Coding Conventions

#### Import ordering
Imports should be grouped into the sections below and in sorted order.

1. Standard libraries
2. Third-party libraries
3. External project libraries
4. Local libraries

## License

See LICENSE.txt for license information

## Lead

+ **Edwin Skidmore <edwin@cyverse.org>**

## Authors

The following individuals who have help/helped make :cloud: great appear in alphabetic order, by surname.

+ **Evan Briones <cloud-alum@cyverse.org>**
+ **Tharon Carlson <tharon@cyverse.org>**
+ **Joseph Garcia <cloud-alum@cyverse.org>**
+ **Steven Gregory <sgregory@cyverse.org>**
+ **Jason Hansen <cloud-alum@cyverse.org>**
+ **Christopher James LaRose <cloud-alum@cyverse.org>**
+ **Amit Juneja <cloud-alum@cyverse.org>**
+ **Andrew Lenards <lenards@cyverse.org>**
+ **Monica Lent <cloud-alum@cyverse.org>**
+ **Chris Martin <cmart@cyverse.org>**
+ **Calvin Mclean <calvinmclean@cyverse.org>**
+ **Andre Mercer <cloud-alum@cyverse.org>**
+ **Connor Osborn <connor@cyverse.org>**
+ **J. Matt Peterson <cloud-alum@cyverse.org>**
+ **Julian Pistorius <julianp@cyverse.org>**

#### GIJI Authors
+ **Xu H. Lucas <xuh@massopen.cloud>**

Where the cloud lives!
