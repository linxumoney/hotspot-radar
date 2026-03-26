# 🔥 热搜雷达 · Hotspot Radar

> 每天 30 秒，搞定今天写什么。

微博 + 百度实时热搜抓取 × SEO 关键词评分，专为公众号/内容创作者设计的选题工具。

无需 API Key，无需注册账号，直接跑。

---

## ✨ 功能

- 📱 **微博热搜** — 实时热搜榜，抓取 TOP 30
- 🔍 **百度热搜** — 实时热词，抓取 TOP 30
- 📊 **SEO 评分** — 对目标关键词做搜索热度打分（0-10），帮你选搜索量更高的词
- 🎯 **一条命令搞定**，输出清晰，直接用于选题决策

---

## 🚀 快速开始

```bash
# 克隆
git clone https://github.com/linxumoney/hotspot-radar.git
cd hotspot-radar

# 直接运行（Python 3.8+，无需安装额外依赖）
python3 scripts/hotspot_radar.py
```

### 示例输出

```
=======================================================
  🔥 热搜雷达  2026-03-27 07:25
=======================================================

📱 微博热搜 TOP30
   1. 游客因拍照设备太专业被景区驱赶
   2. 美方被曝正酝酿对伊朗最后一击
   ...

📊 SEO 关键词评分（百度搜索热度）
  比特币          ██████████ 10/10  → 比特币今日最新 / ...
  加密货币投资       ██████████ 10/10  → 加密货币投资 / ...
  仓位管理         ██████████ 10/10  → 仓位管理是什么意思 / ...
```

---

## 📖 用法

```bash
# 默认：热搜 + 默认关键词评分
python3 scripts/hotspot_radar.py

# 自定义关键词
python3 scripts/hotspot_radar.py --keywords BTC暴跌 美国关税 比特币熊市

# 控制热搜条数
python3 scripts/hotspot_radar.py --limit 20

# JSON 格式输出（供下游程序解析）
python3 scripts/hotspot_radar.py --json
```

### 修改默认关键词

编辑 `scripts/hotspot_radar.py` 第 `DEFAULT_KEYWORDS` 行：

```python
DEFAULT_KEYWORDS = ["比特币", "加密货币投资", "仓位管理", "资产配置", "量化交易"]
```

---

## 🧠 工作原理

| 数据源 | 接口 | 说明 |
|--------|------|------|
| 微博热搜 | `weibo.com/ajax/side/hotSearch` | 网页端侧边栏接口，实时数据 |
| 百度热搜 | `top.baidu.com/api/board` | 百度热搜页接口，实时数据 |
| SEO 评分 | `suggestion.baidu.com/su` | 搜索建议词数量作为热度代理指标 |

所有接口均为公开接口，无需 API Key，模拟浏览器 User-Agent 访问。

---

## 🤖 与 AI 写作工具集成

本工具是 [OpenClaw](https://openclaw.ai) AgentSkill 格式，可直接被 AI Agent 调用：

1. 将目录放入 `~/.openclaw/workspace/skills/`
2. 对 Agent 说「给我看今天热搜」即可自动触发

---

## 📡 关注我

这是「**[林序聊AI · 开源计划](https://github.com/linxumoney)**」的第一个项目。我会持续开源更多 AI 内容创作工具。

| 平台 | 链接 |
|------|------|
| 🐦 X (Twitter) | [@linxumoney](https://x.com/linxumoney) |
| 📺 YouTube | [@LinXuMoney](https://www.youtube.com/@LinXuMoney) |
| 💻 GitHub | [github.com/linxumoney](https://github.com/linxumoney) |

觉得有用的话，**点个 Star ⭐ 支持一下**，让更多人发现这个工具。

---

## 📄 License

MIT License — 自由使用、修改、分发。
