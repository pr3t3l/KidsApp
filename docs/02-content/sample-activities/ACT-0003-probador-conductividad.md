> **Canonical English document.** This document is normative from 18 August 2026 under `DEC-052`. The Spanish [historical record](../../../historical/es/docs/02-content/sample-activities/ACT-0003-probador-conductividad.md) is retained for traceability; all new requirements, decisions, and changes belong in English.

# ACT-0003 — Conductivity Tester

**Status:** Draft — not deliverable to families<br>
**Version:** 0.1.2<br>
**Specification source language:** English (`en-US`)<br>
**Bundles required:** `es-US`, `en-US`<br>
**Authorship:** Project team; AI assisted draft<br>
**Proposed Editorial Manager:** Founding Team/Content<br>
**Revisions logged:** None; pending pedagogical, electrical/safety, bilingual review and family test

## 1. Editorial identity

| Field | Value |
|---|---|
| `activity_id` | `ACT-0003` |
| `version` | `0.1.2` |
| `status` | `draft` |
| `slug` | `probador-conductividad` |
| Title `es-US` | Conductivity tester |
| Title `en-US` | Conductivity Tester |
| Summary `es-US` | Build a low voltage tester and use it to find out which dry objects complete a circuit. |
| Summary `en-US` | Build a low-voltage tester and use it to discover which dry objects complete a circuit. |
| Family duration | 35–50 minutes; up to 60 minutes with approved extension |
| Adult preparation | 10–15 minutes before inviting the children; does not count within the family duration |
| Participants | 1–3 children and at least one supervising adult |
| Indicative age | 5–10 years |
| Functional levels | L1–L3; L4 extension through explanation and control of variables |
| Children's prerequisites | None; reading, writing or mounting components is not a requirement. |
| Child prerequisites | None; reading, writing, and assembling components are not required. |
| Adult prerequisite | Be able to verify labels and polarity and follow the exact published assembly. If you cannot do this, you must use the selected pre-assembled configuration or choose another activity. |
| Adult prerequisite | Ability to verify labels and polarity and follow the exact published setup. Otherwise, use the selected preassembled configuration or choose another activity. |
| Safety level | C: an adult prepares the circuit, inserts or removes batteries, and secures fixed connections; children participate in testing with close assistance |
| Mess | Low |
| Space | Dry, clear and well-lit table, away from kitchen, bathroom, sink and outlets |
| External dependency | None during the session; the complete package can be run offline |

### Editorial status and usage limits

This version is a draft for review and pilot. It does not yet meet the publication gates of `ACT-002`, `SAFE-001` or the independent family execution criteria. No system should recommend it as a published activity.

### Changelog

| Version | Date | Change | Author |
|---|---|---|---|
| 0.1.0 | August 15, 2026 | First bilingual ActivityVersion: circuit with 2 AA batteries, red LED and 330 Ω resistor; roles for 1–3 children; evaluation, safety and visual briefs. | Project team; AI assisted draft |
| 0.1.1 | August 15, 2026 | Cross-review fixes: mechanical retention, full localization, timing, tolerance calculations, fair evidence, safety, structured fields, and A/B gates. | Project team; AI-assisted cross-review |
| 0.1.2 | August 16, 2026 | Clarifies that A/B are editorial candidates, eliminates the ambiguous reference “A is selected” and registers as a design requirement a de-energized child assembly route subject to expert review. | Feedback from the founder; AI-assisted editing |

### Review records

| Gate | Reviewer | State | Date | Findings |
|---|---|---|---|---|
| Pedagogy | To be assigned | Pending | — | — |
| Electricity and safety | To be assigned | Pending | — | Must include mounting, exact components, mechanical retention, and safe failure. |
| Location `es-US` | To be assigned | Pending | — | — |
| Location `en-US` | To be assigned | Pending | — | — |
| Visual and accessibility | To be assigned | Pending | — | — |
| Family Pilot | To be assigned | Pending | — | — |

## 2. Educational purpose

### Central question

- **en-US:** What dry objects allow enough current to pass through to light our LED?
- **en-US:** Which dry objects let enough current pass to light our LED?

### Child's actual decision

Each child predicts which objects will complete the circuit, decides on a trial order, or proposes a more consistent way to make contact. The result is not given in advance and a different prediction is not considered an error.

### Areas and concepts

| Type | Content |
|---|---|
| Main area | `ELE` Electricity |
| Secondary areas | `LOG` logical thinking, `MAT` classification/registration, `COM` explanation, `PRA` safe organization |
| Main concepts | closed and open circuit; conductor and insulator in the context of the tester; LED polarity; current limiting resistor |
| Secondary concepts | fair test; electrical contact; uncertain evidence; materials and coatings |

### Observable abilities

| Local code | Observable ability | Example of contextual evidence |
|---|---|---|
| `ELE-CLOSE-PATH` | Identify or construct a continuous path in a simple circuit. | Mark the path battery → resistance → LED → object → battery and find a gap that prevents the LED from turning on. |
| `ELE-SEQUENCE-TEST` | Run a safe and consistent test sequence. | Keep the switch off when changing objects, separate the tweezers, place an object, and then turn on to observe. |
| `LOG-CLASSIFY-EVIDENCE` | Classify objects according to an observed result. | Set each object to “turned on,” “did not turn on,” or “uncertain result” after testing it. |
| `LOG-CONTROL-VARIABLE` | Keep relevant conditions constant when comparing. | Use the same tester, contact position, and observation time for each object. |
| `COM-EXPLAIN-CIRCUIT` | Explain a conclusion using observation and mechanism. | It says that the metal completed the path and that is why the LED turned on, without stating that all metals will always produce the same glow. |
| `MAT-RECORD-RESULT` | Record and compare categorical results. | Mark a prediction and the result of each object without losing the correspondence. |

The presence of these skills in the activity constitutes exposure. Only the skill chosen as the primary objective of each child is evaluated by default.

## 3. Expected result and scientific precision

The LED should light when the two test clips make clean contact with a material of sufficiently low resistance, such as the metal spoon or aluminum foil. It should remain off with dry plastic, wood, cardboard, rubber/silicone and cloth objects included.

This assembly is a **qualitative tester**, not a conductivity meter. “LED off” means “not enough current passed to turn on this LED under these conditions”; it does not absolutely prove that the material is an insulator. Dirt, paint, rust, a coating, poor contact, weak batteries or an inverted LED can cause a false result. A dim glow is registered as `incierto` and repeats after checking the closed control.

## 4. Structured materials

### 4.1 Circuit — exactly one of two candidate configurations

The letters **A** and **B** are internal labels for comparing two editorial designs; they are not steps or choices that a family should understand. **A** uses visible LEDs and resistors as separate components. **B** uses a pre-assembled LED module with integrated current limiting. None are selected in this draft. Before moving to `pedagogical_review`, the electrical and mechanical gate must choose a configuration, document why it is the lowest risk alternative that preserves learning, and completely remove the other family instructions from the next version.

The founder has defined that building the circuit should be a significant part of the child's experience. This version does not yet authorize children to form fixed joints: a **de-energized co-assembly** route with exact components, mechanically protected connections, and age-defined child actions must first be evaluated. The specialist will decide what the child can connect and what remains `adult-only`; the adult always retains the batteries, the final inspection and the authorization to energize.

**`en-US`:** Letters **A** and **B** are internal labels for comparing two editorial designs; they are not steps or choices a family should need to understand. **A** uses a visible discrete LED and resistor. **B** uses a preassembled LED module with integrated current limiting. Neither is selected in this draft. Before `pedagogical_review`, the electrical and mechanical gate must select one configuration, document why it is the lowest-risk option that preserves the learning, and completely remove the other from the next version's family instructions.

The founder has specified that building the circuit should be a meaningful part of the child experience. This version does not yet authorize children to make fixed joints: a **de-energized co-assembly** path must first be evaluated using exact components, mechanically protected connections, and child actions defined by age. The specialist will decide what a child may connect and what remains `adult-only`; the adult always controls the cells, final inspection, and authorization to energize.

#### Configuration A — visible components, candidate

| ID | Quantity | Material `es-US` | Material `en-US` | Specification and control `es-US` | Specification and control `en-US` |
|---|---:|---|---|---|---|
| `circuit.holder-2aa` | 1 | Closed battery holder for 2 AA batteries, with switch and red/black cables | Enclosed 2-AA battery holder with switch and red/black leads | Compartment intact; screw secured lid preferred; only 3V nominal; the adult inserts and removes the batteries. | Intact compartment; a screw-secured cover is preferred; 3V nominal only; the adult inserts and removes cells. |
| `circuit.cell-aa` | 2 | AA alkaline batteries | AA alkaline cells | Same type, brand and condition; never mix new/used; never use damaged, leaking or rechargeable batteries in this version. | Same type, brand, and condition; never mix new/used cells; never use damaged, leaking, or rechargeable cells in this version. |
| `circuit.led-red` | 1 | High efficiency red LED, 5 mm | High-efficiency red 5 mm LED | Discrete LED without built-in resistor; identifiable anode and cathode. The exact part number and its limits must be approved by `review`; do not replace with white/blue LED, strip or bulb. | Discrete LED without an integrated resistor; identifiable anode and cathode. The exact part number and ratings require approval before `review`; do not substitute a white/blue LED, strip, or bulb. |
| `circuit.resistor-330` | 1 | 330 Ω, 1/4 W, 5% resistor | 330 Ω, 1/4 W, 5% resistor | Required and always in series. It must be provider-labeled; the adult does not guess its value. | Required and always in series. It must be provider-labeled; the adult does not guess its value. |
| `circuit.clip-lead` | 4 | Jumper Cables with Fully Insulated Small Alligator Clips | Fully insulated small alligator-clip jumper leads | Intact caps and teeth with no exposed edges outside the jaw. Only two ends are left free as test clips. Requires validated mechanical retention. | Intact boots and no exposed teeth outside the jaw. Only two ends remain free as test clips. Validated mechanical retention is required. |
| `circuit.insulation-tape` | 1 roll | Certified electrical insulating tape | Listed electrical insulating tape | Only the adult covers the six fixed connections and legs separately. The tape does not replace strain relief or repair damaged insulation. | The adult separately covers all six fixed joints and leads. Tape does not replace strain relief and must not repair damaged insulation. |

#### Configuration B — pre-assembled module, candidate

A **pre-assembled red LED indicator module (`circuit.module-led-3v`) and explicitly specified by its manufacturer for 3 V DC, with integrated current limiting**, connected to the same 2 AA battery holder and two insulated test clips, can be used. The module must have marked polarity and closed, protected and strain-relieved connections. The external resistance is not added if the module already integrates it. A part without a part number, data sheet or clear indication of current limitation is not permitted.

**`en-US`:** A preassembled red LED indicator module (`circuit.module-led-3v`) explicitly manufacturer-rated for 3 V DC with integrated current limiting may connect to the same 2-AA holder and two insulated test clips. It must have marked polarity, enclosed or protected connections, and strain relief. Do not add the external resistor when current limiting is integrated. A module without a part number, datasheet, and stated current limiting is not allowed.

Configurations A and B are not mixed or improvised. This version does not include soldering, breadboard, USB power supply, 9V rectangular battery, rechargeable battery, coin cell battery or connection to household power.

### 4.2 Test objects — dry and loose

| ID | Quantity | Material `es-US` | Material `en-US` | Probable outcome | Control `es-US` / `en-US` |
|---|---:|---|---|---|---|
| `sample.spoon-steel` | 1 | Stainless steel metal spoon, without coated handle | Uncoated stainless-steel spoon | Lit / Lit | No cutting edge; clean and dry / No sharp edge; clean and dry. |
| `sample.foil` | 1 | Strip of aluminum foil, approx. 5 × 15cm / 2 × 6in | Aluminum foil strip, about 5 × 15 cm / 2 × 6 in | Lit / Lit | Fold into four layers to prevent tearing or a thin edge. |
| `sample.ruler-plastic` | 1 | Plastic ruler, approx. 15–30 cm / 6–12 in | Plastic ruler, about 15–30 cm / 6–12 in | Did not turn on / Did not light | No metal parts / No metal parts. |
| `sample.stick-wood` | 1 | Dry wooden stick, no splinters | Dry wooden craft stick with no splinters | Did not turn on / Did not light | The adult inspects and discards it if splintered. |
| `sample.cardboard` | 1 | Strip of dry cardboard, approx. 5 × 15cm / 2 × 6in | Dry cardboard strip, about 5 × 15 cm / 2 × 6 in | Did not turn on / Did not light | No staples, metallic laminate, or moisture. |
| `sample.spatula-silicone` | 1 | Small silicone or rubber spatula, clean and dry | Clean, dry silicone or rubber spatula | Did not turn on / Did not light | No exposed metal core / No exposed metal core. |
| `sample.fabric-cotton` | 1 | Cotton scrap, approx. 10 × 10 cm / 4 × 4 in | Cotton fabric swatch, about 10 × 10 cm / 4 × 4 in | Did not turn on / Did not light | Completely dry and not frayed. |
| `record.result-sheet` | 1 | Printed or drawn recording sheet | Printed or hand-drawn result sheet | Not applicable / N/A | Three columns: prediction, result, note / Three columns: prediction, result, note. |
| `record.result-card` | 3 | Large cards: “turned on”, “did not turn on”, “uncertain” | Large cards: “lit”, “did not light”, “uncertain” | Not applicable / N/A | Text and icon; don't depend only on color / Use text and icon; do not rely on color alone. |
| `record.pencil` | 1 | Pencil or crayon | Pencil or crayon | Not applicable / N/A | It is not tested as a sample / Never tested as a sample. |
| `visual.white-card` | 1 optional | Matte white card | Matte white card | Not applicable / N/A | Behind the LED if visibility is poor. |

### 4.3 Structured state of materials

| Group/ID | Mandatory | Cycle | Replaceable | Adult preparation |
|---|---|---|---|---|
| Configuration A: `circuit.holder-2aa`, `circuit.led-red`, `circuit.resistor-330`, `circuit.clip-lead` | Yes, only if the editorial gate selects the A | Reusable | Not automatic | Select part number, inspect, assemble, isolate and validate retention. |
| `circuit.cell-aa` | Yes, two in A or B | Consumable/replaceable | Only two AA alkaline approved | Insert, remove, count and store. |
| `circuit.insulation-tape` | Yes in A | Consumable | No | Apply separately; replace if detached. |
| `circuit.module-led-3v` | Yes, only if the editorial gate selects configuration B | Reusable | Not automatic | Check card, polarity, limitation and mechanical protection. |
| `sample.*` | Seven in full route; four in short adaptation | Reusable | Only according to 4.4 | Inspect dryness, size, edges, coatings and absence of external connection. |
| `record.*` | Yes | Consumable or reusable depending on format | Yes, for sure equivalent | Prepare columns, icons and language. |
| `visual.white-card` | No | Reusable | Yes, for matte white surface | Reserve if the lighting makes it difficult to see the LED. |

### 4.4 Prohibited and approved substitutions

- Do not replace the source, LED, resistance value, or module type without creating a new safety revision.
- A test object can only be replaced by another **large, dry, loose, non-sharp, non-electronic, not connected to anything, non-food object and previously approved by the adult**. The substitution is recorded as a scan and receives no promised result.
- Never test plugs, outlets, wall switches, installed cables, chargers, devices, screens, appliances, electric toys, batteries, vehicles, valuable jewelry, skin, people, animals, mouth, plants, food, powders, wet objects, liquids, chemicals or unknown objects.
- Never use coins as a battery or button/coin batteries as a source or sample.

**`en-US` non-negotiable substitutions and prohibitions:** Do not change the source, LED, resistor value, or module type without a new safety review. A sample may be replaced only by another large, dry, loose, blunt, nonelectronic, unpowered, nonfood object approved by the adult; no result is promised for a substitute. Never test an outlet, receptacle, wall switch, installed cable, charger, device, screen, appliance, powered toy, battery, vehicle, valuable jewelry, skin, person, animal, mouth, plant, food, powder, wet object, liquid, chemical, or unknown object. Never use a coin as a battery, and never use a button/coin cell as either the source or a sample.

## 5. Exclusive preparation of the adult in this version

All points in this section are `adult-only`. Children can observe from a safe distance, but not insert batteries, select components at random, or prepare fixed joints.

This is an interim restriction for `ACT-0003@0.1.2`, not the final desired experience. During `build`, children can arrange large cards representing the components, mark the trajectory, and decide the logical order with the empty battery holder; they do not handle LEDs, resistors or loose electrical connections in this version. These actions allow you to learn the circuit, but do not replace the future physical co-assembly test. A later version will only be able to extend child permits after the electrical/mechanical gate and an age test.

**`en-US`:** This is a provisional restriction of `ACT-0003@0.1.2`, not the desired final experience. During `build`, children may arrange large cards representing the components, point out the path, and decide the logical order while the battery holder is empty; they do not handle the loose LED, resistor, or electrical connections in this version. Those actions support circuit learning but do not replace the future physical co-assembly test. A later version may expand child permissions only after the electrical/mechanical gate and age-based testing.

1. **Prepare the space.** Work on a dry, clear table, at least 1 m / 3 ft from outlets, sinks, liquids, food and devices. Remove any items that are not on the approved list.
2. **Inspect / Inspect.** Confirm that battery holder, cables, insulation, LED and resistance are not cracked, hot, corroded, wet or damaged. Confirm the tag `330 Ω`.
3. **Keep power off.** Leave the switch at `OFF` and the battery holder empty while connecting the circuit.
4. **Assemble the path.** This step only applies if the editorial gate selects **Configuration A — visible components** and there is an approved diagram that names each component and connection: cable 1 joins red `+` to resistor; Wire 2 joins resistor to long leg/anode; Cable 3 joins short leg/cathode and leaves its other end as test clamp A; cable 4 leaves one end as test clamp B and joins the other to black `−`. “Test clips A and B” are the two ends that will touch the object; they do not refer to A/B editorial configurations. Keep them separate. Separately cover the six fixed joints and all exposed legs. Apply exact approved strain relief; the tape alone does not replace it. If Configuration B is selected, this step is replaced by the approved module-specific instructions; Both routes are never mixed.
5. **Check polarity.** The long leg of the LED goes towards the resistor and the red wire. The short leg and flat side of the capsule go towards the clamp which eventually returns to the black wire. Do not power an inverted LED to “see what happens.”
6. **Insert batteries.** Insert two AA alkaline batteries following `+` and `−`; Close and secure the lid. Keep all loose batteries out of the reach of children.
7. **Open test / Open control.** Separate the clamps, turn on for 2 seconds and confirm that the LED remains off. Turn off.
8. **Closed test.** Only touch the jaws of the two test clips to each other, turn on for 2 seconds and confirm that the LED lights up. Turn off and separate them again. The resistance always remains in the circuit.
9. **Check temperature / Check temperature.** Nothing should feel hot or produce an odor. If the control fails or heat, odor, smoke, spark, corrosion or leak occurs, turn off only if you can do so without approaching or touching a dangerous part. Keep children away. Do not open the battery door or remove batteries while the assembly is hot, smoking, sparking, or leaking; Follow the manufacturer's guide and remove the assembly from service.
10. **Prepare objects and record / Set out samples and record sheet.** Confirm that all objects are dry, large and free of dangerous parts. Place the three result cards.

### Checklist before inviting kids

- [ ] There is only one 2 AA battery holder; There are no coin batteries, USB source or household power.
- [ ] The 330 Ω resistor is connected in series and the fixed junctions are covered.
- [ ] The assembly matches the diagram of the selected configuration; No components move, rotate or expose fixed metal with gentle adult manual inspection.
- [ ] Open control turns off the LED and closed control turns it on.
- [ ] The seven test objects are dry, loose and passed.
- [ ] The adult can reach the switch at all times.
- [ ] The registration sheet and roles are ready.

### `en-US` adult-only preparation bundle

Every item below is `adult-only`. Children may watch from a safe distance, but they do not insert cells, select electrical components, or prepare fixed joints.

1. **Prepare the space.** Work on a dry, clear table at least 1 m / 3 ft from outlets, sinks, liquids, food, and devices. Remove every object that is not on the approved list.
2. **Inspect.** Confirm that the holder, leads, insulation, LED, and resistor are not cracked, warm, corroded, wet, or damaged. Confirm the `330 Ω` label.
3. **Keep power off.** Leave the switch `OFF` and the holder empty while assembling the circuit.
4. **Assemble the path.** This step applies only if the editorial gate selects **Configuration A — visible components** and an approved diagram names every component and connection: lead 1 joins red `+` to the resistor; lead 2 joins the resistor to the long LED lead/anode; lead 3 joins the short lead/cathode and leaves its other end as test clip A; lead 4 leaves one end as test clip B and joins its other end to black `−`. “Test clips A and B” are the two ends that touch the sample; they are not the editorial Configurations A/B. Keep the test clips apart. Separately cover all six fixed joints and every exposed component lead. Apply the exact approved strain relief; tape alone is not strain relief. If Configuration B is selected, replace this step with the approved module-specific instructions; never mix the two paths.
5. **Check polarity.** The LED long lead faces the resistor and red lead. The short lead and flat side of the LED body face the clip that eventually returns to the black lead. Do not energize a reversed LED “to see what happens.”
6. **Insert the cells.** Insert two alkaline AA cells according to `+` and `−`; close and secure the cover. Keep all loose cells out of children's reach.
7. **Open control.** Keep the clips apart, switch on for 2 seconds, and confirm that the LED remains off. Switch off.
8. **Closed control.** Touch only the jaws of the two test clips together, switch on for 2 seconds, and confirm that the LED lights. Switch off and separate them. The resistor stays in the circuit at all times.
9. **Check temperature.** Nothing should feel warm or produce an odor. If a control fails or there is heat, odor, smoke, a spark, corrosion, or leakage, switch off only if this can be done without approaching or touching a hazard. Move children away. Do not open the holder or remove cells while the setup is hot, smoking, sparking, or leaking; follow the manufacturer guidance and remove the setup.
10. **Set out samples and record sheet.** Confirm that every sample is dry, large, and free of hazards. Set out all three result cards.

**Before children join:** confirm that the only source is the enclosed 2-AA holder; all fixed joints are covered and remain fixed during a gentle adult inspection; the setup matches the approved diagram; the open and closed controls work; all seven samples are dry, loose, and approved; the adult can reach the switch; and the record sheet and roles are ready.

## 6. Roles and goal assignment

### 6.1 Role templates

| Role | Meaningful contribution | Responsibilities | Eligible Primary Targets | Exposures planned | Restricted steps |
|---|---|---|---|---|---|
| **Materials Investigator** | Decide what to test and organize the physical evidence. | Names, touches, and observes approved objects; makes predictions; Place each object in the observed category. | `LOG-CLASSIFY-EVIDENCE`, `MAT-RECORD-RESULT`, `COM-EXPLAIN-CIRCUIT` | materials, contextual conductor/insulator, prediction, review of ideas | Does not insert batteries or touch fixed joints; By 5–6 years the adult operates the forceps. |
| **Circuit Keeper** | Keeps testing safe and consistent. | Checks `OFF` before a change; indicates the circuit path; turns it on only when clips are in place; confirms controls. | `ELE-SEQUENCE-TEST`, `ELE-CLOSE-PATH`, `LOG-CONTROL-VARIABLE` | polarity, resistance, open/closed circuit, turns | Does not open the battery door, reconfigure components, or remove tape. |
| **Evidence Engineer/Evidence Engineer** | Makes each test comparable and preserves results. | Helps place clips on separate ends; observe the LED; mark result; detects suspicious contact; asks to repeat when appropriate. | `LOG-CONTROL-VARIABLE`, `MAT-RECORD-RESULT`, `COM-EXPLAIN-CIRCUIT` | comparison, uncertainty, registration, debugging | Do not test unapproved objects or use tweezers near people, liquids, appliances, or outlets. |

All roles have agency. Decorating the sheet does not constitute a separate role.

#### Role bundle `en-US`

| Role | Real contribution | Responsibilities | Eligible primary objectives | Expected exposures | Restricted actions |
|---|---|---|---|---|---|
| **Materials Investigator** | Chooses what to test and organizes physical evidence. | Names, handles, and observations approved samples; predicts; places each item in its observed category. | `LOG-CLASSIFY-EVIDENCE`, `MAT-RECORD-RESULT`, `COM-EXPLAIN-CIRCUIT` | materials, contextual driver/insulator, prediction, review | Does not insert cells or touch fixed joints; the adult operates clips for ages 5–6. |
| **Circuit Keeper** | Keeps the procedure safe and consistent. | Confirms `OFF` before changes, traces the path, switches on only after clips are placed, and confirms controls. | `ELE-SEQUENCE-TEST`, `ELE-CLOSE-PATH`, `LOG-CONTROL-VARIABLE` | polarity, resistor, open/closed circuit, turns | Does not open the holder, reconfigure components, or remove insulation. |
| **Evidence Engineer** | Makes tests comparable and preserves results. | Helps direct clip placement, observes the LED, records results, flags uncertain contact, and requests a repeat when appropriate. | `LOG-CONTROL-VARIABLE`, `MAT-RECORD-RESULT`, `COM-EXPLAIN-CIRCUIT` | comparison, uncertainty, recording, troubleshooting | Does not test unapproved objects or use clips near people, liquids, devices, or outlets. |

#### Step permissions and dependencies

| Role | Permitted `step_id` | Dependency | Single variant |
|---|---|---|---|
| Materials Investigator | `discover`, `imagine`, `build`, `experiment`, `improve`, `explain` | Adult has approved and prepared every sample; Circuit Keeper confirms `OFF` before sample change. | Child predicts, selects, observes, and classifies; adult performs any clip operation required by safety. |
| Circuit Keeper | `discover`, `build`, `experiment`, `improve`, `explain` | Adult has completed controls and retains access to switch; Evidence Engineer confirms result before change. | Child narrates and follows permitted sequence actions; adult retains all `adult-only` actions. |
| Evidence Engineer | `imagine`, `build`, `experiment`, `improve`, `explain` | Materials Investigator identifies current sample; Circuit Keeper confirms safe state. | Child observes and records one result at a time; adult maintains setup. |

No role is permitted to execute `adult-only-preparation`, open the holder, alter fixed joints, select electrical components, remove insulation, or approve new samples.

### 6.2 Configurations for one, two and three children| Participants | Recommended Assignment | Default primary goal when there is no prior evidence | Coordination |
|---:|---|---|---|
| 1 | The child alternates the three roles; the adult handles tweezers when necessary. | `LOG-CLASSIFY-EVIDENCE`: Classify objects after observing the LED. | Complete one test at a time; the adult retains the switch if the child still does not follow the safe sequence. |
| 2 | Child A: Materials Investigator. Child B: Circuit Keeper + Evidence Engineer. | A: `LOG-CLASSIFY-EVIDENCE`. B: `ELE-SEQUENCE-TEST`. | A delivers an approved object; B confirms `OFF`, places/helps place and registers. Change who chooses first, not the objectives, in the middle of the list. |
| 3 | Child A: Materials Investigator. Boy B: Circuit Keeper. Child C: Evidence Engineer. | A: `LOG-CLASSIFY-EVIDENCE`. B: `ELE-SEQUENCE-TEST`. C: `MAT-RECORD-RESULT`. | Use a relay phrase: “object ready” → “circuit ready” → “result recorded”. This way everyone contributes without touching the clamps simultaneously. |

#### Participant configurations `en-US`

| Children | Recommended assignment | Default primary objective without prior evidence | Coordination |
|---:|---|---|---|
| 1 | The child rotates through all three roles; the adult operates clips whenever required. | `LOG-CLASSIFY-EVIDENCE`. | Complete one sample at a time; the adult retains the switch if the child is not yet following the safe sequence. |
| 2 | Child A: Materials Investigator. Child B: Circuit Keeper + Evidence Engineer. | A: `LOG-CLASSIFY-EVIDENCE`; B: `ELE-SEQUENCE-TEST`. | A supplies one approved sample; B confirms `OFF`, directs or helps place it, and records. Switch who chooses first, not the objectives, midway. |
| 3 | Child A: Materials Investigator. Child B: Circuit Keeper. Child C: Evidence Engineer. | A: `LOG-CLASSIFY-EVIDENCE`; B: `ELE-SEQUENCE-TEST`; C: `MAT-RECORD-RESULT`. | Use “sample ready” → “circuit ready” → “result recorded” so all contribute without simultaneous clip handling. |

The recommender may choose another eligible target based on evidence, independence, interest, and role variety. Each child retains **at most one primary goal**. The other skills are exposures unless the adult chooses “Evaluate more.” The adult can change the assignment before starting.

### 6.3 Supports by age and experience

- **5–6 years / Explorer–Builder:** use four objects (spoon, aluminum, plastic ruler, cardboard); the adult fixes the clamps; the child predicts, ignites with permission, observes and classifies using icon cards.
- **7–8 years / Builder–Inventor:** use six or seven objects; child can operate insulated forceps with close assistance, follow sequence `OFF–colocar–ON–observar–OFF` and record with marks.
- **9–10 years / Inventor:** use all objects; draw the trajectory, distinguish negative result from uncertain result and justify a controlled repetition.

Age guides language and safety control; it does not alone determine the objective.

**`en-US` age/experience supports:**

- **Ages 5–6 / Explorer–Builder:** use four samples (spoon, foil, plastic ruler, cardboard). The adult operates the clips; the child predicts, uses the switch with permission when appropriate, observes, and classifies with icon cards.
- **Ages 7–8 / Builder–Inventor:** use six or seven samples. The child may operate intact insulated clips with close help, follow `OFF–place–ON–observe–OFF`, and record with marks.
- **Ages 9–10 / Inventor:** use every sample, draw the path, distinguish a negative from an uncertain result, and justify a controlled repeat.

Age guides language and safety control; it does not determine the objective by itself.

## 7. Bilingual flow of activity

### Temporary view

| Stage | Base time |
|---|---:|
| Discover | 5 min |
| Imagine | 5 min |
| Build | 7 min |
| Experiment | 8–10 min for 4 objects; 14–18 min for 7 objects |
| Improve | 4–8 min |
| Explain + closure | 6–7 min |
| Optional Approved Extension | 8–10 min; maximum total 60 min |

The core lasts approximately 35–43 minutes with four objects and 42–50 minutes with seven. An extension is only added when the remaining time keeps the session at 60 minutes or less.

### Step Structured Contract

| `step_id` | Actor and time | Expected visual | Success sign | Frequent problem and safe solution | Warning | Resumption |
|---|---|---|---|---|---|---|
| `discover` | Cluster; adult controls tester; 5 min | Open/Off and Close/On Control | The child locates the separation between tweezers | If “electricity” remains abstract, physically follow the trajectory with the tester in `OFF` | Only the adult executes controls; do not touch fixed joints | Adult repeats open/close control and turns off again |
| `imagine` | Materials Investigator; 5 min | Aligned objects with attributed prediction | Each chosen object has a prediction or `not sure yet` | If it is treated as an exam, remind everyone that predictions are not graded | Do not connect objects or introduce new samples yet | Keep the sheet/cards and resume with the first untested object |
| `build` | Children organize; adult retains assembly; 7 min | Tester intact, `OFF`, tweezers separated and samples sorted | Roles repeat the sequence and the adult confirms control | If a cable is pulled, stop and remove assembly until adult re-inspection | Children do not touch fixed joints, battery holders or loose components | Adult inspects, repeats control and authorizes resumption |
| `experiment` | Coordinated roles; 8–18 mins | Separate tweezers on a sample and visible LED | Recorded result; `OFF` before each change | If the result is weak, repeat the control and a single test; keep `incierto` | No one touches exposed metal during `ON`; only approved objects | During pause, adult turns off and removes batteries; upon return, re-inspect and repeat controls |
| `improve` | Cluster; 4–8 min | A single contact/visibility variable changes | The result becomes clear or remains honestly `incierto` | If two variables change, return to the last recorded state and change only one | Do not change source, resistor, LED, fixed junctions or power | Use the sheet to identify the chosen test; repeat check before continuing |
| `explain` | Each child according to role; 6–7 min | Conceptual diagram and results sheet | Oral, marked or drawn explanation connects evidence and trajectory | If the language demands too much, allow pointing the way and cards | Closing without new samples or connections | Retake with sheet and diagram; do not re-energize to complete the explanation |

#### Structured step contract `en-US`

| `step_id` | Actor and time | Expected visual | Success signal | Common issue and safe solution | Warning | Resume |
|---|---|---|---|---|---|---|
| `discover` | Group; adult controls tester; 5 min | Open/off and closed/lit controls | Child locates the gap between clips | If electricity feels abstract, trace the physical path with tester `OFF` | Adult alone runs controls; no fixed-joint contact | Adult repeats open/closed controls and switches off |
| `imagine` | Materials Investigator; 5 min | Samples lined up with attributed prediction | Each chosen sample has a prediction or `not sure` | If treated as a quiz, remind children predictions are not graded | Do not connect samples or add new ones yet | Keep sheet/cards and resume at first untested sample |
| `build` | Children organize; adult retains setup; 7 min | Intact tester `OFF`, clips apart, samples ordered | Roles repeat sequence and adult confirmations control | If a lead is pulled, stop and remove setup until adult reinspection | Children do not touch fixed joints, holders, or loose components | Adult reinspections, repeats controls, and authorizes resume |
| `experiment` | Coordinated roles; 8–18 mins | Clips separated on one sample; Visible LED | Result recorded; `OFF` before every change | For dim result, repeat control and one test; keep `uncertain` | No exposed-metal contact during `ON`; approved samples only | Adult switches off/removes cells for pause; reinspects and repeats controls |
| `improve` | Group; 4–8 min | Only one contact/visibility variable changes | Result becomes clearer or honestly remains `uncertain` | If two variables change, restore last recorded state and change one | Do not alter source, resistor, LED, fixed joints, or energy | Use sheet to identify chosen test; repeat control before resuming |
| `explain` | Each child by role; 6–7 min | Concept diagram and result sheet | Spoken, pointed, or drawn explanation connects evidence and path | If language demand is high, allow pointing to path/cards | No new samples or energized connections during close | Resume with sheet/diagram; do not reenergize merely to explain |

### 7.1 Discover — Find the path

**Actor:** group; adult controls the tester.

**Visual cue required:** open and closed circuit diagram.

**es-US — For adults**

Show the tester turned off and the two clamps separated. Say: "This LED can only light if there is a complete path from one battery, through all the pieces, and back to the other part of the battery. These two clamps are the gap we will try to close with an object." Do the open control and then the closed control. Turn off after each demonstration.

**en-US — Question for children**

"What changed when the pincers touched? What could go between them to complete the path?"

**en-US — For the adult**

Show the switched-off tester with the two test clips apart. Say: "This LED can light only when there is a complete path from one side of the battery, through every part, and back to the other side. These two clips are the gap we will try to close with an object." Perform the open control and then the closed control. Switch off after each demonstration.

**en-US — Ask the children**

"What changed when the clips touched? What could go between them to complete the path?"

**Exito / Success:** children identify the separation between the clamps as an open part of the trajectory. They don't need to use the word “driver” yet.

### 7.2 Imagine — predict without grading

**Actor:** Materials Investigator; others can propose reasons.

**Visual cue required:** materials board and prediction sheet.

**en-US**Choose the approved objects you will use. For each, check “I think it will turn on,” “I don't think it will,” or “I'm not sure.” Ask: “What do you observe about the material that makes you think that?” Accept changes of mind before the test and do not reveal results.

**en-US**

Choose the approved objects you will use. For each one, mark “I think it will light,” “I think it will not,” or “I am not sure.” Ask: “What do you notice about the material that makes you think that?” Allow children to review before testing and do not reveal results.

**Success:** there is a prediction attributed to each object; a correct prediction is not the default primary goal.

### 7.3 Build — Set up the test station

**Actor:** the children organize; the adult retains control of fixed joints.

**Visible warning:** `OFF antes de cambiar / OFF before changing`.

**en-US**

1. Place the tester in the center without pulling on the cables.
2. Arrange the objects in a row and place the three result cards.
3. Follow the path with one finger: `battery + → resistor → LED → test clip → object → test clip → battery −`.
4. The Circuit Keeper practices the sequence out loud: “off, place, turn on, observe, turn off.”
5. The adult checks the closed control again and turns off.

**en-US**

1. Place the tester in the center without pulling on its wires.
2. Line up the samples and set out the three result cards.
3. Trace the path with a finger: `battery + → resistor → LED → clip → sample → clip → battery −`.
4. The Circuit Keeper rehearses aloud: “off, place, on, observe, off.”
5. The adult repeats the closed control and switches off.

**Expected result:** circuit intact, clamps separated, switch off and materials organized.

### 7.4 Experiment — Test one object at a time

**Actor:** coordinated roles; adult within reach.

**Time:** 2–2.5 minutes per object; 8–10 minutes for four objects and 14–18 for seven.

Repeat this sequence for each object:

1. **OFF / OFF.** The Circuit Keeper confirms that the switch is off.
2. **Select / Select.** Materials Investigator delivers a single approved object and remembers the prediction.
3. **Connect / Connect.** Hold a clamp on each end of the same object. The jaws should not touch each other. For children 5–6 years old or with motor difficulties, the adult does it following the child's instructions.
4. **Switch on for two seconds.** No one touches exposed metal or changes the setup during observation.
5. **Observe / Observe.** Evidence Engineer says “turned on”, “did not turn on” or “uncertain”; place the object next to that card.
6. **Switch off and record.** Mark the result before removing the object.
7. **Check if in doubt / Control if uncertain.** If the result was unexpected or faint, turn off, remove the object, hold the check closed for 2 seconds and retest once with clean contact. If still ambiguous, keep `incierto`; Don't force a conclusion.

**en-US — Questions during the test**

- “Are the tweezers touching the object, but not each other?”
- “What did we keep the same in this test?”
- “Does the result make us change any category?”

**en-US — Questions during testing**

- “Are both clips touching the object without touching each other?”
- “What did we keep the same in this test?”
- “Does the result make us change any category?”**Success signal:** Each object has a recorded result and the circuit is turned off before each change.

### 7.5 Improve — improve reliability

**Actor:** group, with a childish decision.

**Objective:** to distinguish contact failure from material property.

**en-US**

Choose a test that was difficult to see or hold. Ask: “How can we make contact the same way without changing the source or circuit?” Choose **one** approved improvement: fold the aluminum into four layers, hold the clips farther apart, place the white card behind the LED, or assign a single person to the switch. Repeat the closed control and then that test once. Compare if the result was clearer.

**en-US**

Choose one test that was hard to see or hold. Ask: “How can we make contact in the same way without changing the power source or circuit?” Choose **one** approved improvement: fold the foil to four layers, place the clips farther apart, put the white card behind the LED, or assign only one person to the switch. Repeat the closed control and then repeat that test once. Compare whether the result became clearer.

**Limit:** Upgrade does not allow you to change batteries, resistance, LED, fixed connections, power or safe list of objects.

### 7.6 Explain — Connect evidence and mechanism

**Actor:** each child contributes according to their role.

**Visual cue required:** conceptual diagram, marked “not to scale”.

**es-US — Children's explanation**

"An electrical current needs a complete path. The spoon and aluminum allowed enough current for this LED to turn on; in this tester they acted as conductors. The plastic, dry wood, cardboard, rubber and dry cloth did not allow enough current to pass through to turn it on; in this tester they acted as insulators. The resistor limits the current to protect the LED. The battery has two sides and the LED must face the correct direction."

**en-US — Child-facing explanation**

"Electric current needs a complete path. The spoon and foil allowed enough current through for this LED to light; in this tester they acted as conductors. The plastic, dry wood, cardboard, rubber, and dry fabric did not allow enough current through to light it; in this tester they acted as insulators. The resistor limits current to protect the LED. The battery has two sides, and the LED must face the correct direction."

**Closing questions**

- What result changed or confirmed your idea? / Which result changed or confirmed your idea?
- How do you know the tester worked? / How do you know the tester was working?
- Why can an off LED mean “uncertain” and not always “isolating”? / Why can an unlit LED mean “uncertain” instead of always meaning “insulator”?
- Where should there be an uninterrupted trajectory? / Where must there be an unbroken path?

## 8. Explanations for the adult

### Brief — `es-US`

The metals tested usually have electrons that can move easily, so they complete the path and pass enough current to light the LED. The dry non-metallic objects on this list offer much more strength. The LED only easily passes current in one direction, and the 330 Ω resistor limits the current.

### Brief — `en-US`The tested metals usually contain electrons that can move readily, so they complete the path and allow enough current to light the LED. The dry nonmetal objects on this list have much higher resistance. The LED conducts readily in only one direction, and the 330 Ω resistor limits current.

### Detailed — `es-US`

Two AA batteries in series provide approximately 3V nominal. When an object joins the clamps, the path is closed: battery, resistance, LED, object and return to the battery. The current in a series circuit passes through all of these elements. The resistor reduces the current to a small range so as not to overload the LED. The anode of the LED must be towards the positive side and the cathode towards the negative; if reversed, it normally does not turn on.

“Conductor” and “insulator” are not absolute labels independent of conditions. Every material has some resistance; This tester only shows whether, with about 3V, the available contact and this LED, enough current flowed to produce visible light. That is why open/closed controls and an uncertain category are used.

### Detailed — `en-US`

Two AA cells in series provide about 3 V nominally. When a sample bridges the clips, the path closes: battery, resistor, LED, sample, and back to the battery. Current in a series circuit passes through each one of those elements. The resistor limits the current to a small range so the LED is not overloaded. The LED anode must face the positive side and the cathode the negative side; when reversed, it normally will not light.

“Conductor” and “insulator” are not absolute labels independent of conditions. Every material has some resistance; This tester shows only whether, at about 3 V, with the available contact and this LED, enough current flowed to make visible light. That is why the activity uses open/closed controls and an uncertain category.

## 9. Approved extensions and adaptations

### 9.1 Optional extension: aluminum switch (8–10 min)

**Additional material:** two 8 × 8 cm / 3 × 3 in squares of dry cardboard, two 3 × 6 cm / 1 × 2.5 in strips of aluminum foil and paper adhesive tape. Adult pre-cuts if scissors are required.

1. Glue a strip of aluminum to each cardboard, leaving most of the metal exposed.
2. Using `OFF`, attach a clamp to each aluminum strip.
3. Turn on the cardboard separately: the LED must remain off.
4. The adult turns on. The child holds only the cardboard edges and brings one cardboard closer to the other until the aluminum faces touch. No one touches aluminum, clamps or connections while in `ON`. The LED should turn on.
5. Explain how opening and closing a separation controls the trajectory.

No voltage, current, temperature or speed is increased. If it doesn't work, go back to the base tester; do not add batteries or remove resistance.

**`en-US` — Optional foil-switch extension:** Add two dry cardboard squares, each about 8 × 8 cm / 3 × 3 in, two foil strips about 3 × 6 cm / 1 × 2.5 in, and masking tape. The adult cuts in advance if scissors are needed. Tape one foil strip onto each square, leaving most of the metal exposed. With the tester `OFF`, the adult attaches one test clip to each strip. The adult switches on while the squares are apart; the LEDs should remain off. The child holds only the cardboard edges and brings the cards together until the foil faces meet. No one touches foil, clips, or connections while the tester is `ON`. The LED should light. Explain how opening and closing the gap controls the path. Do not increase voltage, current, temperature, or speed. If it does not work, return to the base tester; never add cells or remove the resistor.

### 9.2 Presentation adaptations

- Read aloud and use photos of each material; do not require children's reading.
- Use icons `💡`, `○` and `?` together with words; do not code results only by red/green.
- Allow spoken, pointed or drawn response.
- For short attention, try four objects, save the sheet and resume later; the adult turns off and removes the batteries during the pause.

**`en-US`:** Read aloud and use material photos; do not require child reading. Use words and icons together rather than red/green color alone. Accept spoken, pointed, or drawn responses. For a shorter attention window, test four samples, save the sheet, and summarize later; the adult switches off and removes the AA cells during the break.

### 9.3 Motor adaptations

- Fix the tester to a non-slip tray without covering ventilation or switch.
- The adult opens and places the tweezers; the child directs the contact points, flips the switch if he or she can do so safely, and classifies the object.
- Use only large objects from the list. Do not replace with beads, coins, screws or small parts.

**`en-US`:** Secure the tester to a nonslip tray without blocking the switch. The adult opens and positions clips while the child directs contact points, operates the switch if safe, and classifies the sample. Use only the large listed objects; do not substitute beads, coins, screws, or other small parts.

### 9.4 Approved challenge increases

- Ask for a diagram of the trajectory and an explanation of the role of resistance.
- Conceal a single safe separation in the assembly **with the switch off and created by the adult**; the child locates it through visual inspection and controls, without opening the battery door or removing insulation.
- Compare the same aluminum strip with contact on exposed metal and with a small area covered by paper tape. Register that the coating blocks contact at that point; do not conclude that aluminum stopped conducting.

**`en-US`:** Approved challenge options are: draw the complete path and explain the resistor; locate one safe gap created by the adult while the tester is off, without opening the holder or removing insulation; or compare contact on exposed foil with contact on a small masking-tape-covered area. Remember that the coating blocks contact at that point, not that the foil stopped conducting.

## 10. Bilingual troubleshooting

Before any diagnosis: `OFF`, dry hands, adult in charge. Never resolve by adding batteries, removing the resistor or testing an external source.

| Problem | Probable cause | Safe Action `es-US` | Safe action `en-US` |
|---|---|---|---|
| The LED does not light in the closed control | Switch off, batteries reversed or weak, LED reversed, or loose connection | Turn off. The adult checks polarity and covered connections; replace both AA cells together if depleted. Do not allow a child to handle the battery holder. | Switch off. The adult checks polarity and covered connections; replace both AA cells together if depleted. Do not allow a child to handle the battery holder. |
| The LED lights up with the clamps separated | The jaws or cables touch; there is an unforeseen bridge | Turn off and separate cables. The adult inspects the assembly. Do not continue until reliable open control is recovered. | Switch off and separate the leads. The adult inspects the setup. Do not continue until the open control is reliable. |
| The LED lights up with all objects | The tweezers touch each other around the object | Turn off and place the forceps on far ends without direct contact between jaws. Repeat open check. | Switch off and place clips at separated ends without jaw-to-jaw contact. Repeat the open control. |
| A metal does not light | Contact on paint/coating, dirt, loose clamp or weak batteries | Do not scrape or cut. Use the control spoon or aluminum, clean and dry; make closed control. Log `incierto` if it persists. | Do not scrape or cut. Use the clean, dry control spoon or foil; perform the closed control. Record `uncertain` if it persists. |
| The LED looks very dim | Strong ambient light, poor contact or object resistance | Place white card behind the LED, improve contact without changing circuit and repeat once. Do not reduce the resistance. | Put the white card behind the LED, improve contact without changing the circuit, and repeat once. Do not lower the resistor value. |
| LED, resistor, cable or batteries become hot; there is odor, smoke, leak, corrosion or spark | Damage or incorrect connection | Turn off only if you can do so without approaching or touching the hazard. Keep children away. Do not open the battery door or remove batteries while they are hot, smoking, sparking, or leaking. Follow the manufacturer's guide and remove the assembly from service. | Switch off only if this can be done without approaching or touching the hazard. Move children away. Do not open the holder or remove cells while it is hot, smoking, sparking, or leaking. Follow the manufacturer guidance and remove the setup. |
| The group loses correspondence between object and result | Too many objects or simultaneous changes | Return all objects to the row and test one at a time with verbal relief. Do not attribute individual evidence if it is not known who performed the action. | Return all objects to the row and test one at a time with the verbal handoff. Do not attribute individual evidence if the actor is unclear. |

## 11. Safety and cleanliness

### Risks and controls

| Danger | Exposed person/condition | Mandatory control |
|---|---|---|
| Ingestion or improper use of batteries/components | Children, especially 5–7 years old | Adult inserts, withdraws, counts and saves; closed battery door; not coin batteries; Stop if a child puts objects in his or her mouth. |
| Prick or pinch of tweezers | Children's fingers | Small tweezers isolated and intact; close help; adult operates for 5–6 years or when coordination is not sufficient. |
| Heating due to incorrect connection or short outside the limited circuit | All | Mandatory series resistance; covered fixed joints; prior control; switch `OFF` between samples; adult within reach. |
| Loose fixed joint, pull or exposed terminal | Children and adult during handling | Selected configuration with validated strain relief; adult inspection before each use; Remove any movement, rotation or visible fixed metal. |
| Contact with external energy | All | Test only dry, loose and listed objects; table away from outlets/devices; explicit prohibitions repeated before testing. |
| Stack Leak | All | Inspection before use; do not use damaged batteries; do not open or remove while heat/smoke/spark/leak exists; keep children away and follow the manufacturer's guide. |
| Confusion due to a negative result | Learning | Closed control before and after doubtful result; category `incierto`; qualitative explanation. |

#### Risk matrix `en-US`

| Hazard | Exposed person/condition | Mandatory control |
|---|---|---|
| Ingestion or misuse of cells/components | Children, especially ages 5–7 | Adult alone inserts, removes, accounts, and stores; holder stays closed; no coin cells; stop if an item approaches the mouth. |
| Clip pinch or puncture | Children's fingers | Use intact small insulated clips with close help; adult operates for ages 5–6 or whenever coordination is insufficient. |
| Heating from incorrect connection or a short outside the limited path | Everyone | Resistor always in series; fixed joints covered; pre-check controls; `OFF` between samples; adult within reach. |
| Loose fixed joint, pull, or exposed terminal | Children and adults during handling | Selected configuration has validated strain relief; adult inspects before every use; remove upon any movement, rotation, or visible fixed metal. |
| Contact with external energy | Everyone | Test only listed dry, loose samples; keep table away from outlets/devices; repeat prohibitions before testing. |
| Cell leakage | Everyone | Inspect before use; never use damaged cells; do not open/remove while there is heat, smoke, a spark, or leakage; move children away and follow manufacturer's guidance. |
| Misreading a negative result | Learning | Closed control before/after doubtful result; retain `uncertain`; use qualitative explanation. |

### Stop signs

Stop immediately if a child tries to test a person, animal, liquid, plug, cord, battery or device; if someone puts a component in their mouth; if the insulation is broken; if a connection cannot be kept covered; or if unexplained heat, odor, smoke, spark, corrosion, leak, or intermittent behavior appears.

**`en-US` stop conditions:** Stop immediately if a child tries to test a person, animal, liquid, outlet, cable, battery, or device; if anyone puts a component in their mouth; if insulation breaks; if a fixed connection cannot remain covered; or if there is heat, odor, smoke, a spark, corrosion, leakage, or unexplained intermittent behavior.

### Cleaning and storage — adult only for the circuit

1. Set the switch to `OFF`.
2. Remove the two AA batteries and store them according to the manufacturer's instructions, out of the reach of children. Do not leave batteries installed between sessions.
3. Count LED, resistor, wires and batteries; do not leave small components loose.
4. Separate everyday objects. Recycle or save aluminum without protruding edges.
5. Save the tester as a drive labeled `3 V — ACT-0003`; Remove from service if tape or insulation comes loose.
6. Wipe the table dry. Do not wash the circuit or use sprays or liquids on it.

**`en-US` cleanup and storage:** The adult switches `OFF`, removes both AA cells, and stores them according to the manufacturer, out of children's reach. Do not leave cells installed between sessions. Count the LED, resistor, leads, and cells; leave no small parts loose. Recycle or store foil without projecting edges. Store the tester as one unit labeled `3 V — ACT-0003` and remove it if tape or insulation lifts. Dry-clean the table; never wash or spray the circuit.

## 12. Observation and evaluation

### 12.1 Automatic registration

If a child participated, automatically record:

- ActivityVersion `ACT-0003@0.1.2`.
- Actual role and configuration of participants.
- Primary objective assigned.
- Exposures planned according to your role.
- Adaptation used and if there was equipment failure.

Participation or exposure does not become evidence of independence. If a child did not participate, do not create an exposure or request an assessment.

### 12.2 Questions by eligible objective

Independence is valued solely on the actions permitted for the child. A mandatory adult action for safety—inserting batteries, holding 5–6 year old clips, protecting joints, or stopping the circuit—is an environmental condition and **does not reduce** the score. It does count as help when the adult makes the evaluated cognitive decision for the child, indicates each response or executes a permitted child action that the child needed to practice.

**`en-US`:** Rate independence only on actions the child is permitted to perform. Safety-required adult action—such as inserting cells, holding clips for ages 5–6, protecting fixed joints, or stopping the circuit—is an environmental control and **does not lower** the rating. Adult action counts as help when the adult makes the assessed cognitive decision, supplies each answer, or performs a permitted child action the child was meant to practice.

| Objective | Question `es-US` | Question `en-US` | Yes it counts as evidence | It doesn't count on its own | External factors |
|---|---|---|---|---|---|
| `LOG-CLASSIFY-EVIDENCE` | How independently did you classify the objects based on what the LED showed? | How independently did they classify the objects based on what the LED showed? | Place each object according to the observed result and correct a prediction when appropriate. | Guess categories before testing; copy another child. | Didn't see LED, objects mixed up, role changed. |
| `ELE-SEQUENCE-TEST` | How independently did you direct and follow your permitted actions in the turn off–place–on–watch–turn off sequence? | How independently did they direct and follow their permitted actions in the off–place–on–observe–off sequence? | Maintains or verbalizes order, waits for mandatory adult action, and requests help before an unsafe change. | Quick manipulation without respect `OFF`; the adult decided and announced each step. | Difficult switch, mandatory motor support, intermittent assembly. |
| `ELE-CLOSE-PATH` | How independently did you identify where the path needed to be closed to turn on the LED? | How independently did they identify where the path had to close to light the LED? | Point out the separation or describe the complete route. | Repeat “circuit” without locating the interruption. | Unclear diagram, hidden joints. |
| `LOG-CONTROL-VARIABLE` | How independently did you keep conditions the same when comparing objects? | How independently did they keep the test conditions the same across samples? | Uses same circuit, sequence and comparable contact; asks to repeat a doubtful. | Obtain many results with simultaneous changes. | Tweezers difficult to hold, another participant changed the assembly. |
| `MAT-RECORD-RESULT` | How independently did you record each result next to the correct object? | How independently did they record each result with the correct object? | Retains correspondence and mark uncertain when applicable. | Complete page written by another; decorate without registering. | Demand for writing, loss of paper, confusing shifts. |
| `COM-EXPLAIN-CIRCUIT` | How independently did you explain a result using the circuit path? | How independently did they explain one result using the circuit path? | Links complete path with LED on and recognizes tester limits. | Saying “just because” or “all metals always light up” without evidence. | Bilingual vocabulary, shyness, preference for pointing/drawing. |

### 12.3 Contextual scale 1–5

| Value | Anchor `es-US` | Anchor `en-US` |
|---:|---|---|
| 1 | He couldn't do it yet, even with reasonable support. | Could not do it yet, even with reasonable support. |
| 2 | He did it with a lot of help. | Did it with substantial help. |
| 3 | He did it with some help. | Did it with some help. |
| 4 | He did it almost single-handedly. | Did it almost independently. |
| 5 | He did it independently and safely. | Did it independently and safely. |

### 12.4 Closing flow

- Show only the children who participated.
- Request an evaluation of a touch by primary objective and child.
- With three children, the normal route is three touches and should be tested under 20 seconds.
- Offer `Evaluar más / Evaluate more` secondary for additional skills.
- Offer an optional voice or text note for the entire session.
- Allow `Omitir / Skip`, `Problema con el equipo / Equipment issue` and post correction.
- If the children collaborated inseparably, record group evidence; do not attribute individual performance without confirmation.

### 12.5 Examples of valid observation

- “During ACT-0003, Lina classified six objects based on the LED and changed the spoon from her prediction ‘no’ to ‘on’ without help.”
- “During ACT-0003, Mateo followed the sequence with reminders to turn off before changing each object.”
- “The closed control failed twice; the conductivity results of this session should not feed inferences.”

These observations retain context and support. They do not produce global labels about ability, intelligence, or personality.

## 13. Visual resource briefs

All assets link to `ACT-0003@0.1.2`, pass automated QA and human approval, and contain text as a programmatic layer. Do not show faces, brands, plugs, liquids, coin batteries, USB source or children manipulating the battery holder.

### ACT-0003-VIS-01 — Photorealistic Materials board

- **Type:** materials board, photorealistic overhead view.
- **Contents:** 2 AA closed battery holder with switch, two alkaline AAs next to it but in an area marked for adults, red LED, 330 Ω labeled resistance, four cables with insulated clamps, insulating tape, metal spoon, folded aluminum, plastic ruler, stick, cardboard, silicone spatula, cloth, sheet and crayon.
- **Composition:** separate objects, coherent scale, neutral dry background; adult components visually grouped with adult hand icon.
- **Exclude:** generated text, ambiguous electrical connections, additional objects, markings, installed batteries, child hands.
- **Alt `es-US`:** Tester materials separated on a table: two AA battery holder, red LED, 330 ohm resistor, insulated wires, and seven dry objects to test.
- **Alt `en-US`:** Conductivity tester materials separated on a table: a two-AA holder, red LED, 330-ohm resistor, insulated leads, and seven dry test objects.

### ACT-0003-VIS-02 — Photorealistic adult preparation + overlay

- **Type:** preparation, photorealistic detail with programmatically superimposed lines.
- **Content:** adult hands connecting with switch `OFF`; red path `+` → resistor → long leg of the LED → clamp A; clamp B → black `−`; batteries still out.
- **Moments:** panel A before inserting batteries; panel B fully covered fixed joints; panel C only the two test clips are free and separated.
- **Exclude:** soldering iron, breadboard, child clamp, exposed metal in fixed joints, direct red-black connection.
- **Alt `es-US`:** Adult hands prepare a series circuit with the switch off and cover the fixed joints before inserting the batteries.
- **Alt `en-US`:** Adult hands prepare the series circuit with the switch off and cover fixed joints before inserting batteries.

### ACT-0003-VIS-03 — Instructional circuit diagram

- **Type:** instructional diagram, not to scale.
- **Content:** simple symbols and recognizable objects in a single path: 2×AA, switch, 330 Ω, LED with anode/cathode, two probes and block `sample/material`; Optional conventional arrows clearly labeled as conventional current.
- **States:** left side open circuit with separate clamps/LED off; Right side shows metal between clamps/LED on.
- **Accessibility:** `+`/`−`, shapes and labels as well as colors; high contrast.
- **Alt `es-US`:** Diagram of an open circuit with the LED off and the same circuit closed by a metal sample with the LED on.
- **Alt `en-US`:** Diagram of an open circuit with the LED off and the same circuit closed by a metal sample with the LED on.

### ACT-0003-VIS-04 — Test Sequence

- **Type:** step diagram with five bullets.
- **Content:** `OFF` → place tweezers on the ends of the object without touching them → `ON 2 s` → observe → `OFF y registrar`.
- **Actor:** for 5–6 year old context, adult hands place the tweezers while a child's hand points to the contact point, uses a result card, or flips the switch with permission; do not show childish hands operating tweezers. For older adults with sufficient coordination, a separate vignette can show children's tweezers with close adult supervision. Never show manipulation of batteries or fixed joints by children.
- **Alt `es-US`:** Five steps show power off, hold a dry object, power on for two seconds, observe the LED, and power off before recording.
- **Alt `en-US`:** Five steps show switching off, clipping onto a dry object, switching on for two seconds, observing the LED, and switching off before recording.

### ACT-0003-VIS-05 — Photorealistic expected results

- **Type:** expected result, three panels.
- **Contents:** spoon with LED on; plastic ruler with LED off; example of doubtful contact marked `?` without claiming result.
- **Critical control:** the jaws must contact separate ends and not touch directly.
- **Alt `es-US`:** Comparison between a spoon that turns on the LED, a plastic ruler that does not turn it on, and a doubtful contact that must be repeated.
- **Alt `en-US`:** Comparison of a spoon that lights the LED, a plastic ruler that does not, and uncertain contact that should be repeated.

### ACT-0003-VIS-06 — Polarity and Contact Troubleshooting

- **Type:** troubleshooting diagram.
- **Content:** correct/incorrect comparison of longleg towards `+`; pincers separated on object versus jaws touching; symbol `OFF` before correcting.
- **Exclude:** suggest investing with energy, removing resistance, adding batteries or scraping objects.
- **Alt `es-US`:** Correction diagram with the tester off: correct polarity of the LED and separated clamps on the sample.
- **Alt `en-US`:** Switch-off correction diagram showing proper LED polarity and test clips separated across the sample.

### ACT-0003-VIS-07 — Conductive/insulating concept

- **Type:** concept diagram, marked `explicativo; no a escala / explanatory; not to scale`.
- **Content:** continuous path through metal compared to blocked path in dry plastic; visible resistance always in series; cautious text “enough current for this LED”.
- **Alt `es-US`:** Conceptual diagram where a metal completes the path and a dry plastic does not allow enough current to pass through this LED.
- **Alt `en-US`:** Concept diagram where metal completes the path and dry plastic does not allow enough current for this LED.

## 14. Preliminary electrical check

This section documents the plausibility of the design; it does not replace physical execution or specialist review.

- An AA alkaline cell has 1.5 V nominal and can approach 1.6 V open circuit when fresh; two in series are conservatively modeled as up to 3.2 V for initial calculation. Source: [Energizer Alkaline Manganese Dioxide Handbook](https://data.energizer.com/pdfs/alkaline_appman.pdf).
- A reference high-efficiency red LED has a typical forward dropout of 1.9 V at 10 mA and continuous limit of 30 mA. Reference source: [Kingbright WP1053IDT datasheet](https://www.kingbrightusa.com/images/catalog/spec/WP1053IDT.pdf). The final editorial piece must have the same or more restrictive specification and be linked to the approved list.
- Illustrative estimate with nominal values: `(3.0 V − 1.9 V) / 330 Ω ≈ 3.3 mA`; with 3.2 V, `≈ 3.9 mA`. The 1.9 V drop on the datasheet is specified at 10 mA, so this count does not replace actual current measurement.
- With a tolerance of −5%, the minimum resistance is `330 Ω × 0.95 = 313.5 Ω`. A failure bound that treats the LED dropout as zero is `3.2 V / 313.5 Ω ≈ 10.2 mA`. Therefore, this version **does not promise** to keep the loop below 10 mA.
- Corresponding conservative power in the resistor: `3.2² / 313.5 ≈ 0.033 W`, still much less than 0.25 W.
- The gate must repeat the calculation with maximum documented voltage of the chosen batteries, minimum resistance per tolerance and limits of the exact LED/module. The maximum calculated current must be below the permitted continuous current with the margin approved by the electrical inspector; a generic specification of “at least 10 mA” is not enough.
- Polarity matters: the LED is a diode. The design avoids deliberately applying reverse voltage and requires checking the long leg/anode toward positive before inserting batteries.
- The test only applies to objects isolated from any other source. Professional continuity practices also require testing components without external power; see [Fluke — A Guide to Continuity Testing](https://www.fluke.com/en-ca/learn/blog/digital-multimeters/how-to-test-for-continuity).

**Pilot Pending Finding:** Confirm visibility of selected LED at actual current under home lighting. If it is not sufficient, the resistance is not automatically reduced: the gate evaluates another high efficiency red LED with part number or the candidate module B and records a new revision before selecting it.

## 15. Gates and validation plan before publishing

### Mandatory reviews

- [ ] Pedagogical review: observable objectives, language 5–10 and roles with agency.
- [ ] Electrical/safety inspection by competent professional: exact components, battery holder, current with tolerances, insulation, safe failure and bilingual warnings.
- [ ] Mechanical review: terminals, separation, stress relief, pull resistance, tape/cover fatigue and detachment behavior.
- [ ] Decision A vs B: compare residual risk, mechanical retention, ease of assembly, availability and pedagogical value; select a single configuration and remove the other from the family bundle of the next version.
- [ ] Child Co-Assembly Gate: Compare at least one de-energized physical path in which the child makes meaningful connections with accurate, protected, and age-appropriate pieces; define in writing actions allowed by rank, adult inspection, prevention of incorrect connections and stopping criteria. If no route passes the gate, keep the joins fixed as `adult-only` and explain the limitation to the founder before the pilot.
- [ ] Bilingual review `es-US`/`en-US`, with special attention to `adult-only`, prohibitions and troubleshooting.
- [ ] Automatic and human visual QA from ACT-0003-VIS-01 to ACT-0003-VIS-07.
- [ ] Accessibility and flow review with divided attention.

### Minimum executions proposed for level C and reinforced gate

- [ ] A complete run by the author/publisher with exact timing and component recording.
- [ ] At least three additional runs in two families, including one led by an adult who did not write the activity.
- [ ] At least one individual case, one of two children and one of three children within 5–10 years.
- [ ] Confirm main evaluation of three children in less than 20 seconds.
- [ ] Record each failure, uncertain outcome, adult intervention, role conflict and time deviation.

### Safety Test Cases

- [ ] The open control remains off and the closed control turns on in ten consecutive cycles.
- [ ] With batteries removed, each joint/cable passes a pull test whose method, force and duration is defined and recorded by the competent reviewer; There is no shifting, twisting, exposed fixed metal or insulation damage.
- [ ] The assembly passes ten complete cycles of preparation, representative handling, open/close control, shutdown and inspection without loosening, detachment or intermittent shifting.
- [ ] The fixed joints are not accessible to normal child handling and the strain relief works without relying solely on adhesive tape.
- [ ] The system/editor does not accept replacement by 9V, USB, coin battery, household power, liquid or device.
- [ ] A coated object produces explanation `incierto`, not a false generalization.- [ ] A control failure invalidates the evidence materials from that session.
- [ ] No components become noticeably hot during 2-second tests or a 30-second accidental closed check; the extended test is performed only by the adult reviewer.

## 16. Traceability

| Requirement/decision | Implementation in this ActivityVersion |
|---|---|
| P-01, LRN-006 | Discover–Imagine–Build–Experiment–Improve–Explain cycle; separate practice, presentation and evaluation. |
| P-02 | Everyday objects; only the small tester requires defined electrical components. |
| P-03, ACT-002 | State `draft`; not deliverable until publication and gates. |
| P-05, ACT-004, DEC-034 | Actual roles and settings for 1–3 children within the 1–4 boundary. |
| P-06, DEC-004–008, EVD-002–006 | One goal and assessment per child; “Evaluate more” and voice optional; close under 20s. |
| P-07, EVD-007–009 | Contextual observations, external factors and correction; no labels. |
| P-10, SAFE-001–009 | Structured risks, adult steps, 2 AA, resistance, prohibitions and adaptation limits. |
| P-11 | Adult changes objectives, helps, omits evaluation and decides to stop. |
| ACT-001, ACT-006–012 | Identity/versioning, bilingual bundles, troubleshooting, review and version-bound assets. |
| ACT-VIS-001–004, DEC-021, DEC-027 | Photorealistic briefs/diagrams; QA and human approval; correct actors. |
| DEC-014 | US market, English/Spanish, ages 5–10. |
| DEC-026 | The app guides the adult; the child participates off screen. |

## 17. Editorial result required to advance

To move from `draft` to `pedagogical_review`, the team must formally decide between A and B, select concrete part numbers for all components of the chosen configuration, document the diagram and stress relief, evaluate the child co-assembly gate, pass the pull test and ten cycles, execute the assembly, complete the results matrix with the seven objects, measure time and brightness, and resolve all gate findings. The unchosen configuration is removed from the family bundle in the next version. Any changes to font, resistance, luminous component, mechanical retention, allowed objects, child permissions or safety steps create a new version and repeat the affected revisions.
