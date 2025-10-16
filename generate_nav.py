#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
书签导航网站生成器
读取YAML格式的书签文件,生成van-nav风格的导航网站
"""

import yaml
from pathlib import Path
from datetime import datetime


def load_bookmarks(yaml_file):
    """加载YAML书签文件"""
    with open(yaml_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def count_bookmarks(data):
    """统计书签总数"""
    total = 0
    for category in data:
        for subcategory in category.get('subcategories', []):
            total += len(subcategory.get('bookmarks', []))
    return total


def generate_html(bookmarks_data, output_file='index.html'):
    """生成HTML导航页面"""
    
    total_bookmarks = count_bookmarks(bookmarks_data)
    total_categories = len(bookmarks_data)
    total_subcategories = sum(len(cat.get('subcategories', [])) for cat in bookmarks_data)
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>我的书签导航</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        :root {{
            --bg-primary: #f5f7fa;
            --bg-secondary: #ffffff;
            --bg-card: #ffffff;
            --text-primary: #2c3e50;
            --text-secondary: #606266;
            --text-muted: #909399;
            --border-color: #e4e7ed;
            --accent-color: #409eff;
            --accent-hover: #66b1ff;
            --tag-bg: #ecf5ff;
            --tag-text: #409eff;
            --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.08);
            --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.12);
        }}

        [data-theme="dark"] {{
            --bg-primary: #1a1a1a;
            --bg-secondary: #2d2d2d;
            --bg-card: #2d2d2d;
            --text-primary: #e8e8e8;
            --text-secondary: #b8b8b8;
            --text-muted: #888888;
            --border-color: #404040;
            --accent-color: #409eff;
            --accent-hover: #66b1ff;
            --tag-bg: #1e3a5f;
            --tag-text: #66b1ff;
            --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.3);
            --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.4);
            --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.5);
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            transition: background 0.3s ease, color 0.3s ease;
        }}

        .header {{
            background: var(--bg-secondary);
            padding: 1.25rem 0;
            box-shadow: var(--shadow-sm);
            position: sticky;
            top: 0;
            z-index: 100;
            transition: background 0.3s ease;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 2rem;
        }}

        .header-content {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .header h1 {{
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--text-primary);
        }}

        .header-stats {{
            display: flex;
            gap: 1.5rem;
            align-items: center;
        }}

        .stat-item {{
            text-align: center;
        }}

        .stat-value {{
            font-size: 1.125rem;
            font-weight: 600;
            color: var(--accent-color);
        }}

        .stat-label {{
            font-size: 0.75rem;
            color: var(--text-muted);
            margin-top: 0.25rem;
        }}

        .theme-toggle {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 0.5rem 1rem;
            cursor: pointer;
            font-size: 1.5rem;
            transition: all 0.3s ease;
        }}

        .theme-toggle:hover {{
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }}

        .search-bar {{
            background: var(--bg-secondary);
            padding: 1rem 0;
            border-bottom: 1px solid var(--border-color);
        }}

        .search-input {{
            width: 100%;
            padding: 0.625rem 1rem;
            font-size: 0.875rem;
            border: 2px solid var(--border-color);
            border-radius: 8px;
            background: var(--bg-card);
            color: var(--text-primary);
            transition: all 0.3s ease;
        }}

        .search-input:focus {{
            outline: none;
            border-color: var(--accent-color);
            box-shadow: 0 0 0 3px rgba(64, 158, 255, 0.1);
        }}

        .category-nav {{
            background: var(--bg-secondary);
            padding: 1rem 0;
            border-bottom: 1px solid var(--border-color);
        }}

        .category-tabs {{
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
            margin-bottom: 0;
        }}

        .category-tab {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 0.4rem 0.875rem;
            cursor: pointer;
            font-size: 0.8125rem;
            font-weight: 500;
            color: var(--text-secondary);
            transition: all 0.2s ease;
            white-space: nowrap;
        }}

        .category-tab:hover {{
            background: var(--tag-bg);
            color: var(--accent-color);
            border-color: var(--accent-color);
        }}

        .category-tab.active {{
            background: var(--accent-color);
            color: white;
            border-color: var(--accent-color);
        }}

        .subcategory-tabs {{
            display: none;
            gap: 0.5rem;
            flex-wrap: wrap;
            margin-top: 0.75rem;
            padding-top: 0.75rem;
            border-top: 1px solid var(--border-color);
        }}

        .subcategory-tabs.active {{
            display: flex;
        }}

        .subcategory-tab {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 0.3rem 0.625rem;
            cursor: pointer;
            font-size: 0.75rem;
            color: var(--text-secondary);
            transition: all 0.2s ease;
            white-space: nowrap;
        }}

        .subcategory-tab:hover {{
            background: var(--tag-bg);
            color: var(--accent-color);
            border-color: var(--accent-color);
        }}

        .subcategory-tab.active {{
            background: var(--tag-bg);
            color: var(--accent-color);
            border-color: var(--accent-color);
            font-weight: 500;
        }}

        .main-content {{
            padding: 1.5rem 0;
        }}

        .category {{
            margin-bottom: 2rem;
        }}

        .category-title {{
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid var(--accent-color);
            color: var(--text-primary);
        }}

        .subcategory {{
            margin-bottom: 1.5rem;
        }}

        .subcategory-title {{
            font-size: 1rem;
            font-weight: 500;
            margin-bottom: 0.75rem;
            color: var(--text-secondary);
            display: flex;
            align-items: center;
        }}

        .subcategory-title::before {{
            content: "";
            width: 3px;
            height: 1rem;
            background: var(--accent-color);
            margin-right: 0.5rem;
            border-radius: 2px;
        }}

        .bookmarks-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 1rem;
        }}

        .bookmark-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1rem;
            transition: all 0.3s ease;
            cursor: pointer;
            text-decoration: none;
            display: block;
            height: 100%;
        }}

        .bookmark-card:hover {{
            transform: translateY(-4px);
            box-shadow: var(--shadow-lg);
            border-color: var(--accent-color);
        }}

        .bookmark-header {{
            display: flex;
            align-items: center;
            margin-bottom: 0.75rem;
        }}

        .bookmark-icon {{
            width: 32px;
            height: 32px;
            border-radius: 6px;
            margin-right: 0.75rem;
            object-fit: cover;
            background: var(--bg-primary);
            padding: 0.375rem;
        }}

        .bookmark-icon-fallback {{
            width: 32px;
            height: 32px;
            border-radius: 6px;
            margin-right: 0.75rem;
            background: linear-gradient(135deg, var(--accent-color), var(--accent-hover));
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1rem;
            font-weight: 600;
            color: white;
        }}

        .bookmark-name {{
            font-size: 0.9375rem;
            font-weight: 600;
            color: var(--text-primary);
            margin: 0;
        }}

        .bookmark-description {{
            font-size: 0.8125rem;
            color: var(--text-secondary);
            margin-bottom: 0.75rem;
            line-height: 1.4;
        }}

        .bookmark-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.375rem;
        }}

        .tag {{
            background: var(--tag-bg);
            color: var(--tag-text);
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-size: 0.6875rem;
            font-weight: 500;
        }}

        .no-results {{
            text-align: center;
            padding: 3rem 2rem;
            color: var(--text-muted);
        }}

        .no-results-icon {{
            font-size: 3rem;
            margin-bottom: 0.75rem;
        }}

        .no-results-text {{
            font-size: 1rem;
        }}

        .footer {{
            background: var(--bg-secondary);
            padding: 2rem 0;
            margin-top: 4rem;
            text-align: center;
            color: var(--text-muted);
            border-top: 1px solid var(--border-color);
        }}

        @media (max-width: 768px) {{
            .header-stats {{
                gap: 1rem;
            }}

            .stat-value {{
                font-size: 1.25rem;
            }}

            .bookmarks-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <header class="header">
        <div class="container">
            <div class="header-content">
                <h1>📚 我的书签导航</h1>
                <div class="header-stats">
                    <div class="stat-item">
                        <div class="stat-value">{total_bookmarks}</div>
                        <div class="stat-label">书签</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{total_categories}</div>
                        <div class="stat-label">分类</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{total_subcategories}</div>
                        <div class="stat-label">子分类</div>
                    </div>
                    <button class="theme-toggle" id="themeToggle" title="切换主题">
                        <span class="theme-icon">🌙</span>
                    </button>
                </div>
            </div>
        </div>
    </header>

    <div class="search-bar">
        <div class="container">
            <input 
                type="text" 
                class="search-input" 
                id="searchInput" 
                placeholder="🔍 搜索书签名称或标签..."
            >
        </div>
    </div>

    <nav class="category-nav">
        <div class="container">
            <div class="category-tabs" id="categoryTabs">
                <button class="category-tab active" data-category="all">全部</button>
'''

    # 生成一级分类标签和二级分类标签
    for category in bookmarks_data:
        category_name = category.get('category', '未分类')
        html += f'''                <button class="category-tab" data-category="{category_name}">{category_name}</button>
'''
    
    html += '''            </div>
'''
    
    # 为每个一级分类生成对应的二级分类标签容器
    for category in bookmarks_data:
        category_name = category.get('category', '未分类')
        subcategories = category.get('subcategories', [])
        
        html += f'''            <div class="subcategory-tabs" id="subcategory-{category_name}" data-parent="{category_name}">
                <button class="subcategory-tab active" data-subcategory="all" data-parent="{category_name}">全部</button>
'''
        
        for subcategory in subcategories:
            subcategory_name = subcategory.get('name', '未命名')
            html += f'''                <button class="subcategory-tab" data-subcategory="{subcategory_name}" data-parent="{category_name}">{subcategory_name}</button>
'''
        
        html += '''            </div>
'''
    
    html += '''        </div>
    </nav>

    <main class="main-content">
        <div class="container" id="bookmarksContainer">
'''

    # 生成书签内容
    for category in bookmarks_data:
        category_name = category.get('category', '未分类')
        html += f'''
            <section class="category" data-category="{category_name}">
                <h2 class="category-title">{category_name}</h2>
'''
        
        for subcategory in category.get('subcategories', []):
            subcategory_name = subcategory.get('name', '未命名')
            html += f'''
                <div class="subcategory" data-subcategory="{subcategory_name}">
                    <h3 class="subcategory-title">{subcategory_name}</h3>
                    <div class="bookmarks-grid">
'''
            
            for bookmark in subcategory.get('bookmarks', []):
                name = bookmark.get('name', '未命名网站')
                url = bookmark.get('url', '#')
                icon = bookmark.get('icon', '')
                description = bookmark.get('description', '')
                tags = bookmark.get('tags', [])
                
                # 生成首字母作为fallback图标
                initial = name[0].upper() if name else '?'
                
                tags_html = ''.join([f'<span class="tag">{tag}</span>' for tag in tags])
                
                html += f'''
                        <a href="{url}" class="bookmark-card" target="_blank" rel="noopener noreferrer"
                           data-name="{name.lower()}" 
                           data-tags="{' '.join([tag.lower() for tag in tags])}"
                           data-description="{description.lower()}">
                            <div class="bookmark-header">
'''
                
                if icon:
                    html += f'''
                                <img src="{icon}" alt="{name}" class="bookmark-icon" 
                                     onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                                <div class="bookmark-icon-fallback" style="display:none;">{initial}</div>
'''
                else:
                    html += f'''
                                <div class="bookmark-icon-fallback">{initial}</div>
'''
                
                html += f'''
                                <h4 class="bookmark-name">{name}</h4>
                            </div>
'''
                
                if description:
                    html += f'''
                            <p class="bookmark-description">{description}</p>
'''
                
                if tags:
                    html += f'''
                            <div class="bookmark-tags">
                                {tags_html}
                            </div>
'''
                
                html += '''
                        </a>
'''
            
            html += '''
                    </div>
                </div>
'''
        
        html += '''
            </section>
'''

    # 生成页脚和JavaScript
    current_year = datetime.now().year
    html += f'''
        </div>

        <div id="noResults" class="no-results" style="display: none;">
            <div class="no-results-icon">🔍</div>
            <div class="no-results-text">没有找到匹配的书签</div>
        </div>
    </main>

    <footer class="footer">
        <div class="container">
            <p>© {current_year} 我的书签导航 | 共收录 {total_bookmarks} 个优质网站</p>
        </div>
    </footer>

    <script>
        // 主题切换功能
        const themeToggle = document.getElementById('themeToggle');
        const themeIcon = document.querySelector('.theme-icon');
        const html = document.documentElement;

        // 从本地存储加载主题
        const savedTheme = localStorage.getItem('theme') || 'light';
        html.setAttribute('data-theme', savedTheme);
        updateThemeIcon(savedTheme);

        themeToggle.addEventListener('click', () => {{
            const currentTheme = html.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            html.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcon(newTheme);
        }});

        function updateThemeIcon(theme) {{
            themeIcon.textContent = theme === 'light' ? '🌙' : '☀️';
        }}

        // 分类导航功能
        let currentCategory = 'all';
        let currentSubcategory = 'all';

        const categoryTabs = document.querySelectorAll('.category-tab');
        const subcategoryTabContainers = document.querySelectorAll('.subcategory-tabs');

        // 一级分类点击事件
        categoryTabs.forEach(tab => {{
            tab.addEventListener('click', () => {{
                const categoryName = tab.getAttribute('data-category');
                
                // 更新当前分类
                currentCategory = categoryName;
                currentSubcategory = 'all';
                
                // 更新一级分类标签样式
                categoryTabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                
                // 显示/隐藏对应的二级分类
                subcategoryTabContainers.forEach(container => {{
                    container.classList.remove('active');
                    // 重置二级分类选中状态
                    const subTabs = container.querySelectorAll('.subcategory-tab');
                    subTabs.forEach(st => st.classList.remove('active'));
                    subTabs[0]?.classList.add('active');
                }});
                
                if (categoryName !== 'all') {{
                    const subcategoryContainer = document.getElementById(`subcategory-${{categoryName}}`);
                    if (subcategoryContainer) {{
                        subcategoryContainer.classList.add('active');
                    }}
                }}
                
                // 清空搜索框
                searchInput.value = '';
                
                // 筛选显示书签
                filterBookmarks();
            }});
        }});

        // 二级分类点击事件
        const subcategoryTabs = document.querySelectorAll('.subcategory-tab');
        subcategoryTabs.forEach(tab => {{
            tab.addEventListener('click', () => {{
                const subcategoryName = tab.getAttribute('data-subcategory');
                const parentCategory = tab.getAttribute('data-parent');
                
                // 更新当前子分类
                currentSubcategory = subcategoryName;
                
                // 更新同一父分类下的二级分类标签样式
                const container = document.getElementById(`subcategory-${{parentCategory}}`);
                if (container) {{
                    const siblingTabs = container.querySelectorAll('.subcategory-tab');
                    siblingTabs.forEach(t => t.classList.remove('active'));
                }}
                tab.classList.add('active');
                
                // 清空搜索框
                searchInput.value = '';
                
                // 筛选显示书签
                filterBookmarks();
            }});
        }});

        // 筛选书签函数
        function filterBookmarks() {{
            const categories = document.querySelectorAll('.category');
            const subcategories = document.querySelectorAll('.subcategory');
            const cards = document.querySelectorAll('.bookmark-card');
            
            let visibleCount = 0;
            
            // 隐藏所有内容
            categories.forEach(cat => cat.style.display = 'none');
            subcategories.forEach(sub => sub.style.display = 'none');
            cards.forEach(card => card.style.display = 'none');
            
            if (currentCategory === 'all') {{
                // 显示所有内容
                categories.forEach(cat => cat.style.display = 'block');
                subcategories.forEach(sub => sub.style.display = 'block');
                cards.forEach(card => {{
                    card.style.display = 'block';
                    visibleCount++;
                }});
            }} else {{
                // 显示指定分类
                categories.forEach(cat => {{
                    const catName = cat.getAttribute('data-category');
                    if (catName === currentCategory) {{
                        cat.style.display = 'block';
                        
                        // 显示该分类下的子分类和书签
                        const catSubcategories = cat.querySelectorAll('.subcategory');
                        catSubcategories.forEach(sub => {{
                            const subName = sub.getAttribute('data-subcategory');
                            
                            if (currentSubcategory === 'all' || subName === currentSubcategory) {{
                                sub.style.display = 'block';
                                
                                // 显示该子分类下的所有书签
                                const subCards = sub.querySelectorAll('.bookmark-card');
                                subCards.forEach(card => {{
                                    card.style.display = 'block';
                                    visibleCount++;
                                }});
                            }}
                        }});
                    }}
                }});
            }}
            
            // 显示/隐藏"无结果"提示
            if (visibleCount === 0) {{
                bookmarksContainer.style.display = 'none';
                noResults.style.display = 'block';
            }} else {{
                bookmarksContainer.style.display = 'block';
                noResults.style.display = 'none';
            }}
        }}

        // 搜索过滤功能
        const searchInput = document.getElementById('searchInput');
        const bookmarksContainer = document.getElementById('bookmarksContainer');
        const noResults = document.getElementById('noResults');

        searchInput.addEventListener('input', (e) => {{
            const searchTerm = e.target.value.toLowerCase().trim();
            
            if (searchTerm === '') {{
                // 如果有分类筛选,则应用分类筛选,否则显示所有内容
                if (currentCategory !== 'all') {{
                    filterBookmarks();
                }} else {{
                    showAllBookmarks();
                }}
                return;
            }}
            
            // 搜索时重置分类选择为"全部"
            currentCategory = 'all';
            currentSubcategory = 'all';
            categoryTabs.forEach(t => t.classList.remove('active'));
            categoryTabs[0]?.classList.add('active');
            subcategoryTabContainers.forEach(container => container.classList.remove('active'));

            const cards = document.querySelectorAll('.bookmark-card');
            const categories = document.querySelectorAll('.category');
            const subcategories = document.querySelectorAll('.subcategory');
            
            let visibleCount = 0;

            // 隐藏所有分类和子分类
            categories.forEach(cat => cat.style.display = 'none');
            subcategories.forEach(sub => sub.style.display = 'none');

            // 检查每个书签卡片
            cards.forEach(card => {{
                const name = card.getAttribute('data-name') || '';
                const tags = card.getAttribute('data-tags') || '';
                const description = card.getAttribute('data-description') || '';
                
                const matches = name.includes(searchTerm) || 
                               tags.includes(searchTerm) || 
                               description.includes(searchTerm);

                if (matches) {{
                    card.style.display = 'block';
                    visibleCount++;
                    
                    // 显示父级分类和子分类
                    const subcategory = card.closest('.subcategory');
                    const category = card.closest('.category');
                    if (subcategory) subcategory.style.display = 'block';
                    if (category) category.style.display = 'block';
                }} else {{
                    card.style.display = 'none';
                }}
            }});

            // 显示/隐藏"无结果"提示
            if (visibleCount === 0) {{
                bookmarksContainer.style.display = 'none';
                noResults.style.display = 'block';
            }} else {{
                bookmarksContainer.style.display = 'block';
                noResults.style.display = 'none';
            }}
        }});

        function showAllBookmarks() {{
            const cards = document.querySelectorAll('.bookmark-card');
            const categories = document.querySelectorAll('.category');
            const subcategories = document.querySelectorAll('.subcategory');
            
            cards.forEach(card => card.style.display = 'block');
            categories.forEach(cat => cat.style.display = 'block');
            subcategories.forEach(sub => sub.style.display = 'block');
            
            bookmarksContainer.style.display = 'block';
            noResults.style.display = 'none';
        }}

        // 添加键盘快捷键
        document.addEventListener('keydown', (e) => {{
            // Ctrl/Cmd + K 聚焦搜索框
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {{
                e.preventDefault();
                searchInput.focus();
            }}
            
            // ESC 清空搜索
            if (e.key === 'Escape' && document.activeElement === searchInput) {{
                searchInput.value = '';
                searchInput.dispatchEvent(new Event('input'));
            }}
        }});

        // 页面加载动画
        window.addEventListener('load', () => {{
            document.body.style.opacity = '0';
            document.body.style.transition = 'opacity 0.3s ease';
            setTimeout(() => {{
                document.body.style.opacity = '1';
            }}, 10);
        }});
    </script>
</body>
</html>
'''

    # 写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ HTML文件已生成: {output_file}")
    print(f"📊 统计信息:")
    print(f"   - 书签总数: {total_bookmarks}")
    print(f"   - 一级分类: {total_categories}")
    print(f"   - 二级分类: {total_subcategories}")


def main():
    """主函数"""
    # 定义文件路径
    yaml_file = 'bookmarks.yaml'
    output_file = 'index.html'
    
    # 检查YAML文件是否存在
    if not Path(yaml_file).exists():
        print(f"❌ 错误: 找不到文件 {yaml_file}")
        return
    
    try:
        # 加载书签数据
        print(f"📖 正在读取 {yaml_file}...")
        bookmarks_data = load_bookmarks(yaml_file)
        
        # 生成HTML
        print(f"🚀 正在生成导航网站...")
        generate_html(bookmarks_data, output_file)
        
        print(f"\n🎉 完成! 请在浏览器中打开 {output_file} 查看效果")
        
    except Exception as e:
        print(f"❌ 发生错误: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()

