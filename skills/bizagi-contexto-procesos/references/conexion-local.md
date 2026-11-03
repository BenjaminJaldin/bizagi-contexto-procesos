# Conexión local con Modeler

Usa las herramientas `modeler_status`, `attach_model`, `refresh_model`, `get_diagram` y `open_model` del servidor `bizagi-modeler-local` cuando estén disponibles. El usuario configura Python, la ruta del servidor y `--root` en su host MCP; los pasos completos están en README.md del repositorio. No configures una ruta privada de un autor como valor predeterminado.

Esta conexión es un puente local al archivo guardado y al inicio de la aplicación. No es una API oficial ni acceso a la memoria de Modeler. `process_running` no prueba que el documento elegido esté abierto. `launch_requested` tampoco prueba éxito visual.

Selecciona con `attach_model` el archivo indicado, pasando la empresa solo si el usuario la conoce. Usa los IDs devueltos por la herramienta para consultar diagramas. Cada consulta relee el archivo: no se mantienen datos previos como si fueran actuales. Tras guardar, `refresh_model` informa si cambió el hash. No hay vigilancia automática entre llamadas.

Para interacción visual, usa la skill de control de escritorio disponible en el host y respeta sus instrucciones. Detecta la ventana real de Modeler, verifica su título y el modelo antes de actuar. Si no existe una herramienta compatible o falla su runtime, informa que el control visual no está disponible en esa sesión; no lo reemplaces por clics a ciegas. No prometas compatibilidad de escritorio fuera de Windows.

Nunca descartes cambios sin guardar para abrir otro modelo. Abrir/navegar no autoriza editar, guardar, publicar o subir un archivo. Para ediciones solicitadas, conserva el original cuando corresponda y verifica el resultado visual y el archivo guardado. Si aparece autenticación, usa el mecanismo admitido por el host o pide al usuario completar el acceso.

Referencias oficiales verificadas el 2026-11-03:
- https://help.bizagi.com/platform/en/bm-faqs.htm — Modeler no admite integración de sistemas.
- https://help.bizagi.com/platform/en/api_odata_authentication.htm — OAuth/OData corresponde a proyectos de la plataforma, no constituye una API de escritorio de Modeler.
- https://github.com/modelcontextprotocol/python-sdk/tree/v1.26.0 — transporte MCP stdio.
