### run in production

Export Env Variable, or set on cloud provider

```
export STRING_URI_MONGO="url_here"
export PASSWORD_MONGO_ATLAS=password
export USERNAME_MONGO_ATLAS=username
```

#### Run test

`pytest --no-header -v --disable-warnings`

#### then

`python server.py`
