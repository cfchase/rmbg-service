#!/usr/bin/env bash
printf "\n\n######## test ########\n"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
MY_ROUTE=http://localhost:5000
MY_IMAGE="${DIR}/example_input.jpg"

curl ${MY_ROUTE}/api/status

(echo -n '{"image": "'; base64 "${MY_IMAGE}"; echo '"}') | curl -X POST -H "Content-Type: application/json" -d @- ${MY_ROUTE}/api/rmbg | jq -r '.image' | base64 -d > "${DIR}/example_output.png"

#(echo -n '{"image": "'; base64 "${MY_IMAGE}"; echo '"}') | curl -X POST -H "Content-Type: application/json" -d @- ${MY_ROUTE}/api/rmbg > "${DIR}/example_output.json"
