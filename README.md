# Sistema de Registro de Atendimentos de Posto de Saúde/UPA

Aplicação web full stack, desenvolvida como projeto de extensão com foco em
comunidades carentes locais, para que um atendente de posto de saúde/UPA
registre e acompanhe os atendimentos do dia. O sistema é **administrativo**:
não lida com dados clínicos, prontuário ou anamnese, apenas com as
informações necessárias para organizar a fila de atendimento (paciente,
tipo de atendimento, status e data/hora).

## Público-alvo e decisões de interface

O sistema foi pensado para atendentes com pouca familiaridade com
tecnologia (muitas vezes usuários mais velhos):

- Poucos campos por tela (o cadastro pede apenas nome do paciente e tipo
  de atendimento).
- Tipo de atendimento é escolhido por **botões grandes** (categoria fixa),
  nunca digitado como texto livre — evita erros de digitação e reduz a
  carga cognitiva.
- Fluxo linear: navbar com apenas duas opções ("Início" e "Novo
  Registro"), sem menus escondidos.
- Feedback visual constante: confirmações grandes e coloridas de sucesso
  (verde) e erro (vermelho) após cada ação.

## Arquitetura

```
project/
├── backend/          # API REST em Flask
│   ├── app.py                          # ponto de entrada / composição da app
│   ├── config.py                       # configurações (Mongo, etc.)
│   ├── models/atendimento.py           # entidade Atendimento + categorias fixas
│   ├── repositories/atendimento_repository.py  # acesso ao MongoDB
│   ├── services/atendimento_service.py         # regras de negócio
│   └── routes/atendimento_routes.py            # endpoints (Blueprint)
├── frontend/         # SPA em React
│   └── src/
│       ├── components/  # FormAtendimento, ListaAtendimentos, DetalheAtendimento
│       ├── services/api.js  # chamadas axios centralizadas
│       └── App.js
└── docker-compose.yml
```

## Modelo de dados: Atendimento

| Campo             | Tipo   | Observações                                                             |
|--------------------|--------|---------------------------------------------------------------------------|
| `nome_paciente`    | string | nome do paciente                                                          |
| `tipo_atendimento` | string | categoria fixa: Consulta Geral, Vacinação, Curativo ou Encaminhamento     |
| `status`           | string | categoria fixa: aguardando, em atendimento ou finalizado                  |
| `data_hora`        | string | data e hora do registro (ISO 8601)                                        |

## Como rodar

Pré-requisito: Docker e Docker Compose instalados.

```bash
docker-compose up --build
```

- Backend (API): http://localhost:5001
- Frontend (React): http://localhost:3000
- MongoDB: porta 27017 (dados persistidos no volume `mongo_data`)

> O backend está mapeado para a porta 5001 no host (`"5001:5000"` no
> `docker-compose.yml`) porque a porta 5000 costuma estar ocupada no
> macOS pelo AirPlay Receiver. Se sua máquina não tiver esse conflito,
> você pode alterar o mapeamento para `"5000:5000"` e ajustar
> `REACT_APP_API_URL` no serviço `frontend` de acordo.

## Endpoints da API

| Método | Rota                        | Descrição                                        |
|--------|------------------------------|-----------------------------------------------------|
| GET    | `/atendimentos`              | Lista os atendimentos (aceita `?status=`)           |
| GET    | `/atendimentos/<id>`         | Detalhes de um atendimento específico               |
| POST   | `/atendimentos`               | Registra um novo atendimento                        |
| PUT    | `/atendimentos/<id>`         | Atualiza um atendimento (ex.: mudar o status)        |
| DELETE | `/atendimentos/<id>`         | Remove um registro de atendimento                    |

## Como os princípios SOLID foram aplicados

O backend é dividido em quatro camadas (`routes` → `services` →
`repositories` → `models`), cada uma com uma função bem definida.

### S — Single Responsibility Principle

- `atendimento_routes.py`: só entende de HTTP (ler request, devolver JSON
  e status code).
- `atendimento_service.py` (`AtendimentoService`): só contém regra de
  negócio (validação e orquestração das operações).
- `atendimento_repository.py` (`AtendimentoRepositoryMongo`): só sabe
  conversar com o MongoDB.
- `atendimento.py` (`Atendimento`): só representa e valida os dados de um
  atendimento, incluindo as categorias fixas permitidas.

### O — Open/Closed Principle

Se um dia o MongoDB for trocado por outro banco, basta criar uma nova
classe que implemente `AtendimentoRepositoryInterface` (ex.:
`AtendimentoRepositoryPostgres`) e trocar a instância criada em
`app.py`. Nenhuma linha de `atendimento_service.py` ou
`atendimento_routes.py` precisa mudar.

### L — Liskov Substitution Principle

`AtendimentoRepositoryMongo` é uma implementação de
`AtendimentoRepositoryInterface` e pode ser usada em qualquer lugar que
espera essa interface sem alterar o comportamento esperado pelo
`AtendimentoService`.

### I — Interface Segregation Principle

`AtendimentoRepositoryInterface` expõe apenas os métodos que o
`AtendimentoService` realmente usa: `listar`, `buscar_por_id`, `criar`,
`atualizar` e `remover`.

### D — Dependency Inversion Principle

`AtendimentoService` depende da abstração `AtendimentoRepositoryInterface`,
não da implementação concreta `AtendimentoRepositoryMongo`. A
implementação concreta é injetada pelo construtor, e quem decide qual usar
é o `app.py`, na composição da aplicação:

```python
repositorio_atendimentos = AtendimentoRepositoryMongo(colecao_atendimentos)
servico_atendimentos = AtendimentoService(repositorio_atendimentos)  # injeção de dependência
```

## Tratamento de erros

O backend usa `try/except` em todas as rotas e retorna:

- `400 Bad Request`: dados inválidos ou ausentes (ex.: tipo de atendimento
  fora das categorias permitidas, JSON malformado).
- `404 Not Found`: atendimento não encontrado.
- `500 Internal Server Error`: erro inesperado (ex.: falha de conexão com
  o banco).
# prj-back-end-faculdade-sistema-atendimento-posto-saude
