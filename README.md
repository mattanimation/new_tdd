# New TDD
kind of like the new internet...

A different approach to unit tests where the developer just runs a script that crawls their code,
and uses a config file that holds the actual test data in it.

**Note!**
EARLY STAGES, don't use this yet! _unless you really want to_.

## Supported Languages
* python 3

## Roadmap
* go
* c++

## Setup
`mkvirtualenv new_tdd -p==python3`
`pip install pyaml`

## Development
activate env: `workon new_ttd`
when done: `deactivate`

## approach
make a config file in json or yaml that has a set of examples that consist of:
* function name
* args
* assertion result given those args

the script for that language would be assuming its in the root of your code base.
It will open / import all methods from all modules then look for them in the config
and test the functions using the arguments therein.

## Example
```
$ cd /python
$ python tdd.py
```
this will look at the _derp_ folder and it's modules inside for testing

look at the `test_config.json` file as an example

## Issues
* doesn't work with module that have `__init__.py` yet


**Note** - yaml not yet fully implemented