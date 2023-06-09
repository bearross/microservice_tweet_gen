# copyscience

## Requirements

- Install `seomoz` package  [here](https://github.com/seomoz/SEOmozAPISamples/tree/master/python)
- Install `NeMo` package `pip install git+https://github.com/NVIDIA/NeMo.git`
- Install Bert Summarizer `pip install bert-extractive-summarizer --upgrade --force-reinstall`
- Install `pke` package `pip install git+https://github.com/boudinfl/pke.git`
- Install keybert package `pip install keybert`
- Download Spacy models `python -m spacy download en`

## The Endpoint API
(The endpoint api won't work sometimes. Please let me know when you want to test it.)

**Function:** User should be able to upload a CSV. <br />
**URL:** http://172.83.12.207:8888/key-own-upload-csv <br />
**Method:** POST <br />
The client should send a form data file as request body with following parameters:
```
csv_file: file - csv formatted file to upload

returns: 
JSON dict with following fields:

op_status:str -"ok", "failure"
```

**Function:** User should be able to submit via the interface. <br />
**URL:** http://172.83.12.207:8888/key-own-upload-raw <br />
**Method:** POST <br />
The client should send a form data file as request body with following parameters:
```
Keyword:
Url:
Position:
Traffic:

returns: 
JSON dict with following fields:

op_status:str -"ok", "failure"
```

**Function:** Rankings data from Semrush APIs can be used to inform keyword ownership. <br />
**URL:** http://172.83.12.207:8888/key-own-from-url <br />
**Method:** POST <br />
The client should send a form data file as request body with following parameters:
```
Url:

returns: 
JSON dict with following fields:

op_status:str -"ok", "failure"
```

**Function:** The user can refresh the data to recalculate keyword ownership. <br />
**URL:** http://172.83.12.207:8888/key-own-refresh <br />
**Method:** POST <br />
The client should send a form data file as request body with following parameters:
```
returns: 
JSON dict with following fields:

op_status:str -"ok", "failure"
```

**Function:** The user can revert to previous versions of the keyword to URL mappings. <br />
**URL:** http://172.83.12.207:8888/key-own-revert <br />
**Method:** POST <br />
The client should send a form data file as request body with following parameters:
```
returns: 
JSON dict with following fields:

op_status:str -"ok", "failure"
```

**Function:** The user can get all data in mysql database [only used in development mode] <br />
**URL:** http://172.83.12.207:8888/key-own-get-db <br />
**Method:** POST <br />

```
returns: 
JSON formatted file of mysql database
```

**Function:** The user can delete all data in mysql database [only used in development mode] <br />
**URL:** http://172.83.12.207:8888/key-own-reset-db <br />
**Method:** POST <br />

```
returns: 
JSON dict with following fields:

op_status:str -"ok", "failure"
```


**Function:** User can provide a URL. <br />
**URL:** http://172.83.12.207:8888/transcript-from-url <br />
**Method:** POST <br />
The client should send a form data file as request body with following parameters:
```
video_url:

returns: 
HTML template like following link
(https://moz.com/blog/seo-target-keywords)

op_status:str -"ok", "failure"
```

**Function:** User can provide a video file. <br />
**URL:** http://172.83.12.207:8888/transcript-from-file <br />
**Method:** POST <br />
The client should send a form data file as request body with following parameters:
```
video_file:

returns: 
HTML template like following link
(https://moz.com/blog/seo-target-keywords)

op_status:str -"ok", "failure"
```
