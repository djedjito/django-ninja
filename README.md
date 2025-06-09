![image](https://github.com/user-attachments/assets/924e12e7-aea3-4142-acbe-9942eefe837e)

🔐 User Management & API Service Platform (Django + Ninja + JWT)

    Este projeto é uma plataforma moderna e escalável de gestão de usuários e serviços web, construída com Django, Django Ninja, JWT e boas práticas de engenharia de software. Foi concebido com uma arquitetura modular e robusta, pensando em segurança, extensibilidade e clareza — ideal para ambientes de produção e demonstrações técnicas.

✨ Destaques

    ✅ Autenticação segura com JWT
    
    ⚙️ Interface web (API REST) via Django Ninja
    
    🧰 CLI administrativa via manage.py
    
    🧩 Arquitetura modular baseada em Django Apps reutilizáveis
    
    🛠️ Separação clara entre componentes internos, externos e bibliotecas
    
    📚 Utilização de bibliotecas modernas e bem suportadas

🧠 Visão Arquitetural

    Nota: A imagem acima mostra o fluxo de dados e interações entre módulos internos, utilizadores externos, bases de dados e bibliotecas compartilhadas.

🔍 Componentes Principais

1. Application Core
    Base principal da lógica de negócio.

    Expõe endpoints REST através do Django Ninja.

    Interage com o User Management Module.

2. User Management Module

    App Django dedicado à criação, autenticação e gerenciamento de usuários.

    Utilizado tanto pela CLI quanto pela camada de serviço web.

3. Management CLI
   
    Interface de linha de comando via manage.py.

    Permite operações administrativas e de manutenção.

4. Web Service Core
   
    Camada que lida com requisições HTTP externas.

    Utiliza Django + Django Ninja para servir APIs protegidas por JWT.

5. User Account Module
    Módulo responsável por dados de conta, configurações e perfis de usuários.

🛡️ Autenticação e Segurança

    Baseada em JWT, com suporte a tokens de acesso e refresh.

    Toda comunicação entre cliente e servidor é feita por HTTPS (recomendado).

    Tokens são verificados em middleware e protegidos com práticas modernas de segurança.

    Melhores práticas de segurança do OWASP top 10, consulte no link: https://owasp.org/Top10/

🗃️ Base de Dados

    Utiliza SQLite para persistência local durante o desenvolvimento.

    Modular e facilmente adaptável para PostgreSQL ou outro SGBD relacional em produção.

🔧 Dependências

        Django==X.X
        djangorestframework==X.X
        django-ninja==X.X
        djangorestframework-simplejwt==X.X
        Consulte requirements.txt para a lista completa.

🚀 Como Rodar o Projeto
    bash
    Copy
    Edit
# 1. Clone o repositório
git clone https://github.com/djedjito/django-ninja.git
cd seu-repo

# 2. Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute as migrações
python manage.py migrate

# 5. Inicie o servidor
    python manage.py runserver
📮 Exemplo de Requisição via API
    http
    Copy
    Edit
    POST /api/auth/token
    Authorization: Bearer <your_token>
    Content-Type: application/json

    {
      "username": "usuario_exemplo",
      "password": "sua_senha"
    }
👤 Usuários e Papéis
    User: Acessa a API via HTTP
    
    End User / Developer / Operator: Atua externamente no banco ou consome serviços
    
    Admin CLI: Executa comandos administrativos (ex: criação em massa, reset de senhas)
    
    Serviço Web: Responsável por autenticação, rotas, autorização e gestão de sessão

🔄 Extensibilidade
    Cada módulo é desacoplado e pode ser substituído, extendido ou reusado em diferentes projetos Django. Exemplo: o módulo de autenticação pode ser facilmente migrado para outro projeto com mínima modificação.

⭐ Se este projeto te ajudou ou chamou atenção, considere dar uma estrela no repositório!
