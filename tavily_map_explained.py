"""
Understanding TavilyMap parameters and optimization for documentation ingestion
"""

def explain_tavily_map_parameters():
    """Explain what each TavilyMap parameter does"""

    print("=" * 80)
    print("🗺️ TAVILY MAP PARAMETERS EXPLAINED")
    print("=" * 80)

    print("🔧 YOUR CURRENT SETTINGS:")
    print("   TavilyMap(max_depth=5, max_breadth=20, max_pages=1000)")
    print()

    print("📊 PARAMETER BREAKDOWN:")
    print()

    print("1️⃣ max_depth=5 (How deep to crawl)")
    print("   • Starting URL = Depth 0")
    print("   • Links on starting page = Depth 1")
    print("   • Links on those pages = Depth 2")
    print("   • ... up to Depth 5")
    print()
    print("   Visual example:")
    print("   docs.langchain.com/")
    print("   ├── /intro (depth 1)")
    print("   │   ├── /intro/installation (depth 2)")
    print("   │   └── /intro/quickstart (depth 2)")
    print("   │       └── /intro/quickstart/examples (depth 3)")
    print("   └── /modules (depth 1)")
    print("       └── /modules/chains (depth 2)")
    print("           └── /modules/chains/advanced (depth 3)")

    print("\n2️⃣ max_breadth=20 (How many links per level)")
    print("   • At each depth level, follow up to 20 links")
    print("   • Helps avoid getting stuck on pages with hundreds of links")
    print("   • Prioritizes most relevant links first")
    print()
    print("   Example: If a page has 100 links, only follow the top 20")

    print("\n3️⃣ max_pages=1000 (Total page limit)")
    print("   • Maximum total pages to discover across all depths")
    print("   • Safety limit to prevent runaway crawling")
    print("   • Stops crawling when this limit is reached")
    print()
    print("   Math check: 5 depths × 20 breadth = up to 20^5 = 3.2M potential pages")
    print("   But max_pages=1000 caps it at 1000 pages total")

def analyze_current_settings():
    """Analyze whether current settings are optimal"""

    print("\n" + "=" * 80)
    print("🎯 ANALYZING YOUR CURRENT SETTINGS")
    print("=" * 80)

    settings = {
        "max_depth": 5,
        "max_breadth": 20,
        "max_pages": 1000
    }

    print("📊 ASSESSMENT:")

    print("\n🟡 max_depth=5 - MIGHT BE TOO DEEP")
    print("   • Documentation sites typically have 2-3 levels")
    print("   • Depth 5 might reach auxiliary pages (legal, contact, etc.)")
    print("   • Recommendation: Try 2-3 first, increase if needed")

    print("\n🟢 max_breadth=20 - GOOD FOR MOST SITES")
    print("   • Captures main sections without getting overwhelmed")
    print("   • Good balance between coverage and efficiency")
    print("   • 20 is reasonable for documentation sites")

    print("\n🟢 max_pages=1000 - REASONABLE SAFETY LIMIT")
    print("   • Large enough for comprehensive documentation")
    print("   • Small enough to prevent runaway crawling")
    print("   • Good starting point")

def site_specific_recommendations():
    """Provide site-specific recommendations"""

    print("\n" + "=" * 80)
    print("📚 SITE-SPECIFIC RECOMMENDATIONS")
    print("=" * 80)

    sites = {
        "Small Documentation Site": {
            "description": "Personal project docs, small libraries",
            "example": "FastAPI docs, Streamlit docs",
            "settings": "TavilyMap(max_depth=2, max_breadth=15, max_pages=200)",
            "reasoning": "Usually well-organized, 2 levels sufficient"
        },
        "Medium Documentation Site": {
            "description": "Framework docs, medium libraries",
            "example": "LangChain, OpenAI API docs",
            "settings": "TavilyMap(max_depth=3, max_breadth=20, max_pages=500)",
            "reasoning": "More comprehensive, but still structured"
        },
        "Large Documentation Site": {
            "description": "Large frameworks, comprehensive guides",
            "example": "Django, React, AWS docs",
            "settings": "TavilyMap(max_depth=4, max_breadth=25, max_pages=1000)",
            "reasoning": "Complex structure, multiple product areas"
        },
        "Your Current Settings": {
            "description": "Conservative approach for unknown sites",
            "example": "General purpose crawling",
            "settings": "TavilyMap(max_depth=5, max_breadth=20, max_pages=1000)",
            "reasoning": "Safe defaults, might be overkill for some sites"
        }
    }

    for site_type, config in sites.items():
        print(f"\n🎯 {site_type.upper()}:")
        print(f"   Description: {config['description']}")
        print(f"   Example: {config['example']}")
        print(f"   Settings: {config['settings']}")
        print(f"   Reasoning: {config['reasoning']}")

def crawling_strategy_tips():
    """Provide crawling strategy tips"""

    print("\n" + "=" * 80)
    print("💡 CRAWLING STRATEGY TIPS")
    print("=" * 80)

    print("🚀 OPTIMIZATION STRATEGIES:")

    print("\n1️⃣ Start Conservative, Then Expand")
    print("   # Phase 1: Quick exploration")
    print("   tavily_map_quick = TavilyMap(max_depth=2, max_breadth=10, max_pages=100)")
    print("   quick_results = tavily_map_quick.run('https://docs.example.com')")
    print("   # Analyze results, then decide if you need more depth")

    print("\n2️⃣ Site-Specific Configuration")
    print("   site_configs = {")
    print("       'docs.langchain.com': {'depth': 3, 'breadth': 25, 'pages': 800},")
    print("       'docs.openai.com': {'depth': 2, 'breadth': 15, 'pages': 300},")
    print("       'docs.python.org': {'depth': 4, 'breadth': 30, 'pages': 1200}")
    print("   }")

    print("\n3️⃣ Progressive Crawling")
    print("   # Crawl in stages to avoid overwhelming servers")
    print("   for depth in [1, 2, 3]:")
    print("       tavily_map = TavilyMap(max_depth=depth, max_breadth=20, max_pages=200)")
    print("       results = tavily_map.run(url)")
    print("       if len(results) < 50:  # Not finding much new")
    print("           break")

    print("\n4️⃣ Monitor and Adjust")
    print("   # Check what you're actually getting")
    print("   results = tavily_map.run(url)")
    print("   print(f'Found {len(results)} pages')")
    print("   # Look at URL patterns to see if depth is appropriate")
    print("   for url in results[:10]:")
    print("       depth = url.count('/') - 2  # Estimate depth")
    print("       print(f'Depth ~{depth}: {url}')")

def performance_considerations():
    """Discuss performance implications"""

    print("\n" + "=" * 80)
    print("⚡ PERFORMANCE CONSIDERATIONS")
    print("=" * 80)

    print("📊 TIME & RESOURCE IMPACT:")

    print("\n🕒 Crawling Time Estimates:")
    print("   • Shallow (depth=2, breadth=10): 30 seconds - 2 minutes")
    print("   • Medium (depth=3, breadth=20): 2-10 minutes")
    print("   • Deep (depth=5, breadth=20): 10-30 minutes")
    print("   • Your settings: Potentially 10-30 minutes")

    print("\n💰 API Cost Considerations:")
    print("   • Each page discovery counts toward Tavily API usage")
    print("   • More pages = higher costs")
    print("   • Balance thoroughness vs. cost")

    print("\n🎯 Optimization Tips:")
    print("   • Start with smaller limits for testing")
    print("   • Use site-specific configurations")
    print("   • Monitor actual pages found vs. limits set")
    print("   • Consider crawling in batches during off-peak hours")

def recommended_adjustments():
    """Provide specific recommendations for your use case"""

    print("\n" + "=" * 80)
    print("🎯 RECOMMENDED ADJUSTMENTS FOR YOUR PROJECT")
    print("=" * 80)

    print("📚 FOR DOCUMENTATION INGESTION:")

    print("\n🥇 RECOMMENDED (More Efficient):")
    print("   tavily_map = TavilyMap(max_depth=3, max_breadth=20, max_pages=500)")
    print("   Reasoning:")
    print("   • Most docs sites have 2-3 meaningful levels")
    print("   • 500 pages covers most documentation sites")
    print("   • Faster crawling, lower API costs")

    print("\n🥈 ALTERNATIVE (Balanced):")
    print("   tavily_map = TavilyMap(max_depth=4, max_breadth=15, max_pages=600)")
    print("   Reasoning:")
    print("   • Slightly deeper for complex sites")
    print("   • Narrower breadth to focus on main content")
    print("   • Good for mixed site types")

    print("\n🥉 YOUR CURRENT (Conservative):")
    print("   tavily_map = TavilyMap(max_depth=5, max_breadth=20, max_pages=1000)")
    print("   Reasoning:")
    print("   • Safe for unknown site structures")
    print("   • Might be overkill for typical documentation")
    print("   • Higher API usage and time")

    print("\n💡 TESTING APPROACH:")
    print("   # Start with recommended settings")
    print("   tavily_map_test = TavilyMap(max_depth=2, max_breadth=10, max_pages=50)")
    print("   test_results = tavily_map_test.run('https://docs.langchain.com')")
    print("   print(f'Test found {len(test_results)} pages')")
    print("   # If you need more coverage, gradually increase limits")

def main():
    """Run all explanations"""

    print("🗺️ TAVILY MAP CONFIGURATION GUIDE")
    print("Optimizing your documentation crawling settings")

    explain_tavily_map_parameters()
    analyze_current_settings()
    site_specific_recommendations()
    crawling_strategy_tips()
    performance_considerations()
    recommended_adjustments()

    print("\n" + "=" * 80)
    print("🎯 QUICK DECISION GUIDE")
    print("=" * 80)
    print("🔥 For most documentation sites:")
    print("   TavilyMap(max_depth=3, max_breadth=20, max_pages=500)")
    print()
    print("🧪 For initial testing:")
    print("   TavilyMap(max_depth=2, max_breadth=10, max_pages=100)")
    print()
    print("🏗️ For comprehensive crawling:")
    print("   TavilyMap(max_depth=4, max_breadth=25, max_pages=800)")
    print()
    print("Your current settings are conservative and safe,")
    print("but you might get better efficiency with lower values! 🚀")

if __name__ == "__main__":
    main()