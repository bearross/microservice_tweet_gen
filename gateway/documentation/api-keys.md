
# Documentation - API Keys Service

## Create API Key
**Function:** User will be able to create API key.  
**URL:** http://localhost:8000/graphql  
**Method:** POST  

**Headers:**
| Name             | Type        | Description |  
| ---------------- | ----------- | ----------- |  
| Authorization    | String      | Auth token provided by sign up/sign in e.g. ```Token 097d93b1-640b-4470-bee9-c698484d8535```|  

**Request Body**
```json
mutation createAPIKey {
    createApiKey(name: "New name test") {
        name,
        secret,
        publicKey,
        owner,
        errors {
            key,
            messages
        }
    }
}
```

**Response Example**
```json
{
    "createApiKey": {
        "name": "New name test",
        "secret": "ITrRRRS2sEs1SpYc784WXa-XtMojxzVY61GOorW76bpS4COQMew1lgs7CobrGO2OyKO4rED4JrS-Q0tymiqGFg",
        "publicKey": "1d6c3bec-340d-4ab3-9dd0-d6fee6b9e7d6",
        "owner": "7c5f9efb-b610-4999-83ae-52f939b37071",
        "errors": null
    }
}
```


## Get Detail
**Function:** User will be able to get api key detail.  
**URL:** http://localhost:8000/graphql  
**Method:** POST  

**Headers:**
| Name             | Type        | Description |  
| ---------------- | ----------- | ----------- |  
| x-api-key        | String      | API Public Key e.g. ```Bearer fcacd5e5-61d7-4d05-b660-6df97738c532```|  
| x-secret-key     | String      | API Secret Key e.g. ```Bearer TUaptm8mXNqNeFKWCz3fpU-6HfC2Ig55yPrnkbJdmsZtf7TOtrtYrbWfwJb2_FtLYZou8XFhxEuMudVw_k3jvw```|  

**Request Body**
```json
query {
    apiKey{
        detail{
            owner,
            publicKey,
            name,
            secret,
            status,
            createdAt,
            modifiedAt,
            errors{
                key,
                messages
            }
        }
    }
}
```

**Response Example**
```json
{
    "apiKey": {
        "detail": {
            "owner": "7c5f9efb-b610-4999-83ae-52f939b37071",
            "publicKey": "1924dd8d-142c-4cea-8d44-2e489de06116",
            "name": "new app 1",
            "secret": "ITrRRRS2sEs1SpYc784WXa-XtMojxzVY61GOorW76bpS4COQMew1lgs7CobrGO2OyKO4rED4JrS-Q0tymiqGFg",
            "status": 0,
            "createdAt": "May 13, 2021 - 07:30:23 AM",
            "modifiedAt": "May 13, 2021 - 07:30:23 AM",
            "errors": null
        }
    }
}
```


## Rotate Secret Key
**Function:** User will be able to rotate API Secret Key.  
**URL:** http://localhost:8000/graphql  
**Method:** POST  

**Headers:**
| Name             | Type        | Description |  
| ---------------- | ----------- | ----------- |  
| Authorization    | String      | Auth token provided by sign up/sign in e.g. ```Token 097d93b1-640b-4470-bee9-c698484d8535```|  

**Request Body**
```json
mutation rotateSecret {
    rotateSecret(publicKey: "5be0a36a-1433-47cb-bbed-cfd80344bbba") {
        owner,
        publicKey,
        secret,
        errors {
            key,
            messages
        }
    }
}
```

**Response Example**
```json
{
    "rotateSecret": {
        "owner": "7c5f9efb-b610-4999-83ae-52f939b37071",
        "publicKey": "5be0a36a-1433-47cb-bbed-cfd80344bbba",
        "secret": "T1ZjYeBo4BoQmos1gI1of75b7qQS9ANFjfpePZPRB_27yIYhBZuX6kCgZ5APg2DupMAYLWo76cQKjjMSskRCzQ",
        "errors": null
    }
}
```


## Update API Key
**Function:** User will be able to update API Key.  
**URL:** http://localhost:8000/graphql  
**Method:** POST  

**Headers:**
| Name             | Type        | Description |  
| ---------------- | ----------- | ----------- |  
| Authorization    | String      | Auth token provided by sign up/sign in e.g. ```Token 097d93b1-640b-4470-bee9-c698484d8535```|  

**Request Body**
```json
mutation updateAPIKey {
    updateApiKey(publicKey: "5be0a36a-1433-47cb-bbed-cfd80344bbba", name: "New name test 1") {
        name,
        errors {
            key,
            messages
        }
    }
}
```

**Response Example**
```json
{
    "updateApiKey": {
        "name": [
            "Name updated"
        ],
        "errors": null
    }
}
```


## Delete API Key
**Function:** User will be able to delete API Key.  
**URL:** http://localhost:8000/graphql  
**Method:** POST  

**Headers:**
| Name             | Type        | Description |  
| ---------------- | ----------- | ----------- |  
| Authorization    | String      | Auth token provided by sign up/sign in e.g. ```Token 097d93b1-640b-4470-bee9-c698484d8535```|  

**Request Body**
```json
mutation deleteAPIKey {
    deleteApiKey(publicKey: "5be0a36a-1433-47cb-bbed-cfd80344bbba") {
        delete,
        errors {
            key,
            messages
        }
    }
}
```

**Response Example**
```json
{
    "deleteApiKey": {
        "delete": [
            "Key deleted"
        ],
        "errors": null
    }
}
```


## List API Keys
**Function:** User will be able to list API Keys.  
**URL:** http://localhost:8000/graphql  
**Method:** POST  

**Headers:**
| Name             | Type        | Description |  
| ---------------- | ----------- | ----------- |  
| Authorization    | String      | Auth token provided by sign up/sign in e.g. ```Token 097d93b1-640b-4470-bee9-c698484d8535```|  
| x-api-key        | String      | API Public Key e.g. ```Bearer fcacd5e5-61d7-4d05-b660-6df97738c532```|  
| x-secret-key     | String      | API Secret Key e.g. ```Bearer TUaptm8mXNqNeFKWCz3fpU-6HfC2Ig55yPrnkbJdmsZtf7TOtrtYrbWfwJb2_FtLYZou8XFhxEuMudVw_k3jvw```|  

**Request Body**
```json
query {
    apiKey{
        list{
            keys{
                owner,
                publicKey,
                name,
                secret,
                status,
                createdAt,
                modifiedAt
            },
            errors{
                key,
                messages
            }
        }
    }
}
```

**Response Example**
```json
{
    "apiKey": {
        "list": {
            "keys": [
                {
                    "owner": "7c5f9efb-b610-4999-83ae-52f939b37071",
                    "publicKey": "1924dd8d-142c-4cea-8d44-2e489de06116",
                    "name": "new app 1",
                    "secret": "ITrRRRS2sEs1SpYc784WXa-XtMojxzVY61GOorW76bpS4COQMew1lgs7CobrGO2OyKO4rED4JrS-Q0tymiqGFg",
                    "status": 0,
                    "createdAt": "May 13, 2021 - 07:30:23 AM",
                    "modifiedAt": "May 13, 2021 - 07:30:23 AM"
                },
                {
                    "owner": "7c5f9efb-b610-4999-83ae-52f939b37071",
                    "publicKey": "95915e81-ef48-4708-9148-578af3bf8e53",
                    "name": "New name test",
                    "secret": "ITrRRRS2sEs1SpYc784WXa-XtMojxzVY61GOorW76bpS4COQMew1lgs7CobrGO2OyKO4rED4JrS-Q0tymiqGFg",
                    "status": 0,
                    "createdAt": "May 13, 2021 - 07:34:06 AM",
                    "modifiedAt": "May 13, 2021 - 07:34:06 AM"
                },
                {
                    "owner": "7c5f9efb-b610-4999-83ae-52f939b37071",
                    "publicKey": "d3aac8e0-447e-4be8-ac05-16895d051790",
                    "name": "New name test",
                    "secret": "ITrRRRS2sEs1SpYc784WXa-XtMojxzVY61GOorW76bpS4COQMew1lgs7CobrGO2OyKO4rED4JrS-Q0tymiqGFg",
                    "status": 0,
                    "createdAt": "May 13, 2021 - 07:34:20 AM",
                    "modifiedAt": "May 13, 2021 - 07:34:20 AM"
                },
                {
                    "owner": "7c5f9efb-b610-4999-83ae-52f939b37071",
                    "publicKey": "1d6c3bec-340d-4ab3-9dd0-d6fee6b9e7d6",
                    "name": "New name test",
                    "secret": "ITrRRRS2sEs1SpYc784WXa-XtMojxzVY61GOorW76bpS4COQMew1lgs7CobrGO2OyKO4rED4JrS-Q0tymiqGFg",
                    "status": 0,
                    "createdAt": "May 13, 2021 - 07:38:29 AM",
                    "modifiedAt": "May 13, 2021 - 07:38:29 AM"
                }
            ],
            "errors": null
        }
    }
}
```

