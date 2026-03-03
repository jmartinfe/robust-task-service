# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-02-15

### Added
- Initial task lifecycle support (create, list, retrieve, complete, delete)
- SQLAlchemy persistence layer
- Domain exception: TaskNotFoundException
- Domain exception: TaskAlreadyCompletedException
- Global exception handlers

## [0.2.0] - 2026-03-03

### Added
- Refactor of task complete boolean field to a status enum field (created, in_progress, on_hold, complete)
- Logging relevant service operations and exception occurrences
- Task service tests
- Alembic migration tool integrated
- API health check and db readiness