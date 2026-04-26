## PR / Review Notes

I structured the work into small, reviewable changes so each task could be checked independently before merging. The local review notes below map to the areas that would be covered in the Graphite PR workflow: scope, implementation diff, tests, and follow-up risks.

Review areas:
- updating backend models and schemas
- improving extraction logic
- adding and validating API routes
- writing and running tests

Manual checks performed:
- inspected the changed routes, schemas, models, and extraction logic with `git diff`
- ran the backend tests after the changes
- checked validation/error behavior for missing notes and unsupported sort fields

Graphite review materials are external to this repository copy; this file records the local review notes and test-focused checks for the submitted code.

## Personal Learnings & Takeaways

Week 7 helped me practice reviewing backend changes by layer. The models define persistence, schemas define request and response validation, services contain extraction logic, and routers expose API behavior.

The most useful review targets were validation and sorting behavior, because small API contract mistakes show up quickly in tests. The main takeaway was that maintainable systems depend on clear separation of concerns and tests that cover edge cases, not just happy paths.
