# Numero de dias vividos 8023
from random import randint
from time import time
import socket,threading,logging
from threading import Lock
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

logging.basicConfig(level=logging.DEBUG,
                    format='%(message)s (%(threadName)-0s)',)

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
def ganarD(matriz,sim):
    cont=0
    i=1
    j=1
    while i<len(matriz[0]):
        if matriz[i][j] == sim:
            cont += 1
        i+=1
        j+=1
        if cont is (len(matriz) - 1):
            return 1
            break
    if cont<(len(matriz) - 1) :
        cont=0
        i=len(matriz)-1
        j=1
        while i>0 and j<len(matriz[0]):
            if matriz[i][j]==sim:
                cont+=1
            i-=1
            j+=1
            if cont is (len(matriz)-1):
                return 1
                break
def verMatriz(matriz):
    alto = len(matriz)
    largo = len(matriz[0])
    for i in range(alto):
        for j in range(largo):  # LARGO
            print(matriz[i][j], "\t", end=" ")
        print()
def colocar(matriz,sim,Client_conn):
    pos=str(Client_conn.recv(buffer_size),"ascii")
    print(pos)
    fila = int(pos[0])
    col = ord(pos[1]) - 64
    matriz[int(fila)][int(col)]=sim
    return pos #Retorna posicion que escogio el jugador en turno para actualizar el tablero en todos los jugadores
def juegoAuto(matriz,sim,listaConexiones,listaHilos):
    cont=0
    while cont==0:
        fila = randint(1,len(matriz)-1)
        col = randint(65,65+(len(matriz)-2))-64 #Codigo ascii desde A hasta el tamaño de la matriz

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
    for j in range(len(listaHilos)):
        print("Actualizando tablero de", listaHilos[j].getName())
        listaConexiones[j].sendall(pos.encode())
        listaConexiones[j].sendall(msg.encode())
        continue
def actTablero(pos, listaConexiones,listaHilos,i):
    for j in range(len(listaHilos)):
        if (i != j): #Evitar que se envíe la posicion al jugador que hizo la jugada
            print("Actualizando tablero de", listaHilos[j].getName())
            listaConexiones[j].sendall(pos.encode())
            continue
def jugar(matriz,listaConexiones,listaHilos):
    simJ="x"
    simS="o"
    termina=False
    cont=0
    print("Jugador es: ", simJ)
    print("Maquina es: ", simS)
    long=(len(matriz)-1)*(len(matriz)-1)
    inicio=time()
    while cont<long:
        for i in range(len(listaConexiones)):
            with Lock(): #Bloquear opciones de tiro mientras esta el jugador correspondiente en turno
                print("TURNO JUGADOR "+listaHilos[i].getName()+"\n")
                pos=colocar(matriz,simJ,listaConexiones[i])
                actTablero(pos, listaConexiones, listaHilos, i)
                verMatriz(matriz)
                if ganarH(matriz,simJ) is 1:
                    print("Gano JUGADOR "+listaHilos[i].getName()+"\n")
                    termina=True
                    break
                if ganarV(matriz, simJ) is 1:
                    print("Gano JUGADOR "+listaHilos[i].getName()+"\n")
                    termina = True
                    break
                if ganarD(matriz, simJ) is 1:
                    print("Gano JUGADOR "+listaHilos[i].getName()+"\n")
                    termina = True
                    break
                cont+=1
                if cont>=long:
                    print("Juego Terminado: EMPATE")
                    termina = True
                    break
            if termina:
                break
        if termina:
            break
        print("TURNO MAQUINA\n")
        juegoAuto(matriz,simS, listaConexiones,listaHilos) #Turno donde la maquina genera su jugada y se actualiza el tablero
        if ganarH(matriz,simS) is 1:
            print("Gano MAQUINA")
            break
        if ganarV(matriz, simS) is 1:
            print("Gano MAQUINA")
            break
        if ganarD(matriz, simS) is 1:
            print("Gano MAQUINA")
            break
        cont+=1
        if cont>=long:
            print("Juego Terminado: EMPATE")
            break
    final=time()
    print("Duracion de la partida %.2f segundos" %(final-inicio))

def gestionHilos():
    logging.debug('Jugador: ')
def IniciarHilos(listaConexiones,case):
    if case==1:
        matriz=matrizP()
        #print("se creo matriz P")
    if case==2:
        matriz=matrizA()
        #print("se creo matriz A")
    for i in range (len(listaConexiones)):
        listaHilos.append(threading.Thread(target=gestionHilos,name="J"+str(i)))
        listaHilos[i].start()
    jugar(matriz,listaConexiones,listaHilos)
def servirPorSiempre(TCPServerSocket, listaConexiones):
    try:
        while True:
            Client_conn, Client_addr = TCPServerSocket.accept()
            listaConexiones.append(Client_conn)
            if len(listaConexiones)<numConn:
                msg="Esperando la conexion de los jugadores faltantes ("+str(numConn-len(listaConexiones))+")"
                Client_conn.sendall(msg.encode())
                print("Faltan "+str(numConn-len(listaConexiones))+" conexion(es)")
            else:
                Client_conn.sendall(b"Eres el jugador que faltaba")
                jugadores=bytes([len(listaConexiones)])
                for i in range (0,len(listaConexiones)):
                    listaConexiones[i].sendall(jugadores)
            if len(listaConexiones)==numConn:
                print("Esperando inicio de juego")
                for j in range(0,len(listaConexiones)):
                    cliente=j.to_bytes(1, 'little')
                    listaConexiones[j].sendall(cliente) #Envia el numero de cliente a cada uno de ellos
                #Solo el jugador 0, el primero en conectarse, puede escoger la dificultad
                case = int.from_bytes(listaConexiones[0].recv(buffer_size), 'little')
                print("Recibido modo de juego: ", case)
                caseb = case.to_bytes(1, 'little')
                for z in range(0,len(listaConexiones)):
                    listaConexiones[z].sendall(caseb) #Envia a todos los clientes el nivel elegido
                IniciarHilos(listaConexiones,case)
    except Exception as e:
        print(e)

HOST = "192.168.1.105"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
buffer_size = 1024
listaConexiones = []
listaHilos=[]

numConn=int(input("Ingrese Número de conexiones a aceptar: "))
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPServerSocket.bind((HOST, PORT))
    TCPServerSocket.listen(int(numConn))
    print("El servidor TCP está disponible y en espera de solicitudes")
    servirPorSiempre(TCPServerSocket, listaConexiones)
