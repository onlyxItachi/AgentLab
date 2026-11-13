# AgentLab

**Language:** [Türkçe](README.md) | English

AgentLab is an educational repository introducing Agentic AI concepts through hands-on sessions, explanations, and interactive Colab notebooks, designed with beginners in mind.

> Lesson notes, glossaries, conceptual exercises, and self-contained Google Colab notebooks for sessions one and two are provided here. Materials for later sessions will be added as they become ready.

## Sessions

1. [LLM Fundamentals](sessions/01-llm-fundamentals/README.en.md)
2. [Agent Architecture, Context and Memory](sessions/02-agent-core-and-state/README.en.md)

## Get started

- [General glossary](docs/en/glossary.md)
- [Session 1 Colab playground](sessions/01-llm-fundamentals/demos/llm-playground/README.en.md)
- [Session 2 G4 Colab demos](sessions/02-agent-core-and-state/demos/README.en.md)

Both sessions run directly in Google Colab without installing Python or setting up a local environment. Session one's [Colab notebook](sessions/01-llm-fundamentals/demos/llm-playground/AgentLab-Colab.ipynb) observes tokens, next-token probabilities, sampling, and tool calling with Qwen3.5-0.8B. Session two's self-contained [G4 Colab notebook](sessions/02-agent-core-and-state/demos/agent-core/AgentLab-Session02-G4.ipynb) pairs a model-free `ScriptedModel` preview with Google's Gemma 4 12B QAT model, matching MTP assistant, and pinned llama.cpp CUDA runtime (262,144 default context capacity) for harness, context, memory, and RAG experiments. Model downloads and VM termination require explicit confirmation in the notebook.
