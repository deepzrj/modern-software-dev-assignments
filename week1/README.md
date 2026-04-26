## LLM Prompting Playground

Practice core LLM prompting techniques essential to using and understanding coding LLMs. The full assignment description
is provided at [assignment.md](./assignment.md)

## Personal Learnings & Takeaways

Week 1 was my first exposure to how different prompting techniques affect model behavior. I initially assumed prompting was just about asking questions, but I learned there is a structure to it—like breaking problems into steps (chain-of-thought) or giving examples (few-shot).

One key takeaway was how sensitive the model is to wording. Small changes in prompts can lead to very different outputs. I also realized that working with prompts feels a lot like debugging—you iterate, test, and refine.

This week helped me understand that using LLMs effectively is more about guiding them properly than just writing code.

## Personal Learnings & Takeaways

Week 1 clarified that LLMs behave as probabilistic systems rather than deterministic programs. A probabilistic system generates outputs based on likelihoods learned from data, meaning the same input can produce slightly different outputs depending on context and prompt structure.

I explored different prompting techniques:
- **Zero-shot prompting**: asking a question without examples.
- **Few-shot prompting**: providing examples to guide the model’s output.
- **Chain-of-thought prompting**: explicitly asking the model to reason step-by-step.
- **Self-consistency prompting**: generating multiple reasoning paths and selecting the most consistent answer.

Chain-of-thought improved accuracy by forcing intermediate reasoning steps, while few-shot prompting acted like lightweight “training” within the prompt.

The main takeaway was that prompt design is effectively a form of programming. Instead of writing logic in code, I am encoding logic in instructions and examples.
