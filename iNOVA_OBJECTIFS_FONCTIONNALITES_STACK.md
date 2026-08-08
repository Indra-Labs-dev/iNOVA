# iNOVA — Objectif, Fonctionnalités, Stack

> Document de référence détaillé du **projet complet** (pas seulement le MVP), dérivé de [iNOVA_MASTER_CONTEXT.md](iNOVA_MASTER_CONTEXT.md) et [iNOVA_CAHIER_DES_CHARGES.md](iNOVA_CAHIER_DES_CHARGES.md).
> Chaque module est étiqueté **[Phase N]** pour situer *quand* il est construit dans la roadmap — mais toutes les fonctionnalités listées font partie du périmètre cible final du produit.
> Matériel IA local retenu pour l'instant : **GPU 4 Go VRAM**, adaptable plus tard.

---

## 1. Objectif du projet

### 1.1 Vision

iNOVA est un **environnement numérique intelligent unifié** — pas une collection d'outils séparés, mais une **plateforme cohérente** où intelligence artificielle, agents autonomes, cybersécurité, développement, veille d'information, apprentissage et productivité partagent un même socle (authentification, permissions, mémoire, événements, design system).

> *iNOVA est un univers numérique intelligent qui apprend, recherche, crée, protège, automatise et évolue avec son utilisateur.*

L'utilisateur doit avoir l'impression d'interagir avec un environnement vivant, pas avec un tableau de bord classique — tout en restant **prévisible, transparent, contrôlable et sécurisé**.

### 1.2 Les 5 objectifs produit

1. **UX exceptionnelle** — interface futuriste hybride 2D/3D, holographique, mascotte interactive, animations contextuelles, sans jamais sacrifier l'usabilité.
2. **IA au-delà du chat** — raisonnement, récupération d'information, utilisation d'outils, appel de services applicatifs, collaboration multi-agents, mémoire contextuelle, explicabilité des décisions.
3. **Personnalisation** — adaptation progressive aux intérêts, habitudes et workflows de l'utilisateur, dans le respect de la vie privée et du consentement explicite.
4. **Écosystème unifié** — tous les modules partagent authentification, permissions, événements, contexte IA, mémoire, notifications, profil utilisateur, design system, recherche, historique.
5. **Extensibilité** — plateforme conçue pour ajouter de nouveaux modules/agents sans réécrire le cœur.

### 1.3 Philosophie produit

- Le monde peut réagir, la mascotte peut être expressive, l'IA peut être conversationnelle — mais le système doit toujours rester **compréhensible et maîtrisable** par l'utilisateur.
- **Construction incrémentale obligatoire** : ne jamais tenter de construire tous les modules en même temps. Prioriser architecture et maintenabilité avant complexité visuelle.
- Un agent IA ne doit **jamais** obtenir un accès non restreint au système, aux fichiers, au réseau, aux identifiants ou aux services externes de l'utilisateur.

---

## 2. Fonctionnalités du projet complet

> Périmètre exhaustif de tout ce qu'iNOVA doit couvrir à terme. Le repère **[Phase N]** indique quand chaque bloc est construit dans la roadmap (voir [cahier des charges §9](iNOVA_CAHIER_DES_CHARGES.md)), mais toutes les fonctionnalités ci-dessous font partie du périmètre cible du projet complet, pas seulement du MVP.

### 2.1 AI Hub — cœur conversationnel et cognitif [Phase 1, étendu en continu]

- Conversation textuelle multi-tours avec mémoire contextuelle
- Interaction multimodale (texte, documents, éventuellement image)
- Analyse de documents uploadés
- Résumé, traduction, génération de contenu
- Raisonnement et récupération d'information (retrieval)
- Utilisation d'outils (function calling) et appel de services applicatifs internes
- Recommandations contextuelles basées sur l'activité de l'utilisateur
- Mémoire persistante (au-delà de la session courante), avec gestion explicite de ce qui est retenu
- Explicabilité : l'IA doit pouvoir expliquer ses décisions et actions
- Collaboration avec les agents spécialisés (délégation de sous-tâches)
- Architecture multi-provider : ne jamais coder en dur autour d'un seul fournisseur de modèle (voir §3.5 — actuellement Ollama local, remplaçable)

### 2.2 Agent Hub — travailleurs IA spécialisés [Phase 4, extension continue]

Agents prévus pour le projet complet :

- `ResearchAgent` — recherche et synthèse d'information
- `CodeAgent` — assistance au développement, analyse de projet
- `CyberAgent` — analyse de sécurité, classification de vulnérabilités
- `OSINTAgent` — collecte d'informations publiques
- `TutorAgent` — accompagnement pédagogique
- `DataAgent` — analyse de données
- `CloudAgent` — assistance infrastructure/cloud
- `WriterAgent` — génération et édition de contenu
- `ProductivityAgent` — organisation, planification

Chaque agent expose : identité, but, capacités, outils, permissions, mémoire/contexte, politique d'exécution, statut, journal d'audit.

**Orchestration** : un Agent Router reçoit les requêtes utilisateur et les distribue vers l'agent (ou les agents) pertinent(s) ; les agents peuvent collaborer sur une même tâche.

**Principe de sécurité permanent** : un agent IA ne doit jamais obtenir un accès non restreint au système, aux fichiers, au réseau, aux identifiants ou aux services externes. Chaque outil a une permission scopée explicite (ex. `productivity.tasks.write`), un niveau de risque (LOW/MEDIUM/HIGH), et une politique de confirmation (optionnelle ou obligatoire) — les actions à risque élevé doivent être sandboxées si possible et systématiquement journalisées (trace complète : requête utilisateur → décision de l'agent → outil sélectionné → vérification de permission → confirmation → exécution → résultat → log d'audit).

### 2.3 Cybersecurity Hub [Phase 6]

- Analyse de sécurité de l'appareil
- Analyse des permissions d'applications
- Analyse des processus en cours
- Analyse réseau, visibilité des ports/services
- Vérifications de configuration
- Renseignement sur les vulnérabilités, recherche CVE
- Recommandations de sécurité personnalisées
- Analyse de fichiers
- Réputation d'URL/domaine
- Threat intelligence
- Alertes de sécurité
- Rapports de sécurité
- Score de posture de sécurité global (ex. tableau de bord "94/100" avec statut par catégorie : appareil, réseau, applications, comptes, vulnérabilités)

**Limites permanentes** : uniquement sur systèmes dont l'utilisateur est propriétaire ou autorisé, analyse défensive et passive/publique uniquement — jamais de plateforme d'automatisation offensive non restreinte.

### 2.4 Programming Hub [Phase 6]

- Éditeur de code intégré (Monaco Editor)
- Explorateur de projet
- Terminal intégré
- Intégration Git et GitHub
- Génération de code assistée par IA
- Refactoring assisté
- Aide au débogage
- Génération et exécution de tests
- Analyse statique de code
- Analyse des dépendances
- Génération de documentation
- Assistance à la décision architecturale
- Test d'API
- Workflows Docker
- Assistance CI/CD
- Revue de code assistée
- Développement conscient de la sécurité (security-aware development)
- Communication bidirectionnelle avec `CodeAgent` et `CyberAgent` — exemple de flux complet :
  `Utilisateur : "Analyse la sécurité de mon API"` → `CodeAgent` inspecte le projet, les dépendances, le code pertinent → `CyberAgent` fait l'analyse de sécurité, classe les vulnérabilités, formule des recommandations → `CodeAgent` propose des correctifs et génère des tests → l'utilisateur vérifie les changements avant application.

Toute modification de code proposée doit rester révisable et réversible par l'utilisateur.

### 2.5 Research & Intelligence Hub [Phase 5]

- Collecte d'informations depuis des sources publiques et autorisées : APIs officielles, flux RSS, pages web publiques (si permis), documentation publique, jeux de données publics, documents uploadés par l'utilisateur
- Traitement et synthèse de ces informations par l'IA
- Priorité systématique aux APIs officielles et flux RSS plutôt qu'au scraping

**Contraintes permanentes** : respect de robots.txt, des conditions d'utilisation, des limites de débit, du droit d'auteur, des exigences d'authentification, attribution systématique des sources. Interdiction absolue de construire des mécanismes de contournement des protections anti-bot ou des contrôles d'accès.

### 2.6 News Intelligence [Phase 5]

Pipeline complet de traitement de l'actualité :

`Sources → Collecte → Normalisation → Déduplication → Classification → Résumé IA → Recoupement des sources → Personnalisation → Fil d'actualité iNOVA`

- Catégories couvertes : IA, cybersécurité, programmation, technologie, startups, science, gaming, actualité locale, économie, sujets définis par l'utilisateur
- Digest personnalisé (ex. "iNOVA Morning Intelligence" avec nombre de mises à jour importantes par catégorie et une recommandation contextuelle de l'IA)
- Conservation systématique des liens source et des dates de publication
- Les résumés IA doivent distinguer clairement : faits sourcés, inférence, opinion, et incertitude

### 2.7 OSINT / Public Intelligence Hub [Futur, après Phase 6]

- Informations DNS
- Informations de certificats publics
- Métadonnées de domaine
- Informations techniques publiques (stack détectée, etc.)
- Informations publiques GitHub
- Informations de réputation publique
- Threat intelligence publique
- Corrélation avec l'actualité

Fonctionnalité destinée à la recherche légitime, la sécurité défensive, l'investigation et l'évaluation autorisée — jamais l'accès non autorisé ou l'exploitation.

### 2.8 Knowledge Graph [Futur]

- Connexion sémantique entre entités, relations, documents, événements, intérêts utilisateur et découvertes des agents
- Exemple de capacité : relier "Flutter" à "Dart", "Android", "iOS", "Firebase", des versions, des articles associés
- Doit permettre de répondre à des questions du type : *"Quelles technologies liées à Flutter ont changé récemment ?"*

### 2.9 Watchlists & alertes intelligentes [Futur]

- L'utilisateur peut surveiller des sujets organisés en listes (ex. Cybersécurité : CVE, OWASP, événements majeurs ; IA : modèles, fournisseurs, LLM locaux ; Développement : Flutter, Python, FastAPI, Docker ; Personnalisé : mots-clés libres)
- Le système agrège et priorise plutôt que d'inonder l'utilisateur de notifications (ex. "37 nouveaux éléments trouvés, 3 nécessitent votre attention" avec niveaux CRITICAL/IMPORTANT/TRENDING)

### 2.10 Learning Hub [Phase 7]

- Parcours d'apprentissage structurés
- Cours
- Explications à la demande
- Exercices
- Quiz
- Suivi de progression
- Difficulté adaptative
- Recommandations personnalisées de contenu
- Tuteur IA dédié
- Révision de connaissances

La mascotte peut agir comme compagnon d'apprentissage de l'utilisateur.

### 2.11 Productivity Hub [Phase 7]

- Gestion de tâches
- Calendrier
- Notes
- Objectifs
- Rappels
- Suivi d'habitudes
- Sessions de concentration (focus sessions)
- Gestion de projet personnel
- Planification personnelle

Exemple d'usage : *"Organise ma journée"* → iNOVA inspecte le contexte calendrier/tâches autorisé, propose un planning, et demande confirmation avant de créer ou modifier des enregistrements importants.

### 2.12 Device Hub [Phase 7]

Intégration avec les appareils possédés par l'utilisateur (téléphone, PC, serveur) :

- CPU, RAM, stockage, batterie
- État réseau
- Processus en cours
- Applications installées
- Informations système générales
- Statut de sécurité de l'appareil

Tout accès à ces informations est strictement basé sur des permissions explicites accordées par l'utilisateur.

### 2.13 Cloud / Infrastructure Hub [Phase 7]

Intégration potentielle avec :

- Docker
- Serveurs
- Machines virtuelles
- Bases de données
- APIs
- Logs
- Monitoring
- Sauvegardes
- Déploiements

iNOVA doit être capable d'expliquer un problème d'infrastructure et de suggérer des correctifs — sans automatisation destructive par défaut.

### 2.14 iNOVA World — environnement 3D [Phase 3, enrichi en continu]

- Monde 3D complet représentant iNOVA : planète/monde central, bâtiments futuristes par module, interfaces holographiques, portails de navigation, systèmes de particules, objets flottants, flux de données visualisés, représentations visuelles de chaque hub (Cyber, IA, Code, Agents, Learning, Productivity, etc.)
- Navigation immersive entre les modules via le monde 3D
- Caméra, effets de profondeur, transitions fluides entre 2D et 3D
- Réactions visuelles du monde aux événements importants (ex. alerte de sécurité, nouvelle mission)

Technologies imposées : Three.js, WebGL, formats GLTF/GLB, shaders et post-processing utilisés seulement si justifiés, systèmes de particules, avec une attention constante à la performance. Le monde 3D ne doit pas être construit en profondeur avant que le produit sous-jacent (IA, données, agents) soit fonctionnel.

### 2.15 Frontend 2D [Phase 0-1, socle permanent]

- Shell applicatif complet (Flutter)
- Navigation entre tous les modules
- Tableaux de bord par hub
- Formulaires
- Paramètres utilisateur
- Cartes d'information (cards)
- Vues de données (data views)
- Layout responsive (mobile, tablette, desktop, web)
- Intégration API REST et WebSocket temps réel

Le 3D reste une couche spécialisée : toutes les vues ne doivent pas devenir 3D.

### 2.16 Mascotte (Nova) [Phase 2, comportements enrichis en continu]

Ensemble complet des états de la mascotte : `idle`, `welcome`, `thinking`, `listening`, `speaking`, `working`, `success`, `joy`, `error`, `warning`, `waiting`, `loading`, `incoming_event`.

La mascotte réagit à : l'état de l'IA, la complétion de tâches, les erreurs, les alertes, les succès/réussites, les interactions directes de l'utilisateur, les événements système importants.

Machine à états dédiée reliant les événements applicatifs aux états visuels (ex. `AI_THINKING` → mascotte `THINKING`, `AI_SUCCESS` → mascotte `JOY`).

### 2.17 Gamification [Intégrée progressivement à partir du MVP]

- Système de points d'expérience (XP)
- Niveaux de progression
- Séries (streaks)
- Missions
- Succès/achievements déblocables
- Éléments visuels déblocables
- Personnalisation de la mascotte
- Évolution visuelle du monde 3D en fonction de la progression

Doit toujours encourager des comportements réellement utiles à l'utilisateur, jamais le manipuler (pas de dark patterns).

### 2.18 Mission System [Phase 4+, capacité majeure du produit complet]

L'utilisateur donne un objectif de haut niveau (ex. *"Sécurise mon projet"*), et le système construit un plan structuré, potentiellement multi-agents :

`Mission → Analyse du code → Analyse des dépendances → Vérifications de sécurité → Tests → Correctifs proposés → Vérification → Rapport`

L'utilisateur doit pouvoir inspecter à tout moment : le plan complet, l'étape en cours, l'agent impliqué, les outils utilisés, les résultats intermédiaires, les confirmations en attente, les erreurs survenues, et le rapport final.

### 2.19 iNOVA Pulse [Futur]

Centre d'intelligence visuelle temps réel représentant : nouvelles actualités, tendances IA, alertes cybersécurité, mises à jour de développement, agents actifs, tâches en cours, événements système (ex. "127 nouveaux éléments collectés — IA +12 tendances, Cyber +8 alertes, Dev +21 mises à jour"). Le monde 3D peut réagir visuellement aux événements les plus importants remontés par Pulse.

### 2.19 iNOVA Pulse

- [Futur] Centre d'intelligence temps réel : actualités, tendances IA, alertes cybersécurité, mises à jour dev, agents actifs, tâches, événements système
- Le monde 3D peut réagir visuellement aux événements importants

---

## 3. Stack technique à utiliser

### 3.1 Frontend 2D

| Élément | Technologie |
|---|---|
| Framework applicatif | **Flutter** (Dart) |
| Gestion d'état | **Riverpod** |
| Éditeur de code intégré (Programming Hub) | **Monaco Editor** |

### 3.2 Frontend 3D

| Élément | Technologie |
|---|---|
| Moteur 3D | **Three.js** |
| Rendu | **WebGL** |
| Format d'assets | **GLTF/GLB** |
| Effets | Shaders et post-processing, seulement si justifiés ; systèmes de particules |

### 3.3 Mascotte / animation

| Élément | Technologie |
|---|---|
| Machine à états interactive de la mascotte | **Rive** |
| Effets ponctuels | **Lottie** |
| Complément | SVG et assets 3D où pertinent |

### 3.4 Backend

| Élément | Technologie |
|---|---|
| Langage / framework API | **Python + FastAPI** |
| Base de données relationnelle | **PostgreSQL** |
| Cache / pub-sub événementiel | **Redis** |
| Temps réel | **WebSocket** (WebRTC envisagé pour des fonctionnalités futures) |
| Stockage de fichiers/assets | Stockage objet (local/MinIO en dev, S3-compatible en prod) |

### 3.5 Intelligence artificielle

| Élément | Choix retenu |
|---|---|
| Mode d'exécution | **Local**, via **Ollama** |
| Contrainte matérielle actuelle | GPU **4 Go VRAM** |
| Modèle de démarrage recommandé | `qwen2.5:3b-instruct-q4_K_M` (tient entièrement en VRAM, bon support natif du tool-use) |
| Modèle de repli si latence acceptable | `qwen2.5:7b-instruct-q4_K_M` (offload CPU partiel) |
| Abstraction logicielle obligatoire | Interface `LLMProvider` découplée — permet de changer de modèle local ou de brancher une API cloud plus tard sans réécrire les agents |

### 3.6 Infrastructure / DevOps

| Élément | Technologie |
|---|---|
| Hébergement backend | VPS (OVH, Scaleway, Hetzner, ou équivalent) |
| Certificats | Let's Encrypt |
| CI/CD | GitHub Actions |
| Monitoring / erreurs | Sentry ou Grafana (tiers gratuits au démarrage) |

### 3.7 Sécurité (transverse à toute la stack)

- Authentification et autorisation dès le départ (JWT + PostgreSQL, ou solution managée si besoin de rapidité)
- Permissions scopées par outil d'agent, avec niveau de risque et confirmation obligatoire pour les actions à risque élevé
- Aucune exécution aveugle de sortie de modèle IA
- TLS obligatoire, secrets hors code source, validation des entrées/sorties, rate limiting, journal d'audit systématique

---

## 4. Structure de projet suggérée (frontend Flutter)

```text
lib/
├── core/            # routing, thème, réseau, stockage, permissions, design system
├── features/        # ai, agents, cybersecurity, programming, news, osint, learning, productivity, cloud, devices
├── nova/            # mascotte, personnalité, émotions, machine à états
├── world/           # scène 3D, objets, caméra, effets, interactions
└── shared/          # widgets, animations, composants partagés
```

Chaque feature doit rester découpée en composants petits et cohérents — pas de fichiers géants.
