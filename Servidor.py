# Numero de dias vividos 8023
from random import randint
from time import time
import socket
import threading
import sys

"""def practica(i):
    switcher={
        0: 'Buscaminas\n',
        1: 'Gato Dummy\n',
        2: 'Memoria\n'
    }
    return switcher.get(i,"no hay ejercicio asignado\n")
dias=8023 #dias vividos
print ("Toca realizar el ejercicio ",dias%3,": ", practica(dias%3))  """


# REALIZAR GATO DUMMY
#CREANDO MATRIZ

def matrizP(): #Tablero Principiante
    filas=["1","2","3"];
    columnas=["A","B","C"];
    alto = len(filas) + 1
    largo=len(columnas)+1;
    matriz=[]
    for i in range(alto):  # ALTO
        matriz.append([])
        for j in range(largo):  # LARGO
            matriz[i].append(" ")
    return generarMatrizInicial(matriz,filas,columnas)
def matrizA(): #Tablero avanzado
    filas=["1","2","3","4","5"];
    columnas=["A","B","C","D","E"];
    alto = len(filas) + 1
    largo=len(columnas)+1;
    matriz=[]
    for i in range(alto):  # ALTO
        matriz.append([])
        for j in range(largo):  # LARGO
            matriz[i].append(" ")
    return generarMatrizInicial(matriz,filas,columnas)
def generarMatrizInicial(matriz,filas,columnas):
    #print("alto=", len(matriz))
    #print("largo=", len(matriz[0]))
    for i in range(len(matriz)):  # ALTO
        for j in range(len(matriz[0])):  # LARGO
            if i is 0:
                if j is 0:
                    matriz[i][j]=" "
                else:
                    matriz[i][j] = columnas[j-1]
            else:
                if j is 0:
                    matriz[i][j]=filas[i-1]
                else:
                    matriz[i][j]="-"
    return matriz
def ganarH(matriz,sim):
    cont=0
    for i in range (1,len(matriz)):
        cont=0
        for j in range(1,len(matriz[0])):
            if matriz[i][j]==sim:
                cont+=1
                if cont is (len(matriz)-1):
                    return 1
                    break;
def ganarV(matriz,sim):
    cont=0
    for j in range (1,len(matriz[0])):
        cont=0
        for i in range(1,len(matriz)):
            if matriz[i][j]==sim:
                cont+=1
                if cont is (len(matriz)-1):
                    return 1
                    break;
def verMatriz(matriz):
    alto = len(matriz)
    largo = len(matriz[0])
    for i in range(alto):
        for j in range(largo):  # LARGO
            print(matriz[i][j], "\t", end=" ")
        print()
def menu(case,Client_conn):
        """print("\tElige una dificultad\t")
        print("1. Principiante")
        print("2. Avanzado")"""
        if case == 1:
            matrizp=matrizP()
            verMatriz(matrizp)
            jugar(matrizp,Client_conn)
            return False
        if case == 2:
            matriza=matrizA()
            verMatriz(matriza)
            jugar(matriza,Client_conn)
            return False


def colocar(matriz,sim,Client_conn):
    pos=str(Client_conn.recv(buffer_size),"ascii")
    print(pos)
    fila = int(pos[0])
    col = ord(pos[1]) - 64
    matriz[int(fila)][int(col)]=sim
def juegoAuto(matriz,sim,Client_conn):
    cont=0
    while cont==0:
        fila = randint(1,len(matriz)-1)
        col = randint(65,65+(len(matriz)-2))-64#COdigo ascii desde A hasta el tamaño de la matriz

        for i in range (len(matriz)):
            if i==fila:
                for j in range (len(matriz[0])):
                    if j==col:
                        if matriz[i][j]=="-":
                            msg="Elegi Casilla: "+str(fila)+(chr(col+64))
                            matriz[i][j]=sim
                            cont+=1
                            verMatriz(matriz)
                        #else:
                            #print("Casilla Ocupada")

                    elif col<=0 or col>=len(matriz[0]):
                        #print("Columna Invalida")
                        break;
            elif fila <= 0 or fila >= len(matriz):
                #print("Fila Invalida")
                break;
    pos=str(fila)+(chr(col+64))
    Client_conn.sendall(pos.encode())
    Client_conn.sendall(msg.encode())

def jugar(matriz,Client_conn):
    simJ="x"
    simS="o"
    cont=0
    print("Jugador es: ", simJ)
    print("Maquina es: ", simS)
    long=(len(matriz)-1)*(len(matriz)-1)
    inicio=time()
    while cont<long:
        print("TURNO JUGADOR\n")
        colocar(matriz,simJ,Client_conn)
        verMatriz(matriz)
        if ganarH(matriz,simJ) is 1:
            print("Gano JUGADOR")
            break;
        if ganarV(matriz, simJ) is 1:
            print("Gano JUGADOR")
            break;
        cont+=1;
        if cont>=long:
            print("Juego Terminado: EMPATE")
            break
        print("TURNO MAQUINA\n")
        juegoAuto(matriz,simS, Client_conn)
        if ganarH(matriz,simS) is 1:
            print("Gano MAQUINA")
            break;
        if ganarV(matriz, simS) is 1:
            print("Gano MAQUINA")
            break;
        cont+=1
        if cont>=long:
            print("Juego Terminado: EMPATE")
            break
    final=time()
    print("Duracion de la partida %.2f segundos" %(final-inicio))

def Iniciar(Client_conn,Client_addr):
    with Client_conn:
        hilo = threading.current_thread()
        print("ID Hilo: ",hilo.ident)
        #print("Conectado a", Client_addr)
        while True:
            case = int.from_bytes(Client_conn.recv(buffer_size), 'little')
            j=menu(case,Client_conn)

            if j is False:
                Client_conn.sendall(b"Juego Terminado.Adios")
                break
def servirPorSiempre(TCPServerSocket, listaconexiones):
    try:
        while True:
            Client_conn, Client_addr = TCPServerSocket.accept()
            #print("Conectado a", Client_addr)
            listaconexiones.append(Client_conn)
            if len(listaconexiones)<numConn:
                Client_conn.sendall(b"Esperando la conexion de los jugadores faltantes ("+len(listaConexiones)+")")
            else:
                Client_conn.sendall(b"Eres el jugador que faltaba")
                for i in range (len(listaConexiones)):
                    listaConexiones[i].sendall(b"Todos los jugadores ("+numConn+") se han conectado")
            if len(listaConexiones)==numConn:
                print("Esperando inicio de juego")
                for i in range(len(listaConexiones)):
                    cliente=i.to_bytes(1, 'little')
                    listaConexiones[i].sendall(cliente) #Envia el numero de cliente a cada uno de ellos
                #Solo el jugador 0, el primero en conectarse, puede escoger la dificultad
                case = int.from_bytes(listaConexiones[0].recv(buffer_size), 'little')
                print("Recibido modo de juego: ", case)
                caseb = case.to_bytes(1, 'little')
                for i in range(1,len(listaConexiones)):
                    listaConexiones[i].sendall(caseb)
                #IniciarHilos(listaConexiones,case)
    except Exception as e:
        print(e)

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
buffer_size = 1024
listaConexiones = []
numConn=int(input("Ingrese Número de conexiones a aceptar: "))
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPServerSocket.bind((HOST, PORT))
    TCPServerSocket.listen(int(numConn))
    print("El servidor TCP está disponible y en espera de solicitudes")
    servirPorSiempre(TCPServerSocket, listaConexiones)