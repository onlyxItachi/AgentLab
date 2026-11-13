# 02 — Ajan Mimarisi, Bağlam ve Bellek

[Ana sayfa](../../README.md) | [English](README.en.md)

**Süre:** Yaklaşık 90 dakika. Önkoşul, [birinci oturumdaki](../01-llm-fundamentals/README.md) model, token ve araç ayrımını hatırlamaktır.

Bu oturumda bir ders asistanını adım adım gözlemleyeceğiz. Model araç önerecek, harness bu öneriyi denetleyecek ve çalışan Python işlevinin sonucunu yeniden modele verecek. Aynı görev üzerinde bağlam seçimini, konuşma durumunu, bellek tercihlerini ve kaynak getirmeyi değiştireceğiz.

## Öğrenme hedefleri

- Modelin önerdiği eylem ile uygulamanın çalıştırdığı eylemi ayırmak.
- Agent loop, ReAct ve Plan-and-Solve yaklaşımlarını bir yürütme izi üzerinden açıklamak.
- Bağlama hangi bilgilerin girdiğini ve hangilerinin dışarıda kaldığını bulmak.
- Konuşma durumu, çalışma zamanı belleği ve kalıcı bellek arasındaki farkı göstermek.
- Retrieval, vektörle arama ve RAG akışını kaynaklarıyla değerlendirmek.

## Derste izleyeceğimiz akış

| Dakika | Konu / gözlem |
| --- | --- |
| 0-10 | Birinci günle bağlantı ve model / uygulama ayrımı |
| 10-25 | Harness, ajan döngüsü ve Deney A (`4F` / `A1`) |
| 25-40 | Context engineering ve Deney B (`B1`–`B3`) |
| 40-55 | State / memory ve Deney C (`C1`–`C4`) |
| 55-75 | Retrieval, vector search, RAG ve Deney D (`D1`–`D3`) |
| 75-87 | Küçük gruplarla alıştırma ve sonuç karşılaştırma |
| 87-90 | Anlayış kontrolü ve ders özeti |

## Materyaller

[Ders notları](ders-notlari.md) | [Oturum sözlüğü](kavram-sozlugu.md) | [Demolar](demos/README.md) | [Alıştırmalar](exercises/README.md)

Canlı demo yolu tek dosyadan oluşan, sözdizimi vurgulu ve hücre hücre modülerleştirilmiş [G4 Colab defteridir](demos/agent-core/AgentLab-Session02-G4.ipynb). Defteri GitHub'dan indirip (veya Drive kopyandan) Colab'da **Dosya → Not defteri yükle** ile aç ve çalışma zamanını **G4 / RTX PRO 6000 Blackwell** seç. Açılış hücreleri çalışma alanını ve GPU donanımını doğrular (`1A`–`1B`), pinli model ve CUDA kurulumunu yönetir (`2A`–`2C`), loopback sunucu istemcisini başlatır (`3A`–`3D`) ve ajan yapıtaşlarını (`4A`–`4F`) parça parça kurar; `1A` sonrası `4A`–`4F` çalıştırılarak GPU veya model indirmeden bile `ScriptedModel` önizlemesi alınabilir. Gemma 4 12B QAT ve eşleşen MTP assistant ile varsayılan context kapasitesi **262.144** tokendır (`3D`). Ders sonunda `9A` model durdurma ve `9B` VM sonlandırma adımlarını ayrı uygula; G4 erişimi ve CU tüketimi katılımcının hesabında ayrıca kontrol edilmelidir.

> **Colab Plan ve GPU Erişimi Notu:** **G4 (`RTX PRO 6000 Blackwell`)** hızlandırıcısı Google Colab'da yalnızca **Ultra** planda sunulmaktadır; **Colab Pro** hesapları çoğunlukla **A100** (veya L4), **Colab Plus / Ücretsiz** hesaplar ise en fazla **T4 (~15 GB VRAM)** erişimi alır. G4 erişiminiz yoksa (1) GPU veya indirme gerektirmeden önce `1A`, ardından `4A`–`4F` hücrelerini çalıştırarak deterministik `ScriptedModel` önizlemesini her ortamda çalıştırabilirsiniz; (2) canlı etkinlikte eğitmen tarafından paylaşıldıysa plana özel (`pro_...` A100 veya `plus_...` T4) ders defterini kullanabilirsiniz.

[Önceki: LLM Temelleri](../01-llm-fundamentals/README.md)
