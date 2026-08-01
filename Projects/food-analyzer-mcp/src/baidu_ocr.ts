interface BaiduOcrResult {
  words_result: { words: string }[];
  words_result_num: number;
}

interface BaiduTokenResponse {
  access_token: string;
  expires_in: number;
}

let cachedToken: string | null = null;
let tokenExpiresAt: number = 0;

async function getAccessToken(apiKey: string, secretKey: string): Promise<string> {
  if (cachedToken && Date.now() < tokenExpiresAt) {
    return cachedToken;
  }

  const response = await fetch(
    `https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=${apiKey}&client_secret=${secretKey}`,
    { method: "POST" }
  );

  const data = (await response.json()) as BaiduTokenResponse;
  cachedToken = data.access_token;
  tokenExpiresAt = Date.now() + (data.expires_in - 60) * 1000;
  return cachedToken;
}

export async function baiduOcr(
  imageBase64: string,
  apiKey: string,
  secretKey: string
): Promise<string> {
  const token = await getAccessToken(apiKey, secretKey);

  const params = new URLSearchParams();
  params.append("image", imageBase64);
  params.append("language_type", "CHN_ENG");

  const response = await fetch(
    `https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token=${token}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: params.toString(),
    }
  );

  const data = (await response.json()) as BaiduOcrResult;

  if (!data.words_result_num) {
    return "";
  }

  return data.words_result.map((w) => w.words).join("，");
}