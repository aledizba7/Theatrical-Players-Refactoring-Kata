# Análisis de Code Smells: Theatrical Players (Código Inicial)

A continuación se detallan los 4 "code smells" (olores de código) identificados en la función original `statement` dentro de `python/statement.py`.

---

### 1. Método Largo (Long Method) y Violación del Principio de Responsabilidad Única (SRP)
*   **Descripción:** La función `statement` es un método monolítico que realiza tres tareas distintas:
    1.  **Cálculo de montos:** Determina cuánto cobrar por cada tipo de obra según las reglas de negocio.
    2.  **Cálculo de créditos:** Determina los puntos de volumen acumulados por el cliente.
    3.  **Formateo/Presentación:** Construye la representación textual del estado de cuenta (factura) en dólares y con una plantilla de texto específica.
*   **Por qué es un problema:** Viola el principio SRP de SOLID. Si las reglas de negocio para los montos cambian, o si se desea imprimir la factura en otro formato (como HTML), se tendrá que modificar la misma función. Esto aumenta el riesgo de introducir errores y dificulta enormemente la legibilidad del código.

### 2. Condicionales Repetidos (Repeated Conditionals)
*   **Descripción:** A lo largo del bucle que procesa las obras, se repite la lógica condicional basada en el tipo de obra (`play['type'] == "tragedy"` o `"comedy"`). Específicamente, se usa un condicional para calcular el monto (`this_amount`) y luego otro condicional para calcular los créditos adicionales (si la obra es comedia).
*   **Por qué es un problema:** Si decidimos agregar un nuevo tipo de obra (por ejemplo, `"history"` o `"pastoral"`), tendremos que buscar y modificar todos los condicionales que pregunten por el tipo de obra a lo largo de todo el código. Esto viola el principio de Abierto/Cerrado (OCP) de SOLID y facilita que olvidemos actualizar algún punto.

### 3. Variables Temporales Excesivas (Excessive Temporary Variables)
*   **Descripción:** Se utilizan variables temporales como `this_amount`, `volume_credits`, `total_amount`, `play`, y `perf`.
*   **Por qué es un problema:** Las variables temporales tienden a acumular y retener el estado dentro de la función. Esto obliga a leer y comprender todo el flujo de ejecución secuencial de la función y dificulta la extracción de la lógica a subfunciones limpias, ya que las variables temporales deben pasarse como parámetros o resolverse localmente. La solución ideal es aplicar la técnica **Replace Temp with Query** (Reemplazar temporal con consulta) extrayendo funciones como `amount_for(perf, play)` que reciba solo la performance y la obra.

### 4. Falta de Separación de Fases (Mixed Phases)
*   **Descripción:** El cálculo de los datos de negocio (montos, créditos, totales) está completamente mezclado con el formateo de la salida textual (`result += ...`).
*   **Por qué es un problema:** Si el cliente requiere un nuevo formato de salida (por ejemplo, generar una factura en formato HTML), no podemos reutilizar la lógica de cálculo sin duplicar el código o realizar una reestructuración profunda. La solución es separar el proceso en dos fases distintas (técnica **Split Phase**):
    1.  **Fase de Cálculo:** Construir un objeto intermedio de datos (`StatementData`) que contenga toda la información calculada.
    2.  **Fase de Presentación (Rendering):** Utilizar ese objeto intermedio para dar el formato deseado (texto plano, HTML, etc.).
