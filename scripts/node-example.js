const fs = require("node:fs/promises");
const baseUrl = "http://127.0.0.1:5000";
const statusPath = "api/status";
const rmbgPath = "api/rmbg";
const imageFilePath = process.env.IMAGE || `${__dirname}/example_input.png`;
const statusUrl = new URL(statusPath, baseUrl).href;
const rmbgUrl = new URL(rmbgPath, baseUrl).href;


const status = async () => {
  try {
    console.log(statusUrl)
    const res = await fetch(
      statusUrl,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });
    console.log("Status Code:", res.status);
    // console.log(res);
    const status = await res.json();
    return(status)
  } catch (err) {
    console.error(err.message);
  }
};


const rmbg = async (image) => {
  try {
    console.log(rmbgUrl)
    const body = {
      "image": image.toString("base64")
    }
    const res = await fetch(
      rmbgUrl,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body)
      });
    console.log("Status Code:", res.status);
    return await res.json();
  } catch (err) {
    console.error(err);
  }
};



(async () => {
  let statusResponse = await status();
  console.log(statusResponse);

  const image = await fs.readFile(imageFilePath)
  let rmbgResponse = await rmbg(image);
  await fs.writeFile("example_output.json", JSON.stringify(rmbgResponse, null, 2));
  const noBgImage = Buffer.from(rmbgResponse.image, "base64");
  await fs.writeFile("example_output.png", noBgImage);
})();
