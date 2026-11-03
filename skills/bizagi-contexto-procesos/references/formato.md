# Formato y límites

Observado en Modeler 4.2.0.003, FilePersistenceVersion 5: .bpm es ZIP; cada .diag es otro ZIP con Diagram.xml XPDL 2.2 y XML auxiliares. Otras versiones requieren inspección.

El lector usa la biblioteca estándar de Python. No extrae archivos al disco. Limita tamaños y rechaza DTD/entidades. Si XML no puede leerse, falla sin sustituir caracteres silenciosamente.

La salida contiene ruta, hash SHA-256, empresa aportada por el usuario y procedencia de cada diagrama. entities y connections normalizan identificadores y relaciones. semantic conserva el árbol completo salvo gráficos; incluye documentación, tipos, condiciones y atributos extendidos. auxiliary conserva XML auxiliares sin interpretar su significado.

Se comprueban extremos de conexiones dentro del diagrama y referencias SubFlow/BlockActivity contra paquetes, procesos y ActivitySet del modelo. No es validación BPMN completa. Las referencias ambiguas o externas se informan. Las actividades aisladas son candidatas a revisión, no errores concluyentes.

uninterpreted_tags enumera etiquetas fuera del conjunto normalizado, incluidas estructuras auxiliares. Conservar campos no equivale a comprenderlos. La asignación geométrica a lanes, reglas en extensiones y simulaciones requieren análisis adicional. Este lector no prueba conectividad con Bizagi ni interpreta BPMN XML de otros esquemas.
