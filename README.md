# Ejemplo actualizado de API TODO

Ejemplo de API TODO en flask de Miguel Grinberg basado en el artículo
[Designing a RESTful API with Python and Flask](
https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask). Debido a que el artículo
data del 20 de Mayo 2023, se han realizado ajustes en el código y
documentación del mismo para que sea funcional con la versión de Python
que se encuentra en `runtime.txt` y las bibliotecas que se encuentran en
`requirements.txt`.

## Para consumir la API

Todos los ejemplos de métodos `HTML` a continuación se realizan desde un
`cmd` de `Windows`.

### Para obtener una tarea por `id` (`GET`)

`>>> curl -u <user>:<pass> -i <host>/todo/api/v1.0/tareas/<id>`

### Para obtener todas las tareas (`GET`)

`>>> curl -u <user>:<pass> -i <host>/todo/api/v1.0/tareas`

### Para crear una tarea nueva (`POST`)

`>>> curl -u <user>:<pass> -i -H "Content-Type: application/json"
-X POST -d "{\"nombre\":\"<nombre tarea>\",\"descripcion\":
\"<descripcion tarea>\"}" <host>/todo/api/v1.0/tareas`

### Para actualizar una tarea existente por `id` (`PUT`)

`>>> curl -u <user>:<pass> -i -H "Content-Type: application/json" -X PUT
-d "{\"nombre\":\"<nombre tarea>\",\"descripcion\":
\"<descripcion tarea>\",\"terminada\":<true o false>}"
<host>/todo/api/v1.0/tareas/<id>`

### Para eliminar una tarea existente por `id` (`DELETE`)

`>>> curl -u <user>:<pass> -i -X DELETE <host>/todo/api/v1.0/tareas/<id>`


