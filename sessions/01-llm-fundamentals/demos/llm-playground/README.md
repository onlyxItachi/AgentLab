# LLM deney alanı

[Demolara dön](../README.md) | [English](README.en.md)

İlk tercih: [AgentLab Colab defteri](AgentLab-Colab.ipynb). Colab'da **Dosya → Not defteri yükle** ile açın ve hücreleri sırayla çalıştırın. Python kurmanız gerekmez. Modelin yaklaşık **1,75 GB** ağırlığı ve gerekli paketler çalışma ortamına indirilir; hücreyi çalıştırmadan önce bağlantı ve depolama durumunuzu kontrol edin. GPU erişimi garanti değildir; CPU çalışır fakat daha yavaştır. Girdiğiniz metinler Colab çalışma ortamında işlenir; gizli bilgi kullanmayın. Son hücre modeli bellekten çıkarır. Önbellekteki dosya ve klasörlerin sahipliği kesin doğrulanamadığı için otomatik disk temizliği yapılmaz; hücrenin gösterdiği geçici klasörü inceleyin.

Hugging Face daha önce farklı bir önbellekle yüklenmişse defter çalışma zamanını yeniden başlatma yönergesi verir.

## Kendi bilgisayarınızda

1. Önce [AgentLab kurulumunu](../../../../setup/README.md) tamamlayın; Python ile birlikte Tkinter desteği bulunmalıdır.
2. İşletim sisteminize uygun [resmî llama.cpp sürümünü](https://github.com/ggml-org/llama.cpp/releases) indirin, arşivi çıkarın; içindeki `llama-server` dosyasını seçmeniz gerekecek. Linux/macOS için çalıştırma izni gerekebilir. Platformunuz desteklenmiyorsa [resmî derleme yönergelerine](https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md) bakın.
3. [Qwen3.5-0.8B GGUF](https://huggingface.co/ggml-org/Qwen3.5-0.8B-GGUF) sayfasından `Qwen3.5-0.8B-Q4_0.gguf` dosyasını indirin: yaklaşık **563 MB**. Model Apache-2.0 lisanslıdır. Ağırlıklar depoda bulunmaz; dosyayı istediğiniz klasöre saklayın.
4. Windows'ta `start.cmd`, macOS'ta `start.command` dosyasını açın; Linux'ta `start.command` dosyasını çalıştırın. Program seçicilerinde önce `llama-server`, sonra `.gguf` dosyasını seçin. Model yüklenince tarayıcı açılır. CPU kullanılabilir; hız donanıma bağlıdır.
5. Pencereyi kapatmak için çalışan başlatıcıda **Ctrl+C** kullanın. Uygulama yalnızca kendi başlattığı sunucuyu durdurur; indirdiğiniz dosyaları silmez. Kaldırmak için bu iki indirmeyi kendi kaydettiğiniz yerden silin ve gerekirse [AgentLab kaldırma yönergesini](../../../../setup/README.md) izleyin.

Yerel arayüz `127.0.0.1` ile sınırlıdır. Model sunucusuna rastgele oluşturulan geçici anahtarla erişilir; hiçbir ücretli API anahtarı gerekmez. Bilgisayarınızda bilinmeyen programlar varsa bu yerel sınır tam bir güvenlik garantisi değildir.

**Yorumlama:** Token parçaları tek başına eksik Unicode baytları içerebilir. Ham tablo ayrı bir isteğin ilk adımını; örnekleme sonrası tablo gösterilen üretimin ilk adımını gösterir. En fazla sekiz aday listelenir; olasılıklar sunulmadığında boşluk açıkça belirtilir. Yerel context değeri modelin teorik sınırı değil, başlatılan sunucunun sınırıdır. Colab'da deney girdi sınırı 2.048 tokendır; kullanılabilir donanım belleği daha düşük olabilir. Araç çağrısı garanti değildir; model çağrı önermezse veya öneri doğrulamayı geçmezse araç çalıştırılmaz. Başka GGUF modellerin araç şablonu uyumlu olmayabilir.
