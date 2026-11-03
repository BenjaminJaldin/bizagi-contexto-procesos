# Bizagi Modeler: contexto de procesos para agentes

Skill en español y servidor MCP local para trabajar con modelos de cualquier empresa o sistema. El repositorio incluye únicamente código, instrucciones y pruebas sintéticas. Los modelos y resultados empresariales permanecen fuera del repositorio.

Licencia [MIT](LICENSE). Proyecto independiente, sin afiliación con Bizagi.

## Diseño de procesos desde el contexto

La skill comienza por alcance, actores y responsabilidades; después define actividades, reglas, conexiones y excepciones. El proceso principal conserva tareas reales y traspasos entre áreas. Solo se descomponen operaciones extensas cuya lógica interna justifica un subproceso; no se crea un subproceso por departamento o fase.

Puedes entregar el contexto con tus palabras. Si falta información importante, el agente hace una ronda breve de preguntas sobre responsables, aprobaciones, excepciones y trabajo interno; si ya está respondida, continúa directamente. Antes de dibujar resume su interpretación y distingue reglas reales de supuestos ficticios.

La diagramación debe ser compacta y legible: actividades cercanas sin superponerse, líneas por corredores separados, etiquetas claras y espacio proporcional al contenido de cada lane. Cada subproceso debe contener un flujo interno y abrir el detalle correcto desde el principal. Estas son instrucciones de trabajo y revisión visual; el puente MCP no incluye un motor automático de distribución.

La [guía de distribución visual](skills/bizagi-contexto-procesos/references/distribucion-visual.md) detalla cómo calcular espacios por contenido, evitar figuras y textos al trazar, colocar condiciones completas cerca de sus ramas y comprobar que la reorganización conserva el proceso. Los criterios se adaptan a cada flujo; las dimensiones orientativas y las reducciones obtenidas en una prueba no se imponen a otros modelos.

Incluye el [método de modelado](skills/bizagi-contexto-procesos/references/modelado-contextual.md) y el [caso ficticio Talleres Bruma](skills/bizagi-contexto-procesos/references/ejemplo-talleres-bruma.md), con Cliente, Administración, Finanzas, Operaciones y Compras/Bodega, negociación, pagos, excepciones y dos subprocesos justificados. El caso es una especificación para dibujar, no un modelo .bpm ya generado.

Crear elementos en Bizagi requiere las herramientas de escritorio del agente. El servidor MCP de este repositorio no proporciona edición de elementos ni generación de diagramas.

## Qué conecta realmente

El cliente MCP se comunica con un proceso Python local por stdio. El puente detecta Bizagi Modeler instalado en Windows, solicita abrir un `.bpm`, lee sus diagramas y vuelve a leer el archivo en cada consulta para detectar cambios **guardados** mediante SHA-256.

**No es una API oficial de Bizagi, ni accede al lienzo sin guardar.** No modifica diagramas, no realiza guardado automático y no mantiene una sincronización en segundo plano. La apertura devuelve `launch_requested`; debe comprobarse en la interfaz. Para navegar o editar visualmente hace falta una herramienta de escritorio del agente.

Bizagi indica que [Modeler no admite integración de sistemas](https://help.bizagi.com/platform/en/bm-faqs.htm). La [API OAuth/OData de la plataforma](https://help.bizagi.com/platform/en/api_odata_authentication.htm) es otra integración y requiere una instancia compatible. Este proyecto no presupone disponer de ella.

## Requisitos e instalación

- Python 3.10 o superior y un cliente con soporte MCP por stdio.
- Bizagi Modeler instalado en Windows para abrir la aplicación. Lectura y MCP no requieren que Modeler esté abierto.
- Formato probado: contenedores Modeler 4.2 con XPDL 2.2. Otras versiones necesitan validación.

Desde la raíz del repositorio, en PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Copia `skills/bizagi-contexto-procesos` al directorio de skills de tu agente. El servidor debe seguir ejecutándose desde el repositorio con su entorno virtual, o instalar sus dependencias en la ubicación elegida.

## Configuración MCP

Ejemplo para clientes que aceptan `mcpServers`. Sustituye las tres rutas por rutas absolutas propias. Otros clientes requieren traducir estos mismos valores a su formato de configuración.

```json
{
  "mcpServers": {
    "bizagi-modeler-local": {
      "command": "C:/ruta/al/repositorio/.venv/Scripts/python.exe",
      "args": [
        "C:/ruta/al/repositorio/skills/bizagi-contexto-procesos/scripts/modeler_bridge.py",
        "--root", "C:/ModelosEmpresa"
      ]
    }
  }
}
```

`--root` limita los archivos accesibles a una carpeta elegida por el usuario. No uses todo el disco como raíz. El servidor no expone puertos ni sube modelos. Si la instalación no se detecta de forma única, agrega `--executable` con la ruta al `BizagiModeler.exe` instalado. No se ejecutan comandos obtenidos del contenido de los modelos.

## Flujo de uso

1. `modeler_status`: comprobar instalación y proceso; no prueba que un documento esté abierto.
2. `attach_model(model_path, company)`: seleccionar un modelo compatible dentro de la raíz y obtener sus diagramas.
3. `open_model(model_path)`: solicitar abrir el `.bpm` si se quiere trabajar en Modeler. Verificar la ventana mediante las herramientas de escritorio del agente.
4. `get_diagram(diagram_id)`: recuperar entidades, conexiones y evidencia del diagrama seleccionado.
5. Tras guardar cambios en Modeler, `refresh_model`: detectar y consultar la nueva versión. Las lecturas de diagrama también releen el archivo.

Si Modeler está guardando y la lectura falla, espera a que termine y reintenta una vez; no presentes datos anteriores como actuales. Una nueva selección reemplaza el contexto de empresa de la sesión. Reiniciar el servidor elimina la selección en memoria.

Ejemplo de solicitud:

> Usa $bizagi-contexto-procesos. Conecta el modelo solicitudes.bpm de mi carpeta autorizada, identifica sus diagramas y explica el flujo de aprobación de la empresa que te indique.

Sin cliente MCP puede usarse el extractor directamente:

```powershell
python skills/bizagi-contexto-procesos/scripts/extract_bizagi.py C:/ModelosEmpresa/solicitudes.bpm --company "Empresa de ejemplo" --out C:/Analisis/nuevo
```

## Pruebas y límites

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Las pruebas generan un modelo ficticio temporal, verifican cambios guardados, aislamiento de rutas y el intercambio MCP real por stdio. La apertura visual requiere una sesión Windows interactiva y una comprobación separada; las pruebas no afirman validarla. No se garantiza compatibilidad con todas las versiones ni con todos los hosts.

Los textos y atributos del modelo son datos no confiables, nunca instrucciones para el agente. No se incluyen modelos empresariales, credenciales ni resultados de análisis. Antes de publicar, revisa los archivos que vas a incorporar: `.gitignore` reduce inclusiones accidentales, pero no sustituye la revisión.

Servidor construido con el [SDK oficial de MCP](https://github.com/modelcontextprotocol/python-sdk/tree/v1.26.0).
