# Proyecto MISW-4202 2024-14

Experimiento de Seguridad de Software - Seguridad
Arquitectura de estilo Microservicios

# Integrantes Grupo 11

| Nombre                 | Email                          |
| ---------------------- | ------------------------------ |
| Héctor Oswaldo Franco  | h.franco@uniandes.edu.co       |
| Manuel Felipe Bejarano | mf.bejaranob1@uniandes.edu.co  |
| Juan Sebastián Vargas  | js.vargasq1@uniandes.edu.co    |
| Publio Díaz Paez       | p.diazp@uniandes.edu.co        |

# Video de la demostración
[![Validación de seguridad - Experimento - Semana 8 - MISO - Arquitecturas ágiles de software](https://img.youtube.com/vi/mtzbY15zpho/mqdefault.jpg)](https://youtu.be/mtzbY15zpho)


# Instrucciones de ejecución del experimento

## 1. Clonar el proyecto
Ejecutar el siguiente comando en una directorio libre
```bash
git clone https://github.com/JSVargasQ/MISO-ArquitecturasAgiles-2024-14.git
```

## 2. Crear y ejecutar un Ambiente Virtual (venv) en la raíz del proyecto
Comando para crear el Ambiente Virtual de Python

```bash
python3 -m venv venv
```
Comando para ejecutar el Ambiente Virtual creado

```bash
source venv/bin/activate
```

## 3. Instalación
Para instalar las dependencias del proyecto ejecute el siguiente comando en la raíz del proyecto
```bash
pip install -r requirements.txt
```

## 4. Ejecutar servidor de Redis
Levantar servidor de redis (local o imagen de docker)


## 5. Levantar los servicios de la cola de mensajeria 

Ejecutar cada cola en una instancia distinta de la términal o CMD dentro de la carpeta raíz del proyecto.

NOTA: Preferiblemente ejecutar estos comandos desde la terminal integrada de Visual Studio Code y dentro de un sistema Linux o UNIX 

1. Cola del Integrity Validator

```bash
celery -A integrity_validator.tasks.queue  worker  -l info -Q send_alert
```

2. Cola que guarda la request original antes de ser modificada en el MITM

```bash
celery -A MITM.tasks.queue worker -l info -Q original_request
```

3. Cola que guarda la request modificada después de ser modificada en el MITM

```bash
celery -A MITM.tasks.queue worker -l info -Q modified_request
```

Imagen de referencia de la ejecución de las colas de Celery con REDIS en distintas instancias de la terminal de VS Code 

<img width="1683" alt="Screenshot 2024-09-28 at 11 24 50 PM" src="https://github.com/user-attachments/assets/b86dac09-33ce-44d2-a794-4ed0e1b3f0ad">


## 6. Ejecutar el Man in the Middle 
Abrir una terminal nueva y ejecutar el Man in the Middle con el siguiente comando
```bash
mitmproxy --mode reverse:http://127.0.0.1:5002/ -s MITM/app.py
```
Imagen de referencia con el MITM ejecutandose en una instancia independiente de la terminal integrada de VS Code

<img width="1681" alt="Screenshot 2024-09-28 at 11 36 33 PM" src="https://github.com/user-attachments/assets/acbaa2a5-26a4-4caa-9372-8a936a5e1764">


## 7. Levantar el componente Integrity Validator
Servicio de Call Handling
```bash
cd integrity_validator
flask run -p 5000
```

## 8. Levantar los Microservicios

Servicio de Call Handling
```bash
cd ms_user_management
flask run -p 5001
```

Servicio de User Management
```bash
cd ms_pqrs_management
flask --app pqrs run -p 5002
```
Imagen de referencia de la ejecución de los servicios en distintas instancias de la terminal de VS Code 


<img width="1682" alt="Screenshot 2024-09-28 at 11 30 18 PM" src="https://github.com/user-attachments/assets/e8f1c62e-5527-4e61-b57c-6b52c3440013">



## 8. Ver la ejecución del experimento

Puede ir a ver los archivos de los resultados del experimento en estos archivos

1. integrity_validator/tasks/send_alert_simulation.txt
2. MITM/tasks/original_request.txt
2. MITM/tasks/modified_request.txt
3. instance/validator.db

## 9. Comprobar resultados

Puede comprobar el resultado del experimento en el siguiente enlace

1. [Presentación del experimento](https://docs.google.com/presentation/d/1OXmXPsKrinOluq2WC6b2i9dH7cQS_o-S/edit?usp=sharing&ouid=104474903328127988920&rtpof=true&sd=true)
