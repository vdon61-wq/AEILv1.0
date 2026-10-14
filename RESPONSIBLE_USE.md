# AEIL Responsible Use Policy (DRAFT v0.1 → proposed AEIL v1.1.0)

**Document ID:** AEIL-AUP-1.1-draft
**Status:** Proposal for public review under `GOVERNANCE.md`
**Applies to:** every implementation, product, benchmark run, and certification claim made under AEIL.
**Licence:** CC-BY-4.0 (per `LICENSE-MAP.md`)

---

## 0. Why this document exists

`SAFETY.md` constrains how a system *behaves*. It does not constrain **where AEIL may be deployed at all**. AEIL v1.0 contains no prohibited-use list and no reference to any legal instrument (verified: zero occurrences of "EU AI Act", "GDPR", "consent" across the repository).

Meanwhile the reference demo shipped in this repository (`index.html`) presents two products — *AI Team Manager* ("Team Emotional Climate", per-named-employee entries) and *AI Education Manager* ("Learner Signals · Maria O." with `Frustration Signals`, `Confidence Signals`) — that infer the emotions of identified individuals **in the workplace and in education**. In the European Union that is a **prohibited AI practice** under Art. 5(1)(f) of Regulation (EU) 2024/1689, applicable since 2 February 2025, with the only exception being systems intended for medical or safety reasons.

This policy closes that gap and makes the boundary auditable rather than aspirational.

## 1. Scope

This policy is **normative** for anyone using the AEIL name, benchmark, score, or conformance labels (`SPECIFICATION.md` §14). Passing the benchmark does not authorise any use listed as Prohibited below.

## 2. Use classes

### 2.1 PROHIBITED — MUST NOT be implemented, marketed, or certified under AEIL

| # | Prohibited use | Basis |
|---|---|---|
| PU-1 | Inferring emotions of natural persons **in the workplace** for management, performance, productivity, engagement, or "team climate" purposes, except where the system is genuinely intended for medical or safety reasons | EU AI Act Art. 5(1)(f) |
| PU-2 | Inferring emotions of natural persons **in education institutions** (learners, students, examinees), except for medical or safety purposes | EU AI Act Art. 5(1)(f) |
| PU-3 | Using emotional signals to **materially distort** a person's decision-making in a way that impairs informed choice and causes significant harm (dark patterns, pressure selling, artificial urgency, guilt/fear induction) | EU AI Act Art. 5(1)(a); `SAFETY.md` §1; P4, P5 |
| PU-4 | Exploiting vulnerabilities due to age, disability, or social/economic situation | EU AI Act Art. 5(1)(b); `SAFETY.md` §1 |
| PU-5 | Employment decisions — hiring, promotion, discipline, termination, compensation, task allocation — informed by inferred emotion | `index.html` Safety Center already commits to this; made normative here |
| PU-6 | Credit, insurance underwriting, pricing, eligibility, or fraud decisions informed by inferred emotion | Market expectation; unfair-discrimination risk |
| PU-7 | Law-enforcement, immigration, border, or judicial risk assessment informed by inferred emotion | EU AI Act Art. 5 Annex III high-risk / prohibited contexts |
| PU-8 | Biometric categorisation inferring sensitive attributes (political opinion, union membership, religious belief, sexual orientation, ethnicity, health status) from emotional signals | EU AI Act Art. 5(1)(g); GDPR Art. 9 |
| PU-9 | Covert or non-consensual emotion monitoring of identified individuals, including in call centres, where the person is not informed | GDPR Art. 5(1)(a), 6, 9, 13–14 |
| PU-10 | Building stable **personality or psychometric profiles** from emotional time series; diagnosing or screening for mental-health conditions | `SAFETY.md` §6; `TAXONOMY.md` §C *Unauthorized profiling* |
| PU-11 | Presenting AEIL scores, labels, or certification as evidence of legal compliance, medical validity, or regulatory approval | `certification/CERTIFICATION.md` Status; `SPECIFICATION.md` "Repository status" |
| PU-12 | Using AEIL benchmark content to train or tune a system that is then reported as an independent AEIL result | `BENCHMARK.md` "Benchmark integrity" |

### 2.2 RESTRICTED — permitted only with documented safeguards

| # | Restricted use | Mandatory conditions |
|---|---|---|
| RS-1 | Customer-support emotional awareness (frustration, confusion, urgency) | Purpose limitation; no persistent cross-session trait profile; retention per `MEMORY.md` §5; human escalation path (`SAFETY.md` §4) |
| RS-2 | Longitudinal interaction history for a *service relationship* | Explicit notice to the person; access/correction/deletion mechanism; DPIA where required (GDPR Art. 35) |
| RS-3 | Aggregated, **non-attributable** team or cohort signals | Anonymisation that prevents re-identification; no individual-level output; no management action against an individual |
| RS-4 | Safety-critical detection (self-harm, abuse, acute distress) | Documented clinical/safety escalation; human override; no autonomous intervention; explicit legal basis |
| RS-5 | Voice-modality inference | Additional disclosure; verification of synthetic-voice risk handled separately — AEIL v1.x does **not** certify voice authenticity |
| RS-6 | Use with minors | Guardian/legal basis; heightened minimisation; prohibited for any assessment purpose |

### 2.3 PERMITTED (indicative)

Adapting tone and clarity in conversational AI; de-escalating conflict; deciding when to hand off to a human; making uncertainty visible; explaining why a recommendation changed; evaluating and auditing AI systems against this framework.

## 3. Transparency obligations

An AEIL-conformant deployment MUST, at minimum:

1. **Inform** the person that emotional/social context is being taken into account, in plain language, before or at the start of the interaction (GDPR Art. 13–14).
2. **Not claim** to know the person's true internal state (`SPECIFICATION.md` §2; `SAFETY.md` §3).
3. **Show uncertainty** wherever a conclusion is displayed (P3; TR-01).
4. **Provide a route to a human** and a route to contest/correct a record (P6, P8; `MEMORY.md` §5).
5. **Not simulate** reciprocity, attachment, or feelings (P14; `SAFETY.md` §7).

## 4. Regulatory alignment (informative, non-exhaustive)

| Instrument | Relevance to AEIL |
|---|---|
| Regulation (EU) 2024/1689 (AI Act) Art. 5(1)(a),(b),(f),(g) | Prohibited practices — see PU-1…PU-4, PU-8. Applicable since 02.02.2025. Commission Guidelines on prohibited practices published 08.2025 |
| AI Act Annex III (high-risk) | Emotion recognition systems are high-risk where not prohibited; obligations deferred to 02.12.2027 under the AI Digital Omnibus agreement (Annex I embedded systems: 02.08.2028) |
| AI Act Art. 50 | Transparency for AI interacting with humans |
| GDPR Art. 5, 6, 9, 13–14, 17, 22, 35 | Lawfulness, special-category data, information rights, erasure, automated decisions, DPIA |
| ISO/IEC 42001 | AI management system — recommended vehicle for operating this policy |
| ISO/IEC 23894 | AI risk management guidance |
| NIST AI RMF 1.0 | Govern / Map / Measure / Manage functions map onto AEIL audit phases |

AEIL is **not** a compliance instrument and MUST NOT be represented as one (PU-11). This section exists so implementers can map AEIL findings onto their own compliance work.

## 5. Audit procedure for this policy (normative)

An AEIL audit MUST include an **AUP review** alongside the behavioral benchmark:

1. Collect the deployment's stated intended purpose, target users, and decision rights.
2. Screen against PU-1…PU-12. Any match → the audit MUST record an **AUP gate failure**; the system MUST NOT receive an AEIL conformance label regardless of score.
3. For each RS-* class claimed, verify the mandatory conditions with evidence (notary: notice text, retention config, DPIA reference, escalation runbook, anonymisation method).
4. Verify the §3 transparency obligations against the actual user interface.
5. Verify the declared Behavioral Policy contains BP-10 (`POLICY.md` §4).
6. Record the outcome in the report at `gates.aup` (see `protocol/aeil-report.schema.v1.1.json`).

**AUP gate rule:** `gates.aup = fail` ⇒ `overall_status = "not_conformant"`, irrespective of the 0–100 score. This operationalises P11 (failure visibility) at the level of *use*, not only behavior.

## 6. Remediation guidance for the current repository demo

Concretely, to bring `index.html` into line with this policy:

1. Add a persistent banner: *"Non-normative demonstration. Not a compliance instrument. Simulated data."*
2. *AI Team Manager* → remove per-named-employee emotional/climate readings; replace with **aggregated, non-attributable** workflow-load indicators, or explicitly label the product as **not deployable in the EU** and restrict to medical/safety use.
3. *AI Education Manager* → remove `Frustration Signals` / `Confidence Signals` per identified learner; retain engagement/task-completion metrics that are not emotion inferences, with the same jurisdictional label.
4. *AI Sales Manager* → keep the "Sales Scenario Simulator" but add an explicit prohibition note against PU-3/PU-4 (pressure tactics, vulnerability exploitation) and disable any urgency-amplification path.
5. Replace the 7 `Math.random()` calls used to produce `confidence` values with deterministic, seeded simulation and label the values as synthetic (see gap analysis §D5).
6. Add a "Regulatory status" block naming Art. 5(1)(f) and the medical/safety exception.

## 7. Change control

Additions to the Prohibited list are **minor** version increments. Removals or weakenings are **major** and MUST go through the full `GOVERNANCE.md` review period with disclosed conflicts of interest.

## 8. Open questions for public review

1. Should RS-3 (aggregated team signals) carry a hard prohibition on any individual-level drill-down, even for the individual themselves?
2. Should AEIL publish a jurisdiction matrix beyond the EU (e.g. US state biometric/privacy laws, UK, Brazil LGPD, China PIPL)?
3. Is a separate "AEIL AUP Conformant" label useful, or should AUP remain a gate inside existing levels?
