# BASH COMMANDS

### 1. Test FastAPI Health Endpoint

```bash
curl http://127.0.0.1:8080/api/health
```

Sends an HTTP GET request through Nginx to the FastAPI health endpoint and prints the JSON response. A successful response is `{"status":"healthy"}`, confirming that Nginx can forward the request to FastAPI.

### 2. Make Deployment Script Executable

```bash
chmod +x scripts/deploy-app.sh
```

Grants execute permission to `deploy-app.sh`, allowing it to be run directly as a program from the terminal.

### 3. Run Deployment Script

```bash
./scripts/deploy-app.sh
```

Executes the deployment script from the current directory. The script removes the existing FastAPI and Nginx containers and recreates them from their custom images inside the `nlab-app` pod.
