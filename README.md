# AgentLab

**Dil:** Türkçe | [English](README.en.md)

AgentLab, ajan odaklı yapay zekâ (Agentic AI) kavramlarını uygulamalı oturumlarla, açıklamalar ve etkileşimli Colab defterleriyle ele alan eğitim deposudur. Yeni başlayanlar da hedef kitlededir.

> İlk iki oturumun ders notları, sözlükleri, kavramsal alıştırmaları ve bağımsız Google Colab defterleri burada sunulur. Sonraki oturumların materyalleri hazırlandıkça eklenecektir.

## Oturumlar

1. [LLM Temelleri](sessions/01-llm-fundamentals/README.md)
2. [Ajan Mimarisi, Bağlam ve Bellek](sessions/02-agent-core-and-state/README.md)

## Başlangıç

- [Genel kavram sözlüğü](docs/tr/kavram-sozlugu.md)
- [Birinci oturum Colab deney alanı](sessions/01-llm-fundamentals/demos/llm-playground/README.md)
- [İkinci oturum G4 Colab demoları](sessions/02-agent-core-and-state/demos/README.md)

Her iki oturum da Python veya yerel ortam kurmadan Google Colab üzerinden çalıştırılabilir. Birinci oturumun [Colab defteri](sessions/01-llm-fundamentals/demos/llm-playground/AgentLab-Colab.ipynb), Qwen3.5-0.8B ile token, sonraki token olasılıkları, örnekleme ve araç çağrısı adımlarını gözlemletir. İkinci oturumun bağımsız [G4 Colab defteri](sessions/02-agent-core-and-state/demos/agent-core/AgentLab-Session02-G4.ipynb), modelsiz `ScriptedModel` önizlemesinin ardından Google'ın Gemma 4 12B QAT modeli, eşleşen MTP assistant ve pinli llama.cpp CUDA çalışma zamanıyla 262.144 varsayılan context kapasitesi üzerinde harness, bağlam, bellek ve RAG deneyleri sağlar. Model indirmeleri ve VM sonlandırma adımları defterde açık onay gerektirir.
