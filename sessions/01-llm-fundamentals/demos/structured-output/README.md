# Mini demo: Araç işlevi ve yapılandırılmış çıktı

[Demolara dön](../README.md) | [English](README.en.md)

**Durum:** Çalışan yerel başlangıç örneği. Bu demo bir LLM, gerçek agent veya harici API çağırmaz. Sabit bir kavram tablosunu araç işlevi gibi çağırır ve sonucu küçük bir şemaya göre kontrol eder. Eğitmenin ders sırasında kullanacağı gerçek AI agent'ı henüz seçilmedi.

Önce [kurulum rehberini](../../../../setup/README.md) tamamla. Depo kökünde terminal aç, demo klasörüne geç ve sistemine uygun komutları kullan:

```text
cd sessions/01-llm-fundamentals/demos/structured-output
```

macOS / Linux:

```sh
../../../../.agentlab/venv/bin/python demo.py --term token
../../../../.agentlab/venv/bin/python demo.py --term bilinmeyen
../../../../.agentlab/venv/bin/python demo.py --term schema
```

Windows PowerShell:

```powershell
..\..\..\..\.agentlab\venv\Scripts\python.exe demo.py --term token
..\..\..\..\.agentlab\venv\Scripts\python.exe demo.py --term bilinmeyen
..\..\..\..\.agentlab\venv\Scripts\python.exe demo.py --term schema
```

Çıktıdaki `term`, `found` ve `explanation` alanlarını gözlemle. [Şema dosyası](schema.json) alanları ve türlerini tarif eder. [Kaynak kod](demo.py) bu şemada kullanılan küçük özellik kümesini yerel olarak kontrol eder; genel amaçlı bir JSON Schema doğrulayıcısı değildir. Şemaya uyum, açıklamanın doğru olduğuna tek başına kanıt oluşturmaz.

Demo ağ bağlantısı kurmaz ve kalıcı kaynak oluşturmaz. Proje ortamı için [kurulum rehberine](../../../../setup/README.md) bak.

## Deney D: Yapı ile doğruluğu ayır

Aynı klasördeki küçük karşılaştırma, iki örneği gerçek doğrulayıcıdan geçirir:

```text
# macOS / Linux
../../../../.agentlab/venv/bin/python schema_lab.py
# Windows PowerShell
..\..\..\..\.agentlab\venv\Scripts\python.exe schema_lab.py
```

A nesnesi geçerli JSON'dur ve şemaya uyar, ancak açıklaması **bilerek yanlıştır**. B de geçerli JSON'dur; `found` alanı boolean yerine metin olduğu için şemayı geçmez. Doğrulayıcı açıklamanın gerçekliğini ölçmez. Örnek çevrimdışıdır ve model çağırmaz.
