# E-commerce API

Uma API RESTful desenvolvida com FastAPI para um e-commerce, com autenticação JWT e persistência em banco de dados PostgreSQL. A API permite realizar operações de criação e consulta de produtos, gerenciamento de pedidos e usuários.

## 🔧 Tecnologias Utilizadas
- **FastAPI**: Framework web moderno e assíncrono.
- **PostgreSQL**: Banco de dados relacional.
- **SQLAlchemy + Alembic**: ORM + controle de migrações.
- **JWT**: Autenticação baseada em tokens.
- **Docker**: Containerização para desenvolvimento e produção.
- **Terraform**: Provisionamento de infraestrutura na AWS.
- **GitHub Actions**: CI/CD automatizado.

## ☁️ Serviços AWS Utilizados

A infraestrutura do projeto é provisionada com Terraform na AWS e inclui os seguintes serviços:

| Serviço     | Finalidade                                                 |
|-------------|------------------------------------------------------------|
| **VPC**     | Isolamento de rede para a aplicação                        |
| **RDS**     | Banco de dados PostgreSQL gerenciado                       |
| **EC2**     | Máquina virtual para hospedar a aplicação (com Docker)     |
| **IAM**     | Controle de permissões para acesso seguro                  |
| **CloudWatch** | Logs e monitoramento do ambiente EC2/RDS     |