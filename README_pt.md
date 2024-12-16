
# Projeto de Integração DocuSign

✨ Este projeto é uma aplicação Python que utiliza o SDK oficial do DocuSign para realizar integrações com a API da plataforma. Ele permite enviar envelopes para assinatura, criar views para assinatura e console, além de criar listas e enviar documentos para elas. ✨

---

## Funcionalidades Principais ⚙️

1. **Envio de envelopes**
   - Permite enviar documentos para assinatura utilizando o DocuSign.

2. **Criação de views**
   - Gera uma view de assinatura para os signatários.
   - Gera uma view de console para administradores ou operadores.

3. **Gestão de listas**
   - Permite criar listas de contatos.
   - Envia envelopes diretamente para listas criadas.

---

## Pré-requisitos ⚡

Para executar este projeto, você precisa ter os seguintes itens instalados no seu ambiente:

- **Python 3.12**
- **Docker** e **Docker Compose**

---

## Configuração e Execução 🚧

### 1. Clone o Repositório 🔧

```bash
 git clone <URL_DO_REPOSITORIO>
 cd <NOME_DO_REPOSITORIO>
```

### 2. Configure as Variáveis de Ambiente 🔢

Execute o seguinte comando para copiar o arquivo de exemplo para o arquivo `.env`:

```bash
cp .env.example .env
```

Esse comando irá copiar o conteúdo de .env.example para o arquivo .env, onde você deve atualizar as variáveis com seus valores específicos.

Além disso, crie um arquivo private.key dentro da pasta src e insira a chave privada fornecida pelo DocuSign.

> **Nota:** Certifique-se de configurar corretamente os valores acima com as credenciais obtidas no DocuSign Developer Center.

### 3. Execute o Projeto 🌐

A aplicação está totalmente containerizada. Para executá-la, siga os passos abaixo:

1. **Construa e inicie os containers**

   ```bash
   docker-compose up --build
   ```

2. **Acesse a Aplicação**
   - A API estará disponível em `http://localhost:8000` (ou conforme configurado no `docker-compose.yml`).

---

## Estrutura do Projeto 🌐

- **src/**: Contém o código-fonte da aplicação.
- **Dockerfile**: Define a imagem Docker para a aplicação.
- **docker-compose.yml**: Gerencia os serviços necessários para o ambiente.
- **.env.example**: Modelo de configuração de variáveis de ambiente.

---

## Como Contribuir 📢

Sinta-se à vontade para abrir issues ou pull requests para contribuir com melhorias ou correções. Certifique-se de seguir as diretrizes de contribuição antes de enviar sua proposta.

---

## Licença 📖

Este projeto está licenciado sob a [MIT License](LICENSE).
