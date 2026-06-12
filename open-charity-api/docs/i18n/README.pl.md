# Otwarty Standard API dla Organizacji Charytatywnych (OCAS)

> Otwarta, niezależna od dostawców specyfikacja dla API obsługujących darowizny.
> Stworzona po to, aby każda organizacja charytatywna, mały meczet, globalna organizacja pozarządowa, bank żywności, hospicjum, mogła zostać zintegrowana przez podmioty trzecie i programistów, w dowolnej aplikacji, w dowolnym miejscu na świecie.

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Spec: OpenAPI 3.1](https://img.shields.io/badge/Spec-OpenAPI_3.1-green.svg)](../../spec/openapi.yaml)
[![Status: Draft](https://img.shields.io/badge/Status-Draft_v0.1-orange.svg)](#)

**Przeczytaj w innym języku:** [English](../../README.md) · [العربية](README.ar.md) · [اردو](README.ur.md) · [Français](README.fr.md) · [Español](README.es.md) · [Türkçe](README.tr.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md) · [Polski](README.pl.md)

---

## Dlaczego to istnieje

Jeśli kiedykolwiek próbowałeś budować oprogramowanie komunikujące się z organizacjami charytatywnymi, prawdopodobnie zderzyłeś się z tym samym murem, co większość programistów: brakiem standardu. Każda fundacja, która udostępnia możliwość przyjmowania darowizn programowo, robi to inaczej. Większość nie udostępnia takiej opcji w ogóle. Organizacje polegają na platformach zewnętrznych (JustGiving, Donorbox, Enthuse, Fundraise Up, GoFundMe), z których każda ma własne interfejsy API, modele danych, metody uwierzytelniania i własne opłaty.

Ta fragmentacja ma swoją cenę:

- Programista, który chce dodać opcję "przekaż darowiznę na rzecz organizacji X" w swojej aplikacji, musi zintegrować się z N różnymi systemami.
- Organizacje charytatywne, których nie stać na płatną usługę platform, nie mają żadnego sposobu, by w sposób zintegrowany uzyskiwać wpłaty z pomocą API.
- Mniejsze organizacje, np. wyznaniowe, lokalne, oddolne są w rzeczywistości niewidoczne dla szerszego ekosystemu technologicznego.
- Standardowe koncepcje, takie jak Gift Aid, darowizny cykliczne, kategorie Zakat i wydawanie rachunków podatkowych, są powielane i implementowane (często źle) raz za razem przez kolejnych twórców oprogramowania zewnętrznego.

**Otwarty Standard API Organizacji Charytatywnych (OCAS)** to próba zniwelowania tego problemu. Jest to darmowa i otwarta specyfikacja techniczna, uchodząca za system z którego każda organizacja pożytku publicznego może odtąd korzystać dla ekspozycji i standardów swoich darowizn. Należą do nich: plany subsykrypcji, kampanie, paragony i procesy obsługi ulg finansowych poprzez ujednolicony i precyzyjnie wykonany w tym względzie model. Dowolna aplikacja może następnie skomunikować swoje oprogramowanie (tzw. "zintegrować się") w każdym ekosystemie przy użyciu tych samych ścieżek kodu, wspierając każdą placówkę posiadającą status działania zgodnie z wymaganiami "OCAS".

Ten projekt jest z założenia:

- **Niezależny od dostawców (Vendor-neutral).** Nie przypisany do systemu płatności Stripe, PayPal ani żadnego pojedynczego procesora płatniczego.
- **Neutralny światopoglądowo.** Działa równie dobrze z wdrożeniami dla świeckich form działalności tj. np. banków żywności podchodząc na tych samych fundamentach do instytucji wyznaniowych.
- **Zintegrowany z religijnym porządkiem.** Oferuje wsparcie bezpośrednio jako podstawowe klasy danych ("First-class support") dla takich darowizn jak: Zakat, Sadaqah, Waqf, Lillah, Fidya, Kaffarah, Qurbani, Aqiqah; uwzględniający tym samym formaty ulg: Gift Aid, 501(c)(3), DGR, ANBI oraz klasyfikacji zwolnień prawnych ulg o specyfice różnych krajów.
- **Możliwy do hostowania (Self-hostable).** Każda organizacja może wdrożyć serwer OCAS, lub poprosić zaufanego operatora IT o zintegrowanie u siebie. OCAS zdejmuje nacisk ze stworzenia scentralizowanego "HUB'a".


## Kto z tego korzysta?

| Jeśli jesteś... | OCAS daje ci... |
|---|---|
| **Organizacją charytatywną** | Specyfikację którą wdrożysz we własnym zakresie (lub wyślesz o jej obsługę prośbę do twórców CRM'a platformy, którą opłacasz), aby jakakolwiek nowa aplikacja potrafiła wtedy przekazać pod twoim patronatem środki na Twoje konto z systemu docelowego. |
| **Twórcą aplikacji** | Jeden zintegrowany, jednolity punkt wymiany informacji. Zaprogramuj interfejsy dla standardu OCAS we wdrożonej aplikacji w Twoim środowisku a zdobędziesz otwarte wrota na pobieranie wszystkich dopłat i wspieranie wszystkich operujących nim podmiotów w ułamku minuty. |
| **Dostawcą CRM / platformą do zbierania środków (Fundraising)** | Standardowy konektor (adapter integracyjny), uwalniający Twoich klientów od koniecznej platformizacji wyłącznie u jednego vendora (vendor-lock'in). |
| **Platformą badawczą lub środowiskiem akademickim** | Standardowy i estetycznie skonstruowany obieg plików, który pomoże zweryfikować badaczom np. wyznaczone cechy pod system zapobiegających praniu pieniędzy na celowości Zakat w środowiskach do dystrybucji na uczciwym środowisku dla celowości badawczych. |
| **Organem regulacyjnym** | Najlepszy wyznacznik techniczny jako audytowany dla ujednoliconego wprowadzania wytycznych pod standaryzacje w raporcie dla urzędników. |


## Szerszy aspekt: Fundacja (The Foundation)

OCAS jest innowacyjnym standardem opublikowanym pod organizacyjnym nadzorem **[The Foundation](../../../README.md)**. Otwartym źródłem na integracje pod szeroko promowanym światowym system rozwiązań non-profit, ze szczególnym poszanowaniem skupiającym się m.in na etycznie rozumianym wdrażaniu modeli oprogramowia udostępniającym technologię społecznościom muzułmańskich programistów, ale zbudowanym tak by przynosić na całym świecie pomoc. 

Nazwa jest z góry zaplanowana. *Foundation* występuje w kontekście `waqf`, stałego, publicznego funduszu wdrożeń technologicznych opartych na swodobnych zasobach. *Foundation (Fundacja)* w sensie elementarnego poziomu od oprogramowania tzw stosu to również: specyfikacje technicznych standardów bazowych używanych globalnie.

## Co znajduje się w tym katalogu

```
Foundation/                         <- katalog główny repozytorium
├── README.md                       <- o czym pisze The Foundation
├── LICENSE                         <- Licencja open source: Apache 2.0
├── NOTICE
├── CODE_OF_CONDUCT.md
├── .gitignore
│
└── open-charity-api/               <- jesteś tutaj
    ├── README.md
    ├── CHANGELOG.md
    ├── SECURITY.md
    ├── spec/
    │   └── openapi.yaml             <- Najnowsza formalnie dostępna na dany moment specyfikacja OpenAPI 3.1
    ├── postman/
    │   └── OCAS.postman_collection.json
    ├── docs/
    │   ├── industry-analysis.md     <- Wyjaśnia zbadane wybory projektowo-modelowe do bazy dla API. 
    │   ├── authentication.md        <- Proces uwierzytelniania np. Klucze dla procesów API Auth, protokołów OAuth, tryb public API.
    │   ├── gift-aid-and-tax.md      <- Zestawy wymogów regulaminu z instrukcjami z urzędów międzynarodowo: System Wielkiej Brytanii tzw. "UK Gift Aid" + itp. 
    │   ├── islamic-considerations.md <- Zakat, Sadaqah, Waqf, Qurbani, itp.
    │   ├── contributing.md          <- Jak wnosić we wdrożenia udoskonalać procedury wewnątrz kodu.
    │   └── i18n/                    <- Tłumaczenia README na m.in 7+ języków globalnych 
    └── examples/
        └── (gotowe wdrożone logiki schematów JSON)
```

## Szybki start (dla dewelopera odpowiedzialnego za integrację API)


Każda fundacja wspierana API i modelem OCAS posiada wymagany minimalny ten URL procesowy:

```
https://{domena-organizacji-charytatywnej}/api/ocas/v1
```

Najważniejszy proces we wsparciu to jedynie dwie odpowiednie dla środowisk zapytania (tzw HTTP kwerendy):

**1. Wyślij Get w API: zapytaj o podstawy (akcja publiczna/zweryfikuje organizacje)**:

```http
GET /charity
```
Możesz stąd zaczerpnąć rejestr wytycznych, numery u prawnej w publicznym państwowym systemie, np z Charity Commission za poparciem u EIN, czy u ABN dla upewnienia walut do systemów i wytycznych z deklaracji by przygotowanych w celu dla wsparcia w modelach.


**2. Wyślij dyspozycję "Wspieraj i wpłać datek - POST Donacja":**

```http
POST /donations
Content-Type: application/json
Authorization: Bearer {token}      # jeśli organizacja procesuje uwierzytelnianie jako wymóg w API; z wariantu 'public' do wyłączenia (omiń to jako pominięcie Headers)

{
  "amount": { "value": 5000, "currency": "GBP" },   // 5000 = £50.00 (wyliczona wartość pomniejszych bilonów np. pensów pod całościowej bazy)
  "donation_type": "sadaqah",
  "donor": {
    "email": "donor@example.com",
    "first_name": "Aisha",
    "last_name": "Khan",
    "address": { "line1": "...", "postcode": "...", "country": "GB" }
  },
  "gift_aid": { "declared": true, "declaration_text_version": "v1" },
  "campaign_id": "ramadan-2026",
  "anonymous": false,
  "message": "Za mojego zmarłego ojca, niech Bóg ma nad nim litość."
}
```

Organizacja procesuje to co wyślemy po operację dla `donation_id` z potwierdzaniami dla API by użyto z zapłat po `payment_intent` jakie z autoryzacją środowisk operatorów zweryfikują opłatę na fundacji, albo we standard autoryzacji systemu wyśle ci z wynikiem u `redirect_url` na adres do systemu zapłaty dedykowanego serwisu bramek.

Skondensowana referencja jest u u specyfikacji OpenAPI [`spec/openapi.yaml`](../../spec/openapi.yaml).


## Autoryzacja i Uwierzytelnienie w jednym słowie

Fundacje zarządzają OCAS w tych trzech znanych od wymiaru platform bezpieczeństwa w ścieżkach do udostępnień w API np `GET /charity`:

- `public`, to wariant dla procesu bez uciążliwego obowiązku udostępniania operacyjnej procedury uwierzytelnienia w zapytaniu `POST /donations`. Każdy opłaca datek. 
- `api_key`, w środowisku u klucza od API do wdrażających platform systemowych u np Headers u uwierzytelniaczy pod nagłówkami jako `Authorization: Bearer`. 
- `oauth2`, czyli uwierzytelnianie autoryzacja typu OAuth 2.0 z uwierzytelniającymi procesami z PKCE u logujących powiązań od wspierających systemów u fundacji we systemowych po autoryzacjach zwrotnych.

Zobacz detale na: [`docs/authentication.md`](../authentication.md).


## Ulgi podatkowe (Gift Aid itp.)

Platforma OCAS z modelem za specyfikację zwrotów i wydanych od pomocy podatkowych udostępnień po formularzach tzw dla `tax_relief_declaration`. Przykłady u wdrażeń "UK Gift Aid" (wsparciu u z Wielkiej Brytanii), lub USA deklarowanych jako tzw wpłaty paragonu dla standardów u podatkowych tzw wpisanych z preferencji w USA po `501(c)(3)`. Dodatkowo u Kanady ("CRA"), do w Niemiec od standardowych procesowanych i opłaconych w (Spendenbescheinigung), Irlandia w standardzie tzw CHY3/CHY4 pod tzw w m.in Holandii do tzw jako modelu procesu dla systemów (ANBI). Wytypowane z formatowaniem specyficznych państw we polach - Sprawdź dokument w pliku: [`docs/gift-aid-and-tax.md`](../gift-aid-and-tax.md).


## Islamskie kategorie darowizn

Dla wsparć po modelu "donation_type" w system podaje we wsparciu operacje pod kategorią u wdrażeń standard na proces od form donacji jak z wpłaty po: Zakat, Sadaqah, Sadaqah Jariyah, Lillah, Waqf, Fidya, Kaffarah, Qurbani/Udhiya, we odpowiedź pod opłatę jako Aqiqah z systemem dla `zakat_metadata` jako z 8 form dystrybucji na Asnaf. Mamy z zapytań wspierający model tzw `zakat/calculator` - Read on we środowisku [`docs/islamic-considerations.md`](../islamic-considerations.md). 

Fundacje z modelem uniwersalnej publicznej wpłaty "donacji ogólnej" ignorują owe islamskie wytyczne jako ominięcie na platformach ze specyfiki w udostępnień do ignorowanych z pól!


## Jak pomagać by wpierając wdrażać na poparcie rozbudowy u projektu?

Mamy po u systemowych od wytycznych pod to te 3 kroki wspierania:

1. **Stwórz "issue".** Czy widzisz błąd/brak pola certyfikatów we wdrażanym API we wytycznych z obcych regulacji prawnych od fundacji państw lub procesowany u tzw bug do z zgłoszeniu u błędu we platform.
2. **Otwarciu "pull request".** Tworzenie poprawek do np edycje innych dokumentów dla ujętych z udostępnionego procesu dla translacji języków w modelu docelowym, procedowanym dla u w wdrażeń u dla wsparcia w dokumentów państw ("ulgi z na Tax"). Wdrażaj ze standard technologicznymi we poprawkach na kod w oprogramowanie we u po kodowaniu we PR u na GitHubie (Pull z prośba). 
3. **Zostań Adaptowanym wspierającym.** Zaadaptuj organizacje do format OCAS by móc dołączyć do wspierania standard we tzw liście wdrażanych u organizacji wspierających m.in we plik `ADOPTERS.md`.


Obserwuj np na wymogi zgromadzone na pliku `docs/contributing.md` procedury wprowadzanych udokumentowanych procedowaniu zmian operacyjnych tzw kodów z breaking changes z np ("procedurami z na po dla u dla RFC udokumentowanych poprawach technicznej modyfikacji"). Zobacz plik: [`docs/contributing.md`](../contributing.md).

## Zarządzanie procesami pod Licencje 

Model OCAS pod kod autorski procedowany udostępnianiu we formacie udostępnione przez otwartą umowę od **Apache License 2.0**. Modele na po specyfikacji u wdrażań w po za dokumentacje API we np środowisko i darmowym modelu: "bez pobranych certyfikatów za komercją. Wdrażajcie, forknijcie lub w wdrażającym środowisku dla siebie osadź poprawiane na modyfikację pod API projekty by na m.in tzw wspierające proces jako (No royalties), u po we po zachowaniu tylko po z z nagłówek licencje za "nie podawaj u ze nas do udokumentowanego m.in procesu o sądu ze u tzw "don't sue us".

## Ważna refleksja celowości 

Projekt powstał w idei u dobrego wdrażania u we na darmowych w po w w fundament z wsparciu od infrastruktury we tj w po charytatywnie by we w ("sadaqah jariyah"- czyli ciągle charytatywne pomoce!). Wykonany nakład wsparcia i w otwarte wspieranej np do wdrażaniu ze procedur u by pomoc łatwiej (z od i np techniczna obrotowa system wspierania społeczność po). Tak by dany z wsparciu dolar, wymiana by wpłacono czy to we w a rupie trafio bezpiecznie ze 2 komunikujących środowisku wsparcia w system po platform! 

---

**Operatorzy projektu (Maintainers):** czytaj referencyjnych na [`MAINTAINERS.md`](MAINTAINERS.md) *(we procedur u jako "do dołożenia we dla by po pod od osoby we")*
**Zgłoszenie procedur we ostrzeżeń u bezpieczeństwa "Security":** od na u na we  [`SECURITY.md`](SECURITY.md) *(w krótkim na jako tzw we a (w ang- coming soon))*
**Zasady postępowania wspierających na Code of conduct:** czyli od po i pakt z na - [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) *(w procedur by do w we w/ wkrotce z na z ang (coming soon, za: Contributor Covenant))*
