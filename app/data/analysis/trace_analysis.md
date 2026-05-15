# SHL Trace Analysis

# Common Patterns

## Clarification Patterns
- Ask language/accent for contact-center or spoken-language roles
- Ask backend vs frontend balance for full-stack engineering roles
- Ask selection vs development purpose for leadership hiring
- Ask seniority when assessment depth changes
- Ask whether role is leadership, IC, or tech lead
- Ask candidate language constraints when assessments are language-specific
- Ask whether hiring is high-volume screening or finalist-stage evaluation
- Ask whether personality assessment should remain if candidate wants shorter battery

## Leadership Hiring Patterns
Signals:
- CXO
- director
- executive
- leadership
- senior leadership
- strategic leadership
- leadership benchmark

Common Recommendations:
- Occupational Personality Questionnaire OPQ32r
- OPQ Leadership Report
- OPQ Universal Competency Report 2.0

Behavioral Patterns:
- Clarify whether use case is selection or development
- Leadership hiring strongly prioritizes personality assessments
- Reports are often bundled with OPQ32r
- Leadership conversations are consultative and benchmark-focused

## Technical Hiring Patterns
Signals:
- backend engineer
- full-stack developer
- networking infrastructure
- senior IC
- platform engineer
- software engineer
- architecture
- systems programming

Common Recommendations:
- Smart Interview Live Coding
- Linux Programming
- Networking and Implementation
- Verify G+
- OPQ32r

Behavioral Patterns:
- Admit when exact skill test does not exist
- Recommend closest alternatives instead of failing
- Senior technical roles often include cognitive testing
- Personality testing is included by default unless explicitly rejected
- Technical batteries are usually balanced with technical + cognitive + personality assessments

## Graduate Hiring Patterns
Signals:
- graduate
- trainee
- final-year students
- entry-level analysts
- campus hiring
- no work experience

Common Recommendations:
- Verify G+
- Numerical Reasoning
- Graduate Scenarios
- OPQ32r
- Financial Accounting
- Basic Statistics

Behavioral Patterns:
- Graduate hiring usually combines cognitive + situational judgement + personality
- Numerical reasoning is heavily used for analyst roles
- Graduate Scenarios appears frequently for work-context judgement
- Technical/domain tests are sometimes reserved for shortlisted candidates
- Two-stage screening is commonly recommended

## Contact Center Patterns

## Safety-Critical Hiring Patterns

## Sales Transformation Patterns

## Common Recommendation Bundles
Patterns:
- Technical + Cognitive + Personality
- Simulation + Behavioral + Language
- Cognitive + Situational Judgement + Personality
- Leadership Personality + Leadership Reports
- Safety Personality + Safety Knowledge
- Quick screen first, deep evaluation later

Examples:
- Verify G+ + OPQ32r + technical assessments
- Graduate Scenarios + Numerical Reasoning + OPQ32r
- SVAR + Contact Center Simulation + behavioral assessment
- DSI + Workplace Health and Safety
- OPQ32r + Leadership Report

Important Insights:
- SHL prefers balanced batteries instead of single-test recommendations
- Personality assessments are commonly bundled by default
- Simulations are frequently paired with behavioral or cognitive measures
- Two-stage hiring funnels are repeatedly recommended

## Common Refinement Operations

## Refusal Patterns
Observed Refusals:
- Legal advice
- Employment law interpretation
- HIPAA compliance interpretation
- Regulatory obligation questions

Behavioral Patterns:
- Refuse only the unsafe/legal portion
- Continue helping with assessment selection
- Use partial refusal instead of hard blocking
- Clarify that legal/compliance teams should advise on regulations

Examples:
- "I can help select assessments, but not interpret legal obligations."
- "Whether this satisfies a legal requirement should be discussed with counsel."

## Important Assessment Patterns
OPQ32r:
- Appears across leadership, technical, graduate, admin, and healthcare hiring
- Functions as the default personality assessment
- Often bundled automatically unless user rejects personality testing

Verify G+:
- Commonly added for senior technical, analytical, and graduate roles
- Used to measure reasoning and learning agility
- Frequently paired with technical tests

Graduate Scenarios:
- Frequently used for graduate and trainee hiring
- Adds situational judgement dimension

DSI:
- Strongly associated with safety-critical or trust-sensitive roles
- Often paired with safety knowledge tests

Simulations:
- Frequently used for customer service and admin hiring
- Often paired with behavioral assessments

Leadership Reports:
- Usually layered on top of OPQ32r
- Used heavily for executive and benchmark-based leadership hiring
## Heuristic Ideas

## Future Backend Improvements
High Priority Improvements:

1. Auto-add OPQ32r unless personality testing is explicitly rejected

2. Add Verify G+ heuristics for:
- senior technical roles
- graduate hiring
- analytical roles
- architecture-heavy engineering roles

3. Improve clarification routing:
- language clarification
- frontend/backend clarification
- selection vs development clarification
- high-volume vs finalist-stage clarification

4. Add refinement operations:
- add assessment
- remove assessment
- replace assessment
- shorten battery

5. Add explanation generation:
- explain why assessments are included
- explain tradeoffs between assessments
- explain cognitive vs technical vs personality differences

6. Improve partial refusal behavior:
- refuse legal/compliance interpretation
- continue helping with assessment selection

7. Add duration extraction:
- under 30 mins
- quick screen
- max duration constraints

8. Improve balanced battery generation:
- technical + cognitive + personality
- simulation + behavioral + language

9. Add fallback recommendations when exact assessment does not exist

10. Improve end_of_conversation logic:
- true for confirmations like "confirmed", "thanks", "finalize"