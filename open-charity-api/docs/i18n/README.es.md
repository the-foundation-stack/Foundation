# Open Charity API Standard (OCAS)

> Una especificación abierta y neutral para las APIs de donaciones de organizaciones benéficas.
> Diseñada para que cualquier entidad, una mezquita pequeña, una ONG internacional, un banco de alimentos o un albergue, pueda integrarse con cualquier aplicación, creada por cualquier desarrollador, en cualquier lugar del mundo.

---

## Por qué existe este proyecto

Si alguna vez has intentado construir software que se comunique con organizaciones benéficas, probablemente te hayas encontrado con el mismo problema que la mayoría de desarrolladores: **no existe un estándar común.** Las entidades que ofrecen alguna forma programática de aceptar donaciones lo hacen cada una a su manera. Y la mayoría no ofrecen nada, dependen de plataformas de terceros (JustGiving, Donorbox, GoFundMe, Enthuse), cada una con su propia interfaz, su propio modelo de datos y sus propias tarifas.

Esta fragmentación tiene un coste:

- El desarrollador que quiere añadir una funcionalidad de "donar a la organización X" dentro de su aplicación debe integrarse con N sistemas distintos.
- Las entidades que no pueden pagar plataformas comerciales quedan fuera del mundo tecnológico.
- Las organizaciones islámicas y comunitarias pequeñas son casi invisibles en el ecosistema de software general.
- Conceptos estándar como Gift Aid, donaciones recurrentes, categorización del Zakat o recibos fiscales se reconstruyen (mal) una y otra vez.

**OCAS** es un intento de resolverlo. Es una especificación libre y abierta que cualquier organización benéfica puede adoptar para exponer sus donaciones, suscripciones, campañas, recibos y declaraciones de desgravación fiscal en un formato estándar. Luego cualquier aplicación puede integrarse con cualquier entidad compatible con OCAS usando el mismo código.

Este proyecto es deliberadamente:

- **Neutral respecto a proveedores.** No está atado a Stripe, PayPal ni a ningún procesador en concreto.
- **Religiosa e ideológicamente neutral en su superficie.** Funciona igual de bien para un banco de alimentos laico o para una mezquita.
- **Religiosamente informado donde importa.** Soporte de primera clase para Zakat, Sadaqah, Sadaqah Jariyah, Waqf, Lillah, Fidya, Kaffarah, Qurbani, Aqiqah, junto con Gift Aid, 501(c)(3), DGR, ANBI y otras desgravaciones fiscales.
- **Autohospedable.** Cada entidad puede ejecutar OCAS en sus propios servidores. No hay autoridad central. No hay hub obligatorio.

## La visión más amplia

OCAS es el primer proyecto de un esfuerzo mayor: construir **estándares, protocolos e infraestructura abiertos y compartidos para software socialmente beneficioso**, con un énfasis particular en permitir que desarrolladores, académicos y comunidades musulmanes colaboren abiertamente, manteniendo el trabajo en sí accesible a todos.

La ambición es que universidades, investigadores y profesores con teorías sobre finanzas islámicas, computación ética, vías de pago halal o distribución justa puedan publicar implementaciones de referencia sobre las que cualquier desarrollador pueda construir, con la debida atribución. Los pull requests, borradores de RFC y artículos académicos son todos bienvenidos.

Si estás construyendo algo consciente de las finanzas islámicas, orientado a la comunidad o alineado con valores, y te encuentras reinventando la rueda, este es el lugar para traer la rueda y dejar que otros la usen.

## Qué hay en el repositorio

```
open-charity-api/
├── README.md                     ← Documento principal (inglés)
├── spec/openapi.yaml             ← Especificación OpenAPI 3.1
├── postman/                      ← Colección de Postman
├── docs/
│   ├── industry-analysis.md      ← Investigación sobre el sector benéfico
│   ├── authentication.md         ← Tres modos de autenticación
│   ├── gift-aid-and-tax.md       ← Gift Aid del Reino Unido + esquemas internacionales
│   ├── islamic-considerations.md ← Zakat, Sadaqah, Qurbani, Waqf, etc.
│   ├── contributing.md           ← Cómo contribuir
│   └── i18n/                     ← Traducciones (esta carpeta)
└── examples/                     ← Ejemplos de payloads JSON
```

## Categorías islámicas de donación soportadas

| Tipo | Significado |
|---|---|
| `zakat` | Donación anual obligatoria, dirigida a una de las 8 categorías canónicas |
| `sadaqah` | Caridad voluntaria general |
| `sadaqah_jariyah` | Caridad de recompensa continua |
| `waqf` | Dotación, capital permanente |
| `lillah` | "Por Allah", no elegible para Gift Aid si no se cumplen las condiciones |
| `fidya` | Compensación (p. ej. ayunos perdidos) |
| `kaffarah` | Expiación |
| `qurbani` / `udhiyyah` | Sacrificio de Eid al-Adha |
| `aqiqah` | Sacrificio por nacimiento de un hijo |
| `interest_purification` | Purificación del Riba, no puede declararse como Zakat |

Consulta `docs/islamic-considerations.md` para detalles y metadatos requeridos.

## La intención

Esto no es un producto comercial. No hay empresa. No hay tarifas. El objetivo es un estándar, propiedad de todos y de nadie, para que las organizaciones benéficas y los desarrolladores puedan colaborar sin pasarelas propietarias extractivas.

Si es útil, adóptalo. Si algo está mal, arréglalo. Si algo falta, añádelo.

---

**Documentación técnica completa en inglés:** [`../../README.md`](../../README.md)
