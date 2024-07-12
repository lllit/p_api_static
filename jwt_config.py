from jwt import encode, decode


def get_token(dato:dict) -> str:
    token: str = encode(payload=dato, key='my_pass', algorithm='HS256')
    return token

def validar_token(token: str) -> dict:
    dato: dict = decode(token, key='my_pass', algorithms=['HS256'])
    return dato