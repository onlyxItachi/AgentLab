# AI Hardware, Memory Hierarchy & Software Ecosystem Reference (November 2026)

[Back to session](README.en.md) | [Türkçe](donanim-referansi-2026.md) | [Lesson notes](lesson-notes.md) | [Glossary](glossary.md) | [Interactive Simulator](demos/inference-visualizer/prefill-decode-kv-sim.html)

This student-facing reference consolidates the **Memory Wall**, **on-chip SRAM / HBM / Unified Memory** hierarchy, and **software backend stacks (`CUDA` / `ROCm` / `Metal-MLX` / `JAX-TorchTPU-XLA` / `CANN` / `Cerebras CSL`)** across 12 contemporary AI accelerator and compute families explored in Session 05.

## Methodology & Capacity / Bandwidth Rule

- **Maximum Memory Policy:** On platforms with configurable memory capacities (Apple Silicon, AMD Radeon PRO / Instinct, NVIDIA Spark, AMD Halo/Point, etc.), the **maximum usable memory configuration** is listed.
- **Capacity vs. Bandwidth Invariance:** Increasing RAM capacity on the same memory bus width and SoC/GPU die leaves theoretical memory bandwidth unchanged. Key exceptions are binned lower-core/channel SKUs (e.g., cut-down Apple `M4 Max` / `M5 Max` bins or the `16 GB` entry `M6` at `153 GB/s` vs. `24/32 GB` at `170 GB/s`) and dual-die packages.
- **Theoretical Decode Ceiling Formula:** During single-user (`batch=1`) autoregressive decode, the memory wall ceiling is $\text{Max tok/s} \approx \text{Memory Bandwidth (GB/s)} / \text{Active Weights (GB)}$. The summary table uses **`Gemma 4 12B Q4_0` (`~7.2 GB`)**—the exact model run apples-to-apples across our three Colab tiers—as the baseline (`BW / 7.2`); real-world inference achieves **~60–80%** of this ceiling due to kernel efficiency, KV reads, and MTP/scaling overhead.

---

## Summary Comparison Table (Memory Wall & Theoretical Decode Ceiling)

> Sorted from highest memory bandwidth to lowest. For rack/system products, both **single-chip/accelerator** specs and rack totals are noted.

| # | Platform / Accelerator | Max Memory (Single Unit) | Memory Type | Bandwidth | Theoretical `Gemma 4 12B Q4 (~7.2 GB)` Decode Ceiling | Primary Software Stack |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | **Cerebras WSE-3 Turbo (`CS-4` wafer)** | `44 GB` (on-chip) | On-Chip **SRAM** | **`43.2 PB/s`** | *No SRAM wall* (`~6,000,000`* — fabric/compute latency bound in practice) | Cerebras SDK / CSL, PyTorch |
| 2 | **Cerebras WSE-3 (`CS-3` wafer)** | `44 GB` (on-chip) | On-Chip **SRAM** | **`21.0 PB/s`** | *No SRAM wall* (`~2,916,667`* — fabric/compute latency bound in practice) | Cerebras SDK / CSL, PyTorch |
| 3 | **AMD Instinct MI455X** (`Helios`) | `432 GB` | HBM4 (12-stack) | **`23.3 TB/s`** | `~3,236 tok/s` | ROCm / HIP, PyTorch, vLLM, SGLang |
| 4 | **AMD Instinct MI430X** (HPC/AI) | `432 GB` | HBM4 | **`23.3 TB/s`** | `~3,236 tok/s` | ROCm / HIP, PyTorch, Slurm/HPC |
| 5 | **Google TPU 8i Max** (dual-die) | `384–768 GB` class | HBM | **`17.2 TB/s`** | `~2,389 tok/s` | JAX/XLA, TorchTPU, TPU Sync, vLLM-TPU |
| 6 | **Google TPU 8i** (single-die) | `288 GB` | HBM (+ `384 MB` SRAM) | **`8.60 TB/s`** (`8,601 GB/s`) | `~1,195 tok/s` | JAX/XLA, TorchTPU, TPU Sync, vLLM-TPU |
| 7 | **NVIDIA B300** (`GB300 NVL72`) | `288 GB` | HBM3e (12-Hi) | **`8.00 TB/s`** | `~1,111 tok/s` | CUDA, TensorRT-LLM, vLLM, SGLang |
| 8 | **NVIDIA B200** (`GB200 NVL72`) | `~186 GB` | HBM3e | **`8.00 TB/s`** | `~1,111 tok/s` | CUDA, TensorRT-LLM, vLLM, SGLang |
| 9 | **AMD Instinct MI355X / MI350X** | `288 GB` | HBM3e | **`8.00 TB/s`** | `~1,111 tok/s` | ROCm / HIP, AITER, vLLM, SGLang |
| 10 | **Google TPU 8t / 8tx** | `216 GB` | HBM (+ `128 MB` SRAM) | **`6.53 TB/s`** (`6,528 GB/s`) | `~907 tok/s` | JAX/XLA, TorchTPU, Pathways, TensorFlow |
| 11 | **AMD Instinct MI300X** | `192 GB` | HBM3 | **`5.30 TB/s`** | `~736 tok/s` | ROCm / HIP, PyTorch, vLLM, SGLang |
| 12 | **NVIDIA H200 SXM / NVL** | `141 GB` | HBM3e | **`4.80 TB/s`** | `~667 tok/s` | CUDA, TensorRT-LLM, vLLM, FlashAttention-3 |
| 13 | **AMD Instinct MI350P** (PCIe) | `144 GB` | HBM3e | **`4.00 TB/s`** | `~556 tok/s` | ROCm / HIP, PyTorch, vLLM, SGLang |
| 14 | **Huawei Ascend 950DT** (Decode) | `144 GB` | HiZQ 2.0 HBM | **`4.00 TB/s`** | `~556 tok/s` | CANN, MindSpore, `torch_npu`, MindIE |
| 15 | **NVIDIA H100 NVL** | `94 GB` | HBM3 | **`3.90 TB/s`** | `~542 tok/s` | CUDA, TensorRT-LLM, vLLM, SGLang |
| 16 | **NVIDIA H100 SXM** *(Colab Pro+/G4-tier peer)* | `80 GB` | HBM3 | **`3.35 TB/s`** | `~465 tok/s` | CUDA, TensorRT-LLM, vLLM, FlashAttention-3 |
| 17 | **Huawei Ascend 910C** | `128 GB` | HBM2e / HBM3 | **`3.20 TB/s`** | `~444 tok/s` | CANN, MindSpore, `torch_npu`, vLLM-Ascend |
| 18 | **NVIDIA H100 PCIe** | `80 GB` | HBM2e | **`2.00 TB/s`** | `~278 tok/s` | CUDA, TensorRT-LLM, vLLM, llama.cpp |
| 19 | **NVIDIA RTX PRO 6000 Blackwell** (`G4`) | `96 GB` | GDDR7 ECC | **`1,792 GB/s`** | `~249 tok/s` | CUDA, vLLM, TensorRT-LLM, llama.cpp |
| 20 | **NVIDIA GeForce RTX 5090** | `32 GB` | GDDR7 | **`1,792 GB/s`** | `~249 tok/s` | CUDA, PyTorch, llama.cpp, TensorRT-LLM |
| 21 | **Huawei Ascend 950PR** (Prefill) | `128 GB` | HiBL 1.0 HBM | **`1,600 GB/s`** | `~222 tok/s` | CANN, MindSpore, `torch_npu`, MindIE |
| 22 | **Apple M5 Ultra** (Mac Studio) | `512 GB` | Unified LPDDR5X | **`1,200 GB/s`** (`1.2 TB/s`) | `~167 tok/s` | Metal, MLX, llama.cpp, Core ML, PyTorch (MPS) |
| 23 | **NVIDIA RTX 6000 Ada** / **AMD RX 7900 XTX** | `48 GB` / `24 GB` | GDDR6 | **`960 GB/s`** | `~133 tok/s` | CUDA (`6000 Ada`) / ROCm, Vulkan (`7900 XTX`) |
| 24 | **NVIDIA L40S** / **AMD PRO W7800 (48 GB)** | `48 GB` | GDDR6 | **`864 GB/s`** | `~120 tok/s` | CUDA (`L40S`) / ROCm, Vulkan (`W7800`) |
| 25 | **Apple M3 Ultra** (Mac Studio) | `512 GB` | Unified LPDDR5 | **`819 GB/s`** | `~114 tok/s` | Metal, MLX, llama.cpp, Core ML, PyTorch (MPS) |
| 26 | **AMD Radeon AI PRO R9700** / **RX 9070 XT** | `32 GB` / `16 GB` | GDDR6 | **`640–644.6 GB/s`** | `~89–90 tok/s` | ROCm / HIP, PyTorch, llama.cpp (ROCm/Vulkan) |
| 27 | **Apple M5 Max** (MacBook Pro) | `128 GB` | Unified LPDDR5X | **`614 GB/s`** | `~85 tok/s` | Metal, MLX, llama.cpp, Core ML, PyTorch (MPS) |
| 28 | **Apple M4 Max** (MacBook Pro) | `128 GB` | Unified LPDDR5X | **`546 GB/s`** | `~76 tok/s` | Metal, MLX, llama.cpp, Core ML, PyTorch (MPS) |
| 29 | **Apple M3 Max** (MacBook Pro) | `128 GB` | Unified LPDDR5 | **`400 GB/s`** | `~56 tok/s` | Metal, MLX, llama.cpp, Core ML, PyTorch (MPS) |
| 30 | **NVIDIA Tesla T4** *(Colab baseline)* | `16 GB` (`15 GiB`) | GDDR6 | **`320 GB/s`** | `~44 tok/s` | CUDA, llama.cpp, PyTorch (CUDA) |
| 31 | **NVIDIA RTX Spark (GB10)** / **NVIDIA L4** | `128 GB` / `24 GB` | LPDDR5X / GDDR6 | **`~300 GB/s`** | `~42 tok/s` | Windows Arm64 CUDA / Linux CUDA |
| 32 | **NVIDIA DGX Spark (GB10)** | `128 GB` | Unified LPDDR5X | **`~273 GB/s`** | `~38 tok/s` | DGX OS (Linux), CUDA, NIM, vLLM, llama.cpp |
| 33 | **AMD Gorgon Halo (`Max+ PRO 495`)** | `192 GB` | Unified LPDDR5X-8000 | **`256 GB/s`** | `~36 tok/s` | ROCm / HIP, Vulkan (`llama.cpp`), Ryzen AI |
| 34 | **AMD Strix Halo (`Max+ 395`)** | `128 GB` | Unified LPDDR5X-8000 | **`256 GB/s`** | `~36 tok/s` | ROCm / HIP, Vulkan (`llama.cpp`), Ryzen AI |
| 35 | **Apple M6 Base** (MBP / Air) | `32 GB` | Unified | **`170 GB/s`** | `~24 tok/s` | Metal, MLX, llama.cpp, Core ML, PyTorch (MPS) |
| 36 | **Apple M5 Base** (MBP / Air) | `32 GB` | Unified | **`153 GB/s`** | `~21 tok/s` | Metal, MLX, llama.cpp, Core ML, PyTorch (MPS) |
| 37 | **AMD Gorgon Point (`HX 470`)** | `256 GB` (platform max) | Dual-Ch. LPDDR5X-8533 | **`~136.5 GB/s`** | `~19 tok/s` | ROCm, Vulkan, DirectML/ONNX + Ryzen AI NPU |
| 38 | **AMD Strix Point (`HX 370`)** | `256 GB` (platform max) | Dual-Ch. LPDDR5X-8000 | **`~128 GB/s`** | `~18 tok/s` | ROCm, Vulkan, DirectML/ONNX + Ryzen AI NPU |
| 39 | **Apple M4 Base** (MBP / Air) | `32 GB` | Unified | **`120 GB/s`** | `~17 tok/s` | Metal, MLX, llama.cpp, Core ML, PyTorch (MPS) |

*\*On Cerebras WSE systems, a `7.2 GB` model fits completely inside `44 GB` of on-chip SRAM, eliminating the HBM memory wall; practical token throughput is governed by on-wafer fabric latency and core compute time.*

---

## 1. Cerebras Wafer-Scale Engines (`WSE-3`, `WSE-3 Turbo / CS-4`, and `WSE-4` Status)

In conventional GPUs, model weights live off-die in HBM chips and are streamed through a narrow pin/bus bottleneck at every decode step. Cerebras leaves an entire 300 mm silicon wafer uncut as **one giant chip**, distributing `44 GB` of **on-chip SRAM** directly across `900,000` cores.

| Feature | Cerebras `WSE-3` (`CS-3`) | Cerebras `WSE-3 Turbo / WSE-3T` (`CS-4`) | `WSE-4` Status Note (November 2026) |
| --- | --- | --- | --- |
| **Process & Area** | TSMC 5nm, `46,225 mm²` (single 300 mm wafer) | TSMC 5nm, `46,225 mm²` (single 300 mm wafer) | As of November 2026, official 3nm-class **`WSE-4`** silicon specs have not shipped; the active flagship often informally called "WSE-4" is **`WSE-3 Turbo (WSE-3T)` inside `CS-4`**. |
| **Transistors & Cores** | `4 Trillion` transistors, `900,000` SLAC cores | `4 Trillion` transistors, `900,000` SLAC cores | — |
| **On-Chip SRAM** | **`44 GB`** directly on-wafer | **`44 GB`** directly on-wafer | — |
| **SRAM Bandwidth** | **`21 PB/s`** | **`43.2 PB/s`** (single wafer) | — |
| **On-Wafer Fabric** | `214 Pb/s` (2D mesh) | `53.5 PB/s` / wafer (`3× WSE-3T` CS-4 rack: `160.5 PB/s`) | — |
| **AI Compute** | `125 PFLOPS` (sparse) | **`250 PFLOPS`** / wafer (**`750 PFLOPS`** `3×` CS-4 rack) | — |
| **External Model Memory** | MemoryX (`1.5 TB – 1.2 PB`) | MemoryX + SwarmX rack scaling | — |

- **Live Inference Impact (`GPT-5.6 Sol Ultrafast`):** Running `GPT-5.6 Sol Ultrafast` on Cerebras hardware delivers **~`750 tok/s`** (~`14×` speedup) with exact weight and precision parity—zero distillation or extra shrinkage required.
- **Engineering Trade-off:** Compared to GPU clusters at equal datacenter power and capital budgets, wafer-scale chips offer lower dense matrix compute density (FLOPS/$); therefore GPU/TPU pods remain preferred for massive pre-training, while wafer-scale excels at **ultra-low-latency decode and multi-step agent loops**.
- **Software Stack:** Cerebras SDK / CSL (**Cerebras Software Language**), Cerebras Weight Streaming compiler, **PyTorch** (Cerebras front-end).

---

## 2. NVIDIA Rack-Scale Supercomputers (`GB200 NVL72` & `GB300 NVL72`)

Liquid-cooled rack systems uniting 72 Blackwell / Blackwell Ultra GPUs and 36 Grace CPUs into a **single unified NVLink 5.0 domain** (`130 TB/s` total switch bandwidth) so trillion-parameter MoE models execute like one logical GPU.

| Feature | `NVIDIA GB200 NVL72` (`B200`) | `NVIDIA GB300 NVL72` (`B300 Ultra`) |
| --- | --- | --- |
| **Compute Node** | `72× B200` + `36× Grace CPU` (`2,592` Arm Neoverse V2 cores, `17 TB` LPDDR5X) | `72× B300 Ultra` + `36× Grace CPU` (`2,592` Arm Neoverse V2 cores, `17 TB` LPDDR5X) |
| **HBM3e Memory (GPU / Rack)** | `~186 GB` / GPU (`~13.4 TB` rack) | **`~288 GB`** 12-Hi HBM3e / GPU (**`~20 TB`** rack) |
| **HBM3e Bandwidth** | **`8 TB/s`** / GPU (`~576 TB/s` rack) | **`8 TB/s`** / GPU (`~576 TB/s` rack) |
| **NVLink 5.0 Interconnect** | `130 TB/s` rack aggregate (`1.8 TB/s` / GPU) | `130 TB/s` rack aggregate (`1.8 TB/s` / GPU) |
| **FP4 Tensor Core** | `~720 PFLOPS` (`~10 PFLOPS` / GPU) | **`1,080 PFLOPS` Dense** / **`1,440 PFLOPS` Sparse** (`~15 PFLOPS` dense / GPU) |
| **FP8 Tensor Core (Sparse)** | `720 PFLOPS` | `720 PFLOPS` |
| **FP64 (Scientific HPC)** | `2,880 TFLOPS` (high FP64) | Reduced to `~100 TFLOPS` (*tuned squarely for inference/reasoning*) |

- **Software Stack:** **CUDA**, cuBLAS / CUTLASS / cuDNN, NCCL, NVSHMEM, **TensorRT-LLM**, **vLLM**, **SGLang**, NVIDIA Dynamo, **PyTorch (CUDA)**, **JAX (CUDA)**.

---

## 3. NVIDIA PCIe / Workstation & Datacenter Cards (+ Colab Reference)

Standard single-node server, workstation, and cloud PCIe/SXM accelerators:

| Card / Architecture | Max VRAM & Type | Memory Bandwidth | FP32 (Vector) | Peak AI / Tensor | TDP & Notes |
| --- | --- | --- | --- | --- | --- |
| **`NVIDIA H200 NVL`** (PCIe form) | **`141 GB` HBM3e** | **`4.8 TB/s`** | — | `1,671` dense / `3,341 TFLOPS` sparse (**FP8**) | `600W` (matches SXM HBM3e capacity) |
| **`NVIDIA H200 SXM`** *(reference)* | **`141 GB` HBM3e** | **`4.8 TB/s`** | — | `1,979` dense / `3,958 TFLOPS` sparse (**FP8**) | `700W`, NVLink 4.0 `900 GB/s` |
| **`NVIDIA H100 NVL`** (PCIe/Bridge) | `94 GB` HBM3 / GPU | **`3.9 TB/s`** | — | `1,670` dense / `3,341 TFLOPS` sparse (**FP8**) | `350–400W`, dual-card NVLink bridge |
| **`NVIDIA H100 SXM`** *(Colab Pro+/G4-tier peer)* | `80 GB` HBM3 | **`3.35 TB/s`** | — | `1,979` dense / `3,958 TFLOPS` sparse (**FP8**) | `700W`, NVLink 4.0 `900 GB/s` |
| **`NVIDIA H100 PCIe`** | `80 GB` HBM2e | **`2.0 TB/s`** | — | `1,513` dense / `3,026 TFLOPS` sparse (**FP8**) | `300–350W` |
| **`RTX PRO 6000 Blackwell`** (`G4`) | **`96 GB` GDDR7 ECC** | **`1,792 GB/s`** | `~125 TFLOPS` | `~4,000 TOPS` sparse (**FP4**) | 512-bit bus, GB202 silicon; native NVFP4 |
| **`GeForce RTX 5090`** | `32 GB` GDDR7 (no ECC) | **`1,792 GB/s`** | `~105 TFLOPS` | `~3,352 TOPS` sparse (**FP4**) | 512-bit bus; identical raw bandwidth to `G4` |
| **`RTX 6000 Ada Generation`** | `48 GB` GDDR6 ECC | **`960 GB/s`** | `91.1 TFLOPS` | `~1,457 TOPS` sparse (**FP8**) | `300W`, 384-bit AD102 workstation |
| **`NVIDIA L40S`** | `48 GB` GDDR6 ECC | **`864 GB/s`** | `91.6 TFLOPS` | `1,466 TFLOPS` sparse (**FP8**) | `350W`, datacenter AD102 |
| *Ref: `NVIDIA L4`* | `24 GB` GDDR6 ECC | `300 GB/s` | — | — | Colab Pro/Plus mid tier (`72W`) |
| *Ref: `NVIDIA Tesla T4`* | `16 GB` (`15 GiB`) GDDR6 | `320 GB/s` | — | — | Colab Plus/Free baseline tier (`70W`, SM75) |

- **Software Stack:** **CUDA**, **TensorRT-LLM**, **vLLM**, **SGLang**, **llama.cpp (CUDA)**, **PyTorch (CUDA)**, **JAX (CUDA)**. *(FlashAttention-3 / CUTLASS FP8 & FP4 kernels are pivotal on Hopper and Blackwell.)*

---

## 4. AMD PCIe Cards (`MI350P` & `Radeon AI PRO / RX` Family)

AMD accelerators and workstation GPUs built for standard PCIe server chassis and workstations:

| Card / Architecture | Max VRAM & Type | Memory Bandwidth | FP32 (Vector) | AI / Matrix Compute | Notes |
| --- | --- | --- | --- | --- | --- |
| **`AMD Instinct MI350P`** (CDNA 4 PCIe) | **`144 GB` HBM3e** | **`4.0 TB/s`** | `72 TFLOPS` | **`4,600 TFLOPS`** dense **MXFP4/MXFP6** / `2,300 TFLOPS` dense **FP8** | Datacenter PCIe card; massive FP4 matrix throughput |
| **`AMD Radeon AI PRO R9700`** (RDNA 4) | **`32 GB` GDDR6** | **`640–644.6 GB/s`** | `47.8 TFLOPS` | `383` dense / `766 TFLOPS` sparse **FP8** (`191 / 383` **FP16**) | Local workstation AI GPU |
| **`AMD Radeon PRO W7800`** (RDNA 3) | **`48 GB` GDDR6** *(max config)* | **`864 GB/s`** *(48 GB; `576 GB/s` on 32 GB)* | `~45.2 TFLOPS` | `90.4 TFLOPS` **FP16 Matrix** / `90.4 TOPS` **INT8** | High-capacity workstation model |
| **`AMD Radeon RX 9070 XT`** (RDNA 4) | `16 GB` GDDR6 | **`640–644.6 GB/s`** | `~48.7 TFLOPS` | `389 TFLOPS` dense **FP16** / `1,557 TOPS` sparse **INT4** | Desktop consumer GPU |
| **`AMD Radeon RX 7900 XTX`** (RDNA 3) | `24 GB` GDDR6 | **`960 GB/s`** | `~61.4 TFLOPS` | `123 TFLOPS` **FP16 Matrix** / `123 TOPS` **INT8** | High GDDR6 bandwidth |

- **Software Stack:** **ROCm / HIP**, `rocBLAS` / `hipBLASLt`, RCCL, AITER, **PyTorch (ROCm)**, **vLLM (ROCm)**, **SGLang (ROCm)**, **llama.cpp (ROCm/HIP & Vulkan)**, ONNX Runtime.

---

## 5. Apple Mac Studio Max-Memory Systems (`M5 Ultra`, `M3 Ultra`)

Apple's **Unified Memory** lets CPU and GPU share one giant zero-copy memory pool, enabling hundred-billion-parameter MoE models inside a single Mac Studio enclosure. *(Note: `M4 Ultra` was skipped.)*

| Model | Max Unified Memory | Bandwidth | CPU / GPU / Neural Engine | Architectural Highlight |
| --- | --- | --- | --- | --- |
| **`Apple M5 Ultra`** | **`512 GB`** | **`1,200 GB/s` (`1.2 TB/s`)** | `36-core CPU` / `80-core GPU` / `32-core Neural Engine` | Embedded **Neural Accelerator** inside every GPU core (sharply accelerates prefill matrix math). |
| **`Apple M3 Ultra`** | **`512 GB`** | **`819 GB/s`** | `32-core CPU` / `80-core GPU` / `32-core Neural Engine` | **UltraFusion** dual-die interconnect; introduced the `512 GB` unified ceiling. |

- **Software Stack:** **Metal**, **Apple MLX** (primary unified-memory LLM/MoE framework on Apple Silicon), **llama.cpp (Metal)**, Core ML, **PyTorch (MPS)**.

---

## 6. Apple MacBook Pro Max-Memory Systems (`M5 Max`, `M4 Max`, `M3 Max`)

Full-die *Max* bins unlock the full memory bus, whereas entry cut-down Max bins run at lower memory bandwidth:

| Model | Max Unified Memory | Full-Bin Bandwidth | CPU / GPU / NPU | Cut-Down Bin Bandwidth Note |
| --- | --- | --- | --- | --- |
| **`Apple M5 Max`** | **`128 GB`** | **`614 GB/s`** | `18-core CPU` / `40-core GPU` (+ Neural Accelerators) / `16-core NPU` | Cut-down GPU bin runs at `~460 GB/s` |
| **`Apple M4 Max`** | **`128 GB`** | **`546 GB/s`** (512-bit LPDDR5X) | `16-core CPU` / `40-core GPU` / `16-core NPU` | 14-core CPU / 32-core GPU bin runs at `410 GB/s` |
| **`Apple M3 Max`** | **`128 GB`** | **`400 GB/s`** | `16-core CPU` / `40-core GPU` / `16-core NPU` | 14-core CPU / 30-core GPU bin runs at `300 GB/s` |

- **Software Stack:** **Metal**, **Apple MLX**, **llama.cpp (Metal)**, Core ML, **PyTorch (MPS)**.

---

## 7. Apple Base MacBook Pro & MacBook Air (Max Memory Configuration: `M6`, `M5`, `M4`)

Portable entry (`Base`) chips cap configurable unified memory at **`32 GB`**, comfortably hosting quantized `7B–14B` local agent models.

| Model | Process | Max Unified Memory | Bandwidth | GPU Cores | Architecture / SKU Note |
| --- | --- | --- | --- | --- | --- |
| **`Apple M6` (Base)** | 2nm | **`32 GB`** | **`170 GB/s`** (`24/32 GB`; `16 GB` SKU is `153 GB/s`) | `12-core GPU` (+ Neural Accelerators) | First wave focuses on base/efficiency; `24/32 GB` SKUs raise bus bandwidth. |
| **`Apple M5` (Base)** | 3nm | **`32 GB`** | **`153 GB/s`** | `10-core GPU` (+ Neural Accelerators) | Adds per-GPU-core Neural Accelerators. |
| **`Apple M4` (Base)** | 3nm | **`32 GB`** | **`120 GB/s`** | `10-core GPU` | `120 GB/s` across `16–32 GB`. |

- **Software Stack:** **Metal**, **Apple MLX**, **llama.cpp (Metal)**, Core ML, **PyTorch (MPS)**.

---

## 8. AMD Datacenter Systems (`MI300X`, `MI350X`, `MI355X`, `MI430X`, `MI455X`, and `AMD Helios`)

AMD's CDNA 3 → CDNA 4 → CDNA 5 roadmap pairs expanding HBM capacity and **HBM4** bandwidth with open rack-scale networking (**AMD Helios**).

| Accelerator / System | Architecture | Memory & Type | Bandwidth | Peak Compute & Highlights |
| --- | --- | --- | --- | --- |
| **`AMD Instinct MI300X`** | CDNA 3 (5nm/6nm) | `192 GB` HBM3 | `~5.3 TB/s` | FP8 / FP16 focused (no native FP4) |
| **`AMD Instinct MI350X / MI355X`** | CDNA 4 (3nm/6nm) | `288 GB` HBM3e | `~8.0 TB/s` | **`~10.1 PFLOPS`** MXFP4 sparse (`350X` air / `355X` liquid cooled) |
| **`AMD Instinct MI430X`** | CDNA 5 (2nm/3nm class) | **`432 GB` HBM4** | **`~23.3 TB/s`** | **`288 TFLOPS` FP64** (HPC / Sovereign AI) + **`~9.2 PFLOPS` MXFP4** |
| **`AMD Instinct MI455X`** | CDNA 5 (2nm/3nm) | **`432 GB` HBM4** (12-stack) | **`~23.3 TB/s`** | **`~40.3 PFLOPS` OCP MXFP4** (*Helios flagship AI accelerator*) |
| **`AMD Helios` (Rack System)** | CDNA 5 + EPYC "Venice" (Zen 6) | **`31 TB` HBM4** (`72× MI455X`) | `72 × 23.3 TB/s` | Double-wide liquid-cooled rack; **`2.9 ExaFLOPS` FP4** + Pensando fabric |

- **Software Stack:** **ROCm**, **HIP**, **RCCL**, **AITER**, **Triton (ROCm)**, **PyTorch (ROCm)**, **vLLM (ROCm)**, **SGLang (ROCm)**, **JAX (ROCm)**.

---

## 9. NVIDIA Personal / Developer AI Computers — `GB10` (`DGX Spark` & `RTX Spark`)

Both systems are built around the **NVIDIA GB10 Grace Blackwell Superchip**: `20-core Arm Grace CPU` + `6,144 CUDA cores` + 5th-gen Tensor Cores (`FP4`/`FP8`) sharing one coherent **NVLink-C2C** memory pool (**`1 PFLOPS` FP4 sparse**).

| Feature | `NVIDIA DGX Spark` (`GB10`) | `NVIDIA RTX Spark` (`GB10` / N1X) |
| --- | --- | --- |
| **Form Factor** | Mini desktop developer appliance (ASUS/MSI/Lenovo/PNY, etc.) | Thin laptops and compact Windows PCs |
| **Max Memory & Type** | **`128 GB` Unified LPDDR5X** (`64 GB` OEM option) | **`128 GB` Unified LPDDR5X** |
| **Memory Bandwidth** | **`~273 GB/s`** (*~`215 GB/s` measured*) | **`~273–300 GB/s`** (tuned mobile/PC profiles) |
| **Power (TDP)** | `~140W` SoC / `240W` external brick | `45–100W` dynamic mobile TDP |
| **Networking / Clustering** | **`ConnectX-7 200 Gb/s`** QSFP (2 units cluster to run `405B`) | Standard consumer networking (no `ConnectX-7`) |
| **OS & Software** | **DGX OS (Ubuntu Linux)**, full datacenter **CUDA**, NIM, TensorRT-LLM, vLLM, llama.cpp, PyTorch (CUDA) | **Windows 11 on Arm**, Windows Arm64 **CUDA**, TensorRT, ONNX Runtime, llama.cpp, PyTorch (CUDA) |

---

## 10. AMD Personal AI PCs (`Strix Halo`, `Gorgon Halo`, `Strix Point`, `Gorgon Point`)

Comparing the high-memory **`Halo`** (`256-bit`) workstation/mini-PC line against ultrabook-oriented **`Point`** (`128-bit`) APUs illustrates the **bandwidth vs. capacity wall** cleanly:

| Platform / Processor | Architecture & GPU / NPU | Max Memory | Memory Bus & Bandwidth | Software Stack |
| --- | --- | --- | --- | --- |
| **`Gorgon Halo` (`Ryzen AI Max+ PRO 495`)** | Zen 5 + RDNA 3.5 refresh + XDNA 2 NPU | **`192 GB`** LPDDR5X-8000 | 256-bit → **`256 GB/s`** | **ROCm / HIP**, **Vulkan (`llama.cpp`)**, PyTorch (ROCm), ONNX / Ryzen AI |
| **`Strix Halo` (`Ryzen AI Max+ 395`)** | `16× Zen 5` + Radeon `8060S` (40 CU) + `50 TOPS` NPU | **`128 GB`** LPDDR5X-8000 | 256-bit → **`256 GB/s`** (*~`212–215 GB/s` measured*) | **ROCm / HIP**, **Vulkan (`llama.cpp`)**, PyTorch (ROCm), ONNX / Ryzen AI |
| **`Gorgon Point` (`Ryzen AI 9 HX 470`)** | Zen 5/5c + Radeon `890M` (16 CU, 3100 MHz) + `55 TOPS` NPU (`86` total) | `256 GB` platform max *(LPDDR5X-8533)* | 128-bit → **`~136.5 GB/s`** | **ROCm**, **Vulkan (`llama.cpp`)**, DirectML / ONNX Runtime + AMD Ryzen AI SDK |
| **`Strix Point` (`Ryzen AI 9 HX 370`)** | `12× Zen 5/5c` + Radeon `890M` (16 CU, 2900 MHz) + `50 TOPS` NPU (`~80` total) | `256 GB` platform max *(LPDDR5X-8000)* | 128-bit → **`~128 GB/s`** | **ROCm**, **Vulkan (`llama.cpp`)**, DirectML / ONNX Runtime + AMD Ryzen AI SDK |

---

## 11. Google 8th-Generation TPU Family (`TPU 8t`, `TPU 8tx`, `TPU 8i`, `TPU 8i Max`)

Following 7th-gen **Ironwood (TPU v7x)** (`192 GiB` HBM, `~4,614 TFLOPS` FP8), Google split 8th-gen silicon into **large-scale training (`8t`)** and **low-latency agentic inference (`8i`)**:

| Feature | `TPU 8t` (Training) | `TPU 8tx` (Confidential AI) | `TPU 8i` (Inference / Reasoning) | `TPU 8i Max` (Massive Context) |
| --- | --- | --- | --- | --- |
| **Primary Target** | Massive pre-training, RL, world models | Confidential training, regulated enterprise AI | Multi-turn reasoning & agent serving | Giant KV-cache, long-context agents |
| **Silicon & Host CPU** | Training die + **Google Axion (Arm)** | `8t` die + **5th-Gen AMD EPYC** (`AMD SEV` & PCIe encryption) | Inference die + **Google Axion (Arm)** | **Dual-die (`2× TPU 8i`)** single package |
| **HBM Capacity** | `216 GB` | `216 GB` | `288 GB` | **`384–768 GB`** class |
| **HBM Bandwidth** | **`6.53 TB/s`** (`6,528 GB/s`) | **`6.53 TB/s`** | **`8.60 TB/s`** (`8,601 GB/s`) | **`17.2 TB/s`** |
| **On-Chip SRAM (`Vmem`)** | `128 MB` | `128 MB` | **`384 MB`** (3× expanded) | **`768 MB`** |
| **Peak Compute (FP4)** | **`12.6 PFLOPS`** | `~12.6 PFLOPS` | **`10.1 PFLOPS`** | **`~20.2 PFLOPS`** equiv. |
| **Fabric & Engines** | **Virgo Network** (3D Torus), `19.2 Tbps`, **SparseCore** (`9,600` chips = `2 PB` HBM, `121 EFLOPS`) | Boardfly fabric, hardware root-of-trust | **Boardfly Interconnect**, **Collectives Acceleration Engine (CAE)** (5× lower collective latency) + **LLM Decoder Engine** | Boardfly + CAE + high rack density |

- **Software Stack:** **JAX / XLA / Pallas**, **TorchTPU** (zero-code-change PyTorch support), **TPU Sync** (tiered HBM ↔ Host DRAM ↔ network KV-cache orchestration, up to 90% transfer latency reduction), **Cloud Pathways**, TensorFlow (XLA), **vLLM-TPU**, **SGLang-TPU**.

---

## 12. Huawei Ascend Latest Systems (`910C`, `950PR` / `950DT`, `Atlas 350`, `CloudMatrix`, and `Atlas 950 SuperPoD`)

Like Google's v8 split, Huawei's 4th-gen Da Vinci v5 (`Ascend 950`) separates **Prefill (`950PR`)** and **Decode/Training (`950DT`)** silicon, pairing domestic HBM (`HiBL 1.0`, `HiZQ 2.0`) with rack-wide global memory (**UnifiedBus / UB Link**).

| System / Chip | Architecture / Role | Memory & Domestic HBM | Bandwidth | Compute & Cluster Scale |
| --- | --- | --- | --- | --- |
| **`Ascend 910C`** | Dual-chiplet NPU | `128 GB` HBM2e / HBM3 | **`~3.2 TB/s`** | `~780–800 TFLOPS` FP16/BF16, `~550W` TDP (`CloudMatrix 384`: optical-mesh 384-NPU node) |
| **`Ascend 950PR`** | Da Vinci v5 (**Prefill & RecSys**) | `128 GB` HiBL 1.0 HBM | **`1.6 TB/s`** | `~1 PFLOPS` FP8 (HiF8/MXFP8) / `2 PFLOPS` FP4 (MXFP4) (`Atlas 350` PCIe: `112 GB`, `1.4 TB/s`) |
| **`Ascend 950DT`** | Da Vinci v5 (**Decode & Training**) | **`144 GB` HiZQ 2.0 HBM** | **`4.0 TB/s`** | `~1 PFLOPS` FP8 / `2 PFLOPS` FP4 |
| **`Atlas 950 SuperPoD`** | Rack / SuperNode (`950DT` based) | `1,024+` NPU unified pool | UB Link PB/s-class fabric | Liquid-cooled, UnifiedBus global memory addressing |
| *Roadmap: `Ascend 960` / `970`* | Next-gen Ascend | `960`: `~288 GB` HBM | Scaled | `970`: `4 PFLOPS` FP8 / `8 PFLOPS` FP4 target |

- **Software Stack:** **CANN** (*Compute Architecture for Neural Networks* — CUDA counterpart), **AscendC** (custom kernel language), **MindSpore**, **PyTorch (`torch_npu`)**, **MindIE**, **vLLM-Ascend**, **SGLang-Ascend**.

---

## 13. Software Ecosystem & Backend Mapping Summary

The same high-level model or agent code (e.g., **PyTorch** or **JAX**) maps down onto each accelerator family's compiler, kernel library, and collective communication layer:

| Hardware Family | Low-Level Kernels / Runtime | Primary Training & Research Framework | Production Inference Engines |
| --- | --- | --- | --- |
| **NVIDIA (NVL72, H100/H200, Blackwell, Spark)** | **CUDA**, cuBLAS / CUTLASS / cuDNN, NCCL | **PyTorch (CUDA)**, JAX (CUDA) | TensorRT-LLM, vLLM, SGLang, Dynamo, llama.cpp |
| **AMD (Instinct, Helios, Radeon, Halo/Point)** | **ROCm / HIP**, rocBLAS / hipBLASLt, RCCL, Vulkan | **PyTorch (ROCm)**, JAX (ROCm) | vLLM (ROCm), SGLang (ROCm), AITER, llama.cpp |
| **Apple Silicon (Mac Studio, MBP, Air)** | **Metal**, Apple Neural Engine (ANE) | **MLX**, PyTorch (MPS) | MLX-LM, llama.cpp (Metal), Core ML |
| **Google TPU (v8 Family)** | **XLA**, Pallas, CAE, **TPU Sync** | **JAX**, **TorchTPU (PyTorch)**, TensorFlow | vLLM-TPU, SGLang-TPU, Cloud Pathways |
| **Huawei Ascend (910C, 950PR/DT, Atlas)** | **CANN**, AscendC, HCCL, UB Link | **MindSpore**, **PyTorch (`torch_npu`)** | MindIE, vLLM-Ascend, SGLang-Ascend |
| **Cerebras (WSE-3 / CS-4 WSE-3T)** | **Cerebras SDK / CSL**, Weight Streaming | **PyTorch** (Cerebras front-end) | Cerebras Cloud Inference Server (custom wafer-scale) |
