# Spec: XIII SARL Pitch Deck

## Purpose

A script that generates a fixed-content investor pitch deck for XIII SARL (Culture · Food · Immobilier — curated dinners, art sales, consulting, real estate) as a 16:9 PowerPoint file.

## Trigger

Manual — run `python3 xiii-sarl/generate_xiii_presentation.py` from a terminal with `python-pptx` installed. No Claude Code skill trigger is involved.

## Inputs

None at runtime — slide titles, bullets, and styling (cover, 11 content slides: mission, problème, solution, offre, marché, business model, structure juridique, équipe, finances clés, ask, roadmap) are hardcoded in the script.

## Outputs

- `xiii-sarl/XIII_SARL_PitchDeck.pptx` — the rendered 16:9 deck, overwritten on each run
- The repo also tracks the built `.pptx` directly (not gitignored), so the script and its output can drift if one is edited without the other

## Key files

- `xiii-sarl/generate_xiii_presentation.py` — entire implementation: `add_cover` / `add_slide` helpers (python-pptx, blank layout, fixed brand colors `PANTONE_RGB`/`WHITE`/`GRAY`/`BLACK`, `Playfair Display` font), the `slides` list of `(title, bullets)` tuples, and the final `ppt.save(...)`
- `xiii-sarl/XIII_SARL_PitchDeck.pptx` — committed build artifact

## Constraints & non-goals

- No CLI arguments or templating — all deck content is hardcoded; changing the pitch means editing the Python source directly
- No persistence beyond the single `.pptx` file; re-running overwrites it
- If the script changes, the committed `.pptx` must be regenerated and committed alongside it (no automated check enforces this, unlike the `llm-council.skill` / `legal.skill` ZIP-sync check)

## Open questions

- No automated tests cover this script
- Whether the built `.pptx` should be committed at all (vs. generated on demand) is not settled
