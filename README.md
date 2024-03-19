# rmbg-service

Returns a JSON object with the base64 encoded image in PNG format of the background removed.

### Input Request JSON
```
{
  "image": "base64 encoded image in PNG or JPEG format"
}
```

### Output Response JSON
```
{
  "image": "base64 encoded image in PNG format"
}
```

### CURL example
```shell
(echo -n '{"image": "'; base64 "${image}"; echo '"}') | curl -X POST -H "Content-Type: application/json" -d @- $rmbg | jq -r '.image' | base64 -d > "${DIR}/example_output.png"

```
Full script: [scripts/curl-example.sh](scripts/curl-example.sh)
```shell
IMAGE=my_image.jpg ./curl-example.sh
```

### Node.js example
```javascript
const fs = require("node:fs/promises");

(async () => {
  const image = await fs.readFile("example_input.png")
  const body = {
    "image": image.toString("base64")
  }
  const res = await fetch(
    "http://127.0.0.1:5000/api/rmbg",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body)
    });
  const jsonResponse =  await res.json();
  const noBgImage = Buffer.from(jsonResponse.image, "base64");
  await fs.writeFile("example_output.png", noBgImage);
})();
```
Full code: [scripts/node-example.js](scripts/node-example.js)
```shell
IMAGE=my_image.jpg node node-example.js
```


