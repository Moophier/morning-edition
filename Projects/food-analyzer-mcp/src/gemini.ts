interface FoodAnalysis {
  ingredients: string[];
  cooking_methods: string[];
  confidence: "high" | "medium" | "low";
}

const SYSTEM_PROMPT = `You are a professional chef and food analyst. Analyze this food photo and return:
1. All visible ingredients
2. Detailed cooking methods in Chinese (step by step)
3. Confidence level: high/medium/low

If OCR text is provided, use it as additional context (e.g. menu name, recipe text, ingredient labels).

Respond in JSON format: {"ingredients": [...], "cooking_methods": ["1. ...", "2. ..."], "confidence": "high"}.
If you cannot determine the food, return {"ingredients": [], "cooking_methods": ["无法识别"], "confidence": "low"}.`;

export async function analyzeFoodImage(
  imageBase64: string,
  ocrText: string,
  apiKey: string
): Promise<FoodAnalysis> {
  const promptParts: { text: string }[] = [
    { text: SYSTEM_PROMPT },
  ];

  if (ocrText) {
    promptParts.push({ text: `[OCR extracted text: ${ocrText}]` });
  }

  const requestBody = {
    contents: [
      {
        parts: [
          ...promptParts,
          {
            inline_data: {
              mime_type: "image/jpeg",
              data: imageBase64,
            },
          },
        ],
      },
    ],
    generation_config: {
      response_mime_type: "application/json",
    },
  };

  const response = await fetch(
    `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(requestBody),
    }
  );

  if (!response.ok) {
    throw new Error(`Gemini API error: ${response.status} ${await response.text()}`);
  }

  const data = (await response.json()) as {
    candidates: { content: { parts: { text: string }[] } }[];
  };

  const text = data.candidates?.[0]?.content?.parts?.[0]?.text || "";
  const cleaned = text.replace(/```json\n?/g, "").replace(/```/g, "").trim();

  try {
    return JSON.parse(cleaned) as FoodAnalysis;
  } catch {
    return { ingredients: [], cooking_methods: ["解析失败"], confidence: "low" };
  }
}