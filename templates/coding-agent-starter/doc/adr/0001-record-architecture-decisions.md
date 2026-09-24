# 1. Record architecture decisions

Date: <YYYY-MM-DD>

## Status

Accepted

## Context

This project is worked on by a coding agent whose memory ends with the session, and by
people whose memory of a reason fades faster than the code that encodes it. `git log`
records what changed and `DECISIONS.md` records short reasons, but neither survives as
a reference: a three-line entry in an append-only log is hard to point at six months
later, and a decision that later work must be consistent with needs an address.

## Decision

We will record decisions with long-lived consequences as ADRs — one file per decision,
in Michael Nygard's format, in `doc/adr/`, numbered in sequence. Short reasons stay in
`DECISIONS.md`. The threshold between them: whether the entry still fits in three
lines.

## Consequences

Each such decision costs its own file and a moment spent deciding which of the two
places it belongs in — real discipline, and some decisions will not be worth it; those
stay in `DECISIONS.md`.

In exchange, "why is it like this" gets an address that can be linked and cited. A
reversed decision is never edited: its `Status` becomes `Superseded by ADR-NNNN` and
the replacement is written as a new file, so the history of what was once believed
correct stays readable.
