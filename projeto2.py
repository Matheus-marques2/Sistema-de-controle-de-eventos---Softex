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