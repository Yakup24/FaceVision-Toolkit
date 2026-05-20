# ADR-001: Use OpenCV

## Status

Accepted

## Context

The project needs camera capture, classic face/eye detection, drawing utilities and a broad local development ecosystem.

## Decision

Use OpenCV as the core computer vision dependency.

## Consequences

OpenCV keeps the project compact and portable, but backend behavior can vary by OS, camera driver and installation method.
