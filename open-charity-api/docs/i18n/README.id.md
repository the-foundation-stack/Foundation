# Open Charity API Standard (OCAS)

> Spesifikasi terbuka dan netral untuk API donasi lembaga amal.
> Dirancang agar lembaga amal mana pun, masjid kecil, LSM internasional, bank pangan, atau penampungan, dapat berintegrasi dengan aplikasi apa pun, yang dibuat oleh pengembang mana pun, di mana pun di dunia.

---

## Mengapa proyek ini ada

Jika Anda pernah mencoba membangun perangkat lunak yang berkomunikasi dengan lembaga amal, Anda mungkin menemui masalah yang sama seperti kebanyakan pengembang: **tidak ada standar bersama.** Lembaga amal yang menawarkan cara programatik untuk menerima donasi melakukannya dengan caranya masing-masing. Dan kebanyakan tidak menawarkan apa pun, mereka bergantung pada platform pihak ketiga (JustGiving, Donorbox, GoFundMe, Enthuse) yang masing-masing memiliki antarmuka sendiri, model data sendiri, dan biaya sendiri.

Fragmentasi ini punya harga:

- Pengembang yang ingin menambahkan fitur "donasi ke Lembaga X" di dalam aplikasinya harus berintegrasi dengan N sistem berbeda.
- Lembaga amal yang tidak mampu membayar platform berbayar tertinggal dari dunia teknologi.
- Lembaga amal Islam kecil dan berbasis komunitas hampir tidak terlihat dalam ekosistem perangkat lunak yang lebih luas.
- Konsep standar seperti Gift Aid, donasi berulang, kategorisasi Zakat, tanda terima pajak dibangun ulang (dengan buruk) setiap kali.

**OCAS** adalah upaya untuk menyelesaikan ini. Ini adalah spesifikasi gratis dan terbuka yang dapat diadopsi oleh lembaga amal mana pun untuk mengekspos donasi, langganan, kampanye, tanda terima, dan deklarasi keringanan pajak mereka dalam bentuk standar. Aplikasi mana pun kemudian dapat berintegrasi dengan lembaga amal yang sesuai dengan OCAS menggunakan jalur kode yang sama.

Proyek ini secara sengaja:

- **Netral terhadap vendor.** Tidak terikat pada Stripe, PayPal, atau pemroses tertentu mana pun.
- **Netral secara religius dan ideologis di permukaan.** Bekerja sama baiknya untuk bank pangan sekuler maupun masjid.
- **Sadar agama jika diperlukan.** Dukungan kelas satu untuk Zakat, Sedekah, Sedekah Jariah, Wakaf, Lillah, Fidyah, Kafarat, Kurban, Akikah, bersama dengan Gift Aid, 501(c)(3), DGR, ANBI, dan skema keringanan pajak lainnya.
- **Dapat di-host sendiri.** Setiap lembaga amal dapat menjalankan OCAS di servernya sendiri. Tidak ada otoritas pusat. Tidak ada hub wajib.

## Visi yang lebih luas

OCAS adalah proyek pertama dari upaya yang lebih besar: membangun **standar, protokol, dan infrastruktur terbuka dan bersama untuk perangkat lunak yang bermanfaat secara sosial**, dengan penekanan khusus pada memungkinkan pengembang, akademisi, dan komunitas Muslim untuk berkolaborasi secara terbuka, sementara karyanya sendiri tetap dapat diakses oleh semua orang.

Ambisinya adalah agar universitas, peneliti, dan profesor yang memiliki teori tentang keuangan Islam, komputasi etis, jalur pembayaran halal, atau distribusi yang adil dapat mempublikasikan implementasi referensi yang dapat digunakan oleh pengembang mana pun, dengan atribusi yang tepat. Pull request, draf RFC, dan makalah akademik semuanya disambut baik.

Jika Anda membangun sesuatu yang sadar akan keuangan Islam, berfokus pada komunitas, atau selaras dengan nilai, dan Anda menemukan diri Anda menemukan kembali roda, di sinilah Anda membawa roda dan membiarkan orang lain menggunakannya.

## Apa yang ada di repo

```
open-charity-api/
├── README.md                     ← Dokumen utama (bahasa Inggris)
├── spec/openapi.yaml             ← Spesifikasi OpenAPI 3.1
├── postman/                      ← Koleksi Postman
├── docs/
│   ├── industry-analysis.md      ← Riset industri amal
│   ├── authentication.md         ← Tiga mode autentikasi
│   ├── gift-aid-and-tax.md       ← Gift Aid UK + skema internasional
│   ├── islamic-considerations.md ← Zakat, Sedekah, Kurban, Wakaf, dll.
│   ├── contributing.md           ← Cara berkontribusi
│   └── i18n/                     ← Terjemahan (folder ini)
└── examples/                     ← Contoh payload JSON
```

## Kategori donasi Islam yang didukung

| Tipe | Arti |
|---|---|
| `zakat` | Donasi tahunan wajib, diarahkan ke salah satu dari 8 kategori kanonik |
| `sadaqah` | Sedekah sukarela umum |
| `sadaqah_jariyah` | Sedekah berpahala berkelanjutan |
| `waqf` | Wakaf, modal permanen |
| `lillah` | "Lillahi taala", tidak memenuhi syarat Gift Aid jika kondisi tidak terpenuhi |
| `fidya` | Kompensasi (mis. puasa yang terlewat) |
| `kaffarah` | Kafarat |
| `qurbani` / `udhiyyah` | Kurban Idul Adha |
| `aqiqah` | Kurban kelahiran anak |
| `interest_purification` | Pembersihan riba, tidak dapat dideklarasikan sebagai Zakat |

Lihat `docs/islamic-considerations.md` untuk detail dan metadata yang diperlukan.

## Niat

Ini bukan produk komersial. Tidak ada perusahaan. Tidak ada biaya. Tujuannya adalah standar, milik semua orang dan tidak ada seorang pun, agar lembaga amal dan pengembang dapat bekerja sama tanpa gerbang berpemilik yang ekstraktif.

Jika berguna, adopsi. Jika ada yang salah, perbaiki. Jika ada yang hilang, tambahkan.

---

**Dokumentasi teknis lengkap dalam bahasa Inggris:** [`../../README.md`](../../README.md)
