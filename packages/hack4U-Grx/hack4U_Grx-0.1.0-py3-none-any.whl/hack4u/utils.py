#!/usr/bin/env python3

from .cursos import cursos

def total_duration():
    return sum(i.duration for i in cursos)