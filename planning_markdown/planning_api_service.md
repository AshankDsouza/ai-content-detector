
I want you to make a REST API service. 

✅ Features
Required Features

## Content Submission Endpoint:
 Build an API endpoint that accepts a piece of text-based content (a poem, a short story excerpt, a blog post) for attribution analysis. The endpoint must return a structured response including the attribution result, confidence score, and the transparency label text that would be shown to the user.

For right now, only rely on the models (CNN and random forest).

## Confidence Scoring with Uncertainty:
 Your system must return a confidence score, not just a binary label. The score should reflect genuine uncertainty — a 0.51 confidence should produce a meaningfully different transparency label than a 0.95. Your README must explain how you approached this and how you tested whether your scores are meaningful.

## Rate Limiting:
 Implement rate limiting on your submission endpoint. Your README must document the limits you chose and your reasoning for those specific values.

## Appeals Workflow:
 Implement a mechanism for creators to contest a classification. At minimum, an appeal must: capture the creator's reasoning, log the appeal alongside the original decision, and update the content's status to "under review." Automated re-classification is not required.

## Audit Log: 
Every attribution decision — including confidence score, signals used, and any appeals — must be captured in a structured audit log. Document the log in your README (or via the GET /log output) with at least 3 entries visible.


## Tools and Setup
This project uses a free backend stack — no new accounts required beyond your existing Groq account.

Recommended stack
API framework:	Flask	
Rate limiting:	Flask-Limiter	
Audit log:	SQLite (built-in) or structured JSON
