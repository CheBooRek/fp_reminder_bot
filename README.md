# TG bot reminder
Simple telegram bot, reminding to submit house meter readings on a regular basis 

## Intallation
 - Fill in conf/params.yaml
 - Add `.env` with `TG_BOT_TOKEN` variable
 - Setup commands:
 ```
 docker build --tag tg_housing_bot:0.1.0 .
 docker compose up
 ```

 ## Bot commands
  - `/start /help` - provide description
  - `/add_user` - add user TG ID to reminder group
