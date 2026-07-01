
Goal:
Create a Machine Learning model to detect if a text is AI generated or not. The model should output a 1 to 100 score of how ai generated the text given to it is. 0 means text with almost no chance of being ai generated and 100% means almost certainly the text is ai generated text. 


Abstract of the approach to achieving the goal: 
The short abstract of how it works is that we train a model using a dataset of ai vs human generated text using an entire array of text metrics as parameters. 

The implementation is described in the paper ai_generated_mll_predictor.pdf. 

The implementation in the paper uses the following software. Please implement it with this software. And it also uses a kaggle dataset which is obtainable using:

```
import kagglehub

# Download latest version
path = kagglehub.dataset_download("shanegerami/ai-vs-human-text")

print("Path to dataset files:", path)
```



spaCy

spaCy is a library for advanced Natural Language Processing in Python and Cython. It's built on the very latest research, and was designed from day one to be used in real products.
https://github.com/explosion/spaCy


TextDescriptives
A Python library for calculating a large variety of metrics from text(s) using spaCy v.3 pipeline components and extensions.

https://github.com/HLasse/textdescriptives



## Signals
The signals we will use are: stylometric hueristics and ml model predicting. 

### Digital tracing-watermark detection:

This is a detection method which is based on the assumption that ai uses certain unicode/ascii characters that humans would not use due to it being invisble to human being. 

### Classical Classification ML Models:

The ml models are trained on patterns and stylometric scores of ai vs human text. Hence, they measure patterns and stylometric features of text to predict if it is ai generated or not. Two algorithms are used: CNN and decision tree. 

### Stylometric Heuristics:

The stylometric heuristics are features of text that are known to be different between ai and human generated text in terms of uniformity, punctuation density and sentence structure. 


### How the signals are combined:

The main signal will be combined like this:
ML Model score: 0.75 weightage for the CNN's score and 0.25 weigtage for the random forest's score. So, ensemble will be 0.75*CNN + 0.25*RF.

Output: score 0-100 where 0 = certainly human, 100 = certainly AI.
A false positive (labeling a human's work as AI-generated) is worse than a false negative on a writing platform.

Verdict will be a "AI generated" if the final score is 80 and above. If the score is 79 and below it will be marked as "Human generated". If the score is 75 from the classical models and the digital trace comes out as red then we mark the verdict as "AI generated" despite the score being 75. 

The warning section will have the report from the digital trace(if the signal is red) and the stylometric analysis(if the signal is failing). The stylometric analysis will otherwise not show up. 

### Uncertainty:
 We will keep the score as 80+ as the mark or 75+ in addition to red flag from the digital trace. Since false negative is to be avoided as much as possible we are being very conservative where we are 80% sure that it is ai generated text before flagging it. Also, since digital trace/watermarks detection is easily removed we will only use it as an additional confirmation when we are 75+ to 79% sure.

### Transparency labels:

High-confidence AI-generated: whenever the verdict from above is "AI generated". 
High-confidence human-generated: whenever the ensemble score of the classical models are anything below 25 and the signal from the digital trace is green.

Uncertain: whenever it is not High-confidence human-generated and it is not High-confidence AI-generated.

### Response

{
    "result": "passed", // passed or failed
    "score": 2,
    "transparency_label": "High-confidence human-generated",
    "warning_report": {
        "digital_trace_report": "",
        "stylometric_report": ""
    }
}


4pts	planning.md
1	Detection signals are described with explanation of what each measures and how their outputs are combined.
1	Uncertainty representation is addressed — specific thresholds or score ranges are defined, not just "it will show a score."
1	Transparency label variants are written out for at least the high-confidence AI, uncertain, and high-confidence human cases.
1	Appeals workflow and at least two anticipated edge cases are described with enough specificity to be useful pre-work; an ## AI Tool Plan section identifies at least one milestone where AI tools will be used for code generation, specifying what spec sections and diagram will be provided as input.

## AI Tool Plan 

AI tools majorly Claude Code was used for the milestone " Implement the Production Layer".

Since AI is very good for routine work and productionising systems I used it to developed the rate limiter, the audit/logging system and appeal system as well. 

The prompt given as input was:

"Rate Limiting: Implement rate limiting on your submission endpoint. Your README must document the limits you chose and your reasoning for those specific values.


Audit Log: Every attribution decision — including confidence score, signals used, and any appeals — must be captured in a structured audit log. Document the log in your README (or via the GET /log output) with at least 3 entries visible."

It generated the required code without much difficulty. 


## Appeals workflow and edge cases

### Workflow

1. Creator submits `POST /appeal/<submission_id>` with `{"reasoning": "<string>"}` explaining why they believe the verdict is wrong.
2. The submission's `status` flips from `decided` to `under_review` and an `appeals` row is recorded (id, submission_id, appealed_at, creator_reasoning), linked to the original `submissions` row via foreign key.
3. A human reviewer pulls submissions with `status = under_review` (currently visible via `GET /log`'s joined output) and inspects the original text, the ensemble score, the individual CNN/RF scores, and the digital-trace/stylometric warning report.
4. Reviewer records a decision — `upheld` (verdict stands) or `overturned` (verdict flipped) — which moves `status` from `under_review` to `resolved`, and the decision plus reviewer notes are appended to the same appeal row so it is visible in the audit log.
5. The creator is notified of the outcome. If overturned, the transparency label and score shown to the creator are updated to reflect the corrected verdict; the audit log keeps both the original automated decision and the overturned outcome so the trail is never rewritten, only appended to.

This closes the gap in the current implementation, where an appeal is recorded but never resolved (status only ever moves into `under_review`, never out of it).

### Edge cases

- **Duplicate/repeated appeals on the same submission:** A creator resubmits an appeal (or spams the endpoint) while the first is still `under_review`. The endpoint should reject a second appeal on a submission that is already `under_review` (or already `resolved`) with a 409, rather than silently inserting another `appeals` row, so reviewers don't see the same submission duplicated in their queue.
- **Appeal on a submission near the decision boundary (score 75-80):** Because verdicts in this 75-79 band already depend on a secondary signal (digital-trace red flag) rather than the score alone, an appeal here should surface both the classical-model score and the digital-trace report to the reviewer explicitly, since overturning based on score alone would ignore the reason the verdict was flagged in the first place.
- **Appeal after the underlying model/dataset has been updated:** If the model version used to score a submission is later retrained or replaced, an appeal on an old submission should be reviewed against the model version active at the time of the original decision (recorded per-submission), not re-scored with the current model — otherwise "overturned" outcomes become inconsistent across submissions decided under different model versions.
- **High volume of appeals against one transparency label:** If appeals cluster heavily around one label (e.g. many `High-confidence AI-generated` appeals overturned), that is treated as a signal to revisit the 80-point threshold or model calibration rather than as isolated case-by-case errors — recorded as a follow-up in the audit log rather than resolved as a one-off appeal.

