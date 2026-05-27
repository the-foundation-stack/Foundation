# Open Charity API Standard (OCAS)

> Hayır kurumlarının bağış API'leri için açık ve tarafsız bir spesifikasyon.
> Herhangi bir hayır kuruluşunun, küçük bir cami, uluslararası bir STK, gıda bankası veya barınak, dünyanın herhangi bir yerindeki herhangi bir geliştiricinin yaptığı herhangi bir uygulamaya entegre olabilmesi için tasarlandı.

---

## Bu proje neden var

Hayır kurumlarıyla iletişim kuran bir yazılım yapmaya çalıştıysanız, muhtemelen çoğu geliştiricinin karşılaştığı sorunla karşılaştınız: **ortak bir standart yok.** Bağış kabul etmenin programatik bir yolunu sunan hayır kurumlarının her biri bunu kendi yöntemiyle yapar. Çoğu ise hiçbir şey sunmaz, JustGiving, Donorbox, GoFundMe, Enthuse gibi her birinin kendi arayüzü, kendi veri modeli ve kendi ücretleri olan üçüncü taraf platformlara dayanır.

Bu parçalanmanın bir bedeli var:

- Uygulamasına "X hayır kurumuna bağış yap" özelliği eklemek isteyen bir geliştirici, N farklı sistemle entegre olmak zorunda kalır.
- Ücretli platformları karşılayamayan hayır kurumları teknoloji dünyasından dışlanır.
- Küçük İslami ve topluluk temelli hayır kurumları daha geniş yazılım ekosisteminde neredeyse görünmez kalır.
- Gift Aid, düzenli bağışlar, Zekât sınıflandırması, vergi makbuzları gibi standart kavramlar her seferinde (kötü bir şekilde) yeniden inşa edilir.

**OCAS** bunu çözmeye yönelik bir girişimdir. Herhangi bir hayır kurumunun bağışlarını, aboneliklerini, kampanyalarını, makbuzlarını ve vergi indirimi beyanlarını standart bir biçimde sunmak için benimseyebileceği, ücretsiz ve açık bir spesifikasyondur. Herhangi bir uygulama daha sonra aynı kod yolunu kullanarak OCAS uyumlu herhangi bir hayır kurumuna entegre olabilir.

Bu proje bilinçli olarak:

- **Sağlayıcıdan bağımsız.** Stripe, PayPal veya belirli bir ödeme işlemcisine bağlı değil.
- **Yüzeysel olarak dini ve ideolojik olarak tarafsız.** Laik bir gıda bankası ve cami için eşit derecede iyi çalışır.
- **Gerektiğinde dini olarak bilgili.** Zekât, Sadaka, Sadaka-i Cariye, Vakıf, Lillah, Fidye, Keffaret, Kurban, Akika için birinci sınıf destek, Gift Aid, 501(c)(3), DGR, ANBI ve diğer vergi indirimi şemalarıyla birlikte.
- **Kendi sunucunda barındırılabilir.** Her hayır kurumu OCAS'ı kendi sunucularında çalıştırabilir. Merkezi otorite yok. Zorunlu hub yok.

## Daha geniş vizyon

OCAS, daha büyük bir çabanın ilk projesidir: **sosyal açıdan faydalı yazılımlar için açık, paylaşılan standartlar, protokoller ve altyapı** inşa etmek; bu çabada özellikle Müslüman geliştiricilerin, akademisyenlerin ve toplulukların açıkça işbirliği yapabilmesi vurgulanır, ancak iş kendi başına herkese açıktır.

Hedef, İslami finans, etik bilişim, helal ödeme kanalları veya adil dağıtım üzerine teorilere sahip üniversitelerin, araştırmacıların ve profesörlerin, herhangi bir geliştiricinin uygun atıfla üzerine inşa edebileceği referans uygulamaları yayımlayabilmesidir. Pull request'ler, RFC taslakları ve akademik makaleler hepsi memnuniyetle karşılanır.

İslami finans bilincine sahip, topluluk odaklı veya değerlere uygun bir şey inşa ediyorsanız ve kendinizi tekerleği yeniden icat ederken buluyorsanız, burası tekerleği getirip başkalarının kullanmasına izin vereceğiniz yerdir.

## Repo'da neler var

```
open-charity-api/
├── README.md                     ← Ana belge (İngilizce)
├── spec/openapi.yaml             ← OpenAPI 3.1 spesifikasyonu
├── postman/                      ← Postman koleksiyonu
├── docs/
│   ├── industry-analysis.md      ← Hayırseverlik sektörü araştırması
│   ├── authentication.md         ← Üç kimlik doğrulama modu
│   ├── gift-aid-and-tax.md       ← İngiltere Gift Aid + uluslararası şemalar
│   ├── islamic-considerations.md ← Zekât, Sadaka, Kurban, Vakıf vb.
│   ├── contributing.md           ← Nasıl katkıda bulunulur
│   └── i18n/                     ← Çeviriler (bu klasör)
└── examples/                     ← Örnek JSON yükleri
```

## Desteklenen İslami bağış kategorileri

| Tür | Anlamı |
|---|---|
| `zakat` | Zorunlu yıllık bağış, 8 kanonik kategoriden birine yönlendirilir |
| `sadaqah` | Genel gönüllü hayır işi |
| `sadaqah_jariyah` | Devam eden ödüllü hayır işi |
| `waqf` | Vakıf, kalıcı sermaye |
| `lillah` | "Allah için", koşullar karşılanmadıysa Gift Aid uygun değil |
| `fidya` | Telafi (örn. tutulmamış oruçlar) |
| `kaffarah` | Keffaret |
| `qurbani` / `udhiyyah` | Eid al-Adha kurbanı |
| `aqiqah` | Çocuk doğumu kurbanı |
| `interest_purification` | Riba arındırma, Zekât olarak beyan edilemez |

Ayrıntılar ve gerekli meta veriler için `docs/islamic-considerations.md` belgesine bakın.

## Niyet

Bu ticari bir ürün değil. Bir şirket yok. Ücret yok. Amaç bir standart, herkese ait ve hiç kimseye ait olmayan, böylece hayır kurumları ve geliştiriciler sömürücü tescilli ağ geçitleri olmadan birlikte çalışabilir.

Faydalıysa benimseyin. Bir şey yanlışsa düzeltin. Bir şey eksikse ekleyin.

---

**İngilizce tam teknik dokümantasyon:** [`../../README.md`](../../README.md)
