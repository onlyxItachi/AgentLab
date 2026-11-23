# Demolar: Altyapı, Performans, Maliyet ve Değerlendirme

[Oturuma dön](../README.md) | [English](README.en.md) | [Ders notları](../ders-notlari.md) | [2026 Donanım Referansı](../donanim-referansi-2026.md) | [Sözlük](../kavram-sozlugu.md) | [Alıştırmalar](../exercises/README.md)

Oturum 05 canlı defterleri **1 Markdown giriş hücresi + 6 gizli kodlu `#@title` form hücresi (`cellView: "form"`)** ile çalışır. Katılımcılar kod içine gizlenmiş bayrak aramaz; her adımda yalnızca **`▶`** çalıştırma düğmesine basar.

> **Donanım Katmanı Eşleştirme (`G4 / H100` · `L4` · `T4` — Tümü `Gemma 4 12B QAT + MTP`):**
> - **[AgentLab-Session05-G4.ipynb](infrastructure-and-evals/AgentLab-Session05-G4.ipynb)** — Colab **Ultra / Pro+** (`RTX PRO 6000 Blackwell [G4]` veya `NVIDIA H100`, `1M` / `1.048.576` GPU KV havuzu, `262.144` aktif bağlam)
> - **[pro_AgentLab-Session05-L4.ipynb](infrastructure-and-evals/pro_AgentLab-Session05-L4.ipynb)** — Colab **Pro / Plus** (`NVIDIA L4`, `512K` / `524.288` GPU KV + `8 GiB` host RAM önbelleği)
> - **[plus_AgentLab-Session05-T4.ipynb](infrastructure-and-evals/plus_AgentLab-Session05-T4.ipynb)** — Colab **Plus / Ücretsiz** (`Tesla T4`, `512K` / `524.288` GPU KV + `3 GiB` host RAM önbelleği)
>
> Bağlı GPU katmanla eşleşmezse (`g4` defterinde yalnız G4 veya H100 kabul edilir) sistem sabit 2 satırlık **`ALAB-E02`** uyarısı gösterir.

## Etkileşimli Çevrimdışı Simülatör (Kurulumsuz)

- **[prefill-decode-kv-sim.html](inference-visualizer/prefill-decode-kv-sim.html)** ([rehber](inference-visualizer/README.md)) — Dış CDN bağlantısı içermeyen, tarayıcıda ve Colab `IPython.display.HTML` içinde çevrimdışı çalışan 4 sekmeli + matematik çekmeceli (`🔬 Matematik & PyTorch`) görsel simülatör:
  1. **Sekme 1 (`🏗️ GPU Bellek Hiyerarşisi & Cerebras WSE`):** `HBM → L2 → SRAM → Tensor Cores`, canlı **Roofline** ibresi ve 2026 donanım seçici.
  2. **Sekme 2 (`⚡ Chunked Prefill (ubatch) vs Decode (GEMV) vs Batching`):** `--ubatch-size` ve `Concurrent Users N` kaydırıcılarıyla `[B × 3840]` GEMM ↔ `[1 × 3840]` GEMV ↔ `[N × 3840]` dönüşümü ve canlı `$/1M Token` + `Joule/Token` düşüşü.
  3. **Sekme 3 (`🗄️ KV Cache, Prefix Caching & Mimari Sıkıştırma`):** `768 KB/tok` vs `4 KB/tok` (`Gemma 4 12B`) vs `890 B/tok` (`DeepSeek-V4.1-Flash`), `Cold vs Warm` zaman çizelgesi ve L4 3'lü Cache Miss vakası.
  4. **Sekme 4 (`🚀 Saf Decode vs MTP vs DFLASH & 2026 Mimariler`):** `α` kabul oranı kaydırıcılı 3 şeritli yarış + 2026 Frontier Pareto kartları.

## 7 Hücreli Form Mimarisi

| Hücre | `#@title` Başlığı / Rolü | Ekranda Gözlenecek Çıktı |
| --- | --- | --- |
| **Hücre 0** | Giriş Markdown kartı | 5 dakikalık Gün 1–4 köprü özeti ve elma-elma `Gemma 4 12B QAT + MTP` katman notu |
| **Hücre 1** | `1. Tek Tuş Kurulum ve Gemma 4 Motor Başlatma` | Adım adım emojili ilerleme ve katmana göre `Gemma 4 12B QAT + MTP` (`f8_e4m3` FP8 KV, `--cache-reuse 64`, `Thinking` açık) hazır bildirimi |
| **Hücre 2** | `Deney 1` — Prefill (`ubatch`) vs Decode (`GEMV`), KV Matematiği & Mini Simülatör | `Gemma 4 12B` `config.json` boyutları, KV byte/token karşılaştırması, mini şekil/önbellek gösterimi ve kısa vs uzun istemde canlı `TTFT (ms)`, `Prefill tok/s`, `Decode tok/s` |
| **Hücre 3** | `Deney 2` — Caching (`Cold vs Warm`), Maliyet (`CU/1M Token`) ve Enerji (`Joule/Token`) | Aynı uzun istemde `Cold Prefill` vs `Warm Prefix Cache` (`cached_tokens`, `prompt_ms`, hızlanma oranı), `nvidia-smi` anlık `Watt` → canlı **`Joule/Token`** & **`CU/1M Token`** + 2026 donanım referans satırları |
| **Hücre 4** | `Deney 3` — Observability Span Trace, Mini Agent Eval Suite & 2026 Mimariler | Çok adımlı ajanda `llm_prefill` / `llm_decode` / `tool_exec` JSON span kayıtları (`day-05-infra-evals`), 3 kontrollü Mini Eval Suite (deterministik + trajectory + LLM-as-a-Judge) ve 2026 Frontier Mimariler tablosu |
| **Hücre 5** | `Canlı Stüdyo` — Portsuz, Çerezsiz Colab WebUI (+ Canlı Telemetri) | `Tam Ekran` (`ESC`), `Durdur`, `Arayüzü Kapat` (Kill Switch), FIFO sırası, Gün 5 hazır çipleri (`⚡ Prefill/Decode & KV Hesapla`, `📊 3 Adımlı Traced Python Analizi`, `🏆 2026 Mimarileri Karşılaştır`) ve her yanıtta canlı **`Cached \| New`**, **`Output`**, **`tok/s`** göstergesi |
| **Hücre 6** | `2. Güvenli Kapanış, Drive Kaydı ve GPU Bırakma` | WebUI arka plan görevini, `MyDrive/AgentLab-Agent-Runtime/day-05-infra-evals` iz/oturum yedeğini (`drive.flush_and_unmount()`), `llama-server` sürecini ve VM'i (`unassign`) kapatır |

## Çalışma zamanı yapılandırması (Hücre 1)

- **Tüm katmanlarda ortak model (`Gemma 4 12B QAT + MTP`):** Üç katmanın tamamında `gemma-4-12B-it-Q4_0.gguf` + `mtp-gemma-4-12B-it-Q4_0.gguf` (`1.0/0.95/64`, **`f8_e4m3` FP8 KV**, `--cache-reuse 64`, `draft_max=3`, `--reasoning on --reasoning-budget -1 --reasoning-preserve`, `enable_thinking=True`, `preserve_thinking=True`) çalışır; fark yalnızca donanım bant genişliği ve GPU KV havuzudur (`G4/H100`: `1M` / `1.048.576`, `L4`: `512K` + `8 GiB` RAM, `T4`: `512K` + `3 GiB` RAM).
- **Tekil kurulum başarı bildirimleri:**
  - `🆕 İlk kurulum tamamlandı ve Drive'a yedeklendi (X.Y sn) — Gemma 4 12B QAT + MTP servinge hazır!`
  - `⚡ Drive önbelleğinden X.Y sn'de yüklendi — Gemma 4 12B QAT + MTP servinge hazır!`
  - `♻️ Açık sunucu algılandı (X.Y sn) — Gemma 4 12B QAT + MTP servinge hazır!`

## Canlı Stüdyo WebUI ve Bağımsız Deneyler

- **Bağımsız `ExperimentSession` izolasyonu:** `Deney 1`, `Deney 2` ve `Deney 3` hücreleri Hücre 1 sonrasında izole çalışma klasörü açar; istenen sırayla tekrar koşulabilir.
- **Portsuz yerel WebSocket kanalı:** `Canlı Stüdyo` (`Hücre 5`) `google.colab.output.register_callback` ve `google.colab.kernel.invokeFunction` üzerinden çalışır; üçüncü taraf çerez gerektirmez ve Colab hücresini kilitlemez.
- **Hata zırhı (`ALAB-E01` – `ALAB-E99`):** Tüm hatalar sabit 2 satırlık `ALAB-Exx` kutusuna düşer. Çözüm adımları Drive klasöründeki `hata-cozum-rehberi.pdf` / `error-guide.pdf` belgelerinde, gözlemleri yazmak için kullanacağın çalışma kitabı ise `oturum-05.pdf` / `session-05.pdf` belgelerinde yer alır.
