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
