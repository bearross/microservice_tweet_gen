## Tweet Generation through Fine-tuned model with Twitter Archive
### Requirements and installation
1. Python 3.8.5

### Preparing database
1. Create folders 
   - ```../../cs-data/tweet-gen```
   - ```alembic/versions```
   - ```files/archives```
   - ```files/dataset```
   - ```files/checkpoints```
2. ```docker-compose up --build -d```
3. ```docker exec -it cs_tweet_gen bash```
4. ```alembic revision --autogenerate -m "Added initial tables"```
5. ```alembic upgrade head```


## Working modules
### Archive Upload
**Function:** User should be able to upload a Twitter Archive through this module. It will process, collect required texts, and trained the model for user.  
**URL:** http://localhost:8888/tweet-gen/archive/upload  
**Method:** POST  

**Input:**
| Name        | Type        | Description |  
| ----------- | ----------- | ----------- |  
| user_id     | Number      | User ID for relational database |  
| archive     | File        | The archive file |  

**Result:**
```json
{
    "data": {
        "user_id": 2,
        "archive": "2--twitter-Sadidul-Islam-2021-03-26.zip",
        "archive_id": 54,
        "status_url": "/status/2/54/"
    }
}
```


### Archive Status
**Function:** User should be able to see status of uploaded file.  
**URL:** http://localhost:8888/tweet-gen/status/2/53  
**Method:** GET  
**Required Parameters**  
**Input:**
| Name        | Type        | Description |  
| ----------- | ----------- | ----------- |  
| user_id     | Number      | User ID for relational database |  
| archive_id  | Number      | The archive id for relational database |  

**Result:**
```json
{
    "data": {
        "status": 0,
        "status_text": "Active",
        "archive_id": 53,
        "user_id": 2,
        "filename": "2--twitter-Sadidul-Islam-2021-03-26.zip"
    }
}
```


### Generate Tweet
**Function:** User should be able to generate tweet based on URL.  
**URL:** http://localhost:8888/tweet-gen/generate  
**Method:** POST  
**Required Parameters**
**Input:**
| Name        | Type        | Description |  
| ----------- | ----------- | ----------- |  
| user_id     | Number      | User ID for relational database |  
| url         | String      | URL of source text |  

**Result:**
```json
{
    "user_id": "2",
    "url_id": 5,
    "tweet_id": 5,
    "url": "https://en.wikipedia.org/wiki/Nikola_Tesla",
    "text": "best known for his contributions to the design of the modern , Tesla studied engineering and physics in the 1870s without receiving a degree, gaining practical experience in the early 1880s working in . In 1884 he emigrated to the United States, where he became a naturalized citizen. He worked for a short time at the in New York City before he struck out on his own. With the help of partners to finance and market his ideas, Tesla set up laboratories and companies in New York to develop a range of electrical and mechanical devices. His in 1888, earned him a considerable amount of money and became the cornerstone of the polyphase system which that company eventually marketed.",
    "tweet": "Tesla studied engineering and physics in the 1870s without receiving a degree. he emigrated to the united states in 1884 before launching his own company in november 1888, becoming the cornerstone of the polyphase system that that company eventually marketed."
}
```

