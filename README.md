# ResponseCashedProxy

This utility works like a regular proxy, but at the same time it caches the response from the service in RAM and, 
if this service is unavailable, returns the last successful response.

## Utility Features

1. Setting a timeout from the service
2. Base64Encoding of params in the request path by key
3. Append params to the request path
4. Search strings in response by regEx and replace them with custom string

## Console arguments

Arg | Required | Default value | Description
-|-|-|-
`--util_port` | False | 9119 | Port on which the proxy web server will start
`--config_file` | False | `config.json` | File name with configs. File must be placed in `config` folder near `main.py`

## Instruction for JSON config file

First of all, you need to create `config` folder near `main.py` file.
Then create inside this folder blank new file. Strongly recommended to create file with name `config.json`, 
because in the future it is not expected to enter a console argument `--config_file`.

### JSON config keys

Key | Required | Default value | Type | Description | Example
-|-|-|-|-|-
`link` | True | Null | String | Link to service | `"link": "https://<host>"`
`timeout` | False | 10 | Integer | Timeout from service | `"timeout": 2`
`base64_keys` | False | Null | JsonArray\[String] | Param keys for base64Encoding | `"base64_keys": \["email"]`
`append_param` | False | Null | JsonObject{String(`request path`): String(`append params`)} | Append params to the request path | `"append_param": {"/modss": "?email=*****&logged=true"}`
`strings_for_replace` | False | Null | JsonObject{String(`request path`): {String(`regEx`): String(`custom string`)}} | Request path where need to set a custom string by regEx | `"strings_for_replace": {"/modss": {"API \\+ 'EPG'": "'http://10.10.0.21:9120/EPG'", "API \\+ 'tvPL'": "'http://10.10.0.21:9120/tvPL'"}`

### JSON config Example

```
{
  "link": "https://lampa.stream",
  "timeout": 5,
  "base64_keys": [
    "email"
  ],
  "append_param": {
    "/modss": "?email=**********&logged=true"
  },
  "strings_for_replace": {
    "/modss": {
      "API \\+ 'EPG'": "'http://10.10.0.21:9120/EPG'",
      "API \\+ 'tvPL'": "'http://10.10.0.21:9120/tvPL'"
    }
  }
}
```

## Installation using Docker

1. Build image `docker build -t response-cached-proxy .`
2. Run container ```docker run -d
    --restart always
    -p 9119:9119
    -v <path-to-config-folder>:/app/config
    -it
    --name response-cached-proxy
    response-cached-proxy```