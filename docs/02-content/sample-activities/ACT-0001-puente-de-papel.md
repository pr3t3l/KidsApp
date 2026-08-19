> **Canonical English document.** This document is normative from 18 August 2026 under `DEC-052`. The Spanish [historical record](../../../historical/es/docs/02-content/sample-activities/ACT-0001-puente-de-papel.md) is retained for traceability; all new requirements, decisions, and changes belong in English.

# ACT-0001 — Paper Bridge

**Status / Status:** Draft — not eligible for family recommendation / not eligible for family recommendation

**Version / Version:** 0.3.0

**Specification source language:** English (`en-US`)

**Required bundles:** `es-US`, `en-US`

**Proposed editorial owner:** Founder

**Authors of this version:** Product team, draft for human review

**Last document review / Last document review:** 2026-08-15

## 1. ActivityVersion control

| Field | Value |
|---|---|
| `activity_id` | `ACT-0001` |
| `version` | `0.3.0` |
| `slug` | `paper-bridge` |
| `status` | `draft` |
| `age_range` | 5–10 years / ages 5–10 |
| `functional_levels` | L1 Explorer, L2 Builder, L3 Inventor, L4 Engineer; assigned by ability and context, not the child's overall level |
| `participant_range` | 1–3 children and one supervising adult / 1–3 children and one supervising adult |
| `duration` | 30–60 minutes / minutes |
| `adult_preparation` | 5–7 minutes / minutes |
| `cleanup` | 2–4 minutes / minutes; included in `duration` / included in `duration` |
| `safety_level` | A — low risk materials under normal adult supervision |
| `mess_level` | Low / Low |
| `space` | Stable, dry, clear table at least 24 × 24 in |
| `prerequisites` | None required; Counting, folding and explaining can be the first presentation with support. /None required; counting, folding, and explaining may be first exposures with support. |
| `accessibility` | Response by voice, gesture, drawing or selection; adult stabilization of the role and change of objective before starting. / Response by voice, gesture, drawing, or choice; adult paper stabilization and objective change before starting. |
| `offline_required` | Yeah; instructions, approved images, roles, objectives, safety and closure must be in the downloaded package |

This version supports sessions for one, two or three children. A four-child session is not eligible until a meaningful configuration for four participants is tested and versioned.

### 1.1 Revision status

| Gate | State | Condition to advance |
|---|---|---|
| `ACT-0001-GATE-01` Editorial property | Pending | One person accepts editorial responsibility. |
| `ACT-0001-GATE-02` Pedagogical review | Pending | Review of goals, observable cues, and adult/child language. |
| `ACT-0001-GATE-03` Scientific/disciplinary review | Pending | A person competent in structures or science teaching validates mechanism, variables and explanations. |
| `ACT-0001-GATE-04` Safety Review | Pending | Execution of safe failure and validation of the vessel, loading protocol and controls. |
| `ACT-0001-GATE-05` Bilingual Review | Pending | Check scientific equivalence, instructions and warnings `es-US`/`en-US`. |
| `ACT-0001-GATE-06` Family pilot → Published | Not started | After `ready_for_pilot`: one founder run and at least three additional runs across two families, including one led by another adult. |
| `ACT-0001-GATE-07` Visual Resources | Pending | Assets tied to 0.3.0 with automatic QA and human approval. |

There are no approved `review_records`. Therefore, this ActivityVersion cannot enter family production plans or sessions.

### 1.2 Canonical serialization convention

This document directly uses JSON Schema patterns where they exist:- `stepId`: `STEP-00` to `STEP-09`; `STEP-00`, `STEP-04` and `STEP-08` make up `adultOnlyStepIds`.
- The integer `minutes` of each step uses the canonical 45-minute path; `minutes_by_path` retains the 30/45/60 variants indicated on the sheet. The cleaning is also recorded in `timing.cleanupMinutes` and is already included in the total for each route.
- `visualBriefId`: `VIS-01` to `VIS-08`; the context `ACT-0001@0.3.0` gives the global namespace.
- `adaptationId`: prefix `ADAPT-`, for example `ADAPT-BRIDGE-PAUSE`.
- `materialId`, `roleTemplateId` and `hazardId`: prefixes `MAT-`, `ROLE-` and `HAZ-` respectively.
- The `ACT-0001-OBJ-*` are local editorial question/rubric identifiers; the serialized field `primaryObjectiveSkillId` and `eligiblePrimarySkillIds` uses the associated canonical `skillId` in 3.2.
- `requiredReviewGates`: `publisher` (`GATE-01`), `education` (`GATE-02`), `subject` (`GATE-03`), `safety` (`GATE-04`), `language` (`GATE-05`) and `visual` (`GATE-07`); `GATE-06` is serialized to `pilotRecords`, not as a review gate type.

Before `ready_for_pilot`, a JSON representation of this version must validate without semantic transformations against `schemas/v0.1/activity-version.schema.json`. The Markdown tab is not a replacement for that validation or a human `review_record`.

## 2. Localized promise

| Bundle | Title | Summary |
|---|---|---|
| `es-US` | Paper bridge | Build and compare bridges made from a single sheet of paper to discover how the shape can help the paper resist a load. |
| `en-US` | Paper Bridge | Build and compare bridges made from one sheet to discover how shape can help paper resist a load. |

### 2.1 Result of the experience

Educational success does not require that a design sustain a certain amount. The experience is successful when the family can run at least two comparable tests, record what happened and propose an improvement based on what was observed.

Educational success does not require a design to hold a specific amount. The experience is successful when the family can run at least two comparable tests, record what happened, and propose an improvement based on what they observed.

## 3. Educational purpose

### 3.1 Areas, concepts and decisions

- **Main area:** `ENG` Engineering — structures, design and iteration.
- **Secondary areas:** `PHY` strength/load and flexion; `MAT` counting, measuring and comparing; `MOT` fold; `LOG` controlled test; `COM` explanation; `SEL` persistence; `PRA` organization and cleaning.
- **Concepts:** structure, load, bending rigidity, shape, load distribution and fair comparison.
- **Real child decision:** how to fold or shape a sheet for the improvement test.
- **Opening Question `es-US`:** “How can a sheet of paper become a bridge that supports a load?”
- **Opening question `en-US`:** “How can one sheet of paper become a bridge that holds a load?”

An exposure to these concepts does not demonstrate understanding. Only an observed action or explanation can provide evidence for an ability.

### 3.2 Eligible primary objectives

Each child receives exactly one of these primary objectives before starting. The others can only be registered as exposures, unless the adult chooses **Evaluate more**.

| ObjectiveID | Canonical `skillId` | Observable skill / Observable skill | Level / Level | Observable signal / Observable signal |
|---|---|---|---|---|
| `ACT-0001-OBJ-01` | `MAT-SKL-ONE-TO-ONE-COUNT` | Add and count one load item at a time using one-to-one correspondence. | L1–L2 | Places one crayon per turn and maintains or recovers the total. |
| `ACT-0001-OBJ-02` | `MOT-SKL-FOLD-SEQUENCE` | Follow a folding sequence and place the structure. / Follow a folding sequence and place the structure. | L1–L3 | Perform the steps in order with appropriate support. / Complete the steps in order with appropriate support. |
| `ACT-0001-OBJ-03` | `MAT-SKL-COMPARE-RESULTS` | Compare results using more, less or equal. / Compare results using more, less, or the same. | L1–L3 | Use the results of two tests to compare them. / Uses two test results to compare them. |
| `ACT-0001-OBJ-04` | `LOG-SKL-KEEP-CONDITIONS` | Keep test conditions constant. /Keep test conditions constant. | L2–L4 | Check distance, orientation, glass and load between designs; the adult restores the supports. / Checks the gap, orientation, cup, and load between designs; the adult resets the supports. |
| `ACT-0001-OBJ-05` | `ENG-SKL-ITERATE-SHAPE` | Propose, build and test a form improvement. / Propose, build, and test a shape improvement. | L2–L4 | Choose a shape change and see what happened. / Chooses a shape change and tests what happened. |
| `ACT-0001-OBJ-06` | `COM-SKL-EVIDENCE-EXPLANATION` | Explain a statement using an observed result. / Explain a claim using an observed result. | L2–L4 | It relates a design to evidence from the test, even if the causal explanation is still initial. / Connects a design to test evidence even when the causal explanation is still emerging. |

Age filters language and safety constraints, but it does not determine the objective by itself. If there is no prior evidence, use the configuration's default objective as exploration or growth and explain the selection as an “opportunity to observe,” not a prediction of ability.

#### 3.2.1 Initial calibration without prior evidence

This table guides the fixture and the first recommendation; it does not replace individual evidence.

| Indicative range | Preferred initial focus | Intent | Why it can provide challenge | If it is easy / difficult |
|---|---|---|---|---|
| 5–6 | `OBJ-01` one-to-one correspondence during your own test | Consolidation or growth | Maintaining one action per number, waiting for stability and recovering the total integrates counting with a physical situation. | Easy: compare your total with the reference. Difficult: have visual or adult support and evaluate only the observed correspondence. |
| 7–8 | `OBJ-05` propose, build and test your own form | Growth | It turns an idea into a testable design and requires relating it to a result, not just folding. | Easy: justify a single change. Difficult: Choose between two approved shapes and build with guides. |
| 9–10 | `OBJ-04` maintain constant conditions | Growth | It requires controlling several conditions while each child tries a different design. | Easy: record and explain why a test was not comparable. Difficult: check an assigned condition with a checklist. |

At any range, recent evidence may justify another eligible target. Counting to 20 without waiting, matching, or retrieval is not used as a primary challenge for a child when there is already evidence of independence; comparison, design, control of conditions or explanation are selected.### 3.3 Planned secondary exposures

An exposure is only recorded when the child actually participated in the corresponding action or conversation.

| Exposure / Exposure | It is recorded when… / Record when… | It doesn't mean… / Doesn't mean… |
|---|---|---|
| Structure and rigidity / Structure and stiffness | Observed or handled at least two forms of paper. / Observed or handled at least two paper shapes. | That understands why one shape resists better. / That the child understands why a shape resists bending better. |
| Load and bending / Load and bending | Participated in a test and observed deformation or stability. / Took part in a test and observed bending or stability. | Which can predict loads or forces. / That the child can predict loads or forces. |
| Counting / Counting | Added, counted or checked cargo pieces. / Added, counted, or checked load items. | Which featured precision and independence. / That the child counted accurately and independently. |
| Measurement / Measurement | Helped to fix or check the separation. / Helped set or check the gap. | Which measures lengths independently. / That the child measures length independently. |
| Fair comparison / Fair comparison | Participated in maintaining equal conditions. / Helped keep conditions the same. | Who knows how to design a controlled trial in other contexts. / That the child can design a controlled test in other contexts. |
| Design and iteration / Design and iteration | Proposed, chosen or constructed a change. / Proposed, chose, or built a change. | That the improvement worked or that you have already mastered design. / That the change improved the bridge or the child has mastered design. |
| Explanation / Explanation | Shared a prediction, observation, or reason. / Shared a prediction, observation, or reason. | That the scientific explanation was complete. / That the scientific explanation was complete. |

### 3.4 Instance of narrative contract

- **Mode:** `hybrid`.
- **Mandatory individual part:** each active participant finds the problem, proposes a way, builds his own sheet, performs his test in turns, observes/records his result and proposes an improvement.
- **Shared part:** the group selects a single change based on the results, builds an improvement sheet and tests it again.
- **Focus rule:** the primary objective determines what signal the adult observes; does not reserve design, construction or testing for a single child.

#### Materials function

| Materials | Function visible before first use | Introduction |
|---|---|---|
| Books | Create two equal supports 15 cm / 6 in apart. | `STEP-00` |
| Paper | Become the bridge; one sheet per design. | `STEP-01` |
| Glass | Charging container placed in the center; always empty when starting a test. | `STEP-01` |
| Crayons | Equal charge units that are added one at a time into the glass. | `STEP-01` |
| Ruler/marks | Check that the gap remains the same. | `STEP-00` |
| Registration sheet | Preserve idea, design, result and comparability of each test. | `STEP-01` |

#### States and continuity

| Step | Entry status | Causal action | Output status | Why enable the following moment |
|---|---|---|---|---|
| `STEP-01` Discover | `STATE-READY` | Present material function and test a flat sheet. | `STATE-BASELINE-OBSERVED` | There is already a problem seen and a reference result to imagine about. |
| `STEP-02` Imagine | `STATE-BASELINE-OBSERVED` | Suggest shapes, watch an adult demonstration, and choose one shape per child. | `STATE-DESIGNS-CHOSEN` | Each child has a specific intention that they can build. |
| `STEP-03` Build | `STATE-DESIGNS-CHOSEN` | Each child builds and labels their own sheet. | `STATE-CHILD-DESIGNS-READY` | There are identifiable artifacts ready to test one by one. |
| `STEP-04/05` Experiment | `STATE-CHILD-DESIGNS-READY` | Each child performs his test in the same setup and records the result. | `STATE-CHILD-RESULTS-RECORDED` | There are several comparable results that allow you to choose an improvement. |
| `STEP-06` Improve | `STATE-CHILD-RESULTS-RECORDED` | They all propose; the group builds and tests a single change. | `STATE-IMPROVEMENT-TESTED` | There is an iteration linked to previous evidence. |
| `STEP-07` Explain | `STATE-IMPROVEMENT-TESTED` | Each child connects his or her design or improvement with something seen or told. | `STATE-EXPLANATION-SHARED` | The experience ends with expressed evidence, not just an object. |

A screen cannot change this order, skip the baseline flat test, or make mandatory individual actions exclusive to a single child.

## 4. Canonical test parameters

These parameters are part of the core and remain the same between designs:

1. Single sheet intact by design, same size and package.
2. The long edge of the blade crosses a space of `15 cm / 6 in` between the inside edges of the supports.
3. The blade rests on both supports without tape, glue, clips or other fixings.
4. The same light glass is placed with its base approximately in the center of the space and without touching the supports.
5. The only approved load is the same set of 20 canonical crayons. In their own test, each child gently lowers a crayon until it is completely inside the glass; He doesn't let it fall. Alternate which side of the center you place it on so you don't concentrate all the load on one edge.
6. Before adding the first crayon, the adult confirms immobile supports, supported leaf, and centered glass. The empty glass should remain stable for a slow count of three.
7. The score is the last number of crayons that remained stable during a slow count of three under a valid setup.
8. If you hold all 20, `20+` is recorded; no objects are added or cargo replaced.

**Canonical parameters `en-US`:**

1. Use one intact sheet per design, with every sheet from the same size and package.
2. The sheet's long edge spans a `15 cm / 6 in` gap between the inner edges of the supports.
3. The sheet rests on both supports without tape, glue, clips, or other attachment.
4. Place the same lightweight cup with its base near the center of the gap and without touching the supports.
5. The only approved load is the same canonical set of 20 crayons. The child whose turn it is gently lowers one crayon fully into the cup and alternates the side of center to avoid concentrating the load on one edge.
6. Before the first crayon, the adult confirms stationary supports, sheet overlap, and a centered cup. The empty cup remains stable for a slow count of three.
7. The score is the last number of crayons that remained stable for a slow count of three under a valid setup.
8. If the bridge holds all 20, record `20+`; do not add or substitute objects.

### 4.1 Test failure classification

| State | Definition `es-US` | Definition `en-US` | Action / Action |
|---|---|---|---|
| `invalid_setup` | An external condition changes before failure can be attributed to the paper: shifted support, uneven sheet overlap, an initially off-center cup, dropped or edge-loaded crayons, a bump, or participant contact. | An external condition changes before failure can be attributed to the paper: shifted support, uneven sheet overlap, an initially off-center cup, dropped or edge-loaded crayons, a bump, or participant contact. | Produces no score. The adult resets once from zero. If it happens again or the cause is uncertain, mark **Not comparable** and stop that design. |
| `bridge_deformation` | With valid mounting, the paper curls, flattens or loses support and then the center touches the towel or the glass tilts or slides. If you fail to place the empty glass correctly, the result is 0. | With a valid setup, the paper bends, flattens, or loses support and then its center touches the towel or the cup tips or slides. If it fails when the empty cup is placed correctly, the result is 0. | End the test and record the last stable quantity; do not restart to search for a higher number. / End the test and record the last stable amount; do not restart to seek a higher number. |
| `safe_stop` | An object breaks, someone puts their face or hand under the assembly, puts material in their mouth, throws the load, or the adult cannot confirm safety. | An item breaks; someone puts a face or hand under the setup, mouths material, throws the load, or the adult cannot confirm safety. | Stop the activity. Do not produce a score for the interrupted test. /Stop the activity. Produces no score for the interrupted test. |

The glass tilt does not reset automatically. The adult uses the above definitions; when in doubt the result is `invalid_setup`, never negative evidence about a child. The cup and load protocol remains subject to the physical gate of section 19.

Cup tipping does not trigger an automatic restart. The adult uses the definitions above; when uncertain, the result is `invalid_setup`, never negative evidence about a child. The cup-and-load protocol remains subject to the physical gate in section 19.

The comparison is valid within the session. No numbers are compared between different families, paper types or loading sets. / The comparison is valid within the session. Do not compare numbers across families, paper types, or different load sets.

## 5. Materials

### 5.1 Canonical list

| ID | Quantity/unit | Required | Consumable | Name `es-US` / `en-US` | Adult preparation / Adult preparation | Safety note / Safety note | Approved substitution / Approved substitution |
|---|---|---:|---:|---|---|---|---|
| `MAT-PAPER-COPY` | 6 `sheet` | Yes | Yes | Standard printer or copy paper, Letter or A4, from the same package | Reserve 1 for the flat baseline and adult demonstration, up to 3 for one child design each, 1 for the group improvement, and 1 for planning/results; inspect for dryness and intact edges. | Remove damp or torn sheets and any sheets with sharp damaged edges. | Letter or A4; choose one and do not mix sizes. |
| `MAT-SUPPORT-BOOK` | 2 `item` | Yes / Yes | No | Stable hardcover books, each at least 15 × 20 cm and 3–6 cm thick; thickness difference ≤0.5 cm / Stable hardcover books, each at least 6 × 8 in and about 1.2–2.4 in thick; thickness difference ≤3/16 in | The adult checks that they are dry, flat, without loose pieces and that they do not slide. / The adult checks that they are dry, flat, have no loose parts, and do not slide. | Only the adult places, moves and stores the supports. / Only the adult places, moves, and stores the supports. | Two closed rectangular boxes, firm, dry, not fragile and of equal height, after adult validation. / Two closed, sturdy, dry, nonbreakable rectangular boxes of equal height after adult validation. |
| `MAT-CUP-LIGHT` | 1 `item` | Yes / Yes | No | Empty lightweight 8–12 oz paper cup with a flat 2–2.75 in / 5–7 cm base | Inspect that it is not crushed, wet or deformed; use the same in all tests. Its function is to contain the load in the center of the bridge. / Check that it is not crushed, damp, or warped; use the same cup in every test. Its function is to hold the load at the bridge center. | Do not use with liquid or if unsteady on a flat table. / Do not use with liquid or if it rocks on a flat table. | None in 0.3.0; another form or material requires physical validation and new version. /None in 0.3.0; another shape or material requires physical validation and a new version. |
| `MAT-CRAYON-LOAD` | 20 `item` | Yes / Yes | No | Twenty standard, non-jumbo, intact, similarly sized crayons, approximately 3–4 in / 8–10 cm long | Count 20, remove fragments and keep exactly the same set during the session. Each crayon is a unit of charge added one at a time. / Count 20, remove fragments, and keep exactly the same set throughout the session. Each crayon is one load unit added one at a time. | Keep out of mouth; Lower each crayon into the glass, do not throw it. / Keep out of mouths; lower each crayon into the cup rather than dropping it. | None in 0.3.0; markers, blocks, coins and other loads are not validated. /None in 0.3.0; markers, blocks, coins, and other loads are not validated. |
| `MAT-RULER` | 1 `item` | Yes / Yes | No | 30 cm / 12 in ruler without broken edges / 30 cm / 12 in ruler with no broken edges | Inspect; the child can read it or point while the adult moves supports. / Inspect it; the child may read or point while the adult moves supports. | Remove a broken ruler or ruler with a sharp edge. / Remove a cracked ruler or one with a sharp edge. | Intact flexible measuring tape under adult control. / Intact flexible measuring tape under adult control. |
| `MAT-MARKER` | 1 `item` | Yes / Yes | No | Pencil or washable marker | Check that it is non-toxic and age appropriate. / Check that it is nontoxic and age-appropriate. | Cover the marker when finished; remove broken tips. / Cap the marker after use; remove broken tips. | Another non-toxic and age-appropriate writing utensil. / Another nontoxic, age-appropriate writing tool. |
| `MAT-TAPE-MARK` | 4 `piece`, 2–3 cm / 1 in | No | Yes / Yes | Optional removable painter's tape | The adult cuts or tears four pieces and uses them only to mark the outside position of the books. / The adult tears or cuts four pieces and uses them only to mark the books' outer positions. | Never fix the bridge or tape it to the skin or hair. / Never attach the bridge or put tape on skin or hair. | Skip and check the position with the ruler before each test. / Omit it and check position with the ruler before each test. |
| `MAT-TOWEL` | 1 `item` | Yes / Yes | No | Hand towel in one layer | Extend under the space without holding the bridge or glass at the beginning. / Lay it under the gap without supporting the bridge or cup at the start. | It should be dry, flat and without loose loops or cords. / It must be dry, flat, and free of loose loops or cords. | Thin, soft, clean and non-slip mat. / Thin, soft, clean, nonslip mat. |

### 5.2 Materials not approved in this version

Do not replace the charge with markers, blocks, coins, marbles, batteries, rocks, cans, glass, tools, food, containers of liquid or other objects. Do not replace the glass in this version. Do not use scissors, staples, pins, tensioned rubber bands or glue gun. Do not fix the bridge to the supports during core testing.

Do not replace the load with markers, blocks, coins, marbles, batteries, rocks, cans, glass, tools, food, liquid-filled containers, or any other objects. Do not replace the cup in this version. Do not use scissors, staples, pins, stretched rubber bands, or a hot glue gun. Do not attach the bridge to the supports during the core tests.

## 6. Adult preparation and safety

### 6.1 `STEP-00` — Adult preparation

- **Stage:** `build_or_do`; **actor:** `adult`; **minutes:** 5 on all routes / 5 on every path.
- **Visual brief IDs:** `VIS-01`, `VIS-02`.
- **Expected result:** two flat and immobile supports, 15 cm / 6 in spacing, materials inspected and configuration assigned. / Two flat, stationary supports, a 15 cm / 6 in gap, inspected materials, and an assigned configuration.
- **Success signal:** the adult confirms checklist, stable glass on a flat table and no broken materials. / The adult confirms the checklist, a cup that is stable on a flat table, and no broken material.
- **Resume:** Re-inspect stability, separation, integrity and counting before continuing. / Recheck stability, gap, integrity, and count before continuing.
- **Warning / Warning:** only the adult moves the supports; do not start if the glass wobbles on the table or the assembly is near an edge or passage area. / Only the adult moves supports; do not begin if the cup rocks on the table or the setup is near an edge or walkway.
- **Common problem / Common problem:** supports of different heights; replace them with a pair that meets the tolerance, without compensating by stacking. /Supports differ in height; replace them with a pair within tolerance rather than compensating by stacking.

#### Instructions `es-US`

1. Clear a firm, dry table away from the edge of a staircase or passage area.
2. Inspect the books, glass, ruler, and crayons. Remove any broken, sharp or fragile objects.
3. Spread the towel in a single layer on the table. Place a book on each side, completely flat; the towel should not touch the bridge or the glass at the beginning.
4. Leave exactly `15 cm / 6 in` between the inside edges. Mark the outside position with removable tape, if you have it.
5. Separate six sheets from the same packet: reference/demonstration, one per child (maximum three), group improvement and registration.
6. Load the participant configuration. Confirms only one primary objective per child; everyone will complete their own design and testing.
7. Keep the 20 crayons within reach and off the edge of the table.

#### Instructions `en-US`

1. Clear a stable, dry table away from stairs and walkways.
2. Inspect the books, cup, ruler, and crayons. Remove anything broken, sharp, or fragile.
3. Lay the towel flat in one layer on the table. Place one book on each side, fully flat; the towel must not touch the bridge or cup at the start.
4. Leave exactly `15 cm / 6 in` between the inner edges. Mark each outer position with removable tape, if available.
5. Set aside six sheets from the same paper package: baseline/demonstration, one per child (up to three), group improvement, and recording.
6. Load the participant configuration. Confirm exactly one primary objective per child; everyone will complete a design and test of their own.
7. Keep the 20 crayons within adult reach and away from the table edge.

### 6.3 Risk and control register

**Level:** A for canonical list only: children handle low-risk paper, glass, and crayons under normal adult supervision. / A for the canonical list only: children handle low-risk paper, cup, and crayons under normal adult supervision.

**Supervision / Supervision:** the adult remains present, controls the supports and can stop the test immediately. / The adult remains present, controls the supports, and can stop the test immediately.

| Hazard ID / category | Danger `es-US` / Hazard `en-US` | Person or condition / Person or condition | Control `es-US` / Control `en-US` | Step IDs |
|---|---|---|---|---|
| `HAZ-FALLING-LOAD` / `other` | Falling support, cup, or load | Any participant if books are stacked, shifted, or near the edge | Books flat, set up low, towel under, table clear and maximum 20 crayons; stop when a support moves. / Flat books, low setup, towel below, clear table, and no more than 20 crayons; stop if a support moves. | `STEP-00`, `STEP-04`, `STEP-05`, `STEP-06`, `STEP-08` |
| `HAZ-SHARP-DAMAGE` / `cut` | Damaged paper or ruler may cut or poke | Child while folding or measuring | Adult inspection, slow movements, and removal of torn paper or a cracked ruler. | `STEP-00`, `STEP-03` |
| `HAZ-MOUTHING` / `ingestion` | Crayon or fragment placed in the mouth | Child, especially one who tends to mouth objects | Only intact crayons, continuous supervision and immediate removal of fragments; stop if it happens. / Intact crayons only, continuous supervision, and immediate fragment removal; stop if it occurs. | `STEP-00`, `STEP-05`, `STEP-09` |
| `HAZ-THROWN-SPILL` / `spill` | Thrown or dropped crayons may create a trip hazard | Group during a failure | Go down one at a time, wait for everything to stop, pick up before continuing and do not chase objects during the test. / Lower one at a time, wait until everything stops, collect before continuing, and do not chase items during the test. | `STEP-05`, `STEP-09` |
| `HAZ-PINCHED-FINGER` / `other` | Fingers under a support / Fingers under a support | Child attempting to move a book or box | Placing, readjusting and storing supports are exclusive actions of the adult; no hand remains under the assembly. / Placing, resetting, and storing supports are adult-only actions; no hand remains under the setup. | `STEP-00`, `STEP-04`, `STEP-08` |
| `HAZ-COMPETITION` / `other` | Frustration or competition if the result is framed as a personal score | Child during testing or explanation | Compare designs, not children; allow pause and celebrate unexpected observations and data. / Compare designs, not children; allow a pause and celebrate observations and unexpected data. | `STEP-05`, `STEP-07` |

### 6.4 Bilingual critical warning

> **Adult / Adult:** Place and readjust the books. Keep the test on a low, stable table. Stop the activity if a support moves, an object breaks, a child puts materials in his mouth, or someone starts throwing the load. /Place and reset the books. Keep the test on a low, stable table. Stop if a support moves, an item breaks, a child mouths materials, or anyone begins throwing the load.

### 6.5 Steps exclusive to adults

`adultOnlyStepIds = [STEP-00, STEP-04, STEP-08]`.

- **`es-US`:** The adult chooses and clears the place; inspects materials; places, measures and rearranges books; place/center the empty glass at the beginning of each test; classifies a fault as `invalid_setup`, `bridge_deformation`, or `safe_stop`; remove the glass between tests; and save the supports. A child can read the ruler or indicate the position, but does not move the supports.
- **`en-US`:** The adult chooses and clears the location; inspects materials; places, measures, and resets the books; places/centers the empty cup at the start of every test; classifies a failure as `invalid_setup`, `bridge_deformation`, or `safe_stop`; removes the cup between tests; and stores the supports. A child may read the ruler or indicate position but does not move the supports.

The AI ​​cannot reassign these steps to a child or remove the warning.

AI may not reassign these steps to a child or remove the warning.

## 7. Roles and settings

### 7.1 Role templates

| Bilingual ID/name | Compatible levels | Contribution / Contribution | Responsibilities / Responsibilities | Eligible objectives / Eligible objectives | Allowed step IDs | Restricted step IDs | Dependencies / Dependencies |
|---|---|---|---|---|---|---|---|
| `ROLE-CHILD-INVESTIGATOR` Bridge Investigator | L1–L4 according to objective / by objective | Complete your own cycle within the shared challenge. / Complete an individual cycle within the shared challenge. | Observe the reference, propose, build a sheet, perform your test, record/observe, recommend an improvement and explain. / Observes the baseline, proposes, builds one sheet, runs an individual test, records/observes, recommends an improvement, and explains. | Any of `OBJ-01` through `OBJ-06`, exactly one per session | `STEP-01`, `STEP-02`, `STEP-03`, `STEP-05`, `STEP-06`, `STEP-07`, `STEP-09` | `STEP-00`, `STEP-04`, `STEP-08` | The adult prepares/reestablishes the setup and everyone waits for their turn to test. / The adult prepares/resets the setup and everyone waits for the testing turn. |

All children use the same internal template because they all live the full cycle. The primary objective personalizes observation, language and support; it assigns no monopolies over designing, counting, or testing. The family UI does not display the technical name of the role.

### 7.2 Setting up a child

| Participant / Participant | Role / Role | Default objective without evidence | Secondary exposures / Secondary exposures |
|---|---|---|---|
| Child 1 / Child 1 | `ROLE-CHILD-INVESTIGATOR` | According to 3.2.1 and evidence; no evidence, `OBJ-01` for 5–6, `OBJ-05` for 7–8 or `OBJ-04` for 9–10 / Per 3.2.1 and evidence | Structure, load, counting, folding, comparison, and explanation only when actually performed |

The adult continues doing the exclusive steps. The child carries out his design and testing with appropriate support. / The adult still performs adult-only steps. The child completes an individual design and test with appropriate support.

### 7.3 Setting up two children

| Participant / Participant | Role / Role | Default objective without evidence | Secondary exposures / Secondary exposures |
|---|---|---|---|
| Child 1 / Child 1 | `ROLE-CHILD-INVESTIGATOR` | According to 3.2.1 and evidence / Per 3.2.1 and evidence | Full cycle on an individual sheet |
| Child 2 / Child 2 | `ROLE-CHILD-INVESTIGATOR` | According to 3.2.1 and evidence / Per 3.2.1 and evidence | Full cycle on an individual sheet |

They both propose, build and test a sheet in turns. They share the final improvement. / Both propose, build, and test one sheet in turn. They share the final improvement.

### 7.4 Three-child configuration

| Participant / Participant | Role / Role | Default objective without evidence | Secondary exposures / Secondary exposures |
|---|---|---|---|
| Child 1 / Child 1 | `ROLE-CHILD-INVESTIGATOR` | According to 3.2.1 and evidence / Per 3.2.1 and evidence | Full cycle on an individual sheet |
| Child 2 / Child 2 | `ROLE-CHILD-INVESTIGATOR` | According to 3.2.1 and evidence / Per 3.2.1 and evidence | Full cycle on an individual sheet |
| Child 3 / Child 3 | `ROLE-CHILD-INVESTIGATOR` | According to 3.2.1 and evidence / Per 3.2.1 and evidence | Full cycle on an individual sheet |

The three propose, build and test their own sheet in visible order. While one tastes, the others observe and compare; Observing someone else's evidence is not a substitute for one's own evidence. All three propose shared improvement. / All three propose, build, and test their own sheet in a visible order. While one tests, the others observe and compare; watching another test does not replace one's own test. All three propose the shared improvement.

### 7.5 Assignment rule

- Before starting: exactly one `primary_objective_id` per participant.
- During the session: each child retains access to the complete cycle; the target may be supported, but is not silently replaced.
- When closing: confirm who participated and if they carried out their own test.
- If a child did not participate: do not create an exposure or ask for an evaluation.
- If the adult did the target action: offer “No se poderobserv / Could not observe”; do not assign a 1.

In serialization, `eligiblePrimarySkillIds` uses the canonical `skillId` from section 3.2; the `OBJ-*` identifies the local question/rubric of this ActivityVersion. / In serialization, `eligiblePrimarySkillIds` uses the canonical `skillId` values ​​in section 3.2; `OBJ-*` identifies this ActivityVersion's local question/rubric.

## 8. Durations and routes

| Phase / Stage | Route / Path 30 min | Route / Path 45 min | Route / Path 60 min |
|---|---:|---:|---:|
| Adult preparation / Adult preparation | 5 min | 5 min | 5 min |
| Discover | 4 min | 6 min | 7 min |
| Imagine | 3 min | 5 min | 7 min |
| Build | 5 min | 8 min | 10 min |
| Experiment | 7 min | 10 min | 14 min |
| Improve | 3 min | 6 min | 11 min |
| Explain and close / Explain and close | 1 min | 2 min | 3 min |
| Cleanup / Cleaning | 2 min | 3 min | 3 min |

The short route retains the six phases and one test per child. The 60-minute route expands planning, construction and comparison; it only repeats the improvement when the number of participants leaves a canon sheet unused. With three children he does not add a seventh leaf in this version. / The short path keeps all six stages and one test per child. The 60-minute path expands planning, building, and comparison; it repeats the improvement only when participant count leaves one canonical sheet unused. With three children, this version does not add to a seventh sheet.

Totals include preparation, closing and cleaning; no hidden time is added to the family block. / Totals include preparation, close, and cleanup; no hidden time is added to the family's block.

## 9. Localized execution

### 9.1 `STEP-01` — Discover (4–7 min)

**Stage:** `discover`. **Actor:** `group`; the adult facilitates / adult-facilitated. **Minutes:** 6 canonical; 4/6/7 on routes 30/45/60/canonical; 4/6/7 on 30/45/60 paths.

**Visual brief IDs:** `VIS-02`.

**Entry / Entrance:** `STATE-READY`. **Exit:** `STATE-BASELINE-OBSERVED`.

**Expected result:** The group understands what glass and crayons are for, observes a real flat sheet test, and records a reference result. / The group understands the purpose of the cup and crayons, observes a real flat-sheet test, and records a baseline result.

**Resume:** can be paused after recording the reference result; upon returning, the adult repeats `STEP-04` before any trial. / Pause after recording the baseline result; on return, the adult repeats `STEP-04` before any test.

**Warning / Warning:** the adult centers the glass and corrects the supports; children only add crayons after the signal and in turns. / The adult centers the cup and adjusts supports; children add crayons only after the signal and in turn.

**`es-US`**

1. Point out the materials: "The books are the supports. This sheet will be the bridge. The glass will be empty in the center and will hold the crayons. Each crayon will be a unit of charge."
2. Place the sheet flat on the supports and ask: "What do you think will happen when the glass starts to fill? Where might it bend?" Each child predicts by talking, pointing or drawing.
3. Give the signal. The adult centers the empty glass. If it remains stable for three seconds, children add one crayon in turn, say the number, and wait three seconds.
4. Stop the test when the paper fails or reaches 20. Record `PLANA`, the last stable number and whether the test was comparable.
5. Question: “What did you see that we now need to change?” Don't explain yet which way will be better.

**`en-US`**

1. Point to the materials: "The books are supported. This sheet will be the bridge. The empty cup will sit in the center and hold the crayons. Each crayon is one load unit."
2. Place the flat sheet on the supports and ask: "What do you think will happen as the cup fills? Where might it bend?" Each child predicts by speaking, pointing, or drawing.
3. Give the signal. The adult centers the empty cup. If it stays stable for three seconds, children add one crayon in turn, say the number, and wait three seconds.
4. Stop when the paper fails or reaches 20. Record `FLAT`, the last stable number, and whether the test was comparable.
5. Ask: “What did you see that we now need to change?” Do not explain which shape will work best.

**Success signal:** everyone observed the physical problem and there is a reference result; Now it makes sense to imagine shapes. / Everyone observed the physical problem and a baseline result exists; imagining shapes now has a reason.

**Common problem / Common issue:** If the child looks for the “correct answer”, respond: “We don't know yet; the test will give us information.” / If the child seeks the “right answer,” respond: “We do not know yet; the test will give us information.”

### 9.2 `STEP-02` — Imagine / Imaginar (3–7 min)

**Stage:** `imagine`. **Actor:** `group`; all children propose and the adult facilitates / all children propose, with adult facilitation. **Minutes:** 5 canonical; 3/5/7 per route/canonical; 3/5/7 by path.

**Visual brief IDs:** `VIS-03`.

**Entry / Entrance:** `STATE-BASELINE-OBSERVED`. **Exit:** `STATE-DESIGNS-CHOSEN`.

**Expected result:** each child chooses or draws their own shape after observing the reference; the group identifies the conditions that will remain the same. / Each child chooses or draws an individual shape after observing the baseline; the group identifies the conditions that will remain the same.

**Resume / Resume:** save each drawing with the child's name; upon return, confirm one form per participant. / Save each drawing with the child's name; on return, confirm one shape per participant.

**Warning / Warning:** only choose approved paper forms; do not add tools, fixings, another blade or a different load. / Choose only approved paper shapes; do not add tools, fasteners, another sheet, or a different load.

**`es-US`**1. Remove glass and load. Display the result `PLANA` and ask: “How could we change the shape of a sheet to make it harder to fold?” Record all ideas.
2. Use the tested reference sheet to show just the beginning of an accordion: folding one stripe, flipping, and folding another. Also shows channel diagrams and wide folds; Don't build childish designs.
3. Give each child a planning space. Each person chooses or draws an approved shape for their own sheet and predicts what will happen.
4. Question: “What should remain the same even if each bridge has a different shape?” Confirm paper, 15 cm, glass, 20 crayons and procedure.
5. Order construction and testing shifts. No idea is eliminated because it seems less resistant.

**`en-US`**

1. Remove the cup and load. Keep the `FLAT` result visible and ask: “How could we change one sheet's shape so it is harder to bend?” Remember every idea.
2. Use the tested baseline sheet to demonstrate only the start of an accordion: fold one strip, turn, and fold again. Also show channel and wide-fold diagrams; do not build the children's designs.
3. Give each child planning space. Each chooses or draws one approved shape for an individual sheet and predicts what will happen.
4. Ask: “What must stay the same even when each bridge has a different shape?” Confirm paper, 6 in, cup, 20 crayons, and procedure.
5. Set the build and test order. Do not remove an idea because it seems less strong.

**Success signal:** there is a form identified by child and a common list of fixed conditions; Now every idea can be built. / One identified shape exists per child and there is a shared list of fixed conditions; each idea can now be built.

**Common problem / Common issue:** multiple incompatible ideas. Register them all and choose one in turn; do not combine them in the same test. / If there are several incompatible ideas, record all of them and choose one per turn; do not combine them in one test.

### 9.3 `STEP-03` — Build (5–10 min)

**Stage:** `build_or_do`. **Actor:** `group`; each participant builds an individual sheet with support. **Minutes:** 8 canonical; 5/8/10 per route / canonical; 5/8/10 by path.

**Visual brief IDs:** `VIS-03`.

**Warning:** use only intact paper; do not use scissors or fixings. / Use only intact paper; do not use scissors or fasteners.

**Entry / Entrance:** `STATE-DESIGNS-CHOSEN`. **Exit:** `STATE-CHILD-DESIGNS-READY`.

**Expected result:** There is a structure of one sheet per child, identified with name/design and test orientation. / There is one single-sheet structure per child, identified by child/design and test orientation.

**Resume / Resume:** keep each structure along with its drawing and name; do not stack them or change their orientation. / Keep each structure beside its drawing and name; do not stack it or change its orientation.

**`es-US`**

1. Give each child an identical sheet. Keep the reference/demo sheet separate.
2. One by one, ask them to show their plan and say or point out which way they will try. The adult can mark guides or hold the paper.
3. Each child builds his own shape. For accordion: fold a strip of approximately `2.5 cm / 1 in`, flip and repeat. For channel: lift both long edges. For wide pleats: repeat the sequence with fewer stripes.
4. The child places his or her name or symbol on the recording sheet, not on the bridge test area.
5. Open and orient each structure so that it crosses the space. The adult checks integrity, but does not correct the design to make it “win.”
6. Order the structures according to the agreed shift.

**`en-US`**

1. Give one equal sheet to each child. Keep the baseline/demonstration sheet separate.
2. One at a time, ask each child to show the plan and say or point to the intended shape. The adult may mark guides or hold the paper.
3. Each child builds the chosen shape. For an accordion: fold a strip about `1 in`, turn, and repeat. For a channel: lift both long edges. For wide folds: repeat the sequence with fewer strips.
4. The child adds a name or symbol to the recording sheet, not to the bridge test area.
5. Open and orient every structure so it can span the gap. The adult checks integrity but does not correct a design to make it “win.”
6. Place structures in the agreed test order.

**Success signal:** each child can identify its structure and how it will be placed; Now there are own artifacts ready to try. / Each child can identify an individual structure and its orientation; individual artifacts are now ready to test.

**Common problems / Common issues:**

- Diagonal folds: continue and register; For improvement, straight guides can be marked. / Diagonal folds: continue and record it; straight guidelines may be marked for the improvement.
- Crushed accordion: open it gently without pulling on the ends. / Flattened accordion: open it gently without pulling the ends.
- Difficult motor skills: the adult holds the paper or marks lines; if you create the folds, `OBJ-02` is not evaluated. / Folding is physically difficult: the adult holds the paper or marks lines; if the adult makes the folds, do not assess `OBJ-02`.

### 9.4 Experiment / Experiment (7–12 min)

#### `STEP-04` — Verify and reset / Verify and reset

**Stage:** `experiment`. **Actor:** `adult`. **Minutes:** 2 canonical; 1/2/2 total minutes per route, divided between repeated / canonical verifications; 1/2/2 total minutes by path, shared across repeated checks.

**Visual brief IDs:** `VIS-02`, `VIS-07`.

**Expected result:** immobile supports, 15 cm / 6 in space, towel without initial contact and sheet with similar support on both sides. / Stationary supports, a 15 cm / 6 in gap, no initial towel contact, and similar sheet overlap on both sides.

**Success signal:** the adult and the child whose turn begins confirm the conditions; only the adult has moved the supports. / The adult and the child whose turn begins confirm the conditions; only the adult has moved the supports.

**Resume / Resume:** repeat all `STEP-04` after a pause and before each design. / Repeat all of `STEP-04` after a pause and before every design.

**Warning / Warning:** only the adult places and readjusts supports; do not stack, lift or hold a book by hand while loading. / Only the adult places and resets supports; do not stack, raise, or hold a book by hand during loading.

**Common problem:** If the markings do not match or the supports differ in height, do not compensate with objects; correct the pair or mark `invalid_setup`. / If marks do not align or supports differ in height, do not compensate with objects; correct the pair or mark `invalid_setup`.

- **`es-US`:** The adult confirms the space and the towel, places the design with similar support and gives the ready signal. Between tests, remove the glass and load, restore the supports and repeat the verification.
- **`en-US`:** The adult confirms the gap and towel, places the design with similar overlap, and gives the ready signal. Between tests, the adult removes the cup and load, resets the supports, and repeats the check.

#### `STEP-05` — Load, observe, and record

**Stage:** `experiment`. **Actor:** `group`; each child tests in turn. **Minutes:** 8 canonical; 6/8/12 per route / canonical; 6/8/12 by path.

**Visual brief IDs:** `VIS-04`, `VIS-05`, `VIS-07`.

**Entry / Entrance:** `STATE-CHILD-DESIGNS-READY`. **Exit:** `STATE-CHILD-RESULTS-RECORDED`.

**Expected result:** the cheat sheet and each child design produce a result `0–20+` under valid assembly or `No comparable` with cause; Each child performed their own test. / The baseline and every child design produces a `0–20+` result under a valid setup or `Not comparable` with a cause; every child ran an individual test.

**Resume / Resume:** record layout, result and status before pausing; when returning, start from `STEP-04`, not from a partial load. / Record design, result, and status before pausing; on return, restart from `STEP-04`, not from a partial load.

**Warning / Warning:** no one brings their face or hands under the assembly; put down, don't let go, one crayon at a time; apply `safe_stop` upon a stop condition. / No one puts a face or hands under the setup; lower rather than drop one crayon at a time; apply `safe_stop` for any stop condition.

**`es-US`**

1. Keep the result `PLANA` visible. Take the first child structure and name the turn: [child] design.
2. The adult completes `STEP-04`, places the structure and centers the empty glass. The child on the turn confirms his form and waits for the signal.
3. The child lowers a crayon completely into the glass, says the number and waits three seconds. Alternate side of center; He doesn't let it fall. Others watch where it bends and whether a condition changes.
4. When a failure occurs, the adult applies 4.
1. In `bridge_deformation`, record the last stable quantity; in `invalid_setup`, does not register number and resets only once.
5. The child on duty says or points out what he observed on his bridge. Record design, result, comparability and observation before removing the sheet.
6. Repeat from `STEP-04` for each participant. Observing someone else's test is no substitute for doing your own.
7. When everyone has tested, compare valid results using `more`, `less`, or `the same`; if a design holds 20, record `20+`.

**`en-US`**

1. Keep the `FLAT` result visible. Take the first child structure and name the turn: [child]'s design.
2. The adult completes `STEP-04`, places the structure, and centers the empty cup. The child confirms the shape and waits for the signal.
3. The child lowers one crayon fully into the cup, says the number, and waits three seconds. Alternate sides of center; do not drop it. Others watch where it bends and whether a condition changes.
4. When a failure occurs, the adult applies 4.
1. For `bridge_deformation`, record the last stable amount; for `invalid_setup`, record no number and reset only once.
5. The child says or points to what happened to the bridge. Record design, result, comparability, and observation before removing the sheet.
6. Repeat from `STEP-04` for every participant. Watching another test does not replace running one's own.
7. After everyone tests, compare valid results using `more`, `less`, or `the same`; if a design holds 20, record `20+`.

**Success signal:** there is one result or honest observation per participant and at least two results can be compared; now improvement can be based on real evidence. / A result or honest observation exists for every participant and at least two results can be compared; improvement can now use real evidence.

**Common problem:** If the glass tilts between ridges, it does not restart automatically; the adult decides between `invalid_setup` and `bridge_deformation` according to 4.
1. / If the cup tips between ridges, do not automatically restart; the adult chooses `invalid_setup` or `bridge_deformation` under 4.1.

### 9.5 `STEP-06` — Improve (3–11 min)

**Stage:** `improve`. **Actor:** `group`; everyone proposes and shares building/testing. **Minutes:** 6 canonical; 3/6/11 per route / canonical; 3/6/11 by path.

**Visual brief IDs:** `VIS-08`.

**Entry / Entrance:** `STATE-CHILD-RESULTS-RECORDED`. **Exit:** `STATE-IMPROVEMENT-TESTED`.

**Expected result:** A group sheet incorporates exactly one change based on the child results and produces a valid or documented `No comparable` result. / One group sheet incorporates exactly one change based on the children's results and produces a valid result or a documented `Not comparable` state.

**Resume / Resume:** draw the chosen improvement and save the sheet without loading; when you return, repeat `STEP-04`. / Draw the chosen improvement and store the unloaded sheet; on return, repeat `STEP-04`.

**Warning / Warning:** do not combine changes or increase weight, height or separation; the adult retains control of supports and classification of faults. / Do not combine changes or increase weight, height, or gap; the adult retains control of supports and failure classification.

**`es-US`**

1. Place the results table and unloaded layouts together. Each child responds: “What would you change after seeing your test and why?”
2. Record the three recommendations. The group chooses a single approved change: width, number or straightness of folds, or raised longitudinal edges.
3. Use the sheet reserved for improvement. Each child performs a compatible part: marking/indicating the change, folding with support and checking that it matches the decision.
4. Everyone predicts whether it will hold more, less, or the same as a previous result and names which one they will compare it to.
5. Repeat `STEP-04/05`: in turns, one confirms the change, another adds/counts load and another monitors conditions; These functions rotate and do not replace the own tests already carried out.
6. Record the result even if it holds less or is not comparable. In 60 minutes, repeat the improvement only if the number of participants left one canonical sheet unused; With three children, deepen the comparison without adding paper.

**`en-US`**

1. Place the result table and unloaded designs together. Each child answers: “After seeing your test, what would you change and why?”
2. Remember all recommendations. The group chooses one approved change: fold width, number, or straightness, or raised long edges.
3. Use the reserved improvement sheet. Each child performs a compatible part: mark/name the change, fold with support, and verify that it matches the decision.
4. Everyone predicts whether it will hold more, less, or the same as one prior result and names the comparison.
5. Repeat `STEP-04/05`: in turn, one confirms the change, one adds/counts load, and one watches conditions; these functions rotate and do not replace the individual tests already completed.
6. Record the result even if it holds less or is not comparable. On a 60-minute path, repeat the improvement only when participant counts left one canonical sheet unused; with three children, deep comparison without adding paper.

**Success signal:** the group changes a variable in form, tests and preserves the result without calling it personal success or failure. / The group changes one shape variable, tests it, and keeps the result without framing it as personal success or failure.

**Common problem / Common issue:** If you want to change several things, draw the ideas and choose one; the rest are left for another sheet or session. / If the group wants to change several things, draw the ideas and choose one; save the others for another sheet or session.

### 9.6 `STEP-07` — Explain (1–3 min)

**Stage:** `explain`. **Actor:** `group`; the adult listens and asks an evidence question. **Minutes:** 2 canonical; 1/2/3 per route/canonical; 1/2/3 by path.

**Visual brief IDs:** `VIS-05`, `VIS-06`.

**Entry / Entrance:** `STATE-IMPROVEMENT-TESTED`. **Exit:** `STATE-EXPLANATION-SHARED`.

**Expected result:** each child connects their own test or group improvement with something seen or told; the family retains unexpected results. / Every child connects an individual test or the group improvement to something seen or counted; the family keeps unexpected results.

**Resume:** can be completed later using the results sheet; indicate that the explanation was deferred. / It may be completed later using the results sheet; mark that explanation was deferred.

**Warning / Warning:** the designs are unloaded and the supports are no longer manipulated; do not present the number as the child's score. / Designs are unloaded and supports are no longer handled; do not frame the number as a child's score.

**`es-US`**

1. Place the unloaded designs together, each one next to its result, and the group improvement at the end.
2. Take turns asking each child: “On your bridge, what did you do and what did you see or tell?” Agree to point, draw or choose.
3. Question: "What did you recommend changing after your test? Where does that idea appear in the group improvement?"
4. Ask the group: “What did we keep the same so we could compare?”
5. You connect your words to shape, load, and bending without stating that more folds are always better. Celebrate completing question, design, test and improvement, not the highest number.

**`en-US`**

1. Put the unloaded designs beside their results, with the group improvement last.
2. In turn ask each child: “In your bridge, what did you do and what did you see or tell?” Accept pointing, drawing, or choosing.
3. Ask: "What change did you recommend after your test? Where can we see that idea in the group improvement?"
4. Ask the group: “What did we keep the same so we could compare?”
5. Connect their words to shape, load, and bending without claiming that more folds are always better. Celebrate completing the question, design, test, and improvement—not the highest number.

**Success signal:** each child identifies their own action and a result; the explanation closes the cycle that began with the flat sheet. Scientific vocabulary is not required. / Every child identifies an individual action and result; the explanation closes the cycle that began with the flat sheet. Scientific vocabulary is not required.

**Common problem:** a child repeats the adult explanation; go back to “what did you see or tell?” and accept gesture, drawing or choice without correcting towards a model sentence. / A child repeats the adult explanation; return to “what did you see or count?” and accept a gesture, drawing, or choice without correcting toward a model sentence.

## 10. Explanations

### 10.1 Brief adult explanation

**`es-US`:** The shape changes how the paper is folded. A flat sheet flexes easily; the folds create ridges and small walls that can help the sheet retain its shape and distribute the load. The test should keep the paper, spacing, cup, and charge the same to attribute the difference primarily to shape.

**`en-US`:** Shape changes how paper bends. A flat sheet flexes easily; folds create ridges and small walls that can help the sheet keep its shape and distribute the load. The test must keep the paper, gap, cup, and load the same so the difference can be attributed mainly to shape.

### 10.2 Detailed adult explanation

**`es-US`:** Flexural stiffness depends on the material and the geometry of the section. Since the sheets come from the same package, the variable we are looking to change is the geometry. When folded, part of the paper is further away from the central area where the structure curves and walls appear that resist deformation. This can increase the rigidity of the assembly without changing the material. The result also depends on the direction, uniformity and damage of the folds; of the place where the load is applied; of space; and the stability of the supports. That's why an accordion is not guaranteed to outperform the flat sheet. An unexpected piece of information invites you to check the assembly and repeat it, not to replace it with the expected result.

**`en-US`:** Bending stiffness depends on both the material and the geometry of its cross-section. Because the sheets come from the same package, geometry is the variable we intend to change. Folding moves some paper further from the central region where the structure bends and creates walls that resist deformation. This can increase the stiffness of the structure without changing the material. The result also depends on fold direction, uniformity, and damage; loadplacement; gapwidth; and support stability. An accordion is therefore not guaranteed to outperform the flat sheet. An unexpected result is a reason to check the setup and repeat—not to replace the data with the expected result.

### 10.2.1 Practical guide for the adult to follow the design

This guide helps the adult ask questions and show possibilities without designing the bridge for the child.

**`es-US`:**

1. Start with the flat sheet and ask, “Where is it bending?” and “How could we make part of the paper stand up instead of completely lying down?”
2. If the child doesn't have an idea, use the planning sheet to show **a single example fold**, not the entire bridge. Then return the decision: “Do you want to repeat it, make it wider or try another shape?”
3. Offers as possibilities, not as answers: an accordion with repeated mountains and valleys; long edges raised like a channel; wider or narrower folds; or guides so that the folds are straight.
4. Before trying, ask: “Do the ridges go from one book to the other?” The ridges that cross the space can function as small walls; if they go from side to side of the bridge, they may not help in the same way.
5. Helps make defined, uniform folds without tearing the paper. Don't say "more pleats are always better": too many small pleats can squish or become uneven.
6. After the test, go back to the evidence: “What did you change?”, “Where did it bend?” and “What would you try now?” The goal is to iterate, not guess the winning design.

**`en-US`:**

1. Begin with the flat sheet and ask, “Where is it bending?” and “How could we make part of the paper stand up instead of lying completely flat?”
2. If the child has no idea, use the planning sheet to demonstrate **one sample fold**, not the complete bridge. Return the choice: “Would you like to repeat it, make it wider, or try another shape?”
3. Offer possibilities rather than answers: an accordion with repeating peaks and valleys; raised long edges forming a channel; wider or narrower folds; or guidelines that help keep folds straight.
4. Before testing, ask, “Do the ridges run from one book to the other?” Ridges that span the gap can act like small walls; Ridges running across the bridge may not help in the same way.
5. Support crisp, even folds without tearing the paper. Do not say “more folds are always better”: too many small folds may flatten or become uneven.
6. After the test, return to evidence: “What did you change?”, “Where did it bend?” and “What would you try next?” The goal is iteration, not guessing the winning design.

### 10.3 Children's explanation

**`es-US`:** "The paper is still paper, but its shape has changed. The ridges are like many small walls that can help it not bend as quickly. The test tells us what happened to our shapes."

**`en-US`:** “The paper is still paper, but its shape changed. The ridges are like many small walls that can help it keep from bending as quickly. The test tells us what happened with our shapes.”

### 10.4 Expected physical observations, no guarantee

**`es-US`:** It is common for the flat sheet to sag or lose stability with little load and for a well-oriented accordion to remain stable with more crayons. It is also possible to obtain a tie or the accordion to hold less due to flattened, diagonal or uneven folds, due to an off-center load or due to movement of the supports. More folds don't always mean better performance. Actual observation of the family prevails over this common pattern.

**`en-US`:** It is common for the flat sheet to sag or lose stability with a small load and for a well-oriented accordion to remain stable with more crayons. A tie is also possible, or the accordion may hold less because folds are flattened, diagonal, or uneven, the load is off-center, or the supports move. More folds do not always mean better performance. The family's current observation takes precedence over this common pattern.

### 10.5 Minimum recording sheet

| Design / Design | Prediction / Prediction | Stable crayons / Stable crayons | What we observe / What we observed |
|---|---|---:|---|
| Flat / Flat | More / Less / Same / More / Less / Same | 0–20+ | Curvature, sliding or stability / Bending, slipping, or stability |
| Accordion / Accordion | More / Less / Same / More / Less / Same | 0–20+ | Direction and evenness of folds / Fold direction and evenness |
| Improvement / Improvement | More / Less / Same / More / Less / Same | 0–20+ | Chosen change and result / Chosen change and result |

## 11. Troubleshooting / Troubleshooting

| Situation / Situation | `es-US` | `en-US` | Impact on evidence / Evidence impact |
|---|---|---|---|
| Books move | Stop the test. The adult returns the books to their marks, checks 15 cm / 6 in, and restarts that design from scratch. | Stop the test. The adult returns the books to their marks, checks 15 cm / 6 in, and restarts that design from scratch. | Do not use the interrupted result for comparison. |
| The glass tilts / Cup tips | Don't reboot automatically. The adult applies 4.1: if there was uneven mounting or external loading, `invalid_setup`; if the paper was warped under a valid mount, `bridge_deformation`. | Do not restart automatically. The adult applies 4.1: external setup or even loading means `invalid_setup`; paper deformation under a valid setup means `bridge_deformation`. | `invalid_setup` produces no score or negative evidence; `bridge_deformation` retains the last stable charge. / `invalid_setup` produces no score or negative evidence; `bridge_deformation` keeps the last stable load. |
| Crayons roll or fall / Crayons roll or fall | Wait for everything to stop and classify the cause: fall after valid deformation = `bridge_deformation`; crayon dropped out of cup or hit = `invalid_setup`; throw, break or material in the mouth = `safe_stop`. | Wait until everything stops and classify the cause: a fall after valid paper deformation = `bridge_deformation`; a crayon dropped outside the cup or a bump = `invalid_setup`; throwing, breakage, or mouthing = `safe_stop`. | Only `bridge_deformation` retains the last stable charge; never guess the total or attribute the fault to the child. / Only `bridge_deformation` keeps the last stable load; never guess the count or attribute the failure to the child. |
| The flat sheet holds 20 / Flat sheet holds 20 | Register `20+`. Don't add weight. Increasing space is not approved as an automatic adaptation for this version. Compare visible deformation or repeat in another versioned session. | Record `20+`. Do not add weight. Increasing the gap is not approved as an automatic adaptation in this version. Compare visible bending or repeat in another versioned session. | Do not infer that there was no learning. / Do not infer that no learning occurred. |
| Both designs give the same result / Both designs match | Check conditions and accept the tie. Ask what new test would help you learn more. | Check the conditions and accept the tie. Ask what new test would help you learn more. | A tie is valid evidence of this test. / A tie is valid evidence from this test. |
| The accordion holds less / Accordion holds less | Check orientation, damage and uniformity. If the test was fair, keep the data and explore improvement. | Check orientation, damage, and evenness. If the test was fair, keep the result and explore an improvement. | Do not substitute an editorial expectation. / Do not replace it with an editorial expectation. |
| Folding is difficult / Folding is difficult | Mark guides, stabilize the paper, or allow the child to direct the adult. Change the goal if it hasn't started yet; if it has already started, record real support. | Mark guidelines, stabilize the paper, or let the child direct the adult. Change the objective if the session has not started; otherwise record the current support. | Do not assess accuracy if the adult created the folds. / Do not rate folding accuracy if the adult made the folds. |
| A child does not want to participate / A child does not want to participate | Offer to observe, draw, or leave. Confirm non-participation at closing. | Offer observing, drawing, or opting out. Confirm nonparticipation at close. | No presentation or main assessment if you did not participate. / No exposure or primary rating when the child did not participate. |
| Children compete for the load / Children compete for the load | Remember that shapes are compared and that each child will have their own test. Maintain visible order; only the child on duty adds load. | Remind them that shapes are compared and every child will run an individual test. Keep the order visible; only the child whose turn it is adds load. | Do not interpret conflict as ability or interest. / Do not interpret conflict as skill or interest. |

## 12. Approved adaptations and extensions

When this version reaches `published`, the AI will be able to choose only these options without creating a new version. You cannot combine options that simultaneously change more than one test variable. While `draft` remains, no options are available for family referral.

Once this version reaches `published`, AI may choose only these options without creating a new version. It may not combine options that change more than one test variable at the same time. While it remains `draft`, no option is available for family recommendation.

| ID/type | Condition / Condition | Change / Change | Limit / Limit | `safetyImpact` | Adult confirmation |
|---|---|---|---|---|---:|
| `ADAPT-BRIDGE-NARRATIVE` / `presentation` | Narrative interest / Narrative interest | Present that the bridge crosses an imaginary river. / Frame the bridge as crossing an imaginary river. | Do not add toys, change materials, scoring or security. / Do not add toys or change materials, scoring, or safety. | `none` | No |
| `ADAPT-BRIDGE-VISUAL-SEQUENCE` / `simplification` | L1 or sequencing difficulty / L1 or sequencing difficulty | Use diagram and mark guides every 2.5 cm / 1 in. / Use the diagram and mark guides every 2.5 cm / 1 in. | If the adult folds, `OBJ-02` is no longer evaluable. / If the adult folds, `OBJ-02` is no longer assessable. | `none` | Yes / Yes |
| `ADAPT-BRIDGE-MOTOR-ACCESS` / `role` | Fatigue or motor access / Fatigue or motor access | The adult stabilizes the paper; the child presses with the palm or directs by speaking or pointing. / The adult stabilizes the paper; the child presses with a palm or directs by speaking or pointing. | Register support and reassign the objective before starting if necessary. / Record support and reassign the objective before starting if needed. | `reduced` | Yes / Yes |
| `ADAPT-BRIDGE-LANGUAGE-ACCESS` / `presentation` | Emerging expressive language / Emerging expressive language | Allow pointing, using more/less/equal cards or responding with a gesture. / Allow pointing, more/less/same cards, or gestures. | `OBJ-06` requires a statement communicated by any modality, not a spoken phrase. / `OBJ-06` requires a communicated claim in any mode, not a spoken sentence. | `none` | No |
| `ADAPT-BRIDGE-COUNT-GROUPS` / `simplification` | The total is lost / Count is lost | Line up the removed crayons outside the cup in visual groups of five after each trial. / After each test, align removed crayons outside the cup in visual groups of five. | During the test one enters at a time; record support and never remove a partial load for bundling. / During a test, one enters at a time; record support and never remove a partial load to group it. | `none` | No |
| `ADAPT-BRIDGE-DIFFICULTY` / `difficulty` | Initial or strong evidence | Measure fold width, justify a controlled variable or repeat the best design. / Measure fold width, justify a controlled variable, or repeat the best design. | Do not add weight, height, adhesives, separation or risk. / Do not add weight, height, adhesives, gap, or risk. | `none` | Yes / Yes |
| `ADAPT-BRIDGE-PAUSE` / `duration` | Need for pause / A pause is needed | Pause after a phase, photograph only the setup if the adult chooses or record results, and label materials. / Pause after a stage, photograph only the setup if the adult chooses or write results, and label materials. | When repeating `STEP-04`; the photo is not saved by default. /On return repeat `STEP-04`; the photo is not saved by default. | `none` | Yes / Yes |
| `ADAPT-BRIDGE-MATERIAL` / `material` | Canonical paper, support, ruler, writing tool, tape, or towel is unavailable | Use only the express substitution of the corresponding row in 5.
1. / Use only the explicit substitute in that material's row in 5.
1. | Do not replace glass or load; use only one type of paper and support during the session. /Do not replace cup or load; use one paper and support type throughout the session. | `reviewed_equivalent` | Yes / Yes |
| `ADAPT-BRIDGE-REPEAT` / `extension` | 60-minute path with one or two participants | Use an unassigned canonical sheet to repeat the improvement and explore repeatability. / Use an unassigned canonical sheet to repeat the improvement and explore repeatability. | Do not add a seventh sheet with three participants; maximum 20 crayons per test. / Do not add a seventh sheet with three participants; no more than 20 crayons per test. | `none` | Yes / Yes |

### 12.1 Prohibited adaptations

- Increase the load above 20 canonical crayons or use another item. / Increase the load beyond the 20 canonical crayons or use another object.
- Raise supports, stack books or try on an open space. / Raise supports, stack books, or test over an open space.
- Increase space as an automatic response to “too easy.” / Increase the gap as an automatic response to “too easy.”
- Wet, heat, cut or perforate the paper. / Wet, heat, cut, or puncture the paper.
- Add tape, glue, staples, clips, string or a second sheet to a core design. / Add tape, glue, staples, clips, string, or a second sheet to a core design.
- Replace glass, supports or load outside of express substitutions and approved gates. / Replace the cup, supports, or load outside explicit substitutions and approved gates.
- Ask the child to move books or hold a stand during carrying. / Ask a child to move books or hold a support during loading.

## 13. Cleanup and storage

### `STEP-08` — Adult teardown

- **Stage:** `cleanup`; **actor:** `adult`; **minutes:** 1 canonical; included in the budget 2/3/4 cleaning / canonical; included in the 2/3/4 cleanup budget.
- **Visual brief IDs:** none / none.
- **Expected result:** glass and crayons remain on a clear area; the supports are stored without child intervention. / The cup and crayons are on a clear area; supports are stored without child handling.
- **Success signal:** No children move supports or remain under the assembly. / No child moves supports or remains under the setup.
- **Resume / Resumption:** if interrupted, leave everything still until the adult returns. / If interrupted, leave everything stationary until the adult returns.
- **Warning / Warning:** the adult first removes the glass and loads it, checks that there are no hands nearby and only then moves the supports. / The adult first removes the cup and load, checks that no hands are nearby, and only then moves the supports.
- **Common problem:** a crayon falls; stop disassembling, wait for everything to be still and pick it up before moving books. / A crayon falls; stop teardown, wait until everything is still, and collect it before moving books.
- **`es-US`:** Remove the glass, empty the crayons onto a clear area and put away the two holders.
- **`en-US`:** Remove the cup, empty the crayons onto a clear area, and store both supports.

### `STEP-09` — Group cleanup

- **Stage:** `cleanup`; **actor:** `group`; **minutes:** 2 canonical; 1/2/3 per route/canonical; 1/2/3 by path.
- **Visual brief IDs:** none / none.
- **Expected result:** the 20 crayons are counted and the area is dry and clear. / All 20 crayons are accounted for and the area is dry and clear.
- **Success signal:** There are no pieces, wet marks or obstacles left on the table or passage area. / No pieces, wet marks, or obstacles remain on the table or walkway.
- **Resume / Resume:** start again by counting the 20 crayons. / Resume by recounting all 20 crayons.
- **Warning / Warning:** the adult collects and discards fragments; children manipulate only intact materials. / The adult collects and discards fragments; children handle intact materials only.
- **Common problem / Common problem:** a crayon is missing; check glass, towel and floor with children still. / A crayon is missing; check the cup, towel, and floor while children stay still.

**`es-US`**

1. Count the 20 crayons and put them away.
2. Children can stack sheets and keep materials intact; the adult removes fragments.
3. Recycle clean paper according to local rules or save a design to explain later.
4. Clean washable marks and leave the passage area clear.

**`en-US`**

1. Count and store all 20 crayons.
2. Children may stack sheets and store intact materials; the adult removes fragments.
3. Recycle clean paper according to local rules or keep one design to explain later.
4. Wipe away washable marks and leave the walkway clear.

## 14. Closure and evidence

### 14.1 Default path

At close-out, show only the children who participated. For each child, ask the question tied to that child's single primary objective and offer a one-tap 1–5 rating. The default path does not assess every exposure. **Evaluate more** remains secondary. One voice or text note for the entire session is optional.

If the objective could not be observed, use **Could not observe**. This does not equal a rating of 1. An assembly problem is recorded as context, not as a child's difficulty.

The adult can skip the closure, complete it later, correct a response, or delete the remark. Omitting does not create negative evidence. / The adult may skip the close, complete it later, correct an answer, or delete the observation. Skipping does not create negative evidence.

### 14.2 Anchors 1–5 bilingual

| Value | `es-US` | `en-US` |
|---:|---|---|
| 1 | He couldn't do it yet, even with reasonable support. | Could not do it yet, even with reasonable support. |
| 2 | He did it with a lot of help. | Did it with substantial help. |
| 3 | He did it with some help. | Did it with some help. |
| 4 | He did it almost single-handedly. | Did it almost independently. |
| 5 | He did it without help and safely. | Did it independently and safely. |

The scale describes independence in this action and context; it does not measure intelligence, value or a global level.

### 14.3 Rubrics by objective

#### `ACT-0001-OBJ-01` — One-to-one correspondence

- **Question `es-US`:** “How independently were [name] able to add one crayon at a time and keep counting?”
- **Question `en-US`:** “How independently could [name] add one crayon at a time and keep track of the count?”
- **Counts as evidence / Counts as evidence:** one piece per turn, total counted or recovered, result communicated. / One item per turn, a count maintained or recovered, and a communicated result.
- **Does not count:** recite numbers without corresponding them to pieces; the adult adds and tells; passive exposure. / Reciting numbers without matching them to items; the adults adding and counting; passive exposure.
- **External factors:** falling pieces, interruption by another child, restart not signaled, hearing or speech difficulty not accommodated. / Falling items, another child's interruption, an unmarked restart, or unaccommodated hearing or speech access.

#### `ACT-0001-OBJ-02` — Folding sequence

- **Question `es-US`:** “How independently was [name] able to follow the sequence of folds and place the structure?”
- **Question `en-US`:** “How independently could [name] follow the folding sequence and place the structure?”
- **Counts as evidence:** alternates orientation, continues the sequence and places ridges in the direction of the space with the registered support. / Alternates orientation, continues the sequence, and places ridges toward the gap with recorded support.
- **Does not count:** the adult completes the folds; evaluate only the final appearance; confuse motor precision with understanding of the sequence. / The adult completes the folds; rating only final appearance; confusing motor precision with sequence understanding.
- **External factors:** damaged paper, inconspicuous lines, fatigue or motor adaptation. / Damaged paper, hard-to-see lines, fatigue, or a motor adaptation.

#### `ACT-0001-OBJ-03` — Compare results

- **Question `es-US`:** “How independently could [name] use the results to say which design held more, less, or the same?”
- **Question `en-US`:** “How could [name] independently use the results to say which design held more, less, or the same?”
- **Counts as evidence / Counts as evidence:** compares the two numbers, collections or marks by word, gesture or visual selection. / Compares two numbers, collections, or marks using words, gestures, or a visual choice.
- **Does not count:** choose the preferred design without using results; repeat another person's response without a hint of comparison. / Choosing a preferred design without results; repeating another person's answer without evidence of comparison.
- **External factors:** lost result, non-comparable tests, inaccessible registration symbols. / A lost result, noncomparable tests, or inaccessible recording symbols.

#### `ACT-0001-OBJ-04` — Fair Test

- **Question `es-US`:** “How independently was [name] able to help keep the separation, vessel, and way of adding the load the same?”
- **Question `en-US`:** “How independently could [name] help keep the gap, cup, and loading method the same?”
- **Counts as evidence:** remembers or checks at least two conditions and requests to correct one that changed. / Remembers or checks at least two conditions and asks to correct one that changed.
- **Does not count:** observe the adult prepare everything; affirm that it was fair without identifying conditions. / Watching the adults prepare everything; saying it was fair without identifying conditions.
- **External factors:** the adult restarts without involving the child, absent marks, accidental change of material. / The adult resets without involving the child, position marks are absent, or material changes accidentally.

#### `ACT-0001-OBJ-05` — Design an improvement

- **Question `es-US`:** “How independently was [name] able to propose a shapeshift, build it, and test it?”
- **Question `en-US`:** “How could [name] independently propose a shape change, build it, and test it?”
- **Counts as evidence:** Choose a specific change, participate in building it, and use the test to find out what happened. / Chooses a specific change, participates in building it, and uses the test to learn what happened.
- **Does not count:** decorate without changing structure; the adult chooses and builds; demand that the result exceed the previous one. / Decorating without structural change; the adult choosing and building; requiring the result to beat the prior one.
- **External factors:** lack of sheet, insufficient time, motor difficulty not accommodated, shift conflict. / Missing paper, insufficient time, unaccommodated motor access, or a turn conflict.

#### `ACT-0001-OBJ-06` — Explain with evidence

- **Question `es-US`:** “How independently could [name] use something he saw or told to explain an idea about the bridge?”
- **Question `en-US`:** “How could [name] independently use something they saw or counted to explain an idea about the bridge?”
- **Counts as evidence / Counts as evidence:** communicates a statement and relates it to an observation or result, by voice, gesture, drawing or accessible selection. / Communicates a claim and links it to an observation or result through voice, gesture, drawing, or an accessible choice.
- **Does not count / Does not count:** memorize the adult explanation; name the design without evidence; demand complete scientific causality. / Memorizing the adult explanation; naming a design without evidence; requiring complete scientific causality.
- **External factors / External factors:** directed question, lack of time, language not accommodated, another child answers first. / A leading question, lack of time, unaccommodated language access, or another child answering first.

### 14.4 Optional note and normalizationExample note `es-US`: "Maya found it difficult to fold, but she pointed out that we should put the glass in the same place. Leo counted up to twelve by himself and then asked for help."

Example note `en-US`: "Folding was difficult for Maya, but she pointed out that we should put the cup in the same place. Leo counted independently to twelve and then asked for help."

Normalization can propose two separate and contextual observations. You should not turn them into “Maya is logical” or “Leo has a low level.” The transcript can be edited; ambiguous attribution requires confirmation. Audio is deleted upon successful transcription or upon expiration of its operating maximum, and the editable transcript expires according to current policy.

Normalization may propose two separate contextual observations. It must not turn them into “Maya is logical” or “Leo is low level.” The transcript is editable; ambiguous attribution requires confirmation. Audio is deleted after successful transcription or its operational maximum, and the editable transcript expires under the current policy.

## 15. Required visual resources

All assets remain in state `planned` until generation, automatic QA and human approval. Text and figures are rendered as controlled layers; they are not part of the generated image. No assets show faces, trademarks or identifiable information.

| AssetID | Type/style | Step/purpose | Canonical Brief | Required / prohibited | Alt text `es-US` | Alt text `en-US` |
|---|---|---|---|---|---|---|
| `VIS-01` | Photorealistic Materials board | Materials list | Top-down view on a neutral background: six letter or A4 sheets stacked, two separate hardcover books, empty paper cup, 20 intact crayons arranged, ruler, pencil, spread towel and, in a separate box, four pieces of removable tape with “Optional / Optional” overlay | Show verifiable quantities and only materials from this version; distinguish optional ribbon; no text generated within the image, charge substitutions, scissors, glass or child's hands | Required paper bridge materials and optional ribbon arranged from the top. | Required paper bridge materials and optional tape arranged from above. |
| `VIS-02` | Photorealistic preparation | Preparation/Discover | Low and firm table; towel under a space between two flat books; ruler showing separation; flat blade resting on both; adult hands adjusting a book | Display 15 cm / 6 in via overlay; adult actor; without stacked books or loaded glass | An adult sets two flat books 15 centimeters apart, with a towel underneath and a sheet of paper across the space. | An adult adjusts two flat books 6 inches apart, with a towel underneath and a sheet crossing the gap. |
| `VIS-03` | Instructional diagram, 6 panels | Imagine/Build | Three approved options—accordion, channel, and wide pleats—followed by the accordion sequence: first 2.5 cm / 1 in. pleat, flip/repeat, and open with longitudinal ridges | Present options, not a correct answer; arrows and numbers as overlays; no scissors, tape or fake adult-only hands | Shape options and steps for folding a sheet accordion with ridges along its length. | Shape options and steps for accordion-folding a sheet with lengthwise ridges. |
| `VIS-04` | Instructional diagram | Experiment | Glass centered on low bridge; a child's hand gently lowers a crayon into the glass; 19 remaining in a row; towel under space; flat books | Show only child action allowed; the crayon does not fall; without faces, substitute loads or hands under supports | A hand lowers a crayon into the glass centered on the bridge, with a towel underneath. | A hand lowers one crayon into the cup centered on the bridge, with a towel underneath. |
| `VIS-05` | Photorealistic expected result, 4 panel sequence | Experiment/Explain | The same setup, camera and glass show flat reference and three different child shapes, one at a time; each panel has external space for symbol/name and result, with no number generated inside the image | Overlay “Same setup; one turn per design; results may vary”; do not duplicate supports, promise superiority or show impossible physics | Four turns of the same assembly show a flat reference and three children's designs tested separately. | Four turns on the same setup show a flat baseline and three child designs tested separately. |
| `VIS-06` | Conceptual diagram, not to scale | Explanation | Cross sections: flat leaf and ridged leaf; loading arrows down; small vertical walls highlighted | Check “diagram, not to scale”; separate bilingual overlays; no equations required | Diagram not to scale compares a flat sheet with ridges that form small walls under a load. | Not-to-scale diagram compares a flat sheet with ridges that form small walls under a load. |
| `VIS-07` | Troubleshooting, comparative diagram | Failures | Three panels: valid assembly; `invalid_setup` with displaced support or initially offset cup; `bridge_deformation` with curved paper before tilting the glass | Cross/check and tags as controlled overlays; do not show fall near a child or suggest automatic restart | Comparison between valid assembly, invalid assembly and deformation of the bridge. | Comparison of a valid setup, an invalid setup, and bridge deformation. |
| `VIS-08` | Instructional diagram | Improve | Four separate options: wider, narrower pleats, straight guides and long raised edges; each uses a single sheet | Present as options, not guaranteed results; without combining them in a design | Four shape changes approved to test a single blade improvement. | Four approved shape changes for testing an improvement with one sheet. |

### 15.1 Specific visual QA checklist

- Automatic counting confirms six sheets and 20 crayons in `VIS-01`.
- The books are flat and the space is on a table in all setups.
- The ridges cross from one support to the other; they do not cross the space laterally.
- The glass appears empty at the beginning and receives only the approved load.
- No images add stickers, clips, coins, glass or weight not allowed.
- `VIS-05` is validated as a possible result, not a guarantee.
- Bundles use the same physical asset when applicable and overlays/alt text reviewed by language.
- `VIS-05` is interpreted as two sequential moments of the same set of materials, never as two simultaneous assemblies.
- `VIS-07` visually differentiates `invalid_setup` from `bridge_deformation` without attributing a cause that the image does not allow to verify.
- Model/provider, brief, QA result, approver, date, and link to `ACT-0001@0.3.0` are recorded.

## 16. Version acceptance criteria

- An adult can prepare the assembly only with the list and `VIS-01`/`VIS-02`.
- The 30, 45 and 60 minute routes retain Discover–Imagine–Build–Experiment–Improve–Explain.
- One-, two-, and three-child configurations assign exactly one primary objective per child and allow each participant to propose, build, test, observe, and recommend an improvement.
- The closing flow requires one touch per participant and can be completed in less than 20 seconds for three children in usability testing.
- Exposures can be recorded without converting them into evidence of independence.
- `invalid_setup`, `bridge_deformation` and `safe_stop` produce different states; only one valid test produces a score and none by itself produces a negative evaluation of the child.
- The activity can be carried out without scissors, coins, stickers on the bridge or a network connection.
- Cup and charge have no substitutions in 0.3.0; any alternative is rejected or a new version created after validation.
- No approved adaptation increases height, energy, weight, temperature, pressure, toxicity or speed.
- The `es-US` and `en-US` bundles communicate the same mechanism and safety controls.
- Each `STEP-00`–`STEP-09` declares actor, stage, time, input/output status, expected result, success signal, resume, warning and common problem; the references comply with the mapping of 1.2.
- The exit of each phase coincides with the entry of the next and the table walkthrough confirms the cup/crayons function and a test per child.
- A JSON instance of 0.3.0 validates against the schema in effect before `ready_for_pilot`.
- A result equal to or contrary to the expectation remains valid and is not replaced by a guaranteed conclusion.

## 17. Traceability

| Rule of this ActivityVersion | Principles and source requirements | Planned verification |
|---|---|---|
| Versioned and non-publishable library without gates | P-03, P-14, ACT-001, ACT-002, ACT-006, ACT-007 | Status, review records and exact session reference |
| One sheet, same separation and same load | P-01, LRN-001, ACT-003 | Observed execution and fair test checklist |
| Meaningful roles 1–3 children | P-05, ACT-004, ACT-008 | Individual pilots, two children and three children |
| One goal per child; other skills like exposure | P-06, LRN-006, EVD-001, EVD-002 | Allocation Restriction and Timed Closing |
| Contextual scale and omission | P-07, EVD-003, EVD-004, EVD-010 | UI Testing and Observation Audit |
| Substitutions and closed extensions | P-10, ACT-005, SAFE-004 | Adaptation tests and rejection of prohibited options |
| Immutable Adult Steps | P-11, SAFE-003, SAFE-006 | Bilingual render and recommender test |
| Test failure classified without child inference | P-07, EVD-004, SAFE-002, SAFE-006 | Cases `invalid_setup`, `bridge_deformation` and `safe_stop` |
| Versioned and revised images | ACT-010, ACT-VIS-001 to ACT-VIS-004 | Automatic QA + human review |
| Complete location | ACT-011, ACT-012 | Specific bilingual review |

## 18. Change log

| Version | State | Changes |
|---|---|---|
| 0.1.0 | Historical draft | Initial skeleton to validate the scheme. |
| 0.2.0 | Historical draft | Expands to bilingual editorial ActivityVersion; sets materials and testing; documents 30–60 minute routes, configurations 1–3, roles, objectives/rubrics, safety, adaptations, troubleshooting, closure and visual briefs. Change loading from ambiguous coins/blocks to intact crayons in light glass and limit this version to three children until validation. |
| 0.2.1 | Historical draft | Remove non-validated glass and load substitutions; distinguishes `invalid_setup`, `bridge_deformation` and `safe_stop`; structure `STEP-00`–`STEP-09`; completes bilingual materials, roles, hazards, and adaptations fields; align IDs with the schema; corrects tolerances and visual briefs; adds scientific gate and physical glass/load gate. |
| 0.2.2 | Historical draft | Add a bilingual, hands-on guide so the adult can propose folds, channels, and design questions without handing over the solution or promising that one shape will be superior. |
| 0.3.0 | Current draft | Rewrite the activity from a causal narrative contract: actual baseline testing in Discover, explicit role of cup and crayons, self-design and testing per child, group improvement, verifiable transitions, and age/evidence calibrated foci. |

## 19. Evidence required before switching to `ready_for_pilot`

1. **Physical Cup and Load Crayon:** run at least ten complete adult cycles with the same type of cup and canonical set of 20 crayons; record approximate mass, vessel dimensions, empty stability, progressive stability, manner of placement and cause of each failure. The protocol only advances if two reviewers can consistently distinguish `invalid_setup` from `bridge_deformation`; if not, the container/protocol is changed and another version is created.
2. Explicitly test for off-center loading, dropped crayon, moved support, uneven support, deformation tilt, and collapse onto the towel; confirm that each case reaches the correct status without producing child evidence.
3. Run on plain letter and A4 paper and document whether 15 cm / 6 in produces at least two comparable tests without substitute loading or increased space.
4. Verify that glass and 20 crayons remain within the safe failure profile on the low table; Any breakage, bounce off the table or need for greater load blocks the version.
5. Time routes and preparation with an adult other than the author, and time cleaning separately.
6. Run table walkthrough and validate continuity, wait and a complete self-test with one, two and three children; No step can require inventing a material's function or transition.
7. Confirm that the closing questions distinguish support, `invalid_setup`, `bridge_deformation`, `safe_stop` and non-observation.
8. Serialize `ACT-0001@0.3.0` and validate all its IDs, localized fields, narrative and references against the current schema.
9. Complete and record scientific, pedagogical, safety and bilingual review.
10. Generate the eight assets and complete QA; do not use family images without separate consent.

Additional family testing pertains to state `family_pilot` and is a subsequent requirement for `published`; they are not confused with the previous evidence needed to enter `ready_for_pilot`.
