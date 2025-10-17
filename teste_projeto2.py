import unittest
from datetime import datetime, timedelta
from io import StringIO
import sys
from unittest import mock

from projeto2 import Participante, Evento, Palestra, Workshop, SistemaEventos


class TestParticipante(unittest.TestCase):
    def test_criacao_participante(self):
        p = Participante("Ana", "ana@email.com")
        self.assertEqual(p.nome, "Ana")
        self.assertEqual(p.email, "ana@email.com")
        self.assertFalse(p.presente)


class TestEvento(unittest.TestCase):
    def setUp(self):
        data_futura = (datetime.now() + timedelta(days=10)).strftime("%d/%m/%Y")
        self.evento = Evento("PythonConf", data_futura, "Auditório", 2, "Tecnologia", 100.0)
        self.participante1 = Participante("João", "joao@email.com")
        self.participante2 = Participante("Maria", "maria@email.com")

    def test_validar_evento_valido(self):
        # Não deve lançar exceção
        self.evento.validar_evento()

    def test_validar_evento_data_passada(self):
        data_passada = (datetime.now() - timedelta(days=1)).strftime("%d/%m/%Y")
        evento = Evento("Evento Passado", data_passada, "Local", 10, "Categoria", 50)
        with self.assertRaises(ValueError):
            evento.validar_evento()

    def test_validar_evento_capacidade_invalida(self):
        data_futura = (datetime.now() + timedelta(days=5)).strftime("%d/%m/%Y")
        evento = Evento("Capacidade Zero", data_futura, "Local", 0, "Categoria", 50)
        with self.assertRaises(ValueError):
            evento.validar_evento()

    def test_inscrever_participante_com_sucesso(self):
        self.evento.inscrever_participante(self.participante1)
        self.assertIn(self.participante1, self.evento.participantes)

    def test_inscrever_participante_evento_lotado(self):
        self.evento.inscrever_participante(self.participante1)
        self.evento.inscrever_participante(self.participante2)
        # Captura do print
        with StringIO() as buf, mock.patch('sys.stdout', buf):
            self.evento.inscrever_participante(Participante("Carlos", "carlos@email.com"))
            output = buf.getvalue()
        self.assertIn("Evento lotado", output)

    def test_cancelar_inscricao_existente(self):
        self.evento.inscrever_participante(self.participante1)
        self.evento.cancelar_inscricao(self.participante1.email)
        self.assertNotIn(self.participante1, self.evento.participantes)

    def test_cancelar_inscricao_inexistente(self):
        with StringIO() as buf, mock.patch('sys.stdout', buf):
            self.evento.cancelar_inscricao("naoexiste@email.com")
            output = buf.getvalue()
        self.assertIn("Participante não encontrado", output)

    def test_check_in_sucesso(self):
        self.evento.inscrever_participante(self.participante1)
        self.evento.check_in(self.participante1.email)
        self.assertTrue(self.participante1.presente)

    def test_check_in_participante_nao_encontrado(self):
        with StringIO() as buf, mock.patch('sys.stdout', buf):
            self.evento.check_in("naoexiste@email.com")
            output = buf.getvalue()
        self.assertIn("Participante não encontrado", output)


class TestSubclassesEvento(unittest.TestCase):
    def test_palestra(self):
        data = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
        palestra = Palestra("AI Talk", data, "Sala X", 50, 30.0, "Dra. Silvia")
        self.assertEqual(palestra.palestrante, "Dra. Silvia")
        self.assertEqual(palestra.categoria, "Palestra")

    def test_workshop(self):
        data = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
        workshop = Workshop("Python Hands-on", data, "Lab", 30, 80.0, "Notebook")
        self.assertEqual(workshop.material_necessario, "Notebook")
        self.assertEqual(workshop.categoria, "Workshop")


class TestSistemaEventos(unittest.TestCase):
    def setUp(self):
        self.sistema = SistemaEventos()
        self.data_futura = (datetime.now() + timedelta(days=2)).strftime("%d/%m/%Y")
        self.evento = Evento("TestEvent", self.data_futura, "Online", 2, "Educação", 100.0)
        self.sistema.eventos.append(self.evento)

    def test_total_inscritos(self):
        p = Participante("Teste", "teste@email.com")
        self.evento.inscrever_participante(p)
        with StringIO() as buf, mock.patch('sys.stdout', buf):
            self.sistema.total_inscritos("TestEvent")
            output = buf.getvalue()
        self.assertIn("1", output)

    def test_receita_total(self):
        p1 = Participante("A", "a@email.com")
        p2 = Participante("B", "b@email.com")
        self.evento.inscrever_participante(p1)
        self.evento.inscrever_participante(p2)
        with StringIO() as buf, mock.patch('sys.stdout', buf):
            self.sistema.receita_total("TestEvent")
            output = buf.getvalue()
        self.assertIn("R$ 200.00", output)

    def test_buscar_por_categoria(self):
        with StringIO() as buf, mock.patch('sys.stdout', buf):
            self.sistema.buscar_por_categoria("Educação")
            output = buf.getvalue()
        self.assertIn("TestEvent", output)

    def test_buscar_por_data(self):
        with StringIO() as buf, mock.patch('sys.stdout', buf):
            self.sistema.buscar_por_data(self.data_futura)
            output = buf.getvalue()
        self.assertIn("TestEvent", output)


if __name__ == "__main__":
    unittest.main()
