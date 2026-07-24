# Playwright MCP

**Registry entry:** `data/components/mcp-playwright.yaml` · **Category:** access-mcp

## What it is

Microsoft's official browser-automation MCP server: 40+ tools driving Chrome/Firefox/WebKit/Edge via accessibility snapshots rather than screenshots/vision models.

## When to use it

Your agent needs to click through real web UIs and you want fast, deterministic DOM-based automation rather than paying vision-model costs per action.

## How to get started

Install per your MCP client's docs; choose persistent-profile mode (keeps cookies/login across sessions) or isolated mode (fresh every run) based on whether you need to stay logged into test accounts.

## Gotchas

- Accessibility-tree-based, not vision-based — sites with poor accessibility markup may automate less reliably than a vision-model-driven tool would.

## How it compares

Contrast with browser-use (this registry's skills-tools category): browser-use is a Python library you embed directly; Playwright MCP is a standalone server any MCP client can call.

## References

- https://github.com/microsoft/playwright-mcp — verified via `gh api`/direct fetch, 2026-07-05
