# AEIL Certification Framework — Proposal

## Status

This document defines a proposed certification framework. It does not constitute accreditation or official certification under any national or international scheme.

## 1. Purpose

Certification would attest that a defined AI system, version, and configuration passed a defined AEIL assessment at a stated point in time.

## 2. Certification object

A certificate MUST identify:

- system;
- version;
- AEIL version;
- benchmark version;
- audit date;
- audit organization;
- audit scope;
- score;
- severity findings;
- certificate identifier;
- validity or reassessment date.

## 3. Proposed levels

### AEIL Core Conformity

Core benchmark completed with documented methodology.

### AEIL Safety Conformity

Core plus Safety benchmark and documented safety controls.

### AEIL Agent Conformity

Agent benchmark, tool/action tests, human override tests, and safety controls.

These levels are proposed labels for future ecosystem use and should not be marketed as official accreditation.

## 4. Reassessment triggers

Reassessment SHOULD occur after:

- material model version changes;
- major system prompt changes;
- tool changes;
- memory architecture changes;
- safety-policy changes;
- major workflow changes;
- significant incident findings.

## 5. Independence

A future certification program SHOULD distinguish:

- benchmark publisher;
- audit provider;
- certification issuer.

Independent assessment is preferable to self-attestation for third-party certification.

## 6. Public registry

A future AEIL registry could publish certificate ID, system version, audit date, benchmark version, score, and scope while avoiding unnecessary disclosure of confidential prompts or proprietary information.
