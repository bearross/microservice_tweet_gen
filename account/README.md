## Account management
### Requirements and installation
1. Docker and docker compose

### Preparing database
1. Create folders 
   - ```../../cs-data/account```
   - ```alembic/versions```
2. ```docker-compose up --build -d```
3. ```docker exec -it cs_account bash```
4. ```alembic revision --autogenerate -m "Added initial tables"```
5. ```alembic upgrade head```

### Working modules
#### Sign up
**Function:** User will sign up for their account.  
**URL:** http://localhost:8001/account/signup  
**Method:** POST  

**Input:**
| Name             | Type        | Description |  
| ---------------- | ----------- | ----------- |  
| first_name       | String      | User's first name |  
| last_name        | String      | User's last name |  
| username         | String      | User's username |  
| email            | String      | Email of the user |  
| password         | String      | Password for the account |  
| confirm_password | String      | Same password again |  


#### Sign in
**Function:** User will sign in to their account.  
**URL:** http://localhost:8001/account/signin  
**Method:** POST  

**Input:**
| Name             | Type        | Description |  
| ---------------- | ----------- | ----------- |  
| username         | String      | User's username or email |  
| password         | String      | Password of the account |  


#### Account Detail
**Function:** User will sign in to their account.  
**URL:** http://localhost:8001/account/detail  
**Method:** POST  

**Headers:**
| Name             | Type        | Description |  
| ---------------- | ----------- | ----------- |  
| Authorization    | String      | Auth token provided by sign up/sign in e.g. ```Token 097d93b1-640b-4470-bee9-c698484d8535```|  


#### Forgot Password (Password reset request)
**Function:** User can reset their password by requesting a reset.  
**URL:** http://localhost:8001/account/password/forgot
**Method:** POST  

**Input:**
| Name             | Type        | Description |  
| ---------------- | ----------- | ----------- |  
| username         | String      | User's username or email |  


#### Reset Password
**Function:** User will sign in to their account.  
**URL:** http://localhost:8001/account/detail  
**Method:** POST  

**Input:**
| Name             | Type        | Description |  
| ---------------- | ----------- | ----------- |  
| token            | String      | Token provide by reset request |  
| password         | String      | New password for the account |  
| confirm_password | String      | Same password again |  


#### Account Update
**Function:** User will be able to update their account information.  
**URL:** http://localhost:8001/account/update  
**Method:** POST  

**Headers:**
| Name             | Type        | Description |  
| ---------------- | ----------- | ----------- |  
| Authorization    | String      | Auth token provided by sign up/sign in e.g. ```Token 097d93b1-640b-4470-bee9-c698484d8535```|  

**Input:**
| Name             | Type        | Description |  
| ---------------- | ----------- | ----------- |  
| first_name       | String      | User's first name |  
| last_name        | String      | User's last name |  
| username         | String      | User's username |  
| email            | String      | Email of the user |  
| password         | String      | Password for the account |  


#### Password Update
**Function:** User will be able to update their account information.  
**URL:** http://localhost:8001/account/password/update  
**Method:** POST  

**Headers:**
| Name             | Type        | Description |  
| ---------------- | ----------- | ----------- |  
| Authorization    | String      | Auth token provided by sign up/sign in e.g. ```Token 097d93b1-640b-4470-bee9-c698484d8535```|  


**Input:**
| Name             | Type        | Description |  
| ---------------- | ----------- | ----------- |  
| current_password | String      | Current Password for the account |  
| password         | String      | New Password to be set for the account |  
| confirm_password | String      | Same new password again |  
