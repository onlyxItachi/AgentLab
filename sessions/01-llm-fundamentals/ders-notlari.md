# Ders notları: LLM Temelleri

[Oturuma dön](README.md) | [English](lesson-notes.md) | [Sözlük](kavram-sozlugu.md)

Bu notlar birinci oturumun başvuru kaynağıdır. Öğrenme sırası LLM → Token → Vektör / Matris / Gömme → İşlev / API / Araç → Yapılandırılmış Çıktı / Şema şeklindedir; **bu sıralama her modelin birebir çalışma hattı değildir**. Deneyler için [Colab deney alanını](demos/llm-playground/README.md) ve [yapılandırılmış çıktı incelemesini](demos/structured-output/README.md) kullanabilirsin.

## 1. LLM ve ajan ilişkisi

Büyük dil modeli (LLM), o ana kadar verilen bağlamı kullanarak bir sonraki token için olasılıklar hesaplar. Bir sonraki token seçildikten sonra süreç yeni bağlamla tekrarlanabilir; böylece bir yanıt oluşur. Modelin eğitimi çok daha geniş bir konudur, fakat burada üretimin temel mantığına odaklanıyoruz. Akıcı bir yanıt, bilginin doğruluğunu kanıtlamaz.

Bir **ajan sistemi**, modelin çevresine bağlam hazırlama, araç önerilerini değerlendirme, sonuçları işleme ve sonraki adımı belirleme gibi uygulama davranışları ekleyebilir. Her model çağrısı bir ajan değildir. Bir aracı modele tarif etmek, aracın çalıştırıldığı veya güvenilir bir sonuca ulaşıldığı anlamına da gelmez.

Örneğin “token nedir?” sorusunda model bir kavram arama aracı önerebilir. Uygulama bu öneriyi kontrol eder, uygun bulursa sözlük işlevini çalıştırır ve sonucu modele geri verir. Model aracı çağırmamayı da seçebilir.

## 2. Token, tokenization ve context window

**Tokenizer**, metni modelin kullandığı tokenlara ayırır. Bir token bir kelime, kelimenin parçası, boşluk, noktalama veya farklı bir parça olabilir. Token sayısı kelime veya karakter sayısına eşit olmak zorunda değildir; kullanılan tokenizer ve tam metin sonucu değiştirir. Bazı özel tokenlar konuşma sınırları gibi yapısal işaretler taşır.

**Token ID**, belirli tokenizer sözlüğündeki bir tokenın kimliğidir; tek başına vektör veya olasılık değildir. Unicode metin bazen birkaç tokenın baytlarıyla temsil edilir. Tek bir token ayrı çözümlendiğinde `�` gibi eksik bir karakter görülebilir; bu durum tek başına özgün metnin hatalı olduğu anlamına gelmez.

**Context window (bağlam penceresi)**, modelin bir seferde ele alabildiği token bütçesidir. Girdi ve konuşma geçmişi ile üretilecek tokenlar için ayrılan yer birlikte düşünülür. Modelin yapılandırılmış üst sınırı, kullanılan donanımın veya defter ayarının o uzunlukta çalışabileceğini garanti etmez.

### Deney A: İki dilde tokenlar

Colab'daki **3. bölümde (Tokenlara bak)** (`3A`–`3B`) iki metni `Merhaba dünya!` ve `Hello world!` olarak dene; varsayılan örneklerin sonundaki el emojisini iki metinden de çıkar. Token sayısını, bir parçayı ve onun ID'sini kaydet. Tek bir örnekten dillerin tümü hakkında genelleme yapma.

### Deney B: Üretim ve örnekleme

Modelin **ham olasılık dağılımı**, belirli bağlamda aday sonraki tokenlara ilişkin tahminidir. Görülen ilk birkaç adayın olasılıkları %100'e toplanmak zorunda değildir; başka adaylar da vardır. Temperature, top-k ve top-p gibi **örnekleme** ayarları seçimi etkileyebilir. Düşük temperature daha olası seçenekleri öne çıkarabilir; yüksek değer dağılımı daha yaygın hâle getirebilir. Top-k aday sayısını, top-p ise olasılık eşiğine göre aday kümesini sınırlar.

Colab'da **4. bölüm (Gerçek sonraki token olasılıkları)** (`4A`–`4C`) bölümünü aç (ardından `5A`–`5B` ile deterministik ve örneklemeli metin üretimini karşılaştırabilirsin). İlk metin olarak `Bugün hava` kullan. Top-k ve top-p sabitken yalnız temperature'ı değiştir; ikinci çağrının `top_k` ve `top_p` değerlerini 20 ve 0.9 yap; sonra ilk ayarlara dönüp bağlamı `Kışın dağlarda bugün hava` yap. Aynı bağlamda ham dağılımı örnekleme sonrası dağılımla karıştırma.

Colab defteri Qwen3.5-0.8B model ağırlıklarıyla olasılık ve örnekleme adımlarını gözlemletir; kullanılan GPU veya CPU çalışma zamanına göre süreler değişebilir.

## 3. Vektör / Matris / Gömme (Embedding)

Bir **vektör**, sayılardan oluşan sıralı bir liste gibi düşünülebilir; bir **matris** ise sayıların satır ve sütunlarla düzenlenmiş hâlidir. Aşağıdaki örnekte vektörün üç elemanı, matrisin iki satırı ve üç sütunu vardır:

$$
\mathbf{v} = \begin{bmatrix} 0.2 \\ -0.1 \\ 0.7 \end{bmatrix} \in \mathbb{R}^{3},
\qquad
\mathbf{M} = \begin{bmatrix} 0.2 & -0.1 & 0.7 \\ 0.4 & 0.5 & -0.2 \end{bmatrix} \in \mathbb{R}^{2 \times 3}
$$

Bu sayılar gerçek modelden alınmamış, gösterim amaçlı değerlerdir. Matrisin her satırı, üç sayıyla temsil edilen ayrı bir örnek vektör olarak okunabilir. **Embedding**, örneğin bir token veya metni sayısal vektörle temsil etme yöntemidir; boyut sayısı kullanılan modele bağlıdır. Bazı embedding uzaylarında vektör yakınlığı ilişkili içerikleri bulmaya yardımcı olur; bu yakınlık tek başına doğruluk garantisi değildir. Her koordinata tek başına bir kelime anlamı yüklemek gerekmez.

Bir token ID'si sözlükteki kimliği, embedding sayısal temsili, olasılık dağılımı ise aday devamlar üzerindeki model tahminini ifade eder. Bunlar farklı şeylerdir.

## 4. İşlev / API / Araç ve tool calling

Bir **function (işlev)**, çağrıldığında tanımlı bir iş yapan kod parçasıdır. **API**, bir yazılımın sunduğu işlev veya verilere erişim kurallarını tarif eden arayüzdür. Bir **tool (araç)**, uygulamanın modele belirli koşullarla kullanıma açtığı bir yetenektir.

Aşağıdaki diyagram bir **örnek akış** gösterir. Modelin önerisi kodu kendiliğinden çalıştırmaz; uygulama veya harness izinleri ve girdileri kontrol eder:

`�``mermaid
flowchart TD
    A["Kullanıcı isteği"] --> B["Model araç çağrısını önerir"]
    B --> C{"Uygulama izni ve girdileri kontrol eder"}
    C -->|Uygun| D["Uygulama aracı çalıştırır"]
    C -->|Uygun değil| X["Uygulama çağrıyı reddeder"]
    D --> E["Araç sonucu uygulamaya döner"]
    E --> F["Uygulama sonucu modele iletir"]
    F --> G["Model yanıt veya sonraki adımı önerir"]
`�``

### Deney C: Bir sözlük aracını gözlemle

Colab'daki **6. bölüm (Araç çağrısı)** (`6A`–`6C`) hücrelerini aç. `What is a token? Use lookup_term first.` sorusuyla dene. Model araç adını ve `term` argümanını önerirse, harness yalnız izin verilen tek çağrıyı ve argümanı doğrular; sabit sözlükten gelen gerçek sonuç modele iletilir. Hangi adımın model, hangisinin uygulama tarafından yapıldığını ayrı ayrı kaydet. Model çağrı önermezse veya öneri geçerli değilse araç çalıştırılmaz.

## 5. Yapılandırılmış Çıktı / Şema ve JSON

**JSON**, nesne, metin, sayı, boolean ve liste gibi değerleri metin olarak gösteren bir veri biçimidir. **JSON Schema**, beklenen alanları, veri türlerini ve başka kuralları tanımlayabilir. Geçerli JSON olmak, belirli bir şemaya uymak ve içeriğin doğru olması üç ayrı kontroldür.

Aşağıdaki örnek demo şemasına uyar ama açıklaması yanlıştır:

`�``json
{"term": "token", "found": true, "explanation": "Token her zaman bir kelimedir."}
`�``

`found` alanını `"true"` yaparsan sonuç hâlâ geçerli JSON'dur; ancak değer boolean yerine metin olduğundan demo şemasına uymaz. Şema, türleri doğru bir açıklamanın anlamsal olarak doğru olduğunu tek başına kanıtlamaz.

### Deney D: Şema ve doğruluk karşılaştırması

[Yapılandırılmış çıktı incelemesinde](demos/structured-output/README.md) yer alan [şema dosyasını](demos/structured-output/schema.json) yukarıdaki iki JSON örneğiyle karşılaştır. İlk nesne `term`, `found` ve `explanation` alanlarının tür kurallarını karşılar fakat açıklaması **bilerek yanlıştır**. `found` alanı `"true"` yapılan ikinci örnek ise geçerli JSON olsa da `boolean` beklentisini bozduğu için şemadan kalır. Bu karşılaştırma kavramsaldır ve harici bir API veya LLM çağırmaz. Pratik sorular [alıştırmalar](exercises/README.md) bölümündedir.
