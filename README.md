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

| #  | Model         | Campos                                                                                                  | Relações                                                                                       |
|----|---------------|---------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------|
| 1  | **Product**   | id, name, slug, description, price, discount_price (opcional), stock_quantity, is_active, created_at, updated_at | 🔁 Pertence a uma ou mais `Categories`  <br> 🖼️ Pode ter várias `ProductImages` <br> 🎨 Pode ter várias `ProductVariants` |
| 2  | **Category**  | id, name, slug, description, parent_id, created_at, updated_at                                          | 🔁 Pode ser hierárquica via `parent_id` <br> 🔁 Tem muitos `Products`                          |
| 3  | **User**      | id, email, hashed_password, full_name, is_active, is_superuser, created_at, updated_at                 | 📬 Tem muitos `Addresses` <br> 🛒 Tem um `Cart` <br> 📦 Tem muitos `Orders` <br> ⭐ Pode fazer `Reviews` |
| 4  | **Address**   | id, user_id, street, number, city, state, zipcode, country, is_default_shipping, is_default_billing    | 🔁 Pertence a um `User`                                                                        |
| 5  | **Cart**      | id, user_id, created_at, updated_at                                                                     | 🔁 Pertence a um `User` <br> 🛍️ Tem muitos `CartItems`                                         |
| 6  | **CartItem**  | id, cart_id, product_id, quantity, price_snapshot                                                       | 🔁 Pertence a um `Cart` <br> 🔁 Refere-se a um `Product`                                        |
| 7  | **Order**     | id, user_id, status, total_price, shipping_address_id, billing_address_id, created_at, updated_at      | 🔁 Pertence a um `User` <br> 📦 Tem muitos `OrderItems` <br> 💳 Tem um `Payment` <br> 🚚 Tem um `Shipment` |
| 8  | **OrderItem** | id, order_id, product_id, quantity, price_snapshot                                                      | 🔁 Pertence a um `Order` <br> 🔁 Refere-se a um `Product`                                       |
| 9  | **Payment**   | id, order_id, payment_method, status, paid_at, transaction_id                                           | 🔁 Refere-se a um `Order`                                                                      |
| 10 | **Shipment**  | id, order_id, tracking_code, status, shipped_at, delivered_at                                          | 🔁 Refere-se a um `Order`                                                                      |
| 11 | **Review**    | id, user_id, product_id, rating, comment, created_at                                                   | 🔁 Refere-se a um `Product` e um `User`                                                        |
| 12 | **Coupon**    | id, code, discount_percent ou discount_fixed, min_order_value, expires_at, usage_limit, used_count     | (sem relações diretas, mas pode ser aplicado em `Orders` futuramente)                        |
