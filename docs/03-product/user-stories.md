> **Canonical English document.** This document is normative from 18 August 2026 under `DEC-052`. The Spanish [historical record](../../historical/es/docs/03-product/user-stories.md) is retained for traceability; all new requirements, decisions, and changes belong in English.

# Initial User Story Catalog

**Status:** Draft
**Version:** 0.2

Stories describe user value. Normative requirements live in the specifications, and detailed acceptance criteria link to tasks in each vertical slice.

## Family and onboarding

### US-FAM-001 — Getting started with little configuration

As an adult, I want to create minimal profiles for my children to receive a first activity without filling out a long form.

**Acceptance:** aliases and age range are sufficient; optional data explains its purpose; no ability is inferred.

### US-FAM-002 — Multiple children

As an adult with several children, I want to choose who participates today so that the project fits the actual group.

**Acceptance:** participants can be changed per session; each participant internally receives a compatible assignment and sees a focus/contribution; an absentee does not receive exposure.

### US-FAM-003 — Today's context

As an adult, I want to indicate that today I have less time or less tolerance for mess so I can receive a viable option without altering my permanent preferences.

## Planning

### US-PLN-001 — Balanced plan

As an adult, I want to receive a varied weekly plan so as not to repeat the same phenomenon or skill.

**Acceptance:** visible reasons; consolidated materials; variety by area, skill, and contribution; individual activity replacement.

### US-PLN-002 — Use what I have

As an adult, I want to prioritize available materials to reduce purchasing and preparation.

### US-PLN-003 — Replace without starting over

As an adult, I want to change an activity that doesn't suit me without regenerating the entire week.

### US-PLN-004 — Open any day

As an adult, I want to open each activity in the plan to understand what we will do, what the child will learn, and how to prepare before accepting it.

**Acceptance:** every card is tappable and opens a detail containing promise, purpose, focus, materials, route, close-out, safety, and editorial status; returning preserves the weekly plan.

### US-PLN-005 — Buy once

As an adult, I want a weekly list organized by shopping location so I can get everything in one go without manually adding up quantities.

**Acceptance:** each total shows its source activities; repeated consumables add up; reusable tools use the maximum amount needed at once; items likely to be at home appear separately.

## Activity

### US-ACT-001 — Prepare before

As an adult, I want to see adult-only materials, timing, safety, and steps before gathering the kids.

### US-ACT-002 — Shared project

As an adult with three children, I want a common activity with different responsibilities to accompany them simultaneously.

**Acceptance:** meaningful, named contributions in each phase; compatible objectives; the oldest child is not automatically made a supervisor; dependencies and turns are shown without requiring the adult to configure technical roles.

### US-ACT-003 — Change an assignment

As an adult, I want to receive a suggested focus and input for each child and be able to record a different participation only if the actual dynamic requires it, without reorganizing the activity before starting.

### US-ACT-004 — Resume

As an adult, I want to pause and continue from the last step to address an interruption without losing context.

### US-ACT-005 — Troubleshoot a problem

As an adult, I want to ask for help from the current step so I don't repeat what activity I'm doing.

### US-ACT-006 — Adjust actual participation

As an adult, I want to indicate that a child is contributing in another way, observing, or no longer participating so the activity can continue without becoming a struggle or requiring me to manage technical roles.

**Acceptance:** the exception does not dominate the guide; the system can recalculate compatible actions; changes are recorded as session context and never as negative evidence, disobedience or personal trait.

### US-ACT-007 — Know how to facilitate learning

As a non-specialist adult, I want to see what to do, what to say, what each child will do, what they can decide and what to observe in each phase to accompany specific skills without reading the entire editorial document.

**Acceptance:** each phase satisfies `UX-FAC-005` to `UX-FAC-009`; help names the problem and the real change; the same pattern works for activities in different areas.

### US-ACT-008 — Live the full cycle

As an adult with several children, I want each one to propose, build or execute, test and observe when the activity allows so that a different focus does not exclude them from the essential experience.

**Acceptance:** the narrative mode and the actions of the cycle are declared; each active participant completes the required actions or the activity justifies why the artifact should be shared.

## Evidence

### US-EVD-001 — Quick close-out

As a busy adult, I want to answer only one rating per child so I can capture what matters in under twenty seconds.

### US-EVD-002 — Register a nuance

As an adult, I want to dictate an optional observation about one or more children so I can capture something important without typing.

### US-EVD-003 — Evaluate more

As an adult who observed several skills, I want to evaluate secondary objectives optionally without the system requiring me to do so each day.

### US-EVD-004 — Correct context

As an adult, I want to point out that the problem was the tool or material to avoid an incorrect conclusion about the child.

## Learning Journey

### US-LRN-001 — Understand an inference

As an adult, I want to open “Why?” to see which observations support an inference.

### US-LRN-002 — See the unknown

As an adult, I want to know in which areas there is still no evidence so as not to confuse lack of data with difficulty.

### US-LRN-003 — Correct or delete

As an adult, I want to correct or delete observations and inferences to maintain control of the profile.

### US-LRN-004 — Avoid comparisons

As an adult, I want to see each child's journey without sibling rankings.

## Privacy

### US-PRV-001 — Temporary photo

As an adult, I want to submit a photo for troubleshooting and know that it will not be retained by default.

### US-PRV-002 — Optional Portfolio

As an adult, I want to explicitly decide whether a project photo is saved in a private portfolio.

### US-PRV-003 — Export and delete

As the family owner, I want to review, export and delete data with clear scope.

## Editorial operation

### US-OPS-001 — Publish with gates

As an editor, I want to prevent publication until pedagogical and safety reviews are completed.

### US-OPS-002 — Remove immediately

As a safety manager, I want to withdraw a version to prevent new recommendations without deleting its history.

### US-OPS-003 — Collaborate by specialty

As an educator, scientist or specialist, I want to comment on fields and propose changes within an ActivityVersion without overwriting the work of others.

### US-OPS-004 — View pending gates

As a publisher, I want to know who approved pedagogy, safety, translation, and images before publishing.

## Community

### US-COM-001 — Private portfolio

As an adult, I want to save a photo or video of the project for my family without posting it.

### US-COM-002 — Inspire other families

As an adult, I want to voluntarily post the result under the corresponding activity after reviewing privacy and policies.

### US-COM-003 — Report content

As an adult, I want to report a post that is inappropriate or exposes children's information so that the team can act quickly.

### US-COM-004 — Separate marketing use

As an adult, I want community sharing not to authorize the use of my media in ads or company social accounts automatically.

## Subscription

### US-SUB-001 — Understand the trial

As an adult, I want to see how long the trial is, when it will be charged, and how much it will cost before I sign up.

### US-SUB-002 — Cancel easily

As an adult, I want to cancel from Account through the channel where I paid, without contacting support or immediately losing the current period.

### US-SUB-003 — Share Family Access

As a payer, I want authorized adults to use the same subscription without seeing my payment details.

### US-SUB-004 — Keep my data

As an adult, I want cancellation to stop future payments without automatically deleting profiles, progress, or portfolio content.
