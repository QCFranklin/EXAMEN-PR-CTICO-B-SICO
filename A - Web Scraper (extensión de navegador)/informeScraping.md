# Informe sobre Web Scraping: Extracción de datos de *Books to Scrape*

## 1. Introducción

El web scraping es una técnica automatizada para extraer información estructurada de sitios web. En este proyecto, se utilizó la extensión **Web Scraper** del navegador para recolectar datos de [https://books.toscrape.com/](https://books.toscrape.com/), un sitio educativo diseñado explícitamente para practicar scraping. Se extrajeron ≥200 registros con los campos: título, precio, calificación (rating), categoría y enlace del libro, mediante un sitemap con paginación y navegación jerárquica por categorías.

## 2. Consideraciones éticas

El scraping debe realizarse con responsabilidad. En este caso:

- El sitio **no contiene datos sensibles ni personales**; su propósito es didáctico.
- No se extrajeron más datos de los necesarios (solo 200+ libros de ~1000 disponibles).
- No se realizó scraping agresivo: se respetó el flujo natural de navegación y no se sobrecargó el servidor.
- El sitio **permite explícitamente el scraping** (ver sección *robots.txt*).

Estas prácticas garantizan que la recolección sea **ética, transparente y no intrusiva**.

## 3. Análisis de `robots.txt`

El archivo `robots.txt` del sitio ([https://books.toscrape.com/robots.txt](https://books.toscrape.com/robots.txt)) contiene:

```
User-agent: *
Disallow:
```

Esto indica que **todos los agentes de usuario tienen permiso total** para acceder a cualquier parte del sitio. Por lo tanto, el scraping realizado **cumple plenamente con las directrices del sitio**.

## 4. Límites técnicos y prácticos del scraping

Aunque Web Scraper es una herramienta accesible, presenta ciertos límites:

- **Dependencia del DOM**: Si el sitio cambia su estructura HTML (clases, etiquetas), los selectores fallan.
- **No ejecuta JavaScript complejo**: Aunque este sitio es estático, sitios dinámicos (con React, Vue, etc.) requieren herramientas más avanzadas (p. ej., Scrapy + Splash o Puppeteer).
- **Rendimiento limitado**: La extensión opera en el navegador, lo que limita la velocidad y escalabilidad frente a soluciones programáticas.
- **Post-procesamiento necesario**: El campo de rating se extrajo como texto de clase CSS (`"star-rating Three"`), requiriendo limpieza adicional para convertirlo a valor numérico.

A pesar de ello, para tareas educativas o de volumen moderado, Web Scraper es una solución eficaz y rápida.

## 5. Decisiones de diseño

Se tomaron las siguientes decisiones clave:

1. **Scraping por categorías, no desde la portada**:  
   La página principal no muestra ni la categoría ni el rating de los libros. Por lo tanto, se partió desde la lista de categorías para garantizar la extracción completa de los cinco campos requeridos.

2. **Uso de paginación (`nextPage`)**:  
   Cada categoría puede tener múltiples páginas. Se configuró un selector de tipo `Link` para seguir el botón “next” y asegurar cobertura completa.

3. **Navegación jerárquica**:  
   La estructura del sitemap sigue una cadena lógica:  
   `_root` → `categoryLink` → `bookLink` → datos del libro.  
   Esto permite asociar correctamente cada libro a su categoría.

4. **Nombres en camelCase**:  
   Se respetó la convención solicitada (`categoryLink`, `ratingClass`, etc.), evitando guiones bajos o medios para compatibilidad con la herramienta.

5. **Extracción del rating como atributo de clase**:  
   Dado que el rating se representa mediante clases CSS (`star-rating One`, ..., `Five`), se utilizó el tipo `Element attribute` para capturar el valor del atributo `class`.

## 6. Conclusión

El proyecto demuestra que el web scraping, cuando se aplica con conocimiento técnico y responsabilidad ética, es una herramienta poderosa para la recolección de datos públicos. El sitio *Books to Scrape* ofrece un entorno ideal para aprender, y las decisiones de diseño adoptadas permitieron cumplir con todos los requisitos solicitados: sitemap con paginación, ≥200 registros, y extracción completa de los campos clave.

> **Entregables generados**:  
> - `booksToscrape.json` (sitemap exportado)  
> - `booksToscrape.csv` (≥200 libros con título, precio, rating, categoría y enlace)