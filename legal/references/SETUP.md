# Legal Skill — Setup Guide

The `legal` skill runs entirely within Claude — no external API keys or scripts are required.

## Installation

Install the `legal.skill` file into Claude Code:

1. Download `legal.skill` from this repository
2. In Claude Code, run: `claude skill install legal.skill`
3. The skill is now available as two commands:
   - `/legal:review-contract` — contract analysis
   - `/legal:meeting-briefing` — meeting preparation

## Usage

### Contract Review

Invoke with the slash command and paste your contract text:

```
/legal:review-contract

[paste your contract text here]
```

Or use natural language:
```
Review this contract for me:

[paste contract text]
```

Accepted input formats:
- Plain text (pasted directly)
- File path (`/path/to/contract.txt` or `.pdf` if readable)
- Partial text (the skill will note what's missing)

### Meeting Briefing

Invoke with context:

```
/legal:meeting-briefing

Meeting with: Acme Corp (vendor)
Purpose: Annual contract renewal negotiation
Our goal: 10% price reduction and better SLA terms
Background: 3-year relationship, they've missed SLAs twice this year
```

Or use natural language:
```
I have a meeting Monday with our SaaS vendor about renewing our contract.
They've been raising prices and I want to push back. Help me prepare.
```

## Privacy Note

Contract text and meeting details are processed by Claude's AI model. Do not paste contracts containing highly sensitive personal data (SSNs, passwords, financial account numbers) if you are using a shared or cloud Claude deployment. Review your organization's data handling policies before use.

## Disclaimer

This skill provides AI-assisted legal analysis for informational and preparation purposes only. It is not a substitute for qualified legal advice. For matters with significant legal, financial, or regulatory exposure, consult a licensed attorney in your jurisdiction.
