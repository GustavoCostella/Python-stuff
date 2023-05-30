class Message:
    def __init__(self, op, id, tr):
        self.op = op
        self.id = id
        self.tr = tr


class Process:
    def __init__(self, id):
        self.id = id
        self.tr = 1
        self.queue = []
        self.received_acks = set()
        self.saldo = 1000.00

    def receive_message(self, msg):
        self.queue.append(msg)

    def send_message(self, msg):
        for p in processes:
            if p.id != self.id:
                p.receive_message(msg)

    def send_ack(self, msg):
        if msg.id <= self.id:
            receiver_id = 1 if self.id == 2 else 2
            receiver = processes[receiver_id - 1]
            receiver.receive_ack(msg)

    def receive_ack(self, msg):
        self.received_acks.add((msg.op, msg.id))

    def process_messages(self):
        for msg in self.queue:
            if all((msg.op, msg.id) in self.received_acks for msg in self.queue):
                if msg.op == "dep100":
                    self.saldo += 100.00
                elif msg.op == "jur1%":
                    self.saldo *= 1.01

        self.queue = []

    def show_balance(self):
        print(f"Saldo em P{self.id}: R${self.saldo:.2f}")


processes = [Process(1), Process(2)]

# Multicast ordenado
for p in processes:
    p.tr += 1
    msg_dep100 = Message("dep100", 1, p.tr)
    msg_jur1 = Message("jur1%", 2, p.tr)
    for p2 in processes:
        p2.receive_message(msg_dep100)
        p2.receive_message(msg_jur1)

# Envio dos acks
for p in processes:
    for msg in p.queue:
        p.send_ack(msg)

# Processamento das mensagens confirmadas
for p in processes:
    p.process_messages()

# Envio do último ack por P1
p1 = processes[0]
ack_msg_jur1 = Message("jur1%", 2, p1.tr)
for p in processes:
    if p.id != p1.id:
        p.receive_ack(ack_msg_jur1)

# Processamento das mensagens confirmadas por P1
p1.process_messages()

# Mostrar saldo
for p in processes:
    p.show_balance()
