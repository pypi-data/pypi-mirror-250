# Changelog

## v0.3.0 (2024-01-09)

#### New Features

* add close method
#### Refactorings

* change `return Log(` statements to `return self.__class__(` to appease the type checker


## v0.2.0 (2023-11-07)

#### New Features

* add functions for getting logpaths and loading Log objects from a logging.Logger instance
#### Performance improvements

* don't set handler formatter until after checking if the handler needs to be added
#### Refactorings

* import Log and Event from models

## v0.1.1 (2023-10-31)

#### Refactorings

* make logpath if it doesn't exist

## v0.1.0 (2023-10-29)

#### New Features

* add support for slicing Log objects and getting their event lengths
#### Fixes

* prevent duplicate log messages


