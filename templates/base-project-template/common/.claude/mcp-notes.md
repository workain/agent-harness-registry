<!-- TEMPLATE FILE — delete this comment once you've read it. -->

# MCP notes

A 5-point note, not a guide — full research (incidents, token-cost measurements, source list) is
this registry's own `deep-dives/components/access-mcp/` catalog, not repeated here.

1. MCP is not the first tool to reach for — check whether a Bash call to an existing command
   (`gh`, `psql`, `aws`) already does the job before adding a standing server.
2. Config lives in `.mcp.json` at the project root for `project` scope — it's reviewed as code,
   not typed into a chat.
3. Keep the connected set minimal: every server is permanent context tokens on every request and
   one more failure/attack surface, whether or not a given task uses it.
4. Before connecting a server, check the "lethal trifecta": private data + untrusted external
   content + an outbound channel, all at once. If a connection would give an agent all three,
   split the work across sessions instead of connecting it as-is.
5. For HTTP-transport servers, only the OAuth flow — never a pasted-in long-lived token.
