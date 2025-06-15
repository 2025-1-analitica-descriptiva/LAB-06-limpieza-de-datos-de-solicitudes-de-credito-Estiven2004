"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y dats faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los dats.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """

    import pandas as pd
    import os

    dats = pd.read_csv("files/input/solicitudes_de_credito.csv", sep=";")

    dats = dats.dropna()
    dats["sexo"] = dats["sexo"].str.lower()
    dats["tipo_de_emprendimiento"] = dats["tipo_de_emprendimiento"].str.lower()

    dats["idea_negocio"] = (
        dats["idea_negocio"]
        .str.lower()
        .str.replace("_", " ", regex=False)
        .str.replace("-", " ", regex=False)
        .str.strip()
    )

    dats["barrio"] = (
        dats["barrio"]
        .str.lower()
        .str.replace("_", " ", regex=False)
        .str.replace("-", " ", regex=False)
    )

    def norm_dates(fecha):
       
        parts = fecha.split("/")
        if len(parts[0]) == 4:
            return f"{parts[2]}/{parts[1]}/{parts[0]}"
        return fecha

    dats["fecha_de_beneficio"] = dats["fecha_de_beneficio"].apply(norm_dates)

    dats["monto_del_credito"] = (
        dats["monto_del_credito"]
        .str.replace(" ", "", regex=False)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .astype(float)
    )

    dats["línea_credito"] = (
        dats["línea_credito"]
        .str.lower()
        .str.replace("_", " ", regex=False)
        .str.replace("-", " ", regex=False)
    )

    col_unis = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "estrato",
        "comuna_ciudadano",
        "fecha_de_beneficio",
        "monto_del_credito",
        "línea_credito"
    ]
   
    dats = dats.drop_duplicates(subset=col_unis)

    os.makedirs(os.path.dirname("files/output/solicitudes_de_credito.csv"), exist_ok=True)
   
    dats.to_csv("files/output/solicitudes_de_credito.csv", sep=";", index=False)
