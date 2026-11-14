# Compliance

## AI Act

The EU AI Act introduces a risk-based framework for AI regulation:

- Unacceptable risk
- High risk
- Limited risk
- Minimal risk

https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai

https://www.europarl.europa.eu/topics/en/article/20230601STO93804/eu-ai-act-first-regulation-on-artificial-intelligence

https://ai-act-service-desk.ec.europa.eu/en/eu-ai-act-compliance-checker


## Data Considerations

To ensure legal clarity and reusability, it is recommended to use only datasets that are explicitly in the public domain, or appropriately licensed for reuse.

Indicative licenses:

- CC0: Public domain dedication; no copyright attribution required.
- MIT: Permissive; retain copyright and license notices.
- Apache 2.0: Permissive; retain required notices and state modifications.

In any and all cases, even when using public domain data, take care to avoid the following risks:

- Intellectual property: Patents, trademarks, and other rights may still apply.
- Privacy: Personal data, images, and recordings may be protected by privacy and publicity laws.
- Legal status: Public domain status may differ across jurisdictions or be incorrectly declared by the dataset provider.

---

You must ensure that no sensitive, confidential, or personally identifiable information is included in the data sent to the LLM (prompts, API calls, etc). 

---

## Platforms' Terms

You must ensure that their use of the LLM aligns with the terms, conditions, and licensing requirements set by the model's provider. This includes adhering to any restrictions on the utilization of the LLMs' output, and guidelines regarding ethical and responsible usage.

- Hugging Face: https://huggingface.co/terms-of-service
- OpenAI: https://openai.com/policies/
- Anthropic: https://www.anthropic.com/legal
- Google Gemini: https://aistudio.google.com/docs/terms

## Ethical AI usage for Developers

Limit LLMs to:

- search and summarize
- explain complex issues
- review, check your solution and find bugs
- check for security vulnerabilities
- adversarial review, what breaks under concurrency/scale/malicious input
- draft documentation
- review architecture

Additionally:

- Never merge code you cannot explain
- Verify outputs with independent tools: linter, static analysis, etc.

Do not use agents to:

- Fully automate the process
- Execute commands, modify code, or perform web actions

Using agents can be risky:

- You may struggle to understand, maintain, or modify agent-generated code.
- Locating and amending relevant code may take longer than rewriting it yourself.
- Agent-generated changes can introduce errors, security risks, and unnecessary complexity.


## End User License Agreement (EULA)

The legal team drafts the End User License Agreement (EULA). As a developer, you must provide the legal team with accurate technical information, e.g.:

1. **Application:** Purpose, functionality, intended users, and deployment environments.
2. **Software Ownership:** Source code, intellectual property, and ownership.
3. **Third-Party Dependencies:** Libraries, models, datasets, APIs, licenses, and provider terms.
4. **Inputs and Outputs:** User inputs, generated outputs, and their intended uses.
5. **Data and Privacy:** Data collection, storage, retention, deletion, third-party sharing, and use for model training.
6. **AI Limitations:** Inaccuracies, hallucinations, bias, and known limitations.
7. **Responsible AI:** Intended use, prohibited uses, human oversight, AI disclosure, and applicable regulatory requirements.
8. **Security:** Authentication, access controls, infrastructure security, and deployment responsibilities.
9. **Service Limitations:** External dependencies, 3rd-party licenses, availability, updates, support, and costs.
10. **User Responsibilities:** Required configurations, acceptable use, and third-party obligations.

The legal team determines the appropriate contractual terms, liability limitations, warranties, consumer protections, and legal compliance requirements.