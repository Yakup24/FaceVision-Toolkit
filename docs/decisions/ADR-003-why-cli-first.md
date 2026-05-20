# ADR-003: Keep the Project CLI-First

## Status

Accepted

## Context

The project should be easy to run from a terminal, over SSH and in CI-style smoke tests.

## Decision

Keep the primary interface as a CLI and use OpenCV windows only for interactive local runs.

## Consequences

The CLI is simple and portable, but it is less friendly than a full desktop GUI. A GUI remains a roadmap item.
