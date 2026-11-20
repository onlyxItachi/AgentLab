# Demolar: Ajan Güvenliği, Yürütme ve İnsan Denetimi

[Oturuma dön](../README.md) | [English](README.en.md) | [Ders notları](../ders-notlari.md) | [Sözlük](../kavram-sozlugu.md) | [Alıştırmalar](../exercises/README.md)

Oturum 04 canlı defterleri **1 Markdown giriş hücresi + 6 gizli kodlu `#@title` form hücresi (`cellView: "form"`)** ile çalışır. Katılımcılar Python kodunun içinde `True`/`False` bayrağı değiştirmez; her adımda yalnızca **`▶`** çalıştırma düğmesine basar.

> **Donanım Katmanı Eşleştirme (`G4` / `L4` / `T4` — Sıkı Fail-Closed `ALAB-E02`):**
> - **[AgentLab-Session04-G4.ipynb](security-and-execution/AgentLab-Session04-G4.ipynb)** — Colab **Ultra / Pro** (`RTX PRO 6000 Blackwell`, `Qwen 3.8 27B + MTP`, `Thinking: xhigh`, hedef+taslak `f8_e4m3` FP8 KV, `1M` / `1.048.576` GPU KV + `8 GiB` RAM, `262.144` aktif bağlam, `draft_max=3`; L4/T4'te `ALAB-E02` verir)
> - **[pro_AgentLab-Session04-L4.ipynb](security-and-execution/pro_AgentLab-Session04-L4.ipynb)** — Colab **Pro / Plus** (`NVIDIA L4`, `Gemma 4 12B QAT + MTP`, `--reasoning on`, `512K` / `524.288` GPU KV + `8 GiB` RAM önbelleği)
> - **[plus_AgentLab-Session04-T4.ipynb](security-and-execution/plus_AgentLab-Session04-T4.ipynb)** — Colab **Plus / Ücretsiz** (`Tesla T4`, `Gemma 4 12B QAT + MTP`, `--reasoning on`, `512K` / `524.288` GPU KV + `3 GiB` RAM önbelleği)
>
> Bağlı GPU türü ile defter katmanı uyuşmazsa sistem sessiz fallback yapmaz; doğrudan `ALAB-E02` kodlu 2 satırlık uyarı gösterir.

## 7 Hücreli Form Mimarisi

| Hücre | `#@title` Başlığı / Rolü | Ekranda Gözlenecek Çıktı |
| --- | --- | --- |
| **Hücre 0** | Giriş Markdown kartı | 5 dakikalık Gün 1–3 köprü özeti ve defter katmanı notu (`G4` / `L4` / `T4`) |
| **Hücre 1** | `1. Tek Tuş Kurulum ve Model Motor Başlatma` | Adım adım emojili ilerleme (`🔍 GPU doğrulanıyor...`, `📂 Drive önbelleği bağlanıyor...`, `🧠 Model GPU'ya yükleniyor...`, `🩺 Canlı çıkarım testi yapılıyor...`) ve saniyeli `<Qwen 3.8 27B | Gemma 4> servinge hazır!` mesajı |
| **Hücre 2** | `Deney 1` — Guardrails ve Prompt Injection (`4.1`) | Girdi/çıktı guardrail denetimleri, doğrudan enjeksiyon ve güvenilmeyen dosya/web/bilet dolaylı enjeksiyon engeli (`untrusted evidence, never instructions`) |
| **Hücre 3** | `Deney 2` — Korumasız vs Sandbox Yürütme (`4.2` & `4.3`) | Gerçek Python ve Bash çalıştırma, `outside_workdir` dizin aşımı engeli, `timeout`, kaynak/ağ kısıtlaması ve secret stripping |
| **Hücre 4** | `Deney 3` — Trust Boundaries, Canlı HITL & Durable Execution (`4.3`–`4.5`) | `read`/`write`/`exec` katmanları, risk kapısı, etkileşimli **`[Onayla]` / `[Reddet]`** duraklatma-devam düğmeleri, `checkpoint`/`resume` ve Drive state |
| **Hücre 5** | `Canlı Stüdyo` — Portsuz, Çerezsiz Colab WebUI | `Tam Ekran` (`ESC`), `Durdur`, `Arayüzü Kapat` (Kill Switch) çubuğu + tıklanabilir **`💭 Düşünce Akışı`** CoT bulutu, **FIFO istem sırası** (`[✕ Sıradan Çıkar]`), **`🔧 Araç & Komut`**, **`🛡️ HITL Onay/Red`**, **`💻 Canlı Terminal`** kartları (ayrı CLI gerekmez) |
| **Hücre 6** | `2. Güvenli Kapanış, Drive Kaydı ve GPU Bırakma` | WebUI arka plan görevini, `MyDrive/AgentLab-Agent-Runtime/day-04-security-execution` yedeğini (`drive.flush_and_unmount()`), `llama-server` sürecini ve VM'i (`unassign`) kapatır |

## Çalışma zamanı yapılandırması (Hücre 1)

- **Katmana özel altyapı (`llama.cpp v1.0.0 b12359`):** **G4** katmanında `Qwen 3.8 27B + MTP` (`f8_e4m3` FP8 hedef+taslak KV, `--ctx-size 1048576 --parallel 4 --kv-unified --kv-unified-per-slot 262144 --ctx-checkpoints 8 --cache-reuse 0 --cache-ram 8192`, `draft_max=3`, `262.144` aktif bağlam / `1.048.576` GPU KV havuzu); **L4/T4** katmanlarında `Gemma 4 12B QAT + MTP` (`f8_e4m3` FP8 KV), Drive'da kişi-agnostik **`MyDrive/AgentLab-Agent-Runtime`** (`setup` günler arası ortak + `day-04-security-execution` oturum durumu).
- **Thinking modu ve örnekleme:** G4 (`Qwen 3.8 27B`) için `enable_thinking=True` + `reasoning_effort="xhigh"` (`temperature=1.0`, `top_p=0.95`, `top_k=20`); L4/T4 (`Gemma 4 12B`) için ikili `--reasoning on --reasoning-budget -1 --reasoning-preserve`, `enable_thinking=True`, `preserve_thinking=True` ve resmi örnekleme (`temperature=1.0`, `top_p=0.95`, `top_k=64`); streaming SSE, `id_slot=0`, `max_tokens=262144` ve `timeout=None`.
- **Tekil kurulum başarı bildirimleri:**
  - `🆕 İlk kurulum tamamlandı ve Drive'a yedeklendi (X.Y sn) — <Qwen 3.8 27B | Gemma 4> servinge hazır!`
  - `⚡ Drive önbelleğinden X.Y sn'de yüklendi — <Qwen 3.8 27B | Gemma 4> servinge hazır!`
  - `♻️ Açık sunucu algılandı (X.Y sn) — <Qwen 3.8 27B | Gemma 4> servinge hazır!`

## Canlı Stüdyo WebUI ve Bağımsız Deneyler

- **Bağımsız `ExperimentSession` izolasyonu:** `Deney 1`, `Deney 2` ve `Deney 3` hücreleri Hücre 1 sonrasında kendi izole çalışma klasörünü açar; birbirine bağımlı değildir ve istenen sırayla tekrar çalıştırılabilir.
- **Portsuz yerel WebSocket kanalı:** `Canlı Stüdyo` (`Hücre 5`) üçüncü taraf çerez gerektiren tünel portu açmaz; doğrudan `google.colab.output.register_callback` ve `google.colab.kernel.invokeFunction` kanalını kullanır ve Colab hücresini kilitlemez.
- **Hata zırhı (`ALAB-E01` – `ALAB-E99`):** Beklenmeyen ham Python izleri yerine tüm hatalar sabit 2 satırlık `ALAB-Exx` kutusuna düşer. Çözüm adımları Drive klasöründeki `hata-cozum-rehberi.pdf` / `error-guide.pdf` belgelerinde, gözlem tabloları ise `oturum-04.pdf` kitapçığında yer alır.
