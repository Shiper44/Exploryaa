# Publicar la web de Exploryaa

La web está en la carpeta `web/` y funciona sin servidor propio:

- **Formulario:** envía cada solicitud a Google Apps Script (`integraciones/google-apps-script/`). Este la guarda en Google Sheets y en Notion, manda la confirmación al cliente y te avisa a ti.
- **Pago:** no se cobra en la web. El cliente paga cuando acepta la propuesta, con un enlace de pago que le envías tú (por ejemplo, un *Payment Link* de Stripe).
- **Alojamiento:** Netlify, gratis, con HTTPS y tu dominio. El archivo `netlify.toml` hace que solo se publique la carpeta `web/`. El código del agente y los documentos no se publican.

```
web/
├── index.html          ← la web (configuración al final, en EXPLORYAA_CONFIG)
├── 404.html            ← página de "no encontrada"
├── robots.txt, sitemap.xml
├── logo.png, favicon.png, apple-touch-icon.png, og-image.png
└── legal/              ← aviso legal, privacidad, condiciones, cookies
```

## 1. Antes de publicar (lista de comprobación)

1. **Logo:** ya está en `web/logo.png` (recortado, con fondo transparente). También hay `favicon.png`, `apple-touch-icon.png` (el avión) y `og-image.png` (el logo cuadrado para compartir en redes).
2. **Configuración:** en `web/index.html` busca `EXPLORYAA_CONFIG` y rellena lo siguiente:
   - `precios`: cámbialos solo aquí. Pon `null` para que se muestre `[PRECIO] €`.
   - `telefono`, `registroAgencia` y `redes`: lo que dejes vacío no aparece en la web.
   - `plausibleDomain` o `ga4Id` si quieres analítica (más abajo, en el apartado 4).
3. **Textos legales:** en los 4 archivos de `web/legal/`, rellena todo lo que está `[ENTRE CORCHETES]`. También el bloque «Responsable» del paso 3 del formulario, en `web/index.html` (busca `[NOMBRE O RAZÓN SOCIAL]`). **Haz que un asesor los revise.** Vender vuelo + hotel juntos es un viaje combinado: exige estar inscrito como agencia y tener garantía de insolvencia.
4. **Dominio:** si tu dominio no es `exploryaa.com`, sustitúyelo en `web/index.html` (cabecera), `web/robots.txt`, `web/sitemap.xml` y en la línea `canonical` de cada página legal.
5. **Fotos:** las de Unsplash son de ejemplo. Puedes dejarlas o cambiarlas por fotos propias.
6. **Prueba el formulario:** abre la URL de Apps Script en el navegador. Debe responder `{"ok":true,...}`. Después envía una solicitud de prueba desde la web.

## 2. Publicar en Netlify (10 minutos)

1. Entra en <https://app.netlify.com> y crea una cuenta con tu GitHub.
2. **Add new site › Import an existing project › GitHub** y elige el repositorio `exploryaa`. Si es privado, autoriza a Netlify a verlo.
3. Netlify lee `netlify.toml` solo. Deja *Build command* vacío y *Publish directory* en `web`. Pulsa **Deploy**.
4. En un minuto tendrás la web en una dirección del tipo `https://nombre-aleatorio.netlify.app`. Cámbiale el nombre en **Site configuration › Change site name**.
5. Cada vez que subas cambios a la rama principal de GitHub, Netlify vuelve a publicar la web automáticamente.

*Alternativa sin GitHub:* en **Add new site › Deploy manually** arrastra la carpeta `web` a la página.

## 3. Conectar tu dominio

1. En Netlify: **Domain management › Add a domain** y escribe tu dominio (por ejemplo, `exploryaa.com`).
2. Netlify te dará una de estas dos opciones:
   - **Usar los DNS de Netlify (recomendado):** en el panel de la empresa donde compraste el dominio (GoDaddy, IONOS, DonDominio…), cambia los *servidores DNS* por los 4 que te indica Netlify.
   - **Mantener tus DNS:** crea un registro `A` para `@` que apunte a `75.2.60.5` y un `CNAME` para `www` que apunte a `tu-sitio.netlify.app`. Usa los valores exactos que muestre Netlify.
3. Espera a que se propague: de unos minutos a 24 horas. Netlify activa HTTPS (el candado) automáticamente.
4. Comprueba que `https://tudominio.com` y `https://www.tudominio.com` abren la web.

## 4. Analítica (opcional)

- **Plausible** (de pago, sin cookies): crea tu sitio en plausible.io y pon tu dominio en `plausibleDomain`. No hace falta aviso de cookies.
- **Google Analytics 4** (gratis, con cookies): pon el ID `G-XXXXXXX` en `ga4Id`. La web mostrará automáticamente el aviso de cookies y solo cargará Analytics si el visitante acepta. También aparecerá el enlace «Configurar cookies» en el pie.

Se miden estos eventos: `inicio_formulario`, `paso_formulario` y `solicitud_enviada`.

## 5. Después de publicar

1. Da de alta la web en **Google Search Console** y envía `https://tudominio.com/sitemap.xml`.
2. Comprueba la vista previa al compartir en WhatsApp o redes. Usa `og-image.png`; si quieres una imagen mejor, crea una de 1200×630 px y cambia esa línea.
3. Sustituye los testimonios de ejemplo por opiniones reales en cuanto las tengas.
