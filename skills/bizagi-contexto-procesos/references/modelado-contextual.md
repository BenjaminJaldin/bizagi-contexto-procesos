# Modelar desde el contexto, no desde una plantilla de cajas

Leer para crear, ampliar o corregir un flujo. Para consultas de lectura sobre un modelo existente, usar el flujo de extracción de SKILL.md.

## 1. Contexto y alcance

Identifica qué ofrece la empresa, quién solicita el trabajo, qué hecho inicia un caso y qué resultados lo terminan. Distingue negocio actual, propuesta futura y caso ficticio. Anota entradas, entregables, sistemas, restricciones y reglas conocidas. No agregues aprobaciones, departamentos o plazos solo para parecer más completo.

En fuentes existentes, conserva la procedencia de cada regla. En un caso ficticio, declara sus supuestos antes de usarlos. Un plazo de ejemplo no debe convertirse en política predeterminada de la skill.

### Preguntas antes de dibujar

Lee primero el relato y las fuentes autorizadas. El usuario puede explicar el caso con sus palabras; no necesita identificar símbolos BPMN ni decidir por sí mismo qué es un subproceso. Pregunta solo por vacíos que cambien el modelo, en una ronda breve y agrupada: normalmente 2 a 5 preguntas, sin convertir ese intervalo en una cuota obligatoria.

Selecciona y adapta las preguntas pertinentes:

- ¿Qué inicia el caso y qué resultado permite considerarlo terminado?
- ¿Quién participa, qué hace cada persona o área y quién recibe su resultado?
- ¿Quién aprueba o rechaza y con qué condiciones o límites?
- ¿Qué ocurre si faltan datos, materiales, un pago o una aprobación? ¿Cómo se retoma o se cierra el caso?
- ¿Qué operación comprende varios pasos, responsables o controles internos? Pide esos pasos y propón la descomposición con criterio, sin exigir al usuario terminología BPMN.

No vuelvas a preguntar información ya aportada. Si el contexto está completo, continúa. Para una empresa real, consulta reglas críticas desconocidas y distingue propuestas de hechos. Para una simulación, puedes completar vacíos con supuestos explícitos y coherentes. Antes de dibujar resume alcance, actores, ruta habitual, excepciones y subprocesos; ese resumen informa al usuario, no introduce una aprobación adicional para trabajo ya autorizado.

## 2. Actores antes de las conexiones

Prepara una matriz breve: actor, responsabilidad, decisiones que puede tomar, información que recibe y resultado que entrega. Cada tarea tiene un responsable identificable. Si varios colaboran, distingue quién ejecuta de quién aporta información; no dupliques la misma tarea por cada participante.

Representa participantes independientes, como cliente y empresa, con pools distintos. Las áreas internas que comparten el proceso, como Administración, Finanzas y Operaciones, se representan mediante lanes dentro del pool de la empresa cuando el contexto lo justifica. Un sistema no necesita un pool independiente solo por ser software: distingue herramienta usada por una persona, tarea automática y servicio externo con interacción propia.

## 3. Trabajo, datos y reglas

Nombra las actividades con verbo y objeto: registrar solicitud, aprobar condiciones, verificar recepción. Para cada una identifica responsable, entrada, salida y condición de terminación. Incluye documentos y registros cuando explican un control o una transferencia; no conviertas cada campo de formulario en una tarea.

Ubica las decisiones después de obtener la información que las sustenta. Expresa compuertas como preguntas y sus salidas con condiciones completas, mutuamente excluyentes cuando corresponda. Una compuerta no realiza la evaluación ni toma una decisión humana: una tarea anterior produce el resultado.

Modela la ruta normal y las alternativas relevantes al contexto: información incompleta, rechazo, corrección, falta de disponibilidad, incumplimiento de calidad o falta de respuesta. Cada retorno debe indicar a qué tarea vuelve y qué cambia. Los estados de espera deben tener el mecanismo o condición de reanudación definido. No añadas temporizadores arbitrarios al negocio real.

## 4. Elegir subprocesos con criterio

Descompón una operación si tiene un objetivo propio, varias acciones relacionadas y lógica interna que estorbaría la comprensión del principal: por ejemplo, preparar materiales con inventario, compra, recepción y discrepancias; o ejecutar un trabajo con seguimiento, controles y retrabajo.

No hay un número universal de tareas ni de días que obligue a usar un subproceso. Una espera larga sola se modela como espera; una tarea simple de facturación puede permanecer en el principal. Cambiar de área no constituye una razón suficiente para descomponer.

Por cada subproceso registra:

- Motivo de la descomposición y responsable de coordinarlo.
- Entradas, precondiciones y referencia a la versión del trabajo aceptado.
- Inicio, actividades, decisiones y fin del detalle.
- Salidas explícitas: éxito y, si aplica, un resultado de excepción.
- Continuación del padre para cada resultado.
- Relación verificable entre el elemento del principal y el diagrama de detalle.

Usa un subproceso colapsado con detalle asociado cuando pertenece al caso actual. Usa actividad de llamada/reutilizable solo si realmente se invoca un proceso reusable. No elijas un subproceso de evento para una operación normal secuencial. No conectes una flecha del principal a un nodo interior del detalle: la entrada y salida se realizan mediante el elemento subproceso.

Si Bizagi presenta el detalle en otra pestaña, configura la vinculación real. Una pestaña con el mismo nombre no acredita esa relación. En representaciones expandidas respeta las restricciones del tipo de subproceso sobre pools y lanes; no copies la colaboración completa dentro de una actividad embebida.

Un símbolo de subproceso no basta: crea su contenido con inicio, trabajo interno, decisiones pertinentes y finales conectados. Antes de entregar, abre cada subproceso desde su elemento padre y comprueba que conduce al detalle correcto, con responsables y resultados coherentes con las salidas del padre. No dejes un detalle predeterminado, vacío o sin editar. Comprueba también la referencia guardada por ID; un nombre coincidente o un `calledElement` en el archivo de intercambio no demuestra que Bizagi haya conservado el enlace.

## 5. Conectar y dibujar

Dentro de un pool usa flujos de secuencia, incluso al cruzar lanes. Entre pools usa mensajes; nunca flujos de secuencia. No uses mensajes para unir Finanzas y Administración dentro del mismo pool. Las asociaciones documentan datos, no mueven el control.

Si se espera una respuesta externa, representa recepción de mensaje o evento apropiado. Para competir entre respuesta y vencimiento usa una compuerta basada en eventos con capturas compatibles; no una decisión que presupone datos todavía inexistentes. Usa paralelismo solo cuando las tareas pueden ejecutarse independientemente y sincroniza las ramas requeridas sin bloquear rutas alternativas.

Ordena el flujo de izquierda a derecha, agrupa por responsabilidad, etiqueta ramas y reduce cruces. Las excepciones pueden ir debajo de la ruta principal. Revisa legibilidad y no soluciones un lienzo confuso ocultando todo detrás de subprocesos. Los elementos deben quedar dentro de su pool/lane, conectados por sus extremos y con nombres completos.

Antes de conectar, distribuye las actividades en columnas por avance del proceso y filas por responsable, reservando espacio para decisiones, etiquetas y retornos. Alinea centros y usa separación consistente; amplía el lienzo o las lanes cuando haga falta, sin reducir las cajas hasta volver ilegible el texto.

### Distribución y revisión visual

Aplica la [guía de distribución compacta y legible](distribucion-visual.md) al materializar el diseño: columnas según el contenido, corredores separados, trazado que evite cajas y textos, etiquetas completas próximas a sus ramas y comparación semántica antes y después. Revisa tanto el principal como cada detalle en Bizagi a escala general y a un zoom de lectura. No soluciones un dibujo confuso ocultando operaciones simples detrás de nuevos subprocesos.

## 6. Validación de negocio y de herramienta

Recorre casos concretos: éxito, rechazo y cada excepción modelada. Comprueba que cada espera tiene salida, que ningún caso aceptado se cierra como completado sin producir el entregable y que no se pierde el estado al volver de un subproceso. Comprueba responsables y transferencias, no solo ausencia de errores sintácticos.

En el editor, ejecuta la validación de Bizagi y conserva su resultado como evidencia de esa comprobación, no como prueba de corrección del negocio. Revisa visualmente el principal y cada detalle; verifica enlaces de subprocesos. Si guardas, usa una ubicación apropiada al pedido y vuelve a leer el archivo para contrastar actores, actividades, conexiones y referencias. Los ejemplos de prueba deben permanecer separados de modelos reales.

Informa por separado: especificación preparada, diagrama creado, validación BPMN ejecutada, archivo guardado y extracción comprobada. No marques como completada una etapa que no se ejecutó.

## Fuentes técnicas

Consultadas el 2026-11-03. Verifica nuevamente al implementar comportamientos específicos de una versión.

- [Interacción entre procesos](https://help.bizagi.com/platform/en/multiple_pools.htm): pools y mensajes.
- [Buenas prácticas de modelado](https://help.bizagi.com/platform/en/best_practices_in_modeling.htm): actores, compuertas y conexiones.
- [Crear subprocesos](https://help.bizagi.com/platform/en/creating_a_sub_process.htm): descomposición y configuración del detalle.
- [Tipos de subproceso](https://help.bizagi.com/platform/en/sub-process_types.htm): diferencias entre subprocesos.
