# Oturum sözlüğü: Ajan Güvenliği, Yürütme ve İnsan Denetimi

[Oturuma dön](README.md) | [English](glossary.md) | [Genel sözlük](../../docs/tr/kavram-sozlugu.md)

> **Canlı ders öncesi 5 dakikalık ön okuma:** Dersten önce bu terimlere hızlıca göz atman yeterlidir. Bu oturumda G4 üzerinde `Qwen 3.8 27B + MTP` (`Thinking: xhigh`), L4/T4 üzerinde `Gemma 4 12B QAT + MTP` (`--reasoning on`) modelini gerçek Python/Bash yürütme yetkisiyle çalıştırırken onu çevreleyen güvenlik korkuluklarını (**Guardrails**), kum havuzunu (**Sandbox**), yetki sınırlarını (**Trust Boundaries**), canlı insan onayını (**HITL**) ve kesintiye dayanıklı yürütmeyi (**Durable Execution**) tanıyacağız.

| Terim | Bu oturumdaki anlamı ve dersteki rolü |
| --- | --- |
| `Guardrail` | Model çağrısı öncesinde (girdi) veya yanıt/eylem öncesinde (çıktı) çalışan deterministik güvenlik ve doğrulama katmanı (`Deney 1`, `4.1`). |
| `Input guardrail` | Aşırı uzunluk, geçersiz şema, yasaklı kalıp veya açık saldırı ifadelerini LLM'e ulaşmadan durduran ön denetim (`4.1`). |
| `Output guardrail` | Model çıktısını kullanıcıya veya yürütücüye vermeden önce sızmış sırları temizleyen, yetkisiz araç önerilerini ve desteksiz iddiaları kesen son denetim (`4.1`). |
| `Prompt injection` | Modelin sistem yönergesini veya uygulama kurallarını bozup yetkisiz işlem yaptırmaya çalışan kötü niyetli talimat enjeksiyonu (`Deney 1`, `4.1`). |
| `Indirect prompt injection` | Doğrudan kullanıcı sohbetinde değil; ajanın okuduğu güvenilmeyen dosya, web sayfası veya destek bileti içine gizlenmiş saldırı talimatı (`Deney 1`, `4.1`). |
| `Untrusted evidence` | Dış kaynaklardan (dosya, web, bilet) gelen verinin asla yürütülebilir komut sayılmaması; `"untrusted evidence, never instructions"` etiketiyle izole edilmesi (`4.1`). |
| `Runtime` | Ajanın önerdiği Python kodu veya Bash kabuk komutlarının fiilen çalıştırıldığı yürütme ortamı (`Deney 2`, `4.2`). |
| `Sandbox` | Kod ve komut çalıştırmayı yalnızca izinli geçici klasör, süre, bellek/CPU ve ağ sınırları içine hapseden izole yürütme kutusu (`Deney 2`, `4.2`). |
| `outside_workdir` | Çalışma dizini dışına (`../`, mutlak yol veya sembolik bağlantı ile) çıkmaya çalışan dosya/komut erişimlerinin Sandbox tarafından engellenmesi (`Deney 2`, `ALAB-E08`). |
| `Execution timeout` | Sonsuz döngüye giren veya kilitlenen bir Python/Bash alt sürecini belirlenen saniye sonunda zorla durduran süre sınırı (`Deney 2`, `ALAB-E08`). |
| `Resource & network limits` | Alt sürecin bellek/CPU tüketimini sınırlayan ve `127.0.0.1` yerel inference dışında harici ağ çıkışını kapatan koruma (`4.2`). |
| `Trust boundary` | Güvenilmeyen veri/model çıktısı, güvenilen politika kapısı (harness) ve ayrıcalıklı işletim sistemi katmanı arasındaki kesin ayrım çizgisi (`4.3`). |
| `Least privilege` | Bir ajana veya alt sürece yalnızca görevini tamamlamak için gereken en dar `read`, `write` veya `exec` yetkisinin verilmesi (`4.3`). |
| `Permission tiers (read / write / exec)` | Salt okunur inceleme (`read`), dosya değiştirme (`write`) ve komut çalıştırma (`exec`) yetkilerinin ayrı risk düzeyleriyle yönetilmesi (`4.3`). |
| `Allow / deny rules` | Politika motorunun hangi yolları, komut kalıplarını ve araçları açıkça izinli (`allow`) veya yasaklı (`deny`) saydığını belirleyen kural listesi (`4.3`). |
| `Secret stripping` | `AGENTLAB_LLAMA_KEY` gibi API anahtarlarını ve ortam sırlarını alt süreç (`subprocess`) ortamından, terminal çıktılarından ve Drive yedeklerinden temizleme işlemi (`Deney 2`–`3`, `4.3`). |
| `Risk gate` | Önerilen eylemin risk düzeyini (düşük riskli otomatik çalışma vs yüksek riskli yıkıcı/dış etki) değerlendiren politika sınıflandırıcısı (`Deney 3`, `4.4`). |
| `Human-in-the-Loop (HITL)` | Yüksek riskli, geri alınamaz veya dış etkili işlemlerden önce yürütmeyi duraklatıp insan denetimi ve açık onay isteyen mekanizma (`Deney 3`, `4.4`). |
| `[Onayla] / [Reddet]` | HITL duraklatması sırasında kullanıcıya sunulan etkileşimli onay veya iptal düğmeleri; karar öncesinde `Thinking` ve önerilen komut incelenir (`Deney 3`, `Canlı Stüdyo`). |
| `Pause-and-resume` | Riskli bir adımda ajanı beklemeye alıp (`pause`), kullanıcı `[Onayla]` verdiğinde kaldığı bağlamdan devam ettirme (`resume`) akışı (`4.4`–`4.5`). |
| `Background agent` | Kullanıcının tek bir eşzamanlı bekleme penceresine kilitlenmeden arka planda uzun adımlar veya onay beklemeli görevler yürüten ajan yapısı (`4.5`). |
| `Durable execution` | Ağ kopması, sekme kapanması veya HITL beklemesi gibi kesintilere rağmen görevi kaybetmeden sürdürebilen yürütme mimarisi (`Deney 3`, `4.5`). |
| `Checkpoint & resume` | Her kritik adım veya HITL duraklatması öncesi oturum durumunu (`checkpoint_id`) diske kaydedip kesinti sonrasında baştan değil kaldığı yerden (`resume`) devam etme (`Deney 3`, `4.5`). |
| `ExperimentSession` | `Deney 1`, `Deney 2` ve `Deney 3` hücrelerinin birbirinden bağımsız, temiz klasör ve bağlamla çalışmasını sağlayan oturum izolasyon yapısı. |
| `MyDrive/AgentLab-Agent-Runtime` | Günler arası ortak `setup` (`Qwen 3.8 27B` / `Gemma 4` + `llama.cpp`) ile Gün 4'e özel `day-04-security-execution` checkpoint ve oturum dosyalarını ayıran Drive klasör düzeni (`Hücre 1`, `Hücre 6`). |
| `Thinking Modu (G4 xhigh / L4-T4 --reasoning on)` | `llama.cpp v1.0.0 b12359` sunucusunda (`max_tokens=262144`, `timeout=None`) G4 için `Qwen 3.8 27B + MTP` `reasoning_effort="xhigh"` (`1.0/0.95/20`), L4/T4 için `Gemma 4 12B + MTP` ikili `--reasoning on --reasoning-budget -1 --reasoning-preserve` (`1.0/0.95/64`) düşünme yapılandırması. |
| `Canlı Stüdyo (Portsuz WebUI)` | `Hücre 5` içinde üçüncü taraf çerez/port tüneli olmadan doğrudan yerel Colab WebSocket (`register_callback` / `invokeFunction`) ile açılan; `Tam Ekran` (`ESC`), `Durdur`, `Arayüzü Kapat` (Kill Switch), tıklanabilir `💭 Düşünce Akışı` CoT bulutu, **FIFO istem sırası** (`[✕ Sıradan Çıkar]`), `🔧 Araç & Komut`, `🛡️ HITL` ve `💻 Terminal` kartları sunan arayüz. |
| `Kill Switch (Arayüzü Kapat)` | `Canlı Stüdyo` WebUI arka plan görevini anında kapatan acil durdurma düğmesi; yeniden açmak için `Hücre 5` tekrar çalıştırılır (`ALAB-E07`). |
| `ALAB-Exx Hata Zırhı` | Ham Python `Traceback` yerine `🚨 [HATA KODU: ALAB-Exx] <Durum açıklaması>` ve sabit 2. satırla gösterilen tanı kutusu (`ALAB-E01`–`ALAB-E99`); çözüm için `hata-cozum-rehberi.pdf` kullanılır. |
