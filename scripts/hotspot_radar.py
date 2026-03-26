#!/usr/bin/env python3
"""
每日热搜 + SEO 关键词评分工具

用法:
    python3 hotspot_radar.py                    # 抓热搜 + 对默认关键词评分
    python3 hotspot_radar.py --keywords k1 k2   # 对指定关键词评分
    python3 hotspot_radar.py --limit 20         # 热搜条数（默认30）
    python3 hotspot_radar.py --json             # 输出 JSON 格式
"""

import argparse
import json
import sys
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Optional

TIMEOUT = 10
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
}

# ── 热搜抓取 ──────────────────────────────────────────────────

def fetch_weibo(limit: int) -> List[Dict]:
    try:
        req = urllib.request.Request(
            "https://weibo.com/ajax/side/hotSearch",
            headers={**HEADERS, "Referer": "https://weibo.com/"},
        )
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            data = json.loads(r.read())
        items = []
        for entry in data.get("data", {}).get("realtime", [])[:limit]:
            note = entry.get("note", "")
            if note:
                items.append({
                    "title": note,
                    "source": "微博",
                    "hot": entry.get("num", 0),
                    "url": f"https://s.weibo.com/weibo?q=%23{urllib.parse.quote(note)}%23",
                })
        return items
    except Exception as e:
        print(f"[warn] 微博热搜失败: {e}", file=sys.stderr)
        return []


def fetch_baidu(limit: int) -> List[Dict]:
    try:
        req = urllib.request.Request(
            "https://top.baidu.com/api/board?platform=wise&tab=realtime",
            headers=HEADERS,
        )
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            data = json.loads(r.read())
        items = []
        for entry in data.get("data", {}).get("cards", [{}])[0].get("content", [])[:limit]:
            title = entry.get("word", "") or entry.get("query", "")
            if title:
                items.append({
                    "title": title,
                    "source": "百度",
                    "hot": entry.get("hotScore", 0),
                    "url": f"https://www.baidu.com/s?wd={urllib.parse.quote(title)}",
                })
        return items
    except Exception as e:
        print(f"[warn] 百度热搜失败: {e}", file=sys.stderr)
        return []


# ── SEO 评分 ──────────────────────────────────────────────────

def seo_score(keyword: str) -> dict:
    """用百度搜索建议数量代理搜索热度，返回评分和相关词。"""
    try:
        url = "https://suggestion.baidu.com/su?" + urllib.parse.urlencode(
            {"wd": keyword, "action": "opensearch", "ie": "utf-8"}
        )
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            data = json.loads(r.read())
        suggs = data[1] if isinstance(data, list) and len(data) >= 2 else []
        score = min(len(suggs), 10)
        return {"keyword": keyword, "score": score, "related": suggs[:5]}
    except Exception as e:
        return {"keyword": keyword, "score": 0, "related": [], "error": str(e)}


# ── 主程序 ────────────────────────────────────────────────────

DEFAULT_KEYWORDS = ["比特币", "加密货币投资", "仓位管理", "资产配置", "量化交易"]


def main():
    parser = argparse.ArgumentParser(description="每日热搜 + SEO 关键词雷达")
    parser.add_argument("--limit", type=int, default=30, help="热搜条数")
    parser.add_argument("--keywords", nargs="+", help="要评分的关键词（不填用默认）")
    parser.add_argument("--json", action="store_true", dest="json_output", help="JSON输出")
    args = parser.parse_args()

    # 抓热搜
    weibo = fetch_weibo(args.limit)
    baidu = fetch_baidu(args.limit)
    all_hotspots = weibo + baidu

    # SEO评分
    keywords = args.keywords or DEFAULT_KEYWORDS
    seo_results = [seo_score(kw) for kw in keywords]

    # 时间戳
    now = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M")

    if args.json_output:
        print(json.dumps({
            "fetched_at": now,
            "hotspots": all_hotspots,
            "seo": seo_results,
        }, ensure_ascii=False, indent=2))
        return

    # 人类可读输出
    print(f"\n{'='*55}")
    print(f"  🔥 热搜雷达  {now}")
    print(f"{'='*55}")

    if weibo:
        print(f"\n📱 微博热搜 TOP{min(len(weibo), args.limit)}")
        for i, item in enumerate(weibo[:args.limit], 1):
            print(f"  {i:2}. {item['title']}")

    if baidu:
        print(f"\n🔍 百度热搜 TOP{min(len(baidu), args.limit)}")
        for i, item in enumerate(baidu[:args.limit], 1):
            print(f"  {i:2}. {item['title']}")

    if not weibo and not baidu:
        print("\n⚠️  热搜抓取失败，请检查网络连接")

    print(f"\n{'─'*55}")
    print(f"  📊 SEO 关键词评分（百度搜索热度）")
    print(f"{'─'*55}")
    for r in seo_results:
        bar = "█" * r["score"] + "░" * (10 - r["score"])
        related = " / ".join(r["related"][:3]) if r["related"] else "无"
        print(f"  {r['keyword']:<12} {bar} {r['score']:2}/10  → {related}")

    print()


if __name__ == "__main__":
    main()
