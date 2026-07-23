# 📝 Lista de Tarefas

Aplicação de lista de tarefas (To-Do List) containerizada com Docker, composta por três serviços independentes: banco de dados PostgreSQL, API REST em Flask e frontend estático servido via Nginx (que também atua como reverse proxy para a API).

## 🏗️ Arquitetura

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   frontend  │ ───► │   backend   │ ───► │      db     │
│   (nginx)   │      │   (flask)   │      │ (postgres)  │
│  porta 8080 │      │  porta 5000 │      │  porta 5432 │
└─────────────┘      └─────────────┘      └─────────────┘
```

- **frontend**: Nginx servindo HTML/CSS/JS estáticos e fazendo proxy de `/api/*` para o serviço `backend`.
- **backend**: API REST em Flask, responsável pelas operações CRUD das tarefas, conectando ao Postgres via `psycopg2`.
- **db**: PostgreSQL responsável por persistir os dados, com healthcheck para garantir que o backend só suba após o banco estar pronto.

Os serviços se comunicam através de duas redes Docker isoladas:
- `frontend`: conecta `frontend` ↔ `backend`
- `backend`: conecta `backend` ↔ `db`

Assim, o banco de dados fica inacessível externamente e o frontend não tem acesso direto ao banco.

## 🛠️ Tecnologias

| Camada     | Tecnologia                              |
|------------|------------------------------------------|
| Frontend   | HTML5, CSS3, JavaScript (Vanilla), Nginx |
| Backend    | Python 3, Flask, Flask-CORS, Gunicorn    |
| Banco      | PostgreSQL 16 (Alpine)                   |
| Infra      | Docker, Docker Compose                   |

## 📂 Estrutura do projeto

```
.
├── compose.yaml
├── .env
├── backend/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
└── frontend/
    ├── Dockerfile
    ├── nginx.conf
    ├── index.html
    └── script.js
```

## ⚙️ Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2, incluso no Docker Desktop)

## 🚀 Como executar

1. Clone o repositório:

   ```bash
   git clone <url-do-repositorio>
   cd <nome-do-projeto>
   ```

2. Crie um arquivo `.env` na raiz do projeto com as variáveis de ambiente do banco de dados:

   ```env
   POSTGRES_DB=teste
   POSTGRES_USER=teste
   POSTGRES_PASSWORD=teste
   ```

   > ⚠️ Use valores fortes e seguros para `POSTGRES_PASSWORD` em ambientes que não sejam apenas locais/de teste.

3. Suba os containers:

   ```bash
   docker compose up --build
   ```

4. Acesse a aplicação no navegador:

   ```
   http://localhost:8080
   ```

5. Para derrubar os containers:

   ```bash
   docker compose down
   ```

   Para remover também o volume de dados do Postgres:

   ```bash
   docker compose down -v
   ```

## 📡 Endpoints da API

Todos expostos através do prefixo `/api`, com proxy feito pelo Nginx.

| Método | Rota               | Descrição                          |
|--------|---------------------|--------------------------------------|
| GET    | `/api/tasks`         | Lista todas as tarefas               |
| POST   | `/api/tasks`         | Cria uma nova tarefa (`title`)       |
| PUT    | `/api/tasks/<id>`     | Atualiza título e/ou status da tarefa |
| DELETE | `/api/tasks/<id>`     | Remove uma tarefa                    |

## 🗃️ Modelo de dados

Tabela `tasks`, criada automaticamente na inicialização do backend:

| Coluna | Tipo     | Descrição                  |
|--------|----------|------------------------------|
| id     | SERIAL   | Chave primária                |
| title  | TEXT     | Título da tarefa               |
| done   | BOOLEAN  | Status de conclusão (default `false`) |

## 📌 Observações

- O backend cria a tabela `tasks` automaticamente na subida da aplicação (`init_db()`), não sendo necessário rodar migrações manuais.
- O `depends_on: condition: service_healthy` no `compose.yaml` garante que o backend só inicie após o Postgres estar pronto para aceitar conexões.
- O arquivo `.env` **não deve** ser versionado; adicione-o ao `.gitignore`.