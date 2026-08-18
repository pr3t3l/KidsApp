(function () {
  "use strict";

  const localeKey = "kids-learning-system-locale";
  const query = new URLSearchParams(window.location.search);
  const requested = query.get("lang");
  let saved = null;
  try { saved = localStorage.getItem(localeKey); } catch (_) { /* Local storage can be unavailable in previews. */ }
  const browserLocale = navigator.language?.toLowerCase().startsWith("es") ? "es" : "en";
  const locale = ["es", "en"].includes(requested) ? requested : (["es", "en"].includes(saved) ? saved : browserLocale);
  try { localStorage.setItem(localeKey, locale); } catch (_) { /* The selector still works for this page load. */ }

  const en = {
    learners: [
      { id: "sofi", name: "Sofi", initials: "SO", age: "ages 5–6", color: "cyan" },
      { id: "mateo", name: "Mateo", initials: "MA", age: "ages 7–8", color: "yellow" },
      { id: "leo", name: "Leo", initials: "LE", age: "ages 9–10", color: "coral" }
    ],
    learningFocuses: {
      designer: {
        title: "Design and test a shape",
        objective: "Propose a shape, build it, and connect the result of their own test to a design decision.",
        question: "How independently did they propose, build, and test a shape using what they had observed?",
        contribution: "Mateo will build and test his own bridge, then propose a change based on the result.",
        reason: "With no prior evidence, this open-ended challenge offers appropriate growth for ages 7–8. Age guides the first opportunity; it does not predict ability.",
        exposure: "counting, folding, fair comparison, and explanation"
      },
      tester: {
        title: "One-to-one counting",
        objective: "During their own test, add one crayon per turn, say one number, and keep or recover the total after waiting.",
        question: "How independently did they add and count one crayon at a time during their own test?",
        contribution: "Sofi will build and test her own bridge; during her turn, she will match one crayon to each number.",
        reason: "With no prior evidence, one-to-one counting with a pause can consolidate learning at ages 5–6. We do not assume it will be easy or hard for her.",
        exposure: "design, structure, prediction, comparison, and explanation"
      },
      coordinator: {
        title: "Fair comparison",
        objective: "Check that distance, orientation, cup, paper, and load stay the same before their test and the other tests.",
        question: "How independently did they check that the conditions stayed the same?",
        contribution: "Leo will build and test his own bridge; he will also use the conditions checklist before each turn.",
        reason: "With no prior evidence, controlling several conditions offers possible growth at ages 9–10. This is not assigned just because he is older and does not imply mastery.",
        exposure: "design, counting, measurement, recording, comparison, and communication"
      }
    },
    stages: [
      {
        name: "Discover", time: "6 min", eyebrow: "See the problem in action",
        title: "Test the flat sheet first",
        purpose: "Understand what the cup and crayons are for and obtain a real result that starts the rest of the activity.",
        entry: "The setup is ready, but you do not yet know how a flat sheet will respond.",
        exit: "You have an observation and a baseline result to help imagine changes.",
        skills: ["prediction", "counting", "load and bending"],
        adultActions: [
          "Name each function: the books are supports; the paper is the bridge; the empty cup will sit in the center and hold the load; each crayon is one unit of load.",
          "Lay a flat sheet across the 6 in / 15 cm gap. Ask what they think will happen and record one prediction per child.",
          "Center the empty cup. After it stays stable for three seconds, invite children to add one crayon per turn, say the number, and wait three seconds. Stop and record the last stable amount."
        ],
        say: "This cup holds the crayons in the center of the bridge. Each crayon adds the same kind of load. What do you think this flat sheet will do as the cup begins to fill?",
        actions: {
          designer: "Predicts where it will bend; on their turn, adds one crayon and watches the shape.",
          tester: "Starts the count: adds one crayon, says one number, and waits for the signal before the next turn.",
          coordinator: "Predicts and checks that the books, paper, and cup do not change during the test."
        },
        decision: "Each child chooses how to share a prediction: speaking, pointing, or drawing.",
        observe: "Notice whether they connect one crayon to one number and whether they see where the paper changes. A correct prediction is not the goal.",
        success: "You recorded what the flat sheet did and the problem you need to solve; there is now a reason to imagine other shapes.",
        warning: "The adult centers the cup and moves the books. Children add crayons only after the signal, one turn at a time, without placing hands or faces underneath.",
        helpOptions: [
          { problem: "They look for the correct answer", change: "Say, ‘We do not know yet; the test will give us information.’", impact: "Keeps prediction exploratory instead of evaluative.", resume: "Ask again for an idea by voice, gesture, or drawing.", limit: "Do not push the paper or run a partial test." },
          { problem: "A child does not want to answer", change: "Let the child watch and rejoin during another phase.", impact: "Do not record a prediction or a negative signal.", resume: "Continue after anyone who wants to share has offered an idea.", limit: "Do not force participation or attribute difficulty." }
        ]
      },
      {
        name: "Imagine", time: "5 min", eyebrow: "From the problem to three ideas",
        title: "Each child chooses a shape",
        purpose: "Use what happened to the flat sheet, introduce possible shapes, and turn each child's idea into a buildable plan.",
        entry: "The flat sheet has shown where and when it bends.",
        exit: "Each child has a design and everyone knows which conditions will not change.",
        skills: ["design", "fair comparison", "communication"],
        adultActions: [
          "Remove the cup and crayons. Ask how they could change the shape of one sheet to make it harder to bend; record every idea.",
          "Using the tested flat sheet, demonstrate only the beginning of an accordion fold: fold one strip, turn it over, and fold another. Also show the channel and wide-fold diagrams.",
          "Ask each child to choose or draw a shape for their own sheet. Confirm that the paper, 6 in / 15 cm gap, cup, crayons, and procedure will stay the same."
        ],
        say: "We saw what the flat sheet did. Which shape will each of you test? You may use an accordion, channel, wide folds, or another approved idea. What must stay the same so we can compare?",
        actions: {
          designer: "Chooses or draws a shape and explains which feature they want to test.",
          tester: "Chooses or draws a shape and predicts more, less, or the same as the flat sheet.",
          coordinator: "Chooses or draws a shape and uses the checklist to name what must stay the same."
        },
        decision: "Each child chooses a shape for their own test. They do not have to choose the same one or guess which will work best.",
        observe: "Notice whether each child connects the shape to something observed in the flat sheet and separates their change from the fixed conditions.",
        success: "Sofi, Mateo, and Leo each have an identified plan; building is now the logical next step.",
        warning: "Do not add tools, fasteners, another sheet, or a different load.",
        helpOptions: [
          { problem: "A child has too many ideas", change: "Draw all of them and ask the child to mark one for the first sheet.", impact: "Practices choosing without discarding creativity; the other ideas can become improvement suggestions.", resume: "Confirm what will change in the design and what will stay the same.", limit: "Do not combine several changes in one test." },
          { problem: "A child does not know which shape to suggest", change: "Point to two approved diagram options and ask the child to choose one for their sheet.", impact: "It remains the child's choice within a safe, approved set.", resume: "Ask what they think will happen with the selected option.", limit: "Do not promise which shape will hold more." }
        ]
      },
      {
        name: "Build", time: "8 min", eyebrow: "One design per child",
        title: "Each child builds a bridge",
        purpose: "Turn the three plans into identifiable structures that can be tested separately.",
        entry: "Each child has selected a shape and the group knows which conditions will stay the same.",
        exit: "There is one identified structure per child, ready for an individual test.",
        skills: ["sequence", "fine-motor skills", "orientation"],
        adultActions: [
          "Give each child an identical sheet and set aside the flat sheet you already tested. Label the new sheets with a name or symbol.",
          "Ask each child to show the plan before folding. If needed, mark guides or steady the paper; do not change their idea to make it ‘win.’",
          "When they finish, place the structures in test order and check that each one can rest across both books."
        ],
        say: "Now each of you will turn your idea into a bridge. It may look different from the drawing; what matters is that we can recognize the shape you wanted to test.",
        actions: {
          designer: "Builds their own shape and points out one feature they chose intentionally.",
          tester: "Builds their own shape with the support they need and labels the sheet with a name or symbol.",
          coordinator: "Builds their own shape and checks that its orientation matches the test plan."
        },
        decision: "Each child decides how to make the shape and when it is ready enough to test.",
        observe: "Notice which parts each child does and what support they need. Do not score appearance; record only actions connected to the learning focus.",
        success: "Sofi, Mateo, and Leo each have a recognizable, labeled structure that can rest on the books.",
        warning: "Use intact paper. Do not use scissors, clips, tape on the bridge, or other fasteners.",
        helpOptions: [
          { problem: "A child has trouble forming the design", change: "Steady the paper, mark one guide, or model one movement on the demonstration sheet; then return the action to the child.", impact: "Preserves authorship and makes the support visible.", resume: "Continue from the last action the child can recognize.", limit: "Do not cut, fasten, or silently replace the child's design." },
          { problem: "A structure is uneven or flattened", change: "Ask whether the child wants to test it as it is or make one small adjustment before calling it ready.", impact: "The child decides, and the result remains informative.", resume: "Label the sheet and place it in test order.", limit: "Do not rebuild it until what happened is hidden." }
        ]
      },
      {
        name: "Experiment", time: "10 min", eyebrow: "One complete turn per child",
        title: "Test each bridge separately",
        purpose: "Give each child their own test and produce comparable results by keeping the other conditions the same.",
        entry: "There are three labeled structures and a result for the flat sheet.",
        exit: "Each child completed a test and has a recorded result or observation.",
        skills: ["one-to-one counting", "controlling variables", "observation"],
        adultActions: [
          "Name whose turn it is. Before each design, reset the books to 6 in / 15 cm, place the structure with similar support, and center the empty cup yourself.",
          "Invite that child to add one crayon, say the number, and wait three seconds before the next one. Everyone else watches where the shape changes.",
          "Record the last stable amount or what happened. Remove the cup and crayons, reset the setup, and repeat until every child has tested their own bridge."
        ],
        say: "Now it is [name]'s test. You will add and count one crayon at a time. The rest of us will watch what the shape does. Then we will reset the setup for the next bridge.",
        actions: {
          designer: "Tests their own design, counts the load, and connects where it bent to a feature of the shape.",
          tester: "Tests their own design: adds one crayon, says one number, and waits for the signal before continuing.",
          coordinator: "Checks the list of conditions and then tests their own design using the same procedure."
        },
        decision: null,
        observe: "For Sofi, observe one crayon–one number correspondence; for Mateo, the connection between shape and result; for Leo, control of conditions. Watching another child's test does not replace their own.",
        success: "There is a result or observation for the flat sheet and for Sofi's, Mateo's, and Leo's structures; noncomparable tests are marked as such.",
        warning: "No one places hands or faces under the setup. Stop if a book moves, something breaks, someone throws a crayon, or material goes near a mouth.",
        helpOptions: [
          { problem: "The bridge bent and the cup fell", change: "Wait for everything to stop moving. Record the last stable amount and remove the load.", impact: "This is a result of the structure, not the child's mistake.", resume: "Repeat the complete adult safety check before the next design.", limit: "Do not chase crayons or add a different type of load." },
          { problem: "The cup was off-center or a book moved", change: "Mark the test NOT COMPARABLE; do not save a number.", impact: "Prevents false evidence about design or counting.", resume: "Reset the 6 in / 15 cm gap, supports, and empty cup once.", limit: "Only the adult moves the books." },
          { problem: "You lost count", change: "Stop the test, remove every load, and return to zero.", impact: "Does not guess the result and preserves counting practice.", resume: "Start again with the empty cup and the adult signal.", limit: "Do not continue from an uncertain total." }
        ]
      },
      {
        name: "Improve", time: "6 min", eyebrow: "Three suggestions, one group test",
        title: "Choose and test an improvement",
        purpose: "Use the individual results to suggest changes and test a new version together.",
        entry: "Each child has the result of their own design and can compare it with the flat sheet.",
        exit: "The group selected one suggestion, built a new version, and recorded its test.",
        skills: ["iteration", "decision-making", "prediction"],
        adultActions: [
          "Place the unloaded designs beside their results. Ask each child to suggest one change and say which observation inspired it.",
          "Help them choose one suggestion, or combine only compatible features, without changing materials or conditions. Give them the reserved group sheet.",
          "Share the actions so everyone helps build it, then repeat the complete Experiment procedure once."
        ],
        say: "Each of you now has information from your bridge. What change do you suggest, and what did you see that led to that idea? We will choose one idea to test together.",
        actions: {
          designer: "Suggests a change based on their result and helps turn the chosen idea into a new shape.",
          tester: "Suggests a change based on their result, predicts more, less, or the same, and participates in the new test.",
          coordinator: "Suggests a change, confirms what stays the same, and records the group decision and result."
        },
        decision: "The three children choose which suggestion to test and how to share the group build and test.",
        observe: "Notice whether each suggestion comes from something seen or counted. The new version may hold less and still produce valid learning.",
        success: "Each child suggested a change, and the group built and tested a new version while preserving the conditions.",
        warning: "Do not change the distance, weight, cup, number of sheets, or add adhesives. Maximum 20 crayons.",
        helpOptions: [
          { problem: "They want to change several things", change: "Draw every idea and let the group mark just one.", impact: "Keeps the test interpretable and preserves the other ideas.", resume: "Say, ‘We will change this part; the other conditions will stay the same.’", limit: "Do not combine options on the group sheet." },
          { problem: "The new design held less", change: "Keep the result and ask what may have influenced it.", impact: "Iteration is evaluated by deciding and testing, not by winning.", resume: "Continue to Explain with all the results.", limit: "Do not alter the distance or load to force a difference." }
        ]
      },
      {
        name: "Explain", time: "2 min", eyebrow: "A story from beginning to end",
        title: "Each child shares what they learned",
        purpose: "Connect their own shape, its result, and the group improvement using something seen, counted, or compared.",
        entry: "The flat sheet, each individual design, the group improvement, and their results are visible.",
        exit: "Each child shared a personal connection and the group closed the story of the investigation.",
        skills: ["explanation", "comparison", "reflection"],
        adultActions: [
          "Remove every load and place the flat sheet, each individual design, and the group improvement beside their results.",
          "Invite each child to point to their bridge, say what happened, and connect that result to the chosen improvement. Listen before explaining it yourself."
        ],
        say: "Point to your bridge: what did you make, what happened in your test, and what did you suggest for the group's version?",
        actions: {
          designer: "Explains one shape decision, the result, and what they would change next.",
          tester: "Counts or compares the result using more, less, or the same and points to the group improvement.",
          coordinator: "Names one condition that stayed the same and connects their test to the group decision."
        },
        decision: "Each child chooses whether to explain by speaking, pointing, drawing, or selecting among the results.",
        observe: "Look for a connection between the design and something observed. Repeating the adult's explanation does not count as independent evidence.",
        success: "Each child shares a connection between their design, a result, and the improvement; celebrate decisions and method, not the highest number.",
        warning: "The designs have no load on them. Compare designs, never children or siblings' abilities.",
        helpOptions: [
          { problem: "Explaining is difficult", change: "Point to two designs and ask, ‘Which bent first?’ or ‘Which held more?’", impact: "Accept a gesture, drawing, or choice as communication.", resume: "Ask them to connect the choice to something seen or counted.", limit: "Do not finish the sentence for the child." },
          { problem: "A child repeats your explanation", change: "Ask, ‘What did you see?’ and offer the option to point to the results.", impact: "Separates verbal memory from the child's own observation.", resume: "Accept a brief answer and move to the next child.", limit: "Do not correct the answer toward a model scientific phrase." }
        ]
      }
    ],
    ratingScale: [
      { value: 1, label: "Not yet", detail: "Could not do it this time" },
      { value: 2, label: "A lot of help", detail: "Needed continuous guidance" },
      { value: 3, label: "Some help", detail: "Did it with reminders" },
      { value: 4, label: "Almost independently", detail: "Needed only one prompt" },
      { value: 5, label: "Independently and safely", detail: "Did it independently" }
    ],
    weeklyActivities: [
      {
        id: "day1", day: "DAY 1", title: "Paper Bridges", duration: 40, color: "var(--yellow)", activityRef: "ACT-0001 · v0.3.0", status: "Draft",
        promise: "Build and compare bridges made from a single sheet of paper to discover how shape can help paper support a load.",
        purpose: "Change the shape of one sheet, run comparable tests, and use observations to improve an idea.",
        primaryArea: "Engineering", secondaryAreas: ["Physics", "Mathematics", "Fine-motor skills", "Communication"], concepts: ["shape", "load", "stiffness", "fair comparison"],
        focus: "One-to-one counting", focusDetail: "Sofi adds one crayon per turn, says one number, and waits before continuing.",
        materials: ["6 identical sheets of paper", "2 hardcover books", "1 paper cup", "20 crayons", "ruler, marker, and hand towel"],
        flow: ["Test the flat sheet and record even a result of 0.", "Sofi imagines and chooses a shape after observing.", "She builds her own bridge using an identical sheet.", "She adds and counts the load one piece at a time.", "She changes one feature and tests again.", "She explains what she made, what happened, and what she would change."],
        closeQuestion: "How independently did she add and count one crayon at a time during her test?",
        safety: "The adult moves the books and centers the cup. No one puts hands or faces under the setup; stop if a support moves, something breaks, or material goes near a mouth.",
        shopping: [
          { key: "copy-paper", name: "Letter or A4 copy paper", qty: 6, unit: "sheet", section: "Stationery", rule: "sum", detail: "All from the same package." },
          { key: "hardcover-books", name: "Similar hardcover books", qty: 2, unit: "book", section: "Home", rule: "max", detail: "Check at home first." },
          { key: "paper-cups", name: "8–12 oz paper cups", qty: 1, unit: "cup", section: "Grocery Store", rule: "sum", detail: "Empty, stable, and undamaged." },
          { key: "crayons", name: "Intact standard crayons", qty: 20, unit: "crayon", section: "Stationery", rule: "max", detail: "Reused on other days." },
          { key: "ruler", name: "12 in / 30 cm ruler", qty: 1, unit: "ruler", section: "Home", rule: "max", detail: "No broken edges." },
          { key: "washable-marker", name: "Washable marker", qty: 1, unit: "marker", section: "Stationery", rule: "max", detail: "Reused during the week." },
          { key: "hand-towel", name: "Hand towel", qty: 1, unit: "towel", section: "Home", rule: "max", detail: "Dry, flat, with no loose cords." },
          { key: "painter-tape", name: "Removable painter's tape", qty: 1, unit: "roll", section: "Stationery", rule: "max", detail: "Optional; also useful on Day 5." }
        ]
      },
      {
        id: "day2", day: "DAY 2", title: "Seed Sorting", duration: 30, color: "var(--cyan)", activityRef: "ACT-0002 · v0.1.1", status: "Draft",
        promise: "Observe the same collection and discover that it can be organized in different ways using clear rules.",
        purpose: "Notice attributes, apply a rule, compare groups, and reorganize the same collection.",
        primaryArea: "Mathematics and data", secondaryAreas: ["Nature", "Language", "Fine-motor skills"], concepts: ["attribute", "category", "rule", "more/less/the same"],
        focus: "Sort using a rule", focusDetail: "Sofi decides where each piece belongs and can explain the rule with words, a gesture, or an example.",
        materials: ["12 chickpeas", "12 black beans", "12 pinto beans", "12 dried green peas", "tray, 5 containers, paper, and marker"],
        flow: ["Observe four different pieces without tasting them.", "Sofi proposes a rule using a visible feature.", "She sorts one piece at a time and uses ‘not sure yet’ when needed.", "Test one uncertain piece and clarify the rule.", "Count and compare the groups.", "Mix them again and create another way to sort."],
        closeQuestion: "How independently did she use a rule to decide where each piece belonged?",
        safety: "These manipulatives are not for eating. Run the activity only with no known or suspected allergy and with continuous supervision. Stop if a piece goes near a mouth, nose, or ear; if ingestion is suspected; or if there is a reaction.",
        shopping: [
          { key: "chickpeas", name: "Sealed dried chickpeas", qty: 1, unit: "small bag", section: "Grocery Store", rule: "sum", detail: "Use 12 pieces; do not return them to the pantry." },
          { key: "black-beans", name: "Sealed dried black beans", qty: 1, unit: "small bag", section: "Grocery Store", rule: "sum", detail: "Use 12 pieces; do not return them to the pantry." },
          { key: "pinto-beans", name: "Sealed dried pinto beans", qty: 1, unit: "small bag", section: "Grocery Store", rule: "sum", detail: "Use 12 pieces; do not return them to the pantry." },
          { key: "green-peas", name: "Sealed dried green peas", qty: 1, unit: "small bag", section: "Grocery Store", rule: "sum", detail: "Use 12 pieces; do not return them to the pantry." },
          { key: "rimmed-tray", name: "Rimmed tray", qty: 1, unit: "tray", section: "Home", rule: "max", detail: "Unbreakable and easy to clean." },
          { key: "small-containers", name: "Small unbreakable containers", qty: 5, unit: "container", section: "Home", rule: "max", detail: "For groups and ‘not sure yet.’" },
          { key: "rigid-container", name: "Rigid container with lid", qty: 1, unit: "container", section: "Home", rule: "max", detail: "Only for activity materials." },
          { key: "washable-marker", name: "Washable marker", qty: 1, unit: "marker", section: "Stationery", rule: "max", detail: "Reuse the one from other days." }
        ]
      },
      {
        id: "day3", day: "DAY 3", title: "Moving Water", duration: 30, color: "var(--mint)", activityRef: "CAND-0001 · v0.0.1", status: "Candidate",
        promise: "Test several tools to discover which one moves more water using the same number of trips.",
        purpose: "Compare volume visibly and improve a procedure without turning it into a race.",
        primaryArea: "Logic and mathematics", secondaryAreas: ["Practical life", "Fine-motor skills", "Engineering"], concepts: ["volume", "absorption", "spill", "fair comparison"],
        focus: "Compare water levels", focusDetail: "Sofi keeps three trips per tool and uses the water marks to choose.",
        materials: ["2 medium plastic containers", "clean sponge", "large spoon", "plastic measuring cup", "water and large towel"],
        flow: ["The adult prepares one container with a small amount of water and one empty container.", "Sofi predicts which tool will leave the highest level.", "She makes three trips with each tool.", "The adult marks the level and resets the same amount.", "Compare the marks and record spills.", "Sofi improves one action and repeats three trips."],
        closeQuestion: "How independently did she compare the levels and use the result to choose a tool?",
        safety: "Dry spills immediately. Do not run, drink the water, bring faces close, or use glass, hot water, soap, or tools that require mouth suction.",
        shopping: [
          { key: "sponge", name: "New sponge with no loose parts", qty: 1, unit: "sponge", section: "Grocery Store", rule: "sum", detail: "No detachable abrasive surface." },
          { key: "medium-bowls", name: "Medium plastic containers", qty: 2, unit: "container", section: "Home", rule: "max", detail: "Unbreakable, 2–4 liters." },
          { key: "large-spoon", name: "Large spoon", qty: 1, unit: "spoon", section: "Home", rule: "max", detail: "No damaged edges." },
          { key: "measuring-cup", name: "Small plastic measuring cup", qty: 1, unit: "cup", section: "Home", rule: "max", detail: "Unbreakable." },
          { key: "large-towel", name: "Large towel", qty: 1, unit: "towel", section: "Home", rule: "max", detail: "Reused on Day 4." }
        ]
      },
      {
        id: "day4", day: "DAY 4", title: "Foil Boat", duration: 35, color: "var(--coral)", activityRef: "CAND-0002 · v0.0.1", status: "Candidate",
        promise: "Design a shape that floats and test how it can distribute a load.",
        purpose: "Connect shape and floating through a first version and one testable improvement.",
        primaryArea: "Engineering", secondaryAreas: ["Physics", "Counting", "Fine-motor skills"], concepts: ["floating", "interior volume", "load", "distribution"],
        focus: "Choose and test an improvement", focusDetail: "Sofi changes one feature of the boat and compares what happened.",
        materials: ["3 aluminum foil squares", "wide container with a little water", "20 craft sticks", "large towel", "paper and crayon"],
        flow: ["Sofi imagines a shape with a dry space for a load.", "She builds a first boat from one foil square.", "She adds one craft stick at a time and counts.", "Record the last stable amount.", "She chooses one change: base, sides, or distribution.", "She builds the second version and compares."],
        closeQuestion: "How independently did she choose an improvement and check what happened?",
        safety: "The adult fills, empties, and moves the container. Stop for a sharp foil edge, water on the floor, or a face near the container. Do not use coins, marbles, glass, or hot water.",
        shopping: [
          { key: "aluminum-foil", name: "Heavy-duty aluminum foil", qty: 1, unit: "roll", section: "Grocery Store", rule: "max", detail: "Enough for three 12 × 12 in / 30 × 30 cm squares." },
          { key: "craft-sticks", name: "Wood craft sticks", qty: 20, unit: "stick", section: "Stationery", rule: "max", detail: "Large, smooth, and splinter-free." },
          { key: "wide-basin", name: "Wide plastic container", qty: 1, unit: "container", section: "Home", rule: "max", detail: "Unbreakable and stable." },
          { key: "large-towel", name: "Large towel", qty: 1, unit: "towel", section: "Home", rule: "max", detail: "Reuse the one from Day 3." },
          { key: "crayons", name: "Intact standard crayons", qty: 1, unit: "crayon", section: "Stationery", rule: "max", detail: "Already included in the Day 1 set." }
        ]
      },
      {
        id: "day5", day: "DAY 5", title: "Cup Tower", duration: 30, color: "var(--yellow)", activityRef: "CAND-0003 · v0.0.1", status: "Candidate",
        promise: "Build, test, and improve a tower while using the same set of pieces every time.",
        purpose: "Observe where a structure loses stability and use that information to change one thing.",
        primaryArea: "Spatial engineering", secondaryAreas: ["Measurement", "Patterns", "Fine-motor skills"], concepts: ["base", "height", "balance", "stability"],
        focus: "Improve stability", focusDetail: "Sofi identifies one change and tests whether the tower stays stable for a count of ten.",
        materials: ["12 identical paper cups", "6 cardstock or thin-cardboard cards", "ruler", "paper and crayon", "optional painter's tape"],
        flow: ["Sofi imagines what a tower needs so it will not fall.", "She chooses a base and a pattern.", "She builds without the adult holding the tower.", "Everyone removes their hands and counts to ten.", "Observe where it began to change.", "Sofi changes one feature and tests again."],
        closeQuestion: "How independently did she identify one change and test whether it made the tower more stable?",
        safety: "Build only within safe reach. Do not climb on furniture, throw pieces, use heavy objects as a load, or fasten the tower with tape.",
        shopping: [
          { key: "paper-cups", name: "8–12 oz paper cups", qty: 12, unit: "cup", section: "Grocery Store", rule: "sum", detail: "Same type as Day 1; quantities are added for the week." },
          { key: "cardstock", name: "Cardstock or thin-cardboard cards", qty: 6, unit: "card", section: "Stationery", rule: "sum", detail: "Identical, with no staples or sharp edges." },
          { key: "ruler", name: "12 in / 30 cm ruler", qty: 1, unit: "ruler", section: "Home", rule: "max", detail: "Reuse the one from Day 1." },
          { key: "painter-tape", name: "Removable painter's tape", qty: 1, unit: "roll", section: "Stationery", rule: "max", detail: "Only to mark the area, not to fasten the tower." },
          { key: "crayons", name: "Intact standard crayons", qty: 1, unit: "crayon", section: "Stationery", rule: "max", detail: "Already included in the Day 1 set." }
        ]
      }
    ],
    shoppingSectionMeta: {
      "Grocery Store": { code: "GROC", note: "Dry foods, household items, and disposables" },
      Stationery: { code: "ART", note: "Stationery and craft supplies" },
      Home: { code: "HOME", note: "Check at home first; buy only if missing" }
    }
  };

  const pairs = [
    ["Simulador móvil", "Mobile prototype"], ["360–430 px · datos sintéticos · ACT-0001 Draft", "360–430 px · synthetic data · ACT-0001 Draft"], ["datos sintéticos", "synthetic data"], ["taller familiar · prototipo", "family workshop · prototype"],
    ["Kids Learning System — Prototipo móvil familiar", "Kids Learning System — Family Mobile Prototype"], ["Simulador móvil del recorrido familiar para preparar, realizar y cerrar una actividad compartida.", "Mobile prototype of the family journey for preparing, doing, and checking out of a shared activity."],
    ["Ir a Hoy", "Go to Today"], ["Ver estado de conexión", "View connection status"], ["En línea", "Online"], ["Sin conexión", "Offline"],
    ["Navegación principal", "Primary navigation"], ["Hoy", "Today"], ["Familia", "Family"], ["Volver", "Back"], ["Cerrar", "Close"],
    ["Domingo · prueba familiar", "Sunday · family trial"], ["Una tarde para", "An afternoon to"], ["pensar", "think"], ["juntos.", "together."],
    ["Elige cuánto tiempo tienen. La actividad se adapta al grupo antes de empezar.", "Choose how much time you have. The activity adapts to the group before you begin."],
    ["El plan está disponible en este dispositivo. Puedes continuar; este prototipo no sincroniza con un servidor.", "The plan is available on this device. You can continue; this prototype does not sync with a server."],
    ["Tiempo disponible", "Time available"], ["incluye cierre", "includes check-out"], ["versión breve", "short version"], ["recomendado", "recommended"], ["con extensión", "with extension"],
    ["¿Quiénes participan?", "Who is participating?"], ["1–4 en producto · 3 en demo", "1–4 in product · 3 in demo"], ["Actividad sugerida", "Suggested activity"],
    ["Vista previa · Draft", "Preview · Draft"], ["Puentes", "Paper"], ["de", ""], ["papel", "Bridges"], ["Puentes de papel", "Paper Bridges"], ["minutos", "minutes"], ["participantes", "participants"], ["riesgo bajo", "low risk"],
    ["Construyan y comparen puentes hechos con una sola hoja para descubrir cómo la forma puede ayudar al papel a resistir una carga.", "Build and compare bridges made from a single sheet of paper to discover how shape can help paper support a load."],
    ["Este prototipo usa una actividad Draft para validar la experiencia. Una familia real solo recibiría contenido publicado.", "This prototype uses a Draft activity to validate the experience. A real family would receive published content only."],
    ["Ver cómo aprenderán", "See how they will learn"], ["Qué van a explorar", "What they will explore"], ["Mapa educativo", "Learning map"],
    ["No es solo construir un puente.", "This is more than building a bridge."], ["Van a cambiar la forma de una hoja, hacer pruebas comparables y usar lo observado para mejorar una idea.", "They will change the shape of one sheet, run comparable tests, and use observations to improve an idea."],
    ["Área principal", "Primary area"], ["Áreas secundarias", "Secondary areas"], ["Ingeniería", "Engineering"], ["Estructuras, diseño e iteración.", "Structures, design, and iteration."],
    ["Física", "Physics"], ["Matemáticas", "Mathematics"], ["Lógica", "Logic"], ["Motricidad", "Fine-motor skills"], ["Comunicación", "Communication"],
    ["Por qué funciona", "Why it works"], ["La forma cambia cómo el papel resiste doblarse. Mantener iguales distancia, vaso, papel y carga permite relacionar el resultado con esa forma.", "Shape changes how paper resists bending. Keeping distance, cup, paper, and load the same lets you connect the result to that shape."],
    ["Estructura", "Structure"], ["Carga", "Load"], ["Rigidez", "Stiffness"], ["Forma", "Shape"], ["Comparación justa", "Fair comparison"],
    ["Decisiones de los niños", "Children's decisions"], ["Cada niño elegirá la forma de su puente; después decidirán juntos qué mejora probar.", "Each child will choose the shape of their bridge; then they will decide together which improvement to test."],
    ["La seguridad y las condiciones de comparación permanecen fijas.", "Safety and comparison conditions remain fixed."], ["Foco sugerido por niño", "Suggested focus for each child"], ["automático y explicable", "automatic and explainable"],
    ["Su aporte", "Their contribution"], ["¿Por qué este foco?", "Why this focus?"], ["También tendrá oportunidades de:", "They will also have opportunities to practice:"], ["Ver preparación", "See preparation"],
    ["Preparación", "Preparation"], ["listos", "ready"], ["5–7 minutos del adulto", "5–7 adult preparation minutes"], ["Reúne y verifica.", "Gather and check."],
    ["Los niños pueden ayudar a contar. El adulto inspecciona materiales y prepara el montaje seguro.", "Children can help count. The adult inspects the materials and prepares the safe setup."],
    ["6 hojas iguales de papel carta o A4", "6 identical sheets of letter or A4 paper"], ["Es el puente cuya forma cambia: 1 referencia plana, 1 por niño, 1 mejora grupal y 1 para plan y resultados.", "The paper is the bridge whose shape changes: 1 flat baseline, 1 per child, 1 group improvement, and 1 for planning and results."],
    ["2 libros de tapa dura, planos y de igual altura", "2 flat hardcover books of equal height"], ["Forman los apoyos del puente a 15 cm; no apilarlos.", "They form the bridge supports 6 in / 15 cm apart; do not stack them."],
    ["1 vaso liviano de papel, 8–12 oz", "1 lightweight 8–12 oz paper cup"], ["Mantiene los crayones reunidos y centrados; debe estar vacío, estable y sin deformaciones.", "It keeps the crayons together and centered; it must be empty, stable, and undamaged."],
    ["20 crayones estándar intactos", "20 intact standard crayons"], ["Son unidades de carga añadidas una a una; mismo tamaño aproximado y sin fragmentos.", "They are units of load added one at a time; use approximately the same size with no fragments."],
    ["1 regla de 30 cm / 12 in", "1 ruler, 12 in / 30 cm"], ["Mantiene la misma distancia entre apoyos; sin bordes rotos.", "It keeps the same distance between supports; no broken edges."],
    ["1 lápiz o marcador lavable", "1 pencil or washable marker"], ["Registra predicciones y resultados sin depender de la memoria.", "It records predictions and results without relying on memory."],
    ["1 toalla de mano seca y plana", "1 dry, flat hand towel"], ["Amortigua la caída y evita que los crayones rueden; nunca toca ni sostiene el puente.", "It cushions a fall and keeps crayons from rolling; it never touches or supports the bridge."],
    ["Mesa firme, seca y despejada", "Firm, dry, clear table"], ["Mantiene el montaje estable, lejos del borde y de zonas de paso.", "It keeps the setup stable, away from the edge and walkways."],
    ["Opcional: 4 trozos de cinta de pintor para marcar la posición exterior de los libros. Nunca fijar el puente.", "Optional: 4 pieces of painter's tape to mark the books' outer positions. Never tape the bridge."],
    ["Prepara el montaje", "Prepare the setup"], ["Solo adulto", "Adult only"], ["Lo que necesitas saber", "What you need to know"], ["guía adulta", "adult guide"], ["Explicación breve", "Short explanation"],
    ["Extiende la toalla en una sola capa bajo el espacio: amortiguará una caída y evitará que los crayones rueden, pero no debe tocar el puente. Coloca los libros completamente planos.", "Spread the towel in one flat layer under the work area: it will cushion a fall and keep crayons from rolling, but it must not touch the bridge. Lay the books completely flat."],
    ["Deja exactamente 15 cm / 6 in entre los bordes interiores. Marca su posición si puedes.", "Leave exactly 6 in / 15 cm between the inner edges. Mark their positions if you can."],
    ["Deja exactamente", "Leave exactly"], ["entre los bordes interiores. Marca su posición si puedes.", "between the inner edges. Mark their positions if you can."],
    ["Comprueba el vaso vacío sobre la mesa: debe permanecer estable durante una cuenta lenta de tres.", "Check the empty cup on the table: it must stay stable for a slow count of three."],
    ["Deja los 20 crayones dentro de tu alcance, lejos del borde. Solo tú moverás los libros.", "Keep all 20 crayons within your reach and away from the edge. Only you will move the books."],
    ["La forma puede hacer al papel más difícil de doblar.", "Shape can make paper harder to bend."], ["Una hoja plana tiene poca altura y se flexiona fácilmente. Los pliegues crean pequeñas paredes. Eso puede aumentar la rigidez, pero no garantiza que una forma siempre gane: por eso se prueba.", "A flat sheet has little height and bends easily. Folds create small walls. That can increase stiffness, but it does not guarantee that one shape will always win—that is why you test."],
    ["Canal", "Channel"], ["Bordes levantados.", "Raised edges."], ["Acordeón", "Accordion"], ["Varios pliegues.", "Several folds."], ["Pliegues anchos", "Wide folds"], ["Pocas crestas.", "A few ridges."], ["Guías rectas", "Straight guides"], ["Ayuda visual.", "Visual guide."],
    ["“No necesitamos saber cuál es mejor. Cada niño elige una forma, mantenemos lo demás igual y dejamos que las pruebas nos den información”.", "‘We do not need to know which one is best. Each child chooses a shape, we keep everything else the same, and we let the tests give us information.’"],
    ["Control del adulto", "Adult control"], ["Tú colocas, mides y reajustas los libros y centras el vaso antes de cada prueba. Los niños añaden los crayones por turnos. Detén la actividad si un soporte se mueve, algo se rompe, se lanza un crayón o un material llega a la boca.", "You place, measure, and reset the books and center the cup before every test. Children add crayons one turn at a time. Stop if a support moves, something breaks, a crayon is thrown, or material goes near a mouth."], ["Empezar actividad", "Start activity"], ["Pausar", "Pause"], ["Modo sin conexión. Las instrucciones, la ayuda y el avance local siguen disponibles.", "Offline mode. Instructions, help, and local progress remain available."],
    ["Etapas de la actividad", "Activity phases"], ["Parten de:", "Starting point:"], ["Practican aquí", "Practice here"], ["Adulto", "Adult"], ["Haz esto", "Do this"], ["Diles", "Say"], ["Durante este paso", "During this step"],
    ["Hoja plana entre dos apoyos con el vaso vacío como resultado cero posible", "Flat sheet between two supports with the empty cup as a possible zero result"],
    ["Tres formas posibles: canal, acordeón y pliegues anchos", "Three possible shapes: channel, accordion, and wide folds"],
    ["Secuencia de plan, plegado y estructura lista", "Sequence from plan to folding to a ready structure"], ["Un turno completo de prueba por niño", "One complete test turn per child"],
    ["Primera versión, una sola mejora y segunda versión", "First version, one improvement, and second version"], ["Explicación conectando lo que se hizo, observó y cambiaría", "Explanation connecting what was made, observed, and would be changed"],
    ["plegar", "fold"], ["listo", "ready"], ["+ una idea", "+ one idea"], ["Hice…", "I made…"], ["Vi…", "I saw…"], ["Cambiaría…", "I would change…"],
    ["Los niños", "Children"], ["Ahora cada uno", "Now each child"], ["Un turno completo a la vez", "One complete turn at a time"], ["Ellos deciden", "They decide"],
    ["Observa sin interrumpir", "Observe without interrupting"], ["Continúa cuando", "Continue when"], ["Así conecta:", "How it connects:"], ["Ayuda con este paso", "Help with this step"], ["Revisar ayuda elegida", "Review selected help"], ["Paso anterior", "Previous step"], ["Cerrar actividad", "Finish activity"],
    ["Cierre rápido", "Quick check-out"], ["Una observación por niño", "One observation per child"], ["Por qué preguntamos", "Why we ask"], ["Objetivo principal de hoy", "Today's primary objective"], ["¿Cuánta ayuda necesitó?", "How much help did they need?"],
    ["No mide inteligencia ni califica al niño. Describe solamente lo que observaste en esta actividad.", "This does not measure intelligence or grade the child. It only describes what you observed during this activity."],
    ["Elige la frase más cercana", "Choose the closest phrase"], ["No se guardará una conclusión", "No conclusion will be saved"], ["Sí pude observar", "I could observe"], ["No pude observar", "I could not observe"],
    ["Observación extra por voz o texto", "Extra observation by voice or text"], ["Editar observación extra", "Edit extra observation"], ["Evaluar más (opcional)", "Evaluate more (optional)"],
    ["Se guardarán la actividad, el foco y la frase elegida. Podrás corregirlos después.", "The activity, focus, and selected phrase will be saved. You can correct them later."], ["Guardar y terminar", "Save and finish"],
    ["Antes de guardar", "Before saving"], ["Puedes corregir cualquier dato", "You can correct any information"], ["Registro contextual", "Contextual record"], ["Esto es lo que aprendimos hoy.", "This is what we learned today."],
    ["Se guarda la actividad, el foco observado y una respuesta contextual. No se crean etiquetas sobre los niños.", "The activity, observed focus, and one contextual response are saved. No labels are created about children."],
    ["Cada participante construyó y probó una estructura; el grupo comparó resultados y probó una mejora.", "Each participant built and tested a structure; the group compared results and tested one improvement."],
    ["Por niño", "For each child"], ["editable", "editable"], ["Observó", "Observed"], ["Sin objetivo evaluado ni exposición inferida.", "No evaluated objective or inferred exposure."], ["El adulto indicó que no pudo observar.", "The adult said they could not observe."], ["Exposiciones:", "Exposures:"],
    ["Observación extra", "Extra observation"], ["Qué hará el sistema", "What the system will do"], ["Usará estas observaciones, junto con evidencia futura, para variar oportunidades. Una sola sesión nunca determina una conclusión fuerte.", "It will use these observations, together with future evidence, to vary opportunities. One session never determines a strong conclusion."], ["Guardar sesión", "Save session"],
    ["Sesión guardada", "Session saved"], ["Listo. Sigan con su tarde.", "Done. Enjoy the rest of your afternoon."], ["El cierre quedó guardado localmente en este dispositivo para el dry run. No se envió a un servidor.", "The check-out was saved locally on this device for the dry run. Nothing was sent to a server."],
    ["Próxima oportunidad", "Next opportunity"], ["La próxima recomendación variará focos y aportes sin convertir una sola observación en una conclusión fuerte.", "The next recommendation will vary focuses and contributions without turning one observation into a strong conclusion."], ["Volver a Hoy", "Return to Today"],
    ["Dry run de fundadora", "Founder dry run"], ["Abre cualquier día o prepara una sola compra para toda la semana.", "Open any day or prepare one shopping list for the entire week."], ["Vista del plan", "Plan view"], ["Actividades", "Activities"], ["Compras", "Shopping"], ["Cinco días con Sofi", "Five days with Sofi"],
    ["Ver compra consolidada", "View combined shopping list"], ["El probador eléctrico permanece fuera de esta semana hasta completar la revisión técnica y seleccionar componentes exactos.", "The electrical tester remains outside this week's plan until the technical review and exact component selection are complete."],
    ["Compra semanal", "Weekly shopping"], ["Los consumibles se suman. Las herramientas reutilizables cuentan una sola vez.", "Consumables are added together. Reusable tools are counted once."], ["SUMA", "ADD"], ["REUSA", "REUSE"],
    ["Probador eléctrico: no comprar todavía", "Electrical tester: do not buy yet"], ["La configuración y los números de parte siguen pendientes del gate técnico.", "The configuration and part numbers are still pending the technical gate."],
    ["Promesa de la actividad", "Activity promise"], ["Propósito educativo", "Learning purpose"], ["Foco sugerido para Sofi", "Suggested focus for Sofi"], ["Materiales", "Materials"], ["para este día", "for this day"], ["Cómo ocurre", "What happens"], ["historia completa", "complete sequence"], ["Una pregunta al cerrar", "One check-out question"], ["Seguridad y detención", "Safety and stopping"],
    ["Aún no es contenido publicado.", "This is not published content yet."], ["Debe convertirse en ActivityVersion y superar revisión antes de publicarse.", "It must become an ActivityVersion and pass review before publication."], ["Preparar actividad", "Prepare activity"], ["Volver al plan", "Return to plan"],
    ["Esta actividad forma parte de un founder pilot controlado. Aún no es contenido publicado.", "This activity is part of a controlled founder pilot. It is not published content yet."],
    ["Esta actividad forma parte de un founder pilot controlado. Debe convertirse en ActivityVersion y superar revisión antes de publicarse.", "This activity is part of a controlled founder pilot. It must become an ActivityVersion and pass review before publication."],
    ["Observaciones, no etiquetas", "Observations, not labels"], ["Una vista del recorrido y de las oportunidades vividas, siempre con contexto.", "A view of the journey and learning opportunities, always with context."], ["Últimas experiencias", "Recent experiences"], ["familia completa", "whole family"], ["Construcción", "Building"], ["Medición", "Measurement"], ["Sofi · Construcción", "Sofi · Building"], ["Mateo · Medición", "Mateo · Measurement"], ["Leo · Comunicación", "Leo · Communication"],
    ["Tuvo oportunidades de plegar, comparar y explicar. Evidencia todavía limitada.", "Had opportunities to fold, compare, and explain. Evidence is still limited."], ["Dos observaciones recientes muestran mayor independencia; no es un diagnóstico.", "Two recent observations show more independence; this is not a diagnosis."], ["Una exposición registrada. Hace falta observar en otros contextos.", "One exposure recorded. More observation in other contexts is needed."], ["Diseño pendiente de validar", "Design pending validation"], ["Esta pantalla prueba cómo comunicar incertidumbre a familias sin convertirla en un tablero de notas.", "This screen tests how to communicate uncertainty to families without turning it into a grade dashboard."],
    ["Cuenta del adulto", "Adult account"], ["Perfiles mínimos para adaptar oportunidades y compartir acceso entre cuidadores.", "Minimal profiles to adapt opportunities and share access among caregivers."], ["Este dispositivo", "This device"], ["La abriste como aplicación", "You opened it as an app"], ["Puedes instalar este piloto", "You can install this pilot"], ["El plan y tu avance operativo quedan disponibles desde este icono.", "Your plan and local progress are available from this icon."], ["Añádelo a la pantalla de inicio para abrirlo sin buscar el enlace.", "Add it to your Home Screen so you can open it without finding the link."], ["Ver instrucciones", "View instructions"], ["Instalar", "Install"], ["Niños", "Children"], ["sin fecha de nacimiento completa", "no full date of birth"], ["Adultos con acceso", "Adults with access"], ["Adulto principal", "Primary adult"], ["Gestiona suscripción, privacidad y permisos.", "Manages subscription, privacy, and permissions."], ["Adulto invitado", "Invited adult"], ["Puede planear y realizar actividades.", "Can plan and run activities."], ["Reiniciar el avance guardado en este dispositivo", "Reset progress saved on this device"],
    ["Instalar en el celular", "Install on your phone"], ["Déjalo como un icono", "Keep it as an icon"], ["Tu avance es local", "Your progress is local"], ["Las compras y el punto de la actividad se conservan en este dispositivo. Este prototipo no crea cuentas ni sincroniza con otro teléfono.", "Shopping and activity progress are kept on this device. This prototype does not create accounts or sync with another phone."],
    ["Entender la actividad", "Understand the activity"], ["Qué aprendizaje sostiene el puente", "What learning the bridge supports"], ["Éxito educativo", "Learning success"], ["Conceptos", "Concepts"], ["Habilidades practicables", "Skills children can practice"], ["Importante", "Important"], ["Entendido", "Got it"],
    ["Cada niño imagina, construye y prueba su propia forma; registra lo ocurrido y recomienda una mejora usando una observación. No importa cuántos crayones sostenga.", "Each child imagines, builds, and tests their own shape, records what happened, and suggests an improvement using an observation. The number of crayons held does not determine success."],
    ["Rigidez a la flexión", "Bending stiffness"], ["Distribución de carga", "Load distribution"], ["Prueba justa", "Fair test"],
    ["Predecir y hacer una pregunta comprobable.", "Predict and ask a testable question."], ["Seguir una secuencia de plegado.", "Follow a folding sequence."], ["Añadir y contar una carga a la vez.", "Add and count one load at a time."], ["Mantener condiciones constantes.", "Keep conditions constant."], ["Comparar resultados usando más, menos o igual.", "Compare results using more, less, or the same."], ["Elegir una mejora y explicar con evidencia.", "Choose an improvement and explain using evidence."],
    ["Una oportunidad de practicar no demuestra capacidad. Solo el foco principal recibe la pregunta final; las demás habilidades se registran como exposición cuando el niño realmente participa.", "One opportunity to practice does not demonstrate ability. Only the primary focus receives a check-out question; other skills are recorded as exposures only when the child actually participates."],
    ["¿Qué está pasando?", "What is happening?"], ["Impacto", "Impact"], ["Reanuda", "Resume"], ["Estas respuestas pertenecen a la versión revisada de la actividad. La IA puede explicarlas, pero no cambiar materiales, carga, distancia ni controles.", "These responses belong to the reviewed activity version. AI may explain them, but it cannot change materials, load, distance, or controls."],
    ["Actividad en pausa", "Activity paused"], ["Tómense el tiempo que necesiten.", "Take all the time you need."], ["Continuar", "Continue"], ["Terminar y cerrar ahora", "Finish and check out now"], ["Salir sin guardar", "Exit without saving"], ["Opcional", "Optional"], ["Guardar observación", "Save observation"],
    ["En el producto real, el adulto podrá dictar, revisar la transcripción y corregirla antes de guardar. Ejemplo: “Cambiaron el diseño cuando vieron que el vaso se inclinaba”.", "In the real product, the adult will be able to dictate, review the transcript, and correct it before saving. Example: ‘They changed the design after seeing that the cup tilted.’"],
    ["Abre este enlace en Safari.", "Open this link in Safari."], ["Toca Compartir.", "Tap Share."], ["Elige “Añadir a pantalla de inicio” y luego “Agregar”.", "Choose ‘Add to Home Screen,’ then ‘Add.’"],
    ["Abre este enlace en Chrome.", "Open this link in Chrome."], ["Toca el menú de tres puntos.", "Tap the three-dot menu."], ["Elige “Agregar a pantalla principal” o “Instalar aplicación”.", "Choose ‘Add to Home screen’ or ‘Install app.’"],
    ["Estado de conexión", "Connection status"], ["Puedes continuar", "You can continue"], ["El contenido está listo", "Content is ready"], ["La aplicación, el plan y el avance local siguen disponibles. No hay sincronización con un servidor en este prototipo.", "The app, plan, and local progress remain available. This prototype does not sync with a server."], ["El dispositivo conservará localmente tus compras y el punto de la actividad.", "The device will keep your shopping and activity progress locally."],
    ["Escala de independencia", "Independence scale"], ["Describe esta ocasión, no al niño.", "Describe this occasion, not the child."], ["Este control está fuera del recorrido que estamos validando.", "This control is outside the flow being validated."],
    ["Flujo opcional documentado; no se abre por defecto.", "The optional flow is documented; it does not open by default."], ["Conexión restaurada.", "Connection restored."], ["Sin conexión: el contenido sigue disponible.", "Offline: content remains available."], ["Aplicación añadida a este celular.", "App added to this phone."]
  ];

  const dictionary = new Map(pairs);
  const text = (value) => {
    if (locale !== "en" || typeof value !== "string") return value;
    if (dictionary.has(value)) return dictionary.get(value);
    return value
      .replace(/^(\d+) de (\d+) listos$/, "$1 of $2 ready")
      .replace(/^(\d+) participantes · (\d+) min$/, "$1 participants · $2 min")
      .replace(/^Sugerido para (.+)$/, "Suggested for $1")
      .replace(/^Independencia observada de (.+)$/, "Observed independence for $1")
      .replace(/^Siguiente: (.+)$/, "Next: $1")
      .replace(/^Apoyo elegido: (.+)$/, "Selected support: $1")
      .replace(/^Apoyo seleccionado\. (.+)$/, "Support selected. $1")
      .replace(/^Reanuda: (.+)$/, "Resume: $1")
      .replace(/^(.+) observó hoy$/, "$1 observed today")
      .replace(/^(.+) · Observó$/, "$1 · Observed")
      .replace(/^Exposiciones: (.+)$/, "Exposures: $1")
      .replace(/^DÍA (\d+)$/, "DAY $1")
      .replace(/ · se reutiliza; compra la cantidad mayor$/, " · reusable; buy the largest required quantity");
  };

  const localizeDom = (root = document) => {
    if (locale !== "en") return;
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach((node) => {
      const original = node.nodeValue;
      const leading = original.match(/^\s*/)?.[0] || "";
      const trailing = original.match(/\s*$/)?.[0] || "";
      const core = original.trim();
      if (core) node.nodeValue = `${leading}${text(core)}${trailing}`;
    });
    root.querySelectorAll?.("[aria-label], [title], [placeholder]").forEach((element) => {
      ["aria-label", "title", "placeholder"].forEach((attribute) => {
        if (element.hasAttribute(attribute)) element.setAttribute(attribute, text(element.getAttribute(attribute)));
      });
    });
  };

  const setLocale = (next) => {
    if (!["es", "en"].includes(next)) return;
    try { localStorage.setItem(localeKey, next); } catch (_) { /* Query parameter remains the fallback. */ }
    const nextUrl = new URL(window.location.href);
    nextUrl.searchParams.set("lang", next);
    window.location.assign(nextUrl.toString());
  };

  document.documentElement.lang = locale === "en" ? "en-US" : "es-US";
  if (locale === "en") {
    document.title = text(document.title);
    const description = document.querySelector('meta[name="description"]');
    if (description) description.content = text(description.content);
  }
  const manifestLink = document.querySelector('link[rel="manifest"]');
  if (manifestLink) manifestLink.href = locale === "en" ? "manifest.en.webmanifest" : "manifest.es.webmanifest";
  window.KidsI18n = { locale, en, text, localizeDom, setLocale, localeKey };
})();
