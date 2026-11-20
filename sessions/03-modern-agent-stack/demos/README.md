# Demolar: Modern Ajan Sistemleri

[Oturuma dön](../README.md) | [English](README.en.md) | [Ders notları](../ders-notlari.md) | [Sözlük](../kavram-sozlugu.md) | [Alıştırmalar](../exercises/README.md)

Oturum 03 canlı defterleri **1 Markdown giriş hücresi + 6 gizli kodlu `#@title` form hücresi (`cellView: "form"`, toplam 7 hücre)** ile **Studio v2** düzeninde çalışır. Katılımcılar Python kodunun içinde `True`/`False` bayrağı değiştirmez; her adımda yalnızca **`▶`** çalıştırma düğmesine basar.

> **Donanım Katmanı Eşleştirme (`G4` / `L4` / `T4` — Sıkı Fail-Closed `ALAB-E02`):**
> - **[AgentLab-Session03-G4.ipynb](modern-agent-stack/AgentLab-Session03-G4.ipynb)** — Colab **Ultra / Pro** (`RTX PRO 6000 Blackwell`, `Qwen 3.8 27B + MTP`, `Thinking: xhigh`, hedef+taslak `f8_e4m3` FP8 KV, `1M` / `1.048.576` GPU KV + `8 GiB` RAM, `262.144` aktif bağlam, `draft_max=3`; L4/T4 üzerinde `ALAB-E02` ile reddeder)
> - **[pro_AgentLab-Session03-L4.ipynb](modern-agent-stack/pro_AgentLab-Session03-L4.ipynb)** — Colab **Pro / Plus** (`NVIDIA L4`, `>= 20.000 MiB` VRAM, `Gemma 4 12B QAT + MTP`, `--reasoning on`, `512K` / `524.288` GPU KV + `8 GiB` RAM önbelleği, `draft_max=3`)
> - **[plus_AgentLab-Session03-T4.ipynb](modern-agent-stack/plus_AgentLab-Session03-T4.ipynb)** — Colab **Plus / Ücretsiz** (`Tesla T4`, `~15 GB VRAM`, `Gemma 4 12B QAT + MTP`, `--reasoning on`, `512K` / `524.288` GPU KV + `3.072–6.144 MiB` RAM önbelleği, `draft_max=2`; `b12359` T4 ölçümü: `14.047 MiB` VRAM / `866 MiB` boş pay, `cached_tokens=182`, `324,07 tok/s` prefill, `41,69 tok/s` decode)
>
> Bağlı GPU türü ile defter katmanı uyuşmazsa sistem sessizce yedek moda düşmez; doğrudan `ALAB-E02` kodlu 2 satırlık tanı kutusu gösterir (`ALAB-E01` ise GPU seçilmediğini bildirir).

## 7 Hücreli Form Mimarisi (Studio v2)

| Hücre | `#@title` Başlığı / Rolü | Ekranda Gözlenecek Çıktı |
| --- | --- | --- |
| **Hücre 0** | Giriş Markdown kartı | 5 dakikalık özet, Studio v2 akışı, donanım katmanı (`G4` / `L4` / `T4`) ve `hata-cozum-rehberi.pdf` notu |
| **Hücre 1** | `🚀 1. Tek Tuş Kurulum ve Model Motor Başlatma (Sadece ▶ Butonuna Bas)` | Sıkı GPU doğrulama (`ALAB-E01`/`E02`), `MyDrive/AgentLab-Agent-Runtime` (`setup` + `day-03-modern-stack`) bağlantısı (`ALAB-E03`), G4'te `Qwen 3.8 27B + MTP` / L4-T4'te `Gemma 4 12B QAT + MTP` + `llama.cpp v1.0.0` (`b12359`, `ALAB-E04`) ve saniyeli `<Model> servinge hazır!` bildirimi |
| **Hücre 2** | `🔍 Deney 1 — MCP Araç Keşfi ve Progressive Disclosure Becerileri` | `SKILL_LIBRARY` (`policy-qa`, `incident-triage`) `saved_chars` tasarrufu ve canlı `MCP` (`InProcessMCPServer`, `tools/list`, `campus_kb`, `ops_desk`, `media_world`, `mcp__campus_kb__read_doc`, `olmayan-belge` fail-closed) |
| **Hücre 3** | `⚡ Deney 2 — Deterministik Kural Kapısı (0 Token) ve StructuredHandoff` | `0` tokenlık `deterministic_gate` (`TR-204`, `6 saat * 8.88 CU`), kısıt koruyan `StructuredHandoff` (`["T4", "14:00"]`, `max_handoffs=2`, `admin_agent` / `untrusted-ticket` reddi) ve `System1DecisionGate` (`Jev`/`Laya`: `Choice`/`Score`/`Noul`) |
| **Hücre 4** | `🧠 Deney 3 — System 1 -> System 2 Kademesi, Thinking ve Gerçek Kod Yürütme` | İzole `ExperimentSession`, `Noul=0.48 < 0.75` eskalasyonu (`escalated_to_system2=True`), System 2 (`Qwen 3.8 27B` `xhigh` / `Gemma 4 12B` `--reasoning on`) ile gerçek Python kod yürütme (`calc.py`) ve `DualLayerSessionStore` + KV önbelleği |
| **Hücre 5** | `🖥️ Canlı Ajan Stüdyosu (Tam Ekran + Thinking + Kod Yürütme + KV)` | Portsuz, çerezsiz `google.colab.output` JS RPC WebUI: tıklanabilir canlı `💭 Thinking` CoT bulutu + `🔧 Araç` kartları, Antigravity FIFO istem sırası (`[✕ Sıradan Çıkar]`), `[KV Kaydet]`/`[Yükle]`, hazır çipler, **`[⛶ Tam Ekran]`** (`ESC`), **`[⏹ Durdur]`** ve **`[🔌 Arayüzü Kapat]`** (Kill Switch -> `ALAB-E07`) |
| **Hücre 6** | `🛑 2. Güvenli Kapanış, Drive Kaydı ve GPU Bırakma (Tek Tık)` | Açık Stüdyo arayüzünü ve `llama-server` sürecini durdurur, Drive önbelleğini yazar (`drive.flush_and_unmount()`) ve Colab VM'ini bırakır (`runtime.unassign()`, `Hücre 1` çalışmamış olsa bile traceback üretmez) |

## Çalışma zamanı ve KV havuzu yapılandırması (Hücre 1)

- **Katmana özel modeller (`llama.cpp v1.0.0 b12359`):** **G4** katmanında `Qwen 3.8 27B + MTP` (`f8_e4m3` FP8 hedef+taslak KV, `1.048.576` `1M` GPU KV havuzu / `262.144` aktif bağlam); **L4/T4** katmanlarında doğal multimodal `Gemma 4 12B QAT + MTP` (`~7,699 GiB` / `8.266.977.117` bayt), Drive'da kişi-agnostik **`MyDrive/AgentLab-Agent-Runtime`** (`setup` günler arası ortak + `day-03-modern-stack` gün durumu).
- **Thinking modu ve örnekleme:** G4 (`Qwen 3.8 27B`) üzerinde `enable_thinking=True` + `reasoning_effort="xhigh"` (`temperature=1.0`, `top_p=0.95`, `top_k=20`); L4/T4 (`Gemma 4 12B`) üzerinde ikili `--reasoning on --reasoning-budget -1 --reasoning-preserve`, `enable_thinking=True`, `preserve_thinking=True` ve resmi Gemma 4 örneklemesi (`temperature=1.0`, `top_p=0.95`, `top_k=64`); tüm katmanlarda streaming SSE, `id_slot=0`, `max_tokens=262144` ve `timeout=None`.
- **KV önbellek havuzu:** Tüm katmanlarda hedef ve taslak (`-ctkd/-ctvd`) **`f8_e4m3` (FP8)** KV nicemleme, `--spec-draft-p-min 0.75` (`--spec-draft-n-max`: T4 `2`, L4/G4 `3`), `--kv-unified --kv-unified-per-slot 262144`, `--ctx-checkpoints 8` ve `cache_prompt=True` uygulanır: G4 `1.048.576` GPU KV (`--parallel 4`, `--cache-ram 8192`, hibrit DeltaNet güvenliği için `--cache-reuse 0`), L4/T4 ise `524.288` GPU KV + RAM (`--cache-reuse 64`) ile **`1.048.576` (`1M+`) toplam havuz** ve **`262.144` maksimum aktif bağlam** sunar.
- **Tekil kurulum başarı bildirimleri:**
  - `🆕 İlk kurulum tamamlandı ve Drive'a yedeklendi (X.Y sn) — <Qwen 3.8 27B | Gemma 4> servinge hazır!`
  - `⚡ Drive önbelleğinden X.Y sn'de yüklendi — <Qwen 3.8 27B | Gemma 4> servinge hazır!`
  - `♻️ Açık sunucu algılandı, kaldığı yerden bağlandı (X.Y sn) — <Qwen 3.8 27B | Gemma 4> servinge hazır!`

## Bağımsız Deneyler, Canlı Stüdyo ve Hata Zırhı

- **Sırasız ve bağımsız deneyler (`Deney 1`–`Deney 3`):** **Hücre 1** tamamlandıktan sonra `Deney 1`, `Deney 2` ve `Deney 3` hücreleri birbirine bağımlı değildir; istenen sırada çalıştırılabilir veya tekrar edilebilir (`ALAB-E05` ise önce Hücre 1'in çalıştırılması gerektiğini bildirir). `research_specialist` (`campus_kb`), `operations_specialist` (`ops_desk`) ve `simulation_specialist` (`media_world` — `generate_architecture_diagram` & `simulate_lab_capacity` T4-uyumlu mockup'ı) yalnızca kendi izinli araçlarını görür; `SLM`, kapalı `Jev` ve açık ağırlıklı ~100M Apache-2.0 `Laya` (`System1DecisionGate`: `Choice`, `Score`, `Noul`) farkı ile `DualLayerSessionStore` (`slot0.kv.bin` `binary_kv_hit` -> uyuşmazlıkta `text_replay_fallback`) doğrudan gözlenir.
- **Portsuz JS RPC WebUI (`Canlı Stüdyo`, Hücre 5):** Harici port yönlendirmesi veya üçüncü taraf çerez gerektirmez; doğrudan **`google.colab.output.register_callback`** + **`google.colab.kernel.invokeFunction`** kullanır. Hazır çipler (`105. Fibonacci Çalıştır`, `Python Maliyet Hesabı`, `Sandbox Kaçış Testi`) yanında `TR-204`, `MCP`, `StructuredHandoff` ve `System 1` senaryoları serbest istemle test edilebilir; `Tam Ekran` (`ESC`), `Durdur` ve `Arayüzü Kapat` (Kill Switch) her zaman görünürdür.
- **Sabit 2 satırlık `ALAB-Exx` hata zırhı:** Beklenmeyen ham Python izleri yerine tüm hatalar `ALAB-E01`–`ALAB-E10` veya `ALAB-E99` kutusuna düşer (`🚨 [HATA KODU: ALAB-Exx] ...`). Çözüm adımları için Drive'daki `hata-cozum-rehberi.pdf` veya `error-guide.pdf` belgelerine, gözlemleri yazmak için `oturum-03.pdf` / `session-03.pdf` çalışma kitapçıklarına bak.
