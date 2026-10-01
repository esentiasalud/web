# Sitio web de Esentia (esentiasalud.com.ar)

Esta carpeta es el "código fuente" del sitio. Netlify la toma de GitHub, arma las páginas y las publica.

## Qué hay en cada carpeta

- `content/noticias/` — una nota por archivo. Se cargan desde el panel (no hace falta tocar archivos).
- `content/ajustes.json` — usuario de Instagram y Feed ID de Behold. También se edita desde el panel.
- `media/noticias/` — fotos que se suben desde el panel.
- `static/` — diseño (colores, logo), fotos del espacio y de las profesionales.
- `build.py` — arma el sitio. Ahí están los textos fijos, los precios y los datos de las profesionales.
- `.pages.yml` — configuración del panel de carga (Pages CMS).
- `netlify.toml` — le dice a Netlify cómo armar el sitio.

## Cómo publicar una noticia

1. Entrar a https://app.pagescms.org e iniciar sesión con GitHub.
2. Elegir este repositorio y abrir "Noticias".
3. "Add an entry": completar título, fecha, foto, resumen y texto. Guardar.
4. En 1 o 2 minutos aparece publicada en la web.

Para dejar una nota sin publicar, activar "Borrador".
