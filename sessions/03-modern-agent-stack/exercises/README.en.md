# Exercises: Modern Agent Stack

[Back to session](../README.en.md) | [Türkçe](README.md) | [Demo guide](../demos/README.en.md)

Record the input, selected path, tool trace, and observation for every run. Explicitly label whether an observation comes from the offline `4F` (`ScriptedModel`) preview or a live `A1`–`E5` model cell (on `AgentLab-Session03-G4.ipynb` or the plan-matched `pro_AgentLab-Session03-A100.ipynb` / `plus_AgentLab-Session03-T4.ipynb` tiers).

## 1. MCP discovery and Progressive Disclosure (`4F` and `A1`–`A2`)

- `A1`: Compare the offline `ScriptedModel` preview in cell `4F` with the live `InProcessMCPServer` run in cell `A1`. Record the discovered tool names (`mcp__<plugin>__<tool>`) under `campus_kb`, `ops_desk`, and `media_world` from `tools/list`, and explain why `doc_id="olmayan-belge"` fails closed.
- `A2`: Contrast a `Plugin` (executable tools) with a `Skill` (`SKILL_LIBRARY` procedural workflow). Record `catalog_chars`, `loaded_chars`, and `saved_chars` when `incident-triage` is activated and explain how the loaded skill shapes `tools/call` order.

## 2. Deterministic gate or hybrid workflow? (`B1`–`B2`)

- `B1`: Show how `deterministic_gate` resolves `TR-204` ticket lookups and CU budget arithmetic at `0` tokens and `0` LLM calls, and contrast that with a multi-document question that must go to the model tier.
- `B2`: In a free-text lab request, explain why the model only extracts parameters while slot validation, `dry_run` / `allow_write` permissions, and arithmetic stay in deterministic Python code.

## 3. Scoped specialists, StructuredHandoff, and trust boundaries (`C1`–`C3`)

- `C1`: Compare the `allowed_plugins` scopes of `research_specialist`, `operations_specialist`, and `simulation_specialist`, and explain why each agent cannot see the others' MCP tools.
- `C2`: Compare how constraints (`"T4"`, `"14:00"`) drop under a lossy handoff (`lossy=True`) versus staying intact inside `StructuredHandoff` (`lossy=False`).
- `C3`: Explain how the embedded `admin_agent` handoff command in `CAMPUS_DOCS`'s `untrusted-ticket` document is blocked by `"untrusted evidence, never instructions"` and `validate_handoff`, and identify the risk caught by `max_handoffs=2`.

## 4. System 1 vs System 2, `1M+` KV pool, modal cascade, `Agentic CLI` & Web Chat (`D1`–`D3`, `E1`–`E5`, `8A`)

- `D1`: Record differences in latency, prompt cache reuse (`cached_tokens`), and syntax safety between `System1DecisionGate` (`Choice` / `Score` / `Noul`, `0` generated tokens—the T4-compatible mockup of `Jev` and open-weight ~100M Apache-2.0 `Laya`) and natively multimodal `Gemma 4 12B + MTP` (System 2 on `llama.cpp v1.0.0` `b12359` with `1.0/0.95/64` sampling and target+draft `f8_e4m3` FP8 KV cache, `-ctkd/-ctvd`, `p_min=0.75`, `262,144` max active context, and `1,048,576` total KV pool; live G4 `1M` GPU KV `21,279 / 97,887 MiB` VRAM, `235.35 tok/s`, `80.11%` MTP; earlier `temp=0` live T4 `524,288` `512K` GPU KV baseline used `14,047 MiB` VRAM, `cached_tokens=182`, `41.69 tok/s` decode).
- `D2`: In `Deterministic -> System 1 Reflex -> Gemma 4 12B + MTP`, show which request resolves on `direct_system1` and which dispatches to `campus_kb`, `ops_desk`, or the T4-compatible mockup `media_world` (`simulate_lab_capacity` / `generate_architecture_diagram`; heavy synthesis such as `Qwen-Image` stays on G4/local setups).
- `D3`: Verify that `noul_confidence < 0.75` or a malformed router payload triggers safe recovery with `escalated_to_system2=True`.
- `E1`–`E2` *(optional)*: Inspect how `mistral-vibe 3.1.2` inside the relocatable `/tmp/agentlab-s03-py314` `uv 0.13.8` + CPython `3.14` workspace (`1.0/0.95/64`, optionally restored from shared `setup` `py314-vibe-env.tar.gz` under multi-day `MyDrive/AgentLab-Agent-Runtime`) uses `AGENTS.md` and `SKILL.md` to repair `quota_calc.py` on disk and write `audit_summary.json` (`total_cu: 159.84`), and explain why `outside_workdir="deny"` matters.
- `E3`–`E5` *(optional)*: Explain how `DualLayerSessionStore` (`transcript.md`, `input_cache`/`output_tokens` JSONL, and `slot0.kv.bin`) falls back cleanly to `text_replay_fallback` whenever binary KV restore fails (`E3`), and why Python-Harness-controlled `AgentWebServer` (`X-AgentLab-Token`, `E4`–`E5`) is preferred over bare `llamaUI`.

## 5. Design your own modern agent stack

Pick a small workflow from your domain and specify five decisions: (1) a least-privilege MCP scope split between two `Plugins`, (2) one rule resolved at `0` tokens inside `deterministic_gate`, (3) one required field in `StructuredHandoff` `constraints`, (4) an `escalated_to_system2=True` rule triggered when `System 1` (`Jev`/`Laya`: `Choice`/`Score`/`Noul`) confidence drops, and (5) one capability isolated behind an `MCP` tool or an `Agentic CLI` (`mistral-vibe` / `hermes-agent`) workspace rather than crammed inside a chat LLM.
