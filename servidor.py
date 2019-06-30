#!/usr/bin/python

import socket

# Configuracoes do servidor
host = '' 
port = 7000 
addr = (host, port) 
serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
serv_socket.bind(addr) 
serv_socket.listen(10)

# Conexao Jogador 1
print 'aguardando conexao do jogador BLUE' 
con1, jogador1 = serv_socket.accept()
con1.send('B')
print 'conectado jogador BLUE com sucesso'

# Conexao Jogador 2
print 'aguardando conexao do jogador RED' 
con2, jogador2 = serv_socket.accept()
con2.send('R')
print 'conectado jogador RED com sucesso'

# Total de celulas no tabuleiro
tam = 64

# Flag de fim de jogo
fim = 0

# Proximo a jogar
proxJog = 1

# Enquanto jogo nao acaba
while fim == 0:

    # Muda flag
    fim = 1

    # Se o BLUE estiver jogando
    if proxJog == 1:
        print 'aguardando turno do jogador BLUE'
        # Recebe turno do BLUE
        turno = con1.recv(1024)
        # Armazena estado atual do tabuleiro
        tabuleiro = turno[:tam]        

        # Verifica se ainda ha pecas do RED
        for i in range(tam):
            if tabuleiro[i] == '2' or tabuleiro[i] == '4':
                fim = 0
                break
        
        # Se o jogo nao acabou, passa a vez para o RED
        if fim == 0:
            print 'vez do RED'
            con1.send('continua')
            con2.send(tabuleiro)
            proxJog = 2
        # Se o jogo acabou, informa vitoria ao BLUE e derrota ao RED
        else:
            print 'fim de jogo'
            con1.send('vitoria')
            con2.send(tabuleiro)

    # Se o RED estiver jogando              
    else:
        print 'aguardando turno do jogador RED'
        # Recebe turno do RED
        turno = con2.recv(1024)
        # Armazena estado atual do tabuleiro
        tabuleiro = turno[:tam]        

        # Verifica se ainda ha pecas do BLUE
        for i in range(tam):
            if tabuleiro[i] == '1' or tabuleiro[i] == '3':
                fim = 0
                break

        # Se o jogo nao acabou, passa a vez para o BLUE  
        if fim == 0:
            print 'vez do BLUE'
            con2.send('continua')
            con1.send(tabuleiro)
            proxJog = 1
        # Se o jogo acabou, informa vitoria ao RED e derrota ao BLUE
        else:
            print 'fim de jogo'     
            con2.send('vitoria')
            con1.send(tabuleiro)

# Fecha conexao       
serv_socket.close()