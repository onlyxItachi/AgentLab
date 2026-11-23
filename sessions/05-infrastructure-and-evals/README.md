# 05 — Altyapı, Performans, Maliyet ve Değerlendirme

[Ana sayfa](../../README.md) | [English](README.en.md)

**Süre:** Yaklaşık 90 dakika. Önkoşullar için önceki günlerin tam tekrarı yerine aşağıdaki **5 dakikalık Gün 1–4 köprü özetini** oku; ayrıntılı geçmiş dersler ([01](../01-llm-fundamentals/README.md), [02](../02-agent-core-and-state/README.md), [03](../03-modern-agent-stack/README.md), [04](../04-security-and-execution/README.md)) ders dışı başvuru içindir.

Bu oturumda "çalışan" bir ajan sistemini **ölçülebilir, hızlı, enerji/maliyet verimli ve doğrulanabilir bir üretim sistemine** dönüştürüyoruz. İlk olarak GPU bellek hiyerarşisini (`HBM → L2 → SRAM → Tensor Cores`), **Roofline / Memory Wall** sınırını, **Chunked Prefill (`GEMM`)** vs **Saf Decode (`GEMV`)**, **Continuous Batching**, nicemleme (`FP16/FP8/NVFP4/Q4_0`), **Speculative Decoding (`MTP` & `DFLASH`)** ve wafer-scale mimariyi (`Cerebras WSE-3 / WSE-3T`) inceleyeceğiz (`5.1`). Ardından **KV Cache & Prefix Caching** belleğini (`768 KB/tok` vs `4 KB/tok` vs `890 B/tok`) ve gerçek L4 üçlü cache-miss vakasını çözecek (`5.2`), **`$/1M Token` ve `Joule/Token`** ile AI Factory ekonomisini ölçecek (`5.3`), `/metrics` ve **Span Tree Tracing** ile gözlemlenebilirlik kuracak (`5.4`), son olarak **Evals**, **Artificial Analysis Pareto** eksenleri ve **2026 Frontier Mimariler Finali** ile oturumu tamamlayacağız (`5.5`).

> **Canlı ders öncesi öneri:** Başlamadan önce [ders notlarının başındaki 5 dakikalık Gün 1–4 köprü özetine](ders-notlari.md#5-dakikalık-gün-14-köprü-özeti), [2026 AI Donanım Referansına](donanim-referansi-2026.md) ve [oturum sözlüğüne](kavram-sozlugu.md) hızlıca göz at.

## Öğrenme hedefleri

- `5.1` GPU bellek hiyerarşisini, **Roofline** modelindeki *memory-bound decode* (`GEMV`) ile *compute-bound prefill / batch* (`GEMM`) farkını, **Chunked Prefill (`--ubatch-size`)**, **Continuous Batching**, nicemleme ve **`MTP` / `DFLASH`** hızlandırmasını kavramak.
- `5.2` **KV Cache** boyutunu katman/başlık mimarisi üzerinden hesaplamak (`768 KB/tok` → `4 KB/tok` → `890 B/tok`), **Prefix Caching (`cache_prompt=True`)** kazancını ölçmek ve token kayması / `SWA 1024` / slot yönlendirmesinden doğan cache-miss nedenlerini teşhis etmek.
- `5.3` `$/1M Token` ve `Joule/Token = Watt / tok_s` denklemleriyle tekil akış (`batch=1`) ile çoklu oturum batching arasındaki AI Factory ekonomi ve enerji farkını (`T4 ~2,33 J/tok` vs `G4 8-slot ~0,46 J/tok`) ölçmek.
- `5.4` Sunucu `/metrics` sayaçları, `timings` alanları ve yapılandırılmış **Span Tree** (`llm_prefill`, `llm_decode`, `tool_exec`) izleriyle üretim gecikmesini ve darboğazları izlemek.
- `5.5` Deterministik testler, **Trajectory Evals**, **LLM-as-a-Judge** (ve yanlılık tuzakları), nicemleme doğruluk değerlendirmesi ve **Artificial Analysis Pareto** eksenleri üzerinden 2026 güncel model mimarilerini kıyaslamak.

## Derste izleyeceğimiz akış

| Dakika | Konu / gözlem |
| --- | --- |
| 0-5 | **5 Dakikalık Gün 1–4 Köprü Özeti** ve tek tuş kurulum (`Hücre 1`: `G4/H100`, `L4` veya `T4` üzerinde `Gemma 4 12B QAT + MTP`) |
| 5-25 | `5.1` Bellek hiyerarşisi (`HBM → SRAM`), Roofline, `Cerebras WSE-3T`, `Chunked Prefill` vs `Decode (GEMV)`, `MTP`/`DFLASH` + [Etkileşimli Simülatör](demos/inference-visualizer/prefill-decode-kv-sim.html) ve **Deney 1** |
| 25-44 | `5.2` KV Cache matematiği, **Prefix Caching** (`Cold vs Warm`), L4 3'lü Cache Miss vakası, `5.3` **`$/1M Token` & `Joule/Token`** ve **Deney 2** |
| 44-58 | `5.4` **Observability & Tracing** (`/metrics`, `timings`, `llm_prefill`/`llm_decode`/`tool_exec` span ağacı) |
| 58-74 | `5.5` **Evals** (Deterministik, Trajectory, LLM-as-a-Judge, Quantization Evals), **Artificial Analysis**, **2026 Mimariler Finali** ve **Deney 3** |
| 74-87 | **Canlı Stüdyo** (`Hücre 5` canlı telemetri: `Cached \| New`, `Output`, `tok/s` + `💭 Thinking` + kod yürütme) ve küçük grup uygulaması |
| 87-90 | `2. Güvenli Kapanış` (`Hücre 6`), Drive kaydı, VM bırakma ve sonraki atölye hazırlığı |

> **Müfredat Dışı Ek (Bonus):** Ders notlarının sonundaki [`Code Mode` (`Cloudflare & Anthropic Programmatic Tool Calling`)](ders-notlari.md#müfredat-dışı-ek-bonus-code-mode--batched-tool-calling-ve-sandbox-orkestrasyonu) bölümü, araç çağrılarını sandbox içinde toplu kod yürütmeye taşıyarak MCP bağlam maliyetini `%90–99` azaltan güncel üretim desenini özetler.

## Materyaller

[Ders notları](ders-notlari.md) | [2026 Donanım Referansı](donanim-referansi-2026.md) | [Oturum sözlüğü](kavram-sozlugu.md) | [Demolar](demos/README.md) | [Alıştırmalar](exercises/README.md) | [Etkileşimli Inference Simülatörü](demos/inference-visualizer/README.md)

## 7 Hücreli Tek-Tuş `#@title` Form Mimarisi ve Donanım Katmanları

Oturum 05 defterleri de **1 Markdown giriş hücresi + 6 gizli kodlu `#@title` form hücresi (`cellView: "form"`)** ile çalışır. Bu günde donanım etkisini **elma-elma** (*apples-to-apples*) karşılaştırabilmek için **üç katmanın tamamı** aynı **`Gemma 4 12B QAT + MTP`** modelini çalıştırır:

1. **Hücre 0 (Giriş Markdown):** 5 dakikalık Gün 1–4 köprü özeti, donanım katmanı eşleşmesi ve simülatör bağlantısı.
2. **Hücre 1 — `1. Tek Tuş Kurulum ve Gemma 4 Motor Başlatma`:** Bağlı GPU'yu katmana özel denetimle (`ALAB-E02`) doğrular, kişi-agnostik **`MyDrive/AgentLab-Agent-Runtime`** (`setup` paylaşımlı + `day-05-infra-evals` gün durumu) önbelleğini bağlar ve üç katmanda da **`Gemma 4 12B QAT + MTP`** (`f8_e4m3` FP8 KV, `--cache-reuse 64`, `Thinking` açık, streaming SSE, `id_slot=0`, `max_tokens=262144`, `timeout=None`) sunucusunu başlatır.
3. **Hücre 2 — `Deney 1`:** `Gemma 4 12B` `config.json` boyutları & KV matematiği (`768 KB/tok` vs `4 KB/tok` vs `890 B/tok`), mini tensör şekil/önbellek gösterimi ve kısa vs uzun istemde canlı `TTFT (ms)`, `Prefill tok/s`, `Decode tok/s` ölçümü (`5.1`).
4. **Hücre 3 — `Deney 2`:** `Cold Prefill` vs `Warm Prefix Cache` (`cache_prompt=True`, `cached_tokens`, `prompt_ms` hızlanma), tekil (`1`) vs çok kullanıcılı Continuous Batching (`8` slot G4/H100, `2` slot L4/T4) altında canlı `nvidia-smi` güç integraliyle **`Toplam Enerji / Toplam Token` (`Joule/Token`)** ve **`CU / 1M Token`** düşüşü + 2026 donanım referans karşılaştırması (`5.2` & `5.3`).
5. **Hücre 4 — `Deney 3`:** Çok adımlı ajanda yapılandırılmış **Span Trace** (`llm_prefill`, `llm_decode`, `tool_exec` → `day-05-infra-evals` iz kaydı), 3 kontrollü **Mini Agent Eval Suite** (deterministik JSON/araç + trajectory + LLM-as-a-Judge) ve 2026 Frontier Mimariler tablosu (`5.4` & `5.5`).
6. **Hücre 5 — `Canlı Stüdyo`:** Portsuz yerel Colab WebSocket WebUI (`register_callback` + `invokeFunction`). `Tam Ekran` (`ESC`), `Durdur`, `Arayüzü Kapat` (Kill Switch), FIFO sıraya ek olarak her yanıt tamamlandığında canlı **`Cached | New`**, **`Output`** ve **`tok/s`** telemetrisini gösterir; Gün 5 hazır çipleri (`⚡ Prefill/Decode & KV Hesapla`, `📊 3 Adımlı Traced Python Analizi`, `🏆 2026 Mimarileri Karşılaştır`) ile gelir.
7. **Hücre 6 — `2. Güvenli Kapanış, Drive Kaydı ve GPU Bırakma`:** WebUI arka plan görevini, `day-05-infra-evals` iz/oturum kayıtlarını (`drive.flush_and_unmount()`), `llama-server` sürecini ve Colab VM'ini (`unassign`) temiz kapatır.

> **Colab Plan ve Donanım Dizilimi (`G4 / H100` · `L4` · `T4` — Tümü `Gemma 4 12B QAT + MTP`):**
> - **[AgentLab-Session05-G4.ipynb](demos/infrastructure-and-evals/AgentLab-Session05-G4.ipynb)** — Colab **Ultra** & **Pro+** (`RTX PRO 6000 Blackwell [G4]` veya `NVIDIA H100`, `1M` / `1.048.576` GPU KV havuzu, `262.144` aktif bağlam)
> - **[pro_AgentLab-Session05-L4.ipynb](demos/infrastructure-and-evals/pro_AgentLab-Session05-L4.ipynb)** — Colab **Pro / Plus** (`NVIDIA L4`, `23 GB VRAM`, `512K` / `524.288` GPU KV + `8 GiB` host RAM önbelleği)
> - **[plus_AgentLab-Session05-T4.ipynb](demos/infrastructure-and-evals/plus_AgentLab-Session05-T4.ipynb)** — Colab **Plus / Ücretsiz** (`Tesla T4`, `15 GB VRAM`, `512K` / `524.288` GPU KV + `3 GiB` host RAM önbelleği)
> - **[prefill-decode-kv-sim.html](demos/inference-visualizer/prefill-decode-kv-sim.html)** — Kurulum gerektirmeyen, tamamen çevrimdışı çalışan 4 sekmeli + matematik çekmeceli etkileşimli sahne simülatörü ([simülatör rehberi](demos/inference-visualizer/README.md))

> **Sabit 2 Satırlık `ALAB-Exx` Hata Zırhı:** Tüm hücreler ham Python `Traceback` yerine `🚨 [HATA KODU: ALAB-Exx] <Durum açıklaması>` ve `İlgili dosyanın hata koduna bakın! Ve çözemezseniz yardım isteyin!` biçiminde 2 satırlık tanı kutusu gösterir. Her kodun adım adım çözümü Google Drive klasöründeki `hata-cozum-rehberi.pdf` (TR) ve `error-guide.pdf` (EN) belgelerinde yer alır.

Yazdırılabilir çalışma kitapçıkları (`oturum-05.pdf` / `session-05.pdf`) ve `ALAB-Exx` hata çözüm rehberleri (`hata-cozum-rehberi.pdf` / `error-guide.pdf`) canlı oturum Google Drive klasörü üzerinden paylaşılır.

[Önceki: Güvenlik ve Yürütme](../04-security-and-execution/README.md) | [Ana sayfa](../../README.md)
