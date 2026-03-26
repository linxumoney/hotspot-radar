---
name: hotspot-radar
description: |
  每日热搜 + SEO 关键词评分工具。抓取微博/百度实时热搜榜，对指定关键词做搜索热度评分，
  辅助公众号/内容创作选题。
  触发词：热搜 / 今日热点 / 热词 / 选题参考 / SEO评分 / 关键词热度 / 热搜雷达
---

# 热搜雷达 Skill

## 脚本

```
scripts/hotspot_radar.py
```

Python 3.8+，无需第三方库，直接运行。

## 用法

```bash
# 抓微博+百度热搜 + 对默认关键词评分（比特币/加密货币投资/仓位管理/资产配置/量化交易）
python3 scripts/hotspot_radar.py

# 自定义关键词评分
python3 scripts/hotspot_radar.py --keywords BTC暴跌 美国关税 比特币熊市

# 控制热搜条数
python3 scripts/hotspot_radar.py --limit 20

# JSON 格式输出（供下游程序解析）
python3 scripts/hotspot_radar.py --json
```

## 工作原理

| 数据源 | 接口 | 说明 |
|--------|------|------|
| 微博热搜 | `weibo.com/ajax/side/hotSearch` | 实时热搜榜，无需登录 |
| 百度热搜 | `top.baidu.com/api/board` | 实时热词，无需登录 |
| SEO 评分 | `suggestion.baidu.com/su` | 搜索建议词数量代理搜索热度，满分10分 |

## 典型流程

1. 运行脚本，获取今日热搜 + 目标关键词 SEO 评分
2. 结合热搜话题 + 高分关键词，挑出最适合当天写作的选题
3. 将选题交给写文章技能生成文章

## 默认关键词

脚本内 `DEFAULT_KEYWORDS` 列表，可直接编辑修改：

```python
DEFAULT_KEYWORDS = ["比特币", "加密货币投资", "仓位管理", "资产配置", "量化交易"]
```
