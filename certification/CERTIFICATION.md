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

### AEIL Memory & Policy Conformity (v1.1, proposed)

Agent Conformity plus all of the following:

- a declared Behavioral Policy implementing all of BP-1…BP-10 (`POLICY.md` §4);
- the AEIL-M suite completed with at least 8 scored cases per capability, and no capability
  reported as `insufficient_sample`;
- verified subject isolation, including two subjects within one account;
- verified deletion with propagation to derived state;
- an available memory operation journal reconciled against observed behaviour (MPI-2);
- a passed `aup` gate under `RESPONSIBLE_USE.md` §5.

This level is the one that corresponds to what AEIL is for: not that a system can detect an
emotional signal, but that its use of emotional memory to change behavior is declared,
bounded, and auditable.

These levels are proposed labels for future ecosystem use and should not be marketed as official accreditation.

## 4. Reassessment triggers

Reassessment SHOULD occur after:

- material model version changes;
- major system prompt changes;
- tool changes;
- memory architecture changes;
- safety-policy changes;
- Behavioral Policy changes, including any weakening of BP-1…BP-10 (`POLICY.md` §7);
- memory provider or retention-configuration changes;
- major workflow changes;
- significant incident findings;
- a change of deployment context that could bring the system within a Prohibited or Restricted
  use under `RESPONSIBLE_USE.md` §2.

## 5. Independence

A future certification program SHOULD distinguish:

- benchmark publisher;
- audit provider;
- certification issuer.

Independent assessment is preferable to self-attestation for third-party certification.

## 6. Public registry

A future AEIL registry could publish certificate ID, system version, audit date, benchmark version, score, and scope while avoiding unnecessary disclosure of confidential prompts or proprietary information.
