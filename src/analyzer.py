import json
import os
import re
import time

import requests
from dotenv import load_dotenv

load_dotenv()

LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://integrate.api.nvidia.com/v1")

MODEL = "deepseek-ai/deepseek-v4-pro"

SYSTEM_PROMPT = """You are a technical analyst. Analyze the given GitHub project and return ONLY valid JSON with exactly these fields:
- scenario: 1-2 sentences in Chinese describing the application scenario
- usage: 3-step quick start guide in Chinese, each step concise

Output ONLY raw JSON. No markdown fences, no backticks, no extra text."""


def _parse_json(content):
    content = content.strip()
    content = (
        content.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    )
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", content, re.DOTALL)
        if m:
            return json.loads(m.group(0))
        raise


def _call_llm_messages(messages, max_retries=4):
    for attempt in range(max_retries + 1):
        try:
            resp = requests.post(
                f"{LLM_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {LLM_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": MODEL,
                    "messages": messages,
                    "max_tokens": 512,
                },
                timeout=45,
            )
            if resp.status_code == 529:
                wait = 2 * (attempt + 1)
                time.sleep(wait)
                continue
            resp.raise_for_status()
            content = resp.json()["choices"][0]["message"]["content"].strip()
            return _parse_json(content)
        except Exception as e:
            if attempt == max_retries:
                return {
                    "scenario": "暂无法解析 (API超载)",
                    "usage": "1.访问项目主页 2.阅读README 3.按说明安装使用",
                }
            time.sleep(2)
    return {"scenario": "获取失败", "usage": "获取失败"}


def analyze_project(repo):
    user_msg = f"""Project Name: {repo["name"]}
Description: {repo["description"]}
Language: {repo["language"]}
Topics: {", ".join(repo["topics"][:5])}
Stars: {repo["stars"]}
Fork: {repo["forks"]}
README (excerpt): {repo["readme"][:2000]}"""
    return _call_llm_messages(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ]
    )
