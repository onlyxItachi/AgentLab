# Kavramsal inceleme: Araç işlevi ve yapılandırılmış çıktı

[Demolara dön](../README.md) | [English](README.en.md)

Bu inceleme, bir kavram arama işlevinden dönen JSON çıktısı ile [şema dosyasındaki](schema.json) kuralların nasıl ayrıldığını gösterir. Herhangi bir LLM veya harici API çağrısı yapmaz.

## Beklenen şema alanları

[Şema dosyası](schema.json) her nesnede yalnız üç zorunlu alan (`term`, `found`, `explanation`) tanımlar (`additionalProperties: false`):

- `term`: kavram adı (`string`)
- `found`: kavramın sözlükte bulunup bulunmadığı (`boolean`)
- `explanation`: açıklama metni (`string`)

Bilinen bir kavram için örnek çıktı:

```json
{"term": "token", "found": true, "explanation": "Tokenizer'ın metinden elde ettiği ve modelin işlediği birim."}
```

Bilinmeyen bir kavram için örnek çıktı:

```json
{"term": "bilinmeyen", "found": false, "explanation": "Kavram sözlükte bulunamadı."}
```

Şemaya uyum, açıklamanın doğru olduğuna tek başına kanıt oluşturmaz.

## Deney D: Yapı ile doğruluğu ayır

Aşağıdaki iki örneği [şema dosyasına](schema.json) göre karşılaştır:

1. **A nesnesi** (geçerli JSON ve şemaya uyar, ancak açıklaması **bilerek yanlıştır**):

```json
{"term": "token", "found": true, "explanation": "Token her zaman bir kelimedir."}
```

2. **B nesnesi** (geçerli JSON'dur, ancak `found` alanı boolean yerine metin olduğundan şemayı geçmez):

```json
{"term": "token", "found": "true", "explanation": "Tokenizer'ın metinden elde ettiği ve modelin işlediği birim."}
```

Geçerli JSON olmak, bir şemaya uymak ve içeriğin doğru olması birbirinden ayrı üç kontroldür.
