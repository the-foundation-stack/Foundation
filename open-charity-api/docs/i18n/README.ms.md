# Open Charity API Standard (OCAS)

> Spesifikasi terbuka dan neutral untuk API derma badan kebajikan.
> Direka supaya mana-mana badan kebajikan — masjid kecil, NGO antarabangsa, bank makanan, atau pusat perlindungan — boleh berintegrasi dengan mana-mana aplikasi, yang dibina oleh mana-mana pembangun, di mana-mana sahaja di dunia.

---

## Mengapa projek ini wujud

Jika anda pernah cuba membina perisian yang berkomunikasi dengan badan kebajikan, anda mungkin menemui masalah yang sama seperti kebanyakan pembangun: **tiada piawaian bersama.** Badan kebajikan yang menawarkan cara berprogram untuk menerima derma melakukannya mengikut cara masing-masing. Dan kebanyakannya tidak menawarkan apa-apa — mereka bergantung pada platform pihak ketiga (JustGiving, Donorbox, GoFundMe, Enthuse) yang setiap satunya mempunyai antara muka sendiri, model data sendiri, dan caj sendiri.

Pemecahan ini ada kosnya:

- Pembangun yang ingin menambah ciri "derma kepada Badan X" dalam aplikasinya terpaksa berintegrasi dengan N sistem berbeza.
- Badan kebajikan yang tidak mampu membayar platform berbayar tertinggal daripada dunia teknologi.
- Badan kebajikan Islam kecil dan berasaskan komuniti hampir tidak kelihatan dalam ekosistem perisian yang lebih luas.
- Konsep piawai seperti Gift Aid, derma berulang, pengkategorian Zakat, resit cukai dibina semula (dengan tidak elok) setiap kali.

**OCAS** adalah percubaan untuk menyelesaikan ini. Ia adalah spesifikasi percuma dan terbuka yang boleh diterima pakai oleh mana-mana badan kebajikan untuk mendedahkan derma, langganan, kempen, resit, dan pengisytiharan pelepasan cukai mereka dalam bentuk piawai. Mana-mana aplikasi kemudiannya boleh berintegrasi dengan mana-mana badan kebajikan yang patuh OCAS menggunakan laluan kod yang sama.

Projek ini sengaja:

- **Neutral terhadap vendor.** Tidak terikat dengan Stripe, PayPal, atau pemproses tertentu.
- **Neutral dari segi agama dan ideologi di permukaan.** Berfungsi sama baik untuk bank makanan sekular dan masjid.
- **Memahami agama apabila perlu.** Sokongan kelas pertama untuk Zakat, Sedekah, Sedekah Jariah, Wakaf, Lillah, Fidyah, Kifarat, Korban, Akikah — bersama Gift Aid, 501(c)(3), DGR, ANBI, dan skim pelepasan cukai lain.
- **Boleh dihos sendiri.** Setiap badan kebajikan boleh menjalankan OCAS pada pelayan mereka sendiri. Tiada autoriti pusat. Tiada hab wajib.

## Visi yang lebih luas

OCAS ialah projek pertama daripada usaha yang lebih besar: membina **piawaian, protokol, dan infrastruktur terbuka dan dikongsi untuk perisian yang bermanfaat secara sosial**, dengan penekanan khusus untuk membolehkan pembangun, ahli akademik, dan komuniti Muslim berkolaborasi secara terbuka — sementara karya itu sendiri kekal boleh diakses oleh semua orang.

Cita-citanya ialah agar universiti, penyelidik, dan profesor yang mempunyai teori tentang kewangan Islam, pengkomputeran beretika, laluan pembayaran halal, atau pengagihan adil dapat menerbitkan pelaksanaan rujukan yang boleh dibangunkan oleh mana-mana pembangun, dengan atribusi yang sewajarnya. Pull request, draf RFC, dan kertas akademik semuanya dialu-alukan.

Jika anda sedang membina sesuatu yang sedar tentang kewangan Islam, berfokus komuniti, atau selaras dengan nilai, dan anda mendapati diri anda mencipta semula roda, di sinilah anda membawa roda itu dan membiarkan orang lain menggunakannya.

## Apa yang ada dalam repo

```
open-charity-api/
├── README.md                     ← Dokumen utama (Bahasa Inggeris)
├── spec/openapi.yaml             ← Spesifikasi OpenAPI 3.1
├── postman/                      ← Koleksi Postman
├── docs/
│   ├── industry-analysis.md      ← Penyelidikan industri kebajikan
│   ├── authentication.md         ← Tiga mod pengesahan
│   ├── gift-aid-and-tax.md       ← Gift Aid UK + skim antarabangsa
│   ├── islamic-considerations.md ← Zakat, Sedekah, Korban, Wakaf, dll.
│   ├── contributing.md           ← Cara menyumbang
│   └── i18n/                     ← Terjemahan (folder ini)
└── examples/                     ← Contoh muatan JSON
```

## Kategori derma Islam yang disokong

| Jenis | Maksud |
|---|---|
| `zakat` | Derma tahunan wajib, ditujukan kepada salah satu daripada 8 kategori kanonik |
| `sadaqah` | Sedekah sukarela umum |
| `sadaqah_jariyah` | Sedekah berpahala berterusan |
| `waqf` | Wakaf, modal kekal |
| `lillah` | "Kerana Allah", tidak layak Gift Aid jika syarat tidak dipenuhi |
| `fidya` | Pampasan (cth. puasa tertinggal) |
| `kaffarah` | Kifarat |
| `qurbani` / `udhiyyah` | Korban Aidiladha |
| `aqiqah` | Korban kelahiran anak |
| `interest_purification` | Pembersihan riba, tidak boleh diisytiharkan sebagai Zakat |

Lihat `docs/islamic-considerations.md` untuk butiran dan metadata yang diperlukan.

## Niat

Ini bukan produk komersial. Tiada syarikat. Tiada caj. Matlamatnya ialah satu piawaian — milik semua orang dan bukan milik sesiapa — supaya badan kebajikan dan pembangun boleh bekerjasama tanpa gerbang berhakmilik yang mengeksploitasi.

Jika ia berguna, gunakan. Jika ada yang salah, betulkan. Jika ada yang kurang, tambahkan.

---

**Dokumentasi teknikal lengkap dalam Bahasa Inggeris:** [`../../README.md`](../../README.md)
