<h1 style="text-align: center;">Things to do: RayCasting</h1>

---

Esta es una lista de cosas que quiero implementar sobre ray tracing de primeras. La idea es hacerlo sobre una matriz de pixeles en 2D ya que posteriormente quiero llevarlo a un juego de Voxeles en 3D. Primero quiero empezar implementando las cosas más básicas y poco a poco ir añadiendo funcionalidades y optimizaciones. Al usarlo sobre una cuadrícula encontramos algunas ventajas de eficiencia y además me gustaría poder optimizarlo más utilizando Quadtrees en 2D o Octrees en 3D, ya que de la forma normal estaría recorriendo demasiados puntos vacíos en el espacio, que se pueden reducir mediante estas técnicas, lo que aún no se si es posible. 

- [x] Implementar algoritmo de ray tracing: `ray_trace.py`
- [x] Codificar PyGame de manera que se pueda utilizar como plantilla para cada juego que quiera hacer con píxeles: `game.py`
- [x] Implementar el algoritmo para un único rayo y que se pueda visualizar: `one_ray.py`. 
- [ ] Implementar rayos en todas las direcciones de un jugador, basicamente crear una _linterna_ en un juego de píxeles 2D:
  - [x] Hacer que funcione con blanco y negro, donde el blanco markara todo lo que puede ver `lantern_MINE.py`. Esta es una implementación donde se tiran rayos para todas las direcciones, creada a partir de la implementación de un único rayo, sin saber como se suele hacer de forma más eficiente y implementada completamente por mi. 
  Funciona feo porque deja muchas lineas negras por el medio pero es un inicio y una forma chula de visualizarlo, además que está hecha por mi.
  - [x] Hacerlo direccional.
  - [x] Implementar que se vean solo los cuadrados a los que llegan los rayos y poder ir a "oscuras" con la linterna encendida.
  - [ ] Implementar el algoritmo pero que sea eficiente y de la forma "correcta": `lantern_GOOD.py`. En este caso el algoritmo funciona muy diferente a como lo había planteado. No merece la pena tirar rayos en todas las direcciones porque consume mucho (aunque me vaya a +300 FPS no es worth). Se suele detectar primero los bordes de los objetos y se mapean, de esta forma tienes muchos menos datos con los que trabajar y es más fácil y eficiente. 
  - [ ] Hacer el efecto de una linterna real?
- [ ] Añadir Quadtrees?
- [ ] HACER QUE NUMBA COMPILE AL INICIO. Por ahora con lo de "cache=True" sirve pero no es lo óptimo (o sí?).
- [ ] Llevarlo a 3D. _(Futuro)_
