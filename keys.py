import uuid
import secrets

print('Resultado con uuid:')
print(uuid.uuid4().hex)
print('Resultado con secrets:')
print(secrets.token_hex(64))