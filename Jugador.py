from time import time
import socket
import sys

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
def verMatriz(matriz):
    alto = len(matriz)
    largo = len(matriz[0])
    for i in range(alto):
        for j in range(largo):  # LARGO
            print(matriz[i][j], "\t", end=" ")
        print()
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
def verMenu(TCPClientSocket):
        print("\tElige una dificultad\t")
        print("1. Principiante")
        print("2. Avanzado")
        case=int(input("Opcion: "))
        caseb = case.to_bytes(1, 'little')
        TCPClientSocket.sendall(caseb)
def menu(case,Jugadores,Cliente,TCPClientSocket):
    if case == 1:
        print("Nivel Principiante")
        matrizp = matrizP()
        verMatriz(matrizp)
        jugar(matrizp, TCPClientSocket,Jugadores,Cliente)
    if case == 2:
        print("Nivel Avanzado")
        matriza = matrizA()
        verMatriz(matriza)
        jugar(matriza, TCPClientSocket,Jugadores,Cliente)
def colocar(matriz,sim,TCPClientSocket):
    cont=0
    while cont==0:
        pos=str(input("Ingrese una coordenada (Ej. 1A,2C): "))
        fila = int(pos[0])
        col = ord(pos[1]) - 64
        #print(fila, ",", col)
        for i in range (len(matriz)):
            if i==fila:
                for j in range (len(matriz[0])):
                    if j==col:
                        if matriz[i][j]=="-":
                            matriz[i][j]=sim
                            cont+=1
                            verMatriz(matriz)
                        else:
                            print("Casilla Ocupada")

                    elif col<=0 or col>=len(matriz[0]):
                        print("Columna Invalida")
                        break;
            elif fila <= 0 or fila >= len(matriz):
                print("Fila Invalida")
                break
    TCPClientSocket.sendall(pos.encode())
def juegoAuto(matriz,sim,TCPClientSocket): #Juego de la maquina
    pos=str(TCPClientSocket.recv(int(buffer_size/2)),"ascii")
    fila = int (pos[0])
    col = ord(pos[1]) - 64
    matriz[int(fila)][int(col)] = sim
    #print(str(TCPClientSocket.recv(buffer_size),"ascii"))
def actTablero(matriz,sim,pos): #Recibe las jugadas de los otros jugadores
    fila = int(pos[0])
    col = ord(pos[1]) - 64
    matriz[int(fila)][int(col)] = sim
    #print(str(TCPClientSocket.recv(buffer_size), "ascii"))
def jugar(matriz, TCPClientSocket,Jugadores,Cliente):
    simJ="x"
    simS="o"
    cont=0
    print("Jugador es: ", simJ)
    print("Maquina es: ", simS)
    long=(len(matriz)-1)*(len(matriz)-1)
    termina=False
    inicio=time()
    while cont<long:
        for i in range (Jugadores):
            if i!=Cliente:
                print("TURNO JUGADOR " + str(i) + "\n")
                pos = str(TCPClientSocket.recv(buffer_size), "ascii")
                actTablero(matriz,simJ,pos)
                verMatriz(matriz)
                if ganarH(matriz, simJ) is 1:
                    print("Gano JUGADOR " + str(i) + "\n")
                    termina=True
                    break
                if ganarV(matriz, simJ) is 1:
                    print("Gano JUGADOR " + str(i) + "\n")
                    termina = True
                    break
                if ganarD(matriz, simJ) is 1:
                    print("Gano JUGADOR " + str(i) + "\n")
                    termina = True
                    break
                cont += 1
                if cont >= long:
                    print("Juego Terminado: EMPATE")
                    termina = True
                    break
            else:
                print("TU TURNO JUGADOR " + str(i) + "\n")
                colocar(matriz, simJ, TCPClientSocket)
                if ganarH(matriz, simJ) is 1:
                    print("Ganaste JUGADOR " + str(i) + "\n")
                    termina = True
                    break
                if ganarV(matriz, simJ) is 1:
                    print("Ganaste JUGADOR " + str(i) + "\n")
                    termina = True
                    break
                if ganarD(matriz, simJ) is 1:
                    print("Ganaste JUGADOR " + str(i) + "\n")
                    termina = True
                    break
                cont += 1
                if cont >= long:
                    print("Juego Terminado: EMPATE")
                    termina = True
                    break
            if termina:
                break
        if termina:
            break
        print("TURNO MAQUINA\n")
        juegoAuto(matriz,simS,TCPClientSocket)
        verMatriz(matriz)
        if ganarH(matriz,simS) is 1:
            print("Gano MAQUINA")
            break;
        if ganarV(matriz, simS) is 1:
            print("Gano MAQUINA")
            break;
        if ganarD(matriz, simS) is 1:
            print("Gano MAQUINA")
            break;
        cont+=1
        if cont>=long:
            print("Juego Terminado: EMPATE")
            break
    final=time()
    print("Duracion de la partida %.2f segundos" %(final-inicio))


HOST = str(input("Ingrese IP del servidor: "))  # The server's hostname or IP address
PORT = int(input("Ingrese Puerto del servidor: "))  # The port used by the server
#HOST = "192.168.1.64" # Standard loopback interface address (localhost)
#PORT = 56432  # Port to listen on (non-privileged ports are > 1023)
buffer_size = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, PORT))

    Jugadores = int.from_bytes(TCPClientSocket.recv(int(buffer_size)), byteorder='little')  # Tener presente cuantos jugadores hay
    cliente = int.from_bytes(TCPClientSocket.recv(int(buffer_size/2)), 'little')  # Veririficar que jugador soy
    print("Jugador: ",cliente)
    if Jugadores==0:
        print("Eres el jugador que faltaba")#mensaje de ultimo jugador que faltaba
        Jugadores = cliente
    else:
        print("Esperando la conexion de los jugadores faltantes (%d)" % Jugadores)  # Mensaje de espera de otros jugadores
        Jugadores+=cliente
    Jugadores+=1
    print(Jugadores)
    TCPClientSocket.recv(int(buffer_size/2))
    print("Todos los jugadores (%d) estan conectados"%Jugadores)
    if(cliente==0):
        verMenu(TCPClientSocket) #Menu para elegir dificultad
    else:
        print("Esperando tablero de juego")
    case = int.from_bytes(TCPClientSocket.recv(buffer_size), 'little')#Dificultad elegida por jugador 1
    menu(case,Jugadores,cliente,TCPClientSocket)# Se genera el tablero con la dificultad elegida
