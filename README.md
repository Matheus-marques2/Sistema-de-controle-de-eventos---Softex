# Sistema-de-controle-de-eventos---Softex

## Descrição

Este projeto consiste em um sistema básico para gerenciamento de eventos, permitindo o cadastro de eventos, inscrição de participantes, realização de check-in, cancelamento de inscrições, e consultas diversas (por categoria, data, vagas disponíveis, receita total, etc).

### Objetivo Educativo

Este projeto foi desenvolvido com **finalidade educacional**, com foco em demonstrar os desafios práticos e as soluções para:

- Modelagem orientada a objetos (POO) em Python;
- Tratamento de dados de eventos e participantes;
- Persistência de dados simples utilizando arquivos JSON;
- Validação de dados (datas futuras, capacidade máxima, integridade de inscrições);
- Interação básica via linha de comando.

O uso de arquivos JSON para salvar e carregar os dados do sistema é uma escolha simples, porém didática, que evidencia as dificuldades comuns como:

- Conversão entre objetos Python e formatos serializáveis (dicionários);
- Manutenção do estado do sistema entre execuções;
- Controle de integridade dos dados armazenados.

## Funcionalidades

- Cadastro de eventos (com validação de datas e capacidade);
- Inscrição e cancelamento de participantes;
- Realização de check-in dos participantes;
- Listagem e consulta de eventos por categoria e data;
- Visualização de vagas disponíveis e receita total;
- Persistência de dados em arquivo JSON para salvar o estado entre execuções.

## Estrutura do Projeto

- **Participante**: classe que representa um participante do evento.
- **Evento**: classe base para eventos, com subclasses específicas para `Palestra` e `Workshop`.
- **SistemaEventos**: gerencia a coleção de eventos e participantes, interage com o usuário e controla a persistência dos dados.

## Como usar

1. Execute o script principal para iniciar o sistema.
2. Use o menu para cadastrar eventos, inscrever participantes e outras operações.
3. Os dados são automaticamente salvos em arquivo JSON ao sair do sistema.
4. Na próxima execução, os dados anteriores serão carregados automaticamente.

## Observações

- A persistência por JSON é feita manualmente, transformando objetos em dicionários e vice-versa.
- Certas funcionalidades, como o cancelamento de inscrições, fazem uso de buscas lineares simples.
- O projeto pode ser expandido para usar bancos de dados reais, melhor interface, entre outros.

## Requisitos

- Python 3.x
- Bibliotecas padrão (`datetime`, `json`, `os`)

## Testes

O projeto inclui testes unitários para as principais funcionalidades utilizando `unittest`.

Para rodar os testes:

```bash
python -m unittest
