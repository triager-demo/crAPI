@echo off
cd /d "%~dp0..\..\deploy\docker"
docker compose build crapi-community %*
