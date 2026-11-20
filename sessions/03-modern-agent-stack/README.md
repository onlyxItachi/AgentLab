# 03 — Modern Ajan Sistemleri

[Ana sayfa](../../README.md) | [English](README.en.md)

**Süre:** Yaklaşık 90 dakika. Önkoşul, [ikinci oturumdaki](../02-agent-core-and-state/README.md) harness, araç doğrulama, bağlam bütçesi ve bellek sınırlarını hatırlamaktır.

Bu oturumda 2. gündeki tek-ajan harness yapısını modüler ve üretime yakın bir mimariye taşıyoruz. Sabit kodlu tek bir araç listesi yerine `MCP` (`JSON-RPC 2.0`, `InProcessMCPServer`) ile `campus_kb`, `ops_desk` ve `media_world` eklentilerini çalışma anında (`tools/list`) keşfedecek, `Plugin` ve `Skill` katmanlarını `Progressive Disclosure` ile ayıracak, `deterministic_gate` ile `0` tokenlık kararları (`TR-204`, CU hesabı) LLM'e göndermeden çözecek, en az yetkili uzman ajanlar arasında `StructuredHandoff` kuracak ve `System1DecisionGate` (`Jev` ile açık ağırlıklı ~100M Apache-2.0 `Laya` karar ilkelleri: `Choice`/`Score`/`Noul`), `SLM`, `System 2` (G4'te **`Qwen 3.8 27B + MTP`** `xhigh` Thinking; L4/T4'te doğal multimodal **`Gemma 4 12B QAT + MTP`** `--reasoning on`), `World Model` (`media_world` mockup) ile çift katmanlı oturum kalıcılığını (`DualLayerSessionStore`) tek bir portsuz **Studio v2** deneyiminde birleştireceğiz.

> **Canlı ders öncesi öneri:** Başlamadan önce [oturum sözlüğündeki](kavram-sozlugu.md) temel terimlere 5 dakikalık bir göz atış yapman dersteki canlı akışı takip etmeni kolaylaştırır.

## Öğrenme hedefleri

- `MCP`, `JSON-RPC 2.0`, `Plugin` (`campus_kb`, `ops_desk`, `media_world`) ve `Skill` kavramlarını ayırmak; `InProcessMCPServer` üzerinde `tools/list` ile dinamik araç keşfini ve `Progressive Disclosure` bağlam tasarrufunu göstermek.
- Her görevin LLM gerektirmediğini savunmak; `deterministic_gate` (`0` token) ve hibrit doğrulama akışlarını uygulamak.
- Çoklu ajan orkestrasyonunda `routing`, `delegation` ve şemalı `StructuredHandoff` kullanarak bağlam kaybını (`context loss`) ve sahte yetki tırmandırmayı (`admin_agent`) önlemek.
- `System 1` karar ilkelleri (`Jev` ve açık ağırlıklı ~100M Apache-2.0 `Laya`: `Choice`/`Score`/`Noul`, `RLCD`), `SLM`, `System 2` (G4: `Qwen 3.8 27B + MTP` `xhigh` Thinking, hedef+taslak `f8_e4m3` FP8 KV, `1.048.576` `1M` GPU KV havuzu; L4/T4: doğal multimodal `Gemma 4 12B + MTP`, `llama.cpp v1.0.0 b12359`, `--reasoning on`, `f8_e4m3` FP8 KV, GPU içi `524.288` `512K` KV; tüm katmanlarda `262.144` maksimum aktif bağlam), T4-uyumlu `media_world` / `World Model` mockup orkestrasyonu ve `DualLayerSessionStore` (`binary_kv_hit` + `text_replay_fallback`) katmanlarını tanımak; `noul_confidence < 0.75` veya bozuk yüklerde `escalated_to_system2=True` eskalasyonunu görmek.

## Derste izleyeceğimiz akış

| Dakika | Konu / gözlem |
| --- | --- |
| 0-8 | 2. gün harness köprüsü ve tek tuş kurulum (`Hücre 1`: G4 `Qwen 3.8 27B servinge hazır!` / L4-T4 `Gemma 4 servinge hazır!`) |
| 8-24 | Araç ekosistemi: `MCP` (`tools/list`), `Plugin`, `Skill`, `Progressive Disclosure` ve **Deney 1** (`Hücre 2`) |
| 24-44 | Deterministik kural kapısı (`0` token), çoklu ajan `StructuredHandoff`, `System1DecisionGate` ve **Deney 2** (`Hücre 3`) |
| 44-66 | `System 1 -> System 2` eskalasyonu, `DualLayerSessionStore` + `f8_e4m3` KV önbelleği, Thinking & canlı kod yürütme ve **Deney 3** (`Hücre 4`) |
| 66-85 | **Canlı Stüdyo** (`Hücre 5` portsuz JS RPC WebUI, `💭 Thinking` + `🔧 Tool Call` + KV kaydet/yükle) ve küçük grup alıştırması |
| 85-90 | `2. Güvenli Kapanış` (`Hücre 6`: Drive kaydı + VM bırakma) ve Oturum 04'e geçiş |

## Materyaller

[Ders notları](ders-notlari.md) | [Oturum sözlüğü](kavram-sozlugu.md) | [Demolar](demos/README.md) | [Alıştırmalar](exercises/README.md)

## 7 Hücreli Tek-Tuş `#@title` Form Mimarisi (Studio v2) ve Donanım Katmanları

Bu oturumda katılımcılardan hücre içinde `True`/`False` bayrağı avlamaları istenmez. Colab defterleri **1 Markdown giriş hücresi + 6 gizli kodlu `#@title` form hücresi (`cellView: "form"`)** ile tasarlanmıştır; her adımda yalnızca başlık ve **`▶`** çalıştırma düğmesi görünür (`Deney 1`–`Deney 3` birbirinden bağımsızdır ve sırasız çalıştırılabilir):

1. **Hücre 0 (Giriş Markdown):** 5 dakikalık özet, Studio v2 hızlı akış, donanım katmanı seçimi ve hata kodu başvurusu.
2. **Hücre 1 — `🚀 1. Tek Tuş Kurulum ve Model Motor Başlatma (Sadece ▶ Butonuna Bas)`:** Bağlı GPU'yu sıkı katman doğrulamasıyla kontrol eder (`G4` yalnızca RTX PRO 6000 Blackwell'i kabul eder, aksi durumda `ALAB-E02` verir), **`MyDrive/AgentLab-Agent-Runtime`** (`setup` paylaşımlı + `day-03-modern-stack` gün durumu) önbelleğini bağlar ve G4 katmanında **`Qwen 3.8 27B + MTP`** (hedef+taslak `f8_e4m3` FP8 KV, `reasoning_effort="xhigh"`, `1.0/0.95/20`, `--ctx-size 1048576 --parallel 4 --kv-unified --kv-unified-per-slot 262144 --ctx-checkpoints 8 --cache-reuse 0 --cache-ram 8192`, `draft_max=3`, `262.144` aktif bağlam / `1.048.576` GPU KV havuzu), L4/T4 katmanlarında **`Gemma 4 12B QAT + MTP`** (`--reasoning on --reasoning-budget -1 --reasoning-preserve`, `enable_thinking=True`, `preserve_thinking=True`, `1.0/0.95/64`, hedef+taslak `f8_e4m3` FP8 KV önbelleği, `--spec-draft-p-min 0.75`, `draft_max`: T4 `2`, L4 `3`, `524.288` GPU KV + RAM = `1.048.576` toplam KV havuzu) sunucusunu `llama.cpp v1.0.0` (`b12359`, `timeout=None`) ile başlatır; canlı test sonunda **`Qwen 3.8 27B servinge hazır!`** (G4) veya **`Gemma 4 servinge hazır!`** (L4/T4) bildirimini kesin saniye (`X.Y sn`) bilgisiyle basar.
3. **Hücre 2 — `🔍 Deney 1 — MCP Araç Keşfi ve Progressive Disclosure Becerileri`:** `Progressive Disclosure` (`SKILL_LIBRARY`, `policy-qa`, `incident-triage`, `saved_chars`) ve canlı `MCP` (`InProcessMCPServer`, `tools/list`, `campus_kb`, `ops_desk`, `media_world`, `olmayan-belge` fail-closed) araç çağrısı ile deterministik sınırları gösterir.
4. **Hücre 3 — `⚡ Deney 2 — Deterministik Kural Kapısı (0 Token) ve StructuredHandoff`:** `TR-204` ve `6 saat * 8.88 CU` sorgularını `0` LLM tokenıyla çözen `deterministic_gate` kapısını, kısıt koruyan (`["T4", "14:00"]`, `max_handoffs=2`, `admin_agent` ve `untrusted-ticket` reddi) çoklu ajan `StructuredHandoff` yapısını ve `System1DecisionGate` (`Jev` / açık ağırlıklı ~100M Apache-2.0 `Laya`: `Choice`/`Score`/`Noul`) sözleşmesini doğrular.
5. **Hücre 4 — `🧠 Deney 3 — System 1 -> System 2 Kademesi, Thinking ve Gerçek Kod Yürütme`:** İzole `ExperimentSession` içinde `Noul=0.48 < 0.75` düşük güven eskalasyonunu (`escalated_to_system2=True`), System 2 devralımını (`Qwen 3.8 27B + MTP` `xhigh` / `Gemma 4 12B + MTP` `--reasoning on`), çalışma alanında gerçek Python kod yürütmeyi ve `DualLayerSessionStore` + KV önbelleğini çalıştırır.
6. **Hücre 5 — `🖥️ Canlı Ajan Stüdyosu (Tam Ekran + Thinking + Kod Yürütme + KV)` (`Canlı Stüdyo`):** Harici port veya üçüncü taraf çerez gerektirmeyen yerel **`google.colab.output`** JS RPC WebUI (`register_callback` + `invokeFunction`). Açılır-kapanır tıklanabilir canlı **`💭 Düşünce Akışı (Thinking)`** CoT bulutu, **`🔧 Tool Call`** / çıktı akışı, Antigravity tarzı **FIFO istem sırası (`[✕ Sıradan Çıkar]`)**, `DualLayerSessionStore` `[KV Kaydet]` / `[Yükle]` (`binary_kv_hit` + `text_replay_fallback` + geçmiş senkronizasyonu), hazır istem çipleri, **`[⛶ Tam Ekran]`** (`ESC` ile küçülür), **`[⏹ Durdur]`** ve **`[🔌 Arayüzü Kapat]`** (Kill Switch -> `ALAB-E07`) kontrollerini sunar.
7. **Hücre 6 — `🛑 2. Güvenli Kapanış, Drive Kaydı ve GPU Bırakma (Tek Tık)`:** Açık Stüdyo arayüzünü ve `llama-server` sürecini durdurur, Google Drive önbelleğini yazar (`drive.flush_and_unmount()`) ve Colab VM'ini (`runtime.unassign()`) bırakır; `Hücre 1` çalıştırılmamış olsa bile izsiz, traceback'siz tamamlanır (`ALAB-E10` zırhı).

> **Colab Plan ve Donanım Dizilimi (`G4` / `L4` / `T4` — Sıkı Fail-Closed `ALAB-E02`):** Oturum 03'te üç katman desteklenir:
> - **[AgentLab-Session03-G4.ipynb](demos/modern-agent-stack/AgentLab-Session03-G4.ipynb)** — Colab **Ultra / Pro** (`RTX PRO 6000 Blackwell`, `Qwen 3.8 27B + MTP`, `Thinking: xhigh`, hedef+taslak `f8_e4m3` FP8 KV, `1M` / `1.048.576` GPU KV + `8 GiB` RAM, `262.144` aktif bağlam, `draft_max=3`; L4/T4 bağlıysa `ALAB-E02` ile durur)
> - **[pro_AgentLab-Session03-L4.ipynb](demos/modern-agent-stack/pro_AgentLab-Session03-L4.ipynb)** — Colab **Pro / Plus** (`NVIDIA L4`, `>= 20.000 MiB` VRAM, `512K` / `524.288` GPU KV + `8 GiB` RAM önbelleği, `draft_max=3`)
> - **[plus_AgentLab-Session03-T4.ipynb](demos/modern-agent-stack/plus_AgentLab-Session03-T4.ipynb)** — Colab **Plus / Ücretsiz** (`Tesla T4`, `~15 GB VRAM`, `512K` / `524.288` GPU KV + `3.072–6.144 MiB` RAM önbelleği, `draft_max=2`; `b12359` T4 ölçümünde `14.047 MiB` VRAM, `cached_tokens=182`, `324,07 tok/s` prefill, `41,69 tok/s` decode)

> **Sabit 2 Satırlık `ALAB-Exx` Hata Zırhı:** Defterdeki tüm hücreler ham Python `Traceback` yerine `🚨 [HATA KODU: ALAB-Exx] <Durum açıklaması>` ve `İlgili dosyanın hata koduna bakın! Ve çözemezseniz yardım isteyin!` biçiminde 2 satırlık tanı kutusu gösterir (`ALAB-E01`–`ALAB-E10`, `ALAB-E99`). Her kodun çözümü Drive klasöründeki `hata-cozum-rehberi.pdf` ve `error-guide.pdf` belgelerinde yer alır.

Basılabilir Türkçe (`oturum-03.pdf`) ve İngilizce (`session-03.pdf`) öğrenci çalışma kitapçıkları Google Drive dağıtım klasöründe paylaşılır.

[Önceki: Ajan Mimarisi ve Bellek](../02-agent-core-and-state/README.md) | [Sonraki: Güvenlik ve Yürütme](../04-security-and-execution/README.md)
