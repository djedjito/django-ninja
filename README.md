![image](https://github.com/user-attachments/assets/924e12e7-aea3-4142-acbe-9942eefe837e)

📝 Sistema de Autenticação com Django Ninja + JWT
Um sistema completo de autenticação com perfis de usuário (Admin, Anfitrião, Convidado) e menus dinâmicos, desenvolvido com Django Ninja e JWT.

🚀 Funcionalidades Principais
Autenticação por JWT (Tokens de acesso e refresh)

CRUD de usuários completo

Sistema de perfis com três níveis:

👑 Administrador (acesso total)

🏠 Anfitrião (gerencia propriedades)

👋 Convidado (acesso básico)

Menus dinâmicos por perfil

Transição entre perfis (Admin pode alterar perfis de outros usuários)

🛠 Tecnologias Utilizadas
Python 3.9+

Django 4.2

Django Ninja (para API REST)

SimpleJWT (para autenticação)

SQLite (banco de dados padrão)

⚙️ Configuração do Ambiente
Clone o repositório:

bash
git clone https://github.com/seu-usuario/django-auth-system.git
cd django-auth-system
Crie e ative um ambiente virtual:

bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
Instale as dependências:

bash
pip install -r requirements.txt
Configure o ambiente:

Renomeie .env.example para .env

Preencha com suas configurações

Aplique as migrações:

bash
python manage.py migrate
Crie um superusuário:

bash
python manage.py createsuperuser
Inicie o servidor:

bash
python manage.py runserver
📚 Estrutura do Projeto

django-auth-system/

├── auth_project/

├── users/    
│   ├── models.py    
│   ├── api.py            
│   └── signals.py        
├── .env.example           
├── requirements.txt       
└── manage.py            
🌐 Endpoints da API
Método	Endpoint	Descrição	Acesso
* POST	/api/register	Registrar novo usuário	Público
* POST	/api/token	Obter tokens JWT	Público
* GET	/api/profile/menu	Obter menu por perfil	Autenticado
* POST	/api/request-anfitriao	Solicitar upgrade para Anfitrião	Convidado
* POST	/api/users/{id}/change-profile	Alterar perfil de usuário	Admin
🔒 Modelos de Permissão
python
PROFILE_CHOICES = [
    ('admin', 'Administrador'),     # Acesso completo
    ('anfitriao', 'Anfitrião'),     # Gerenciar propriedades
    ('guest', 'Convidado')          # Acesso básico
]
🧪 Executando Testes
bash
python manage.py test
🤝 Como Contribuir
Faça um fork do projeto

Crie uma branch (git checkout -b feature/AmazingFeature)

Commit suas mudanças (git commit -m 'Add some AmazingFeature')

Push para a branch (git push origin feature/AmazingFeature)

Abra um Pull Request

📄 Licença
Distribuído sob a licença MIT. Veja LICENSE para mais informações.

✉️ Contato
Seu Nome - @seu_twitter - seu-email@exemplo.com

Link do Projeto: https://github.com/seu-usuario/django-auth-system
