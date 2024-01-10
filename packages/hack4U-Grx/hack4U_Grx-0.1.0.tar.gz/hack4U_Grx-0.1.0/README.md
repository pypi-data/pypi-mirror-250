# Hack4u Academy Cursos Library
 
Una Bilbioteca Python para consultar cursos de la academia Hack4U

## Cursos disponibles:

- Introducción a Linux
- Personalización de Linux
- Introducción al Hacking
- Python Ofensivo

## Instalación

Instala el paquete usando `pip3`:
```python3
pip3 install hack4u
```
## Uso básico

### Listar todos los cursos
```python3
from hack4u import list_curso

for i in list_curso():
    print(i)
```

### Obtener un curso por nombre:
```python3
from hack4u import search_curso_by_name

curso = search_curso_by_name("Introducción a Linux")
print(curso)
```

### Calcular el tiempo total de los cursos
```python3
from hack4u.utils import total_duration

print(f"Duración total: {total_duration()} horas")
```