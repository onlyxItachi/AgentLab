# Inference, Bellek Hiyerarşisi ve KV Cache Simülatörü

[Demolara dön](../README.md) | [English](README.en.md)

[prefill-decode-kv-sim.html](prefill-decode-kv-sim.html) dosyası, **Oturum 05 (Altyapı, Performans ve Değerlendirme)** kapsamında **%100 çevrimdışı** çalışacak şekilde tek bir HTML5/CSS/JS dosyası olarak tasarlanmış etkileşimli sahne simülatörüdür. Hiçbir harici CDN, internet bağlantısı veya yerel sunucu gerektirmez; tarayıcıda doğrudan açılabilir (`800p` ve `1080p` projektör çözünürlüklerine uyumludur) ya da Google Colab içinde `IPython.display.HTML` ile hücre çıktısı olarak görüntülenebilir.

## Nasıl Açılır?

- **Yerel Tarayıcı:** [prefill-decode-kv-sim.html](prefill-decode-kv-sim.html) dosyasına çift tıklayın veya herhangi bir modern tarayıcıda (`Chrome`, `Edge`, `Firefox`, `Safari`) açın.
- **Colab Hücresi İçinde:**
  ```python
  from IPython.display import HTML
  HTML(open("prefill-decode-kv-sim.html", encoding="utf-8").read())
  ```

## Simülatör Sekmeleri ve Özellikleri

1. **🏗️ GPU Bellek Hiyerarşisi & Cerebras WSE:**
   - `HBM/VRAM` → `L2 Cache` → `On-Chip SRAM / FlashAttention` → `Tensor Cores` canlı paket transferi animasyonu.
   - `Tesla T4`, `RTX PRO 6000 Blackwell (G4)`, `H100 SXM`, `H200 SXM`, `NVIDIA B300`, `AMD MI455X`, `Google TPU 8i`, `Huawei Ascend 950DT`, `Apple M5 Ultra`, `DGX Spark GB10`, `AMD Gorgon Halo`, `Cerebras WSE-3` ve `Cerebras WSE-3T / CS-4` profilleri için teorik ve ~%70 pratik decode (`tok/s`) hesabı ile canlı **Roofline** göstergesi (`Memory-Bound` vs `Compute-Bound`).
2. **⚡ Chunked Prefill (`ubatch`) vs Decode (`GEMV`) vs Batching:**
   - `Oynat / Duraklat / Adım / Sıfırla` kontrolleriyle `Tokenization` → `Embedding lookup E[ids]` → `Chunked Prefill` (`--ubatch-size` `64..512`, `[B × 3840] × W` GEMM) → `Saf Decode` (`[1 × 3840] × W` GEMV darboğazı) → `Continuous Batching` (`Concurrent Users N` `1..64`) akışı.
   - Eşzamanlı kullanıcı sayısı arttıkça canlı `$/1M Token` ve `Joule/Token` düşüşü.
3. **🗄️ KV Cache, Prefix Caching & Mimari Sıkıştırma:**
   - `8K`, `32K`, `128K`, `256K` ve `1M` bağlam uzunluklarında **Klasik 48L FP16 MHA**, **Gemma 4 12B (FP16 / FP8)**, **Qwen 3.8 27B (`3:1` DeltaNet + Full)**, **DeepSeek-V4-Flash** ve **DeepSeek-V4.1-Flash (`890 B/tok`)** bellek karşılaştırması.
   - `Cold Prefill` vs `Warm Prefix Cache` (`cache_prompt=True`) zaman çizelgesi ve etkileşimli **3 Yönlü Cache Miss Vaka Analizi** (`enable_thinking=False` 3-token şablon kayması, `SWA=1024` duvarı ve `--parallel 2` LRU slot yönlendirmesi).
4. **🚀 Saf Decode vs MTP vs DFLASH & 2026 Mimariler:**
   - Kabul oranı (`α`) kaydırıcısı ile 3 şeritli kayıpsız spekülatif doğrulama yarışı (`Saf Decode`, tek kullanıcı & continuous batching destekli `MTP`, paralel blok difüzyonlu `DFLASH`).
   - `Gemma 4 12B`, `Gemma 4 26B A4B`, `Qwen 3.8 27B`, `DeepSeek-V4-Flash`, `DeepSeek-V4.1-Flash` ve `Kimi 3.1 Pro` için etkileşimli Pareto haritası.
5. **🔬 Matematik & PyTorch Çekmecesi (Sağ Üst Düğme):**
   - Varsayılan olarak gizlidir; `google/gemma-4-12B-it/config.json` kesin katman boyutlarını ve okunabilir `Gemma4MiniModel` PyTorch referans kodunu açar.
