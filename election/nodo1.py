import socket
import sys
import time

# Configurações do servidor
HOST = ''  # Todas as interfaces de rede
PORT = 5000  # Número da porta para conexão

def send_message(conn, message):
    """Função para enviar uma mensagem ao outro nodo"""
    message = message.encode('utf-8')
    conn.sendall(message)

def receive_message(conn):
    """Função para receber uma mensagem do outro nodo"""
    message = b''
    while True:
        data = conn.recv(1024)
        if not data:
            break
        message += data
    return message.decode('utf-8')

def main():
    """Função principal do servidor"""
    # Cria um socket TCP/IP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Associa o socket a uma porta
        s.bind((HOST, PORT))
        # Coloca o socket em modo de escuta por conexões
        s.listen()

        # Lista de conexões com outros nodos
        connections = []

        # Adiciona a conexão do servidor na lista de conexões
        connections.append(s)

        # ID do nodo atual (servidor)
        node_id = 1

        print('Nodo {} iniciado como líder'.format(node_id))

        # Loop principal do servidor
        while True:
            # Aceita novas conexões
            conn, addr = s.accept()
            print('Conexão estabelecida com ', addr)

            # Adiciona a nova conexão na lista de conexões
            connections.append(conn)

            # Recebe uma mensagem do outro nodo
            message = receive_message(conn)

            # Processa a mensagem recebida
            if message == 'ELECTION':
                send_message(conn, 'ID {}'.format(node_id))
            elif message.startswith('LEADER'):
                new_leader = int(message.split(' ')[1])
                if new_leader != node_id:
                    print('Líder atualizado para', new_leader)
                else:
                    print('Líder mantido')

            # Se o servidor foi desconectado, inicia uma eleição
            if not conn:
                connections.remove(conn)
                send_message(election_controller_conn, 'ELECTION')
                break

if __name__ == '__main__':
    main()
