# Alıştırmalar: Modern Ajan Sistemleri

[Oturuma dön](../README.md) | [English](README.en.md) | [Demo rehberi](../demos/README.md)

Her alıştırmada girdiyi, seçilen yolu, araç izini ve gözlemi kaydet. `4F` (`ScriptedModel`) çevrimdışı önizlemesi ile `A1`–`E5` canlı model deneylerini (`AgentLab-Session03-G4.ipynb` veya plana özel `pro_AgentLab-Session03-A100.ipynb` / `plus_AgentLab-Session03-T4.ipynb` üzerinde) etiketleyerek ayır.

## 1. MCP keşfi ve Progressive Disclosure (`4F` ve `A1`–`A2`)

- `A1`: `4F` hücresindeki `ScriptedModel` önizlemesi ile `A1` hücresindeki canlı `InProcessMCPServer` çalışmasını karşılaştır. `tools/list` yanıtında `campus_kb`, `ops_desk` ve `media_world` altından keşfedilen araç adlarını (`mcp__<plugin>__<tool>`) kaydet ve `doc_id="olmayan-belge"` çağrısının neden fail-closed reddedildiğini yaz.
- `A2`: `Plugin` (çalıştırılabilir araç) ile `Skill` (`SKILL_LIBRARY` prosedür yönergesi) ayrımını göster. `incident-triage` skill'i seçildiğinde `catalog_chars`, `loaded_chars` ve `saved_chars` değerlerinin nasıl değiştiğini ve bunun `tools/call` davranışına etkisini açıkla.

## 2. Deterministik kapı mı, hibrit akış mı? (`B1`–`B2`)

- `B1`: `TR-204` bilet durumu ve CU bütçe hesabı sorularında `deterministic_gate` mekanizmasının nasıl `0` token ve `0` LLM çağrısı ile sonuca gittiğini yaz; çoklu belge sentezi gerektiren bir soruda ise neden model katmanına geçildiğini karşılaştır.
- `B2`: Kullanıcının serbest metin olarak girdiği laboratuvar talebinde modelin yalnızca parametre çıkarımı yaptığını, slot doğrulaması, `dry_run` / `allow_write` izni ve sayısal kontrollerin neden Python katmanında kaldığını açıkla.

## 3. En az yetkili uzman, StructuredHandoff ve güven sınırı (`C1`–`C3`)

- `C1`: `research_specialist`, `operations_specialist` ve `simulation_specialist` ajanlarının `allowed_plugins` kapsamlarını karşılaştır; birinin diğerinin MCP araçlarını neden göremediğini belirt.
- `C2`: Bağlam kaybeden (`lossy=True`) devir ile şemalı `StructuredHandoff` (`lossy=False`) arasında `"T4"` ve `"14:00"` kısıtlarının nasıl taşındığını kontrol et.
- `C3`: `CAMPUS_DOCS` içindeki `untrusted-ticket` belgesinde yer alan `admin_agent` handoff komutunun `"untrusted evidence, never instructions"` etiketi ve `validate_handoff` ile nasıl engellendiğini yaz; `max_handoffs=2` sınırının yakaladığı riski açıkla.

## 4. System 1 vs System 2, `1M+` KV havuzu, modal kademe, `Agentic CLI` ve Web Sohbet (`D1`–`D3`, `E1`–`E5`, `8A`)

- `D1`: `Jev` ve açık ağırlıklı ~100M Apache-2.0 `Laya` karar modellerinin T4-uyumlu mockup'ı olan `System1DecisionGate` (`Choice` / `Score` / `Noul`, `0` üretim tokenı) ile `llama.cpp v1.0.0` (`b12359`), `1.0/0.95/64` örnekleme ve hedef+taslak `f8_e4m3` FP8 KV önbellekli (`-ctkd/-ctvd`, `p_min=0.75`, `262.144` maks aktif bağlam, `1.048.576` toplam KV havuzu; canlı G4 `1M` GPU KV `21.279 / 97.887 MiB` VRAM, `235,35 tok/s`, `%80,11` MTP; önceki `temp=0` canlı T4 GPU içi `524.288` `512K` KV temel ölçümünde `14.047 MiB` VRAM, `cached_tokens=182`, `41,69 tok/s` decode) doğal multimodal `Gemma 4 12B + MTP` (System 2) modelinin gecikme, önbellek (`cached_tokens`) ve sözdizimi güvenliği farklarını kaydet.
- `D2`: `Deterministic -> System 1 Reflex -> Gemma 4 12B + MTP` kademesinde hangi isteğin `direct_system1` olarak çözüldüğünü, hangisinin `campus_kb`, `ops_desk` veya T4-uyumlu mockup `media_world` (`simulate_lab_capacity` / `generate_architecture_diagram`; `Qwen-Image` gibi ağır medya üretimi G4/yerel ajanlara ayrılır) araçlarına yönlendiğini göster.
- `D3`: `noul_confidence < 0.75` olduğunda veya yönlendirici yükü bozuk geldiğinde orkestratörün nasıl `escalated_to_system2=True` ile güvenli eskalasyon yaptığını doğrula.
- `E1`–`E2` *(isteğe bağlı)*: `/tmp/agentlab-s03-py314` altındaki `uv 0.13.8` + izole CPython `3.14` + `mistral-vibe 3.1.2` (`1.0/0.95/64`, varsa `1C`/`8C` çoklu gün `MyDrive/AgentLab-Agent-Runtime` altında ortak `setup` önbelleğinden `py314-vibe-env.tar.gz`) ortamında `AGENTS.md` ve `SKILL.md` kurallarıyla çalışan gerçek CLI ajanının `quota_calc.py` hatasını nasıl düzeltip `audit_summary.json` (`total_cu: 159.84`) ürettiğini ve `outside_workdir="deny"` sınırının neden kritik olduğunu incele.
- `E3`–`E5` *(isteğe bağlı)*: `DualLayerSessionStore` (`transcript.md`, `input_cache`/`output_tokens` JSONL ve `slot0.kv.bin`) içinde binary KV geri yükleme (`binary_kv_hit`) başarısız olduğunda sistemin nasıl otomatik olarak `text_replay_fallback` moduna geçtiğini (`E3`) ve `AgentWebServer` (`X-AgentLab-Token`) ile Python Harness kontrollü Colab Web Sohbet Çerçevesinin (`E4`–`E5`) saf `llamaUI` yerine neden tercih edildiğini açıkla.

## 5. Kendi modern ajan mimarin

Kendi çalışma alanın için küçük bir görev akışı seç ve beş karar öner: (1) iki ayrı `Plugin` arasında en az yetkili MCP kapsam sınırı, (2) `deterministic_gate` ile `0` tokenda çözülecek bir kural, (3) `StructuredHandoff` içinde mutlaka korunacak bir `constraints` alanı, (4) `System 1` (`Jev`/`Laya`: `Choice`/`Score`/`Noul`) eşiği düştüğünde devreye girecek `escalated_to_system2=True` kuralı, (5) doğrudan LLM içine gömmek yerine `MCP` aracı veya izole `Agentic CLI` (`mistral-vibe` / `hermes-agent`) katmanına ayıracağın bir yetenek.
