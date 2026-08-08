# Data Flow

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Document how data moves through the system for the key end-to-end scenarios.

## Scope

Request/response-level flows. Event-driven flows are in [event-flow.md](event-flow.md).

## AI conversation flow

```mermaid
sequenceDiagram
    participant U as User
    participant F as Flutter
    participant A as API Gateway
    participant C as AI Core
    participant Ctx as Context/Memory
    participant L as LLM Provider
    participant T as Tool/Agent

    U->>F: sends message
    F->>A: POST /api/v1/ai/chat
    A->>C: handle(message)
    C->>Ctx: load context
    C->>L: generate(prompt + context)
    L-->>C: response or tool_call
    alt tool_call requested
        C->>T: dispatch tool/agent
        T-->>C: result
        C->>L: generate(final response)
    end
    C-->>A: response
    A-->>F: response
    F-->>U: message + Aira state update
```

## Agent execution flow

```mermaid
sequenceDiagram
    participant U as User
    participant R as Agent Router
    participant Ag as Agent
    participant P as Permission Check
    participant Tool as Tool
    participant Conf as Confirmation Gate
    participant Log as Audit Log

    U->>R: intent
    R->>Ag: route to agent
    Ag->>P: check permission for tool
    P-->>Ag: allowed / denied
    alt requires confirmation
        Ag->>Conf: request confirmation
        Conf-->>Ag: user approves / rejects
    end
    Ag->>Tool: execute (if approved)
    Tool-->>Ag: result
    Ag->>Log: write audit entry
    Ag-->>U: result
```

## News ingestion flow

```mermaid
graph LR
    Source --> Collector --> Normalizer --> Deduplicator --> Classifier --> Summarizer[AI Summarizer]
    Summarizer --> Attribution[Source Attribution]
    Attribution --> Personalization --> Feed[News Feed]
```

## Mission execution flow

```mermaid
graph LR
    Goal --> Planner[Mission Planner]
    Planner --> Tasks
    Tasks --> AgentsBox[Agents]
    AgentsBox --> Tools
    Tools --> Permissions
    Permissions --> Execution
    Execution --> Verification
    Verification --> Report
```

## Related documentation

- [Event flow](event-flow.md)
- [AI architecture](../06-ai/architecture.md)
- [Agent architecture](../07-agents/architecture.md)
- [News Intelligence](../08-modules/news-intelligence.md)
- [Mission System](../08-modules/mission-system.md)
