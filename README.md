# Repositorio de IISAIA — Ingeniería de Software Asistida por IA

**Estudiante:** Victoria Villalba Tevez  
**Posgrado:** Posgrado en Inteligencia Artificial (FIUBA)  
**Año:** 2026

---

## Descripción general

Este repositorio reúne las entregas desarrolladas en la materia **Introducción a la Ingeniería de Software Asistida por IA (IISAIA)**. El trabajo se centra en explorar cómo incorporar modelos de lenguaje y flujos de prompting en el ciclo de desarrollo de software, aplicando la metodología **Prompt Driven Development (PDD)** en distintos escenarios.

La colección incluye ejercicios de diseño frustrante, especificación de APIs y prototipos con integración de IA.

---

## Entregas del repositorio

### TP1 — Bad UI: formulario frustrante

Proyecto frontend que implementa un formulario de registro diseñado intencionalmente para ser poco usable, pero completamente funcional. El objetivo fue experimentar con interacciones no convencionales, estados complejos y comportamiento reactivo en una sola página HTML.

Ubicación:
- [TP1/](TP1/)
- [TP1/index.html](TP1/index.html)
- [TP1/prompts.md](TP1/prompts.md)
- [TP1/Readme.md](TP1/Readme.md)

### TP2 — API de control de stock para kiosco

Documento OpenAPI que especifica una API para gestionar kioscos, productos, inventario y movimientos de stock, con validación de reglas de negocio como stock insuficiente y errores de entrada.

Ubicación:
- [TP2/](TP2/)
- [TP2/openapi.yaml](TP2/openapi.yaml)
- [TP2/README.md](TP2/README.md)
- [TP2/prompts.md](TP2/prompts.md)

### TP3 — Modelador espacial con IA

Aplicación que integra una API de visión de Gemini para analizar imágenes y responder con una descripción del contenido observado. El proyecto incluye backend en Python, pruebas automatizadas y una pequeña interfaz web.

Ubicación:
- [TP3/](TP3/)
- [TP3/backend/](TP3/backend/)
- [TP3/frontend/](TP3/frontend/)
- [TP3/README.md](TP3/README.md)

---

## Estructura del repositorio

```text
.
├── README.md                    # Índice principal del repositorio
├── TP1/                         # TP1: Bad UI
│   ├── index.html               # Artefacto final
│   ├── prompts.md               # Bitácora de prompts
│   └── Readme.md                # Descripción del trabajo
├── TP2/                         # TP2: API OpenAPI de stock
│   ├── openapi.yaml             # Especificación de la API
│   ├── prompts.md               # Registro de prompts
│   └── README.md                # Documentación del ejercicio
├── TP3/                         # TP3: Integración con IA
│   ├── backend/                 # Servicio Python con Gemini API
│   ├── frontend/                # Interfaz web de consumo
│   └── README.md                # Instrucciones de uso y ejecución
└── .git/                        # Metadatos del repositorio
```

---

## Objetivo académico

El repositorio busca mostrar la evolución del uso de IA como herramienta de apoyo al desarrollo, enfatizando:

- generación y refinamiento de artefactos de software;
- iteración guiada por prompts;
- validación de resultados con pruebas y documentación;
- trabajo práctico en distintos niveles de complejidad tecnológica.

---

## Cómo navegar el proyecto

- Para ver la entrega de interfaz frustrante: comenzar por [TP1/Readme.md](TP1/Readme.md).
- Para revisar la especificación de la API: abrir [TP2/openapi.yaml](TP2/openapi.yaml) y [TP2/README.md](TP2/README.md).
- Para ejecutar la aplicación con IA: seguir las instrucciones en [TP3/README.md](TP3/README.md).

---

## Estado del repositorio

El repositorio se encuentra en desarrollo y organizado por entregas, con documentación y artefactos funcionales para cada una de las actividades prácticas.
