@echo off
cd /d "%~dp0..\..\deploy\docker"
docker compose build api.mypremiumdealership.com %*
