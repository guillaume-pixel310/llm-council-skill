# 23 — RAG Database

> But : index structuré du vault pour interrogation par IA (RAG) — quels fichiers, quelles métadonnées, comment les requêter.

## Architecture du pipeline

```
ZIP, ChatGPT, Claude, Gmail, PDF, Notes, Contrats, Comptabilité, Calendrier, Notion
        ↓
   Embeddings
        ↓
     Qdrant
        ↓
  Guillaume OS
        ↓
Claude / ChatGPT / Gemini
```

1. **Sources** — exports/connecteurs bruts : archives ZIP, historiques ChatGPT et Claude, Gmail, PDF, Notes, Contrats, Comptabilité, Calendrier, Notion.
2. **Embeddings** — chaque source est découpée et vectorisée.
3. **Qdrant** — base vectorielle qui stocke les embeddings et leurs métadonnées, interrogeable par similarité.
4. **Guillaume OS** — ce vault sert de couche de structure/contexte au-dessus des vecteurs bruts (sections, fiches, registres).
5. **Claude / ChatGPT / Gemini** — les modèles interrogent Qdrant + Guillaume OS pour répondre avec le contexte personnel complet.

## Index des sources
| Source | Type de contenu | Format | Fréquence de mise à jour |
|---|---|---|---|
| ZIP | *(à compléter — archive de quoi ?)* | | |
| ChatGPT | Historique de conversations | export JSON | |
| Claude | Historique de conversations | export JSON | |
| Gmail | E-mails | API / export | |
| PDF | Documents | PDF | |
| Notes | Notes personnelles | *(à compléter)* | |
| Contrats | Contrats juridiques | PDF | renvoi [16_DOCUMENTS](../16_DOCUMENTS/README.md) |
| Comptabilité | Données comptables | *(à compléter)* | renvoi [07_PATRIMONY](../07_PATRIMONY/README.md) |
| Calendrier | Événements | API (Google Calendar, etc.) | |
| Notion | Pages/bases Notion | API / export | |

## Métadonnées à maintenir
- *(à compléter — tags, dates, sensibilité, source d'origine)*

## Pipeline d'indexation
- **Embeddings** : *(à compléter — modèle utilisé)*
- **Stockage** : Qdrant — *(à compléter — instance, collection(s))*
- **Fréquence de ré-indexation** : *(à compléter)*
- **Accès** : Claude / ChatGPT / Gemini interrogent Qdrant via *(à compléter — MCP, API, retrieval layer)*
