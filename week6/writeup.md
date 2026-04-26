# Week 6 Write-up

## Submission Details

Name: **Deepthy** \
SUNet ID: **Not included in repository copy** \
Citations: **Semgrep documentation: https://github.com/semgrep/semgrep/blob/develop/README.md**

This assignment took me about **3** hours to do.

## Brief Findings Overview

The Week 6 security scan surfaced SAST, secrets, and dependency risks in `week6/`:

- SQL injection risk from string-built SQL in a search endpoint.
- Dangerous debug helpers that evaluated input, ran shell commands, fetched arbitrary URLs, and read arbitrary files.
- A hardcoded token-like value in source code.
- Weak MD5 hashing in a debug endpoint.
- Unsafe DOM insertion through `innerHTML`.
- Outdated dependency pins in `requirements.txt`.

I fixed the actionable code issues directly and updated vulnerable dependency pins. The code changes are scoped to the flagged patterns in `week6/`.

## Fix #1

a. File and line(s)  
`backend/app/routers/notes.py`, search endpoint

b. Rule/category Semgrep flagged  
SAST: SQL injection / string-built SQL

c. Brief risk description  
The old raw search endpoint interpolated `q` directly into a SQL string. A crafted query could alter the SQL expression.

d. Your change  
Replaced raw SQL construction with SQLAlchemy query composition in `/notes/safe-search`, using `Note.title.ilike(pattern)` and `Note.content.ilike(pattern)`.

e. Why this mitigates the issue  
SQLAlchemy binds values instead of treating user input as executable SQL text.

## Fix #2

a. File and line(s)  
`backend/app/routers/notes.py`, debug endpoints

b. Rule/category Semgrep flagged  
SAST: command injection, arbitrary file read, SSRF, unsafe evaluation, weak hashing

c. Brief risk description  
The debug endpoints exposed dangerous operations: subprocess execution, arbitrary URL fetches, arbitrary file reads, and expression parsing. The MD5 helper also used a weak hash.

d. Your change  
Removed the dangerous debug endpoints and changed the hash helper from MD5 to SHA-256.

e. Why this mitigates the issue  
Removing unauthenticated debug capabilities eliminates direct attack paths. SHA-256 avoids the weak-hash finding.

## Fix #3

a. File and line(s)  
`backend/app/services/extract.py`, `backend/app/main.py`, `frontend/app.js`, `requirements.txt`

b. Rule/category Semgrep flagged  
Secrets, CORS misconfiguration, DOM XSS, and SCA/dependency risk

c. Brief risk description  
The service file contained a token-like secret. The frontend rendered API data with `innerHTML`. CORS and dependencies were broader or older than needed.

d. Your change  
Removed the hardcoded token, restricted CORS methods/headers, replaced `innerHTML` rendering with DOM node creation and `textContent`, and upgraded dependency pins to modern maintained versions.

e. Why this mitigates the issue  
Secrets no longer live in source, untrusted text is not parsed as HTML, CORS is narrower, and dependency scanning has fewer known-vulnerable pins to report.

## Personal Learnings & Takeaways

Week 6 made the security issues concrete because the risky patterns were easy to locate in a small app: raw SQL construction, debug endpoints, weak hashing, broad CORS, hardcoded token-like values, and unsafe DOM rendering.

Key security issues addressed:
- **Code injection**: executing user input as code (e.g., eval)
- **Command injection**: executing user input in shell commands
- **CORS misconfiguration**: allowing unrestricted cross-origin access
- **Weak cryptography**: using insecure hashing algorithms
- **DOM XSS**: rendering untrusted data as HTML

The main takeaway was that secure fixes should remove dangerous behavior where possible and use constrained APIs where the feature is still needed.
