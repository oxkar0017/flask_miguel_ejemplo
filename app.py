from flask import abort, Flask, jsonify, make_response, request, url_for
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
