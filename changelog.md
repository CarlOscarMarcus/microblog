# Changelog

## [v11.0.0] - 2025-01-16
### Added
- Followers-funktionalitet (follow/unfollow-användare).
- Ny migrationsfil för followers-tabellen.
- CI/CD-pipelines (GitHub Actions) med tester, linting och Docker-build.
- Docker-image pushas automatiskt till Docker Hub.
- Dockerfile-prod för att starta prod miljö
- Dockerfile-test fär att testa lokala miljö
- docker-compose kommando `prod` för starta produktions miljö med mysql server
- docker-compose kommando `test` för att köra `make test` på lokala miljön

### Changed
- Uppdaterad User-modell med following/followers-logik.


