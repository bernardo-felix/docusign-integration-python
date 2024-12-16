
# DocuSign Integration Project

✨ This project is a Python application that uses the official DocuSign SDK to integrate with the platform's API. It allows you to send envelopes for signature, create signing and console views, and also create and send to contact lists. ✨

---

## Main Features ⚙️

1. **Envelope Sending**
   - Allows sending documents for signature using DocuSign.

2. **View Creation**
   - Generates a signing view for signatories.
   - Generates a console view for administrators or operators.

3. **List Management**
   - Allows creating contact lists.
   - Sends envelopes directly to created lists.

---

## Requirements ⚡

To run this project, you need to have the following installed in your environment:

- **Python 3.12**
- **Docker** and **Docker Compose**

---

## Setup and Execution 🚧

### 1. Clone the Repository 🔧

```bash
 git clone <REPOSITORY_URL>
 cd <REPOSITORY_NAME>
```

### 2. Configure Environment Variables 🔢

Run the following command to copy the example file to the .env file:

```bash
cp .env.example .env
```

This command copies the content of .env.example into the .env file, where you should update the variables with your specific values.

Additionally, create a private.key file inside the src folder and insert the private key provided by DocuSign.

> **Note:** Make sure to configure the values above correctly with the credentials obtained from the DocuSign Developer Center.

### 3. Run the Project 🌐

The application is fully containerized. To run it, follow the steps below:

1. **Build and start the containers**

   ```bash
   docker-compose up --build
   ```

2. **Access the Application**
   - The API will be available at `http://localhost:8000` (or as configured in `docker-compose.yml`).

---

## Project Structure 🌐

- **src/**: Contains the application source code.
- **Dockerfile**: Defines the Docker image for the application.
- **docker-compose.yml**: Manages the necessary services for the environment.
- **.env.example**: Environment variable configuration template.

---

## How to Contribute 📢

Feel free to open issues or pull requests to contribute with improvements or fixes. Be sure to follow the contribution guidelines before submitting your proposal.

---

## License 📖

This project is licensed under the [MIT License](LICENSE).
