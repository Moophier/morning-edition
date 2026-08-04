import { baiduOcr } from "../baidu_ocr";
import { analyzeFoodImage } from "../gemini";

function base64FromUrl(imageUrl: string): Promise<string> {
  if (imageUrl.startsWith("data:image/")) {
    return Promise.resolve(imageUrl.split(",")[1]);
  }
  return fetch(imageUrl)
    .then((r) => r.arrayBuffer())
    .then((buf) => btoa(String.fromCharCode(...new Uint8Array(buf))));
}

export async function analyzeFood(
  imageUrl?: string,
  imageBase64?: string
): Promise<{
  content: { type: "text"; text: string }[];
}> {
  const env = globalThis as unknown as Record<string, unknown>;
  const geminiKey = env.GEMINI_API_KEY as string;
  const baiduApiKey = env.BAIDU_OCR_API_KEY as string;
  const baiduSecret = env.BAIDU_OCR_SECRET_KEY as string;

  if (!imageUrl && !imageBase64) {
    return {
      content: [{ type: "text", text: "请提供 image_url 或 image_base64" }],
    };
  }

  const inputImage = imageBase64 || (await base64FromUrl(imageUrl!));

  let ocrText = "";
  try {
    ocrText = await baiduOcr(inputImage, baiduApiKey, baiduSecret);
  } catch {
    ocrText = "";
  }

  try {
    const analysis = await analyzeFoodImage(inputImage, ocrText, geminiKey);

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(
            {
              ingredients: analysis.ingredients,
              cooking_methods: analysis.cooking_methods,
              ocr_text: ocrText,
              confidence: analysis.confidence,
            },
            null,
            2
          ),
        },
      ],
    };
  } catch (e) {
    if (ocrText) {
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(
              {
                ingredients: [],
                cooking_methods: ["AI 分析失败，仅提取到图片文字"],
                ocr_text: ocrText,
                confidence: "low",
              },
              null,
              2
            ),
          },
        ],
      };
    }

    return {
      content: [
        {
          type: "text",
          text: `分析失败: ${(e as Error).message}`,
        },
      ],
    };
  }
}