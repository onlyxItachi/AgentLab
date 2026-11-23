# Session glossary: Infrastructure, Performance & Evals

[Back to session](README.en.md) | [Türkçe](kavram-sozlugu.md) | [2026 Hardware Reference](hardware-reference-2026.md) | [General glossary](../../docs/en/glossary.md)

> **5-minute pre-read before the live workshop:** In Session 05, all three tiers (**`G4 / H100`**, **`L4`**, and **`T4`**) run the exact same **`Gemma 4 12B QAT + MTP`** model apples-to-apples so we can isolate hardware throughput, KV cache footprints, cost/energy economics, tracing spans, and eval quality.

| Term | Meaning in this session and role in the lesson |
| --- | --- |
| `Inference` | Running a trained model's weights to process a prompt (`Prefill`) and generate output tokens (`Decode`) (`5.1`). |
| `Chunked Prefill (GEMM)` | Splitting long prompts into `--ubatch-size` slices (`64..512`) and executing matrix-matrix multiplication (`[B × d] × W`) to populate the KV cache while saturating Tensor Cores (**compute-bound**) (`5.1`, `Deney 1`). |
| `Decode (GEMV & Memory Wall)` | Generating 1 token per step (`[1 × d] × W`), which streams all active weights from HBM/VRAM per step and hits the **Memory Wall** ($\text{Max tok/s} \approx \text{BW} / \text{Active Weights}$) (`5.1`, `Deney 1`). |
| `Roofline Model` | Analytical model distinguishing *memory-bound* kernels (pure decode) from *compute-bound* kernels (prefill and large concurrent batches) (`5.1`). |
| `Continuous Batching` | Iteration-level scheduling that merges concurrent users (`N`) so `[1 × d]` GEMV becomes `[N × d]` GEMM, raising GPU utilization and total `tok/s` (`5.1`, `5.3`). |
| `HBM vs. On-Chip SRAM` | High-capacity off-compute memory (**HBM3/HBM3e/HBM4**: `3.35–23.3 TB/s`) vs. tiny ultra-fast local memory right inside compute cores (**SRAM**: GPU shared memory / TPU `Vmem` / Cerebras `44 GB` wafer SRAM: `43.2 PB/s`) (`5.1`). |
| `Wafer-Scale (WSE-3 / WSE-3T)` | Cerebras's uncut 300 mm wafer chip with `44 GB` **on-chip SRAM** and `900,000` cores; removes the HBM memory wall (`GPT-5.6 Sol Ultrafast ~750 tok/s`) while trading off dense FLOPS/$ density vs. GPU training pods (`5.1`). |
| `Quantization (FP16 / FP8 / NVFP4 / Q4_0)` | Representing weights and KV tensors in 8-bit or 4-bit formats instead of 16-bit to shrink memory-wall traffic and expand context capacity (`5.1`, `5.5`). |
| `TTFT & TPOT` | **Time to First Token (`TTFT`)**: latency from request arrival to first emitted token (ms); **Time Per Output Token (`TPOT`)**: average time between consecutive decode tokens (`ms/tok`, inverse of `tok/s`) (`5.1`, `Deney 1`). |
| `KV Cache` | Stored Key/Value tensors from prefill and prior turns reused during decode; spans `768 KB/tok` (naive 48L FP16 MHA) → `4 KB/tok` (`Gemma 4 12B FP8`) → `890 B/tok` (`DeepSeek-V4.1-Flash`) (`5.2`, `Deney 1`). |
| `GQA & Sliding Window Attention (SWA)` | Sharing fewer KV heads across multiple Q heads (**Grouped-Query Attention**) and keeping only the latest `1024` tokens (`n_swa=1024`) in local layers; `Gemma 4 12B` pairs 40 sliding layers with 8 global (`K=V`) layers (`5.2`). |
| `Prefix Caching (cache_prompt=True)` | Reusing KV blocks across identical prompt prefixes (system instructions, schemas, chat history) to turn `Cold Prefill` into fast `Warm Cache Hits`, backed by `DualLayerSessionStore` (GPU VRAM + host RAM `--cache-ram`) (`5.2`, `Deney 2`). |
| `3-Way Cache Miss (L4 Case Study)` | Combined failure of `(1)` `enable_thinking=False` 3-token template shift, `(2)` `SWA 1024` disabling `--cache-reuse`, and `(3)` `--parallel 2` `slot_prompt_similarity=0.1` + unpinned `id_slot` causing `Cached: 0` (`5.2`). |
| `Speculative Decoding (MTP & DFLASH)` | Generating multiple draft tokens cheaply and verifying them losslessly in one mini-GEMM pass: **MTP** (sequential draft — works in both single-user and multi-user continuous batching) and **DFLASH** (Block Diffusion: 1 parallel forward pass for 8–16 draft tokens, verified in 1 pass) (`5.1`). |
| `MoE (Active vs. Total Params)` | **Mixture of Experts**: stores many total parameters (e.g., `Gemma 4 26B A4B` at `26B` total) while activating only a small subset (`4B` active) per token to keep decode memory traffic low (`5.5`). |
| `CED & CSA2` | **DeepSeek-V4.1-Flash** context and attention compression mechanisms reducing KV footprint to `890 B/tok` (`< 0.9 GB` at `1M` context with FP4 KV) (`5.2`, `5.5`). |
| `$/1M Token & Joule/Token` | AI Factory economics and energy metrics: $\text{Cost/1M} = (\text{Hourly Rate} / (\text{tok/s} \times 3600)) \times 10^6$ and $\text{Joule/Token} = \text{Watt} / \text{tok/s}$ (`T4 ~2.33 J/tok` vs. `G4 8-slot ~0.46 J/tok`) (`5.3`, `Deney 2`). |
| `Observability & Tracing` | Tracking production agent behavior via `/metrics` counters, `timings` telemetry, live `nvidia-smi` `power.draw`, and structured **Span Trees** (`llm_prefill`, `llm_decode`, `tool_exec`) (`5.4`, `Deney 3`). |
| `Evals (Det. / Trajectory / Judge)` | Three-layer evaluation for non-deterministic agents: **Deterministic** (JSON Schema/tool checks), **Trajectory** (step order & tool selection), and **LLM-as-a-Judge** (quality grading, guarding against length/position biases) (`5.5`, `Deney 3`). |
| `Artificial Analysis Pareto` | Comparing models along Intelligence vs. **Price (`$/1M`)**, **Speed (`tok/s`)**, and **Latency (`TTFT`)** Pareto frontiers to match architectures to workload goals (`5.5`). |
| `Code Mode (Programmatic Tool Calling)` | **Extracurricular Bonus:** Instead of injecting huge `MCP` tool catalogs (`~1.17M` tokens) and running `N+1` sequential tool loops, exposes `search()` + `execute()` so the model writes one sandboxed script (Cloudflare V8 Isolates / Anthropic `PTC`) that batches calls and returns only filtered results (`90–99%` fewer tokens). |
