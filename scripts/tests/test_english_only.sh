#!/usr/bin/env bash
# Demonstrates that pre-commit check 3 (English-only) fires in BOTH directions, and that
# every path on which it cannot check exits loudly rather than printing a clean result.
#
#   bash scripts/tests/test_english_only.sh
#
# Why this file exists: the root CLAUDE.md's LANGUAGE rule was prose with nothing behind it
# for long enough that an entire template shipped in Russian under it. A gate whose failure
# mode is silent is not proven until it has been made to fail loudly against a real case —
# so assertion 7 below runs the check against the actual pre-rework template file, taken out
# of this repository's own history, rather than against a fixture written to be caught.

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CHECKS="$REPO_ROOT/scripts/pre-commit-checks.sh"
PASS=0; FAIL=0

pass() { printf '  PASS  %s\n' "$1"; PASS=$((PASS + 1)); }
fail() { printf '  FAIL  %s\n' "$1"; FAIL=$((FAIL + 1)); }

# assert_contains <label> <haystack> <needle>  -- and note that an EMPTY haystack fails,
# rather than vacuously passing the way an assert-NOT-contains would.
assert_contains() {
    local label="$1" hay="$2" needle="$3"
    if [ -z "$hay" ]; then fail "$label (no output at all — the check never ran)"; return; fi
    case "$hay" in *"$needle"*) pass "$label" ;; *) fail "$label — expected '$needle' in:
$hay" ;; esac
}

assert_absent() {
    local label="$1" hay="$2" needle="$3"
    if [ -z "$hay" ]; then fail "$label (no output at all — nothing was asserted)"; return; fi
    case "$hay" in *"$needle"*) fail "$label — '$needle' should NOT appear in:
$hay" ;; *) pass "$label" ;; esac
}

# Build a throwaway repo on a feature branch (check 1 blocks commits on main) with $1 staged.
new_repo() {
    local dir; dir="$(mktemp -d)"
    git -C "$dir" init -q -b main
    git -C "$dir" -c user.email=t@t -c user.name=t commit -q --allow-empty -m base
    git -C "$dir" switch -q -c feature
    printf '%s' "$dir"
}

run_checks() { ( cd "$1" && bash "$CHECKS" 2>&1 ); }

echo "English-only pre-commit check — demonstration"
echo

# --- 1. Clean English file: the check passes and says so ---
D="$(new_repo)"; printf 'A plain English line.\n' > "$D/clean.md"; git -C "$D" add clean.md
OUT="$(run_checks "$D")"; RC=$?
assert_contains "clean English file: check reports OK" "$OUT" "English-only (no Cyrillic)... "
[ "$RC" -eq 0 ] && pass "clean English file: exit 0" || fail "clean English file: exit $RC, expected 0"
assert_absent "clean English file: not reported as a failure" "$OUT" "Cyrillic text in staged files"
rm -rf "$D"

# --- 2. Cyrillic in a staged file: BLOCKED ---
D="$(new_repo)"
printf 'Line one.\nЭто русский текст.\n' > "$D/dirty.md"; git -C "$D" add dirty.md
OUT="$(run_checks "$D")"; RC=$?
assert_contains "Cyrillic staged: check fails" "$OUT" "Cyrillic text in staged files"
assert_contains "Cyrillic staged: names the file and line" "$OUT" "dirty.md:2:"
assert_contains "Cyrillic staged: commit blocked" "$OUT" "Commit blocked"
[ "$RC" -eq 1 ] && pass "Cyrillic staged: exit 1" || fail "Cyrillic staged: exit $RC, expected 1"
rm -rf "$D"

# --- 3. Latin non-ASCII (em dash, typographic quotes, accents) must NOT trip it ---
D="$(new_repo)"
printf 'A sentence — with an em dash, “smart quotes” and a café.\n' > "$D/latin.md"
git -C "$D" add latin.md
OUT="$(run_checks "$D")"; RC=$?
assert_absent "Latin non-ASCII: no false positive" "$OUT" "Cyrillic text in staged files"
[ "$RC" -eq 0 ] && pass "Latin non-ASCII: exit 0" || fail "Latin non-ASCII: exit $RC, expected 0"
rm -rf "$D"

# --- 4. Override: proceeds, but says so and echoes the reason ---
D="$(new_repo)"; printf 'Цитата оператора.\n' > "$D/quote.md"; git -C "$D" add quote.md
OUT="$( cd "$D" && AHR_ALLOW_NON_ENGLISH=1 AHR_NON_ENGLISH_REASON='verbatim operator quote' bash "$CHECKS" 2>&1 )"; RC=$?
assert_contains "override: reported, not silent" "$OUT" "OVERRIDE"
assert_contains "override: reason echoed" "$OUT" "verbatim operator quote"
[ "$RC" -eq 0 ] && pass "override: exit 0" || fail "override: exit $RC, expected 0"
rm -rf "$D"

# --- 5. python3 missing: fails CLOSED and loudly, never a clean-looking OK ---
D="$(new_repo)"; printf 'Fine.\n' > "$D/x.md"; git -C "$D" add x.md
SHIM="$(mktemp -d)"   # a PATH with git but no python3
for tool in git grep sed sort uniq cat printf bash env date; do
    W="$(command -v "$tool" 2>/dev/null)" && ln -sf "$W" "$SHIM/$tool"
done
OUT="$( cd "$D" && PATH="$SHIM" bash "$CHECKS" 2>&1 )"; RC=$?
assert_contains "no python3: says it could not check" "$OUT" "CHECK-UNAVAILABLE"
assert_absent "no python3: does not print a clean OK for this check" "$OUT" "English-only (no Cyrillic)... [0;32mOK"
[ "$RC" -eq 1 ] && pass "no python3: exit 1 (fails closed)" || fail "no python3: exit $RC, expected 1"
rm -rf "$D" "$SHIM"

# --- 6. Binary staged file: skipped without crashing the gate ---
D="$(new_repo)"
printf '\x89PNG\r\n\x1a\n\xd0\x9f\xd1\x80\x00\x01\x02' > "$D/img.png"; git -C "$D" add img.png
OUT="$(run_checks "$D")"; RC=$?
assert_contains "binary file: gate still completed" "$OUT" "English-only (no Cyrillic)... "
[ "$RC" -eq 0 ] && pass "binary file: exit 0" || fail "binary file: exit $RC, expected 0"
rm -rf "$D"

# --- 7. THE REAL CASE: the template file as it actually shipped, from this repo's history ---
# Not a fixture written to be caught — the bytes that were live on main and that this gate
# exists because of. If this assertion ever goes quiet because the blob is unreachable, it
# reports that instead of passing.
REAL_BLOB="a73a330:templates/coding-agent-starter/CLAUDE.md"
if git -C "$REPO_ROOT" cat-file -e "$REAL_BLOB" 2>/dev/null; then
    D="$(new_repo)"
    git -C "$REPO_ROOT" show "$REAL_BLOB" > "$D/CLAUDE.md"
    git -C "$D" add CLAUDE.md
    OUT="$(run_checks "$D")"; RC=$?
    assert_contains "real shipped template (a73a330): blocked" "$OUT" "Cyrillic text in staged files"
    [ "$RC" -eq 1 ] && pass "real shipped template: exit 1" || fail "real shipped template: exit $RC, expected 1"
    rm -rf "$D"
else
    fail "real shipped template: blob $REAL_BLOB unreachable — this assertion did not run"
fi

echo
echo "  $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] || exit 1
