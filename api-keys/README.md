## API Keys Service
### Requirements and installation
1. Docker and docker compose

### Preparing database
1. Create folders 
   - ```../../cs-data/api-keys```
   - ```alembic/versions```
2. ```docker-compose up --build -d```
3. ```docker exec -it cs_api_keys bash```
4. ```alembic revision --autogenerate -m "Added initial tables"```
5. ```alembic upgrade head```

### Working modules
#### Create Key
**Function:** User will be able to create key.  
**URL:** http://localhost:8005/create  
**Method:** POST  

**Input:**  
| Name             | Type        | Description |  
| ---------------- | ----------- | ----------- |  
| name             | String      | Name for the key |  
| account_id       | String      | Account id |  

**Example response**
```json
{
    "data": {
        "name": "new app 1",
        "account_id": "0966bf69-705f-469c-80ba-546e82ca0f04",
        "key": "d675fd23-be02-47df-b621-678fa646992b",
        "api_secret": "qcxRSNOskSdms-ba_3rkDMUy_sQFTCcOvh043np6D2giSui_QpqMc1cpKIjkciODST__x3Oj-wPN9TKvdEPdHwlDvsDRiP93L_KKVJa1X1xJFyaJoxZ_NaA-o1OL1IY8dKayNaHg8C-OIH-P_Ory6jVXu4RcH6Vj1oorSLdswbM"
    }
}
```

#### Rotate Key
**Function:** User will be able to rotate key.  
**URL:** http://localhost:8005/key/rotate  
**Method:** POST  

**Input:**  
| Name             | Type        | Description |  
| ---------------- | ----------- | ----------- |  
| key              | String      | Provided key |  
| account_id       | String      | Account id |  

**Example Response**
```json
{
    "data": {
        "account_id": "0966bf69-705f-469c-80ba-546e82ca0f04",
        "key": "0c0f00a9-ca94-42e1-a334-7b6947d399bd"
    }
}
```

#### Rotate Secret
**Function:** User will be able to rotate secret.  
**URL:** http://localhost:8005/secret/rotate  
**Method:** POST  

**Input:**  
| Name             | Type        | Description |  
| ---------------- | ----------- | ----------- |  
| key              | String      | Provided key |  
| account_id       | String      | Account id |  

**Example Response**
```json
{
    "data": {
        "account_id": "0966bf69-705f-469c-80ba-546e82ca0f04",
        "key": "fcacd5e5-61d7-4d05-b660-6df97738c532",
        "secret": "bcnusZ-CsUuKb6f0rgSaqnAapCsL3wS85jFRt-IChIHSFwVcwXQx5oZZ1ejgbZuMTUXfkYwfmnm0gg-Gd1dPbmfAgvUqYaxB9NL1hhD5l5iN6JiXH2IS6MeGTdVFjYZozmJxGa2EdNDNs8xgkHEWqknITIkU6UozM3rihVuQuQE"
    }
}
```

#### Update key details
**Function:** User will be able to update key detail.  
**URL:** http://localhost:8005/update  
**Method:** POST  

**Input:**  
| Name             | Type        | Description |  
| ---------------- | ----------- | ----------- |  
| key              | String      | Provided key |  
| account_id       | String      | Account id |  
| name             | String      | New name of the key |  

**Example Response**
```json
{
    "data": {
        "name": [
            "Name updated"
        ]
    }
}
```

#### Delete Key
**Function:** User will be able to delete key.  
**URL:** http://localhost:8005/delete  
**Method:** POST  

**Input:**  
| Name             | Type        | Description |  
| ---------------- | ----------- | ----------- |  
| key              | String      | Provided key |  
| account_id       | String      | Account id |  

**Example Response**
```json
{
    "errors": {
        "key": [
            "Invalid key"
        ]
    }
}
```

#### List Key
**Function:** User will be able to list keys.  
**URL:** http://localhost:8005/delete  
**Method:** POST  

**Input:**  
| Name             | Type        | Description |  
| ---------------- | ----------- | ----------- |  
| account_id       | String      | Account id |  

**Example Response**
```json
{
    "data": [
        {
            "key": "fcacd5e5-61d7-4d05-b660-6df97738c532",
            "secret": "j4lOeRaM672qZxyk3GhFU1NSRiaB5hOHn6Z3_eL6CSliq8NOUZ83X2s_hndziqoXO8wVdxQm5PDiLSqkr98_d5w0uXLMFExzgVa71WBjYLDq368JJvCwjwO2oC921QcDwWDfkFg3SbHkZAZrEszDBWhgX13WLilLo-mm2fTzbWs",
            "name": "new app",
            "status": 0
        },
        {
            "key": "fff884dc-1fbf-432b-99bf-9d3f529378c4",
            "secret": "dS0QYKWhKJJH8D19NutZhGznVBKcpaP0I7At0XzVevujbDm7P5f6KSZrUs0hAg1Nncj20bG_nVrfh-w31YNYV3DUJSZWrN_hCs78tKz1DyU5EDWqy_VnhyXRp9OUsocT4Zr8RoNt2sG8fmorgY0KvR-CUWRv4kdNG52ZKJMjIXI",
            "name": "new app 1",
            "status": 0
        },
        {
            "key": "0c0f00a9-ca94-42e1-a334-7b6947d399bd",
            "secret": "qcxRSNOskSdms-ba_3rkDMUy_sQFTCcOvh043np6D2giSui_QpqMc1cpKIjkciODST__x3Oj-wPN9TKvdEPdHwlDvsDRiP93L_KKVJa1X1xJFyaJoxZ_NaA-o1OL1IY8dKayNaHg8C-OIH-P_Ory6jVXu4RcH6Vj1oorSLdswbM",
            "name": "new app 1",
            "status": 0
        }
    ]
}
```

#### Key Detail
**Function:** User will be able to key detail and could be used for authentication check.  
**URL:** http://localhost:8005/detail  
**Method:** POST  

**Headers:**  
| Name             | Type        | Description |  
| ---------------- | ----------- | ----------- |  
| x-api-key        | String      | API Secret key |  
| x-public-key     | String      | API Public key |  

**Input:**  
| Name             | Type        | Description |  
| ---------------- | ----------- | ----------- |  
| account_id       | String      | Account id |  

**Example Response**
```json
{
    "data": {
        "owner": "0966bf69-705f-469c-80ba-546e82ca0f04",
        "public_key": "fcacd5e5-61d7-4d05-b660-6df97738c532",
        "status": 0,
        "created_at": "May 11, 2021 - 10:43:13 AM",
        "modified_at": "May 11, 2021 - 10:43:13 AM"
    }
}
```