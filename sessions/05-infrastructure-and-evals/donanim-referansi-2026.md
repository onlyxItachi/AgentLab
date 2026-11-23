# AI Donanım, Bellek Hiyerarşisi ve Yazılım Ekosistemi Referansı (Kasım 2026)

[Oturuma dön](README.md) | [English](hardware-reference-2026.md) | [Ders notları](ders-notlari.md) | [Sözlük](kavram-sozlugu.md) | [Etkileşimli Simülatör](demos/inference-visualizer/prefill-decode-kv-sim.html)

Bu öğrenci referansı; Oturum 05 kapsamında incelediğimiz **bellek duvarı (Memory Wall)**, **on-chip SRAM / HBM / Unified Memory** hiyerarşisi ve **yazılım yığını (`CUDA` / `ROCm` / `Metal-MLX` / `JAX-TorchTPU-XLA` / `CANN` / `Cerebras CSL`)** karşılaştırmalarını 12 güncel hızlandırıcı ve AI bilgisayar ailesi üzerinden tek kaynakta sunar.

## Metodoloji ve Kapasite / Bant Genişliği Kuralı

- **Maksimum Bellek Politikası:** Bellek kapasitesi yapılandırılabilen tüm platformlarda (Apple Silicon, AMD Radeon PRO / Instinct, NVIDIA Spark, AMD Halo/Point vb.) **maksimum kullanılabilir bellek konfigürasyonu** baz alınmıştır.
- **Kapasite vs Bant Genişliği Sabitliği:** Aynı bellek yolu genişliği ve SoC/GPU zarında RAM kapasitesi artsa dahi teorik bant genişliği sabittir. Bilinen başlıca istisnalar, kırpılmış bellek kanallı/GPU çekirdekli alt binler (ör. Apple `M4 Max` / `M5 Max` düşük çekirdekli binler veya `M6` 16 GB giriş sürümünün `153 GB/s` vs `24/32 GB` sürümlerinin `170 GB/s` olması) ve çift zarlı paketlerdir.
- **Teorik Decode Tavanı Hesabı:** Tek kullanıcı (`batch=1`) otoregresif decode sırasında bellek duvarı formülü $\text{Max tok/s} \approx \text{Bellek Bant Genişliği (GB/s)} / \text{Aktif Ağırlık (GB)}$ şeklindedir. Aşağıdaki özet tabloda üç Colab katmanında elma-elma çalıştırdığımız **`Gemma 4 12B Q4_0` (`~7,2 GB`)** için teorik üst sınır (`BW / 7,2`) referans alınmıştır; gerçek çıkarımda çekirdek verimliliği, KV okumaları ve MTP/ölçekleme ek yükü nedeniyle bunun **%60–80'i** gözlenir.

---

## Özet Karşılaştırma Tablosu (Bellek Duvarı & Teorik Decode Tavanı)

> Sıralama en yüksek bellek bant genişliğinden en düşüğe doğrudur. Raf/sistem ürünlerinde **tek çip/hızlandırıcı** değerleri yanında raf toplamı da belirtilmiştir.

| # | Platform / Hızlandırıcı | Maks. Bellek (Tek Birim) | Bellek Tipi | Bant Genişliği | Teorik `Gemma 4 12B Q4 (~7,2 GB)` Decode Tavanı | Birincil Yazılım Yığını |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | **Cerebras WSE-3 Turbo (`CS-4` wafer)** | `44 GB` (on-chip) | On-Chip **SRAM** | **`43,2 PB/s`** | *SRAM duvarı yok* (`~6.000.000`* — pratikte latency/compute sınırlı) | Cerebras SDK / CSL, PyTorch |
| 2 | **Cerebras WSE-3 (`CS-3` wafer)** | `44 GB` (on-chip) | On-Chip **SRAM** | **`21,0 PB/s`** | *SRAM duvarı yok* (`~2.916.667`* — pratikte latency/compute sınırlı) | Cerebras SDK / CSL, PyTorch |
| 3 | **AMD Instinct MI455X** (`Helios`) | `432 GB` | HBM4 (12-stack) | **`23,3 TB/s`** | `~3.236 tok/s` | ROCm / HIP, PyTorch, vLLM, SGLang |
| 4 | **AMD Instinct MI430X** (HPC/AI) | `432 GB` | HBM4 | **`23,3 TB/s`** | `~3.236 tok/s` | ROCm / HIP, PyTorch, Slurm/HPC |
| 5 | **Google TPU 8i Max** (çift zar) | `384–768 GB` sınıfı | HBM | **`17,2 TB/s`** | `~2.389 tok/s` | JAX/XLA, TorchTPU, TPU Sync, vLLM-TPU |
| 6 | **Google TPU 8i** (tek zar) | `288 GB` | HBM (+ `384 MB` SRAM) | **`8,60 TB/s`** (`8.601 GB/s`) | `~1.195 tok/s` | JAX/XLA, TorchTPU, TPU Sync, vLLM-TPU |
| 7 | **NVIDIA B300** (`GB300 NVL72`) | `288 GB` | HBM3e (12-Hi) | **`8,00 TB/s`** | `~1.111 tok/s` | CUDA, TensorRT-LLM, vLLM, SGLang |
| 8 | **NVIDIA B200** (`GB200 NVL72`) | `~186 GB` | HBM3e | **`8,00 TB/s`** | `~1.111 tok/s` | CUDA, TensorRT-LLM, vLLM, SGLang |
| 9 | **AMD Instinct MI355X / MI350X** | `288 GB` | HBM3e | **`8,00 TB/s`** | `~1.111 tok/s` | ROCm / HIP, AITER, vLLM, SGLang |
| 10 | **Google TPU 8t / 8tx** | `216 GB` | HBM (+ `128 MB` SRAM) | **`6,53 TB/s`** (`6.528 GB/s`) | `~907 tok/s` | JAX/XLA, TorchTPU, Pathways, TensorFlow |
| 11 | **AMD Instinct MI300X** | `192 GB` | HBM3 | **`5,30 TB/s`** | `~736 tok/s` | ROCm / HIP, PyTorch, vLLM, SGLang |
| 12 | **NVIDIA H200 SXM / NVL** | `141 GB` | HBM3e | **`4,80 TB/s`** | `~667 tok/s` | CUDA, TensorRT-LLM, vLLM, FlashAttention-3 |
| 13 | **AMD Instinct MI350P** (PCIe) | `144 GB` | HBM3e | **`4,00 TB/s`** | `~556 tok/s` | ROCm / HIP, PyTorch, vLLM, SGLang |
| 14 | **Huawei Ascend 950DT** (Decode) | `144 GB` | HiZQ 2.0 HBM | **`4,00 TB/s`** | `~556 tok/s` | CANN, MindSpore, `torch_npu`, MindIE |
| 15 | **NVIDIA H100 NVL** | `94 GB` | HBM3 | **`3,90 TB/s`** | `~542 tok/s` | CUDA, TensorRT-LLM, vLLM, SGLang |
| 16 | **NVIDIA H100 SXM** *(Colab G4/H100 referansı)* | `80 GB` | HBM3 | **`3,35 TB/s`** | `~465 tok/s` | CUDA, TensorRT-LLM, vLLM, FlashAttention-3 |
| 17 | **Huawei Ascend 910C** | `128 GB` | HBM2e / HBM3 | **`3,20 TB/s`** | `~444 tok/s` | CANN, MindSpore, `torch_npu`, vLLM-Ascend |
| 18 | **NVIDIA H100 PCIe** | `80 GB` | HBM2e | **`2,00 TB/s`** | `~278 tok/s` | CUDA, TensorRT-LLM, vLLM, llama.cpp |
| 19 | **NVIDIA RTX PRO 6000 Blackwell** (`G4`) | `96 GB` | GDDR7 ECC | **`1.792 GB/s`** | `~249 tok/s` | CUDA, vLLM, TensorRT-LLM, llama.cpp |
| 20 | **NVIDIA GeForce RTX 5090** | `32 GB` | GDDR7 | **`1.792 GB/s`** | `~249 tok/s` | CUDA, PyTorch, llama.cpp, TensorRT-LLM |
| 21 | **Huawei Ascend 950PR** (Prefill) | `128 GB` | HiBL 1.0 HBM | **`1.600 GB/s`** | `~222 tok/s` | CANN, MindSpore, `torch_npu`, MindIE |
| 22 | **Apple M5 Ultra** (Mac Studio) | `512 GB` | Unified LPDDR5X | **`1.200 GB/s`** (`1,2 TB/s`) | `~167 tok/s` | Metal, MLX, llama.cpp, Core ML, PyTorch (MPS) |
| 23 | **NVIDIA RTX 6000 Ada** / **AMD RX 7900 XTX** | `48 GB` / `24 GB` | GDDR6 | **`960 GB/s`** | `~133 tok/s` | CUDA (`6000 Ada`) / ROCm, Vulkan (`7900 XTX`) |
| 24 | **NVIDIA L40S** / **AMD PRO W7800 (48 GB)** | `48 GB` | GDDR6 | **`864 GB/s`** | `~120 tok/s` | CUDA (`L40S`) / ROCm, Vulkan (`W7800`) |
| 25 | **Apple M3 Ultra** (Mac Studio) | `512 GB` | Unified LPDDR5 | **`819 GB/s`** | `~114 tok/s` | Metal, MLX, llama.cpp, Core ML, PyTorch (MPS) |
| 26 | **AMD Radeon AI PRO R9700** / **RX 9070 XT** | `32 GB` / `16 GB` | GDDR6 | **`640–644,6 GB/s`** | `~89–90 tok/s` | ROCm / HIP, PyTorch, llama.cpp (ROCm/Vulkan) |
| 27 | **Apple M5 Max** (MacBook Pro) | `128 GB` | Unified LPDDR5X | **`614 GB/s`** | `~85 tok/s` | Metal, MLX, llama.cpp, Core ML, PyTorch (MPS) |
| 28 | **Apple M4 Max** (MacBook Pro) | `128 GB` | Unified LPDDR5X | **`546 GB/s`** | `~76 tok/s` | Metal, MLX, llama.cpp, Core ML, PyTorch (MPS) |
| 29 | **Apple M3 Max** (MacBook Pro) | `128 GB` | Unified LPDDR5 | **`400 GB/s`** | `~56 tok/s` | Metal, MLX, llama.cpp, Core ML, PyTorch (MPS) |
| 30 | **NVIDIA Tesla T4** *(Colab baz referansı)* | `16 GB` (`15 GiB`) | GDDR6 | **`320 GB/s`** | `~44 tok/s` | CUDA, llama.cpp, PyTorch (CUDA) |
| 31 | **NVIDIA RTX Spark (GB10)** / **NVIDIA L4** | `128 GB` / `24 GB` | LPDDR5X / GDDR6 | **`~300 GB/s`** | `~42 tok/s` | Windows Arm64 CUDA / Linux CUDA |
| 32 | **NVIDIA DGX Spark (GB10)** | `128 GB` | Unified LPDDR5X | **`~273 GB/s`** | `~38 tok/s` | DGX OS (Linux), CUDA, NIM, vLLM, llama.cpp |
| 33 | **AMD Gorgon Halo (`Max+ PRO 495`)** | `192 GB` | Unified LPDDR5X-8000 | **`256 GB/s`** | `~36 tok/s` | ROCm / HIP, Vulkan (`llama.cpp`), Ryzen AI |
| 34 | **AMD Strix Halo (`Max+ 395`)** | `128 GB` | Unified LPDDR5X-8000 | **`256 GB/s`** | `~36 tok/s` | ROCm / HIP, Vulkan (`llama.cpp`), Ryzen AI |
| 35 | **Apple M6 Base** (MBP / Air) | `32 GB` | Unified | **`170 GB/s`** | `~24 tok/s` | Metal, MLX, llama.cpp, Core ML, PyTorch (MPS) |
| 36 | **Apple M5 Base** (MBP / Air) | `32 GB` | Unified | **`153 GB/s`** | `~21 tok/s` | Metal, MLX, llama.cpp, Core ML, PyTorch (MPS) |
| 37 | **AMD Gorgon Point (`HX 470`)** | `256 GB` (platform maks.) | Dual-Ch. LPDDR5X-8533 | **`~136,5 GB/s`** | `~19 tok/s` | ROCm, Vulkan, DirectML/ONNX + Ryzen AI NPU |
| 38 | **AMD Strix Point (`HX 370`)** | `256 GB` (platform maks.) | Dual-Ch. LPDDR5X-8000 | **`~128 GB/s`** | `~18 tok/s` | ROCm, Vulkan, DirectML/ONNX + Ryzen AI NPU |
| 39 | **Apple M4 Base** (MBP / Air) | `32 GB` | Unified | **`120 GB/s`** | `~17 tok/s` | Metal, MLX, llama.cpp, Core ML, PyTorch (MPS) |

*\*Cerebras WSE sistemlerinde `7,2 GB` model tamamen `44 GB` on-chip SRAM içine sığdığı için HBM bellek duvarı ortadan kalkar; gerçek token hızı wafer içi ağ (fabric) gecikmesi ve çekirdek hesaplama süresiyle belirlenir.*

---

## 1. Cerebras Wafer-Scale Motorları (`WSE-3`, `WSE-3 Turbo / CS-4` ve `WSE-4` Durumu)

Geleneksel GPU'larda bellek HBM yongalarında (dışarıda) yaşar ve her decode adımında ağırlıklar dar bir kapıdan çekilir. Cerebras, 300 mm silikon plakasını (`wafer`) parçalara kesmek yerine **tek parça dev çip** olarak bırakıp `44 GB` **on-chip SRAM** belleği doğrudan `900.000` çekirdeğin içine dağıtır.

| Özellik | Cerebras `WSE-3` (`CS-3`) | Cerebras `WSE-3 Turbo / WSE-3T` (`CS-4`) | `WSE-4` Durum Notu (Kasım 2026) |
| --- | --- | --- | --- |
| **Üretim & Alan** | TSMC 5nm, `46.225 mm²` (tek 300 mm wafer) | TSMC 5nm, `46.225 mm²` (tek 300 mm wafer) | Kasım 2026 itibarıyla 3nm sınıfı resmi **`WSE-4`** silikon spesifikasyonu henüz piyasaya sürülmedi; piyasada çoğu zaman "WSE-4" diye anılan aktif amiral **`CS-4` içindeki `WSE-3 Turbo (WSE-3T)`**'dir. |
| **Transistör & Çekirdek** | `4 Trilyon` transistör, `900.000` SLAC çekirdeği | `4 Trilyon` transistör, `900.000` SLAC çekirdeği | — |
| **On-Chip SRAM** | **`44 GB`** doğrudan çip üstü SRAM | **`44 GB`** doğrudan çip üstü SRAM | — |
| **SRAM Bant Genişliği** | **`21 PB/s`** | **`43,2 PB/s`** (tek wafer) | — |
| **Wafer İçi Fabric** | `214 Pb/s` (2D mesh) | `53,5 PB/s` / wafer (`3× WSE-3T` CS-4 rafı: `160,5 PB/s`) | — |
| **AI Hesaplama** | `125 PFLOPS` (sparse) | **`250 PFLOPS`** / wafer (**`750 PFLOPS`** `3×` CS-4 rafı) | — |
| **Dış Model Belleği** | MemoryX (`1,5 TB – 1,2 PB`) | MemoryX + SwarmX raf ölçekleme | — |

- **Canlı Çıkarım Etkisi (`GPT-5.6 Sol Ultrafast`):** Cerebras donanımı üzerinde çalışan `GPT-5.6 Sol Ultrafast` modu, damıtma (*distillation*) veya ekstra küçültme olmadan birebir aynı ağırlık ve hassasiyetle saniyede **~`750 tok/s`** (~`14×` hızlanma) üretim hızına ulaşır.
- **Mühendislik Ödünleşimi:** Aynı veri merkezi güç ve maliyet bütçesindeki GPU kümeleriyle karşılaştırıldığında yoğun matris hesaplama (*dense compute* / FLOPS/$) yoğunluğu düşüktür; bu yüzden devasa ön-eğitim (*pre-training*) işlerinde GPU/TPU kümeleri tercih edilirken, wafer-scale mimari **düşük gecikmeli decode ve ajan akışlarında** öne çıkar.
- **Yazılım Yığını:** Cerebras SDK / CSL (**Cerebras Software Language**), Cerebras Weight Streaming derleyicisi, **PyTorch** (Cerebras front-end).

---

## 2. NVIDIA Rack-Scale Süper Bilgisayarları (`GB200 NVL72` ve `GB300 NVL72`)

72 Blackwell / Blackwell Ultra GPU'yu ve 36 Grace CPU'yu tek bir dev **NVLink 5.0** alanına (*single unified NVLink domain*) bağlayan sıvı soğutmalı raf sistemleridir. İletişim katmanında `130 TB/s` toplam raf anahtarlama hızı sunarak Trilyon parametreli MoE modellerini tek büyük mantıksal GPU gibi koşturur.

| Özellik | `NVIDIA GB200 NVL72` (`B200`) | `NVIDIA GB300 NVL72` (`B300 Ultra`) |
| --- | --- | --- |
| **Bilgisayar Düğümü** | `72× B200` + `36× Grace CPU` (`2.592` Arm Neoverse V2 çekirdeği, `17 TB` LPDDR5X) | `72× B300 Ultra` + `36× Grace CPU` (`2.592` Arm Neoverse V2 çekirdeği, `17 TB` LPDDR5X) |
| **HBM3e Bellek (GPU / Raf)** | `~186 GB` / GPU (`~13,4 TB` raf) | **`~288 GB`** 12-Hi HBM3e / GPU (**`~20 TB`** raf) |
| **HBM3e Bant Genişliği** | **`8 TB/s`** / GPU (`~576 TB/s` raf) | **`8 TB/s`** / GPU (`~576 TB/s` raf) |
| **NVLink 5.0 Ara Bağlantı** | `130 TB/s` raf toplamı (`1,8 TB/s` / GPU) | `130 TB/s` raf toplamı (`1,8 TB/s` / GPU) |
| **FP4 Tensor Core** | `~720 PFLOPS` (`~10 PFLOPS` / GPU) | **`1.080 PFLOPS` Dense** / **`1.440 PFLOPS` Sparse** (`~15 PFLOPS` dense / GPU) |
| **FP8 Tensor Core (Sparse)** | `720 PFLOPS` | `720 PFLOPS` |
| **FP64 (Bilimsel HPC)** | `2.880 TFLOPS` (yüksek FP64) | `~100 TFLOPS`'a düşürülmüş (*tam inference/reasoning odaklı*) |

- **Yazılım Yığını:** **CUDA**, cuBLAS / CUTLASS / cuDNN, NCCL, NVSHMEM, **TensorRT-LLM**, **vLLM**, **SGLang**, NVIDIA Dynamo, **PyTorch (CUDA)**, **JAX (CUDA)**.

---

## 3. NVIDIA PCIe / İş İstasyonu ve Veri Merkezi Kartları (+ Colab Referansı)

Tek düğümlü sunucular, iş istasyonları ve bulut PCIe/SXM katmanları için standart referans kartlar:

| Kart / Mimari | Maks. VRAM & Tip | Bellek Bant Genişliği | FP32 (Vektör) | AI / Tensor Tepe Performans | TDP & Notlar |
| --- | --- | --- | --- | --- | --- |
| **`NVIDIA H200 NVL`** (PCIe form) | **`141 GB` HBM3e** | **`4,8 TB/s`** | — | `1.671` dense / `3.341 TFLOPS` sparse (**FP8**) | `600W` (SXM sürümüyle aynı HBM3e kapasitesi) |
| **`NVIDIA H200 SXM`** *(referans)* | **`141 GB` HBM3e** | **`4,8 TB/s`** | — | `1.979` dense / `3.958 TFLOPS` sparse (**FP8**) | `700W`, NVLink 4.0 `900 GB/s` |
| **`NVIDIA H100 NVL`** (PCIe/Köprü) | `94 GB` HBM3 / GPU | **`3,9 TB/s`** | — | `1.670` dense / `3.341 TFLOPS` sparse (**FP8**) | `350–400W`, çift kart NVLink köprü destekli |
| **`NVIDIA H100 SXM`** *(Colab Pro+/G4-eşleniği)* | `80 GB` HBM3 | **`3,35 TB/s`** | — | `1.979` dense / `3.958 TFLOPS` sparse (**FP8**) | `700W`, NVLink 4.0 `900 GB/s` |
| **`NVIDIA H100 PCIe`** | `80 GB` HBM2e | **`2,0 TB/s`** | — | `1.513` dense / `3.026 TFLOPS` sparse (**FP8**) | `300–350W` |
| **`RTX PRO 6000 Blackwell`** (`G4`) | **`96 GB` GDDR7 ECC** | **`1.792 GB/s`** | `~125 TFLOPS` | `~4.000 TOPS` sparse (**FP4**) | 512-bit veri yolu, GB202 silikonu; donanımsal NVFP4 |
| **`GeForce RTX 5090`** | `32 GB` GDDR7 (ECC yok) | **`1.792 GB/s`** | `~105 TFLOPS` | `~3.352 TOPS` sparse (**FP4**) | 512-bit veri yolu; `G4` ile aynı ham bant genişliği |
| **`RTX 6000 Ada Generation`** | `48 GB` GDDR6 ECC | **`960 GB/s`** | `91,1 TFLOPS` | `~1.457 TOPS` sparse (**FP8**) | `300W`, 384-bit AD102 workstation |
| **`NVIDIA L40S`** | `48 GB` GDDR6 ECC | **`864 GB/s`** | `91,6 TFLOPS` | `1.466 TFLOPS` sparse (**FP8**) | `350W`, veri merkezi AD102 |
| *Referans: `NVIDIA L4`* | `24 GB` GDDR6 ECC | `300 GB/s` | — | — | Colab Pro/Plus orta katman (`72W`) |
| *Referans: `NVIDIA Tesla T4`* | `16 GB` (`15 GiB`) GDDR6 | `320 GB/s` | — | — | Colab Plus/Ücretsiz baz katman (`70W`, SM75) |

- **Yazılım Yığını:** **CUDA**, **TensorRT-LLM**, **vLLM**, **SGLang**, **llama.cpp (CUDA)**, **PyTorch (CUDA)**, **JAX (CUDA)**. *(Blackwell ve Hopper kartlarda FlashAttention-3 / CUTLASS FP8 & FP4 çekirdekleri kritiktir.)*

---

## 4. AMD PCIe Kartları (`MI350P` & `Radeon AI PRO / RX` Ailesi)

İş istasyonu ve standart PCIe sunucu kasalarına giren AMD hızlandırıcı ve ekran kartları:

| Kart / Mimari | Maks. VRAM & Tip | Bellek Bant Genişliği | FP32 (Vektör) | AI / Matrix Performansı | Notlar |
| --- | --- | --- | --- | --- | --- |
| **`AMD Instinct MI350P`** (CDNA 4 PCIe) | **`144 GB` HBM3e** | **`4,0 TB/s`** | `72 TFLOPS` | **`4.600 TFLOPS`** dense **MXFP4/MXFP6** / `2.300 TFLOPS` dense **FP8** | Veri merkezi PCIe kartı; devasa FP4 matris gücü |
| **`AMD Radeon AI PRO R9700`** (RDNA 4) | **`32 GB` GDDR6** | **`640–644,6 GB/s`** | `47,8 TFLOPS` | `383` dense / `766 TFLOPS` sparse **FP8** (`191 / 383` **FP16**) | Yerel iş istasyonu AI kartı |
| **`AMD Radeon PRO W7800`** (RDNA 3) | **`48 GB` GDDR6** *(maks. konfig)* | **`864 GB/s`** *(48 GB; 32 GB'da `576 GB/s`)* | `~45,2 TFLOPS` | `90,4 TFLOPS` **FP16 Matrix** / `90,4 TOPS` **INT8** | Bellek kapasitesi yüksek iş istasyonu sürümü |
| **`AMD Radeon RX 9070 XT`** (RDNA 4) | `16 GB` GDDR6 | **`640–644,6 GB/s`** | `~48,7 TFLOPS` | `389 TFLOPS` dense **FP16** / `1.557 TOPS` sparse **INT4** | Masaüstü tüketici kartı |
| **`AMD Radeon RX 7900 XTX`** (RDNA 3) | `24 GB` GDDR6 | **`960 GB/s`** | `~61,4 TFLOPS` | `123 TFLOPS` **FP16 Matrix** / `123 TOPS` **INT8** | Yüksek GDDR6 bant genişliği |

- **Yazılım Yığını:** **ROCm / HIP**, `rocBLAS` / `hipBLASLt`, RCCL, AITER, **PyTorch (ROCm)**, **vLLM (ROCm)**, **SGLang (ROCm)**, **llama.cpp (ROCm/HIP & Vulkan)**, ONNX Runtime.

---

## 5. Apple Mac Studio Maksimum Donanımları (`M5 Ultra`, `M3 Ultra`)

Apple'ın birleşik bellek (**Unified Memory**) mimarisi sayesinde CPU ve GPU aynı devasa bellek havuzuna kopyalamasız (*zero-copy*) erişir; tek bir Mac Studio kasa içinde yüz milyarlarca parametreli MoE modelleri çalıştırılabilir. *(Not: `M4 Ultra` atlanmıştır.)*

| Model | Maks. Unified Memory | Bant Genişliği | CPU / GPU / Neural Engine | Öne Çıkan Mimari Notu |
| --- | --- | --- | --- | --- |
| **`Apple M5 Ultra`** | **`512 GB`** | **`1.200 GB/s` (`1,2 TB/s`)** | `36-core CPU` / `80-core GPU` / `32-core Neural Engine` | Her GPU çekirdeğinin içinde gömülü **Neural Accelerator** birimi (prefill matris hızını sıçratır). |
| **`Apple M3 Ultra`** | **`512 GB`** | **`819 GB/s`** | `32-core CPU` / `80-core GPU` / `32-core Neural Engine` | **UltraFusion** çift zarlı birleştirme; `512 GB` kapasite ilk kez burada sunuldu. |

- **Yazılım Yığını:** **Metal**, **Apple MLX** (birleşik bellek + Apple Silicon için birincil LLM/MoE çıkarım çatısı), **llama.cpp (Metal)**, Core ML, **PyTorch (MPS)**.

---

## 6. Apple MacBook Pro Maksimum Donanımları (`M5 Max`, `M4 Max`, `M3 Max`)

Tam GPU çekirdekli üst *Max* binlerinde tam bellek yolu aktifken, giriş seviyesi kırpılmış Max binlerinde bant genişliğinin düştüğüne dikkat edilmelidir.

| Model | Maks. Unified Memory | Tam Bin Bant Genişliği | CPU / GPU / NPU | Alt (Kırpılmış) Bin Bant Genişliği Notu |
| --- | --- | --- | --- | --- |
| **`Apple M5 Max`** | **`128 GB`** | **`614 GB/s`** | `18-core CPU` / `40-core GPU` (+ Neural Accelerators) / `16-core NPU` | Kırpılmış GPU bininde `~460 GB/s` |
| **`Apple M4 Max`** | **`128 GB`** | **`546 GB/s`** (512-bit LPDDR5X) | `16-core CPU` / `40-core GPU` / `16-core NPU` | 14-core CPU / 32-core GPU bininde `410 GB/s` |
| **`Apple M3 Max`** | **`128 GB`** | **`400 GB/s`** | `16-core CPU` / `40-core GPU` / `16-core NPU` | 14-core CPU / 30-core GPU bininde `300 GB/s` |

- **Yazılım Yığını:** **Metal**, **Apple MLX**, **llama.cpp (Metal)**, Core ML, **PyTorch (MPS)**.

---

## 7. Apple Base MacBook Pro ve MacBook Air (Maksimum Bellek Konfigürasyonu: `M6`, `M5`, `M4`)

Taşınabilir giriş/temel serilerde (`Base` yongalar) maksimum yapılandırılabilir bellek **`32 GB`** düzeyindedir; küçük `7B–14B` nicemlenmiş ajan modelleri yerel çalıştırılabilir.

| Model | Üretim | Maks. Unified Memory | Bant Genişliği | GPU Çekirdeği | Mimari / Konfigürasyon Notu |
| --- | --- | --- | --- | --- | --- |
| **`Apple M6` (Base)** | 2nm | **`32 GB`** | **`170 GB/s`** (`24/32 GB`; `16 GB` sürüm `153 GB/s`) | `12-core GPU` (+ Neural Accelerators) | İlk dalgada odak verimlilik/base katmanda; 24/32 GB sürümlerde bant genişliği yükselir. |
| **`Apple M5` (Base)** | 3nm | **`32 GB`** | **`153 GB/s`** | `10-core GPU` (+ Neural Accelerators) | Gömülü GPU Neural Accelerators desteği. |
| **`Apple M4` (Base)** | 3nm | **`32 GB`** | **`120 GB/s`** | `10-core GPU` | 16–32 GB aralığında `120 GB/s`. |

- **Yazılım Yığını:** **Metal**, **Apple MLX**, **llama.cpp (Metal)**, Core ML, **PyTorch (MPS)**.

---

## 8. AMD Veri Merkezi Sistemleri (`MI300X`, `MI350X`, `MI355X`, `MI430X`, `MI455X` ve `AMD Helios`)

AMD'nin CDNA 3 → CDNA 4 → CDNA 5 yol haritası, HBM kapasitesi ve **HBM4** bant genişliği ile raf ölçekli açık ağ altyapısını (**AMD Helios**) birleştirir.

| Hızlandırıcı / Sistem | Mimari | Bellek & Tip | Bant Genişliği | Tepe Hesaplama & Öne Çıkan Özellik |
| --- | --- | --- | --- | --- |
| **`AMD Instinct MI300X`** | CDNA 3 (5nm/6nm) | `192 GB` HBM3 | `~5,3 TB/s` | FP8 / FP16 odaklı (donanımsal FP4 yok) |
| **`AMD Instinct MI350X / MI355X`** | CDNA 4 (3nm/6nm) | `288 GB` HBM3e | `~8,0 TB/s` | **`~10,1 PFLOPS`** MXFP4 sparse (`350X` hava / `355X` sıvı soğutmalı) |
| **`AMD Instinct MI430X`** | CDNA 5 (2nm/3nm sınıfı) | **`432 GB` HBM4** | **`~23,3 TB/s`** | **`288 TFLOPS` FP64** (HPC / Sovereign AI) + **`~9,2 PFLOPS` MXFP4** |
| **`AMD Instinct MI455X`** | CDNA 5 (2nm/3nm) | **`432 GB` HBM4** (12-stack) | **`~23,3 TB/s`** | **`~40,3 PFLOPS` OCP MXFP4** (*Helios amiral AI hızlandırıcısı*) |
| **`AMD Helios` (Raf Sistemi)** | CDNA 5 + EPYC "Venice" (Zen 6) | **`31 TB` HBM4** (`72× MI455X`) | `72 × 23,3 TB/s` | Çift genişlikli sıvı soğutmalı raf; **`2,9 ExaFLOPS` FP4** + Pensando ağı |

- **Yazılım Yığını:** **ROCm**, **HIP**, **RCCL**, **AITER**, **Triton (ROCm)**, **PyTorch (ROCm)**, **vLLM (ROCm)**, **SGLang (ROCm)**, **JAX (ROCm)**.

---

## 9. NVIDIA Son Kullanıcı / Geliştirici AI Bilgisayarları — `GB10` (`DGX Spark` ve `RTX Spark`)

Her iki platform da **NVIDIA GB10 Grace Blackwell Superchip** üzerine kuruludur: `20-core Arm Grace CPU` + `6.144 CUDA çekirdeği` + 5. nesil Tensor Core (`FP4`/`FP8`) tek **NVLink-C2C** tutarlı bellek havuzunda buluşur (**`1 PFLOPS` FP4 sparse**).

| Özellik | `NVIDIA DGX Spark` (`GB10`) | `NVIDIA RTX Spark` (`GB10` / N1X) |
| --- | --- | --- |
| **Form Faktörü** | Mini masaüstü geliştirici kutusu (ASUS/MSI/Lenovo/PNY vb.) | İnce dizüstü bilgisayar ve kompakt Windows PC |
| **Maks. Bellek & Tip** | **`128 GB` Unified LPDDR5X** (`64 GB` OEM seçenekli) | **`128 GB` Unified LPDDR5X** |
| **Bellek Bant Genişliği** | **`~273 GB/s`** (*gerçek ölçüm ~`215 GB/s`*) | **`~273–300 GB/s`** (ayarlanmış mobil/PC profilleri) |
| **Güç (TDP)** | `~140W` SoC / `240W` harici adaptör | `45–100W` dinamik mobil TDP |
| **Ağ / Kümeleme** | **`ConnectX-7 200 Gb/s`** QSFP (2 ünite birleşip `405B` çalıştırabilir) | Standart tüketici ağı (`ConnectX-7` yok) |
| **İşletim Sistemi & Yazılım** | **DGX OS (Ubuntu Linux)**, tam veri merkezi **CUDA**, NIM, TensorRT-LLM, vLLM, llama.cpp, PyTorch (CUDA) | **Windows 11 on Arm**, Windows Arm64 **CUDA**, TensorRT, ONNX Runtime, llama.cpp, PyTorch (CUDA) |

---

## 10. AMD Son Kullanıcı AI Bilgisayarları (`Strix Halo`, `Gorgon Halo`, `Strix Point`, `Gorgon Point`)

Büyük yerel modeller için tasarlanan yüksek bellekli **`Halo`** (`256-bit`) ailesi ile ince ultrabook'lara yönelik **`Point`** (`128-bit`) ailesi arasındaki fark **bant genişliği ve kapasite duvarını** net biçimde gösterir:

| Platform / İşlemci | Mimari & GPU / NPU | Maks. Bellek | Bellek Yolu & Bant Genişliği | Yazılım Yığını |
| --- | --- | --- | --- | --- |
| **`Gorgon Halo` (`Ryzen AI Max+ PRO 495`)** | Zen 5 + RDNA 3.5 refresh + XDNA 2 NPU | **`192 GB`** LPDDR5X-8000 | 256-bit → **`256 GB/s`** | **ROCm / HIP**, **Vulkan (`llama.cpp`)**, PyTorch (ROCm), ONNX / Ryzen AI |
| **`Strix Halo` (`Ryzen AI Max+ 395`)** | `16× Zen 5` + Radeon `8060S` (40 CU) + `50 TOPS` NPU | **`128 GB`** LPDDR5X-8000 | 256-bit → **`256 GB/s`** (*gerçek ölçüm ~`212–215 GB/s`*) | **ROCm / HIP**, **Vulkan (`llama.cpp`)**, PyTorch (ROCm), ONNX / Ryzen AI |
| **`Gorgon Point` (`Ryzen AI 9 HX 470`)** | Zen 5/5c + Radeon `890M` (16 CU, 3100 MHz) + `55 TOPS` NPU (`86` top.) | `256 GB` platform maks. *(LPDDR5X-8533)* | 128-bit → **`~136,5 GB/s`** | **ROCm**, **Vulkan (`llama.cpp`)**, DirectML / ONNX Runtime + AMD Ryzen AI SDK |
| **`Strix Point` (`Ryzen AI 9 HX 370`)** | `12× Zen 5/5c` + Radeon `890M` (16 CU, 2900 MHz) + `50 TOPS` NPU (`~80` top.) | `256 GB` platform maks. *(LPDDR5X-8000)* | 128-bit → **`~128 GB/s`** | **ROCm**, **Vulkan (`llama.cpp`)**, DirectML / ONNX Runtime + AMD Ryzen AI SDK |

---

## 11. Google 8. Nesil TPU Ailesi (`TPU 8t`, `TPU 8tx`, `TPU 8i`, `TPU 8i Max`)

7. nesil **Ironwood (TPU v7x)** (`192 GiB` HBM, `~4.614 TFLOPS` FP8) sonrasında Google, 8. nesilde "tek kalıp" yaklaşımını terk edip silikonu **büyük eğitim (`8t`)** ve **düşük gecikmeli ajan çıkarımı (`8i`)** olarak ikiye ayırmıştır:

| Özellik | `TPU 8t` (Training) | `TPU 8tx` (Confidential AI) | `TPU 8i` (Inference / Reasoning) | `TPU 8i Max` (Massive Context) |
| --- | --- | --- | --- | --- |
| **Ana Hedef** | Dev ön-eğitim, RL, dünya modelleri | Gizli eğitim, regüle kurumsal AI | Çok turlu akıl yürütme ve ajan servisi | Dev KV-cache, uzun bağlamlı ajanlar |
| **Silikon & Host CPU** | Eğitim silikonu + **Google Axion (Arm)** | `8t` silikonu + **5. Nesil AMD EPYC** (`AMD SEV` & PCIe şifreleme) | Çıkarım silikonu + **Google Axion (Arm)** | **Çift zarlı (`2× TPU 8i`)** tek paket |
| **HBM Kapasitesi** | `216 GB` | `216 GB` | `288 GB` | **`384–768 GB`** sınıfı |
| **HBM Bant Genişliği** | **`6,53 TB/s`** (`6.528 GB/s`) | **`6,53 TB/s`** | **`8,60 TB/s`** (`8.601 GB/s`) | **`17,2 TB/s`** |
| **On-Chip SRAM (`Vmem`)** | `128 MB` | `128 MB` | **`384 MB`** (3× genişletilmiş) | **`768 MB`** |
| **Tepe Hesaplama (FP4)** | **`12,6 PFLOPS`** | `~12,6 PFLOPS` | **`10,1 PFLOPS`** | **`~20,2 PFLOPS`** eşdeğeri |
| **Ağ & Özel Motor** | **Virgo Network** (3D Torus), `19,2 Tbps`, **SparseCore** (`9.600` çip = `2 PB` HBM, `121 EFLOPS`) | Boardfly ağı, donanım tabanlı kök-güven | **Boardfly Interconnect**, **Collectives Acceleration Engine (CAE)** (5× düşük collective gecikme) + **LLM Decoder Engine** | Boardfly + CAE + yüksek raf yoğunluğu |

- **Yazılım Yığını:** **JAX / XLA / Pallas**, **TorchTPU** (kod değiştirmeden doğrudan PyTorch desteği), **TPU Sync** (HBM ↔ Host DRAM ↔ ağ arası katmanlı KV-cache yönetimi, %90'a varan transfer gecikmesi düşüşü), **Cloud Pathways**, TensorFlow (XLA), **vLLM-TPU**, **SGLang-TPU**.

---

## 12. Huawei Ascend En Son Sistemleri (`910C`, `950PR` / `950DT`, `Atlas 350`, `CloudMatrix` ve `Atlas 950 SuperPoD`)

Huawei de tıpkı Google TPU v8 gibi 4. nesil Da Vinci v5 (`Ascend 950`) mimarisinde iş yükünü **Prefill (`950PR`)** ve **Decode/Eğitim (`950DT`)** çiplerine bölmüş, dış kısıtları yerli HBM (`HiBL 1.0`, `HiZQ 2.0`) ve küresel raf belleği (**UnifiedBus / UB Link**) ile aşmıştır.

| Sistem / Yonga | Mimari / Rol | Bellek & Yerli HBM | Bant Genişliği | Hesaplama & Küme Ölçeği |
| --- | --- | --- | --- | --- |
| **`Ascend 910C`** | Çift yongacıklı (chiplet) NPU | `128 GB` HBM2e / HBM3 | **`~3,2 TB/s`** | `~780–800 TFLOPS` FP16/BF16, `~550W` TDP (`CloudMatrix 384`: optik örgülü 384 NPU düğümü) |
| **`Ascend 950PR`** | Da Vinci v5 (**Prefill & Öneri**) | `128 GB` HiBL 1.0 HBM | **`1,6 TB/s`** | `~1 PFLOPS` FP8 (HiF8/MXFP8) / `2 PFLOPS` FP4 (MXFP4) (`Atlas 350` PCIe: `112 GB`, `1,4 TB/s`) |
| **`Ascend 950DT`** | Da Vinci v5 (**Decode & Eğitim**) | **`144 GB` HiZQ 2.0 HBM** | **`4,0 TB/s`** | `~1 PFLOPS` FP8 / `2 PFLOPS` FP4 |
| **`Atlas 950 SuperPoD`** | Raf / Süper Düğüm (`950DT` tabanlı) | `1.024+` NPU unified pool | UB Link PB/s sınıfı fabric | Sıvı soğutmalı, UnifiedBus küresel bellek adresleme |
| *Yol Haritası: `Ascend 960` / `970`* | Yeni nesil Ascend | `960`: `~288 GB` HBM | Ölçeklenmiş | `970`: `4 PFLOPS` FP8 / `8 PFLOPS` FP4 hedefi |

- **Yazılım Yığını:** **CANN** (*Compute Architecture for Neural Networks* — CUDA muadili), **AscendC** (özel çekirdek dili), **MindSpore**, **PyTorch (`torch_npu`)**, **MindIE**, **vLLM-Ascend**, **SGLang-Ascend**.

---

## 13. Yazılım Ekosistemi & Backend Eşleme Özeti

Aynı üst seviye model veya ajan kodu (ör. **PyTorch** veya **JAX**), hedef donanımın alt düzey derleyici ve haberleşme katmanına bağlanarak çalışır:

| Donanım Ailesi | Alt Düzey Çekirdek / Runtime | Ana Eğitim & Araştırma Çatısı | Üretim Inference Motorları |
| --- | --- | --- | --- |
| **NVIDIA (NVL72, H100/H200, Blackwell, Spark)** | **CUDA**, cuBLAS / CUTLASS / cuDNN, NCCL | **PyTorch (CUDA)**, JAX (CUDA) | TensorRT-LLM, vLLM, SGLang, Dynamo, llama.cpp |
| **AMD (Instinct, Helios, Radeon, Halo/Point)** | **ROCm / HIP**, rocBLAS / hipBLASLt, RCCL, Vulkan | **PyTorch (ROCm)**, JAX (ROCm) | vLLM (ROCm), SGLang (ROCm), AITER, llama.cpp |
| **Apple Silicon (Mac Studio, MBP, Air)** | **Metal**, Apple Neural Engine (ANE) | **MLX**, PyTorch (MPS) | MLX-LM, llama.cpp (Metal), Core ML |
| **Google TPU (v8 Ailesi)** | **XLA**, Pallas, CAE, **TPU Sync** | **JAX**, **TorchTPU (PyTorch)**, TensorFlow | vLLM-TPU, SGLang-TPU, Cloud Pathways |
| **Huawei Ascend (910C, 950PR/DT, Atlas)** | **CANN**, AscendC, HCCL, UB Link | **MindSpore**, **PyTorch (`torch_npu`)** | MindIE, vLLM-Ascend, SGLang-Ascend |
| **Cerebras (WSE-3 / CS-4 WSE-3T)** | **Cerebras SDK / CSL**, Weight Streaming | **PyTorch** (Cerebras front-end) | Cerebras Cloud Inference Server (özel wafer-scale) |
