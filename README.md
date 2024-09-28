# Proyecto MISW-4202 2024-14

Experimiento de Disponibilidad de Software - Sprint 1
Arquitectura de estilo Microservicios con comunicación asincrónica

# Integrantes Grupo 11

| Nombre                 | Email                          |
| ---------------------- | ------------------------------ |
| Héctor Oswaldo Franco  | h.franco@uniandes.edu.co       |
| Manuel Felipe Bejarano | mf.bejaranob1@uniandes.edu.co  |
| Juan Sebastián Vargas  | js.vargasq1@uniandes.edu.co    |
| Publio Díaz Paez       | p.diazp@uniandes.edu.co        |

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

1. Cola del monitor que va hacia los Microservicios

```bash
celery -A monitor.tasks.queue worker -l info -Q health_check
```

2. Cola de Health Response que responde desde los Microservicios hacia el Monitor

```bash
celery -A ms_call_handling.tasks.queue worker -l info -Q health_response
```

3. Cola del logger del Microservicio de Call Handling cuando se realiza la petición

```bash
celery -A ms_call_handling.tasks.queue worker -l info -Q monitor_calls_logs
```

4. Cola del logger del Microservicio de User Management cuando se realiza la petición

```bash
celery -A ms_user_management.tasks.queue worker -l info -Q monitor_users_logs
```
Imagen de referencia de la ejecución de las colas de Celery con REDIS en distintas instancias de la terminal de VS Code 

![Screenshot 2024-09-08 at 9 30 35 PM](https://github.com/user-attachments/assets/83259a05-e2e2-41a2-8fa5-c15b3a37c294)


## 6. Levantar los Microservicios

Servicio de Call Handling
```bash
cd ms_call_handling
flask run -p 5001
```

Servicio de User Management
```bash
cd ms_user_management
flask run -p 5002
```

## 7. Levantar el componente Monitor
Servicio de Call Handling
```bash
cd monitor
flask run -p 5000
```
Imagen de referencia de la ejecución de los servicios en distintas instancias de la terminal de VS Code 

![Screenshot 2024-09-08 at 9 32 45 PM](https://github.com/user-attachments/assets/6322a3c6-1a8a-44bf-8722-5f2f27c62570)

## 8. Comprobar resultados

Puede comprobar el resultado del experimento en los siguientes enlaces

1. [Analísis cuantitativo en Looker Studio](https://lookerstudio.google.com/u/0/reporting/78fcc402-1401-4ac0-8a6c-0cd8a7d85644/page/Gg3)
2. [Presentación del experimento](https://docs.google.com/presentation/d/15z_ZGMFctxYSBiOPJ_o3gk4V7D6VAych/edit?usp=sharing&ouid=104474903328127988920&rtpof=true&sd=true)

## 9. Ejecutar el Man in the Middle 
```bash
mitmproxy --mode reverse:http://127.0.0.1:5002/ -s MITM/app.py
```
