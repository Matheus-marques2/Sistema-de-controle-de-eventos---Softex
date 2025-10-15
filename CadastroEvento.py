from datetime import datetime

class Evento:
    def __init__(self, nome, data, local, capacidade_max, categoria, preco):
        self.nome = nome
        self.data = self.validar_data(data)
        self.local = local
        self.capacidade_max = self.validar_capacidade(capacidade_max)
        self.categoria = categoria
        self.preco = float(preco)
        self.inscritos = []  # participantes vão ser guardados aqui depois

    def validar_data(self, data_str):
        # Confere se a data informada não é antes de hoje
        try:
            data_evento = datetime.strptime(data_str, "%d/%m/%Y")
            hoje = datetime.now()
            if data_evento.date() < hoje.date():
                raise ValueError("A data do evento não pode ser anterior à data atual.")
            return data_evento
        except ValueError as e:
            print(f"Erro: {e}")
            return None

    def validar_capacidade(self, capacidade):
        # Garante que o número seja positivo
        try:
            capacidade = int(capacidade)
            if capacidade <= 0:
                raise ValueError("A capacidade máxima deve ser um número positivo.")
            return capacidade
        except ValueError as e:
            print(f"Erro: {e}")
            return None

    def __str__(self):
        return (f"Evento: {self.nome}\n"
                f"Data: {self.data.strftime('%d/%m/%Y')}\n"
                f"Local: {self.local}\n"
                f"Categoria: {self.categoria}\n"
                f"Capacidade: {self.capacidade_max}\n"
                f"Preço: R$ {self.preco:.2f}\n"
                f"Inscritos: {len(self.inscritos)}")


# Lista geral de eventos
eventos = []

def cadastrar_evento():
    print("=== Cadastro de Evento ===")
    nome = input("Nome do evento: ")
    data = input("Data do evento (dd/mm/aaaa): ")
    local = input("Local do evento: ")
    capacidade = input("Capacidade máxima: ")
    categoria = input("Categoria (ex: Tech, Marketing...): ")
    preco = input("Preço do ingresso: ")

    evento = Evento(nome, data, local, capacidade, categoria, preco)
    if evento.data and evento.capacidade_max:
        eventos.append(evento)
        print("Evento cadastrado com sucesso!")
    else:
        print("Erro ao cadastrar. Verifique os dados.")
def listar_eventos():
    print("\n=== Lista de Eventos ===")
    if not eventos:
        print("Nenhum evento cadastrado.")
    for i, evento in enumerate(eventos, start=1):
        print(f"\n{i}. {evento}")
# Deixei o menu simples para testar as funcionalidades voces podem melhorar depois
if __name__ == "__main__":
    while True:
        print("\n=== Sistema de Eventos ===")
        print("1 - Cadastrar novo evento")
        print("2 - Listar eventos")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_evento()
        elif opcao == "2":
            listar_eventos()
        elif opcao == "0":
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")

