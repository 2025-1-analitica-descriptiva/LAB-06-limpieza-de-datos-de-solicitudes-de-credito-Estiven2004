"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""
import pandas as pd
import numpy as np
import unicodedata
import re
import os

def pregunta_01():
    # Leer el archivo CSV
    df = pd.read_csv("files/input/solicitudes_de_credito.csv", sep=";",decimal=".", index_col=0)

    # Eliminar na's
    df = df.dropna()

    # Función de normalización
    def normalizar_texto(texto):
        if pd.isnull(texto):
            return np.nan
        texto = str(texto).lower().strip()
        texto = str(texto).replace("_"," ")
        texto = str(texto).replace("  "," ")
        texto = str(texto).replace("-"," ")
        texto = re.sub(r"\s+", " ", texto)
        texto = unicodedata.normalize("NFKD", texto).encode("ascii", errors="ignore").decode("utf-8")
        return texto

    # Normalizar columnas tipo texto
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].apply(normalizar_texto)

    # Corregir formato de fechas
    def parse_mixed_dates(date_str):
        """
        Función para parsear fechas en múltiples formatos
        """
        if pd.isna(date_str):
            return None
        
        # Lista de formatos posibles
        formats = ['%d/%m/%y', '%y/%m/%d', '%d/%m/%Y', '%Y/%m/%d']
        
        for fmt in formats:
            try:
                return pd.to_datetime(date_str, format=fmt)
            except ValueError:
                continue
        
        # Si ningún formato funciona, intentar parseo automático
        try:
            return pd.to_datetime(date_str, infer_datetime_format=True)
        except:
            return None
        
    df["fecha_de_beneficio"] = df["fecha_de_beneficio"].apply(parse_mixed_dates)

    # Limpiar y convertir montos a numérico
    df["monto_del_credito"] = (
        df["monto_del_credito"]
        .astype(str)
        .str.replace(r"[^\d]", "", regex=True)
        .replace("", np.nan)
        .astype(float)
    )

    # Limpiar valores inválidos
    df = df[df['monto_del_credito'] > 0]

    # # Eliminar na's
    # df = df.dropna()
    
    # Eliminar duplicados
    df = df.drop_duplicates()

    # Limpiar valores inválidos
    df = df[df['monto_del_credito'] > 0] 

    # Crear carpeta output si no existe
    if not os.path.exists("files/output"):
        os.makedirs("files/output")
    # print(df.sexo.value_counts())
    # print(df.línea_credito.value_counts())
    # print(df.idea_negocio.value_counts())
    # print(df.comuna_ciudadano.value_counts())
    print(df.barrio.value_counts())
    # print(df.info())
    # def verificar_y_limpiar_barrio_comuna(df):
    #     """
    #     Verifica que cada barrio esté asociado siempre a la misma comuna
    #     y elimina las filas con inconsistencias
    #     """
    #     print("🔍 VERIFICANDO CONSISTENCIA BARRIO-COMUNA")
    #     print("=" * 50)
        
    #     df_original = df.copy()
    #     filas_a_eliminar = set()
        
    #     # 1. Agrupar por barrio y verificar si hay más de una comuna por barrio
    #     barrios_comunas = df.groupby('barrio')['comuna_ciudadano'].nunique()
        
    #     # 2. Encontrar barrios con más de una comuna
    #     barrios_inconsistentes = barrios_comunas[barrios_comunas > 1]
        
    #     if len(barrios_inconsistentes) == 0:
    #         print("✅ Todos los barrios están consistentemente en una sola comuna")
    #         return df_original
    #     else:
    #         print(f"❌ Se encontraron {len(barrios_inconsistentes)} barrios con inconsistencias:")
    #         print("-" * 40)
            
    #         # 3. Para cada barrio inconsistente, determinar la comuna correcta y marcar filas para eliminar
    #         for barrio in barrios_inconsistentes.index:
    #             # Obtener todas las comunas para este barrio
    #             comunas_barrio = df[df['barrio'] == barrio]['comuna_ciudadano'].value_counts()
                
    #             # La comuna correcta es la más frecuente
    #             comuna_correcta = comunas_barrio.index[0]
    #             total_registros = comunas_barrio.sum()
    #             registros_correctos = comunas_barrio.iloc[0]
    #             registros_incorrectos = total_registros - registros_correctos
                
    #             print(f"📍 Barrio: '{barrio}'")
    #             print(f"   Comuna correcta (más frecuente): {comuna_correcta} ({registros_correctos} registros)")
    #             print(f"   Comunas incorrectas:")
                
    #             # Marcar filas incorrectas para eliminación
    #             for i, (comuna, count) in enumerate(comunas_barrio.items()):
    #                 if i > 0:  # Saltar la primera (correcta)
    #                     print(f"     - {comuna}: {count} registros (SERÁN ELIMINADOS)")
    #                     # Encontrar índices de filas con esta combinación incorrecta
    #                     indices_incorrectos = df[(df['barrio'] == barrio) & 
    #                                         (df['comuna_ciudadano'] == comuna)].index
    #                     filas_a_eliminar.update(indices_incorrectos)
    #             print()
            
    #         # 4. Mostrar resumen y eliminar filas
    #         total_inconsistentes = len(filas_a_eliminar)
    #         print(f"📊 RESUMEN:")
    #         print(f"Total de filas originales: {len(df_original)}")
    #         print(f"Filas con inconsistencias a eliminar: {total_inconsistentes}")
    #         print(f"Porcentaje de filas a eliminar: {(total_inconsistentes/len(df_original))*100:.2f}%")
            
    #         # 5. Mostrar algunas filas que serán eliminadas (muestra)
    #         if total_inconsistentes > 0:
    #             print(f"\n🔍 Muestra de filas que serán eliminadas:")
    #             filas_muestra = list(filas_a_eliminar)[:5]
    #             print(df_original.loc[filas_muestra, ['barrio', 'comuna_ciudadano']])
                
    #             # Eliminar filas inconsistentes
    #             df_limpio = df_original.drop(index=filas_a_eliminar).reset_index(drop=True)
                
    #             print(f"\n✅ LIMPIEZA COMPLETADA:")
    #             print(f"Filas eliminadas: {total_inconsistentes}")
    #             print(f"Filas restantes: {len(df_limpio)}")
    #             print(f"Porcentaje de datos conservados: {(len(df_limpio)/len(df_original))*100:.2f}%")
                
    #             # Verificar que ahora esté consistente
    #             print(f"\n🔄 VERIFICACIÓN POST-LIMPIEZA:")
    #             barrios_comunas_limpio = df_limpio.groupby('barrio')['comuna_ciudadano'].nunique()
    #             barrios_inconsistentes_limpio = barrios_comunas_limpio[barrios_comunas_limpio > 1]
                
    #             if len(barrios_inconsistentes_limpio) == 0:
    #                 print("✅ Todos los barrios ahora están consistentemente en una sola comuna")
    #             else:
    #                 print(f"⚠️ Aún quedan {len(barrios_inconsistentes_limpio)} barrios inconsistentes")
                
    #             return df_limpio
            
    #         return df_original
        
    # df = verificar_y_limpiar_barrio_comuna(df)
    # Guardar el archivo limpio
    df.to_csv("files/output/solicitudes_de_credito.csv", sep=";", index=False)
    

pregunta_01()