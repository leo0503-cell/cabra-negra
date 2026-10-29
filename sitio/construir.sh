#!/bin/bash
# Arma la version subible a cualquier hosting a partir de index.html (que
# es el fuente del artifact y por eso NO trae doctype/html/head/body).
set -e
raiz="$(cd "$(dirname "$0")" && pwd)"
salida="$raiz/publicar"
DOMINIO="${1:-https://cabranegra.mx}"

rm -rf "$salida"; mkdir -p "$salida"
cp -R "$raiz/assets" "$salida/assets"

# el <title> y los <meta>/<link> del fuente van al <head>; el resto al <body>
corte=$(grep -n '^<style>' "$raiz/index.html" | head -1 | cut -d: -f1)
cabeza=$(sed -n "1,$((corte-1))p" "$raiz/index.html")
cuerpo=$(sed -n "${corte},\$p" "$raiz/index.html")

{
  echo '<!doctype html>'
  echo '<html lang="es">'
  echo '<head>'
  echo '<meta charset="utf-8">'
  echo '<meta name="viewport" content="width=device-width, initial-scale=1">'
  echo '<meta name="theme-color" content="#0C1013">'
  echo "<link rel=\"canonical\" href=\"$DOMINIO/\">"
  echo '<link rel="icon" href="assets/favicon.png" type="image/png">'
  echo '<link rel="apple-touch-icon" href="assets/favicon.png">'
  echo "$cabeza"
  # tarjeta para WhatsApp, Facebook e Instagram
  echo '<meta property="og:type" content="website">'
  echo '<meta property="og:site_name" content="Cabra Negra">'
  echo '<meta property="og:title" content="Cabra Negra — La parrilla comienza aquí.">'
  echo '<meta property="og:description" content="Tablas, grillbox, piezas de hierro, piel y mandiles en madera real con grabado láser. Envíos a todo México.">'
  echo "<meta property=\"og:url\" content=\"$DOMINIO/\">"
  echo "<meta property=\"og:image\" content=\"$DOMINIO/assets/og.jpg\">"
  echo '<meta property="og:image:width" content="1200">'
  echo '<meta property="og:image:height" content="630">'
  echo '<meta property="og:locale" content="es_MX">'
  echo '<meta name="twitter:card" content="summary_large_image">'
  echo '</head>'
  echo '<body>'
  echo "$cuerpo"
  echo '</body>'
  echo '</html>'
} > "$salida/index.html"

# 404 que regresa al inicio
cat > "$salida/404.html" <<'H404'
<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Página no encontrada — Cabra Negra</title>
<style>body{margin:0;min-height:100vh;display:grid;place-items:center;text-align:center;
padding:24px;background:#0C1013;color:#F2EDE6;font:300 17px/1.5 system-ui,sans-serif}
h1{font-size:2rem;margin:0 0 10px;text-transform:uppercase;letter-spacing:.02em}
p{color:#949BA2;margin:0 0 22px}
a{display:inline-block;padding:13px 24px;background:#C8792F;color:#0C1013;
text-decoration:none;font-weight:600;text-transform:uppercase;letter-spacing:.06em}</style>
</head><body><div>
<h1>Aquí no hay nada</h1>
<p>Esa página no existe.</p>
<a href="/">Volver al inicio</a>
</div></body></html>
H404

cat > "$salida/robots.txt" <<RB
User-agent: *
Allow: /
Sitemap: $DOMINIO/sitemap.xml
RB

cat > "$salida/sitemap.xml" <<SM
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>$DOMINIO/</loc><changefreq>monthly</changefreq><priority>1.0</priority></url>
</urlset>
SM

# cache larga para los assets (Apache / Hostinger). El HTML no se cachea.
cat > "$salida/.htaccess" <<'HT'
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css application/javascript image/svg+xml
</IfModule>
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType image/jpeg "access plus 1 year"
  ExpiresByType image/png  "access plus 1 year"
  ExpiresByType video/mp4  "access plus 1 year"
  ExpiresByType text/css   "access plus 1 month"
  ExpiresDefault           "access plus 2 days"
</IfModule>
<IfModule mod_headers.c>
  <FilesMatch "\.html$">
    Header set Cache-Control "no-cache, must-revalidate"
  </FilesMatch>
</IfModule>
ErrorDocument 404 /404.html
HT

echo "listo -> $salida ($(du -sh "$salida" | cut -f1))"
