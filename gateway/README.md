## Tweet Generation through Fine-tuned model with Twitter Archive
### Requirements and installation
1. Docker and docker compose

### Preparing database
1. Create folders 
   - ```../../cs-data/gateway```
   - ```alembic/versions```
2. ```docker-compose up --build -d```
3. ```docker exec -it cs_gateway bash```
4. ```alembic revision --autogenerate -m "Added initial tables"```
5. ```alembic upgrade head```

## Microservices - Documentation
[Account Management](documentation/account.md)  
[Tweet Generator](documentation/tweet-generator.md)  
[API Keys](documentation/api-keys.md)
