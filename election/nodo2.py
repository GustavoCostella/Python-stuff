import socket
import time

# Configurações do cliente
HOST = 'localhost'  # Endereço IP do servidor
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
    """Função principal do cliente"""
    # Cria um socket TCP/IP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Tenta se conectar ao servidor
        while True:
            try:
                s.connect((HOST, PORT))
                break
            except ConnectionRefusedError:
                pass

        # ID do nodo atual
        node_id = 2

        # Envia uma mensagem ao servidor para indicar que está conectado
        send_message(s, 'CONNECTED')

        # Loop principal do cliente
        while True:
            # Recebe uma mensagem do servidor
            message = receive_message(s)

            # Processa a mensagem recebida
            if message.startswith('ID'):
                sender_id = int(message.split(' ')[1])
                if sender_id > node_id:
                    # Se o ID do outro nodo for maior, inicia uma nova eleição
                    send_message(s, 'ELECTION')
                elif sender_id < node_id:
                    # Se o ID do outro nodo for menor, atualiza o líder
                    send_message(s, 'LEADER {}'.format(node_id))
                else:
                    # Se os IDs forem iguais, mantém o líder
                    send_message(s, 'LEADER {}'.format(sender_id))

            # Se o servidor foi desconectado, sai do loop principal
            if not message:
                break

if __name__ == '__main__':
    main()
