import redis
import random

# Conexión a Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Ejemplo: establecer una clave con un valor
r.set('nombre', 'Juan')

# Obtener el valor de la clave
nombre = r.get('nombre')
print(f"Nombre: {nombre.decode('utf-8')}")  # Decodificar porque Redis devuelve bytes

# Establecer un valor con un tiempo de expiración (en segundos)
r.setex('temporal', 10, 'Este valor expira en 10 segundos')

# Obtener el valor de una clave que expira
temporal = r.get('temporal')
print(f"Temporal: {temporal.decode('utf-8') if temporal else 'El valor expiró'}")

# Incrementar un valor numérico
r.set('contador', 0)
r.incr('contador')
contador = r.get('contador')
print(f"Contador: {contador.decode('utf-8')}")

# Borrar una clave
# r.delete('nombre')

def generar_numero_aleatorio(minimo, maximo):
    return random.randint(minimo, maximo)

# Llamar a la función para obtener un número aleatorio entre 1 y 13
numero = generar_numero_aleatorio(1, 3)
print(numero)