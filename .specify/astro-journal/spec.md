# Spec: Astro Journal

## Purpose

A standalone, client-side daily astrology journal for Guillaume: computes today's moon sign/phase from a real lunar ecliptic-longitude calculation, scores compatibility against his fixed natal chart, and lets him generate an AI-written personalized daily reading and jot a journal note.

## Trigger

Manual — the user opens `astro-journal/index.html` in a browser. No Claude Code skill trigger is involved; this runs entirely client-side.

## Inputs

- Today's date (read from the browser clock) — drives the moon-sign/phase calculation
- An Anthropic API key, entered once and stored in `localStorage` (`astro_journal_api_key`), used for the `x-api-key` header on direct browser calls to the Anthropic Messages API (model `claude-sonnet-4-6`)
- A free-text journal note entered by the user

## Outputs

- Today's moon sign, moon phase, and element/compatibility score, computed locally from `getMoonEclipticLongitude` / `getMoonSign` / `getCompatibility`
- An AI-generated daily reading (strict JSON: `titreJour`, `messageCore`, `domainesJour`, `luneMessage`, `actionDuJour`, `motSymbolique`) rendered in the UI, personalized against Guillaume's hardcoded natal chart and life context
- Saved journal notes, listed in the UI for the current session

## Key files

- `astro-journal/index.html` — entire implementation: natal chart constants (`NATAL`), moon phase/sign/compatibility math, the `AstroJournal` React component (loaded via CDN React + Babel standalone, no build step), the Anthropic API call

## Constraints & non-goals

- Single-user tool — the natal chart (`NATAL`) and life context baked into the AI prompt (CARNIS, séparation, Clara-Gabriela, Caroline, Grande Loge de Luxembourg) are hardcoded for Guillaume specifically, not parameterized for other users
- Journal notes are kept only in React component state (`useState`) — they are **not** persisted to `localStorage` or any backend, so they are lost on page refresh
- No server component — all computation and the Anthropic call happen directly in the browser
- API key handling is client-side only (`localStorage`) — there is no backend proxy or key rotation

## Open questions

- Journal notes have no persistence; if Guillaume wants notes to survive a refresh, this needs `localStorage` (or a backend) — not yet decided
- No automated tests cover this file
