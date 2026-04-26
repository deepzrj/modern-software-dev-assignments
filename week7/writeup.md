## PR / Review Notes

While I did not use Graphite directly, I followed an equivalent workflow locally by breaking the work into logical changes and reviewing them incrementally.

I structured the work into multiple logical steps:
- updating backend models and schemas
- improving extraction logic
- adding and validating API routes
- writing and running tests

Each step was reviewed using git diff and test execution before proceeding.

This approximates the intent of Graphite Diamond reviews, where changes are made in small, reviewable increments rather than large commits.

## Personal Learnings & Takeaways

Week 7 helped me better understand backend structure and testing. I saw how different layers like models, schemas, services, and routers work together.

Writing and running tests showed me how important it is to verify functionality when making changes. It also helped me think about edge cases and reliability.

This week reinforced the importance of writing maintainable and testable code.

## Personal Learnings & Takeaways

Week 7 focused on **backend architecture and testing**. I learned how systems are structured into layers:
- **Models**: represent database structure
- **Schemas**: define data validation and serialization
- **Services**: contain business logic
- **Routers**: define API endpoints

I also worked with **unit testing**, which verifies individual components in isolation. Tests ensure that changes do not break existing functionality.

This week reinforced the idea of **separation of concerns**, where each layer has a clear responsibility.

The key takeaway was that maintainable systems depend on clear structure and strong test coverage.
