#!/usr/bin/env python3

class Curso:
    def __init__(self, name, duration, link):
        self.name = name
        self.duration = duration
        self.link = link
    
    def __repr__(self): #similar a __str__
        return f"{self.name} [{self.duration} horas] ({self.link})"



cursos = [
    Curso("Introducción a Linux", 15, "https://hack4u.io/cursos/introduccion-a-linux/11149" ),
    Curso("Personalización de Linux", 3, "https://hack4u.io/cursos/personalizacion-de-entorno-en-linux/14290"),
    Curso("Introducción al Hacking", 53, "https://hack4u.io/cursos/introduccion-al-hacking/14610"),
    Curso("Python Ofensivo", 35, "https://hack4u.io/cursos/python-ofensivo/18870")
]

def list_curso():
    for i in cursos:
        print(i)

def search_curso_by_name(name):
    for i in cursos:
        if i.name == name:
            return i
        
    return None
