# Distribución compacta y legible en Bizagi

Leer al crear, importar, reordenar o compactar un diagrama. Aplica el método a los actores, ramas y dimensiones del caso actual. No copies coordenadas, cantidades de tareas, IDs ni proporciones de un ejemplo. Estos criterios orientan el trabajo del agente; no constituyen un motor de distribución del puente MCP ni garantizan compatibilidad con todas las versiones de Bizagi.

## 1. Conservar el proceso al cambiar su presentación

Para una mejora exclusivamente visual, conserva una versión anterior y registra actividades, tipos BPMN, responsables, condiciones, extremos de conexiones y referencias de subprocesos. Mantén sus IDs cuando el formato lo permita. Si una conversión los reemplaza, conserva una correspondencia explícita para poder comparar las relaciones; los conteos por sí solos no prueban equivalencia.

No elimines tareas, decisiones, mensajes o excepciones para reducir el ancho. No cambies responsables de lane ni agregues subprocesos solo para hacer caber el dibujo. Si hace falta una modificación semántica, sepárala de la reorganización visual y resuélvela según el alcance solicitado.

## 2. Distribuir por contenido

Calcula las columnas con el ancho real de las figuras que contienen, sus etiquetas y el espacio que necesitan sus conexiones. Usa columnas más estrechas para eventos o compuertas cuando sea posible; evita aplicar a todo el proceso el intervalo que exige la zona más congestionada. Mantén alineados los centros de una misma ruta y acerca las tareas consecutivas.

Como orientación inicial, tareas de 150–180 por 70–90 píxeles suelen permitir espacios horizontales libres de unos 80–100 píxeles. Ajusta estos espacios según el texto, la escala y los conectores; no son dimensiones obligatorias de BPMN. Conserva el tamaño legible de las cajas al compactar. Amplía solo la zona que necesita más espacio.

Dimensiona cada lane a partir de sus filas ocupadas, etiquetas inferiores y corredores de retorno. Elimina altura vacía innecesaria sin mover actividades fuera de su responsable. Ubica la ruta habitual de izquierda a derecha y las excepciones en filas separadas. Evita plegar el proceso en un zigzag artificial para ajustarlo a una pantalla.

## 3. Trazar conexiones sin amontonarlas

Considera como obstáculos tanto las figuras como los rectángulos de sus etiquetas, incluidos los nombres bajo eventos, compuertas y subprocesos. Reserva un margen libre alrededor de esos obstáculos. Un trazado que evita cajas pero atraviesa sus textos todavía necesita corrección.

Enruta por espacios libres con segmentos ortogonales y extremos realmente unidos al elemento correspondiente. Separa corredores paralelos y retornos; una distancia inicial de unos 15–25 píxeles puede servir, pero debe ampliarse cuando haya texto o varias ramas. Evita compartir segmentos entre conexiones diferentes salvo el contacto inevitable con un extremo común; no debe parecer que existe una unión donde no la hay.

Al elegir una ruta, prioriza evitar obstáculos, después reduce segmentos compartidos y cruces, y finalmente quiebres y longitud innecesarios. Se puede usar una búsqueda en cuadrícula o por puntos de paso cuando exista generación programática, pero revisa sus resultados: encontrar un camino no demuestra que sea claro. No impongas una cuadrícula si la herramienta disponible permite resolver el dibujo directamente.

Si falta espacio, mueve el punto de quiebre o amplía el intervalo local y vuelve a trazar. No alejes todas las actividades ni hagas converger todos los retornos por el mismo corredor central. Los cruces inevitables deben distinguirse visualmente de una unión BPMN.

## 4. Colocar etiquetas completas y cerca de su rama

Una vez trazadas las conexiones, busca posiciones de sus condiciones alrededor de sus segmentos. Descarta posiciones que se superpongan con figuras, nombres de nodos, otras etiquetas o cualquier línea. Entre las posiciones libres, prefiere la más cercana a la rama correspondiente; no elijas un hueco lejano solo porque sea el primero disponible.

Calcula ancho y alto para el texto completo, con margen de tipografía y ajuste de línea. La longitud en caracteres es solo una estimación: comprueba en Bizagi que las palabras no estén cortadas. Aumenta la caja de texto o permite varias líneas antes de reducir la fuente. Si ninguna posición cercana es legible, ajusta el recorrido o la separación de esa zona y repite la colocación.

Tras mover una figura, recalcula sus conexiones y revisa de nuevo todas las etiquetas afectadas. No conserves coordenadas de texto de la distribución anterior. Al generar archivos, serializa los números de forma independiente de la configuración regional y verifica su interpretación en la versión instalada; evita decimales innecesarios para coordenadas enteras. No inventes atributos de un formato que no se haya inspeccionado.

## 5. Verificar en el archivo y en el editor

Cuando haya acceso a geometría, comprueba figuras superpuestas, segmentos que atraviesen figuras ajenas, colisiones con etiquetas y puntos de conexión. Detecta también tramos coincidentes y cruces para revisarlos: no todos los cruces son eliminables. Comprueba la semántica después del ajuste, no solo la geometría.

En Bizagi revisa el principal y cada detalle de dos maneras: vista general para detectar huecos y congestión, y zoom de lectura para comprobar palabras completas, separación de líneas, flechas y condiciones. Un archivo válido puede renderizarse distinto de lo previsto. Corrige, vuelve a abrir o importar cuando corresponda y repite solo las comprobaciones afectadas.

Abre cada subproceso desde su elemento padre y confirma que lleva al flujo interno correcto. Ejecuta la validación de Bizagi (por ejemplo, «Validar Todo» si está disponible), guarda la copia autorizada y relee el resultado para contrastar las relaciones y detectar referencias rotas o actividades aisladas.

Compara con la versión anterior: ancho y alto del lienzo, tamaño de las actividades, espacio entre tareas y facilidad para seguir las ramas. Una reducción porcentual sirve como evidencia, nunca como objetivo universal; no sacrifiques legibilidad para obtenerla. Distingue comprobación geométrica, validación BPMN y revisión visual. No afirmes ausencia de colisiones de texto si únicamente comprobaste figuras.

## 6. Mantener las pruebas fuera de la skill pública

Los modelos, capturas, extracciones, generadores específicos de una empresa y rutas del computador permanecen en el área local de trabajo. Para mejorar una skill pública, incorpora únicamente criterios generales y recursos reutilizables revisados, sin copiar archivos de prueba ni sus metadatos. Publicar la skill no autoriza publicar los modelos utilizados para comprobarla.
