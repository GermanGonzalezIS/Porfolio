from usuarios.models import Entidad_Federativa
import csv


def run():
    with open('usuarios/entidades_federativas.csv') as file:
        reader = csv.reader(file)

        for row in reader:

            entidad = Entidad_Federativa.objects.get_or_create(
                clave=row[0],
                entidad=row[1]
                )