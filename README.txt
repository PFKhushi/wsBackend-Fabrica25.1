# Rick and Morty Explorer - Documentação

## Visão Geral

Rick and Morty Explorer é uma aplicação Django que utiliza a API do Rick and Morty para buscar e exibir informações sobre personagens do universo da série. A aplicação oferece funcionalidades de autenticação (login, logout e registro) e armazena dados de personagens, localizações e episódios no banco de dados.

## Estrutura do Projeto

### Modelos

O projeto utiliza três modelos principais, todos estendendo a classe abstrata `SlugModel` que gera automaticamente slugs para as entidades:

#### SlugModel (Abstrato)
- Classe base abstrata que adiciona funcionalidade de slug automático para outros modelos
- Gera slugs únicos com base em um campo definido (por padrão, o campo "name")

#### Location
- Representa localizações do universo Rick and Morty
- Campos: id, name, location_type, dimension, url, created, slug

#### Character
- Representa personagens do universo Rick and Morty
- Campos: id, name, status, species, subspecies, gender, origin, location, image_url, url, created, slug
- Relacionamentos:
  - Muitos para um com Location (origin)
  - Muitos para um com Location (location)
  - Muitos para muitos com Episode

#### Episode
- Representa episódios da série Rick and Morty
- Campos: id, name, air_date, episode_code, url, created, slug

### Autenticação

O sistema usa o sistema de autenticação padrão do Django com as seguintes funcionalidades:

#### Login
- Função `user_login` que processa autenticação de usuários
- Template: `authenticate/login.html`

#### Logout
- Função `user_logout` protegida pelo decorador `@login_required`
- Redireciona para a página inicial após o logout

#### Registro
- Função `register_user` que utiliza o formulário `UserCreationForm` do Django
- Template: `authenticate/register_user.html`

### Admin Interface

O projeto configura o painel administrativo do Django para gerenciar:

- Personagens (`CharacterAdmin`)
- Episódios (`EpisodeAdmin`)
- Localizações (`LocationAdmin`)

Cada interface admin inclui campos de exibição (list_display), filtros (list_filter) e configuração de geração de slug (prepopulated_fields).

## Comportamento do Sistema

- **Autenticação Persistente**: Usuários registrados são armazenados permanentemente no banco de dados
- **Dados de Personagens**: Os dados dos personagens são carregados da API do Rick and Morty, mas não são persistidos entre sessões
- **Formulários**: Um formulário `CharacterSelectionForm` permite aos usuários selecionar personagens para visualização

## Configuração e Uso

### Requisitos
- Django
- Biblioteca para consumo da API do Rick and Morty (não especificada na documentação fornecida)

### Fluxo Básico
1. Usuário se registra ou faz login
2. Após autenticado, o usuário pode buscar personagens
3. Os detalhes do personagem são exibidos, incluindo:
   - Informações básicas (nome, espécie, gênero, status)
   - Localização de origem
   - Localização atual
   - Episódios em que aparece

## Limitações Atuais

- CRUD incompleto (algumas operações de escrita não estão implementadas)
- Dados de personagens não são persistidos permanentemente no banco de dados
- A documentação atual não inclui detalhes sobre a integração com a API externa

## Testes

O projeto inclui testes para os modelos:
- `LocationModelTest`: Testa a geração de slug, representação de string e validadores
- `CharacterModelTest`: Testa relacionamentos, valores padrão e geração de slug
- `EpisodeModelTest`: Testa representação e relacionamentos
- `SlugModelTest`: Testa a funcionalidade de geração e personalização de slugs

Estes testes garantem que o comportamento básico dos modelos está funcionando conforme esperado.