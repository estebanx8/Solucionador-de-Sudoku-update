# Solucionador de Sudokus con Interfaz Gráfica Mejorada

Este proyecto es un **fork** del repositorio original [Solucionador-de-Sudokus](https://github.com/Jeremy-Vanegas/Solucionador-de-Sudokus) de Jeremy Vanegas.  
Aquí se han realizado varias mejoras para optimizar la experiencia de usuario y la funcionalidad del solucionador de Sudokus en Python usando Tkinter.

---

## Mejoras respecto al código original

- **Barra de progreso animada y precisa:**  
  Ahora el usuario puede ver el avance real del proceso de resolución del Sudoku, con una barra de progreso que se actualiza dinámicamente durante el cálculo.

- **Interfaz no bloqueante:**  
  El proceso de resolución se ejecuta en un hilo separado, permitiendo que la interfaz gráfica permanezca siempre activa y responsiva.

- **Validación mejorada de entradas:**  
  El sistema detecta y muestra mensajes de error si se ingresan letras, números fuera de rango o más de un dígito por celda.

- **Colores diferenciados en la solución:**  
  Los números originales del Sudoku aparecen en rojo y los números calculados por el solucionador en verde, facilitando la visualización de la solución.

- **Mensajes de estado claros:**  
  Se informa al usuario si el Sudoku fue resuelto, si hubo un error en la entrada o si el Sudoku no tiene solución.

---

## Requisitos

- Python 3.x
- Tkinter (incluido en la mayoría de instalaciones de Python)
- No requiere librerías externas adicionales

---

## Uso

1. **Clona este repositorio o descarga el archivo `Sudoku_Tkinter.py`.**
2. Ejecuta el archivo:
   ```bash
   python Sudoku_Tkinter.py
   ```
3. Ingresa tu Sudoku en la cuadrícula (deja en blanco las celdas vacías).
4. Haz clic en **"Resolver"** para ver la solución y el progreso.
5. Usa **"Nuevo Sudoku"** para limpiar la cuadrícula o **"Ejemplo para resolver"** para cargar un Sudoku de prueba.

---

## Créditos

- Código base: [Jeremy Vanegas](https://github.com/Jeremy-Vanegas/Solucionador-de-Sudokus)
- Mejoras y optimización de interfaz: [Esteban Torres] (https://github.com/estebanx8)

---

¡Disfruta resolviendo Sudokus con una experiencia visual mejorada!
