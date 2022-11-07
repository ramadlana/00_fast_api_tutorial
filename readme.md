### run in production

Export Env Variable, or set on cloud provider

```
export MONGO_SERVER_STRING="mongodb://xxxx"
```

#### Run test

`pytest --no-header -v --disable-warnings`

#### then

`python server.py`

#### Docker

`docker build -t image_name:<tag_or_version> . `

dont forget dot in end of syntax
