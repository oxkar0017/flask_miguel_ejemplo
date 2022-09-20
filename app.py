from flask import abort, Flask, jsonify, make_response, request, url_for
from flask import wrappers
from flask_httpauth import HTTPBasicAuth
from typing import Optional


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
    caso de no existir el identificador, se presenta el error `404`

    :param id: Identificador de la tarea en `tareas`
    :type id: int
    :return: Json publicando la tarea con llaves `uri`, `nombre`,
      `descripcion` y `finalizado`
    :rtype: wrappers.Response
    """
    tarea = [t for t in tareas if t['id'] == id]
    assert tarea, abort(404)

    return jsonify({'tarea': publicar_tarea(tarea[0])})
