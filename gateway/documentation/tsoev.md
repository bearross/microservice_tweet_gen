
# Documentation - [TSOEV] Text Summarizer, Segmentation, Ownership Keyword, Extractor, Video Transcription 

## Upload Keyword Ownership CSV
**Function:** User should be able to upload keyword ownership csv.  
**URL:** http://localhost:8000/graphql  
**Method:** POST  
**Headers:**
| Name             | Type        | Description |  
| ---------------- | ----------- | ----------- |  
| Authorization    | String      | Auth token provided by sign up/sign in e.g. ```Token 097d93b1-640b-4470-bee9-c698484d8535```|  

**Input:**
| Name        | Type        | Description |  
| ----------- | ----------- | ----------- |  
| query       | JSON        | GraphQL query JSON |  
| csv_file    | File        | The keyword ownership csv file |  


**Example query**
```json
mutation {
    uploadKeywordOwnershipCsv(EnabledPA: "", csvFile: ""){
        opStatus
    }
}
```

**Response Example**
```json
{
    "uploadKeywordOwnershipCsv": {
        "opStatus": "ok"
    }
}
```


## Add Keyword Ownership
**Function:** User should be able to add keyword ownership row.  
**URL:** http://localhost:8000/graphql  
**Method:** POST  
**Headers:**
| Name             | Type        | Description |  
| ---------------- | ----------- | ----------- |  
| Authorization    | String      | Auth token provided by sign up/sign in e.g. ```Token 097d93b1-640b-4470-bee9-c698484d8535```|  


**Example query**
```json
mutation {
    addKeywordOwnership(Keyword: "amazon", URL: "https://www.chase.com/personal/credit-cards/amazon", 
    Position: 25, Traffic: 10, PA: 39){
        opStatus
    }
}
```

**Response Example**
```json
{
    "addKeywordOwnership": {
        "opStatus": "ok"
    }
}
```


## Add Keyword Ownership URL
**Function:** User should be able to add keyword ownership row.  
**URL:** http://localhost:8000/graphql  
**Method:** POST  
**Headers:**
| Name             | Type        | Description |  
| ---------------- | ----------- | ----------- |  
| Authorization    | String      | Auth token provided by sign up/sign in e.g. ```Token 097d93b1-640b-4470-bee9-c698484d8535```|  


**Example query**
```json
mutation {
    addKeywordOwnershipUrl(Url: "https://flask-mysql.readthedocs.io/en/stable/"){
        opStatus
    }
}
```

**Response Example**
```json
{
    "addKeywordOwnershipUrl": {
        "opStatus": "ok"
    }
}
```


## Own Keyword
**Function:** User should be able to own keyword.  
**URL:** http://localhost:8000/graphql  
**Method:** POST  
**Headers:**
| Name             | Type        | Description |  
| ---------------- | ----------- | ----------- |  
| Authorization    | String      | Auth token provided by sign up/sign in e.g. ```Token 097d93b1-640b-4470-bee9-c698484d8535```|  


**Example query**
```json
mutation {
    ownKeyword{
        opStatus
    }
}
```

**Response Example**
```json
{
    "ownKeyword": {
        "opStatus": "ok"
    }
}
```

## Keyword Refresh
**Function:** User should be able to keyword refresh.  
**URL:** http://localhost:8000/graphql  
**Method:** POST  
**Headers:**
| Name             | Type        | Description |  
| ---------------- | ----------- | ----------- |  
| Authorization    | String      | Auth token provided by sign up/sign in e.g. ```Token 097d93b1-640b-4470-bee9-c698484d8535```|  


**Example query**
```json
mutation {
    ownKeywordRefresh{
        opStatus
    }
}
```

**Response Example**
```json
{
    "ownKeywordRefresh": {
        "opStatus": "ok"
    }
}
```


## Revert Keyword
**Function:** User should be able to revert keyword.  
**URL:** http://localhost:8000/graphql  
**Method:** POST  
**Headers:**
| Name             | Type        | Description |  
| ---------------- | ----------- | ----------- |  
| Authorization    | String      | Auth token provided by sign up/sign in e.g. ```Token 097d93b1-640b-4470-bee9-c698484d8535```|  


**Example query**
```json
mutation {
    ownKeywordRevert{
        opStatus
    }
}
```

**Response Example**
```json
{
    "ownKeywordRevert": {
        "opStatus": "ok"
    }
}
```


## Reset Keywords
**Function:** User should be able to reset keyword.  
**URL:** http://localhost:8000/graphql  
**Method:** POST  
**Headers:**
| Name             | Type        | Description |  
| ---------------- | ----------- | ----------- |  
| Authorization    | String      | Auth token provided by sign up/sign in e.g. ```Token 097d93b1-640b-4470-bee9-c698484d8535```|  


**Example query**
```json
mutation {
    ownKeywordReset{
        opStatus
    }
}
```

**Response Example**
```json
{
    "ownKeywordReset": {
        "opStatus": "ok"
    }
}
```
