# LLM deney alanı

[Demolara dön](../README.md) | [English](README.en.md)

Başlangıç noktası: [AgentLab Colab defteri](AgentLab-Colab.ipynb). Defteri GitHub'dan indirip (veya Drive kopyandan) Colab'da **Dosya → Not defteri yükle** ile açın ve hücreleri sırayla çalıştırın (`0A` ortam/aygıt denetimi, `1A` kütüphane kurulumu, `2A`–`2E` sabit revizyon manifesti ve model yükleme, `3A`–`3B` token inceleme, `4A`–`4C` olasılık dağılımı ve örnekleme, `5A`–`5B` greedy vs. örneklemeli metin üretimi, `6A`–`6C` tekil araç çağrısı doğrulama döngüsü, `7A` bellek boşaltma). Python kurmanız gerekmez. Modelin yaklaşık **1,75 GB** ağırlığı ve gerekli paketler çalışma ortamına indirilir; hücreyi çalıştırmadan önce bağlantı ve depolama durumunuzu kontrol edin. GPU erişimi garanti değildir; CPU çalışır fakat daha yavaştır. Girdiğiniz metinler Colab çalışma ortamında işlenir; gizli bilgi kullanmayın. Son hücre (`7A`) modeli bellekten çıkarır. Önbellekteki dosya ve klasörlerin sahipliği kesin doğrulanamadığı için otomatik disk temizliği yapılmaz; hücrenin gösterdiği geçici klasörü inceleyin; bu nedenle `7A` hücresinin bellek temizliğinin ardından otomatik silmeyi durdurmak için bilinçli olarak `RuntimeError` güvenlik uyarısı yükseltmesi beklenen davranıştır.

Hugging Face daha önce farklı bir önbellekle yüklenmişse defter çalışma zamanını yeniden başlatma yönergesi verir.

## Yorumlama

Token parçaları tek başına eksik Unicode baytları içerebilir. `4B` (`next_token_distribution`), tek bir ileri geçişten gelen ham olasılık dağılımını ve temperature/top-k/top-p örneklemesi sonrası dağılımını yan yana gösterir; çok adımlı metin üretimi `5A`–`5B` (`generate_text`) hücrelerinde ayrı çalışır. En fazla sekiz aday listelenir; olasılıklar sunulmadığında boşluk açıkça belirtilir. Colab'da deney girdi sınırı 2.048 tokendır; kullanılabilir donanım belleği daha düşük olabilir. Araç çağrısı garanti değildir; model çağrı önermezse veya öneri doğrulamayı geçmezse araç çalıştırılmaz.
