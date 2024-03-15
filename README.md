# rmbg-service
```
#!/usr/bin/env bash
printf "\n\n######## dev ########\n"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
MY_ROUTE=http://localhost:5000
MY_IMAGE="${DIR}/twodogs.jpg"

curl ${MY_ROUTE}/status

(echo -n '{"image": "'; base64 "${MY_IMAGE}"; echo '"}') | curl -X POST -H "Content-Type: application/json" -d @- ${MY_ROUTE}/api/rmbg
```
