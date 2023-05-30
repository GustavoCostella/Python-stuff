import socket
import time

# Configurações do controlador da eleição
HOST = ''  # Todas as interfaces de rede
PORT = 5001  # Número da porta para conexão

def send_message(conn, message):
    """Função para enviar uma mensagem a um nodo"""
    message = message.encode('utf-8')
    conn.sendall(message)

def receive_message(conn):
    """Função para receber uma mensagem de um nodo"""
    message = b''
    while True:
        data = conn.recv(1024)
        if not data:
            break
        message += data
    return message.decode('utf-8')

def main():
    """Função principal do controlador da eleição"""
    # Cria um socket TCP/IP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Associa o socket a uma porta
        s.bind((HOST, PORT))
        # Coloca o socket em modo de escuta por conexões
        s.listen()

        # Lista de conexões com os nodos
        connections = []

        # Adiciona a conexão do controlador na lista de conexões
        connections.append(s)

        # ID do nodo líder
        leader_id = 1

        # Loop principal do controlador
        while True:
            # Aceita novas conexões
            conn, addr = s.accept()
            print('Conexão estabelecida com ', addr)

            # Adiciona a nova conexão na lista de conexões
            connections.append(conn)

            # Recebe uma mensagem do nodo conectado
            message = receive_message(conn)

            # Se o nodo estiver conectando, não faz nada
            if message == 'CONNECTED':
                pass
            # Se o nodo iniciou uma eleição, inicia uma nova eleição
            elif message == 'ELECTION':
                leader_id = None
                for conn in connections:
                    if conn != s:
                        send_message(conn, 'ID {}'.format(leader_id or -1))
                        response = receive_message(conn)
                        if response.startswith('ID'):
                            sender_id = int(response.split(' ')[1])
                            if sender_id > leader_id:
                                leader_id = sender_id
                if leader_id is None:
                    leader_id = 1
                print('Novo líder:', leader_id)
                for conn in connections:
                    if conn != s:
                        send_message(conn, 'LEADER {}'.format(leader_id))

            # Fecha a conexão com o nodo desconectado
            connections.remove(conn)
            conn.close()

if __name__ == '__main__':
    main()
