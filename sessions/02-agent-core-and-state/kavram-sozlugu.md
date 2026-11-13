# Oturum sözlüğü: Ajan Mimarisi, Bağlam ve Bellek

[Oturuma dön](README.md) | [English](glossary.md) | [Genel sözlük](../../docs/tr/kavram-sozlugu.md)

| Terim | Bu oturumdaki anlamı |
| --- | --- |
| Harness | Model çağrılarını, bağlamı, araç izinlerini ve görev akışını yöneten uygulama. |
| Agent loop | Model önerisi, doğrulama, araç sonucu ve devam/durma kararını tekrarlayan kontrol döngüsü. |
| ReAct | Görev değerlendirmesini eylem ve gözlemlerle birlikte ilerletme yaklaşımı. |
| Plan-and-Solve | Önce kısa bir görev planı kurup sonra adımları yürütme yaklaşımı. |
| Action / eylem | Modelin önerdiği veya uygulamanın doğrulayıp çalıştırdığı işlem; bu iki aşama ayrıdır. |
| Observation / gözlem | Gerçekte çalıştırılan araçtan dönen sonuç veya hata. |
| Trace / yürütme izi | Gözlenebilir istek, araç, sonuç ve durma bilgilerinin kaydı. |
| Context engineering | Model isteğine hangi bilgilerin hangi bütçeyle ekleneceğini tasarlama. |
| State / durum | Görevin mevcut mesajları, sonuçları ve ilerleme bilgisidir. |
| Session / oturum | Uygulamanın bir arada tuttuğu konuşma ve görev kapsamı. |
| Memory / bellek | Daha sonra yeniden kullanılmak üzere seçilmiş kayıtlar. |
| Persistence / kalıcılık | Verinin bir süreç veya oturum bittikten sonra da saklanabilmesi. |
| Retrieval | Bir koleksiyondan soruyla ilişkili parçaları getirme işlemi. |
| Corpus / kaynak koleksiyonu | Aramanın yapıldığı belge veya kayıt kümesi. |
| Vector search | Sayısal vektörleri benzerlik ölçüsüne göre sıralayan arama. |
| Cosine similarity | İki vektörün yön benzerliğini ölçen, uzunluklarıyla normalize edilmiş skaler çarpım. |
| Embedding | Bir öğenin sayısal vektörle temsilidir; kullanılan yöntem sonucu belirler. |
| RAG | Getirilen kanıtları üretim bağlamına ekleyerek yanıt oluşturma akışı. |
| Grounding | Yanıtı incelenebilir kaynaklarla destekleme. |
| Allowlist / izin listesi | Uygulamanın kabul ettiği araç ve argüman sınırları. |
| Step limit / adım sınırı | Döngünün sonsuza kadar sürmesini önleyen üst sınır. |
| KV cache | Üretimde önceki token hesaplarının bir bölümünü tutan çalışma belleği; model ağırlıklarından ayrıdır. |
