# FreshRSS

## Descrição

O **FreshRSS** é um agregador de feeds RSS de código aberto que permite reunir notícias e conteúdos de diversos sites em uma única interface web.

A aplicação foi configurada utilizando Docker Compose e utiliza o banco de dados **SQLite integrado**, sem necessidade de um serviço externo de banco de dados.

---

## Requisitos

* Docker
* Docker Compose

---

## Configuração

Crie um arquivo `.env` na raiz do projeto:

```env
BASE_URL=http://localhost:8080
ADMIN_EMAIL=admin@admin.com
ADMIN_PASSWORD=admin
ADMIN_API_PASSWORD=admin
PUBLISHED_PORT=8080
```

Variáveis:

* `BASE_URL`: endereço de acesso da aplicação.
* `ADMIN_EMAIL`: e-mail do usuário administrador.
* `ADMIN_PASSWORD`: senha do administrador.
* `ADMIN_API_PASSWORD`: senha da API do FreshRSS.
* `PUBLISHED_PORT`: porta utilizada para acesso no navegador.

---

## Execução

Na pasta do projeto, execute:

```bash
docker compose up
```

A aplicação estará disponível em:

```
http://localhost:8080
```

Para parar a aplicação:

```bash
docker compose down
```

---

## Configurações do Docker Compose

* Foi utilizada a imagem oficial:

```
freshrss/freshrss:edge
```

* Os dados da aplicação são persistidos através do volume Docker:

```
data:/var/www/FreshRSS/data
```

* A porta HTTP do container (`80`) foi mapeada para a porta definida no arquivo `.env`.

* As configurações do administrador foram definidas através de variáveis de ambiente, mantendo os dados de configuração separados do arquivo `compose.yaml`.

* O banco de dados utilizado é o SQLite, incluído na própria aplicação FreshRSS.
