# Week 2 — Language and Speech AI

## Objective

This lab explores how to identify appropriate AI capabilities for a
text-processing problem before selecting or implementing an AI service.

The exercise focuses on:

- Entity detection
- Sentiment analysis
- Summarization
- Speech recognition
- Speech synthesis
- Generative AI
- Agentic AI

## Program

`nlp_task_identifier.py` accepts a block of text and identifies AI
workloads that may be appropriate for the supplied information.

The program intentionally does not connect to an AI model or cloud
service.

Its purpose is workload identification rather than production AI
implementation.

## Run the Program

From the repository root:

```powershell
py .\hands-on\week-02-language-and-speech-ai\nlp_task_identifier.py
```

Enter a block of text and press Enter on an empty line to begin the
analysis.

## Traditional NLP vs. Large Language Models

| Task | Traditional NLP | LLM / Generative AI |
|---|---|---|
| Entity detection | Strong fit for consistent structured extraction | Useful for contextual or domain-specific extraction |
| Sentiment analysis | Strong fit for repeatable labels and scores | Useful for nuanced interpretation and explanation |
| Keyword extraction | Strong fit for structured text analytics | Useful when meaning depends heavily on context |
| Summarization | Limited or specialized approaches | Strong fit for natural-language summarization |
| Question answering | Usually requires purpose-built techniques | Strong fit for conversational question answering |
| Content generation | Not the primary purpose | Strong fit |
| Structured classification | Strong fit when categories are known | Useful when categories or instructions are complex |

## Speech AI

Speech AI handles spoken language rather than text alone.

**Speech recognition** converts:

```text
Speech → Text
```

**Speech synthesis** converts:

```text
Text → Speech
```

Once speech has been converted to text, NLP or generative AI can analyze
the resulting text.

## Key Lesson

AI capabilities overlap, but they serve different purposes.

Traditional NLP services are often appropriate when an application needs
predictable, structured analysis.

Large language models are particularly useful when an application needs
generation, summarization, contextual interpretation, or conversational
reasoning.

Agents are different from both. An agent uses AI reasoning to determine
steps and use tools in pursuit of a goal.

This week's exercise recognizes these workloads before introducing cloud 
services later in the project.