# Proyecto MISW-4202 2024-14

Grupo 11

## Integrantes
1. Publio Díaz
2. Manuel Bejarano
3. Juan Sebastián Vargas
4. Héctor Franco

## Instrucciones de ejecución

## 1. Instalación

## 2. Ejecución

## Correr servidor de Redis - Celery
1. Levantar servidor de redis (local o imagen de docker)
2. Correr el siguiente comando 

```bash
celery -A ms_call_handling.logs.logs worker -l info -Q health_logs
```