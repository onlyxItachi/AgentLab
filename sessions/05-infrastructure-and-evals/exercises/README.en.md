# Exercises: Infrastructure, Performance & Evals

[Back to session](../README.en.md) | [Türkçe](README.md) | [Demo guide](../demos/README.en.md) | [2026 Hardware Reference](../hardware-reference-2026.md)

For every exercise, record your chosen hardware/architecture parameters alongside observed `TTFT`, `Prefill/Decode tok/s`, `cached_tokens`, `Joule/Token`, and evaluation scores. All exercises run independently after **Cell 1** in `AgentLab-Session05-G4.ipynb` (Ultra/Pro+ G4 or H100), `pro_AgentLab-Session05-L4.ipynb` (Pro/Plus L4), or `plus_AgentLab-Session05-T4.ipynb` (Plus/Free T4), or directly inside the [interactive offline simulator](../demos/inference-visualizer/prefill-decode-kv-sim.html).

## 1. GPU Memory Hierarchy, Roofline & Prefill vs. Decode (`Deney 1` & Simulator — `5.1`)

- **1A (Memory Wall calculation):** Using the [2026 Hardware Reference](../hardware-reference-2026.md), compute the theoretical decode ceiling (`BW / 7.2`) and practical `~70%` range for `Gemma 4 12B Q4_0 (~7.2 GB)` on `Tesla T4` (`320 GB/s`), `RTX PRO 6000 Blackwell` (`1,792 GB/s`), `H100 SXM` (`3.35 TB/s`), and `AMD MI455X` (`23.3 TB/s`); compare with your live `Deney 1` benchmark.
- **1B (`ubatch` GEMM vs. Pure Decode `GEMV` vs. Batching):** In simulator **Tab 2**, adjust `--ubatch-size` and `Concurrent Users N` to record why Tensor Cores sit mostly idle during single-user decode (`GEMV`) and saturate compute (`GEMM`) as `N` scales toward `32/64`.
- **1C (`MTP` vs. `DFLASH` & `WSE-3T`):** In simulator **Tab 4**, sweep acceptance rate (`α`) from `30%` to `80%` to compare `MTP` vs. `DFLASH` (Block Diffusion) speedups, and explain why `Cerebras WSE-3T` (`43.2 PB/s` on-chip SRAM) accelerates `batch=1` decode dramatically while trading off dense-compute density for large pre-training clusters.

## 2. KV Cache Engineering, Prefix Caching & the L4 Cache Miss Case (`Deney 2` & Simulator — `5.2`)

- **2A (`768 KB` vs. `4 KB` vs. `890 B`):** Compute total KV cache size at `256K` (`262,144` tokens) and `1M` (`1,048,576` tokens) for a naive 48L FP16 MHA model (`768 KB/tok`), `Gemma 4 12B FP8` (`4 KB/tok`), and `DeepSeek-V4.1-Flash` (`890 B/tok`), and mark which accelerators can hold each in VRAM.
- **2B (`Cold` vs. `Warm` Prefix Caching):** From `Deney 2`, compare Turn 1 (`Cold`) and Turn 2 (`Warm`) `cached_tokens`, `prompt_ms`, and `TTFT`, and calculate the speedup ratio.
- **2C (Three-way Cache Miss diagnosis):** Explain how each factor in the Session 03 L4 live case study—`(1) enable_thinking=False 3-token shift`, `(2) SWA 1024 disabling --cache-reuse`, and `(3) --parallel 2 slot_prompt_similarity=0.1 + unpinned id_slot`—is resolved (`preserve_thinking=True`, `id_slot=0`, `--swa-full` / `vLLM APC`).

## 3. Cost & AI Factory Energy Economics (`Deney 2` — `5.3`)

- **3A (`Joule/Token` & `$/1M Token`):** From live `nvidia-smi` power (`Watt`) and speed (`tok/s`) in `Deney 2`, compute your GPU's `Joule/Token = Watt / tok_s` and compare against reference baselines (`T4 ~2.33 J/tok` vs. `G4 8-slot MTP5 ~0.46 J/tok`).
- **3B (Batching energy curve):** Summarize in two sentences why increasing `N` from `1` to `16` lowers both `Joule/Token` and `$/1M Token` sharply even though total board power rises slightly.

## 4. Observability & Tracing (`Deney 3` — `5.4`)

- **4A (Span tree breakdown):** Inspect the JSON trace saved by `Deney 3` under `day-05-infra-evals`; sum `llm_prefill`, `llm_decode`, and `tool_exec` durations and compute each phase's percentage of `total_ms`.
- **4B (`/metrics` alert thresholds):** Specify which `/metrics` and `timings` signals you would monitor when KV pool utilization exceeds `90%` or `p95 TTFT` doubles in production.

## 5. Evals, Artificial Analysis & 2026 Frontier Finale (`Deney 3` — `5.5`)

- **5A (3-Layer Eval Design):** From the `Deney 3` Mini Eval Suite output, identify the distinct failure modes caught by deterministic (JSON/tool), trajectory (step order), and `LLM-as-a-Judge` checks, and state one rule to mitigate length/position bias in `LLM-as-a-Judge`.
- **5B (2026 Frontier Selection):** Choose and justify the best fit among `Gemma 4 12B`, `Gemma 4 26B A4B`, `Qwen 3.8 27B`, `DeepSeek-V4-Flash`, `DeepSeek-V4.1-Flash`, and `Kimi 3.1 Pro` for: (i) tightest single-T4 footprint, (ii) `< 1 GB` KV cache at `1M` context, and (iii) active `4B` MoE throughput vs. dense `27B` reasoning quality.

## 6. Design Your Own Inference, Hardware & Eval Budget

Pick a target agent workload and specify a 5-part production budget: (1) model + quantization (`FP8` / `NVFP4` / `Q4_0`), (2) hardware selected via Roofline `BW / active weights` + `ubatch` / batching policy, (3) `KV cache` bytes/token budget + `Prefix Caching` rule, (4) `$/1M Token` and `Joule/Token` targets, and (5) `Observability` spans + 3-tier `Eval` gate. Test your queries in `Canlı Stüdyo` (`Cell 5`) and close cleanly with **Cell 6 (`2. Güvenli Kapanış`)**.
