from flask import abort, Flask, jsonify, make_response, request, url_for
from flask import wrappers
from flask_httpauth import HTTPBasicAuth
from typing import Optional, Tuple


app = Flask(__name__, static_url_path='')
auth = HTTPBasicAuth()


@auth.get_password
def get_password(usuario: str) -> Optional[str]:
    """Devuelve la contraseña de `miguel` o None en caso contrario

    :param usuario: Usuario
    :type usuario: str
    :return: Contraseña
    :rtype: Optional[str]
    """
    if usuario == 'miguel':
        return 'python'

    return None


@auth.error_handler
def unauthorized() -> wrappers.Response:
    """Genera error `403` por acceso no autorizado, en lugar de `401`
    para evitar que los navegadores muestren el cuadro de diálogo de
    autenticación predeterminado

    :return: Error `403` de acceso no autorizado
    :rtype: wrappers.Response
    """
    return make_response(jsonify({'error': 'Acceso no autorizado'}), 403)


@app.errorhandler(400)
def bad_request() -> wrappers.Response:
    """Genera error `400` por un error en la solicitud por parte del
    cliente

    :return: Error `400` de mala solicitud
    :rtype: wrappers.Response
    """
    return make_response(jsonify({'error': 'Mala solicitud'}), 400)


app = Flask(__name__, static_url_path='')


tareas = [
    {
        'id': 1,
        'nombre': u'Comprar comida',
        'descripcion': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'terminada': False
    },
    {
        'id': 2,
        'nombre': u'Aprender python',
        'descripcion': (
            u'Necesito encontrar un buen sitio web de tutorial python'), 
        'terminada': False
    }
]


def publicar_tarea(tarea: dict) -> dict:
    """Publica json de una tarea generando el endpoint para visualizar
    la misma

    :param tarea: Diccionario con llaves `id`, `nombre`, `descripcion` y
      `terminada`
    :type tarea: dict
    :return: Diccionario con llaves `uri`, `nombre`, `descripcion` y
      `terminada`
    :rtype: dict
    """
    vista_tarea = {}
    for llave in tarea:
        if llave == 'id':
            vista_tarea['uri'] = url_for(
                'obtener_tarea', id=tarea['id'], _external=True)
        else:
            vista_tarea[llave] = tarea[llave]

    return vista_tarea


@app.route('/todo/api/v1.0/tareas/<int:id>', methods=['GET'])
@auth.login_required
def obtener_tarea(id: int) -> wrappers.Response:
    """Solicita la información de la tarea identificada por `id`. En
    caso de no existir el identificador, se presenta el error `404`.
    Para realizar el método `GET` para obtener una tarea se digita el
    comando

    >>> curl -u <user>:<pass> -i <host>/todo/api/v1.0/tasks/<id>

    :param id: Identificador de la tarea en `tareas`
    :type id: int
    :return: Json publicando la tarea con llaves `uri`, `nombre`,
      `descripcion` y `terminada`
    :rtype: wrappers.Response
    """
    tarea = [t for t in tareas if t['id'] == id]
    assert tarea, abort(404)

    return jsonify({'tarea': publicar_tarea(tarea[0])})


@app.route('/todo/api/v1.0/tareas', methods=['GET'])
@auth.login_required
def obtener_tareas() -> wrappers.Response:
    """Solicita la información de todas las tareas. Para realizar el
    método `GET` para obtener todas las tareas se digita el comando

    >>> curl -u <user>:<pass> -i <host>/todo/api/v1.0/tasks

    :return: Json publicando todas las tareas con llaves `uri`,
      `nombre`, `descripcion` y `terminada`
    :rtype: wrappers.Response
    """
    return jsonify({'tareas': [publicar_tarea(t) for t in tareas]})


@app.route('/todo/api/v1.0/tareas', methods=['POST'])
@auth.login_required
def crear_tarea() -> Tuple[wrappers.Response, int]:
    """Agrega una tarea nueva a la base de datos `tareas` generando como
    respuesta el valor `201`. Para realizar el método `POST` para
    crear una tarea nueva se digita el comando

    >>> curl -u <user>:<pass> -i -H "Content-Type: application/json" -X POST -d 
    "{\"nombre\":\"<nombre tarea>\",\"descripcion\":\"<descripcion tarea>\"}" 
    <host>/todo/api/v1.0/tasks

    :return: Json publicando la nueva tarea con llaves `uri`, `nombre`,
      `descripcion` y `terminada`, y el valor `201`
    :rtype: Tuple[wrappers.Response, int]
    """
    tarea_nueva = request.json
    assert tarea_nueva and 'nombre' in tarea_nueva, abort(400)

    tarea = {
        'id': tareas[-1]['id'] + 1,
        'nombre': tarea_nueva['nombre'],
        'descripcion': tarea_nueva.get('descripcion', ''),
        'terminada': False
    }
    tareas.append(tarea)

    return jsonify({'tarea': publicar_tarea(tarea)}), 201


@app.route('/todo/api/v1.0/tareas/<int:id>', methods=['PUT'])
@auth.login_required
def actualizar_tarea(id: int) -> wrappers.Response:
    """Actualiza los valores `nombre`, `descripcion` o `terminada` para
    una tarea existente en `tareas` con identificador `id`. Para
    realizar el método `PUT` para actualizar una tarea vieja se digita
    el comando

    >>> curl -u <user>:<pass> -i -H "Content-Type: application/json" -X PUT -d 
    "{\"nombre\":\"<nombre tarea>\",\"descripcion\":\"<descripcion tarea>\",\"terminada\":\"<true o false>\"}" 
    <host>/todo/api/v1.0/tasks/<id>

    :param id: Identificador de la tarea
    :type id: int
    :return: Json publicando la nueva tarea con llaves `uri`, `nombre`,
      `descripcion` y `terminada`
    :rtype : wrappers.Response
    """
    tarea = [t for t in tareas if t['id'] == id]
    tarea_act = request.json

    cond_no_error_cliente = (
        tarea
        and tarea_act
        and ('nombre' not in tarea_act or isinstance(tarea_act['nombre'], str))
        and ('descripcion' not in tarea_act or isinstance(tarea_act['descripcion'], str))
        and ('terminada' not in tarea_act or isinstance(tarea_act['terminada'], bool))
        and ('nombre' in tarea_act or 'descripcion' in tarea_act or 'terminada' in tarea_act))
    assert cond_no_error_cliente, abort(404)

    tarea = tarea[0]

    tarea['nombre'] = tarea_act.get('nombre', tarea['nombre'])
    tarea['descripcion'] = tarea_act.get('descripcion', tarea['descripcion'])
    tarea['terminada'] = tarea_act.get('terminada', tarea['terminada'])

    return jsonify({'tarea': publicar_tarea(tarea[0])})
