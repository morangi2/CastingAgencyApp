import json
import os
from urllib.request import urlopen
from flask import redirect, request, session, url_for
from functools import wraps
from jose import jwt

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://' + os.environ['AUTH0_DOMAIN'] + '/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=os.environ['ALGORITHMS'],
                audience=os.environ['API_AUDIENCE'],
                issuer='https://' + os.environ['AUTH0_DOMAIN'] + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)
    # raise Exception('Not Implemented')


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError(
            {
                'code': 'missing_permissions_string',
                'description': 'Requested permission string is not in the payload permissions array.'
            }, 400
        )
    
    if len(payload['permissions']) == 0:
        raise AuthError(
            {
                'code': 'missing_permissions_string',
                'description': 'sorry, your account has not been assigned any permissions yet.'
            }, 401
        )
    
    if permission not in payload['permissions']:
        raise AuthError(
            {
                'code': 'permissions_not_included',
                'description': 'sorry, you do not have permission to perform this action'
            }, 403
        )
    
    return True
    #raise Exception('Not Implemented')



"""
create a new decorator that validates the user session, 
and if no session is found it will redirect the users automatically to the login view. 
If, on the contrary, there's an existing session we'll continue with the default method.
"""
"""
def requires_auth(f):
    # use on routes that need a valid session, otherwise abort with a 403 status code
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('user') is None:
            return redirect(url_for('auth.login'))

        access_token = session.get('user').get('access_token')
        print('**AAACCEESS TKN*****')
        print(access_token)

        return f(*args, **kwargs)

    return decorated
"""

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if session.get('user') is None:
                return redirect(url_for('auth.login'))
            else:
                token = session.get('user').get('access_token')
                print('***heres the token***')
                print(token)
                payload = verify_decode_jwt(token)
                check_permissions(permission, payload)
                return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator