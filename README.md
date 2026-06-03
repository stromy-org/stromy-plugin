# Stromy Deliverables

Claude Code plugin for Stromy branded deliverables

## Prerequisites

- Claude Code v2.1.49+
- Node.js 18+, Python 3.11+ with [uv](https://docs.astral.sh/uv/)
- GitHub access to this repo (`gh auth login`)

## Installation

Via marketplace:
```bash
/plugin marketplace add stromy-org/stromy-marketplace
/plugin install stromy
```

For local development:
```bash
git clone https://github.com/stromy-org/stromy.git
cd stromy
npm install
uv sync
claude --plugin-dir .
```

## Skills

Skills are split between MCP-hosted stubs (fetched at runtime via
`ReadMcpResourceTool`) and locally-authored skills (frontmatter `_local: true`).
See `skills/README.md` for the maintenance workflow; the maintainer skill
`plugin-maintain` covers add / refresh / release.

## Updating

```bash
/plugin update stromy
```

## License

See [LICENSE](LICENSE) for terms.
