# Proyecto MISW-4202 2024-14

Experimiento de Disponibilidad de Software - Sprint 1
Arwquitectura de estilo Microservicios con comunicación asincrónica

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
soruce venv/bin/activate
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

## 8. Comprobar resultados

Una vez se haya levantado 
