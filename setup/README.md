# İlk kurulum: Yeni başlayanlar için

[Ana sayfa](../README.md) | [English](README.en.md)

Bu rehber daha önce Python veya geliştirme aracı kurmamış kişiler içindir. Komutları kopyalamadan önce aşağıdaki adımlarla **AgentLab klasörünü** aç. Bu ilk örnek için Python 3.10 veya üstü gerekir; Git, GPU, API anahtarı ve ücretli bir hesap gerekmez.

## 1. Dosyaları edin ve klasörü aç

Eğitmenin paylaştığı AgentLab klasörünü bilgisayarına indir ve sıkıştırılmışsa çıkar. Dosyaları GitHub üzerinden indirmek için **Code → Download ZIP** seçeneğini de kullanabilirsin. İçinde `README.md` dosyası ve `setup` klasörü görünen klasörü aç.

- **Windows:** Dosya Gezgini'nde bu klasör açıkken adres çubuğuna `powershell` yazıp Enter'a bas.
- **macOS:** Terminal'i aç, `cd ` yaz ve AgentLab klasörünü Finder'dan pencereye sürükleyip Enter'a bas.
- **Linux:** Dosya yöneticinde AgentLab klasörünü açıp “Terminalde aç” seçeneğini kullanabilir veya terminalde `cd ` yazıp klasörü pencereye sürükleyebilirsin.

## 2. Kurulumu başlat

**Windows PowerShell:** Windows’ta bu yolu kullan. Git Bash üzerinden `start.sh`, bazı Python yükleyicilerinde otomatik kurulumu tetikleyebilir.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\setup\start.ps1 -Action install
```

Bu komut yalnızca açtığı PowerShell işlemi için çalıştırma ilkesini değiştirir; bilgisayarın kalıcı ilkesini değiştirmez. Kurum politikası çalışmayı engellerse yöneticine danış.

**macOS veya Linux terminali:**

```bash
bash setup/start.sh install
```

Script Python'u ve gerekli `venv` bileşenini kontrol eder. Python yoksa resmî indirme sayfasının adresini gösterir ve sayfayı açmadan önce sana sorar. Python'u indirmeyi ve yüklemeyi sen başlatırsın; script otomatik indirme, sistem kurulumu veya `sudo` işlemi yapmaz. Yükleyici sistem genelinde değişiklik isteyebilir; onay vermeden önce gösterdiklerini oku. Kurulumdan sonra terminali kapatıp aç ve aynı AgentLab komutunu yeniden çalıştır.

Windows'ta indirdiğin uygulama yalnızca **Python Install Manager**'ı kurduysa bir Python sürümünü de ayrıca kurman gerekir. Yeni bir PowerShell penceresinde, örneğin CI'da denenen Python 3.11 için `py install 3.11` komutunu kendin çalıştırabilir, yükleyicinin adımlarını inceleyebilirsin. Ardından AgentLab kurulum komutunu yeniden çalıştır.

Debian/Ubuntu'da Python bulunup `venv` eksikse, dağıtımının resmî paket yönergelerini kontrol ederek `python3-venv` paketini kendin kurabilirsin. Bu işlem sistem paketlerini değiştirebilir ve kendi onayını gerektirir.

Uygun Python bulunduğunda script `.agentlab/venv` içinde bu projeye ait bir sanal ortam oluşturur ve ortamı doğrular. Paket veya model indirmez. Aynı kurulum komutunu tekrar çalıştırmak, ortam değişmemişse mevcut ortamı korur ve yeniden doğrular.

## 3. Ortamı doğrula ve demoyu dene

**Windows PowerShell:**

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\setup\start.ps1 -Action verify
.\.agentlab\venv\Scripts\python.exe sessions/01-llm-fundamentals/demos/structured-output/demo.py --term token
```

**macOS veya Linux:**

```bash
bash setup/start.sh verify
.agentlab/venv/bin/python sessions/01-llm-fundamentals/demos/structured-output/demo.py --term token
```

Demo açıklaması için [araç ve yapılandırılmış çıktı örneğine](../sessions/01-llm-fundamentals/demos/structured-output/README.md) bak. Demo gerçek bir yapay zekâ modeli çağırmaz.

## 4. Ortamı güvenle kaldır

Otomatik kaldırma, eşzamanlı dosya değişikliklerini güvenle ayırt edemediği için kapalıdır. Kaldırma komutu `.agentlab` varsa hiçbir dosyayı silmez, durumu bildirir ve çıkış kodu 1 ile durur; Python kurulu olması da gerekmez. Klasör yoksa işlem başarıyla tamamlanır.

1. AgentLab demolarını ve bu ortama bağlı programları kapat.
2. AgentLab proje klasöründeki **`.agentlab`** klasörünü dosya yöneticisinde bul. Görünmüyorsa gizli öğeleri göster: Windows Dosya Gezgini'nde **Görünüm → Gizli öğeler**; macOS Finder'da **Command + Shift + .** kullanabilirsin.
3. İçindeki dosyaları incele. Sana ait veya emin olmadığın içerik varsa sakla ya da önce güvenli bir yere kopyala. Klasörün tamamını silmek istemiyorsan otomatik işlem yapma.
4. Yalnızca içeriğin kaldırılmasının güvenli olduğundan eminsen `.agentlab` klasörünü kendin çöp kutusuna taşı. Bu işlem ayrıca kurduğun sistem Python'unu kaldırmaz.
5. Klasör kaldırıldıktan sonra `bash setup/start.sh uninstall` veya Windows'ta `powershell -NoProfile -ExecutionPolicy Bypass -File .\setup\start.ps1 -Action uninstall` komutu ortamın bulunmadığını bildirir. İstersen kurulumu yeniden başlatabilirsin.

Daha önceki sürümde kaldırma yarıda kaldıysa `removing` işaretçisi ve kalan dosyalar aynen korunur; aynı inceleme ve elle kaldırma adımlarını izle. Klasör dururken kurulum veya doğrulama kurtarma uyarısıyla durur; içeriği inceleyip kaldırdıktan sonra kurulum yeniden çalışır.
