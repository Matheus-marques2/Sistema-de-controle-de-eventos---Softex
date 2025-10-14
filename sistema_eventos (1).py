#!/usr/bin/env python3
"""Sistema simples de gerenciamento de eventos com comentários em cada função.

Funcionalidades:
- Cadastro de eventos (valida data e capacidade)
- Inscrição de participantes (não permite duplicados por e-mail por evento, nem ultrapassar capacidade)
- Cancelamento de inscrição
- Check-in de participante
- Listagens, buscas por categoria/data
- Relatórios: inscritos por evento, eventos com vagas, receita total por evento
- Salvamento/carregamento em arquivo JSON (persistência simples)

Como usar:
- Rode: python sistema_eventos.py
- Siga o menu interativo.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Optional, Set

DATA_FILE = Path("eventos_db.json")


def today_date() -> date:
    """Retorna a data atual do sistema (usada para validar datas de eventos)."""
    return date.today()


@dataclass
class Participant:
    name: str
    email: str

    def to_dict(self):
        """Converte o participante em dicionário para salvar em JSON."""
        return {"name": self.name, "email": self.email}

    @staticmethod
    def from_dict(d):
        """Cria um objeto Participant a partir de um dicionário."""
        return Participant(name=d["name"], email=d["email"])


@dataclass
class Event:
    id: int
    name: str
    date: date
    location: str
    capacity: int
    category: str
    price: float
    participants: List[Participant] = field(default_factory=list)
    checked_in: Set[str] = field(default_factory=set)

    def free_slots(self) -> int:
        """Retorna o número de vagas disponíveis no evento."""
        return self.capacity - len(self.participants)

    def is_full(self) -> bool:
        """Verifica se o evento está lotado."""
        return len(self.participants) >= self.capacity

    def register_participant(self, participant: Participant) -> bool:
        """Inscreve um participante, se houver vaga e o e-mail não estiver duplicado."""
        email = participant.email.lower()
        if self.is_full():
            return False
        if any(p.email.lower() == email for p in self.participants):
            return False
        self.participants.append(participant)
        return True

    def cancel_participant(self, email: str) -> bool:
        """Cancela a inscrição de um participante, removendo-o da lista e do check-in."""
        email = email.lower()
        for i, p in enumerate(self.participants):
            if p.email.lower() == email:
                self.participants.pop(i)
                self.checked_in.discard(email)
                return True
        return False

    def check_in(self, email: str) -> bool:
        """Marca presença do participante (check-in)."""
        email = email.lower()
        if any(p.email.lower() == email for p in self.participants):
            self.checked_in.add(email)
            return True
        return False

    def revenue(self) -> float:
        """Calcula a receita total do evento (número de participantes * preço)."""
        return len(self.participants) * self.price

    def to_dict(self):
        """Converte o evento e seus participantes em dicionário para salvar em JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date.isoformat(),
            "location": self.location,
            "capacity": self.capacity,
            "category": self.category,
            "price": self.price,
            "participants": [p.to_dict() for p in self.participants],
            "checked_in": list(self.checked_in),
        }

    @staticmethod
    def from_dict(d):
        """Cria um objeto Event a partir de um dicionário (para carregar do JSON)."""
        ev = Event(
            id=d["id"],
            name=d["name"],
            date=datetime.fromisoformat(d["date"]).date(),
            location=d["location"],
            capacity=int(d["capacity"]),
            category=d["category"],
            price=float(d["price"]),
        )
        ev.participants = [Participant.from_dict(p) for p in d.get("participants", [])]
        ev.checked_in = set(d.get("checked_in", []))
        return ev


class EventManager:
    def __init__(self):
        """Inicializa o gerenciador com um dicionário de eventos e um contador de IDs."""
        self.events: Dict[int, Event] = {}
        self._next_id = 1

    def add_event(self, name: str, date_str: str, location: str, capacity: int, category: str, price: float) -> Event:
        """Adiciona um novo evento após validar a data e capacidade."""
        event_date = parse_date(date_str)
        if event_date < today_date():
            raise ValueError("A data do evento não pode ser anterior à data atual.")
        if capacity <= 0:
            raise ValueError("A capacidade máxima deve ser um número positivo.")
        ev = Event(id=self._next_id, name=name, date=event_date, location=location, capacity=capacity, category=category, price=price)
        self.events[self._next_id] = ev
        self._next_id += 1
        return ev

    def list_events(self) -> List[Event]:
        """Lista todos os eventos cadastrados, ordenados por data e nome."""
        return sorted(self.events.values(), key=lambda e: (e.date, e.name))

    def find_by_category(self, category: str) -> List[Event]:
        """Busca eventos por categoria (case-insensitive)."""
        return [e for e in self.events.values() if e.category.lower() == category.lower()]

    def find_by_date(self, date_str: str) -> List[Event]:
        """Busca eventos por uma data específica."""
        d = parse_date(date_str)
        return [e for e in self.events.values() if e.date == d]

    def get_event(self, event_id: int) -> Optional[Event]:
        """Obtém um evento pelo seu ID (ou None se não existir)."""
        return self.events.get(event_id)

    def register(self, event_id: int, name: str, email: str) -> bool:
        """Inscreve um participante em um evento existente."""
        ev = self.get_event(event_id)
        if not ev:
            raise ValueError("Evento não encontrado")
        part = Participant(name=name, email=email.lower())
        return ev.register_participant(part)

    def cancel_registration(self, event_id: int, email: str) -> bool:
        """Cancela a inscrição de um participante pelo e-mail."""
        ev = self.get_event(event_id)
        if not ev:
            raise ValueError("Evento não encontrado")
        return ev.cancel_participant(email)

    def check_in(self, event_id: int, email: str) -> bool:
        """Realiza o check-in de um participante (marca presença)."""
        ev = self.get_event(event_id)
        if not ev:
            raise ValueError("Evento não encontrado")
        return ev.check_in(email)

    def total_inscritos(self, event_id: int) -> int:
        """Retorna o total de inscritos em um evento específico."""
        ev = self.get_event(event_id)
        if not ev:
            raise ValueError("Evento não encontrado")
        return len(ev.participants)

    def eventos_com_vagas(self) -> List[Event]:
        """Lista eventos que ainda têm vagas disponíveis."""
        return [e for e in self.events.values() if not e.is_full()]

    def receita_total(self, event_id: int) -> float:
        """Calcula a receita total de um evento pelo ID."""
        ev = self.get_event(event_id)
        if not ev:
            raise ValueError("Evento não encontrado")
        return ev.revenue()

    def save(self, path: Path = DATA_FILE):
        """Salva todos os dados (eventos e participantes) em um arquivo JSON."""
        payload = {
            "next_id": self._next_id,
            "events": [e.to_dict() for e in self.events.values()],
        }
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False))

    def load(self, path: Path = DATA_FILE):
        """Carrega dados de eventos de um arquivo JSON, se existir."""
        if not path.exists():
            return
        payload = json.loads(path.read_text())
        self._next_id = int(payload.get("next_id", 1))
        self.events = {e_d["id"]: Event.from_dict(e_d) for e_d in payload.get("events", [])}


def parse_date(s: str) -> date:
    """Converte uma string (YYYY-MM-DD) em um objeto date, com tratamento de erro."""
    try:
        return datetime.fromisoformat(s).date()
    except Exception:
        raise ValueError("Formato de data inválido. Use YYYY-MM-DD")


def print_event(e: Event):
    """Exibe as informações resumidas de um evento formatadas na tela."""
    print(f"ID: {e.id} | {e.name} | {e.date.isoformat()} | {e.location} | Categoria: {e.category} | Capacidade: {e.capacity} | Inscritos: {len(e.participants)} | Preço: R$ {e.price:.2f}")


def interactive_menu():
    """Menu interativo que permite o uso completo do sistema via terminal."""
    mgr = EventManager()
    mgr.load()

    while True:
        print("\n--- Sistema de Eventos ---")
        print("1. Cadastrar evento")
        print("2. Listar eventos")
        print("3. Buscar por categoria")
        print("4. Buscar por data")
        print("5. Inscrever participante")
        print("6. Cancelar inscrição")
        print("7. Check-in")
        print("8. Relatórios")
        print("9. Salvar e sair")
        print("0. Sair sem salvar")
        choice = input("Escolha: ").strip()

        try:
            if choice == "1":
                name = input("Nome do evento: ").strip()
                date_str = input("Data (YYYY-MM-DD): ").strip()
                location = input("Local: ").strip()
                capacity = int(input("Capacidade máxima: ").strip())
                category = input("Categoria: ").strip()
                price = float(input("Preço do ingresso (use . para decimais): ").strip())
                ev = mgr.add_event(name, date_str, location, capacity, category, price)
                print(f"Evento criado com ID {ev.id}")

            elif choice == "2":
                for e in mgr.list_events():
                    print_event(e)

            elif choice == "3":
                cat = input("Categoria: ").strip()
                found = mgr.find_by_category(cat)
                if not found:
                    print("Nenhum evento nessa categoria.")
                for e in found:
                    print_event(e)

            elif choice == "4":
                d = input("Data (YYYY-MM-DD): ").strip()
                found = mgr.find_by_date(d)
                if not found:
                    print("Nenhum evento nessa data.")
                for e in found:
                    print_event(e)

            elif choice == "5":
                event_id = int(input("ID do evento: ").strip())
                name = input("Nome do participante: ").strip()
                email = input("Email: ").strip().lower()
                success = mgr.register(event_id, name, email)
                if success:
                    print("Inscrição realizada com sucesso.")
                else:
                    ev = mgr.get_event(event_id)
                    if ev is None:
                        print("Evento não encontrado.")
                    elif ev.is_full():
                        print("Evento lotado. Não foi possível inscrever.")
                    else:
                        print("E-mail já inscrito nesse evento.")

            elif choice == "6":
                event_id = int(input("ID do evento: ").strip())
                email = input("Email do participante a cancelar: ").strip().lower()
                ok = mgr.cancel_registration(event_id, email)
                if ok:
                    print("Inscrição cancelada.")
                else:
                    print("Participante não encontrado no evento.")

            elif choice == "7":
                event_id = int(input("ID do evento: ").strip())
                email = input("Email do participante para check-in: ").strip().lower()
                ok = mgr.check_in(event_id, email)
                if ok:
                    print("Check-in realizado.")
                else:
                    print("Participante não inscrito ou evento não encontrado.")

            elif choice == "8":
                print("--- Relatórios ---")
                print("a) Número total de inscritos por evento")
                print("b) Lista de eventos com vagas disponíveis")
                print("c) Calcular receita total de um evento")
                sub = input("Escolha: ").strip().lower()
                if sub == "a":
                    for e in mgr.list_events():
                        print(f"ID {e.id} - {e.name}: {len(e.participants)} inscritos")
                elif sub == "b":
                    for e in mgr.eventos_com_vagas():
                        print_event(e)
                elif sub == "c":
                    eid = int(input("ID do evento: ").strip())
                    print(f"Receita total: R$ {mgr.receita_total(eid):.2f}")
                else:
                    print("Opção inválida.")

            elif choice == "9":
                mgr.save()
                print("Dados salvos. Saindo...")
                break

            elif choice == "0":
                print("Saindo sem salvar...")
                break

            else:
                print("Escolha inválida.")

        except Exception as ex:
            print(f"Erro: {ex}")


if __name__ == "__main__":
    interactive_menu()
