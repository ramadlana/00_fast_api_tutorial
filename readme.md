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

Notes:

- Cloudbuild is for Google Cloud Run CI/CD
- Dockerfile to build manually docker-images. if use cloudbuild yaml, ignore this
- .dockerignore is ignore file for dockerfile build
