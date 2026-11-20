# Genel kavram sözlüğü

[Ana sayfa](../../README.md) | [English](../en/glossary.md)

Bu başlangıç sözlüğü, tüm eğitimin tamamlanmış bir referansı değildir. Oturuma özel sözlükler ilgili dersin sayfasında bulunur.

| Kavram | Kısa açıklama |
|---|---|
| LLM | Çok miktarda metinden öğrendiği örüntülerle, bağlama göre sonraki metin parçalarını tahmin ederek üretim yapan büyük dil modeli. |
| Token | Modelin işlediği metin birimi; her zaman tek bir kelimeye karşılık gelmez. |
| Embedding | Bir öğeyi sayılardan oluşan bir vektörle temsil etme biçimi. |
| API | Yazılımların belirlenmiş kurallarla birbirinden işlev veya veri istemesine yarayan arayüz. |
| Tool (araç) | Bir uygulamanın modele kontrollü kullanım için sunduğu işlev veya yetenek. |
| Schema (şema) | Bir verinin beklenen yapısını ve uygulanabilir kısıtlarını tarif eden tanım. |
| Agent loop | Modelin önerileri, araç sonuçları ve uygulamanın kontrol adımları arasında yinelenen süreç. |
| State (durum) | Bir uygulamanın mevcut işleyişte kullandığı, zamanla değişebilen bilgiler. |
| Guardrails | Bir sistemin model çağrısı öncesinde (girdi) ve yanıt/eylem öncesinde (çıktı) istenmeyen davranışları, şema ihlallerini veya sır sızıntılarını durdurmak için uyguladığı deterministik güvenlik kontrolleri. |
| Eval | Bir sistemin belirlenen ölçütlere göre sistematik olarak değerlendirilmesi. |
| MCP | Ajan uygulamalarının araçları ve veri kaynaklarını standart biçimde keşfedip çağırmasını sağlayan açık entegrasyon protokolü (Model Context Protocol). |
| Skill | Bir ajanın belirli bir iş akışını nasıl yürüteceğini tanımlayan, yalnızca gerektiğinde bağlama yüklenen prosedürel yönerge paketi. |
| Routing | Gelen bir isteğin kural kapısı, karar katmanı, küçük bir model veya uzman ajanlar arasından en uygun işleyiciye yönlendirilmesi. |
| Handoff | Bir görevin kontrolünün, hedef ve kısıtlarla birlikte bir ajandan veya bileşenden diğerine devredilmesi. |
| SLM | Düşük gecikme ve düşük kaynak maliyetiyle hızlı metin taslağı veya basit yanıtlar üreten küçük otoregresif dil modeli (Small Language Model). |
| System 1 decision model | Kapalı kaynak `Jev` ve açık ağırlıklı (~100M, Apache-2.0) `Laya` gibi, serbest metin tokenı üretmeden tek ileri geçişte tipli karar ilkelleri (`Choice`, `Score`, `Noul`) döndüren hızlı refleks karar modeli. |
| Multimodal LLM | Metnin yanında görsel, belge veya ses girdilerini doğrudan algılayıp araç çağırabilen model sınıfı (`Gemma 4 12B` doğal olarak multimodaldir). |
| World model | Bir eylem sonrasında fiziksel, uzamsal veya operasyonel ortam durumunun nasıl değişeceğini simüle eden uzman model veya motor. |
| Agentic CLI | Yerel `127.0.0.1` `llama-server`, `MCP` keşfi, `SKILL.md` / `AGENTS.md` progressive disclosure ve gerçek dosya/kabuk araçlarını terminalde birleştiren ajan koşumu. |
| KV cache & 1M+ prompt pool | `llama.cpp v1.0.0` üzerinde `f8_e4m3` (FP8) KV nicemleme, `--kv-unified` ortak yuva havuzu (T4/L4'te `524.288` `512K`, G4'te `1.048.576` GPU KV), `--cache-reuse` ve `--cache-ram` ile modelin `262.144` (`256K`) maksimum aktif bağlamını `1M+` toplam KV havuzuyla çalıştırma düzeni. |
| Prompt Injection | Modelin sistem kurallarını bozup yetkisiz işlem yaptırmaya çalışan kötü niyetli talimat enjeksiyonu; dosya, web veya bilet içinden gelen dolaylı saldırılar `"untrusted evidence, never instructions"` etiketiyle izole edilir. |
| Sandbox | Ajanın ürettiği gerçek Python ve Bash kodunu izole çalışma dizini (`outside_workdir` engeli), kesin zaman aşımı (`timeout`), bellek/CPU sınırları ve kapalı dış ağ politikası içine hapseden yürütme kutusu. |
| Trust Boundary | Güvenilmeyen girdi/model çıktısı, güvenilen politika kapısı (`harness`) ve ayrıcalıklı işletim sistemi katmanı arasındaki ayrım; en az yetki (`read`/`write`/`exec` `allow`/`deny`) ve `secret stripping` ile korunur. |
| Human-in-the-Loop (HITL) | Yüksek riskli, geri alınamaz veya dış etkili eylemlerden önce yürütmeyi duraklatıp kullanıcıya `Thinking` ve tam komutu göstererek `[Onayla]` / `[Reddet]` kararı sunan insan denetimi kapısı. |
| Durable Execution | Ağ kopması, sekme kapanması veya HITL beklemesi gibi kesintilere rağmen adım `checkpoint` kayıtları ve Google Drive kalıcılığıyla görevi `resume` edip sürdüren yürütme mimarisi. |
| Studio v2 | Oturum 03 ve 04 Colab defterlerindeki bayrak avlamasız **7 hücreli `#@title` form** arayüzü; tek tuş kurulum, bağımsız deneyler, portsuz `google.colab.output` JS RPC `Canlı Stüdyo`, `DualLayerSessionStore` ve güvenli kapanışı birleştirir. |
| ALAB-Exx | Defterlerde karmaşık Python `Traceback` çıktıları yerine gösterilen sabit 2 satırlık tanı kutusu (`ALAB-E01`–`ALAB-E99`); her kodun adım adım çözümü `hata-cozum-rehberi.pdf` içinde yer alır. |

Terimlerin kapsamı ileride ilgili oturumların materyalleriyle genişletilecektir.
