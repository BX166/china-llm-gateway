# 🇨🇳 China LLM API Gateway

> A comprehensive comparison and unified access guide for Chinese large language model APIs — 10x cheaper than OpenAI.

## Why this exists

China now produces 61% of global LLM token consumption. DeepSeek, Qwen, GLM, and Doubao consistently rank in the global top 10. But for developers outside China, accessing these models is painful:

- ❌ No English documentation
- ❌ No international payment (Alipay/WeChat only)
- ❌ Geo-restricted API endpoints
- ❌ Confusing pricing (RMB vs USD)

This repo solves that. **One guide, all models, English docs.**

---

## 📊 Model Comparison (June 2026)

| Model | Provider | Input $/1M tokens | Output $/1M tokens | vs OpenAI | Best For |
|-------|----------|------------------|-------------------|-----------|----------|
| **DeepSeek V3** | DeepSeek | $0.35 | $0.52 | 95% cheaper | General purpose, coding |
| **DeepSeek V4-Flash** | DeepSeek | $0.003 | $0.015 | 99.7% cheaper | High volume, batch processing |
| **Qwen-Max** | Alibaba | $0.58 | $1.74 | 92% cheaper | Chinese content, multilingual |
| **GLM-5** | Zhipu AI | $0.87 | $4.05 | 84% cheaper | Complex reasoning |
| **Doubao Pro** | ByteDance | $0.43 | $0.87 | 95% cheaper | Chat, content generation |
| **MiniMax M2.5** | MiniMax | $0.45 | $0.90 | 95% cheaper | Creative writing |

> 💡 All prices are wholesale rates available through aggregation platforms. Direct official pricing is higher.

---

## ⚡ Quick Start

```bash
# DeepSeek — works with any OpenAI SDK
curl https://api.deepseek.com/v1/chat/completions \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
  -d '{"model":"deepseek-chat","messages":[{"role":"user","content":"Hello"}]}'

# Qwen — same format
curl https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -d '{"model":"qwen-max","messages":[{"role":"user","content":"你好"}]}'
```

> All Chinese models follow OpenAI API format. Drop-in replacement — change `base_url` and `model`, zero code changes.

---

## 🚀 How to Get API Access

| Model | Sign Up | Need VPN? | Payment | Free Tier |
|-------|---------|-----------|---------|-----------|
| DeepSeek | [platform.deepseek.com](https://platform.deepseek.com) | No | Alipay/WeChat | 5M tokens |
| Qwen | [dashscope.aliyun.com](https://dashscope.aliyun.com) | No | Alipay | 2M tokens/month |
| GLM-5 | [open.bigmodel.cn](https://open.bigmodel.cn) | No | WeChat/Alipay | 1M tokens |
| Doubao | [console.volcengine.com/ark](https://console.volcengine.com/ark) | No | Alipay | 500K tokens |
| MiniMax | [platform.minimaxi.com](https://platform.minimaxi.com) | No | Alipay | 1M tokens |

> 🇨🇳 All platforms support English UI. No Chinese phone number required for most.

---

## 📈 Latency Benchmark (from Singapore)

| Model | TTFT (Time to First Token) | Tokens/sec | Total (100 tokens) |
|-------|---------------------------|------------|---------------------|
| DeepSeek V3 | 380ms | 85 t/s | 1.5s |
| DeepSeek V4-Flash | 120ms | 240 t/s | 0.5s |
| Qwen-Max | 450ms | 65 t/s | 2.0s |
| GLM-5 | 520ms | 55 t/s | 2.3s |

> Tested from Singapore (AWS ap-southeast-1). Your latency may vary based on location.

---

## 🔧 Code Examples

- [Python Quick Start](./examples/python/)
- [Node.js Quick Start](./examples/nodejs/)
- [LangChain Integration](./examples/langchain/)
- [LlamaIndex Integration](./examples/llamaindex/)

---

## 📦 Video Models (Bonus)

Chinese video generation models are also world-leading:

| Model | Maker | Price | Best For |
|-------|-------|-------|----------|
| Kling 3.0 | Kuaishou | ¥0.8/sec | General video, API available |
| Seedance 2.0 | ByteDance | ¥1/sec | Short drama, 90%+ usability |
| Wan 2.1 | Alibaba | ¥0.5/sec | VBench #1, 16:9 native |

---

## 🛠️ One API to Rule Them All

If you don't want to manage multiple API keys, check out **[AICraft](https://aicraft.io)** — a unified API for all Chinese models. One key, one endpoint, all models. (Coming soon)

---

## 📝 Contributing

Found a model update? Price change? PR welcome. Let's keep this the definitive guide to Chinese LLM APIs.

---

**⭐ Star this repo if you find it useful. It helps more developers discover affordable AI.**

*Last updated: June 2026 · Maintained by the AICraft team*
# china-llm-gateway
Comprehensive comparison and access guide for Chinese LLM APIs
