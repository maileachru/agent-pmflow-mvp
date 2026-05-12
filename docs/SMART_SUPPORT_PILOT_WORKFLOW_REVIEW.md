# Smart Support Pilot Workflow Review

Date: 2026-05-12

## Purpose

This review validates the full PMFlow weekly workflow on an invented project and records the issues found during the run.

## Invented project

**Project:** Smart Support Pilot — MVP pilot for AI-assisted customer support triage in the US SMB segment.

**Main milestones:**

- Kickoff: 2026-05-12
- Data sample ready: 2026-05-15
- Triage workflow prototype: 2026-05-22
- Legal/privacy review: 2026-05-26
- Pilot enablement pack: 2026-05-29
- Pilot start: 2026-06-02

**Planned meetings:**

- Daily implementation sync: 2026-05-13 through 2026-05-22
- Legal/privacy checkpoint: 2026-05-20
- Pilot readiness review: 2026-05-29
- Stakeholder demo: 2026-06-05

## Workflow executed

The workflow was run with the standard command:

```bash
pmflow run-weekly --meeting meetings/inbox/smart-support-pilot.md --title smart-support-pilot
```

Expected PMFlow artifacts were generated:

- meeting protocol
- decisions log
- action items log
- weekly stakeholder status
- Telegram reminder draft
- Mermaid Gantt plan
- PowerPoint outline and PPTX export
- output manifest

Telegram was not sent because the command did not include explicit send approval.

## Issues found

### Fixed in this review

1. **Decision text could become a false action item.**
   A line such as `Decision: We will run the pilot...` matched the generic `will` action pattern and produced an invalid owner `We`.
2. **Milestone and meeting lines could become false action items.**
   Lines containing words such as `review` were added as actions even when no action pattern matched, for example planned review meetings or milestone target descriptions.
3. **Russian `сделает` was listed as a candidate trigger but had no parser pattern.**
   This meant Russian action lines with `сделает` were detected as candidates but were not parsed consistently after unmatched candidates were stopped from becoming actions.

### Remaining product observations

1. **Weekly status is structurally correct but not fully executive-polished.**
   The status report embeds raw action and decision markdown rather than summarizing the highest-impact items.
2. **Presentation outline is deterministic but generic.**
   It uses extracted decisions, risks, and first actions, but the first slides still describe the workflow execution more than the business state of the invented project.
3. **Relative dates are handled safely but require PM review.**
   Items due `Friday` or `next week` correctly remain out of the scheduled Gantt timeline until a PM confirms ISO dates.

## Conclusion

The end-to-end workflow is usable for a minimal deterministic PM agent. It correctly creates all expected artifacts, keeps Telegram in draft-only mode by default, and produces a Gantt diagram only from explicit ISO due dates. The main inconsistency was action extraction being too permissive; that has been fixed and covered by a regression test. The next minimal improvement should be stakeholder-status summarization quality, not new integrations.
