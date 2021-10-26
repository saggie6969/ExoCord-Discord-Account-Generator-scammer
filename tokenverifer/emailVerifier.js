// import { Inbox } from "gmail-inbox";

const { Inbox } = require("gmail-inbox");
var HTMLParser = require("node-html-parser");
let axios = require("axios");
const Captcha = require("2captcha");
const fs = require("fs");

let proxies = fs
  .readFileSync("proxies.txt")
  .toString()
  .replace(/\r\n/g, "\n")
  .split("\n");

let verifier = async (mailToken) => {
  const solver = new Captcha.Solver("CAPTCHA KEY");

  try {
    let data;
    try {
      ({ data } = await solver.hcaptcha(
        "f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34",
        "https://discord.com/"
      ));
    } catch {
      ({ data } = await solver.hcaptcha(
        "f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34",
        "https://discord.com/"
      ));
    }
    let verify = await axios.post(
      "https://discord.com/api/v9/auth/verify",
      {
        captcha_key: data,
        token: mailToken,
      },
      {
        headers: {
          "content-type": "application/json",
          accept: "*/*",
          "accept-language": "it",
          "content-length": "2494",
          "content-type": "application/json",
          cookie:
            "__dcfduid=b869a603173111ec93fb42010a0a08eb; __sdcfduid=b869a603173111ec93fb42010a0a08eb3357755a7de89e44770dd66a95570c3c027fec30b341002eb04881e3aaebfacb; locale=it",
          origin: "https://discord.com",
          referer: "https://discord.com/verify",
          "sec-ch-ua":
            'Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93',
          "sec-ch-ua-mobile": "?0",
          "sec-ch-ua-platform": "Windows",
          "sec-fetch-dest": "empty",
          "sec-fetch-mode": "cors",
          "sec-fetch-site": "same-origin",
          "user-agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
          "x-debug-options": "bugReporterEnabled",
          "x-super-properties":
            "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzkzLjAuNDU3Ny44MiBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiOTMuMC40NTc3LjgyIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiJodHRwczovL2Rpc2NvcmQuY29tL2xvZ2luIiwicmVmZXJyaW5nX2RvbWFpbiI6ImRpc2NvcmQuY29tIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjk3NjYyLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==",
        },
      }
    );
    console.log(verify.data);
    fs.writeFileSync("pastaccs.txt", mailToken + "\n", { flag: "a+" });
  } catch (e) {
    console.log(e);
  }
};

async function verifyLatestMail() {
  let inbox = new Inbox("credentials.json");
  await inbox.authenticateAccount(); // logs user in

  let messages = await inbox.getLatestMessages();
  console.log(messages.length);

  for (message of messages) {
    const root = HTMLParser.parse(message.body.html);
    let link;
    try {
      link = root
        .querySelector("tr:nth-child(2) > td > table > tbody > tr > td > a")
        .rawAttrs.split('="')[1]
        .split('"')[0];
    } catch (e) {
      console.log("No new accs to verify!");
      return;
    }
    res = await axios.get(link);
    let mailToken = res.request.res.responseUrl.split("=")[1];
    if (fs.readFileSync("pastaccs.txt").includes(mailToken)) {
      console.log("No new accs to verify!");
      return;
    }

    if (!mailToken) return;
    console.log("Verifying " + mailToken);
    verifier(mailToken);
  }

  // console.log(messages[2].body.html);
}

// (async () => {
//   if (!fs.existsSync("gmail-token.json")) {
//     let inbox = new Inbox("credentials.json");
//     await inbox.authenticateAccount();
//   } else {
//     setInterval(() => {
//       try {
//         verifyLatestMail();
//       } catch {}
//     }, 2000);
//   }
// })();

verifyLatestMail();
