## LLM Prompting Playground

Practice core LLM prompting techniques essential to using and understanding coding LLMs. The full assignment description
is provided at [assignment.md](./assignment.md)

## Personal Learnings & Takeaways

Week 1 was my first exposure to how different prompting techniques affect model behavior. I initially assumed prompting was just about asking questions, but the exercises showed that the prompt structure matters.

The few-shot and chain-of-thought tasks were the most useful comparisons. Few-shot examples helped constrain the output format, while step-by-step reasoning made the model more reliable on tasks that needed intermediate logic. Self-consistency also showed why running several attempts can be useful when the first answer is plausible but not always correct.

I practiced these techniques:
- **Zero-shot prompting**: asking a question without examples.
- **Few-shot prompting**: providing examples to guide the model’s output.
- **Chain-of-thought prompting**: explicitly asking the model to reason step-by-step.
- **Self-consistency prompting**: generating multiple reasoning paths and selecting the most consistent answer.

My main takeaway was that prompt design is an iterative process: define the expected behavior, run the model, inspect failures, and tighten the instructions or examples.
