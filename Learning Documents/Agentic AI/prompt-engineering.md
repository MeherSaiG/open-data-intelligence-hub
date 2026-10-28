# Prompt Engineering

Prompt engineering is the practice of designing, refining, and structuring text inputs to get the most accurate, relevant, and high-quality outputs from generative AI models. Rather than just asking a basic question, it involves systematically guiding the AI to understand exactly what you want and how you want it delivered.

## The Anatomy of a High-Quality Prompt

While simple queries work for basic tasks, a well-engineered prompt typically combines up to four elements:

| Element | Purpose | Example |
|---|---|---|
| **Instruction** | The specific action you want the AI to take. | "Summarize this article..." |
| **Context** | Background information to frame the perspective or tone. | "...for a high school student with no background in biology." |
| **Input Data** | The raw information the AI needs to process. | "[Pasted text of the article]" |
| **Output Indicator** | The required structure, length, or format of the answer. | "Provide 3 bullet points, using no more than 100 words total." |

---

## Core Techniques

Prompt engineering ranges from simple instructions to complex logical frameworks. Here are the foundational techniques:

* **Zero-Shot Prompting:** Asking the AI to perform a task directly without giving it any examples. It relies entirely on the AI's pre-existing knowledge. 
    * *Example:* "Classify the sentiment of this review as Positive, Neutral, or Negative: 'The food was okay, but the service was incredibly slow.'"
* **Few-Shot Prompting:** Providing a few examples of the desired input-output pattern before giving the actual task. This "teaches" the model the exact format or logic you want.
    * *Example:* "Awesome -> Positive. Terrible -> Negative. Okay -> Neutral. Fantastic ->"
* **Chain-of-Thought (CoT):** Asking the model to "think step-by-step" or explicitly outline its reasoning. This drastically improves the AI's accuracy on complex math, logic, or coding problems by forcing it to break the problem down rather than rushing to a final answer.
* **Role-Prompting:** Assigning a specific persona or profession to the AI. This instantly calibrates the vocabulary, depth, and tone of the response.
    * *Example:* "Act as a senior cybersecurity analyst auditing a new network architecture..."
