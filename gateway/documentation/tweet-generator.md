
# Documentation - Tweet Generator Service

## Upload Archive
**Function:** User should be able to upload a Twitter Archive through this module. It will process, collect required texts, and trained the model for user.  
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
| archive     | File        | The archive file |  

**Example query**
```json
mutation uploadArchive($archive: Upload) {
    uploadArchive(archive: $archive){
        accountId,
        archiveId
    }
}
```

**Response Example**
```json
{
    "uploadArchive": {
        "accountId": "0966bf69-705f-469c-80ba-546e82ca0f04",
        "archiveId": 12
    }
}
```

## Status Checking
**Function:** User should be able to see status of uploaded file.  
**URL:** http://localhost:8000/graphql  
**Method:** POST  
**Headers:**
| Name             | Type        | Description |  
| ---------------- | ----------- | ----------- |  
| Authorization    | String      | Auth token provided by sign up/sign in e.g. ```Token 097d93b1-640b-4470-bee9-c698484d8535```|  

**Request Body**
```json
query {
    archive{
        status(archiveId: "11"){
            accountId,
            statusText,
            status,
            filename
        }
    }
}
```

**Response Example**
```json
{
    "archive": {
        "status": {
            "accountId": "0966bf69-705f-469c-80ba-546e82ca0f04",
            "statusText": "Active",
            "status": 0,
            "filename": "0966bf69-705f-469c-80ba-546e82ca0f04--2021-05-07--11:38:09.zip"
        }
    }
}
```

## Generating Tweet
**Function:** User should be able to generate tweet based on URL.  
**URL:** http://localhost:8000/graphql  
**Method:** POST  
**Headers:**
| Name             | Type        | Description |  
| ---------------- | ----------- | ----------- |  
| Authorization    | String      | Auth token provided by sign up/sign in e.g. ```Token 097d93b1-640b-4470-bee9-c698484d8535```|  

**Request Body**
```json
query {
    generator{
        tweet(accountId: "0966bf69-705f-469c-80ba-546e82ca0f04", url: "https://en.wikipedia.org/wiki/Nikola_Tesla"){
            accountId,
            text,
            tweet
        }
    }
}
```

**Response Example**
```json
{
    "generator": {
        "tweet": {
            "accountId": "0966bf69-705f-469c-80ba-546e82ca0f04",
            "text": "best known for his contributions to the design of the modern , Tesla studied engineering and physics in the 1870s without receiving a degree, gaining practical experience in the early 1880s working in . In 1884 he emigrated to the United States, where he became a naturalized citizen. He worked for a short time at the in New York City before he struck out on his own. With the help of partners to finance and market his ideas, Tesla set up laboratories and companies in New York to develop a range of electrical and mechanical devices. His in 1888, earned him a considerable amount of money and became the cornerstone of the polyphase system which that company eventually marketed.",
            "tweet": "he studied engineering and physics in the 1870s without receiving a degree. emigrated to the u.s. in 1884 and became the cornerstone of the polyphase system which that company eventually marketed."
        }
    }
}
```
