# AgentLab

**Language:** [Türkçe](README.md) | English

AgentLab is an educational repository introducing Agentic AI concepts through hands-on sessions, explanations, and interactive Colab notebooks, designed with beginners in mind.

> Lesson notes, glossaries, conceptual exercises, and self-contained Google Colab notebooks for sessions one through three are provided here. Materials for later sessions will be added as they become ready.

## Sessions

1. [LLM Fundamentals](sessions/01-llm-fundamentals/README.en.md)
2. [Agent Architecture, Context and Memory](sessions/02-agent-core-and-state/README.en.md)
3. [Modern Agent Stack](sessions/03-modern-agent-stack/README.en.md)

## Get started

- [General glossary](docs/en/glossary.md)
- [Session 1 Colab playground](sessions/01-llm-fundamentals/demos/llm-playground/README.en.md)
- [Session 2 G4 Colab demos](sessions/02-agent-core-and-state/demos/README.en.md)
- [Session 3 G4 Colab demos](sessions/03-modern-agent-stack/demos/README.en.md)

All three sessions run directly in Google Colab without installing Python or setting up a local environment. Session one's [Colab notebook](sessions/01-llm-fundamentals/demos/llm-playground/AgentLab-Colab.ipynb) observes tokens, next-token probabilities, sampling, and tool calling with Qwen3.5-0.8B. Session two's self-contained [G4 Colab notebook](sessions/02-agent-core-and-state/demos/agent-core/AgentLab-Session02-G4.ipynb) pairs a model-free `ScriptedModel` preview with Google's Gemma 4 12B QAT model, matching MTP assistant, and pinned llama.cpp CUDA runtime (262,144 default context capacity) for harness, context, memory, and RAG experiments. Session three's 51-cell self-contained [G4 Colab notebook](sessions/03-modern-agent-stack/demos/modern-agent-stack/AgentLab-Session03-G4.ipynb) (alongside plan-matched `pro_AgentLab-Session03-A100.ipynb` and `plus_AgentLab-Session03-T4.ipynb` notebooks shared via Google Drive during live workshops) begins with a model-free `ScriptedModel` preview (`1A` and `4A`–`4F`) and then runs a single pinned natively multimodal `Gemma 4 12B QAT + MTP` runtime (`GpuMtpRuntime`, ~`7.699 GiB` on **`llama.cpp v1.0.0` (`b12359`)**) with Google's official Gemma 4 sampling (`temperature=1.0`, `top_p=0.95`, `top_k=64`), **`f8_e4m3` FP8 target + draft (`-ctkd/-ctvd`) KV cache**, **`--spec-draft-p-min 0.75`** (`--spec-draft-n-max`: T4 `2`, L4/A100/G4 `3`), active prompt caching (`--cache-ram`, `--ctx-checkpoints 8`, `--cache-reuse 64`, `cache_prompt=True`), a **`1,048,576` (`1M+`) total KV pool**, **`262,144` (`256K`) maximum active inference context**, and a multi-day person-agnostic Google Drive runtime (`1C`/`8C`, `MyDrive/AgentLab-Agent-Runtime` with shared `setup` + per-day `day-03-modern-stack`) (verified live on G4 `RTX PRO 6000 Blackwell` @ `1M` GPU KV at `21,279 / 97,887 MiB` VRAM, **`235.35 tok/s` decode**, and **`80.11%` MTP acceptance**; earlier `b12359` live `Tesla T4` `temp=0` baseline verified GPU-resident **`524,288` (`512K` = `2 × 262,144`)** KV at `14,047 MiB` VRAM / `866 MiB` free headroom, `cached_tokens=182`, `324.07 tok/s` prefill, and **`41.69 tok/s` decode**). It demonstrates `MCP` (`campus_kb`, `ops_desk`, `media_world`), `Skill` progressive disclosure, deterministic gating, multi-agent `StructuredHandoff`, `System 1` decision primitives (`Jev` and open-weight ~100M Apache-2.0 `Laya`: T4-compatible `Choice`/`Score`/`Noul` mockup), `World Model` / `media_world` orchestration, optional **`uv 0.13.8` + isolated CPython `3.14` + `mistral-vibe 3.1.2`** real `Agentic CLI` (`E1`–`E2`), and Python-Harness-controlled Colab Web Chat Frame (`AgentWebServer`) + fallback-aware `DualLayerSessionStore` (`transcript.md`, `input_cache`/`output_tokens` JSONL, `slot0.kv.bin`) (`E3`–`E5`) experiments. Model downloads and VM termination require explicit confirmation in the notebooks.
