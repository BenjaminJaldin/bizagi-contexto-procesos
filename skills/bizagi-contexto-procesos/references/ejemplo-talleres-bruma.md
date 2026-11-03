# Caso ficticio: Talleres Bruma — servicio técnico de equipos

Este caso fue inventado para enseñar el nivel de análisis y modelado. No contiene datos, nombres, modelos ni reglas de una empresa real. Es una **especificación para diagramar**, no un archivo .bpm ni evidencia de creación en el editor. Sus políticas no se heredan a otros casos.

## Enunciado

Talleres Bruma realiza mantenimiento de equipos de laboratorio. Un cliente envía una solicitud con la identificación del equipo, el problema observado y su disponibilidad. Administración comprueba los antecedentes y pide correcciones cuando faltan datos. Operaciones evalúa la viabilidad del servicio y define el alcance técnico. Finanzas calcula el precio y las condiciones de pago; Administración prepara y envía una cotización versionada.

El cliente puede aceptar, rechazar o solicitar ajustes. Los ajustes producen una nueva evaluación y versión de la propuesta, sin sobrescribir la aceptada. Si acepta, Finanzas verifica el anticipo antes de comprometer recursos. Operaciones prepara el servicio: confirma acceso, reserva personal y equipos, verifica repuestos y gestiona faltantes mediante Compras y Bodega. Solo inicia la ejecución cuando todo está disponible.

Durante la ejecución se registran avances y se controlan resultados. Un fallo de calidad genera retrabajo. Si surge una desviación que cambia alcance o precio, el trabajo afectado se detiene y Administración gestiona una modificación con el cliente. Cuando el trabajo termina conforme, el cliente recibe el informe y firma la recepción. Finanzas factura y concilia el pago; Administración cierra el expediente. Cancelaciones y saldos pendientes tienen estados diferenciados.

## Alcance y supuestos ficticios

- Inicio: solicitud recibida. Fin normal: servicio recibido, saldo conciliado y expediente cerrado.
- Fines alternativos: solicitud rechazada, propuesta vencida, cancelación regularizada. El cierre por cancelación no se registra como servicio entregado.
- Una cotización vence a los cinco días hábiles. El anticipo se espera hasta la fecha pactada. Estos tiempos son supuestos del ejemplo.
- Se permite una reiteración al pedir antecedentes; si no llegan al vencer el plazo de respuesta acordado, se cierra la solicitud incompleta.
- Un anticipo contabilizado se conserva como crédito del caso. Una modificación aceptada solo puede exigir la diferencia; nunca se cobra el mismo anticipo dos veces.
- Cada envío tiene identificador de caso y versión. Se ignoran como habilitantes las aceptaciones de versiones anteriores.
- La cancelación de un caso aceptado exige resolver compromisos, consumos, saldo o devolución antes del cierre.
- La cobranza vencida se deriva a una gestión fuera del alcance de este modelo, dejando el caso en estado suspendido por cobro, sin afirmar pago ni cierre normal.

## Actores y representación

| Participante / área | Representación | Responsabilidad y salida |
|---|---|---|
| Cliente | Pool externo | Entrega antecedentes, decide sobre propuesta y cambios, permite acceso, recibe el servicio y paga. |
| Talleres Bruma | Pool de la empresa | Gestiona el caso de principio a fin. |
| Administración | Lane de Bruma | Mantiene expediente y versiones; solicita datos; comunica propuestas, cambios y cierre. |
| Finanzas | Lane de Bruma | Determina precio/condiciones, comprueba anticipos, emite factura, concilia cobros o devoluciones. |
| Operaciones | Lane de Bruma | Define viabilidad y alcance; coordina preparación, ejecución, control técnico y retrabajo. |
| Compras y Bodega | Lane de Bruma, usada en el detalle de preparación cuando la representación lo permita | Comprueba existencias, compra faltantes y registra materiales conformes. No se inventa actividad en el principal solo para ocupar esta lane. |
| Proveedor | Pool externo de caja negra, en la colaboración pertinente | Recibe orden y responde por entrega o discrepancias; su proceso interno queda fuera de alcance. |

El sistema de gestión es una herramienta de registro, no un participante externo adicional. Los responsables de las tareas internas del detalle se documentan aun cuando el tipo de subproceso no admita lanes internas.

## Qué permanece visible y qué se descompone

| Operación | Decisión de modelado | Motivo |
|---|---|---|
| Registrar solicitud, verificar datos, evaluar alcance, calcular precio, enviar cotización | Tareas del principal | Explican responsables y decisiones del negocio sin requerir otro diagrama en este caso. |
| Verificar anticipo, emitir factura, conciliar pago | Tareas del principal | No se oculta toda Finanzas detrás de un subproceso genérico. |
| SP1 — Preparar servicio | Subproceso colapsado con detalle vinculado | Incluye disponibilidad, reserva, faltantes, compra, recepción y discrepancias; puede terminar listo o inviable. |
| SP2 — Ejecutar y verificar servicio | Subproceso colapsado con detalle vinculado | Incluye actividades técnicas, seguimiento, control, retrabajo y detección de cambios de alcance. |
| Solicitar ajuste o comunicar rechazo | Tarea o mensaje, según responsable | No justifican un subproceso independiente. |

No hay un subproceso por cada fase. El principal conserva la negociación, el pago y la recepción del cliente.

## Diagrama principal de Bruma

Los IDs siguientes son referencias de diseño, no IDs extraídos de un archivo. Las uniones de rutas alternativas se implementan con compuertas XOR de convergencia separadas de las compuertas de decisión. Los saltos de la tabla significan secuencias dentro del pool; los intercambios con Cliente son mensajes.

| ID | Elemento / responsable | Salida y continuación |
|---|---|---|
| E0 | Inicio por mensaje: solicitud recibida / Administración | A1. |
| A1 | Registrar solicitud / Administración | A2. |
| A2 | Comprobar antecedentes / Administración | G1. |
| G1 | XOR: ¿Antecedentes completos? | Sí → A4. No → A3. |
| A3 | Pedir antecedentes faltantes / Administración | Esperar respuesta del cliente o vencimiento. Respuesta → A2; primer vencimiento → reiterar y esperar una vez más; segundo → fin Solicitud incompleta. |
| A4 | Evaluar viabilidad y definir alcance / Operaciones | G2. Recibe también ajustes desde A8. |
| G2 | XOR: ¿Servicio viable? | Sí → F1. No → A5. |
| A5 | Comunicar inviabilidad / Administración | Si no existe compromiso aceptado: fin Solicitud rechazada. Si es revisión de un caso ya aceptado: A13 para regularizar cancelación. |
| F1 | Calcular precio, plazo y condiciones / Finanzas | A6. Considera anticipos existentes y costos de cambio cuando corresponda. |
| A6 | Generar versión y enviar cotización / Administración | W1. |
| W1 | Compuerta basada en eventos: respuesta o vencimiento | Mensaje respuesta → A7. Temporizador de vigencia → A9 con motivo Vencimiento. |
| A7 | Registrar y verificar versión de la respuesta / Administración | Si no corresponde a la versión vigente: informar versión actual y volver a W1 conservando su fecha de vencimiento; si corresponde → G3. |
| G3 | XOR: ¿Respuesta del cliente? | Acepta → F2. Pide ajustes → A8. Rechaza → A9 con motivo Rechazo. |
| A8 | Registrar cambios solicitados / Administración | A4 para reevaluar alcance y emitir nueva versión. |
| A9 | Registrar rechazo o vencimiento / Administración | Caso no aceptado previamente → fin Propuesta rechazada/vencida. Caso con compromisos → A13. |
| F2 | Verificar anticipo o diferencia exigible / Finanzas | G4. Puede resultar Sin importe adicional requerido. |
| G4 | XOR: ¿Condición financiera cumplida? | Sí → SP1. No → A10. |
| A10 | Solicitar regularización del anticipo / Administración | Esperar comprobante o fecha límite. Comprobante → F2; vencimiento → A13. No confundir comprobante con pago conciliado. |
| SP1 | Preparar servicio / Operaciones | G5 lee resultado de SP1. |
| G5 | XOR: ¿Preparación lista? | Lista → SP2. Inviable → A13. |
| SP2 | Ejecutar y verificar servicio / Operaciones | G6 lee resultado de SP2. |
| G6 | XOR: ¿Resultado de ejecución? | Conforme → A11. Cambio de alcance requerido → A8. Imposible continuar → A13. |
| A11 | Enviar informe y solicitar recepción / Administración | W2: esperar acta, observaciones o plazo de respuesta acordado. Acta → F3. Observaciones → O1. Vencimiento → seguimiento con nueva fecha registrada y vuelta a W2; no presume aceptación. |
| O1 | Evaluar observaciones / Operaciones | Defecto del alcance pactado → SP2 como retrabajo; solicitud adicional → A8; observación ya resuelta documentalmente → A11 con explicación. |
| F3 | Emitir factura descontando anticipo / Finanzas | Enviar al cliente; esperar pago o vencimiento. Pago → F4; vencimiento → registrar derivación a cobranza y fin suspendido por cobro. |
| F4 | Conciliar pago / Finanzas | Completo → A12; insuficiente o no acreditado → solicitar saldo y volver a la espera de F3 sin emitir otra factura. |
| A12 | Archivar acta, informe y comprobantes / Administración | Fin Servicio cerrado y pagado. |
| A13 | Evaluar cancelación y compromisos / Administración con información de Operaciones | Operaciones libera reservas y registra consumos; Finanzas determina saldo/devolución → F5. |
| F5 | Regularizar saldo o devolución / Finanzas | Resuelto → A14; pendiente → seguimiento hasta resolver o derivación documentada a gestión externa, dejando fin suspendido, no cancelación regularizada. |
| A14 | Comunicar cancelación regularizada / Administración | Fin Caso cancelado. |

F3 y F5 no se ejecutan como tareas eternas: las esperas se dibujan con sus mensajes/plazos o se derivan explícitamente a un proceso externo. Un final suspendido significa fin del alcance de esta gestión, no liquidación comercial.

## Colaboración con Cliente

El cliente puede mostrarse como pool de caja negra si se desea focalizar el principal. Para probar actores y traspasos, este ejemplo usa un pool con comportamiento visible:

1. Necesidad detectada → enviar solicitud → esperar mensajes de Bruma.
2. Petición de antecedentes → completar y enviar datos → volver a esperar.
3. Cotización recibida → evaluar → aceptar, pedir ajustes o rechazar mediante mensajes separados → esperar confirmación o nueva versión.
4. Solicitud de anticipo → realizar pago y enviar comprobante → esperar coordinación.
5. Coordinación de acceso → confirmar disponibilidad → esperar ejecución/informe.
6. Informe recibido → revisar servicio → enviar acta u observaciones.
7. Factura recibida → pagar saldo → recibir confirmación de cierre → fin.
8. Rechazo, vencimiento o cancelación recibidos → registrar resolución → fin alternativo. Las comunicaciones de regularización preceden al cierre cuando existen compromisos.

En el dibujo, usa recepciones y selección por evento para los mensajes que pueden llegar en distinto orden. No conectes esas ocho líneas como una secuencia obligatoria: los antecedentes, el anticipo y los cambios son condicionales. Todos los mensajes llevan caso y versión cuando aplica.

## SP1 — Preparar servicio

**Motivo:** reúne coordinación, abastecimiento y control de recepción; no es una sola acción. **Coordinación:** Operaciones. **Entrada:** alcance/version aceptados, condición financiera satisfecha y pendientes existentes. **Salida:** `preparacion = lista | inviable`, reservas y registro de materiales; motivo obligatorio si inviable.

| ID | Actividad o decisión / responsable | Conexión |
|---|---|---|
| P0 | Inicio de preparación | P1. |
| P1 | Revisar alcance vigente y recursos ya reservados / Operaciones | P2; evita repetir reservas al reingresar por un cambio. |
| P2 | Confirmar acceso, fecha y disponibilidad técnica / Operaciones, con mensaje al Cliente | Confirmado → P3. No disponible → proponer alternativa; aceptada → P2; imposible antes de la fecha límite pactada → PF. |
| P3 | Reservar personal y equipos / Operaciones | P4. |
| P4 | Verificar repuestos y consumibles / Compras y Bodega | Disponibles → P9. Faltantes → P5. |
| P5 | Solicitar oferta y plazo al proveedor / Compras y Bodega | Oferta recibida → P6; sin respuesta al plazo acordado → buscar otro proveedor; sin alternativa viable → PF. |
| P6 | Evaluar costo/plazo de faltantes / Operaciones y autorización financiera documentada | Dentro de condiciones aceptadas → P7; cambio de compromiso → registrar imposibilidad de preparación → PF. No autorizar sobrecostos silenciosamente. |
| P7 | Emitir orden de compra / Compras y Bodega | Esperar entrega o plazo. Entrega → P8; incumplimiento → gestionar alternativa, volver a P5 o PF según viabilidad. |
| P8 | Inspeccionar recepción / Compras y Bodega | Conforme → registrar ingreso → P9. Discrepancia → reclamar al proveedor y esperar reposición; reposición → P8; sin solución viable → PF. |
| P9 | Preparar kit y entregar materiales a Operaciones / Compras y Bodega | P10. |
| P10 | Verificar condiciones de inicio / Operaciones | Completas → fin `lista`; pendientes corregibles → tarea específica P2, P3 o P4; imposibles → PF. |
| PF | Registrar impedimento y compromisos existentes / Operaciones | Fin `inviable`; el padre G5 conduce a regularización, sin perder órdenes ni reservas. |

El proveedor es un participante externo: oferta, orden, entrega y reclamo son mensajes. El inventario, reservas y acta de entrega son datos asociados. El proceso del proveedor no se dibuja dentro de SP1 como si perteneciera a Bruma.

## SP2 — Ejecutar y verificar servicio

**Motivo:** combina intervención técnica, registro, controles y retrabajo. **Coordinación:** Operaciones. **Entrada:** preparación lista, alcance/version aceptados, estado de avances y, si existe, observación del cliente. **Salida:** `ejecucion = conforme | cambio_requerido | imposible`, informe de avance y trazabilidad de consumos.

| ID | Actividad o decisión / responsable | Conexión |
|---|---|---|
| X0 | Inicio de ejecución o reingreso | X1. |
| X1 | Revisar alcance vigente, avances y pendientes / Operaciones | X2. Reingreso no borra trabajo terminado ni duplica consumos. |
| X2 | Asignar y ejecutar actividades pendientes / Operaciones | X3. |
| X3 | Registrar avance, horas, materiales e incidencias / Operaciones | X4. |
| X4 | XOR: ¿Hay impedimento? | No → X7. Sí → X5. |
| X5 | Evaluar impacto y solución / Operaciones | Dentro del alcance y resoluble → X6. Exige cambio de alcance/precio → XC. Sin solución → XI. |
| X6 | Resolver incidencia y registrar acción / Operaciones | X2; si requiere reprogramación, registrar nueva fecha y condición de reanudación. |
| X7 | XOR: ¿Trabajo técnico completo? | No → X2. Sí → X8. |
| X8 | Ejecutar pruebas de calidad / Operaciones | X9. |
| X9 | XOR: ¿Cumple criterios de aceptación? | Sí → X10. No → X11. |
| X11 | Registrar defecto y definir retrabajo / Operaciones | Corregible dentro del alcance → X2 con pendientes actualizados; exige cambio → XC; técnicamente imposible → XI. |
| X10 | Consolidar informe técnico y evidencia / Operaciones | Fin `conforme`; padre continúa en A11. |
| XC | Dejar trabajo afectado detenido y documentar cambio / Operaciones | Fin `cambio_requerido`; padre gestiona A8, reevaluación, versión y anticipo diferencial antes de SP1/SP2. |
| XI | Documentar imposibilidad y estado seguro del equipo / Operaciones | Fin `imposible`; padre continúa A13. |

El control técnico de X8 no sustituye la recepción del cliente en A11. Una devolución del cliente vuelve a revisar pendientes: no se representa como factura automática ni aceptación tácita.

## Prueba de recorridos antes de dibujar

| Caso | Recorrido esperado y comprobación |
|---|---|
| Normal, materiales en stock | E0 → A1/A2 → A4 → F1/A6 → aceptación vigente → F2 → SP1(lista) → SP2(conforme) → acta → F3/F4 → A12. No compra innecesaria. |
| Antecedentes incompletos | G1 → A3 → respuesta → A2. Sin respuesta tras reiteración: fin incompleta, sin cotización ficticia. |
| Cotización con ajuste | G3 → A8 → A4/F1/A6. Se emite nueva versión; aceptación vieja no habilita ejecución. |
| Rechazo inicial | G3 → A9 → fin rechazada; no pasa por ejecución ni genera factura por servicio. |
| Anticipo no acreditado | G4 → A10 → F2 o A13 por vencimiento. Un comprobante no habilita recursos sin verificación. |
| Material incorrecto | P8 → reclamo → P8. No sale `lista` hasta contar con material conforme. |
| Cambio durante ejecución | X5 → XC → G6/A8 → nueva versión aceptada → F2 por diferencia → SP1/SP2 retomando avances. |
| Calidad insuficiente | X9 → X11 → X2 → X8. No se solicita acta de recepción con defecto pendiente. |
| Cliente observa defecto | A11 → O1 → SP2(retrabajo) → A11. No se factura dos veces. |
| Saldo no pagado | F3 espera/vencimiento → derivación a cobranza; nunca fin cerrado y pagado. |
| Cancelación con anticipos y compras | A13 → F5 → A14 solo tras regularizar. Si no se resuelve, estado suspendido con motivo y derivación. |

## Entregable al materializar este caso

Un principal con Cliente y Bruma, lanes internas justificadas, tareas concretas, decisiones y mensajes; dos detalles vinculados a SP1 y SP2 con los responsables documentados. Nombres coherentes entre padre y detalle, resultados de excepción visibles y comprobación visual de ambos enlaces. Guardar como un modelo ficticio separado y verificar con el extractor. No presentar este documento por sí solo como ese entregable ya creado.
