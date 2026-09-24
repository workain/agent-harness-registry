#!/usr/bin/env bash
# Pre-commit checks for this repository.
#
# Install (per-checkout — hooks are NOT committed/auto-installed by git):
#   cp scripts/pre-commit-checks.sh .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
#
# Governance gate ported from the PMO workain/agent-lab-manager's own pre-commit-checks.sh,
# trimmed to the checks that apply to a direction/execution repo (dropped: the manager-specific
# citation / research dual-output / best-practice / audit-issue-ref / lessons gates, which are
# tied to its knowledge-base machinery and do not belong here). A mechanical gate is preferred
# over relying on a session remembering the convention (manager CLAUDE.md §3.5-style).
#
# Checks:
# 1. BLOCK direct commit to `main` (branch + PR, always — including docs and one-liners).
# 2. Secret scan on staged files (block obvious key patterns / .env-style credential exports).
# 3. BLOCK non-English (Cyrillic) text in staged files — the mechanical half of the root
#    CLAUDE.md's LANGUAGE rule, which until now was prose only and was broken by a whole
#    shipped template. Override with AHR_ALLOW_NON_ENGLISH=1 plus AHR_NON_ENGLISH_REASON=...
#    (echoed, never silent) when a verbatim non-English quote is genuinely the artifact.
# 9. WARN if a commit introduces/touches a Tasks/<slug>/ folder with no log.md inside it
#    (running-log convention — see agent-lab-manager's blueprint/conventions.md). Numbered "9"
#    to match the upstream script's numbering across repos, not because checks 3-8 exist here.

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

ERRORS=0

echo "Running pre-commit checks..."

# --- 1. Block direct commit to main ---
echo -n "  Branch guard (no commit to main)... "
BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo '')"
if [ "$BRANCH" = "main" ]; then
    echo -e "${RED}FAIL${NC}"
    echo -e "    ${RED}Direct commits to 'main' are forbidden (branch + PR, always).${NC}"
    echo -e "    ${RED}Create a feature branch first, e.g.:${NC}"
    echo -e "    ${RED}  git switch -c issue-NNN-short-description${NC}"
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}OK${NC} (on '$BRANCH')"
fi

# --- 2. Secret scan ---
echo -n "  Secret scan... "
STAGED_ALL="$(git diff --cached --name-only --diff-filter=ACM || true)"
SECRET_FAIL=0
for f in $STAGED_ALL; do
    case "$f" in
        *.json|*.html|*.png|*.jpg|*.jpeg|*.gif|*.pdf|*.lock) continue ;;
    esac
    [ -f "$f" ] || continue
    if grep -qiE '(api[_-]?key|api[_-]?secret|secret[_-]?key|private[_-]?key|password|passwd|token)[[:space:]]*[:=][[:space:]]*["\x27][A-Za-z0-9+/_-]{16,}' "$f" 2>/dev/null; then
        echo -e "${RED}FAIL${NC}: possible secret in $f"
        SECRET_FAIL=1
        ERRORS=$((ERRORS + 1))
    fi
    if grep -qiE '^[[:space:]]*(export[[:space:]]+)?(AWS_SECRET_ACCESS_KEY|AWS_ACCESS_KEY_ID|GITHUB_TOKEN|GH_TOKEN|OPENAI_API_KEY|ANTHROPIC_API_KEY)[[:space:]]*=[[:space:]]*["\x27]?[A-Za-z0-9+/_-]{16,}' "$f" 2>/dev/null; then
        echo -e "${RED}FAIL${NC}: possible credential env assignment in $f"
        SECRET_FAIL=1
        ERRORS=$((ERRORS + 1))
    fi
done
[ "$SECRET_FAIL" -eq 0 ] && echo -e "${GREEN}OK${NC}"

# --- 3. English-only (block Cyrillic in staged text) ---
# The root CLAUDE.md binds every technical artifact in this repository to English. That rule
# was prose with nothing behind it, and a complete template shipped in Russian under it. This
# is its mechanical half. Cyrillic is what this repository actually drifts into; a general
# "non-ASCII" check would reject the em dashes and typographic quotes the prose already uses
# everywhere, so the detector names the script it is guarding against rather than pretending
# to a generality it does not have.
echo -n "  English-only (no Cyrillic)... "
if ! command -v python3 >/dev/null 2>&1; then
    # Fail CLOSED and loudly. A language check that cannot run must not print OK: "checked,
    # found nothing" and "could not check" are the same output otherwise, and the second one
    # is how a gate quietly stops gating.
    echo -e "${RED}FAIL${NC}"
    echo -e "    ${RED}CHECK-UNAVAILABLE: python3 not found, so staged text could not be scanned.${NC}"
    echo -e "    ${RED}Install python3, or set AHR_ALLOW_NON_ENGLISH=1 AHR_NON_ENGLISH_REASON='...' to proceed.${NC}"
    if [ "${AHR_ALLOW_NON_ENGLISH:-0}" = "1" ]; then
        echo -e "    ${YELLOW}OVERRIDE accepted: ${AHR_NON_ENGLISH_REASON:-<no reason given>}${NC}"
    else
        ERRORS=$((ERRORS + 1))
    fi
else
    CYR_HITS=""
    for f in $(git diff --cached --name-only --diff-filter=ACM || true); do
        case "$f" in
            *.png|*.jpg|*.jpeg|*.gif|*.pdf|*.ico|*.woff|*.woff2|*.zip) continue ;;
            # Exactly two exemptions, by full path, and they are the detector itself and the
            # suite that proves it fires. Both must contain Cyrillic to do their job — the
            # character range in the regex below, and the fixtures the test blocks on — so
            # without this the gate refuses every commit that edits the gate, and the override
            # becomes the routine way to touch it. Named paths, not a scripts/ prefix: a
            # directory-wide exemption would silently cover the next script written there.
            scripts/pre-commit-checks.sh|scripts/tests/test_english_only.sh) continue ;;
        esac
        [ -f "$f" ] || continue
        HIT="$(python3 - "$f" <<'PYEOF'
import re, sys
path = sys.argv[1]
try:
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            if re.search(r"[Ѐ-ӿ]", line):
                print(f"{n}: {line.strip()[:70]}")
                break
except (UnicodeDecodeError, OSError):
    pass          # binary or unreadable: nothing to say about its language
PYEOF
)" || { echo -e "${RED}FAIL${NC}"; echo -e "    ${RED}CHECK-ERROR: the scanner raised on $f; treating as unchecked.${NC}"; ERRORS=$((ERRORS + 1)); CYR_HITS="__error__"; break; }
        if [ -n "$HIT" ]; then
            CYR_HITS="$CYR_HITS
      $f:$HIT"
        fi
    done
    if [ "$CYR_HITS" = "__error__" ]; then
        :
    elif [ -z "$CYR_HITS" ]; then
        echo -e "${GREEN}OK${NC}"
    elif [ "${AHR_ALLOW_NON_ENGLISH:-0}" = "1" ]; then
        echo -e "${YELLOW}OVERRIDE${NC}"
        echo -e "    ${YELLOW}Cyrillic found, allowed by AHR_ALLOW_NON_ENGLISH=1:${CYR_HITS}${NC}"
        echo -e "    ${YELLOW}Reason: ${AHR_NON_ENGLISH_REASON:-<no reason given>}${NC}"
    else
        echo -e "${RED}FAIL${NC}"
        echo -e "    ${RED}Cyrillic text in staged files (root CLAUDE.md: artifacts are English):${CYR_HITS}${NC}"
        echo -e "    ${RED}Translate it, or set AHR_ALLOW_NON_ENGLISH=1 AHR_NON_ENGLISH_REASON='why this quote must stay verbatim'.${NC}"
        ERRORS=$((ERRORS + 1))
    fi
fi

# --- 9. Running-log WARN (ported from agent-lab-manager's blueprint/conventions.md) ---
# Any commit touching a Tasks/<slug>/ path with no log.md present gets flagged. WARN, not
# hard-block — Small tasks legitimately may not need one. Checks EVERY commit that touches a
# Tasks/<slug>/ path, not just a slug's first-ever commit (the upstream script's own round-2 fix
# for a real bug: a first-commit-only check goes silently clean on every subsequent commit).
TOUCHED_TASK_SLUGS="$(git diff --cached --name-only --diff-filter=ACM | grep -E '^Tasks/[^/]+/' | sed -E 's#^(Tasks/[^/]+)/.*#\1#' | sort -u || true)"
if [ -n "$TOUCHED_TASK_SLUGS" ]; then
    echo -n "  Running log (warn)... "
    MISSING_LOG=""
    for slug in $TOUCHED_TASK_SLUGS; do
        if [ ! -f "$slug/log.md" ]; then
            MISSING_LOG="$MISSING_LOG $slug"
        fi
    done
    if [ -z "$MISSING_LOG" ]; then
        echo -e "${GREEN}OK${NC}"
    else
        echo -e "${YELLOW}WARN${NC}"
        echo -e "    ${YELLOW}Tasks/ folder(s) touched with no log.md:${MISSING_LOG}${NC}"
        echo -e "    ${YELLOW}Medium+ work should carry a running log.${NC}"
    fi
else
    echo "  Running log (warn)... (no Tasks/ folders touched, skip)"
fi

# --- Result ---
echo ""
if [ "$ERRORS" -gt 0 ]; then
    echo -e "${RED}Pre-commit: $ERRORS check(s) failed. Commit blocked.${NC}"
    exit 1
else
    echo -e "${GREEN}Pre-commit: all checks passed.${NC}"
    exit 0
fi
