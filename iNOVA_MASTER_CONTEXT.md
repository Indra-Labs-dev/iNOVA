# iNOVA — Project Context & Master Brief

> **Document purpose:** This file is the canonical context document to provide to Claude AI before implementing, refactoring, or making architectural decisions for iNOVA.
>
> **Project status:** Concept / architecture definition phase.
>
> **Important:** Do not treat this document as permission to implement everything at once. Build iNOVA incrementally, preserving architecture, security, maintainability, and UX quality.

---

# 1. Vision

## iNOVA — Intelligent Digital Universe

iNOVA is an ambitious AI-powered digital environment combining:

- Artificial Intelligence
- Autonomous / semi-autonomous AI agents
- Cybersecurity
- Programming and developer tooling
- Research and web intelligence
- News aggregation and analysis
- OSINT / public-source intelligence
- Learning
- Productivity
- Device and infrastructure management
- A futuristic 2D/3D interface
- An evolving AI mascot / digital companion
- Gamification and progression

The goal is **not** to build a collection of unrelated tools.

The goal is to create a coherent **Digital Operating Environment** where all capabilities communicate through a shared core.

### Core vision

> **iNOVA is an intelligent digital universe that learns, researches, creates, protects, automates, and evolves with its user.**

The user should feel like they are interacting with a living digital environment rather than navigating a conventional dashboard.

---

# 2. Product Objectives

iNOVA should pursue five major objectives.

## Objective 1 — Exceptional UX

Create a visually distinctive interface combining:

- futuristic UI
- 2D interfaces
- interactive 3D environments
- holographic visual language
- particles and depth
- smooth transitions
- contextual animations
- interactive mascot

The visual layer must remain functional and must never compromise usability.

## Objective 2 — AI beyond chat

The AI should not be limited to a chatbot.

It should be capable of:

- reasoning
- retrieving information
- using tools
- calling application services
- analyzing data
- executing permitted workflows
- collaborating with specialized agents
- maintaining contextual memory
- explaining its decisions/actions

## Objective 3 — Personalization

iNOVA should progressively adapt to its user:

- interests
- preferences
- workflows
- frequently used modules
- learning progression
- productivity patterns
- preferred AI behavior

Personalization must respect privacy and explicit permissions.

## Objective 4 — Unified ecosystem

Cybersecurity, programming, research, news, agents, learning, productivity, etc. should not behave like separate applications.

They should share:

- authentication
- permissions
- events
- AI context
- memory
- notifications
- user profile
- design system
- search
- activity history

## Objective 5 — Extensibility

iNOVA must be designed as a platform.

New modules and agents should be addable without rewriting the core.

---

# 3. High-Level Product Map

```text
                         iNOVA
                           |
                  +--------+--------+
                  |                 |
               AI CORE          iNOVA WORLD
                  |                 |
          +-------+-------+     +---+---+
          |       |       |     |       |
       Agents   Memory  Tools   2D      3D
          |
   +------+-------------------------------+
   |      |       |       |       |       |
 Cyber   Code    News   Research Learn Productivity
   |      |       |       |       |       |
   +------+-------+-------+-------+-------+
                  |
             iNOVA CORE
                  |
      +-----------+-----------+
      |           |           |
   Events      Identity     Data
      |           |           |
    Redis       Auth      PostgreSQL
```

---

# 4. Main Product Modules

## 4.1 AI Hub

The AI Hub is the central conversational and intelligence layer.

Capabilities may include:

- text conversation
- multimodal interaction
- document analysis
- summarization
- translation
- reasoning
- content generation
- contextual recommendations
- memory
- tool use
- agent orchestration

The architecture must support multiple AI providers/models where practical.

Avoid hard-coding the product around a single model provider.

---

# 5. Agent Hub

Agents are specialized AI workers.

Potential agents:

- `ResearchAgent`
- `NewsAgent`
- `CyberAgent`
- `CodeAgent`
- `OSINTAgent`
- `TutorAgent`
- `DataAgent`
- `CloudAgent`
- `WriterAgent`
- `ProductivityAgent`

An agent should have:

```text
Agent
├── identity
├── purpose
├── capabilities
├── tools
├── permissions
├── memory/context
├── execution policy
├── status
└── audit trail
```

## Agent orchestration

iNOVA should eventually include an orchestrator/router:

```text
User
  |
iNOVA Core
  |
Agent Router
  |
+---------+---------+---------+
|         |         |         |
Cyber    Code    Research   Data
Agent    Agent     Agent     Agent
|         |         |         |
+---------+---------+---------+
          |
       Result
          |
        User
```

Agents may collaborate, but high-impact actions must require explicit authorization when appropriate.

### Important agent principle

**An AI agent must never automatically gain unrestricted access to the user's system, files, network, credentials, or external services.**

Use:

- scoped permissions
- tool allowlists
- confirmation gates
- sandboxing where possible
- audit logs
- rate limits
- clear action previews

---

# 6. Cybersecurity Hub

Cybersecurity is a first-class module.

Possible capabilities:

- device security analysis
- application permission analysis
- process analysis
- network analysis
- port/service visibility
- configuration checks
- vulnerability intelligence
- CVE lookup
- security recommendations
- file analysis
- URL/domain reputation
- threat intelligence
- security alerts
- security reports
- security posture score

Example:

```text
iNOVA SECURITY

Security Score: 94/100

[OK] Device
[OK] Network
[WARN] Applications
[OK] Accounts
[CRITICAL] Vulnerabilities
```

## Security boundaries

Security capabilities must be designed around:

- authorized systems
- defensive analysis
- passive/public intelligence
- explicit user ownership or authorization
- safe execution boundaries

Do not turn iNOVA into an unrestricted offensive automation platform.

---

# 7. Programming Hub

The Programming Hub is an AI-assisted developer environment.

Potential features:

- code editor
- project explorer
- terminal
- Git integration
- GitHub integration
- code generation
- refactoring
- debugging
- testing
- static analysis
- dependency analysis
- documentation
- architecture assistance
- API testing
- Docker workflows
- CI/CD assistance
- code review
- security-aware development

For web-based code editing, consider **Monaco Editor**.

The Programming Hub should communicate with CodeAgent and CyberAgent.

Example workflow:

```text
User:
"Analyze my API security."

CodeAgent
    |
    +--> inspect project
    +--> inspect dependencies
    +--> inspect relevant code
    |
CyberAgent
    |
    +--> security analysis
    +--> vulnerability classification
    +--> recommendations
    |
CodeAgent
    |
    +--> propose fixes
    +--> generate tests
    |
Review
    |
    +--> verify changes
```

All code changes should be reviewable and reversible.

---

# 8. Research & Intelligence Hub

iNOVA should be capable of collecting, processing, and synthesizing information from permitted public sources.

Potential sources:

- official APIs
- RSS feeds
- public web pages where permitted
- public documentation
- public datasets
- uploaded documents

Prefer official APIs and RSS when available.

Respect:

- robots.txt where applicable
- terms of service
- rate limits
- copyright
- authentication requirements
- source attribution

Do not build systems intended to bypass anti-bot protections or access controls.

---

# 9. News Intelligence

News should be more than a feed.

Pipeline:

```text
Sources
   |
Collection
   |
Normalization
   |
Deduplication
   |
Classification
   |
AI summarization
   |
Source cross-checking
   |
Personalization
   |
iNOVA News Feed
```

Possible categories:

- AI
- cybersecurity
- programming
- technology
- startups
- science
- gaming
- local news
- economy
- user-defined topics

## Personalized digest

Example:

```text
iNOVA MORNING INTELLIGENCE

AI
5 important updates

Cybersecurity
3 important updates

Development
4 important updates

iNOVA Recommendation:
"This story is especially relevant to your current interests."
```

News should retain source links and publication dates.

AI summaries must clearly distinguish between:

- source facts
- inference
- opinion
- uncertainty

---

# 10. OSINT / Public Intelligence Hub

Potential functionality:

- DNS information
- public certificate information
- domain metadata
- public technology information
- public GitHub information
- public reputation information
- public threat intelligence
- public news correlation

The feature is intended for legitimate research, defensive security, investigation, and authorized assessment.

Do not design it around unauthorized access or exploitation.

---

# 11. Knowledge Graph

A future iNOVA capability should connect information semantically.

Example:

```text
Flutter
 |
+-- Dart
+-- Android
+-- iOS
+-- Firebase
+-- Version X
+-- Article A
+-- Article B
```

The graph can help answer questions such as:

> "What technologies related to Flutter changed recently?"

The knowledge layer may combine:

- entities
- relationships
- documents
- events
- user interests
- agent findings

---

# 12. Watchlists & Intelligent Alerts

Users should be able to monitor topics.

Example:

```text
MY WATCHLISTS

Cybersecurity
- CVE
- OWASP
- major security events

AI
- AI models
- major providers
- local LLMs

Development
- Flutter
- Python
- FastAPI
- Docker

Custom
- user-defined keywords
```

Instead of flooding the user with notifications, iNOVA should aggregate and prioritize information.

Example:

```text
iNOVA found 37 new items.

3 require your attention:

[CRITICAL] Security vulnerability
[IMPORTANT] Flutter update
[TRENDING] New AI model
```

---

# 13. Learning Hub

Potential features:

- learning paths
- courses
- explanations
- exercises
- quizzes
- progress tracking
- adaptive difficulty
- personalized recommendations
- AI tutor
- knowledge review

The mascot can act as the user's learning companion.

---

# 14. Productivity Hub

Potential features:

- tasks
- calendar
- notes
- goals
- reminders
- habits
- focus sessions
- project management
- personal planning

Example:

> "Organize my day."

iNOVA can inspect permitted calendar/task context, propose a schedule, and ask for confirmation before creating or modifying important records.

---

# 15. Device Hub

Potential future integration with user-owned devices:

```text
             iNOVA
                |
      +---------+---------+
      |         |         |
     Phone      PC       Server
      |         |         |
      +---------+---------+
                |
           Device Hub
```

Possible information:

- CPU
- RAM
- storage
- battery
- network
- processes
- applications
- system information
- security status

Device access must be permission-based.

---

# 16. Cloud / Infrastructure Hub

Potential integration with:

- Docker
- servers
- virtual machines
- databases
- APIs
- logs
- monitoring
- backups
- deployments

iNOVA should be able to explain infrastructure problems and suggest fixes.

Avoid destructive automation by default.

---

# 17. iNOVA World — 3D Environment

The frontend must use:

> **Three.js / WebGL for the 3D layer.**

This is an explicit architectural decision.

Do not replace Three.js with Unity unless a future architectural decision explicitly requires it.

## Concept

The interface is a digital world.

```text
                 iNOVA WORLD

                     NOVA

        Cyber             AI
          |               |
       Security         Intelligence

     Code                 Agents

       Learning         Productivity
```

The 3D world can contain:

- planet / world
- futuristic buildings
- holographic interfaces
- portals
- particles
- floating objects
- data streams
- interactive environments
- visual representations of modules

## 3D technology direction

Use:

- Three.js
- WebGL
- GLTF/GLB
- shaders where justified
- particle systems
- post-processing where justified

3D must be performance-conscious.

Do not build a huge 3D environment before the underlying product is functional.

---

# 18. 2D Frontend

Primary application frontend:

> **Flutter**

Flutter handles:

- application shell
- navigation
- 2D interface
- dashboards
- forms
- settings
- cards
- data views
- responsive layout
- API integration
- WebSocket integration

The 3D layer is specialized and should not force every screen to become 3D.

---

# 19. Mascot

iNOVA needs an intelligent mascot / digital companion.

The mascot is not decorative.

It is part of the UX.

Possible states:

```text
idle
welcome
thinking
listening
speaking
working
success
joy
error
warning
waiting
loading
incoming_event
```

The mascot should react to:

- AI state
- task completion
- errors
- alerts
- achievements
- user interactions
- important events

## Animation technology

Use:

- **Rive** for interactive mascot state machines
- **Lottie** for selected effects
- SVG where appropriate
- 3D assets where appropriate

The mascot should have a dedicated state machine.

Example:

```text
AI_THINKING
      |
      v
Mascot -> THINKING

AI_SUCCESS
      |
      v
Mascot -> JOY
```

---

# 20. Gamification

iNOVA may include:

- XP
- levels
- streaks
- missions
- achievements
- unlockable visual elements
- mascot customization
- world evolution

Example:

```text
NOVA LEVEL 17

12,450 XP

[██████████████░░░] 82%

Achievements:
- First Mission
- Cyber Guardian
- AI Explorer
- World Builder
```

Gamification should encourage useful behavior, not manipulate the user.

---

# 21. Mission System

A major future feature.

The user gives iNOVA a goal.

Example:

> "Secure my project."

The system creates a structured plan:

```text
MISSION
 |
+-- Analyze code
+-- Analyze dependencies
+-- Security checks
+-- Tests
+-- Proposed fixes
+-- Verification
+-- Report
```

The mission can involve multiple agents.

The user should be able to inspect:

- plan
- current step
- agent involved
- tools used
- results
- pending confirmations
- errors
- final report

---

# 22. iNOVA Pulse

A visual real-time intelligence center.

It can represent:

- new news
- AI trends
- cybersecurity alerts
- development updates
- active agents
- tasks
- system events

Example:

```text
                 iNOVA PULSE

          127 new items collected

       AI       CYBER       DEV
       +12        +8         +21
      trends    alerts     updates
```

The 3D world may react visually to important events.

---

# 23. Design Language

The visual identity should be:

- futuristic
- premium
- clean
- immersive
- intelligent
- slightly cyberpunk
- readable
- accessible

Avoid making the UI look like a generic "neon hacker" dashboard.

The futuristic aesthetic should be supported by strong UX and hierarchy.

Suggested starting palette:

```text
Deep Space      #07111F
Electric Blue   #0066FF
Cyan            #20D9FF
Purple          #8B5CFF
Neon Orange     #FF5A1F
White           #F5F8FF
```

These are starting values, not immutable brand rules.

---

# 24. Frontend Stack

## Primary

- Flutter
- Dart
- Riverpod
- Rive
- Lottie

## 3D

- Three.js
- WebGL
- GLTF/GLB

## Code editor

- Monaco Editor where appropriate for web-based developer tooling

## Real-time

- WebSocket

## Backend communication

- REST API
- WebSocket
- potentially WebRTC for future real-time communication features

---

# 25. Frontend Architecture

Suggested Flutter structure:

```text
lib/
|
+-- core/
|   +-- routing/
|   +-- theme/
|   +-- networking/
|   +-- storage/
|   +-- permissions/
|   +-- design_system/
|
+-- features/
|   +-- ai/
|   +-- agents/
|   +-- cybersecurity/
|   +-- programming/
|   +-- news/
|   +-- osint/
|   +-- learning/
|   +-- productivity/
|   +-- cloud/
|   +-- devices/
|
+-- nova/
|   +-- mascot/
|   +-- personality/
|   +-- emotions/
|   +-- state_machine/
|
+-- world/
|   +-- scene/
|   +-- objects/
|   +-- camera/
|   +-- effects/
|   +-- interactions/
|
+-- shared/
    +-- widgets/
    +-- animations/
    +-- components/
```

Avoid giant files.

A feature should be split into small, cohesive components.

---

# 26. iNOVA Design System

Create a centralized design system rather than scattering visual constants.

Potential components:

```text
iNovaColors
iNovaTypography
iNovaSpacing
iNovaRadius
iNovaShadows
iNovaGlass
iNovaMotion
```

UI components:

```text
NovaCard
NovaButton
NovaPanel
NovaGlass
NovaOrb
NovaHologram
NovaMetric
NovaBadge
NovaDialog
NovaCommandBar
NovaAgentCard
```

This is critical for consistency.

---

# 27. Animation System

Centralize motion rules.

```text
iNOVA Motion

Micro
- hover
- press
- fade
- scale

Interface
- page transition
- modal
- panel
- navigation

World
- camera
- particles
- hologram
- portal

Mascot
- idle
- emotion
- interaction
- reaction
```

Animations should be purposeful and respect reduced-motion accessibility settings where possible.

---

# 28. Backend Direction

The frontend must remain independent from backend implementation details.

A likely backend architecture:

```text
Flutter / Web Frontend
          |
      API Gateway
          |
        FastAPI
          |
 +--------+--------+--------+
 |        |        |        |
AI Core  Agents  Modules  Events
 |        |        |        |
LLM     Runtime  Services Redis
          |
      PostgreSQL
```

Potential backend technologies:

- Python
- FastAPI
- PostgreSQL
- Redis
- background workers
- WebSocket
- object storage
- AI model providers
- local LLM support where appropriate

These are architectural directions, not permission to add unnecessary dependencies.

---

# 29. Data Architecture Principles

The system should separate:

- identity
- user preferences
- conversations
- AI memory
- agent executions
- tools
- permissions
- tasks
- news
- sources
- documents
- security findings
- projects
- audit logs

Prefer normalized domain models over one giant "user data" table.

---

# 30. Security Principles

Security is a core product requirement.

Implement from the beginning:

- authentication
- authorization
- scoped permissions
- secure sessions
- encrypted transport
- secret management
- input validation
- output validation
- audit logging
- rate limiting
- agent permission boundaries
- tool allowlists
- confirmation gates
- safe defaults
- data deletion controls

AI agents must be treated as potentially untrusted decision-makers.

Never blindly execute arbitrary model output.

---

# 31. AI Agent Safety Model

Every tool should have an explicit capability definition.

Example:

```text
Tool: create_task

Permission:
  productivity.tasks.write

Risk:
  LOW

Confirmation:
  optional
```

Example:

```text
Tool: execute_command

Permission:
  system.command.execute

Risk:
  HIGH

Confirmation:
  REQUIRED

Sandbox:
  REQUIRED where possible
```

The system should maintain an audit trail:

```text
User request
   |
Agent decision
   |
Tool selected
   |
Permission check
   |
Confirmation
   |
Execution
   |
Result
   |
Audit log
```

---

# 32. Development Principles for Claude

Claude must follow these principles while working on iNOVA:

1. **Understand before modifying.**
2. Inspect existing architecture before creating new files.
3. Do not rewrite functioning systems without a clear reason.
4. Prefer small, isolated changes.
5. Avoid giant source files.
6. Keep modules cohesive.
7. Use typed models and explicit interfaces.
8. Separate UI, business logic, data access, and infrastructure.
9. Do not duplicate functionality.
10. Do not introduce dependencies without justification.
11. Do not expose secrets in source code.
12. Add tests for meaningful business logic.
13. Preserve backward compatibility where possible.
14. Run relevant tests after changes.
15. Fix root causes rather than hiding symptoms.
16. Document important architectural decisions.
17. Do not implement speculative features merely because they are listed in this document.
18. Treat this document as the product vision and architectural context, not as a command to build the entire roadmap immediately.

---

# 33. Development Workflow

For each significant feature:

```text
1. Inspect
2. Understand
3. Plan
4. Define architecture
5. Implement smallest viable slice
6. Test
7. Review
8. Refactor
9. Document
10. Continue
```

For UI work:

```text
Design
  |
Component
  |
Interaction
  |
Animation
  |
Accessibility
  |
Responsive behavior
  |
Test
```

For AI/agent work:

```text
Capability
  |
Tool definition
  |
Permission model
  |
Agent behavior
  |
Failure handling
  |
Auditability
  |
Test
```

---

# 34. MVP Recommendation

Do NOT attempt to build every module initially.

The first MVP should prove the central concept.

Recommended MVP:

```text
iNOVA MVP
|
+-- 🤖 AI Companion
|     +-- Chat
|     +-- Basic memory
|     +-- Tool system
|
+-- 🌌 Futuristic Dashboard
|     +-- 2D UI
|     +-- Initial 3D world
|
+-- 🧬 Mascot
|     +-- Rive
|     +-- Basic emotional states
|
+-- 🤖 Agent Hub
|     +-- ResearchAgent
|     +-- CodeAgent
|
+-- 📰 News Intelligence
|     +-- RSS/API ingestion
|     +-- AI summarization
|
+-- 🛡️ Basic Security Hub
|     +-- security posture
|     +-- recommendations
|
+-- 🎯 Missions
      +-- simple tasks
      +-- XP
```

The MVP goal is to prove:

> **AI + Agent + Data + Mascot + 2D/3D interface can operate as one coherent experience.**

---

# 35. Future Roadmap

## Phase 0 — Foundation

- repository
- architecture
- design system
- authentication
- core API
- database
- frontend shell

## Phase 1 — iNOVA Core

- AI chat
- memory
- event system
- tool system
- permissions

## Phase 2 — Mascot

- Rive
- state machine
- emotions
- contextual reactions

## Phase 3 — World

- Three.js/WebGL
- initial 3D scene
- navigation
- interactive objects
- 2D/3D transitions

## Phase 4 — Agents

- agent runtime
- Agent Router
- ResearchAgent
- CodeAgent
- tool permissions
- audit system

## Phase 5 — Intelligence

- News
- Research
- watchlists
- intelligent alerts
- knowledge graph

## Phase 6 — Cyber & Dev

- CyberSecurity Hub
- Programming Hub
- security-aware coding workflows

## Phase 7 — Ecosystem

- Learning
- Productivity
- Cloud
- Devices
- advanced missions
- advanced personalization

---

# 36. Success Criteria

iNOVA should eventually achieve:

### UX

- instantly recognizable visual identity
- fast interactions
- coherent 2D/3D experience
- accessible interface
- responsive layouts

### AI

- contextual conversations
- reliable tool use
- useful memory
- transparent agent actions

### Agents

- specialized agents
- controlled permissions
- observable execution
- recoverable failures

### Data

- high-quality source ingestion
- deduplication
- source attribution
- useful summaries
- personalized intelligence

### Security

- secure architecture
- least privilege
- auditable actions
- explicit consent for sensitive operations

### Engineering

- modular architecture
- strong tests
- maintainable code
- clear documentation
- reproducible development environment

---

# 37. Key Product Philosophy

The most important principle:

> **iNOVA should feel alive without pretending to be alive.**

The mascot can be expressive.

The world can react.

The AI can be conversational.

The interface can evolve.

But the product must remain:

- predictable
- transparent
- controllable
- secure
- respectful of user privacy

The futuristic experience should never obscure what the system is doing.

---

# 38. Final Instruction to Claude

When working on iNOVA:

> **Do not treat this project as a simple Flutter application.**
>
> Treat it as a modular AI platform with a futuristic interactive frontend.
>
> The central architectural pillars are:
>
> **iNOVA Core + AI + Agents + Data Intelligence + Cybersecurity + Programming + 2D UI + Three.js/WebGL 3D + Rive Mascot + Events + Security.**
>
> Build incrementally.
>
> Prioritize architecture and maintainability before visual complexity.
>
> Keep the 3D layer specialized.
>
> Keep AI agents permission-controlled.
>
> Keep the frontend independent from backend implementation details.
>
> Prefer small composable modules over monolithic files.
>
> Before implementing a new major feature, inspect the existing project and explain how it fits into the architecture.
>
> Never sacrifice security, accessibility, performance, or maintainability merely to create a flashy demo.

---

## End of iNOVA Master Context
