# Revisión del sitio — 16 de octubre de 2026

Sitio: https://cabra-negra-taller.ponynoise.chatgpt.site/
Versión publicada: 6. Fuente: 2f0ab2e227b66f3b70e9931f0b10a0404d4a013b.

Implementado y verificado:
- CSP por meta: solo scripts, estilos, fuentes, medios e imágenes propios; iframe de Instagram autorizado; conexiones de scripts y envío HTTP de formularios deshabilitados.
- Tipografías locales con licencias; enlaces externos con noopener noreferrer y política no-referrer.
- Instagram bloqueado por defecto; aceptación/rechazo guardados sin identificadores; revocar retira iframe. Pruebas de persistencia, rechazo y retiro aprobadas.
- Formulario local sin base de datos. Revisión previa antes de abrir WhatsApp. Entrada con etiquetas HTML mostrada como texto (sin nodos HTML).
- Páginas públicas de privacidad, cookies y condiciones de cotización, enlazadas en pie y formulario.
- Navegación móvil sin desbordamiento; scripts revisados con node --check.

Pendientes y límites:
- Identidad legal y domicilio del responsable pendientes de confirmación por Leonardo. Marcados expresamente en el aviso publicado; no se considera cerrado el contenido legal hasta completarlos.
- El alojamiento de Sites no aplicó el archivo _headers. La revisión de respuesta HTTP no encontró CSP por cabecera, X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Permissions-Policy ni HSTS propios. La CSP y política de referrer sí están activas por meta. No se afirma protección de frame-ancestors, nosniff, Permissions-Policy o HSTS adicionales. Requiere soporte del alojamiento o migración a un servidor con control de cabeceras para ampliar esa capa.
- Cookie técnica __cf_bm observada, administrada por Cloudflare. No se instaló analítica ni publicidad.
- No se auditaron las prácticas operativas internas del negocio ni la seguridad de su cuenta de WhatsApp. Las condiciones específicas de cada pedido deben proporcionarse en la cotización.

Fuentes verificadas:
- https://www.ordenjuridico.gob.mx/Documentos/Federal/html/wo125102.html (artículos 14–16 y 31).
- https://www.diputados.gob.mx/LeyesBiblio/pdf/LFPDPPP.pdf
- https://developers.cloudflare.com/fundamentals/reference/policies-compliances/cloudflare-cookies/
- https://developers.cloudflare.com/workers/static-assets/headers/

## Actualización posterior — versión 7
Leonardo confirmó el nombre del responsable “cabranegramx” y el domicilio Harold R. Pape 209, Desarrollo Especial Galerías, 20078 Aguascalientes, Ags. El aviso publicado ya contiene esos datos y se retiró la nota de identidad pendiente. La limitación de cabeceras del alojamiento sigue vigente.
