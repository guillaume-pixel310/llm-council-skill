# Conseil

Système modulaire de conseil multi-agents pour les décisions de XIII SARL (et
réutilisable au-delà). Treize personas spécialisées délibèrent contradictoirement sur
une question, s'appuient sur des fiches de domaine, et produisent une sortie suivant
des gabarits standardisés.

Distinct de `conseil-agents/index.html`, qui reste l'application web autonome
existante (10 agents, personas en JS, appel direct au navigateur). Ce dossier
externalise et étend les personas en fichiers structurés, indépendants de toute
implémentation — destinés à être chargés par n'importe quel script, skill ou
application future (y compris, à terme, une refonte de `conseil-agents/`).

## Structure

```
conseil/
  agents/       13 personas (front-matter + mandat + prompt + marqueurs de sortie)
  skills/       8 fiches de domaine (gastronomie, hôtel, immobilier, investissement,
                M&A, luxe, communication, IA) — référence factuelle pour les agents
  templates/    gabarits de sortie (rapport long, résumé exécutif, radar chart,
                feuille de route)
  outputs/      artefacts générés (html/, pdf/, pptx/) — non versionnés sauf .gitkeep
```

## Agents

| # | Agent | Rôle |
|---|---|---|
| 01 | Avocat du Diable | Failles, angles morts, scénarios d'échec |
| 02 | Déconstructeur | Faits vs hypothèses vs aspirations |
| 03 | Optimiste | Scénarios haussiers chiffrés, asymétrie favorable |
| 04 | Regard Extérieur | Œil naïf, taux de base, bon sens |
| 05 | Homme d'Action | Exécution, test minimal, biais pour l'engagement |
| 06 | Grand Avocat | Plaidoirie, droit des affaires |
| 07 | Stratège Business | Vision systémique, position concurrentielle |
| 08 | Politicien | Rapport de force, acceptabilité institutionnelle |
| 09 | Stratège International | Expansion transfrontalière, risque géopolitique |
| 10 | Directeur Artistique | Cohérence curatoriale, identité visuelle |
| 11 | Directeur de la Communication | Narrative, presse, réputation, crise |
| 12 | Family Office | Allocation patrimoniale, gouvernance, transmission |
| 13 | Expert-Comptable | Conformité, comptabilité, fiscalité |

## Usage prévu

1. Choisir les agents pertinents pour la question posée (pas nécessairement les 13).
2. Faire délibérer chaque agent en lui fournissant sa fiche `agents/*.md` et les
   fiches `skills/*.md` pertinentes en contexte.
3. Synthétiser dans un gabarit de `templates/`.
4. Exporter le résultat dans `outputs/` (html, pdf ou pptx selon le besoin).
