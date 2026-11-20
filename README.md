# AgentLab

**Dil:** Türkçe | [English](README.en.md)

AgentLab, ajan odaklı yapay zekâ (Agentic AI) kavramlarını uygulamalı oturumlarla, açıklamalar ve etkileşimli Colab defterleriyle ele alan eğitim deposudur. Yeni başlayanlar da hedef kitlededir.

> İlk dört oturumun ders notları, sözlükleri, kavramsal alıştırmaları ve bağımsız Google Colab defterleri burada sunulur. Sonraki oturumların materyalleri hazırlandıkça eklenecektir.

## Oturumlar

1. [LLM Temelleri](sessions/01-llm-fundamentals/README.md)
2. [Ajan Mimarisi, Bağlam ve Bellek](sessions/02-agent-core-and-state/README.md)
3. [Modern Ajan Sistemleri](sessions/03-modern-agent-stack/README.md)
4. [Güvenlik ve Yürütme](sessions/04-security-and-execution/README.md)

## Başlangıç

- [Genel kavram sözlüğü](docs/tr/kavram-sozlugu.md)
- [Birinci oturum Colab deney alanı](sessions/01-llm-fundamentals/demos/llm-playground/README.md)
- [İkinci oturum G4 Colab demoları](sessions/02-agent-core-and-state/demos/README.md)
- [Üçüncü oturum G4 / L4 / T4 Colab demoları](sessions/03-modern-agent-stack/demos/README.md)
- [Dördüncü oturum G4 / L4 / T4 Colab demoları](sessions/04-security-and-execution/demos/README.md)

Her dört oturum da Python veya yerel ortam kurmadan Google Colab üzerinden çalıştırılabilir. Birinci oturumun [Colab defteri](sessions/01-llm-fundamentals/demos/llm-playground/AgentLab-Colab.ipynb), Qwen3.5-0.8B ile token, sonraki token olasılıkları, örnekleme ve araç çağrısı adımlarını gözlemletir. İkinci oturumun bağımsız [G4 Colab defteri](sessions/02-agent-core-and-state/demos/agent-core/AgentLab-Session02-G4.ipynb), modelsiz `ScriptedModel` önizlemesinin ardından Google'ın Gemma 4 12B QAT modeli, eşleşen MTP assistant ve pinli llama.cpp CUDA çalışma zamanıyla 262.144 varsayılan context kapasitesi üzerinde harness, bağlam, bellek ve RAG deneyleri sağlar. Üçüncü oturumun **7 hücreli `#@title` Studio v2** düzenindeki [G4 Colab defteri](sessions/03-modern-agent-stack/demos/modern-agent-stack/AgentLab-Session03-G4.ipynb) `Qwen 3.8 27B + MTP` (`Thinking` eforu `xhigh`, hedef+taslak `f8_e4m3` FP8 KV, `--ctx-size 1048576 --parallel 4 --kv-unified --kv-unified-per-slot 262144 --ctx-checkpoints 8 --cache-reuse 0 --cache-ram 8192`, `262.144` aktif bağlam / `1.048.576` GPU KV havuzu), aynı klasör ve Google Drive atölye setindeki [pro_AgentLab-Session03-L4.ipynb](sessions/03-modern-agent-stack/demos/modern-agent-stack/pro_AgentLab-Session03-L4.ipynb) ve [plus_AgentLab-Session03-T4.ipynb](sessions/03-modern-agent-stack/demos/modern-agent-stack/plus_AgentLab-Session03-T4.ipynb) defterleri ise doğal multimodal `Gemma 4 12B QAT + MTP` (`--reasoning on`, `f8_e4m3` FP8 KV, GPU içi `524.288` KV + RAM = `1.048.576` toplam KV havuzu, sıkı fail-closed `ALAB-E02` katman koruması ve `MyDrive/AgentLab-Agent-Runtime`) başlatır; sırasız çalışabilen `Deney 1`–`Deney 3` hücreleri (`MCP`, `StructuredHandoff`, `System1DecisionGate` / `Jev` & `Laya`, `DualLayerSessionStore`) ile harici port/çerez gerektirmeyen `google.colab.output` JS RPC **Canlı Stüdyo** WebUI (tıklanabilir `💭 Thinking` CoT bulutu ve Antigravity tarzı FIFO istem sırası) sunar. Dördüncü oturumun **7 hücreli `#@title` Studio v2** düzenindeki [G4 Colab defteri](sessions/04-security-and-execution/demos/security-and-execution/AgentLab-Session04-G4.ipynb) (`Qwen 3.8 27B + MTP` `xhigh`) ve aynı klasördeki [pro_AgentLab-Session04-L4.ipynb](sessions/04-security-and-execution/demos/security-and-execution/pro_AgentLab-Session04-L4.ipynb) ile [plus_AgentLab-Session04-T4.ipynb](sessions/04-security-and-execution/demos/security-and-execution/plus_AgentLab-Session04-T4.ipynb) (`Gemma 4 12B + MTP`) defterleri 5 dakikalık Gün 1–3 Köprü Özeti ile başlar; gerçek Python/Bash yürütmede **Guardrails**, **Prompt Injection** savunması, izole **Sandbox** (`outside_workdir` & timeout), **Trust Boundaries**, policy tabanlı canlı **`[Onayla]` / `[Reddet]` HITL** kapısı, **Durable Execution** (`checkpoint`/`resume`) ve sabit 2 satırlık **`ALAB-Exx`** hata zırhını tıklanabilir Thinking bulutu ve FIFO sıralı portsuz **Canlı Stüdyo** üzerinde gösterir.
