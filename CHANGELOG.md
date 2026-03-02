# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-02-15

### Added
- Initial task lifecycle support (create, list, retrieve, complete, delete)
- SQLAlchemy persistence layer
- Domain exception: TaskNotFoundException
- Domain exception: TaskAlreadyCompletedException
- Global exception handlers