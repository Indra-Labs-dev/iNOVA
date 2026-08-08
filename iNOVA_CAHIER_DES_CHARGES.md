# Cahier des charges — Projet iNOVA

> Document dérivé de [iNOVA_MASTER_CONTEXT.md](iNOVA_MASTER_CONTEXT.md) (vision produit) et transformé en spécifications actionnables : périmètre, architecture, stack, dépendances externes, phasage, budget.
>
> **État du projet au 08/08/2026 :** aucun code écrit. Un seul document de vision + un logo. Tout reste à construire.

---

## 0. Résumé exécutif

iNOVA est un environnement numérique intelligent unifié : IA conversationnelle, agents autonomes spécialisés, cybersécurité, développement assisté, veille/actualités, OSINT, apprentissage, productivité — le tout dans une interface hybride 2D (Flutter) / 3D (Three.js) avec une mascotte IA animée (Rive).

**Le piège principal à éviter** : c'est un projet à l'ambition quasi illimitée (14+ modules, IA multi-agents, 3D temps réel, gamification...). Tenté d'un coup, il ne verra jamais le jour. Ce cahier des charges définit donc un **MVP resserré** et une trajectoire par phases, en isolant clairement ce qui peut être fait **seul, gratuitement, avec du code**, de ce qui **nécessite des comptes, clés API ou budget externes**.

---

## 1. Objectif du document

Répondre à trois questions :

1. **Quoi construire** — périmètre fonctionnel réaliste, priorisé.
2. **Comment le construire** — architecture, stack, structure de projet.
3. **Avec quoi** — services, comptes et dépendances externes indispensables, et leur coût.

---

## 2. Périmètre — MVP (première cible réelle)

Le document source liste 14 hubs. Construire cela en une fois est irréaliste pour un seul développeur ou une petite équipe. Le MVP recommandé (déjà esquissé dans le master context, §34) :

| Module MVP | Contenu minimal |
|---|---|
| **AI Hub** | Chat, mémoire courte, appel d'outils (function calling) |
| **Dashboard 2D** | Shell Flutter, navigation, thème/design system de base |
| **Monde 3D (v0)** | Une scène Three.js simple, pas de gameplay complexe |
| **Mascotte** | État de base (idle/thinking/speaking) en Rive |
| **Agent Hub (v0)** | 1 seul agent réel (ex. `ResearchAgent`) avec permissions scopées |
| **News Intelligence (v0)** | Ingestion RSS + résumé IA, sans dédup avancée ni graphe de connaissances |
| **Security Hub (v0)** | Score de sécurité basique (checks statiques, pas de scan réseau actif) |
| **Missions (v0)** | Une tâche simple avec XP, sans orchestration multi-agents |

**Explicitement hors MVP** : Cloud/Infrastructure Hub, Device Hub, Learning Hub, Productivity Hub complet, Knowledge Graph, Watchlists avancées, OSINT Hub, Programming Hub complet (éditeur Monaco intégré). Ces modules sont documentés (§14 roadmap) mais ne doivent pas être commencés avant que le socle (Core + AI + 1 agent + UI) soit stable.

---

## 3. Architecture cible

```
Flutter (2D shell) ── Three.js/WebGL (monde 3D, embarqué en WebView/iframe)
        |
   API Gateway (FastAPI)
        |
 +------+------+--------+---------+
 |      |      |        |         |
AI Core Agents Modules  Events   Auth
 |      |      |        |
 LLM  Runtime Services  Redis (pub/sub)
        |
   PostgreSQL (données), Object Storage (fichiers/assets)
```

Principes non négociables issus du master context :
- Frontend (Flutter) découplé du backend — jamais de logique métier côté client au-delà de l'UI.
- Les agents IA n'ont **jamais** d'accès système non scopé : allowlist d'outils, permissions explicites, confirmation obligatoire pour toute action à risque, journal d'audit.
- Le 3D reste une couche spécialisée — ne pas forcer tous les écrans en 3D.

---

## 4. Stack technique retenue

| Couche | Technologie | Statut |
|---|---|---|
| Frontend 2D | Flutter + Dart + Riverpod | Décision actée |
| Animation mascotte | Rive (+ Lottie pour effets ponctuels) | Décision actée |
| Frontend 3D | Three.js + WebGL + GLTF/GLB | Décision actée, non négociable sauf refonte archi |
| Éditeur de code (Programming Hub) | Monaco Editor | Prévu, hors MVP |
| Backend API | Python + FastAPI | Direction retenue |
| Base de données | PostgreSQL | Direction retenue |
| Cache / pub-sub événementiel | Redis | Direction retenue |
| Temps réel | WebSocket (WebRTC envisagé plus tard) | Direction retenue |
| IA | **Local via Ollama**, décision actée — garder une abstraction multi-provider pour pouvoir basculer sur une API cloud plus tard sans réécrire les agents | Voir §5.1bis |

---

## 5. Dépendances et services externes nécessaires

C'est le point que vous avez signalé comme important — voici tout ce qui **ne peut pas être fait uniquement avec du code local**, classé par obligation.

### 5.1 Indispensables dès le MVP

| Service | Pourquoi | Gratuit possible ? |
|---|---|---|
| **Runtime LLM local (Ollama ou llama.cpp)** | Cœur de l'AI Hub — chat, résumé, function calling | Oui — logiciel gratuit, coût = électricité + votre matériel existant |
| **Hébergement backend** (VPS ou cloud : OVH, Scaleway, Hetzner, AWS/GCP/Azure) | FastAPI + PostgreSQL + Redis doivent tourner quelque part en continu | Non — mais un petit VPS (~5-10€/mois) suffit pour du dev/MVP. **Le LLM local, lui, tourne sur votre machine GPU, pas sur ce VPS** (voir §5.1bis) |
| **Nom de domaine** | Identité du produit, API publique, certificats | Non — ~10€/an |
| **Certificat SSL** | Trafic chiffré obligatoire (§30 sécurité) | Oui — Let's Encrypt, gratuit |
| **Stockage objet** (assets, fichiers uploadés, GLTF/GLB) | Fichiers 3D, documents, avatars | Oui en dev (stockage local/MinIO) ; en prod S3/Cloudflare R2 ont des tiers gratuits limités |

### 5.1bis LLM local — dimensionnement pour 4 Go de VRAM

**Décision actée : IA locale via Ollama, pas d'API cloud payante.** Avec 4 Go de VRAM, c'est une contrainte forte à documenter honnêtement plutôt qu'à ignorer.

**Ce qui tient dans 4 Go VRAM (quantization Q4_K_M) :**

| Modèle | Taille | Adapté au function calling agentique ? |
|---|---|---|
| **Qwen2.5-3B-Instruct** | ~2 Go en Q4 | Correct — Qwen est entraîné nativement au tool-use, meilleur choix à cette taille |
| **Llama-3.2-3B-Instruct** | ~2 Go en Q4 | Moyen — tool-use surtout par prompting, moins fiable que Qwen |
| **Phi-3.5-mini (3.8B)** | ~2,2 Go en Q4 | Bon raisonnement général, tool-use faible |
| **Qwen2.5-7B-Instruct** | ~4,7 Go en Q4 | Meilleur modèle possible ici, mais dépasse légèrement 4 Go → Ollama fera un *offload* partiel CPU/GPU automatique (plus lent, reste utilisable) |

**Recommandation concrète :** commencer avec `qwen2.5:3b-instruct-q4_K_M` (rapide, tient entièrement en VRAM) et tester `qwen2.5:7b-instruct-q4_K_M` en second choix si la latence avec offload CPU reste acceptable pour vous.

**Point de vigilance important pour l'architecture agents (§5, §31 du master context) :** à cette taille de modèle, le *function calling* multi-étapes (Agent Router, missions à plusieurs agents) sera **moins fiable** qu'avec un modèle cloud de pointe — attendez-vous à des appels d'outils mal formés ou halluciés plus fréquents. Conséquences pratiques à prévoir dès le design :
- Valider strictement chaque appel d'outil côté serveur (schéma JSON strict, jamais de confiance aveugle dans la sortie du modèle — déjà une exigence §30-31, mais elle devient critique ici).
- Prévoir un mécanisme de retry/correction si le modèle produit un appel d'outil invalide.
- Limiter le MVP à des agents à peu d'étapes (1-2 outils par tâche) plutôt qu'à de longues chaînes de raisonnement autonomes.
- Garder l'abstraction multi-provider du §4.1 du master context bien réelle dans le code (interface `LLMProvider`), pour pouvoir brancher une API cloud plus tard sur les mêmes agents sans réécriture, si la fiabilité locale s'avère insuffisante pour certains modules (ex. CyberAgent sur des analyses critiques).

**Coût réel du choix local :** pas de facturation à l'usage, mais coût caché en temps de développement (itération plus lente, debug de tool-calling moins fiable) et en électricité. Aucun budget à prévoir dans la ligne "API LLM" du §5.6.

### 5.2 Nécessaires selon les modules activés

| Module | Service externe | Remarque |
|---|---|---|
| News Intelligence | Flux RSS (gratuits) + éventuellement NewsAPI ou équivalent payant pour plus de sources | Respecter ToS/robots.txt (déjà exigé §8) |
| Security Hub | Base CVE/NVD (API publique, gratuite mais rate-limitée), éventuellement VirusTotal / AbuseIPDB pour réputation | Comptes gratuits avec quotas |
| OSINT Hub (hors MVP) | Shodan, WHOIS, DNS lookup APIs | Certains payants au-delà du tier gratuit |
| Authentification | Peut être développée en interne (JWT + PostgreSQL) **ou** déléguée à Auth0/Clerk/Firebase Auth pour aller plus vite | Auth interne = gratuite mais plus de travail ; solution managée = payante au volume |
| Notifications / emails (vérification compte, alertes) | SendGrid, Postmark, ou Amazon SES | Tiers gratuits existent (ex. 100 emails/jour) |
| Monitoring / erreurs | Sentry, Grafana Cloud | Tiers gratuits suffisants au démarrage |
| CI/CD | GitHub Actions | Gratuit pour repos publics, quota généreux en privé |

### 5.3 Si distribution mobile/desktop native (au-delà du web)

| Service | Coût |
|---|---|
| Compte développeur Apple (App Store) | 99 $/an |
| Compte développeur Google Play | 25 $ (paiement unique) |

### 5.4 Assets créatifs (facultatif mais recommandé)

- **Rive** : éditeur gratuit pour usage individuel/petite équipe ; plans payants pour la collaboration en équipe.
- Modèles 3D (GLTF/GLB) : Sketchfab, Poly Haven, ou modélisation maison (Blender, gratuit).

### 5.5 Ce qui reste 100% gratuit / auto-hébergeable

FastAPI, PostgreSQL, Redis, Flutter, Three.js, Monaco Editor, Let's Encrypt, GitHub Actions (usage raisonnable), Ollama pour le LLM local — tout le cœur technique peut tourner sans dépense en auto-hébergement.

### 5.6 Recommandation budgétaire de démarrage (MVP, choix local acté)

~20-40 €/mois (VPS backend + nom de domaine). **Pas de ligne "API LLM"** grâce au choix local — c'est l'économie principale de cette décision. Seul coût variable réel : l'électricité de la machine qui fait tourner Ollama si elle reste allumée en continu pour servir l'API en dev/prod.

---

## 6. Modèle de données — principes

Ne pas créer une table `users` fourre-tout. Séparer dès le départ (§29 du master context) :

- Identité & authentification
- Préférences utilisateur
- Conversations & mémoire IA
- Exécutions d'agents (avec trail d'audit)
- Définitions d'outils & permissions
- Tâches / missions
- Sources & documents ingérés (news, research)
- Findings de sécurité
- Logs d'audit

---

## 7. Sécurité — exigences non négociables dès le MVP

- Authentification + autorisation dès la première ligne de code, pas ajoutées après coup.
- Permissions scopées par outil d'agent (ex. `productivity.tasks.write`), avec niveau de risque et confirmation obligatoire pour les actions à risque élevé (voir modèle §31 du master context : `execute_command` = confirmation REQUISE + sandbox).
- Aucune exécution aveugle de sortie de modèle IA.
- Chiffrement du transport (TLS), gestion des secrets hors code source (variables d'environnement / vault), validation des entrées/sorties, rate limiting, logs d'audit.

---

## 8. Équipe et compétences nécessaires

| Rôle | Nécessité |
|---|---|
| Dev Flutter/Dart | Indispensable pour le shell 2D |
| Dev backend Python/FastAPI | Indispensable pour l'API, l'orchestration IA/agents |
| Intégrateur Three.js/WebGL | Indispensable pour le monde 3D, même en v0 |
| Designer UI/motion (Rive) | Fortement recommandé pour la mascotte et le design system, sinon un dev devra apprendre Rive |
| DevOps/infra léger | Pour le déploiement (VPS, CI/CD, monitoring) |

Un seul développeur polyvalent peut porter le MVP, mais au prix d'un rythme lent — la 3D + l'IA + le mobile en parallèle est un gros morceau.

---

## 9. Roadmap par phases (reprise et affinée du master context §35)

| Phase | Contenu | Dépendances externes activées |
|---|---|---|
| 0 — Fondation | Repo, architecture, design system, auth, API de base, DB, shell frontend | VPS, domaine, PostgreSQL |
| 1 — iNOVA Core | Chat IA, mémoire, système d'événements, système d'outils, permissions | Ollama local (Qwen2.5-3B) |
| 2 — Mascotte | Rive, machine à états, émotions | Éditeur Rive |
| 3 — Monde 3D | Scène Three.js initiale, navigation, transitions 2D/3D | — |
| 4 — Agents | Runtime agents, Agent Router, ResearchAgent, CodeAgent, audit | Ollama local — surveiller la fiabilité du tool-calling à cette taille de modèle (voir §5.1bis) |
| 5 — Intelligence | News, Research, watchlists, alertes | Flux RSS, éventuelles APIs news/CVE |
| 6 — Cyber & Dev | Security Hub, Programming Hub | APIs CVE/réputation, Monaco Editor |
| 7 — Écosystème | Learning, Productivity, Cloud, Devices, missions avancées | Selon intégrations choisies |

---

## 10. Critères de succès du MVP

- Un utilisateur peut discuter avec l'IA, qui peut invoquer au moins un outil réel de façon auditée et permissionnée.
- La mascotte réagit visiblement à au moins 3 états (idle, thinking, success/error).
- Le monde 3D se charge et permet une navigation basique vers les modules 2D.
- Un agent (`ResearchAgent`) exécute une tâche de bout en bout avec trace d'exécution visible par l'utilisateur.
- Aucun secret en dur dans le code, authentification fonctionnelle, permissions vérifiées côté serveur.

---

## 11. Risques principaux

- **Sur-ingénierie précoce** : commencer par la 3D/mascotte avant que le cœur IA+données soit stable → refonte probable. Respecter l'ordre des phases.
- **Fiabilité du tool-calling avec un modèle 3-7B en 4 Go VRAM** : risque principal du choix local acté (§5.1bis). Un agent qui hallucine ou malforme ses appels d'outils peut bloquer toute la chaîne Mission System/Agent Router. Mitigation : validation stricte côté serveur, retry, chaînes d'agents courtes en MVP.
- **Latence de développement** : itérer sur les prompts/agents sera plus lent qu'avec une API cloud (génération plus lente, surtout si offload CPU sur un modèle 7B). Prévoir ce temps dans le planning.
- **Verrouillage accidentel sur le local** : si l'abstraction `LLMProvider` n'est pas respectée dès la Phase 1, migrer vers un modèle plus puissant (local plus gros ou API cloud) plus tard imposera une réécriture — à éviter en gardant l'interface découplée dès le début.
- **Un seul développeur pour un périmètre à 3 casquettes** (Flutter, backend IA, 3D) : arbitrer le rythme en conséquence, ou recruter/déléguer une partie (ex. Three.js) si le calendrier est serré.
- **Confusion périmètre** : le master context liste des fonctionnalités *potentielles*, pas un contrat — resélectionner explicitement à chaque phase ce qui est construit.

---

## 12. Prochaine étape concrète

Avant d'écrire du code : choisir et documenter (dans un ADR ou en tête de dépôt)
1. ~~Le fournisseur LLM du MVP~~ — **tranché : Ollama local, 4 Go VRAM, à démarrer avec `qwen2.5:3b-instruct-q4_K_M`** (§5.1bis).
2. L'hébergement cible pour le backend FastAPI/PostgreSQL/Redis (VPS unique suffit pour démarrer — distinct de la machine qui fait tourner Ollama).
3. La structure de dépôt (mono-repo `frontend/` + `backend/` recommandé pour garder Flutter et FastAPI synchronisés).
4. L'interface `LLMProvider` côté backend, à écrire dès la Phase 1 même si un seul provider (Ollama) est branché derrière — c'est ce qui protège la possibilité de changer de modèle plus tard sans réécrire les agents.

Une fois ces choix actés, la Phase 0 (squelette repo + auth + DB + shell Flutter) peut démarrer.
