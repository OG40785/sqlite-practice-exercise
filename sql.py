import sqlite3
from Mensajes import *

class sql:
    

    def __init__(self,bd):
        self.DNI = sqlite3.connect(bd)
        self.mensaje = Mensajes()

    def crear_tabla_origen(self,lista_dni): 

   # Esta función crea la tabla de origen y la imprime a través de otra función 
   # :param lista_dni: es una lista de tuplas con dni 
   # :return: no hace falta
        cursor=self.DNI.cursor()
        self.crear_tabla("DNIs_origen_OG")
        cursor.executemany("INSERT INTO DNIs_origen_OG VALUES (?,?)",lista_dni)
        self.mensaje.ok()
        self.DNI.commit()
        self.imprimir_tabla("DNIs_origen_OG")
        cursor.close()

    def imprimir_tabla(self,nombre):
   # Esta función imprime cualquier tabla   
   # :param nombre str:  nombre de la tabla 
   # :return: no hace falta
        cursor=self.DNI.cursor()
        self.mensaje.texto("TABLA "+nombre)
        for row in cursor.execute("SELECT * FROM "+nombre):
            self.mensaje.texto(row[0]+"-"+row[1])
        cursor.close()

    def imprimir_tabla_ordenada(self,nombre):
       # Esta función imprime cualquier tabla ORDENADA por el numero
   # :param nombre str: nombre de la tabla 
   # :return: no hace falta
        cursor=self.DNI.cursor()
        self.mensaje.texto("TABLA "+nombre)
        for row in cursor.execute("SELECT * FROM "+nombre+" order by Numero"):
            self.mensaje.texto(row[0]+"-"+row[1])
        cursor.close()

    def duplicar_tabla(self):
       # Esta función hace la copia de la tabla dni origen 
   # :param : sin parametro 
   # :return: no hace falta
        cursor=self.DNI.cursor()
        cursor.execute ("CREATE TABLE DNIs_origen2_OG as SELECT * FROM DNIs_origen_OG")
        #self.imprimir_tabla("DNIs_origen2_OG")
        cursor.close()

    def crear_tabla(self,nombre):
       # Esta función crea la tabla de dos columnas-numero str y letra str   
   # :param nombre str:  nombre de la tabla 
   # :return: no hace falta
        cursor=self.DNI.cursor()
        cursor.execute("CREATE TABLE "+ nombre +" (Numero VARCHAR, Letra VARCHAR)")
        #cursor.execute ("CREATE TABLE DNIs_origen2 as SELECT * FROM DNIs_origen")
        #cursor.execute("CREATE TABLE DNIs_correctos (Numero VARCHAR, Letra VARCHAR)")
        #cursor.execute("CREATE TABLE DNIs_corregidos (Numero VARCHAR, Letra VARCHAR)")
        cursor.close()

    def letra_dni(self, numero):
       # Esta función busca la letra de dni correcta  
   # :param numero str: es el numero de dni
   # :return: letra de dni
        letras = "TRWAGMYFPDXBNJZSQVHLCKE"
        letrapos= int(numero) % 23
        letra = str(letras[letrapos])
        return letra   

    def comprobar_tabla_origen(self):
           # Esta función comprueba los dnis de la tabla origen , si un dni es correcto -lo añade a la tabla correctos , si no - a la tabla corregidos 
   # :param : sin parametro
   # :return: no hace falta
        cursor=self.DNI.cursor()
        self.crear_tabla("DNIs_correctos_OG")
        self.crear_tabla("DNIs_corregidos_OG")
        cursor.execute("SELECT * FROM DNIs_origen_OG")
        rows=cursor.fetchall()
        for row in rows:
            if self.letra_dni(row[0])==row[1]:
                self.DNI.execute("INSERT INTO DNIs_correctos_OG VALUES (?, ?)",row)
            else:
                self.DNI.execute("INSERT INTO DNIs_corregidos_OG VALUES ('" + row[0] + "','" + self.letra_dni(row[0])+"')")
        self.DNI.commit()
        cursor.close()
        self.imprimir_tabla("DNIs_correctos_OG")
        self.imprimir_tabla("DNIs_corregidos_OG")

    def crear_tabla_ordenada(self):

           # Esta función crea la tabla de dni ordenados yimprime los datos de manera ordenada  
   # :param : sin parametro
   # :return: no hace falta
        cursor=self.DNI.cursor()
        self.crear_tabla("DNIs_ordenados_OG")
        cursor.execute("SELECT * FROM DNIs_correctos_OG order by Numero")
        datos = cursor.fetchall()
        cursor.execute("SELECT * FROM DNIs_corregidos_OG order by Numero")
        datos += cursor.fetchall()
        cursor.executemany("INSERT INTO DNIs_ordenados_OG VALUES (?,?)",datos)
        self.imprimir_tabla_ordenada("DNIs_ordenados_OG")

    def corregir_tabla2(self):
# Esta función corrige la tabla de dni origen 2 yimprime los datos de manera ordenada  
   # :param : sin parametro
   # :return: no hace falta
        cursor=self.DNI.cursor()
        cursor.execute("SELECT * FROM DNIs_origen2_OG")
        rows=cursor.fetchall()
        for row in rows:
            if self.letra_dni(row[0]) !=row[1]:
                cursor.execute('UPDATE DNIs_origen2_OG SET letra = "' + self.letra_dni(row[0]) + '" where numero = "'+row[0]+'"')
        self.imprimir_tabla_ordenada("DNIs_origen2_OG")

    def limpiar(self):
    # Esta función borra todas las tablas  
   # :param : sin parametro
   # :return: no hace falta
        self.DNI.execute("Drop table DNIs_origen_OG")
        self.DNI.execute("Drop table DNIs_origen2_OG")
        self.DNI.execute("Drop table DNIs_ordenados_OG")
        self.DNI.execute("Drop table DNIs_corregidos_OG")
        self.DNI.execute("Drop table DNIs_correctos_OG")









