# Guía del material para el portfolio

Cómo tener preparado cada proyecto para meterlo en el portfolio: qué archivos, en qué formato, a qué medida y cómo se rellena la ficha.

---

## 1. Cómo se añade un proyecto (resumen)

1. Crea una carpeta `img/<id>/` con todas sus imágenes. El `id` es el nombre corto del proyecto (`pegopadel`, `grupohogares`…).
2. Añade su ficha en `proyectos.json`, copiando la de Pàdel Pego y cambiando lo que toque.
3. Ejecuta `python generar.py` en esta carpeta.
4. Se crean solos `index.html`, con la tarjeta nueva, y `<id>.html`, con su página.

El orden de los proyectos en `proyectos.json` es el orden de la portada. **El primero sale en grande.**

> No edites `index.html` ni las páginas de proyecto a mano: se sobrescriben cada vez que generas. Lo que se edita es `proyectos.json`, `plantillas/portada.html` y `estilos.css`.

---

## 2. Reglas para todos los archivos

| Regla | Detalle |
|---|---|
| **Nombres** | En minúsculas, sin espacios ni acentos, con guiones: `dia-de-partit.jpg` y no `Día de Partit.JPG` |
| **Fotos, capturas y carteles** | JPG, calidad 80–85 % |
| **Logos e iconos** | SVG, siempre en vector y con el texto convertido en curvas |
| **PNG** | Solo si hace falta transparencia; si no, JPG (pesa mucho menos) |
| **Color** | sRGB. Nada de CMYK, que en pantalla sale apagado |
| **Ancho máximo** | 2000 px. Más no se ve mejor y la web va más lenta |
| **Peso** | Ideal menos de 300 KB por imagen, nunca más de 600 KB |
| **Proporción exacta** | Exporta justo a la medida que pide cada bloque. Si sobra, la web recorta por el centro y puede cortarte un texto |

Si no puedes ajustar la medida o el peso, déjame los originales en la carpeta y los reduzco yo.

---

## 3. Bloques de un proyecto

Todos los proyectos tienen la **cabecera**, la **ficha con el texto** y el **siguiente proyecto**. Además llevan uno o varios bloques opcionales, según lo que hayas hecho:

| Si el proyecto es… | Bloques |
|---|---|
| Solo una web o landing | Pantallas |
| Solo carteles | Piezas (A3) |
| Landing y redes sociales | Pantallas + Piezas (post) + Piezas (story) |
| Solo una marca | Identidad |
| Marca, carteles y web (como Pàdel Pego) | Identidad + Piezas + Pantallas |

Puedes repetir un bloque: por ejemplo, dos bloques de piezas, uno de publicaciones y otro de stories. El orden en la ficha es el orden en la página.

---

## 4. Textos de la ficha

| Campo | Qué poner | Largo |
|---|---|---|
| `titulo` | Nombre del proyecto | 1 a 3 palabras |
| `lema` | Qué es, en una frase | Hasta unos 60 caracteres |
| `anio` | Año | `2026` |
| `tipo` | `Proyecto propio`, `Encargo` o `En empresa` | 1 a 3 palabras |
| `hice` | Lo que hiciste (también sale bajo la tarjeta de la portada) | 2 a 4 cosas cortas |
| `con` | Herramientas | 2 a 4 |
| `texto` | La idea: qué hacía falta y cómo lo resolviste | 1 o 2 párrafos, unas 60–80 palabras en total |
| `redes` | Redes del proyecto, si tiene: `[{"nombre": "Instagram", "url": "…"}]` | Opcional; salen en la ficha |
| `enlace` | La web del proyecto | Solo si **no** hay bloque de pantallas, porque ese ya lleva su enlace |

No repitas en el texto lo que ya dicen la ficha o los bloques («hice el logo, los carteles…»). Cuenta la idea.

---

## 5. Identidad

### Logo — `img/<id>/logo.svg`
- **Exportarlo de Affinity:** Archivo › Exportar › SVG, con «Rasterizar: nada», el texto en curvas y «Usar viewBox» marcado. Sin fondo.
- **Hazlo en negro.** Yo lo preparo para que cambie de color en cada versión. Si tiene partes de otro color (como la pelota de pegopadel), dímelo y las separo en variables.
- **Recórtalo justo al logo**, sin margen alrededor.

### O logo de texto (sin SVG)
Si el logo es solo texto con una fuente de Google Fonts (como Typeroll), no hace falta exportarlo: en la ficha se pone `logo_texto` con cada parte y su estilo. Se pinta con la letra real. Mira la ficha de Typeroll.

### Versiones de color
Para cada versión, en la ficha: nombre, color de fondo y color del logo. Lo normal son entre 3 y 6:
- **Principal:** la oficial.
- **En negativo:** claro sobre oscuro.
- **A una tinta:** todo de un color.
- **Sobre otros colores de la paleta.**

### Icono (opcional) — `img/<id>/icono.svg`
El símbolo o la versión reducida del logo, en vector y **cuadrado**. Si solo lo tienes en PNG (como el favicon), vale un `icono.png` de al menos 256 × 256 px con fondo transparente.

### Colores
Nombre y código hexadecimal (`#E9F542`). Entre 3 y 8. El color del texto encima de cada muestra se elige solo.

### Tipografías
Para cada una:
- **Nombre y uso:** «Instrument Serif» · «Titulares».
- **Muestra:** una frase corta del propio proyecto, mejor que «Aa».
- **Dónde está la fuente:**
  - si está en Google Fonts, su nombre, como `Unbounded:wght@700`;
  - si no, el archivo `.woff2` u `.otf` en `fuentes/`. Comprueba antes que la licencia deja usarla en web.

---

## 6. Piezas (carteles, publicaciones, stories…)

Cada bloque de piezas tiene **un solo formato**. Si tienes carteles y stories, van en dos bloques. Al pulsar una pieza se abre en grande, así que **expórtalas con buena resolución y legibles**.

| Formato | Proporción | Medida de exportación | Cuántas quedan bien |
|---|---|---|---|
| `a3`: carteles, flyers, cualquier A | 1 : 1,414 (A3, A4…) | **1000 × 1414 px** | 3 a 6 |
| `post`: publicación de Instagram | 4 : 5 | **1080 × 1350 px** | 6 o 12, que van de 6 en 6 |
| `retrato`: publicación 3:4 (la cuadrícula nueva de Instagram) | 3 : 4 | **900 × 1200 px** (de originales 1080 × 1440) | 6, 12 o 18, de 6 en 6 |
| `story`: stories, reels, TikTok | 9 : 16 | **1080 × 1920 px** | 5 o 10, de 5 en 5 |
| `cuadrado`: post cuadrado, tarjeta | 1 : 1 | **1080 × 1080 px** | 4 u 8, de 4 en 4 |

- **Desde Affinity:** exporta la mesa de trabajo entera en JPG, ajustando el ancho a la medida de la tabla. Los carteles de Pàdel Pego salen de mesas de 3508 × 4961 reducidas a 1000 de ancho.
- **Cada pieza lleva un nombre corto**, que sale debajo y en el visor: «Dia de partit».
- **Un formato que no esté en la tabla** (horizontal, banner, valla…): dímelo y añado el formato a la plantilla.

---

## 7. Pantallas (webs y apps)

| Archivo | Proporción | Medida | Qué captura |
|---|---|---|---|
| `escritorio` | 16 : 10 | **1600 × 1000 px** | La primera pantalla de la web en un ordenador de 1440 × 900 |
| `movil` | 390 : 844 | **780 × 1688 px** | La primera pantalla en un móvil de 390 × 844 a doble resolución |
| `secciones` (opcional) | 16 : 10 | **1600 × 1000 px** | Otras partes de la web: servicios, contacto… Mejor de 3 en 3 |

- **Antes de capturar:**
  - quita el aviso de cookies y los pop-ups;
  - espera a que carguen las fuentes y las imágenes;
  - pon contenido real, nada de «Lorem ipsum».
- **Sin la barra del navegador**, solo la página. Las esquinas redondas y la sombra las pone el portfolio.
- **Cómo capturar:**
  - en Chrome: F12 › icono del móvil › elige el tamaño › menú ⋮ › «Capture screenshot»;
  - o pídemelo: si la web está publicada, la capturo yo con las medidas exactas.
- **Áreas privadas o CRM:** captura con datos de prueba, nunca con datos de clientes reales.
- **App sin versión de escritorio** (como Rogue): captura varias pantallas a 780 × 1688 px y dímelo. Hace falta un formato «móvil» en piezas, que aún no existe, y lo añado.

---

## 8. Tarjeta de la portada

Cada proyecto elige cómo se ve su tarjeta, sin necesidad de material nuevo:

| `tipo` | Qué muestra | Material |
|---|---|---|
| `carteles` | Una fila de 3 a 5 piezas verticales sobre un color | Las mismas imágenes del bloque de piezas, más un `fondo` |
| `pantalla` | Una captura de la web sobre un color | La imagen `escritorio`, más un `fondo` |
| `logo` | El logo grande sobre su color | Sale solo de la primera versión de la identidad |
| `foto` | Una imagen a sangre | **1600 × 1200 px** (4 : 3); si el proyecto va el primero, en grande, **2400 × 1000 px** |

---

## 9. Archivo (imágenes sueltas)

Para cosas que no son un proyecto: un cartel suelto, una prueba, una ilustración, una foto… Salen en la portada, en la sección **Archivo**, en mosaico y sin recortar: cada imagen mantiene su proporción. Al pulsar se abren en grande.

- **Imágenes:** en `img/archivo/`, en JPG (PNG solo si tiene transparencia), con el lado largo de **1600 px como máximo** y menos de 400 KB. Cualquier proporción vale.
- **Ficha:** en `proyectos.json`, al mismo nivel que `"proyectos"`, una lista `"archivo"`. Una línea por imagen; el año es opcional. Arriba lo más nuevo.

```json
"archivo": [
  { "imagen": "img/archivo/cartel-trail.jpg", "nombre": "Pego Trail", "anio": 2026 },
  { "imagen": "img/archivo/prueba-tipografica.jpg", "nombre": "Prueba tipográfica" }
]
```

Mientras la lista esté vacía o no exista, la sección y su enlace del menú no aparecen.

---

## 10. Lista antes de generar

- [ ] Carpeta `img/<id>/` con nombres en minúsculas, sin espacios ni acentos
- [ ] Cada imagen a su medida y por debajo de 600 KB
- [ ] Logo e icono en SVG con texto en curvas
- [ ] Ficha en `proyectos.json`: título, lema, año, tipo, qué hice, con qué y texto
- [ ] Cada pieza con nombre
- [ ] Capturas sin avisos de cookies ni datos reales de clientes
- [ ] `python generar.py`: si falta algún archivo, el script avisa y no genera nada
