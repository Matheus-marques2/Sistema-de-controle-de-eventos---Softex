from datetime import datetime
import json
import os

class Participante:
    def __init__(self, nome, email):
        self.__nome = nome
        self.__email = email
        self.presente = False

    @property
    def nome(self):
        return self.__nome

    @property
    def email(self):
        return self.__email
    
    def to_dict(self): #transforma um objeto participante em um dicionário fazendo com que possa ser lido por um arquivo json
            return {
            "nome": self.__nome,
            "email": self.__email,
            "presente": self.presente
        }

    @staticmethod
    def from_dict(data):
        p = Participante(data["nome"], data["email"])
        p.presente = data.get("presente", False)
        return p


class Evento:
    def __init__(self, nome, data, local, capacidade_max, categoria, preco):
        self.__nome = nome
        self.__data = datetime.strptime(data, "%d/%m/%Y")
        self.__local = local
        self.__capacidade_max = capacidade_max
        self.__categoria = categoria
        self.__preco = preco
        self.__participantes = []
        self.validar_evento()

    @property
    def nome(self):
        return self.__nome

    @property
    def data(self):
        return self.__data

    @property
    def local(self):
        return self.__local

    @property
    def categoria(self):
        return self.__categoria

    @property
    def preco(self):
        return self.__preco

    @property
    def capacidade_max(self):
        return self.__capacidade_max

    @property
    def participantes(self):
        return self.__participantes

    def validar_evento(self):
        if self.__data < datetime.now():
            raise ValueError("A data do evento não pode ser anterior à data atual.")
        if self.__capacidade_max <= 0:
            raise ValueError("A capacidade máxima deve ser um número positivo.")

    def inscrever_participante(self, participante):
        if len(self.__participantes) < self.__capacidade_max:
            self.__participantes.append(participante)
            print(f"{participante.nome} foi inscrito no evento {self.__nome}.")
        else:
            print("Evento lotado! Não é possível realizar novas inscrições.")

    def cancelar_inscricao(self, email):
        for p in self.__participantes:
            if p.email == email:
                self.__participantes.remove(p)
                print(f"Inscrição de {p.nome} cancelada com sucesso.")
                return
        print("Participante não encontrado para cancelamento.")

    def check_in(self, email):
        for p in self.__participantes:
            if p.email == email:
                p.presente = True
                print(f"{p.nome} realizou check-in com sucesso!")
                return
        print("Participante não encontrado para check-in.")
        
    def detalhes(self):
        return f"Evento: {self.__nome} | Data: {self.__data.strftime('%d/%m/%Y')} | Local: {self.__local} | Categoria: {self.__categoria} | Preço: R$ {self.__preco:.2f}"    
        
    def to_dict(self):
        return {
            "tipo": self.__class__.__name__,
            "nome": self.__nome,
            "data": self.__data.strftime("%d/%m/%Y"),
            "local": self.__local,
            "capacidade_max": self.__capacidade_max,
            "categoria": self.__categoria,
            "preco": self.__preco,
            "participantes": [p.to_dict() for p in self.__participantes],
            "extra": self._get_extra_data()
        }

    @staticmethod
    def from_dict(data):
        tipo = data["tipo"]
        if tipo == "Palestra":
            evento = Palestra(data["nome"], data["data"], data["local"], data["capacidade_max"], data["preco"], data["extra"])
        elif tipo == "Workshop":
            evento = Workshop(data["nome"], data["data"], data["local"], data["capacidade_max"], data["preco"], data["extra"])
        else:
            evento = Evento(data["nome"], data["data"], data["local"], data["capacidade_max"], data["categoria"], data["preco"])

        for p_data in data.get("participantes", []):
            participante = Participante.from_dict(p_data)
            evento.inscrever_participante(participante)

        return evento

    def _get_extra_data(self):
        return None    


class Palestra(Evento):
    def __init__(self, nome, data, local, capacidade_max, preco, palestrante):
        super().__init__(nome, data, local, capacidade_max, "Palestra", preco)
        self.__palestrante = palestrante

    @property
    def palestrante(self):
        return self.__palestrante
    
    def detalhes(self):
        return super().detalhes() + f" | Palestrante: {self.__palestrante}"
    
    def _get_extra_data(self):
        return self.__palestrante


class Workshop(Evento):
    def __init__(self, nome, data, local, capacidade_max, preco, material_necessario):
        super().__init__(nome, data, local, capacidade_max, "Workshop", preco)
        self.__material_necessario = material_necessario

    @property
    def material_necessario(self):
        return self.__material_necessario
    
    def detalhes(self):
        return super().detalhes() + f" | Material necessário: {self.__material_necessario}"
    
    def _get_extra_data(self):
        return self.__material_necessario 


class SistemaEventos:
    def __init__(self):
        self.eventos = []
        self.participantes = []

    def adicionar_evento(self):
        print("------ Cadastro de Evento ------")
        nome = input("Digite o nome do evento: ")
        data = input("Digite a data do evento (dd/mm/aaaa): ")
        local = input("Digite o local do evento: ")

        try:
            capacidade_max = int(input("Digite a capacidade máxima do evento: "))
            if capacidade_max <= 0:
                print("Capacidade deve ser positiva.")
                return
        except ValueError:
            print("Capacidade inválida.")
            return

        categoria = input("Digite a categoria do evento: ")
        try:
            preco = float(input("Digite o preço do ingresso: "))
        except ValueError:
            print("Preço inválido.")
            return

        evento = Evento(nome, data, local, capacidade_max, categoria, preco)
        self.eventos.append(evento)
        print("Evento cadastrado com sucesso.")

    def listar_eventos(self):
        print("\n------ Lista de Eventos ------")
        for evento in self.eventos:
            print(f"{evento.nome} - {evento.data.strftime('%d/%m/%Y')} - {evento.local} - Capacidade: {evento.capacidade_max}")
        print("-------------------------------\n")

    def inscrever_participante(self, nome_evento):
        nome = input("Digite o nome do participante: ")
        email = input("Digite o e-mail do participante: ")

        evento = None
        for e in self.eventos:
            if e.nome == nome_evento:
                evento = e
                break

        if evento is None:
            print(f"Erro: Evento '{nome_evento}' não encontrado.")
            return False

        for p in evento.participantes:
            if p.email == email:
                print("Este e-mail já está inscrito neste evento.")
                return False

        if len(evento.participantes) >= evento.capacidade_max:
            print(f"Erro: Evento '{nome_evento}' está lotado.")
            return False

        participante = Participante(nome, email)
        evento.participantes.append(participante)
        self.participantes.append(participante)
        print(f"{nome} foi inscrito com sucesso no evento '{nome_evento}'!")
        return True

    def total_inscritos(self, nome_evento):
        evento = next((e for e in self.eventos if e.nome == nome_evento), None)
        if evento:
            total = len(evento.participantes)
            print(f"O total de inscritos no evento '{nome_evento}' é de {total}.")
        else:
            print(f"Evento '{nome_evento}' não encontrado.")

    def vagas_disponiveis(self):
        print("\n------ Eventos com Vagas Disponíveis ------")
        for evento in self.eventos:
            vagas = evento.capacidade_max - len(evento.participantes)
            if vagas > 0:
                print(f"{evento.nome} - Vagas disponíveis: {vagas}")
        print("-------------------------------------------\n")

    def receita_total(self, nome_evento):
        evento = next((e for e in self.eventos if e.nome == nome_evento), None)
        if evento:
            receita = len(evento.participantes) * evento.preco
            print(f"A receita total do evento '{evento.nome}' é de R$ {receita:.2f}")
        else:
            print(f"Erro: Evento '{nome_evento}' não encontrado.")
            
    def buscar_por_categoria(self, categoria):
        # Mostra os eventos que pertencem à categoria informada
        print(f"\n🔎 Eventos da categoria '{categoria}':")
        encontrados = [e for e in self.eventos if e.categoria.lower() == categoria.lower()]
        # Exibe resultados, se houver
        for e in encontrados:
            print(f"• {e.nome} em {e.data.strftime('%d/%m/%Y')} no {e.local}")
        if not encontrados:
            print("Nenhum evento encontrado nessa categoria.")

    def buscar_por_data(self, data):
        # Mostra os eventos que acontecem em uma data específica
        data_busca = datetime.strptime(data, "%d/%m/%Y")
        print(f"\n📅 Eventos na data {data}:")
        encontrados = [e for e in self.eventos if e.data == data_busca]
        for e in encontrados:
            print(f"• {e.nome} - {e.local} ({e.categoria})")
        if not encontrados:
            print("Nenhum evento encontrado nessa data.")
            
    def cancelar_inscricao(self, nome_evento):
        email = input("Digite o e-mail do participante para cancelar inscrição: ")
        evento = next((e for e in self.eventos if e.nome == nome_evento), None)
        if not evento:
            print(f"Erro: Evento '{nome_evento}' não encontrado.")
            return False

        if evento.cancelar_inscricao(email):
            # Remove da lista geral de participantes (se existir)
            self.participantes = [p for p in self.participantes if p.email != email]
            return True
        return False         
            
    def realizar_check_in(self, nome_evento):
        email = input("Digite o e-mail do participante para check-in: ")
        evento = next((e for e in self.eventos if e.nome == nome_evento), None)
        if not evento:
            print(f"Erro: Evento '{nome_evento}' não encontrado.")
            return False

        return evento.check_in(email)         
            
    def salvar_dados_em_json(self, arquivo="dados_eventos.json"):
            dados = {
            "eventos": [e.to_dict() for e in self.eventos]
        }
            with open(arquivo, "w", encoding="utf-8") as f:
                json.dump(dados, f, ensure_ascii=False, indent=4)
            print("✅ Dados salvos com sucesso.")

    def carregar_dados_de_json(self, arquivo="dados_eventos.json"):
        if not os.path.exists(arquivo):
            return

        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)

        self.eventos = []
        for e_data in dados.get("eventos", []):
            evento = Evento.from_dict(e_data)
            self.eventos.append(evento)
            self.participantes.extend(evento.participantes)
        print("✅ Dados carregados com sucesso.")             
    
def main():
    sistema = SistemaEventos()
    sistema.carregar_dados_de_json()

    while True:
        print("\n====== Sistema de Gerenciamento de Eventos ======")
        print("1. Cadastrar novo evento")
        print("2. Listar eventos")
        print("3. Inscrever participante em evento")
        print("4. Ver total de inscritos em um evento")
        print("5. Ver eventos com vagas disponíveis")
        print("6. Ver receita total de um evento")
        print("7. Buscar evento por categoria")
        print("8. Buscar evento por data")
        print("9. Cancelar inscrição de participante")
        print("10. Realizar check-in de participante")
        print("0. Sair")
        print("=================================================")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            sistema.adicionar_evento()
        elif opcao == "2":
            sistema.listar_eventos()
        elif opcao == "3":
            nome_evento = input("Digite o nome do evento para inscrição: ")
            sistema.inscrever_participante(nome_evento)
        elif opcao == "4":
            nome_evento = input("Digite o nome do evento: ")
            sistema.total_inscritos(nome_evento)
        elif opcao == "5":
            sistema.vagas_disponiveis()
        elif opcao == "6":
            nome_evento = input("Digite o nome do evento: ")
            sistema.receita_total(nome_evento)
        elif opcao == "7":
            categoria = input("Digite a categoria do evento: ")
            sistema.buscar_por_categoria(categoria)  
        elif opcao == "8":
            data = input("Digite a categoria do evento: ")
            sistema.buscar_por_data(data)
        elif opcao == "9":
            nome_evento = input("Digite o nome do evento para cancelar inscrição: ")
            sistema.cancelar_inscricao(nome_evento)
        elif opcao == "10":
            nome_evento = input("Digite o nome do evento para check-in: ")
            sistema.realizar_check_in(nome_evento)           
        elif opcao == "0":
            sistema.salvar_dados_em_json()
            print("Encerrando o sistema. Até logo!")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

if __name__ == "__main__":
    main()                 