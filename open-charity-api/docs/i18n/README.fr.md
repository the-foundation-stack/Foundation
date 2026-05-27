# Open Charity API Standard (OCAS)

> Une spécification ouverte et neutre pour les API de dons des organisations caritatives.
> Conçue pour que n'importe quelle association — petite mosquée, ONG internationale, banque alimentaire, refuge — puisse s'intégrer à n'importe quelle application, créée par n'importe quel développeur, n'importe où dans le monde.

---

## Pourquoi ce projet existe

Si vous avez déjà essayé de construire un logiciel qui dialogue avec des associations caritatives, vous vous êtes probablement heurté au même problème que la plupart des développeurs : **il n'existe aucun standard commun.** Les associations qui proposent une manière programmatique d'accepter les dons le font chacune à leur façon. Et la plupart n'en proposent aucune — elles s'appuient sur des plateformes tierces (JustGiving, Donorbox, GoFundMe, Enthuse), chacune avec sa propre interface, son propre modèle de données et ses propres frais.

Cette fragmentation a un coût :

- Le développeur qui veut ajouter une fonctionnalité « faire un don à l'association X » dans son application doit s'intégrer à N systèmes différents.
- Les associations qui ne peuvent pas se permettre les plateformes payantes restent en marge de l'écosystème technologique.
- Les petites associations musulmanes et communautaires sont quasi invisibles dans l'écosystème logiciel élargi.
- Des concepts standard comme le Gift Aid, les dons récurrents, la catégorisation de la Zakât, les reçus fiscaux sont reconstruits (mal) à chaque fois.

**OCAS** est une tentative de résoudre cela. C'est une spécification libre et ouverte que n'importe quelle association peut adopter pour exposer ses dons, abonnements, campagnes, reçus et déclarations d'allègement fiscal dans un format standard. N'importe quelle application peut alors s'intégrer à n'importe quelle association conforme à OCAS en utilisant le même code.

Ce projet est délibérément :

- **Neutre vis-à-vis des fournisseurs.** Pas lié à Stripe, PayPal, ou un processeur particulier.
- **Religieusement et idéologiquement neutre en surface.** Fonctionne aussi bien pour une banque alimentaire laïque que pour une mosquée.
- **Religieusement informé là où c'est nécessaire.** Support de premier ordre pour la Zakât, la Sadaqa, le Sadaqa Jariya, le Waqf, le Lillah, la Fidya, la Kaffara, le Qurbani, l'Aqiqa — aux côtés du Gift Aid, du 501(c)(3), du DGR, de l'ANBI et d'autres dispositifs d'allègement fiscal.
- **Auto-hébergeable.** Chaque association peut faire tourner OCAS sur ses propres serveurs. Aucune autorité centrale. Aucun hub obligatoire.

## La vision plus large

OCAS est le premier projet d'un effort plus vaste : construire des **standards, protocoles et infrastructures ouverts et partagés pour des logiciels socialement bénéfiques**, avec un accent particulier sur la possibilité pour les développeurs, universitaires et communautés musulmans de collaborer ouvertement — tout en gardant le travail lui-même accessible à tous.

L'ambition est que des universités, chercheurs et professeurs ayant des théories sur la finance islamique, l'informatique éthique, les rails de paiement halal ou la distribution équitable puissent publier des implémentations de référence sur lesquelles tout développeur peut s'appuyer, avec attribution appropriée. Les pull requests, projets de RFC et articles académiques sont tous les bienvenus.

Si vous construisez quelque chose de conscient de la finance islamique, axé sur la communauté, ou aligné sur des valeurs, et que vous vous retrouvez à réinventer la roue, c'est ici qu'il faut apporter la roue et laisser les autres l'utiliser.

## Ce que contient le dépôt

```
open-charity-api/
├── README.md                     ← Document principal (anglais)
├── spec/openapi.yaml             ← Spécification OpenAPI 3.1
├── postman/                      ← Collection Postman
├── docs/
│   ├── industry-analysis.md      ← Recherche sur le secteur caritatif
│   ├── authentication.md         ← Trois modes d'authentification
│   ├── gift-aid-and-tax.md       ← Gift Aid UK + dispositifs internationaux
│   ├── islamic-considerations.md ← Zakât, Sadaqa, Qurbani, Waqf, etc.
│   ├── contributing.md           ← Comment contribuer
│   └── i18n/                     ← Traductions (ce dossier)
└── examples/                     ← Exemples de charges JSON
```

## Catégories de dons islamiques prises en charge

| Type | Signification |
|---|---|
| `zakat` | Don annuel obligatoire, vers l'une des 8 catégories canoniques |
| `sadaqah` | Charité volontaire générale |
| `sadaqah_jariyah` | Charité à récompense continue |
| `waqf` | Dotation, capital permanent |
| `lillah` | « Pour Allah », non éligible au Gift Aid si conditions non remplies |
| `fidya` | Compensation (par ex. jeûnes manqués) |
| `kaffarah` | Expiation |
| `qurbani` / `udhiyyah` | Sacrifice de l'Aïd al-Adha |
| `aqiqah` | Sacrifice à la naissance d'un enfant |
| `interest_purification` | Purification du Riba, ne peut être déclarée comme Zakât |

Voir `docs/islamic-considerations.md` pour les détails et les métadonnées requises.

## L'intention

Ceci n'est pas un produit commercial. Il n'y a pas d'entreprise. Il n'y a pas de frais. L'objectif est un standard — appartenant à tout le monde et à personne — pour que les associations et les développeurs puissent collaborer sans passerelles propriétaires extractives.

Si c'est utile, adoptez-le. Si quelque chose ne va pas, corrigez-le. Si quelque chose manque, ajoutez-le.

---

**Documentation technique complète en anglais :** [`../../README.md`](../../README.md)
