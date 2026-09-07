\# TP1: Bad UI \- Formulario de Registro Frustrante

\#\# Integrantes / Autor  
\* \*\*Nombre:\*\* VillalbaTevez Victoria  
\* \*\*Materia:\*\* Interfaces de Usuario e IA Generativa (IISAIA)

\---

\#\# Descripción del Proyecto

Este proyecto consiste en un \*\*formulario de registro de usuario\*\* deliberadamente diseñado bajo el concepto de \*\*Bad UI\*\*. El objetivo es crear una experiencia totalmente frustrante y absurda pero \*\*100% funcional\*\*, donde cada campo exige una mecánica de interacción no convencional e hiper-sensible para ser completado con éxito.

El desarrollo se realizó mediante la técnica de \*\*Prompt Driven Development (PDD)\*\* en colaboración con \*\*Gemini Canvas\*\*, manteniendo como restricción estricta la generación de un artefacto en un único archivo ejecutable sin dependencias externas.

\---

\#\# Mecánicas Implementadas

1\. \*\*Nombre y Apellido (Teclado Desordenado y Flotante):\*\*  
   \* El input nativo se encuentra bloqueado (\`readonly\`).  
   \* Para ingresar cada letra, el usuario debe interactuar con un teclado virtual cuyas teclas flotan levemente y \*\*reordenan su posición de forma aleatoria\*\* tras cada clic.

2\. \*\*Teléfono (Potenciómetro Hiper-sensible):\*\*  
   \* Sustituye la entrada de texto por un \`\<input type="range"\>\` nativo mapeado a un rango numérico de 10 dígitos.  
   \* Un desplazamiento de apenas un píxel salta cientos de miles de números. Incluye botones de ajuste fino (\`+1\` / \`-1\`) con retardo e inestabilidad deliberada, ajustado al formato argentino \`XX XXXX-XXXX\`.

3\. \*\*Contraseña (Pulsador en Código Morse):\*\*  
   \* La clave se compone registrando pulsaciones en un único botón mediante los eventos \`mousedown\` y \`mouseup\`.  
   \* Pulsaciones cortas (\< 250 ms) generan puntos (\`.\`) y largas rayas (\`-\`), que un temporizador traduce progresivamente a caracteres alfanuméricos.

4\. \*\*Términos y Condiciones (Scroll Estricto por Velocidad):\*\*  
   \* Cuadro de texto con 10.000 líneas de contenido.  
   \* El checkbox de aceptación solo se habilita al llegar al píxel final del scroll. Si se detecta un desplazamiento demasiado rápido (scroll agresivo), salta una alerta de "Lectura no detectada" y devuelve el scroll al inicio.

5\. \*\*Botón de Envío Escurridizo:\*\*  
   \* Al acercar el cursor (\`mouseenter\`), el botón de envío cambia su posición aleatoriamente en pantalla durante los primeros 10 intentos, obligando al usuario a perseguirlo antes de fijar su posición definitiva.

\---

\#\# Proceso de Desarrollo e IA (Prompt Driven Development)

Para la construcción del artefacto se utilizó una metodología iterativa dividida en patrones de prompting:

1\. \*\*Patrón 1 — Describir el artefacto:\*\* Se definió la estructura base HTML5, el diseño visual dark sobrio en CSS y el manejo central del estado JS (\`formData\`) en un único prompt inicial para establecer el esqueleto.  
2\. \*\*Patrón 2 — Iterar sobre el estado:\*\* Se inyectó cada mecánica componente por componente, definiendo explícitamente:  
   \* \*\*Cambio de estado (Ida):\*\* Captura de eventos nativos (\`mouseenter\`, \`scroll\`, \`mousedown\`, \`input\`) para actualizar \`formData\`.  
   \* \*\*Condición de vuelta/restablecimiento:\*\* Botones de borrado, reinicio de temporizadores o liberación de bloqueos (ej. habilitación del botón de envio tras 10 intentos).

\---

\#\# Archivos del Repositorio

\`\`\`text  
tp1/  
├── index.html     \# Artefacto final (HTML \+ CSS en \<style\> \+ JS en \<script\>)  
├── prompts.md     \# Registro detallado de prompts y patrones aplicados  
└── README.md      \# Informe y documentación del proyecto  
