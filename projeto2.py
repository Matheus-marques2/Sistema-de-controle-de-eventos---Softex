class Participante:
    def __init__(self, nome, email):
        self.__nome = nome
        self.__email = email

    @property
    def nome(self):
        return self.__nome

    @property
    def email(self):
        return self.__email
    
class Evento:
    def __init__(self, nome, data, local, capacidade_max, categoria, preco):
        self.__nome = nome
        self.__data = data
        self.__local = local
        self.__capacidade_max = capacidade_max
        self.__categoria = categoria
        self.__preco = preco
        self.__participantes = []

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
    
class Workshop(Evento):
    def __init__(self, nome, data, local, capacidade_max, preco, material_necessario):
        super().__init__(nome, data, local, capacidade_max, "Workshop", preco)
        self.__material_necessario = material_necessario

    @property
    def material_necessario(self):
        return self.__material_necessario
    
class Palestra(Evento):
    def __init__(self, nome, data, local, capacidade_max, preco, palestrante):
        super().__init__(nome, data, local, capacidade_max, "Palestra", preco)
        self.__palestrante = palestrante

    @property
    def palestrante(self):
        return self.__palestrante  

class SistemaEventos:
    def __init__(self):
        self.eventos = []
        self.participantes = []
        self.emails_inscritos = set()

    def adicionar_evento(self, evento):
        self.eventos.append(evento)

    def listar_eventos(self):
        for evento in self.eventos:
            print(f"{evento.nome} - {evento.data} - {evento.local} - Capacidade: {evento.capacidade_max}")

    def inscrever_participante(self, nome, email, nome_evento):
        # Verifica se o e-mail já está cadastrado
        if email in self.emails_inscritos:
            print(f"Erro: O e-mail '{email}' já está inscrito em um evento.")
            return False

        # Procura o evento
        evento = next((e for e in self.eventos if e.nome == nome_evento), None)
        if evento is None:
            print(f"Erro: Evento '{nome_evento}' não encontrado.")
            return False

        # Verifica se há vagas
        if len(evento.participantes) >= evento.capacidade_max:
            print(f"Erro: Evento '{nome_evento}' está lotado.")
            return False

        # Cria o participante e inscreve
        participante = Participante(nome, email)
        evento.participantes.append(participante)
        self.participantes.append(participante)
        self.emails_inscritos.add(email)
        print(f"{nome} foi inscrito com sucesso no evento '{nome_evento}'!")
        return True          

    from datetime import datetime  # Importa a classe datetime para trabalhar com datas

# CLASSE EVENTO
class Evento:
    def __init__(self, nome, data, local, capacidade_maxima, categoria, preco):
        # Inicializa os atributos principais de um evento
        self.nome = nome
        # Converte a data de string (ex: "25/11/2025") para formato datetime
        self.data = datetime.strptime(data, "%d/%m/%Y")
        self.local = local
        self.capacidade_maxima = capacidade_maxima
        self.categoria = categoria
        self.preco = preco
        # Lista para armazenar os participantes inscritos neste evento
        self.participantes = []

    def validar_evento(self):
        # Verifica se o evento possui uma data válida (futura)
        if self.data < datetime.now():
            raise ValueError("A data do evento não pode ser anterior à data atual.")
        # Garante que a capacidade máxima seja positiva
        if self.capacidade_maxima <= 0:
            raise ValueError("A capacidade máxima deve ser um número positivo.")

    def inscrever_participante(self, participante):
        # Adiciona um participante ao evento, se houver vagas disponíveis
        if len(self.participantes) < self.capacidade_maxima:
            self.participantes.append(participante)
            print(f"{participante.nome} foi inscrito no evento {self.nome}.")
        else:
            print("Evento lotado! Não é possível realizar novas inscrições.")

    def cancelar_inscricao(self, email):
        # Cancela a inscrição de um participante com base no e-mail
        for p in self.participantes:
            if p.email == email:
                self.participantes.remove(p)
                print(f"Inscrição de {p.nome} cancelada com sucesso.")
                return
        print("Participante não encontrado para cancelamento.")

    def check_in(self, email):
        # Marca a presença de um participante no evento
        for p in self.participantes:
            if p.email == email:
                p.presente = True
                print(f"{p.nome} realizou check-in com sucesso!")
                return
        print("Participante não encontrado para check-in.")

# CLASSE PARTICIPANTE
class Participante:
    def __init__(self, nome, email):
        # Inicializa os dados do participante
        self.nome = nome
        self.email = email
        self.presente = False  # Indica se o participante fez check-in (False por padrão)

# CLASSE SISTEMA DE EVENTOS
class SistemaEventos:
    def __init__(self):
        # Cria uma lista para armazenar todos os eventos do sistema
        self.eventos = []

    def cadastrar_evento(self, evento):
        # Valida o evento antes de adicioná-lo ao sistema
        evento.validar_evento()
        self.eventos.append(evento)
        print(f"Evento '{evento.nome}' cadastrado com sucesso!")

    def listar_eventos(self):
        # Exibe todos os eventos cadastrados e suas principais informações
        print("\n📋 Lista de Eventos:")
        for e in self.eventos:
            print(f"📅 {e.nome} - {e.data.strftime('%d/%m/%Y')} - {e.local} - {e.categoria} - R${e.preco}")
        if not self.eventos:
            print("Nenhum evento cadastrado ainda.")

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
  