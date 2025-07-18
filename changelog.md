# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.5] - 7/13/2025

### Changed

* Laying more groundwork for LVGL integration.
* Fixing bugs in the `logging` API.
    * Note: This API is no-longer 1:1 to Micropython's Standard Library.
* Fixing lockup issues in the `picocalc.wifi` module.
* Adding Third-Party libraries to `./libs`
    * `datetime` - `micropython-lib`
    * `ustrftime` - From https://github.com/iyassou/ustrftime/blob/main/ustrftime.py

## [0.0.4] - 7/12/2025

### Added

* Adding LICENSE file.

## [0.0.3] - 7/12/2025

### Changed

- Breaking up Micropython setup to separate Markdown file.
- Adding notes on Wifi setup.

## [0.0.2] - 7/12/2025

### Changed

- Added Documentation for startup script
- Adding Wifi manager


## [0.0.1] - Pre 7/12/2025

### Added

- First update with changelog
- README has instructions on compiling Micropython
- Scripts have instructions on running local mp and building micropython

