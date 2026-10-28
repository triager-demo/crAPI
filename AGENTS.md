# Repository guidance

- Architecture: `services/web` is React/TypeScript and OpenResty; `identity` is Java 17/Spring Boot/Gradle; `community` and `gateway-service` are Go; `workshop` is Python 3.11/Django; `chatbot` is Python 3.11. Compose also runs PostgreSQL, MongoDB, Chroma, and MailHog.
- Preserve existing vulnerability behavior. Do not harden authentication, validation, queries, uploads, assistant tools, dependency versions, or API responses as incidental cleanup. Keep technical weakness comments, initialization assets, seeded accounts, certificates/JWKS, and assistant retrieval fixtures.
- Use existing language conventions: Prettier for web, Spotless for Java, gofmt for Go. Prefer narrow changes and committed lockfiles; do not rewrite vendored dependencies.
- Commands: `npm ci`, `npm run lint`, `npm run build` in `services/web`; `./gradlew test spotlessCheck bootJar` in `services/identity`; `go test ./...`, `go vet ./...`, `go build ./...` in each Go service. Workshop tests require both databases and the service `.env`; see README. Chatbot helper tests use pytest with `PYTHONPATH=services/chatbot/src`.
- Local validation: `docker compose -p crapi-local -f deploy/docker/docker-compose.yml build`, then `up -d --no-build --wait --wait-timeout 300`; run `python3 scripts/smoke.py`. Do not remove volumes containing someone else's data.
- CI lives in `.github/workflows/ci.yml`. Keep required checks synchronized with its actual job names. Preserve failing-check enforcement without requiring another maintainer's approval.
- Work on a focused branch targeting `main`; respect concurrent edits. Do not deploy, provision infrastructure, configure DNS, publish images, add deployment workflows, or merge without an explicit request.
