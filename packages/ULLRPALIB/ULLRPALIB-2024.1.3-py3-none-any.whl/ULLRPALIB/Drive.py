from Driveup.drive import Drive
from Driveup.features.auth import authorize

import pandas as pd
import sys
from datetime import datetime, time, timedelta
import socket
import platform
import getpass

SECRET_PATH = "Z:\\RPA\RPA23\\0000_Utils\\Ultrasecreto\\Robi_ultrasecreto.json"

AUTOMATIZACIONES_SHEET_ID = "18ayh5C5l1c782_ZbAalzsi3PPiiYY2FMi41-8w2sFNM" # https://docs.google.com/spreadsheets/d/18ayh5C5l1c782_ZbAalzsi3PPiiYY2FMi41-8w2sFNM

def robi_drive():
    creds = authorize(SECRET_PATH)
    drive = Drive(creds)

    return drive

def record_last_execution(auto_number):

    drive = robi_drive()
    
    auto_number = "{:0>4}".format(str(auto_number))

    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    df = drive.df_download(AUTOMATIZACIONES_SHEET_ID,"Auto",unformat=True)

    df.loc[df['Automatización'] == auto_number, 'Última ejecución'] = now

    drive.df_update(df,AUTOMATIZACIONES_SHEET_ID,"Auto",unformat=True)

def record_complete_execution(auto_number,execution_start=None,notas_text=None):

    auto_number = "{:0>4}".format(str(auto_number))

    record_last_execution(auto_number)
    
    drive = robi_drive()

    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    df_auto = drive.df_download(AUTOMATIZACIONES_SHEET_ID,"Auto",unformat=True)

    df = drive.df_download(AUTOMATIZACIONES_SHEET_ID,"Execution History",unformat=True)

    if df_auto.loc[df_auto['Automatización'] == auto_number, 'Frecuencia de ejecución'].values[0] == 'Diaria':
        hora_prevista = df_auto.loc[df_auto['Automatización'] == auto_number, 'Hora de ejecución'].values[0]
    else: 
        hora_prevista = 'No prevista'

    routine_check = False

    if hora_prevista != 'No prevista':

        lista_horas_previstas = hora_prevista.split(";")

        hours_count = 0
        while(routine_check == False and hours_count < len(lista_horas_previstas)):
            current_hour = lista_horas_previstas[hours_count]
            if in_time(current_hour):
                routine_check = True
            hours_count +=1

    execution_time = None

    if execution_start != None:
        execution_time = datetime.now() - execution_start

    if routine_check and notas_text == None:
        notas_text = f'Ejecución rutinaria de la automatización {auto_number}'


    execution_row = pd.DataFrame({
        'Automatización': auto_number,
        'Fecha de ejecución': now,
        'Hora prevista': hora_prevista,
        'Tiempo de ejecución': execution_time if execution_time != None else "Desconocido",
        'Tipo de ejecución': "Rutinaria" if routine_check else "No rutinaria",
        'Host': socket.gethostname(),
        'Usuario': getpass.getuser(),
        'Sistema operativo': f'{platform.system()} {platform.version()}',
        'Estructura': platform.machine(),	
        'Arquitectura': " ".join(platform.architecture()),
        'Notas': notas_text
    },index=[0])

    new_df = pd.concat([df,execution_row])

    drive.df_update(new_df,AUTOMATIZACIONES_SHEET_ID,"Execution History",unformat=True)

def in_time(target_time,margin=[0,25,0]):
    current_time = datetime.now().time()
    margin_time = timedelta(hours=margin[0], minutes=margin[1], seconds=margin[2])

    target_time_converted = datetime.strptime(target_time, '%H:%M:%S').time()

    # Add the margin to the target time
    time_after_margin = (datetime.combine(datetime.today(), target_time_converted) + margin_time).time()

    # # Subtract the margin from the target time
    # time_before_margin = (datetime.combine(datetime.today(), target_time_converted) - margin_time).time()

    if current_time > target_time_converted and current_time < time_after_margin:
        in_time_checker = True
    else:
        in_time_checker = False

    return in_time_checker