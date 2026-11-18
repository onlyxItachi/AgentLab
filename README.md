# AgentLab

**Dil:** Türkçe | [English](README.en.md)

AgentLab, ajan odaklı yapay zekâ (Agentic AI) kavramlarını uygulamalı oturumlarla, açıklamalar ve etkileşimli Colab defterleriyle ele alan eğitim deposudur. Yeni başlayanlar da hedef kitlededir.

> İlk üç oturumun ders notları, sözlükleri, kavramsal alıştırmaları ve bağımsız Google Colab defterleri burada sunulur. Sonraki oturumların materyalleri hazırlandıkça eklenecektir.

## Oturumlar

1. [LLM Temelleri](sessions/01-llm-fundamentals/README.md)
2. [Ajan Mimarisi, Bağlam ve Bellek](sessions/02-agent-core-and-state/README.md)
3. [Modern Ajan Sistemleri](sessions/03-modern-agent-stack/README.md)

## Başlangıç

- [Genel kavram sözlüğü](docs/tr/kavram-sozlugu.md)
- [Birinci oturum Colab deney alanı](sessions/01-llm-fundamentals/demos/llm-playground/README.md)
- [İkinci oturum G4 Colab demoları](sessions/02-agent-core-and-state/demos/README.md)
- [Üçüncü oturum G4 Colab demoları](sessions/03-modern-agent-stack/demos/README.md)

Her üç oturum da Python veya yerel ortam kurmadan Google Colab üzerinden çalıştırılabilir. Birinci oturumun [Colab defteri](sessions/01-llm-fundamentals/demos/llm-playground/AgentLab-Colab.ipynb), Qwen3.5-0.8B ile token, sonraki token olasılıkları, örnekleme ve araç çağrısı adımlarını gözlemletir. İkinci oturumun bağımsız [G4 Colab defteri](sessions/02-agent-core-and-state/demos/agent-core/AgentLab-Session02-G4.ipynb), modelsiz `ScriptedModel` önizlemesinin ardından Google'ın Gemma 4 12B QAT modeli, eşleşen MTP assistant ve pinli llama.cpp CUDA çalışma zamanıyla 262.144 varsayılan context kapasitesi üzerinde harness, bağlam, bellek ve RAG deneyleri sağlar. Üçüncü oturumun 51 hücrelik bağımsız [G4 Colab defteri](sessions/03-modern-agent-stack/demos/modern-agent-stack/AgentLab-Session03-G4.ipynb) (ve canlı etkinlikte Google Drive üzerinden paylaşılan plana özel `pro_AgentLab-Session03-A100.ipynb` ile `plus_AgentLab-Session03-T4.ipynb` defterleri) ise `ScriptedModel` önizlemesiyle (`1A` ve `4A`–`4F`) başlayıp tek pinli doğal multimodal `Gemma 4 12B QAT + MTP` çalışma zamanını (`GpuMtpRuntime`, ~`7,699 GiB`, **`llama.cpp v1.0.0` (`b12359`)**) Google'ın resmi Gemma 4 örneklemesi (`temperature=1.0`, `top_p=0.95`, `top_k=64`), **`f8_e4m3` FP8 hedef + taslak (`-ctkd/-ctvd`) KV önbelleği**, **`--spec-draft-p-min 0.75`** (`--spec-draft-n-max`: T4 `2`, L4/A100/G4 `3`), açık prompt önbelleği (`--cache-ram`, `--ctx-checkpoints 8`, `--cache-reuse 64`, `cache_prompt=True`), **`1.048.576` (`1M+`) toplam KV havuzu**, **`262.144` (`256K`) maksimum aktif model bağlamı** ve çoklu gün Drive omurgasıyla (`1C`/`8C`, `MyDrive/AgentLab-Agent-Runtime` altında ortak `setup` + gün bazlı `day-03-modern-stack`) çalıştırır (canlı G4 `RTX PRO 6000 Blackwell` @ `1M` GPU KV doğrulamasında `21.279 / 97.887 MiB` VRAM, **`235,35 tok/s` decode** ve **`%80,11` MTP**; önceki `b12359` canlı `Tesla T4` `temp=0` temel ölçümünde GPU içi **`524.288` (`512K` = `2 × 262.144`)** KV havuzu `14.047 MiB` VRAM / `866 MiB` boş pay, `cached_tokens=182`, `324,07 tok/s` prefill ve **`41,69 tok/s` decode** ile doğrulandı). Bu altyapı üzerinde `MCP` (`campus_kb`, `ops_desk`, `media_world`), `Skill` progressive disclosure, deterministik kural kapısı, çoklu ajan `StructuredHandoff`, `System 1` karar ilkelleri (`Jev` ve açık ağırlıklı ~100M Apache-2.0 `Laya`: T4-uyumlu `Choice`/`Score`/`Noul` mockup'ı), `World Model` / `media_world` kademesi, isteğe bağlı **`uv 0.13.8` + izole CPython `3.14` + `mistral-vibe 3.1.2`** gerçek `Agentic CLI` (`E1`–`E2`) ve Python Harness kontrollü konuşulabilir Colab Web Sohbet Çerçevesi (`AgentWebServer`) + fallback-aware `DualLayerSessionStore` (`transcript.md`, `input_cache`/`output_tokens` JSONL, `slot0.kv.bin`) (`E3`–`E5`) deneylerini sunar. Model indirmeleri ve VM sonlandırma adımları defterlerde açık onay gerektirir.
