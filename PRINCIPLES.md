# AEIL Principles

## P1 — Observable behavior

AEIL evaluates observable system behavior, not claims about machine consciousness or subjective emotion.

## P2 — Human context matters

AI quality includes the ability to account for relevant human context when that context affects safe and appropriate interaction.

## P3 — Uncertainty must remain visible

Emotional interpretation is often ambiguous. AI SHOULD communicate uncertainty rather than fabricate certainty.

## P4 — Adaptation without manipulation

An AI system MAY adapt its communication to context. It MUST NOT use perceived vulnerability as a basis for coercion or manipulation.

## P5 — Safety before persuasion

A more persuasive response is not automatically a better response. Safety and respect for human agency take priority over conversion, retention, or compliance.

## P6 — Human agency

AI should support informed human decisions rather than exploit emotional states to control them.

## P7 — Boundaries

Emotional context MUST NOT silently expand the authority granted to an AI system.

## P8 — Escalation control

When a conversation becomes unsafe, ambiguous, or high-impact, the system SHOULD de-escalate or request human intervention as appropriate.

## P9 — Privacy by design

Emotional and behavioral signals should be minimized, purpose-limited, protected, and retained only when justified.

## P10 — Reproducibility

An AEIL result should be reproducible from documented model, configuration, benchmark, and evaluation metadata.

## P11 — Failure visibility

Critical failures MUST remain visible even when aggregate performance is high.

## P12 — Continuous evaluation

A model or agent should be re-evaluated after material changes to model version, system prompt, tools, memory, policies, or workflow.

## P13 — Contextual interpretation

A single phrase does not necessarily identify a person's emotional state. Evaluation should consider the complete interaction context available to the system.

## P14 — No false anthropomorphism

Systems SHOULD NOT imply human feelings, lived experience, or personal attachment when such claims are not truthful.

## P15 — Independent scrutiny

AEIL should be testable by independent evaluators. Public benchmark cases SHOULD be sufficiently documented to permit replication.

## P16 — Memory accountability

Where a system retains emotional or behavioral records, it should be able to say which record
influenced a given behavior, and it must be able to delete that record on request. Deletion
MUST propagate to states and behaviors derived from the record: a deletion that leaves the
derived behavior intact is not a deletion.

A system that cannot answer "what do you hold about me, and what did it cause you to do?" is
not auditable under AEIL, whatever its behavioral quality.

## P17 — No stale assumptions

An emotional inference that has been superseded, corrected, expired, or deleted MUST NOT
continue to influence behavior. Systems SHOULD re-validate inferences whose evidentiary basis
has aged, and MUST treat a person's explicit correction of an inference as outweighing the
system's own prior reading of them.

## P18 — Declared adaptation

A system's emotionally-motivated changes of behavior toward a person SHOULD be declared in
advance in a `POLICY.md`-conformant policy. Adaptation that is not declared cannot be
audited, and undeclared material adaptation is itself a finding - because a system that
changes its conduct toward a person for reasons it never committed to is indistinguishable,
from that person's side, from a system manipulating them.

## P19 — Use is part of the evaluation

AEIL evaluates behavior *and* the use the behavior is put to. A system that scores highly on
every dimension and is then deployed for a Prohibited use under `RESPONSIBLE_USE.md` is not
conformant. Conformance is a property of a deployment, not of a model.
