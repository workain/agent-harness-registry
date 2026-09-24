---
paths:
  - "tests/**"
  - "**/*.test.*"
  - "**/*.spec.*"
---

# Rules for tests

Loaded only when a file matching one of the globs above is read. In a session that
touches no test file it costs nothing — which is why it is a separate file rather than
another section of `CLAUDE.md`.

- Tests do not reach the network. External calls are intercepted; a new test that makes
  one has to intercept it the same way.
- A test that "fails sometimes" is fixed or deleted, never re-run until it passes. A
  re-run that turns red into green has measured nothing.
- A new test is proven by making it fail on purpose once, before it is committed. A test
  that cannot fail is not evidence, and it will be believed anyway.
- Assert on the behaviour, not on the implementation: a test that breaks on every
  refactor gets deleted by the next person in a hurry.

<!-- Replace the contents with what is true for THIS project's tests — fixtures,
     isolation, what counts as flaky, what is forbidden in a test. If the project has no
     test-specific conventions yet, delete this file AND the line pointing at it in
     CLAUDE.md's "Where things live"; they go together or not at all.

     A note on the globs: an invalid pattern (an unescaped `[`, say) matches nothing and
     this rule then silently never loads — no error, no warning. The rule's other
     patterns keep working. Confirm a rule actually loaded with `/context`, not by
     seeing the file on disk. Per Claude Code's memory documentation (fetched
     2026-09-24), a path-scoped rule triggers when a matching file is read; after
     `/compact` the project-root CLAUDE.md is re-read from disk automatically, while
     this file reloads only when a matching file is opened again. That asymmetry is why
     CLAUDE.md keeps a one-line pointer to this file even though the glob works on its
     own. -->
