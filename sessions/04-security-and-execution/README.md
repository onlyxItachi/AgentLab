# 04 — Ajan Güvenliği, Yürütme ve İnsan Denetimi

[Ana sayfa](../../README.md) | [English](README.en.md)

**Süre:** Yaklaşık 90 dakika. Önkoşullar için önceki günlerin tam tekrarı yerine aşağıdaki **5 dakikalık Gün 1–3 köprü özetini** oku; ayrıntılı geçmiş dersler ([01](../01-llm-fundamentals/README.md), [02](../02-agent-core-and-state/README.md), [03](../03-modern-agent-stack/README.md)) ders dışı başvuru içindir.

Bu oturumda artık yalnızca metin üreten veya salt okunur sözlük arayan değil, **gerçek Python ve Bash kodu çalıştırabilen** bir ajanı üretim güvenliği sınırlarıyla çevreliyoruz. İlk olarak girdi/çıktı **Guardrails** katmanını ve güvenilmeyen dosya/web/bilet içeriklerinden gelen **Prompt Injection** saldırılarını engelleyecek (`4.1`), ardından gerçek kod yürütmeyi **`Sandbox`** (`outside_workdir`, zaman aşımı, kaynak/ağ kısıtı) içine hapsedecek (`4.2`), en az yetkili **izin katmanları ve Trust Boundaries** ile **secret stripping** uygulayacak (`4.3`), riskli/yıkıcı eylemleri **`[Onayla]` / `[Reddet]`** düğmeli canlı **Human-in-the-Loop (HITL)** kapısında durduracak (`4.4`) ve uzun görevleri **Background Agents & Durable Execution** (`checkpoint` / `resume` + Google Drive kalıcılığı) ile kesintiye dayanıklı hâle getireceğiz (`4.5`).

> **Canlı ders öncesi öneri:** Başlamadan önce [ders notlarının başındaki 5 dakikalık Gün 1–3 köprü özetine](ders-notlari.md#5-dakikalık-gün-13-köprü-özeti) ve [oturum sözlüğündeki](kavram-sozlugu.md) temel terimlere hızlıca göz at.

## Öğrenme hedefleri

- `4.1` Girdi/çıktı **Guardrails** kurmak; doğrudan ve güvenilmeyen dosya, web sayfası veya destek bileti (`untrusted evidence, never instructions`) üzerinden gelen **dolaylı Prompt Injection** saldırılarını tespit edip durdurmak.
- `4.2` Gerçek Python/Bash çalıştırma ortamlarını (**Runtime**) dosya yolu izolasyonu (`outside_workdir`), dizin aşımı (`..`) engeli, zaman aşımı (`timeout`), bellek/CPU sınırları ve ağ kısıtlamalarıyla **Sandbox** içine almak.
- `4.3` **Trust Boundaries** ve en az yetki (**Least Privilege**) ilkesiyle `read`, `write` ve `exec` yetki katmanlarını `allow`/`deny` kurallarıyla ayırmak; API anahtarları ve ortam sırlarını **secret stripping** ile model bağlamından ve çıktılardan temizlemek.
- `4.4` Yıkıcı veya dış etkili eylemlerden önce politika risk kapısı kurarak **Human-in-the-Loop (HITL)** duraklatması yapmak; canlı **`[Onayla]` / `[Reddet]`** düğmeleriyle kullanıcı müdahalesi sonrasında akışı güvenle sürdürmek veya iptal etmek.
- `4.5` Asenkron **Background Agents** ve **Durable Execution** için adım **checkpoint** kayıtları tutmak; hata, durdurma veya oturum kesintisi sonrasında **`resume`** durumunu Google Drive üzerinden geri yüklemek.

## Derste izleyeceğimiz akış

| Dakika | Konu / gözlem |
| --- | --- |
| 0-5 | **5 Dakikalık Gün 1–3 Köprü Özeti** (4 önkoşul) ve tek tuş kurulum (`Hücre 1`) |
| 5-22 | `4.1` Girdi/çıktı **Guardrails**, doğrudan/dolaylı **Prompt Injection** ve **Deney 1** |
| 22-40 | `4.2` Korumasız vs **Sandbox** içinde gerçek Python/Bash yürütme, `outside_workdir` ve **Deney 2** |
| 40-56 | `4.3` **Trust Boundaries**, `read`/`write`/`exec` `allow`/`deny` kuralları ve **secret stripping** |
| 56-74 | `4.4` & `4.5` Canlı risk kapısı, **`[Onayla]` / `[Reddet]`** **HITL**, **Durable Execution** (`checkpoint`/`resume`) ve **Deney 3** |
| 74-87 | **Canlı Stüdyo** (`Hücre 5` portsuz WebUI, `💭 Thinking` + `🛡️ HITL` + `💻 Canlı Terminal`) ve küçük grup uygulaması |
| 87-90 | `2. Güvenli Kapanış` (`Hücre 6`), Drive kaydı, VM bırakma ve Oturum 05'e geçiş |

## Materyaller

[Ders notları](ders-notlari.md) | [Oturum sözlüğü](kavram-sozlugu.md) | [Demolar](demos/README.md) | [Alıştırmalar](exercises/README.md)

## 7 Hücreli Tek-Tuş `#@title` Form Mimarisi ve Donanım Katmanları

Bu oturumda öğrencilerden hücre içinde `True`/`False` bayrağı avlamaları istenmez. Colab defterleri **1 Markdown giriş hücresi + 6 gizli kodlu `#@title` form hücresi (`cellView: "form"`)** ile tasarlanmıştır; her adımda yalnızca başlık ve **`▶`** çalıştırma düğmesi görünür:

1. **Hücre 0 (Giriş Markdown):** Gün 1–3 köprü özeti, donanım katmanı seçimi ve hızlı başlangıç.
2. **Hücre 1 — `1. Tek Tuş Kurulum ve Model Motor Başlatma`:** Bağlı GPU'yu sıkı katman doğrulamasıyla kontrol eder (`G4` yalnızca RTX PRO 6000 Blackwell kabul eder, aksi durumda `ALAB-E02` verir), kişi-agnostik **`MyDrive/AgentLab-Agent-Runtime`** (`setup` paylaşımlı + `day-04-security-execution` gün durumu) önbelleğini bağlar ve pinli `llama.cpp v1.0.0` (`b12359`, `timeout=None`, `id_slot=0`, `max_tokens=262144`) üzerinde G4 katmanında **`Qwen 3.8 27B + MTP`** (`reasoning_effort="xhigh"`, `enable_thinking=True`, `1.0/0.95/20`, hedef+taslak `f8_e4m3` FP8 KV, `--ctx-size 1048576 --parallel 4 --kv-unified --kv-unified-per-slot 262144 --ctx-checkpoints 8 --cache-reuse 0 --cache-ram 8192`, `draft_max=3`, `262.144` aktif bağlam / `1.048.576` GPU KV havuzu), L4/T4 katmanlarında **`Gemma 4 12B QAT + MTP`** (ikili `--reasoning on --reasoning-budget -1 --reasoning-preserve`, `enable_thinking=True`, `preserve_thinking=True`, `1.0/0.95/64`, `f8_e4m3` FP8 KV) sunucusunu streaming SSE ile başlatır.
3. **Hücre 2 — `Deney 1`:** Girdi/çıktı **Guardrails** ve doğrudan/dolaylı **Prompt Injection** savunması (`4.1`).
4. **Hücre 3 — `Deney 2`:** Korumasız çalışma vs **`Sandbox`** içinde gerçek Python ve Bash yürütme (`4.2` & `4.3` — `outside_workdir`, zaman aşımı, kaynak/ağ sınırı, secret stripping).
5. **Hücre 4 — `Deney 3`:** **Trust Boundaries**, canlı politika risk kapısı + **`[Onayla]` / `[Reddet]`** **HITL** duraklatma/devam ve **Durable Execution** `checkpoint`/`resume` (`4.3`–`4.5`).
6. **Hücre 5 — `Canlı Stüdyo`:** Portsuz ve üçüncü taraf çerezsiz yerel Colab WebSocket WebUI (`google.colab.output.register_callback` + `google.colab.kernel.invokeFunction`). Üst çubukta **`Tam Ekran`** (`ESC` ile küçülür), **`Durdur`** ve **`Arayüzü Kapat` (Kill Switch)** düğmeleri; sohbette tıklanabilir **`💭 Düşünce Akışı`** CoT bulutu, Antigravity tarzı **FIFO istem sırası** (`[✅ Onayla]`/`[🛑 Reddet]` HITL beklerken veya akış sürerken yeni istemler sıraya alınır, `[✕ Sıradan Çıkar]`), **`🔧 Araç & Komut`**, **`🛡️ HITL Onay/Red`** ve **`💻 Canlı Terminal`** kartları yer alır (ayrı terminal CLI kurulumu gerekmez, kaldırılmıştır).
7. **Hücre 6 — `2. Güvenli Kapanış, Drive Kaydı ve GPU Bırakma`:** Açık WebUI görevini, oturum/checkpoint kayıtlarını (`drive.flush_and_unmount()`), `llama-server` sürecini ve Colab VM'ini (`unassign`) tek tıkla kapatır.

> **Colab Plan ve Donanım Dizilimi (`G4` / `L4` / `T4` — Sıkı Fail-Closed `ALAB-E02`):** Oturum 04'te `G4`, `L4` ve `T4` katmanları desteklenir (uyuşmayan donanımda sessiz fallback yok, doğrudan `ALAB-E02` verir):
> - **[AgentLab-Session04-G4.ipynb](demos/security-and-execution/AgentLab-Session04-G4.ipynb)** — Colab **Ultra** ve **Pro** (`RTX PRO 6000 Blackwell`, `Qwen 3.8 27B + MTP`, `Thinking: xhigh`, hedef+taslak `f8_e4m3` FP8 KV, `1M` / `1.048.576` GPU KV + `8 GiB` RAM, `262.144` aktif bağlam, `draft_max=3`)
> - **[pro_AgentLab-Session04-L4.ipynb](demos/security-and-execution/pro_AgentLab-Session04-L4.ipynb)** — Colab **Pro / Plus** (`NVIDIA L4`, `23 GB VRAM`, `512K` / `524.288` GPU KV + `8 GiB` RAM önbelleği)
> - **[plus_AgentLab-Session04-T4.ipynb](demos/security-and-execution/plus_AgentLab-Session04-T4.ipynb)** — Colab **Plus / Ücretsiz** (`Tesla T4`, `15 GB VRAM`, fallback `512K` / `524.288` GPU KV + `3 GiB` RAM önbelleği)

> **Sabit 2 Satırlık `ALAB-Exx` Hata Zırhı:** Defterdeki tüm hücreler ham Python `Traceback` yerine `🚨 [HATA KODU: ALAB-Exx] <Durum açıklaması>` ve `İlgili dosyanın hata koduna bakın! Ve çözemezseniz yardım isteyin!` biçiminde 2 satırlık tanı kutusu gösterir. Her kodun adım adım çözümü Google Drive klasöründeki `hata-cozum-rehberi.pdf` (TR) ve `error-guide.pdf` (EN) belgelerinde yer alır.

Yazdırılabilir çalışma kitapçıkları (`oturum-04.pdf` / `session-04.pdf`) ve `ALAB-Exx` hata çözüm rehberleri (`hata-cozum-rehberi.pdf` / `error-guide.pdf`) canlı oturum Google Drive klasörü üzerinden paylaşılır.

[Önceki: Modern Ajan Sistemleri](../03-modern-agent-stack/README.md) | [Ana sayfa](../../README.md)
