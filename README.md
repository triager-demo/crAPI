# crAPI Vehicle Services

crAPI connects vehicle owners with maintenance services, a parts shop, and a driver community. Owners can manage their profile and vehicles, contact mechanics, track service reports, place orders, and use an automotive assistant.

## Architecture

| Service | Stack | Responsibility |
| --- | --- | --- |
| Web | React 18, TypeScript, OpenResty | Portal and API reverse proxy |
| Identity | Java 17, Spring Boot, Gradle | Accounts, authentication, profiles, vehicles |
| Community | Go 1.21 | Posts, comments, coupons |
| Workshop | Python 3.11, Django | Mechanics, service reports, products, orders |
| Chatbot | Python 3.11, LangChain | Assistant, retrieval, MCP tools |
| Dealership gateway | Go 1.21 | Vehicle ownership integration |
| MailHog | Go | Local email capture |

PostgreSQL and MongoDB store application data; Chroma stores assistant retrieval data. Services seed accounts, vehicles, products, and other fixtures on startup. API definitions are in `openapi-spec/`; existing request collections are in `postman_collections/`.

## Local setup

Install Docker with Compose v2, then run from the repository root:

```sh
docker compose -p crapi-local -f deploy/docker/docker-compose.yml build
docker compose -p crapi-local -f deploy/docker/docker-compose.yml up -d --no-build --wait --wait-timeout 300
```

Open [the portal](http://localhost:8888) and [local email](http://localhost:8025). HTTPS is available at `https://localhost:8443` with a local certificate. Images are built from this checkout and are never pushed. The first build downloads dependencies and can take several minutes.

Register using an `example.com` address, sign in, and use the vehicle details delivered to MailHog to add your vehicle. Browse the shop, place an order, contact a mechanic, and visit the community. The ordinary vehicle dashboard and mechanic dashboard remain part of the application.

```sh
docker compose -p crapi-local -f deploy/docker/docker-compose.yml logs --tail=100
docker compose -p crapi-local -f deploy/docker/docker-compose.yml down
```

Named volumes retain data after shutdown. Add `-v` to `down` only when you want to discard local data and reseed.

## Configuration

`deploy/docker/.env` controls service ports, TLS, log level, and optional compatibility behavior. The default bind is `127.0.0.1`. Existing shell-injection and Log4j toggles retain their original defaults. Do not change these as part of routine cleanup. The gateway hostname resolves inside the Compose network; no DNS setup is needed.

The assistant requires provider credentials to generate responses; the rest of the portal works without them. See [configuration](docs/setup.md). The bundled account directory and key documents are consumed by retrieval and must be retained as runtime fixtures.

## Development and checks

```sh
# Web: Node 20, committed npm lockfile
cd services/web
npm ci
npm run lint
npm run build
npm start
```

The development server proxies API calls to the local portal on port 8888.

```sh
# Identity: Java 17, committed Gradle wrapper
(cd services/identity && ./gradlew test spotlessCheck bootJar)
# Go services: Go 1.21, committed modules/checksums
(cd services/community && go test ./... && go vet ./... && go build ./...)
(cd services/gateway-service && go test ./... && go vet ./... && go build ./...)
# Lightweight assistant tests (Python 3.11)
python -m pip install pytest==8.3.5
PYTHONPATH=services/chatbot/src python -m pytest services/chatbot/src/chatbot/tests -q
# Cross-service checks against a running local stack
python3 scripts/smoke.py
```

For workshop tests, start `services/docker-database.yml`, install `services/workshop/requirements.txt` and `dev-requirements.txt` in a Python 3.11 virtual environment (with PostgreSQL and Cairo development libraries installed), then run `source .env` and `IS_TESTING=True python manage.py test --no-input` from `services/workshop`. Use a separate test stack; test databases are disposable.

CI separates formatting, builds, unit tests, seven container builds, and application integration. Container artifacts are used only by the integration job, without registry publication. No deployment workflows are included. Development targets `main` through pull requests.

## Provenance

This repository is derived from [OWASP crAPI](https://github.com/OWASP/crAPI), originally Completely Ridiculous API. It retains the upstream vulnerability behavior and is not production-ready. Presentation changes do not harden the services. Apache 2.0 licensing and existing copyright notices remain in place; see [LICENSE.md](LICENSE.md).
