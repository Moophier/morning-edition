import { McpServer, WebStandardStreamableHTTPServerTransport, fromJsonSchema } from "@modelcontextprotocol/server";
import { analyzeFood } from "./tools/analyze_food";

const server = new McpServer({
  name: "food-analyzer-mcp",
  version: "1.0.0",
});

type AnalyzeFoodInput = {
  image_url?: string;
  image_base64?: string;
};

const schema = fromJsonSchema<AnalyzeFoodInput>({
  type: "object",
  properties: {
    image_url: {
      type: "string",
      description: "食物图片的 URL。与 image_base64 二选一。",
    },
    image_base64: {
      type: "string",
      description: "Base64 编码的图片数据。与 image_url 二选一。",
    },
  },
});

server.registerTool(
  "analyze_food",
  {
    description:
      "上传食物照片，自动识别原料并返回烹饪方法。支持图片URL或Base64。先调用百度 OCR 提取图片中文字，再结合 Gemini 视觉分析。",
    inputSchema: schema,
  },
  async (input: AnalyzeFoodInput) => {
    return analyzeFood(input.image_url, input.image_base64);
  }
);

const transport = new WebStandardStreamableHTTPServerTransport({
  sessionIdGenerator: undefined,
});

await server.connect(transport);

export default {
  fetch: (request: Request) => transport.handleRequest(request),
};