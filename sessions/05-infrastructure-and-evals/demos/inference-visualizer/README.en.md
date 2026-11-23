# Inference, Memory Hierarchy & KV Cache Simulator

[Back to demos](../README.en.md) | [Türkçe](README.md)

[prefill-decode-kv-sim.html](prefill-decode-kv-sim.html) is a **100% offline**, single-file HTML5/CSS/JS interactive stage simulator built for **Session 05 (Infrastructure, Performance & Evals)**. It uses zero external CDN links and requires no internet connection or local server: open it directly in any modern browser (designed for `800p` and `1080p` projectors) or embed it inside a Google Colab cell via `IPython.display.HTML`. *(The simulator UI uses Turkish labels paired with standard English technical terms.)*

## How to Run

- **Local Browser:** Open [prefill-decode-kv-sim.html](prefill-decode-kv-sim.html) directly in `Chrome`, `Edge`, `Firefox`, or `Safari`.
- **Inside Google Colab:**
  ```python
  from IPython.display import HTML
  HTML(open("prefill-decode-kv-sim.html", encoding="utf-8").read())
  ```

## Simulator Tabs & Features

1. **🏗️ GPU Memory Hierarchy & Cerebras WSE:**
   - Animated pipeline from `HBM/VRAM` → `L2 Cache` → `On-Chip SRAM / FlashAttention` → `Tensor Cores`.
   - Selectable hardware profiles (`Tesla T4`, `RTX PRO 6000 Blackwell / G4`, `H100 SXM`, `H200 SXM`, `NVIDIA B300`, `AMD MI455X`, `Google TPU 8i`, `Huawei Ascend 950DT`, `Apple M5 Ultra`, `DGX Spark GB10`, `AMD Gorgon Halo`, `Cerebras WSE-3`, and `Cerebras WSE-3T / CS-4`), active model footprints, theoretical & ~70% practical decode `tok/s`, and a live **Roofline** gauge (`Memory-Bound` vs `Compute-Bound`).
2. **⚡ Chunked Prefill (`ubatch`) vs Decode (`GEMV`) vs Batching:**
   - Step-by-step `Play / Pause / Step / Reset` animation from `Tokenization` → `Embedding lookup E[ids]` → `Chunked Prefill` (`--ubatch-size` `64..512`, `[B × 3840] × W` GEMM) → `Pure Autoregressive Decode` (`[1 × 3840] × W` GEMV bottleneck) → `Continuous Batching` (`Concurrent Users N` `1..64`).
   - Live `$/1M Token` and `Joule/Token` telemetry readouts as concurrency scales.
3. **🗄️ KV Cache, Prefix Caching & Architectural Compression:**
   - Live KV cache memory calculator across `8K`, `32K`, `128K`, `256K`, and `1M` context lengths comparing **Classic 48L FP16 MHA**, **Gemma 4 12B (FP16 / FP8)**, **Qwen 3.8 27B (`3:1` DeltaNet + Full)**, **DeepSeek-V4-Flash**, and **DeepSeek-V4.1-Flash (`890 B/tok`)**.
   - `Cold Prefill` vs `Warm Prefix Cache` (`cache_prompt=True`) timeline plus an interactive **3-Way Cache Miss Case Study** (`enable_thinking=False` 3-token template shift, `SWA=1024` window boundary, and `--parallel 2` LRU slot routing).
4. **🚀 Pure Decode vs MTP vs DFLASH & 2026 Architectures:**
   - 3-lane lossless verification race controlled by an acceptance-rate (`α`) slider (`Pure Decode`, `MTP` with single-user and continuous-batching toggles, and block-diffusion `DFLASH`).
   - Interactive 2026 Frontier Architectures & Evals Pareto map covering `Gemma 4 12B`, `Gemma 4 26B A4B`, `Qwen 3.8 27B`, `DeepSeek-V4-Flash`, `DeepSeek-V4.1-Flash`, and `Kimi 3.1 Pro`.
5. **🔬 Math & PyTorch Slide-Out Drawer (Header Button):**
   - Hidden by default; displays exact `google/gemma-4-12B-it/config.json` dimensions and a concise `Gemma4MiniModel` PyTorch reference implementation.
