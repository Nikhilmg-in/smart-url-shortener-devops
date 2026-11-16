# Smart URL Shortener (DevOps Project)

FastAPI URL shortener with Git, Jenkins CI, Ansible, Docker and Kubernetes.

Endpoints: `GET /`, `GET /health`, `GET /info`, `POST /shorten`, `GET /{code}`

## Component 1: CI

### 1.1 Git (2 branches + merge commit)
```bash
git init -b main
git add . && git commit -m "Initial commit: FastAPI app"
git checkout -b feature/ci-pipeline
# make a change (e.g. edit README), then:
git add . && git commit -m "Add CI pipeline"
git checkout main
git merge --no-ff feature/ci-pipeline -m "Merge feature/ci-pipeline into main"
git log --oneline --graph --all
git remote add origin <your-github-url> && git push -u origin --all
```

### 1.2 App
```bash
python3 -m venv .venv && source .venv/bin/activate
make install
make run            # then in another terminal:
curl -i http://localhost:8000/health
curl -i http://localhost:8000/info
curl -i -X POST http://localhost:8000/shorten -H "Content-Type: application/json" -d '{"url":"https://example.com"}'
```

### 1.3 Build
```bash
make test
make build          # creates dist/smart_url_shortener-1.0.0-py3-none-any.whl
```

### 1.4 Jenkins
New Item -> Pipeline -> "Pipeline script from SCM" -> Git -> your repo URL, branch `*/main`,
script path `Jenkinsfile`. Tick "GitHub hook trigger for GITScm polling" (webhook) and/or
"Poll SCM". The Jenkinsfile also polls every ~2 min as a fallback.
Jenkins machine needs: python3, python3-venv, make (and docker for the optional Docker stage).

### 1.5 Enhancements
- A: Test stage in Jenkinsfile (tests/test_main.py)
- B: Docker image tag = build number + git SHA (Jenkinsfile)
- C: .github/workflows/ci.yml

## Component 2

### 2.1 Ansible
Prerequisite: `sudo apt install -y ansible python3-venv`
```bash
cd ansible
ansible-playbook -i inventory.ini playbook.yml     # expect failed=0
curl -i http://localhost:8081/health
```
Variables: `app_port`, `app_env`, `app_dir`. Handler: "Restart url shortener".
Role: `roles/urlshortener` (galaxy layout).

### 2.2 Docker
```bash
docker build -t smart-url-shortener:v1 .
docker images
docker run -d -p 8000:8000 --name urlshort smart-url-shortener:v1
curl -i http://localhost:8000/health
docker ps
docker rm -f urlshort
```

### 2.3 Kubernetes (minikube)
```bash
minikube start
eval $(minikube docker-env)                     # build image INSIDE minikube
docker build -t smart-url-shortener:v1 .
kubectl apply -f k8s/
kubectl get deployments,services,pods -o wide
curl -i $(minikube service smart-url-shortener-service --url)/health
```
(kind instead: `kind load docker-image smart-url-shortener:v1`)

### 2.4 Scaling
```bash
kubectl scale deployment smart-url-shortener --replicas=5
kubectl get pods
kubectl scale deployment smart-url-shortener --replicas=3
kubectl get pods
```

### 2.5 Enhancements
- B: ConfigMap (k8s/configmap.yaml, injected with envFrom)
- C: liveness + readiness probes on /health
- D: multi-stage Dockerfile
- F: /health returns status, ready and uptime_seconds
- A (optional rollback demo):
```bash
kubectl set image deployment/smart-url-shortener smart-url-shortener=smart-url-shortener:broken
kubectl rollout status deployment/smart-url-shortener
kubectl rollout undo deployment/smart-url-shortener
kubectl get pods
```

## Demo tip
Storage is in memory and each pod has its own copy, so show `/health` and `/info`
through the Service. For the redirect demo use `kubectl port-forward pod/<name> 8000:8000`.
