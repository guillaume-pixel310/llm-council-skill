# Intelligence Artificielle

Référence de domaine sur l'usage de modèles de langage (LLM) dans un contexte de
conseil et d'aide à la décision — à consulter pour tout projet qui s'appuie sur de
l'IA générative, y compris le Conseil lui-même.

## Usages pertinents pour un conseil d'agents

- **Synthèse** : condenser un débat multi-perspectives en une recommandation
  actionnable — la valeur ajoutée vient de l'arbitrage, pas de la simple
  concatenation des positions.
- **Simulation de débat contradictoire** : faire porter explicitement des
  perspectives opposées (optimiste vs avocat du diable) avant de trancher, plutôt
  que de soumettre une question à un seul point de vue.
- **Rédaction structurée** : produire rapidement des premiers jets de rapports,
  résumés exécutifs ou supports de présentation à partir de données déjà
  vérifiées — jamais à partir de données non vérifiées par ailleurs.

## Risques à connaître

- **Hallucination** : un modèle peut produire une affirmation plausible mais fausse
  (un chiffre, une référence juridique, un précédent) avec la même assurance qu'une
  affirmation correcte — toute donnée chiffrée ou citation issue d'un LLM doit être
  vérifiée avant d'être utilisée dans une décision.
- **Confidentialité** : les informations soumises à une API externe transitent par un
  tiers — vérifier les conditions de traitement des données avant d'y soumettre des
  informations sensibles (financières, personnelles, stratégiques non publiques).
- **Biais de confirmation** : un modèle interrogé de façon suggestive a tendance à
  renforcer la position de celui qui pose la question — d'où l'intérêt de personas
  contradictoires forcés plutôt qu'une réponse unique.

## Build vs buy

- Utiliser une API généraliste (Anthropic, OpenAI) quand le besoin est de
  raisonnement ou de génération de texte sur des données déjà structurées.
- Construire un outil dédié quand le besoin est répétitif, à fort volume, ou
  nécessite une garantie de format de sortie strict (ex. génération automatisée de
  feuilles de calcul ou de présentations).

## Patterns de prompt pour agents multiples

- Donner à chaque agent une **persona stable** et des **marqueurs de sortie**
  identifiables facilite la synthèse automatisée du débat en aval.
- Limiter l'historique transmis à chaque agent (les derniers échanges plutôt que la
  totalité) évite une croissance quadratique du coût en tokens à mesure que le
  débat avance.
- Réserver un agent de synthèse final (l'Arbitre) plutôt que de faire la moyenne des
  positions — un arbitrage explicite produit une recommandation plus actionnable
  qu'un consensus mou.
