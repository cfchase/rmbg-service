#!/usr/bin/env bash
printf "\n\n######## test ########\n"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
base_url="${BASE_URL:-http://127.0.0.1:5000}"
#BASE_URL=http://localhost:5000
#IMAGE="${DIR}/example_input.png"
image="${IMAGE:-$DIR/example_input.png}"
echo $base_url
echo $image
echo ${base_url}/api/status
rmbg=${base_url}/api/rmbg
echo ${rmbg}

curl ${base_url}/api/status
(echo -n '{"image": "'; base64 "${image}"; echo '"}') | curl -X POST -H "Content-Type: application/json" -d @- $rmbg > example_output.json
(echo -n '{"image": "'; base64 "${image}"; echo '"}') | curl -X POST -H "Content-Type: application/json" -d @- $rmbg | jq -r '.image' | base64 -d > "${DIR}/example_output.png"

