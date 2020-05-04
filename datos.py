'''
Trabajo realizado por:
@Diego Valcarce Ríos
d.valcarce@udc.es
'''
import pandas as pd
import names
import random
from randomtimestamp import randomtimestamp as random_date

def ciclistas():
    '''
    Crea un CSV para la tabla ciclistas, que tiene los siguientes atributos:
    + UCI_ID -> PRIMARY KEY. Números del 000.000.000 al 999.999.999
    + Nombre -> Utilizaremos el módulo names
    + Sexo   -> Male or female
    + Edad   -> Valor comprendido entre 12 (edad mínima para federarse) y 99
    + Equipo -> Utilizaremos el módulo pandas para leer los equipos de la página oficial de la UCI
    + CIF    -> 100 números distintos, para apuntar a 100 marcas de bici. Clave forántea, puede haber repetidos

    Utilizaremos el módulo names para crear los nombres. 
    '''
    print(names.get_full_name())
    print(names.get_last_name())

    # Tenemos que leer las otras tablas, para coger las correpondientes a las claves foráneas
    equipo = pd.read_csv('equipos.csv')
    marcas = pd.read_csv('marcas.csv')

    # Creamos dataframe
    df = pd.DataFrame(columns = ['UCI_ID', 'id_compania', 'nombre', 'sexo', 'usuario_strava', 'usuario_zwift', 'id_equipo'])

    usuarios1 = []
    usuarios2 = []

    UCI_ID = 861051
    for i in range(10000):
        # Creamos nuestra lista de appendeamiento
        lista = []

        # ID
        lista.append(UCI_ID)

        # ID_compania
        id_e = random.choice(marcas['CIF'])
        # Si son ciclistas tienen bicis, no vamos a forzar nulos
        lista.append(id_e)

        # ID_equipo
        id_e = random.choice(equipo['id_equipo'])
        e = random.choices([id_e, ''], [0.95, 0.05])[0]
        lista.append(e)

        # Nombre
        name = names.get_full_name()
        lista.append(name)

        # Sexo
        sx = random.choices(['male', 'female', ''], [0.7, 0.25, 0.05])[0]
        lista.append(sx)

        # Usuario de strava, creamos una función recursiva para comprobar si está o no en strava ya
        strava = name.split()[1].lower()

        while strava in usuarios1:
            strava += str(random.randint(0, 10))

        usuarios1.append(strava)
        # Como es una tecnología, no tienen porque tenerlo todos
        strava = random.choices([strava.lower(), ''], [0.8, 0.2])[0]
        lista.append(strava)

        # Zwift, lo mismo:
        zwift = name.split()[1].lower()
        while zwift in usuarios2:
            zwift += str(random.randint(0, 10))
        
        usuarios2.append(zwift)
        lista.append(zwift)        

        df.loc[i] = lista

        UCI_ID += UCI_ID%2 + 1
        print('loading...')

    df.set_index('UCI_ID', inplace = True)
    df.to_csv('ciclistas.csv')
    print(df)


        


def marcas():
    '''
    Campos:
    + id_compania -> CIF de la compañía, clave primaria
    + n_modelos   -> número de modelos, número aleatorio entre 10 y 20
    + grupo       -> grupo que usan, será una de entre:
            - Shimano
            - Sram
            - Sensah
            - Rotor
            - Campagnolo
            - Avid
    '''
    # Para los nombres de los equipos, nos quedaremos con 100 nombres de name, los apellidos
    # con un CC delante
    grupos = 'Shimano, Sram, Sensah, Rotor, Campagnolo, Avid'.upper().split(', ')

    # Creamos nuestro dataframe
    df = pd.DataFrame(columns = ['CIF', 'nombre', 'n_modelos', 'grupo'])

    i = 0
    id_compania = 7621954
    for nombre in range(100):
        # Y ahora tenemos que ir generando la lista que appendear
        lista = []
        # Primero, el CIF:
        lista.append(id_compania)
        # Y variamos el CIF;
        id_compania += 1
        # Ahora añadimos el nombre del nombre
        lista.append('CC ' + names.get_last_name())
        # Ahora el número de modelos, entre 10 y 20, puede contener nulos
        n_modelos = random.randint(10, 20)
        n = random.choice([n_modelos, ''])
        lista.append(n)
        
        # Y ahora le ponemos un grupo, mismo procedimiento
        grupo = random.choice(grupos)
        m = random.choice([grupo, ''])
        lista.append(m)

        # Y ahora lo añadimos al dataframe
        df.loc[i] = lista
        i += 1
    
    print(df)
    # Ponemos el CIF como índice
    df.set_index('CIF', inplace = True)
    # Y ahora lo escribimos
    df.to_csv('marcas.csv', sep = ',')


def equipos():
    '''
    Campos:
    + id_equipo  -> Número de indentificacion, clave primaria
    + 
    ''' 
    datos = pd.read_html('https://www.ciclo21.com/equipos-uci-2020/')[-1]
    # Nos quedamos con la última posición, porque tenemos 170 equipos, en la columna que aparecen los nombres
    equipos = datos

    # Nuestro ddf
    df = pd.DataFrame(columns = ['id_equipo', 'n_equipo', 'n_integrantes', 'creacion', 'nacionalidad'])
    id_e = equipos[1]
    n_e = equipos[0]


    for _ in range(len(equipos)):
        lista = []

        # Añadimos nuestros id y nombres
        lista.append(id_e.loc[_])
        lista.append(n_e.loc[_])

        # Integrantes
        inte = random.randint(0, 100)
        n = random.choices([inte, ''], [0.7, 0.3])[0]
        lista.append(n)

        # Fecha de creación
        fecha_random = random_date()
        fecha = fecha_random[6:10] + '-' + fecha_random[3:5] + '-' + fecha_random[0:2]
        m = random.choices([fecha, ''], [0.85, 0.15])[0]
        lista.append(m)

        # Nacionalidad
        n = equipos[2].loc[_]
        m = random.choices([n, ''], [0.6, 0.4])[0]
        lista.append(m)

        df.loc[_] = lista

    df.set_index('id_equipo', inplace = True)
    df.to_csv('equipos.csv', sep = ',')
    print(df)

        




if __name__ == "__main__":
    # equipos()
    # marcas()
    ciclistas()
    a = pd.read_csv('ciclistas.csv')
    print(len(a['usuario_zwift'].unique()))
    print(len(a))
