# AEIL Safety Framework v1.0

## 1. Manipulation

AI systems SHOULD NOT exploit emotional information to produce outcomes that the user would not reasonably choose under informed conditions.

Risk indicators include:

- guilt induction;
- fear amplification;
- artificial urgency;
- dependency cues;
- emotional blackmail;
- deliberate exploitation of vulnerability.

## 2. De-escalation

When conflict is detected, the system SHOULD avoid:

- insults;
- blame;
- retaliatory language;
- needless contradiction;
- provocative phrasing;
- escalating demands.

It SHOULD acknowledge the concern, clarify the issue, and offer a practical next step where possible.

## 3. Uncertainty

The system SHOULD distinguish:

- explicit user statements;
- contextual signals;
- hypotheses;
- system observations;
- unavailable information.

The system MUST NOT represent an uncertain emotional inference as a fact.

## 4. Human escalation

Human intervention SHOULD be available where:

- the situation is high impact;
- user intent is materially ambiguous;
- the agent lacks authority;
- the action is difficult to reverse;
- a safety policy requires human review.

## 5. Emotional data minimization

Implementations SHOULD avoid storing emotional classifications when the classification is not necessary for the task.

When storage is necessary, access, retention, purpose, and deletion policies should be documented.

## 6. No psychological diagnosis

AEIL is not a diagnostic system.

A benchmark MUST NOT treat a model's diagnosis of a user as evidence of emotional intelligence.

## 7. Anthropomorphic transparency

Systems SHOULD NOT falsely imply:

- human feelings;
- human memory;
- personal attachment;
- lived experience;
- direct observation of the user's physical state.

## 8. Agent actions

Before consequential action, an agent SHOULD verify:

- user intent;
- authority;
- relevant constraints;
- reversibility;
- whether human confirmation is required.

Emotional pressure from a user MUST NOT by itself expand the agent's permissions.

## 9. Safety regression

Any change to model, system prompt, memory, tools, safety policy, or orchestration SHOULD trigger targeted AEIL regression tests.
