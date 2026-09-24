# doc/adr — architecture decisions

One file per decision, in Michael Nygard's format (the one `adr-tools` implements).
Name them `NNNN-short-title.md`. Numbers run in sequence and are never reused. A new
ADR starts from `0000-template.md`.

**The threshold against `DECISIONS.md`.** A three-line "why" goes in `DECISIONS.md`.
A decision whose consequences outlive the people who made it, and that later work will
have to reference, goes here. If every decision you have made still fits in three
lines, you can delete this directory and lose nothing — but delete the two pointers to
it as well, in `CLAUDE.md` ("Where things live") and at the end of `DECISIONS.md`'s
format section. A pointer to a directory that is not there costs context in every
session.

**The status changes; the text does not.** A reversed decision is not edited and not
deleted. It gets `Status: Superseded by ADR-NNNN`, and the new decision is written as
its own file. The record of what you once believed was right is the value of this
directory.

`0001-record-architecture-decisions.md` is the first entry, already written: deciding
to keep ADRs is itself a decision, and this is the one ADR a template can fill in
honestly. Put today's date on it when you adopt the scaffold.

**How strong the evidence is, stated plainly.** ADRs are a documented and widely used
practice *for human teams* (Michael Nygard, 2011; `adr-tools` is the reference command
set). There is no controlled measurement showing that ADRs improve a coding agent's
results. Keeping them here is a judgement call carried over from human practice, not a
conclusion drawn from data. [Unverified — these three statements come from a source
review done outside this repository and were not re-checked here; the third is a claim
of absence, which reading one page cannot establish either way.]
