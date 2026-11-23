# Alıştırmalar: Altyapı, Performans, Maliyet ve Değerlendirme

[Oturuma dön](../README.md) | [English](README.en.md) | [Demo rehberi](../demos/README.md) | [2026 Donanım Referansı](../donanim-referansi-2026.md)

Her alıştırmada seçtiğin donanım/mimari parametrelerini, ölçülen `TTFT`, `Prefill/Decode tok/s`, `cached_tokens`, `Joule/Token` ve değerlendirme skorlarını kaydet. Tüm alıştırmalar `AgentLab-Session05-G4.ipynb` (Ultra/Pro+ G4 veya H100), `pro_AgentLab-Session05-L4.ipynb` (Pro/Plus L4) ya da `plus_AgentLab-Session05-T4.ipynb` (Plus/Ücretsiz T4) defterlerindeki **Hücre 1** kurulumundan sonra veya [etkileşimli simülatör](../demos/inference-visualizer/prefill-decode-kv-sim.html) üzerinde bağımsız olarak çalışır.

## 1. GPU Bellek Hiyerarşisi, Roofline ve Prefill vs Decode (`Deney 1` & Simülatör — `5.1`)

- **1A (Memory Wall hesabı):** [2026 Donanım Referansı](../donanim-referansi-2026.md) tablosunu kullanarak `Gemma 4 12B Q4_0 (~7,2 GB)` için `Tesla T4` (`320 GB/s`), `RTX PRO 6000 Blackwell` (`1.792 GB/s`), `H100 SXM` (`3,35 TB/s`) ve `AMD MI455X` (`23,3 TB/s`) teorik decode tavanlarını (`BW / 7,2`) ve `%70` pratik hız aralığını hesapla; `Deney 1` içindeki canlı ölçümünle karşılaştır.
- **1B (`ubatch` GEMM vs Saf Decode `GEMV` vs Batching):** Simülatörün **Sekme 2** ekranında `--ubatch-size` ve `Concurrent Users N` kaydırıcılarını değiştirerek neden tek kullanıcılı decode sırasında Tensor Core'ların boş kaldığını (`GEMV`) ve `N=32/64` eşzamanlı kullanıcıda hesaplamaya nasıl doyduğunu (`GEMM`) kaydet.
- **1C (`MTP` vs `DFLASH` & `WSE-3T`):** Simülatör **Sekme 4** üzerinde kabul oranını (`α`) `%30` ile `%80` arasında kaydırarak `MTP` ile `DFLASH` (Block Diffusion) hızlanmasını ve `Cerebras WSE-3T` (`43,2 PB/s` on-chip SRAM) mimarisinin neden `batch=1` decode hızında sıçrama yapıp yoğun ön-eğitimde GPU kümelerine göre farklı ödünleşim sunduğunu açıkla.

## 2. KV Cache Mühendisliği, Prefix Caching ve L4 Cache Miss Vakası (`Deney 2` & Simülatör — `5.2`)

- **2A (`768 KB` vs `4 KB` vs `890 B`):** `256K` (`262.144` token) ve `1M` (`1.048.576` token) bağlamda klasik 48L FP16 MHA (`768 KB/tok`), `Gemma 4 12B FP8` (`4 KB/tok`) ve `DeepSeek-V4.1-Flash` (`890 B/tok`) toplam KV bellek gereksinimlerini hesapla ve hangi kartların VRAM'ine sığdığını işaretle.
- **2B (`Cold` vs `Warm` Prefix Caching):** `Deney 2` çıktısından ilk (`Cold`) ve ikinci (`Warm`) turun `cached_tokens`, `prompt_ms` ve `TTFT` değerlerini karşılaştırıp hızlanma çarpanını yaz.
- **2C (3'lü Cache Miss teşhisi):** Oturum 03 L4 canlı vakasındaki `(1) enable_thinking=False 3-token kayması`, `(2) SWA 1024 penceresi nedeniyle --cache-reuse kapanması` ve `(3) --parallel 2 slot_prompt_similarity=0.1 + sabitlenmemiş id_slot` etkilerinden her birinin hangi ayarla (`preserve_thinking=True`, `id_slot=0`, `--swa-full` / `vLLM APC`) çözüldüğünü açıkla.

## 3. Maliyet ve AI Factory Enerji Ekonomisi (`Deney 2` — `5.3`)

- **3A (`Joule/Token` & `$/1M Token`):** `Deney 2` içinde okunan canlı `nvidia-smi` güç (`Watt`) ve hız (`tok/s`) değerlerinden kendi GPU'nun anlık `Joule/Token = Watt / tok_s` değerini hesapla; baz ölçümlerle (`T4 ~2,33 J/tok` vs `G4 8-slot MTP5 ~0,46 J/tok`) kıyasla.
- **3B (Batching ile enerji düşüşü):** Simülatörde `N=1` ve `N=16` durumlarında toplam `tok/s` artarken neden `Joule/Token` ve `$/1M Token` değerlerinin düştüğünü 2 cümleyle özetle.

## 4. Observability ve Tracing (`Deney 3` — `5.4`)

- **4A (Span ağacı okuma):** `Deney 3` tarafından `day-05-infra-evals` altına yazılan JSON trace çıktısındaki `llm_prefill`, `llm_decode` ve `tool_exec` span sürelerini topla; toplam duvar süresinin (`total_ms`) yüzdesel dağılımını çıkar.
- **4B (`/metrics` alarm eşiği):** Üretimde KV havuzu doluluğu `%90` üzerine çıktığında veya `TTFT p95` iki katına fırladığında hangi `/metrics` ve `timings` sinyallerine bakacağını belirt.

## 5. Evals, Artificial Analysis ve 2026 Mimariler Finali (`Deney 3` — `5.5`)

- **5A (3 Katmanlı Eval Tasarımı):** `Deney 3` Mini Eval Suite çıktısında deterministik (JSON/araç), trajectory (adım sırası) ve `LLM-as-a-Judge` kontrollerinin her birinin yakaladığı farklı hata türünü yaz; `LLM-as-a-Judge` için uzunluk/konum yanlılığını azaltacak bir kural öner.
- **5B (2026 Frontier Mimari Seçimi):** Aşağıdaki senaryolar için `Gemma 4 12B`, `Gemma 4 26B A4B`, `Qwen 3.8 27B`, `DeepSeek-V4-Flash`, `DeepSeek-V4.1-Flash` ve `Kimi 3.1 Pro` arasından seçim yapıp gerekçelendir: (i) tek T4 üzerinde minimum bellek, (ii) `1M` bağlamda `< 1 GB` KV cache, (iii) maksimum kodlama/ajan kalitesi vs toplam `26B / 4B aktif` MoE hız dengesi.

## 6. Kendi Inference, Donanım ve Eval Bütçeni Tasarla

Seçtiğin bir ajan iş yükü için beş kararlı bir üretim bütçesi çıkar: (1) hedef model ve nicemleme (`FP8` / `NVFP4` / `Q4_0`), (2) Roofline `BW / aktif ağırlık` hesabıyla seçilen donanım ve `ubatch` / `batch` stratejisi, (3) `KV cache` bayt/token hedefi + `Prefix Caching` kuralı, (4) `$/1M Token` ve `Joule/Token` hedef eşiği, (5) `Observability` span'ları ile 3 adımlı `Eval` kapısı. Çalışmanı `Canlı Stüdyo` (`Hücre 5`) üzerinde test ettikten sonra **Hücre 6 (`2. Güvenli Kapanış`)** ile oturumu kapat.
