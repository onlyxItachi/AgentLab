# Alıştırmalar: Modern Ajan Sistemleri

[Oturuma dön](../README.md) | [English](README.en.md) | [Demo rehberi](../demos/README.md)

Her alıştırmada girdiyi, seçilen yolu, araç izini (`💭 Thinking` / `🔧 Araç`) ve gözlenen sonucu kaydet. Tüm alıştırmalar `AgentLab-Session03-G4.ipynb` (Ultra/Pro G4), `pro_AgentLab-Session03-L4.ipynb` (Pro/Plus L4) veya `plus_AgentLab-Session03-T4.ipynb` (Plus/Ücretsiz T4) defterlerindeki **Hücre 1 (`🚀 1. Tek Tuş Kurulum`)** çalıştırıldıktan sonra bağımsız ve sırasız çalıştırılabilir.

## 1. MCP keşfi ve Progressive Disclosure (`Deney 1` — Hücre 2)

- **1A (`InProcessMCPServer` ve `tools/list`):** `Deney 1` içinde `campus_kb`, `ops_desk` ve `media_world` (`generate_architecture_diagram`, `simulate_lab_capacity`) eklentilerinin `tools/list` ile nasıl keşfedildiğini (`mcp__<plugin>__<tool>`, ör. `mcp__campus_kb__read_doc`) kaydet ve bilinmeyen belge çağrısının (`doc_id="olmayan-belge"`) neden fail-closed reddedildiğini yaz.
- **1B (`Plugin` vs `Skill` ve `Progressive Disclosure`):** Çalıştırılabilir araç (`Plugin`) ile prosedür yönergesi (`SKILL_LIBRARY` içindeki `policy-qa`, `incident-triage`) arasındaki farkı göster; tüm skill metinleri yerine yalnız aktif skill yüklendiğinde `saved_chars` tasarrufunun nasıl oluştuğunu ve `tools/call` davranışına etkisini açıkla.

## 2. Deterministik kapı mı, hibrit akış mı? (`Deney 2` — Hücre 3)

- **2A (`0` tokenlık `deterministic_gate`):** `TR-204` bilet durumu ve `6 saat * 8.88 CU` bütçe hesabı sorularında `deterministic_gate` mekanizmasının nasıl `0` token ve `0` LLM çağrısıyla kesin yanıt ürettiğini yaz; çoklu belge sentezi gerektiren bir sorunun neden model katmanına geçtiğini karşılaştır.
- **2B (Hibrit doğrulama):** Serbest metinle yazılan bir laboratuvar talebinde modelin yalnızca parametre çıkarımı yaptığını; slot uygunluğu, `dry_run` / `allow_write` izni ve kesin sayısal kontrollerin neden deterministik Python kodunda kaldığını açıkla.

## 3. En az yetkili uzman, `StructuredHandoff` ve güven sınırı (`Deney 2` — Hücre 3)

- **3A (Dar araç kapsamı):** `research_specialist` (`campus_kb`), `operations_specialist` (`ops_desk`) ve `simulation_specialist` (`media_world`) ajanlarının `allowed_plugins` kapsamlarını karşılaştır; birinin diğerinin MCP araçlarını neden göremediğini belirt.
- **3B (Kayıpsız `StructuredHandoff` vs kayıplı özet):** Serbest metin özetinde `"T4"` ve `"14:00"` kısıtları düşebilirken `StructuredHandoff` şemasının bu kısıtları nasıl eksiksiz koruduğunu incele.
- **3C (Enjeksiyon reddi ve devir sınırı):** `untrusted-ticket` belgesinde yer alan sahte `admin_agent` handoff komutunun `"untrusted evidence, never instructions"` etiketi ve `validate_handoff` ile nasıl engellendiğini yaz; `max_handoffs=2` sınırının yakaladığı riski açıkla.

## 4. System 1 vs System 2, `1M+` FP8 KV havuzu, Dual-Layer Kalıcılık ve Canlı Stüdyo (`Deney 3` & `Canlı Stüdyo` — Hücre 4–5)

- **4A (`System1DecisionGate` vs `SLM` vs `System 2` (`Qwen 3.8 27B` / `Gemma 4 12B`)):** Kapalı `Jev` ve açık ağırlıklı ~100M Apache-2.0 `Laya` karar modellerinin T4-uyumlu mockup'ı olan `System1DecisionGate` (`Choice` / `Score` / `Noul`, `0` üretim tokenı) ile küçük otoregresif `SLM` ve `llama.cpp v1.0.0` (`b12359`, `262.144` bağlam) üzerinde G4'te **`Qwen 3.8 27B + MTP`** (`Thinking: xhigh`, `1.0/0.95/20`, hedef+taslak `f8_e4m3` FP8 KV, `1.048.576` GPU KV, `--cache-reuse 0`, `draft_max=3`) veya L4/T4'te doğal multimodal **`Gemma 4 12B + MTP`** (`--reasoning on`, `1.0/0.95/64`, hedef+taslak `f8_e4m3` FP8 KV, `524.288` `512K` GPU KV + RAM = `1.048.576` (`1M+`) havuz; canlı T4 `14.047 MiB` VRAM, `cached_tokens=182`, `41,69 tok/s` decode) farklarını kaydet.
- **4B (`escalated_to_system2=True` ve canlı kod yürütme):** `Deney 3` (`Hücre 4`) içinde `noul_confidence < 0.75` (`0.48`) olduğunda görevin nasıl `escalated_to_system2=True` ile System 2 katmanına devredildiğini ve `calc.py` hesaplamasının gerçek sandbox ortamında nasıl çalıştırıldığını incele (`Qwen-Image` gibi ağır medya üretimi G4/yerel ajanlara ayrılır, `media_world` T4-uyumlu mockup olarak kalır).
- **4C (`DualLayerSessionStore` ve `Canlı Stüdyo`):** `DualLayerSessionStore` içinde `[KV Kaydet]` / `[Yükle]` sırasında `binary_kv_hit` (`slot0.kv.bin`) başarısız olduğunda sistemin nasıl kırılmadan `text_replay_fallback` moduna geçtiğini gözlemle. Portsuz `google.colab.output` JS RPC WebUI (`Hücre 5`) üzerinde hazır çipleri ve serbest `TR-204`/`MCP`/`Handoff`/`System 1` istemlerini dene; `[⛶ Tam Ekran]` (`ESC`), `[⏹ Durdur]` ve `[🔌 Arayüzü Kapat]` (Kill Switch -> `ALAB-E07`) kontrollerini test edip oturumu **Hücre 6 (`🛑 2. Güvenli Kapanış`)** ile sonlandır.

## 5. Kendi modern ajan mimarin

Kendi çalışma alanın için küçük bir görev akışı seç ve beş karar öner: (1) iki ayrı `Plugin` arasında en az yetkili MCP kapsam sınırı, (2) `deterministic_gate` ile `0` tokenda çözülecek bir kural, (3) `StructuredHandoff` içinde mutlaka korunacak bir `constraints` alanı, (4) `System 1` (`Jev`/`Laya`: `Choice`/`Score`/`Noul`) eşiği düştüğünde devreye girecek `escalated_to_system2=True` kuralı, (5) doğrudan LLM içine gömmek yerine `MCP` aracı veya çalışma alanı sandbox'ına ayıracağın bir yetenek.
