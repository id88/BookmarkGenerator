import csv
from collections import defaultdict

def csv_to_yaml(csv_file_path, yaml_file_path):
    """
    将CSV书签文件转换为YAML格式
    
    Args:
        csv_file_path (str): 输入的CSV文件路径
        yaml_file_path (str): 输出的YAML文件路径
    """
    
    try:
        # 读取CSV文件
        with open(csv_file_path, 'r', encoding='utf-8-sig') as csv_file:
            reader = csv.DictReader(csv_file)
            csv_data = list(reader)
        
        if not csv_data:
            print("CSV文件为空")
            return
        
        # 构建层级数据结构
        yaml_data = []
        
        # 使用嵌套的defaultdict来组织数据
        category_structure = defaultdict(lambda: defaultdict(list))
        
        for row in csv_data:
            category = row['一级分类'].strip()
            subcategory = row['二级分类'].strip()
            
            # 构建书签对象
            bookmark = {
                'name': row['网站名称'].strip(),
                'url': row['网址'].strip()
            }
            
            # 添加图标URL（如果存在且非空）
            icon_url = row.get('图标URL', '').strip()
            if icon_url:
                bookmark['icon'] = icon_url
            
            # 添加标签（如果存在且非空）
            tags_str = row.get('标签', '').strip()
            if tags_str:
                # 处理标签字符串，分割成列表并去除空格
                tags = [tag.strip() for tag in tags_str.split(',')]
                bookmark['tags'] = tags
            
            # 添加简介（如果存在且非空）
            description = row.get('简介', '').strip()
            if description:
                bookmark['description'] = description
            
            # 添加到数据结构中
            category_structure[category][subcategory].append(bookmark)
        
        # 转换为YAML所需的格式
        for category, subcategories in category_structure.items():
            category_data = {
                'category': category,
                'subcategories': []
            }
            
            for subcategory_name, bookmarks in subcategories.items():
                subcategory_data = {
                    'name': subcategory_name,
                    'bookmarks': bookmarks
                }
                category_data['subcategories'].append(subcategory_data)
            
            yaml_data.append(category_data)
        
        # 写入YAML文件，使用自定义格式器来获得更好的输出格式
        with open(yaml_file_path, 'w', encoding='utf-8') as yaml_file:
            yaml_file.write(generate_formatted_yaml(yaml_data))
        
        # 统计信息
        stats = {
            'categories': len(yaml_data),
            'subcategories': sum(len(cat['subcategories']) for cat in yaml_data),
            'bookmarks': sum(len(sub['bookmarks']) for cat in yaml_data for sub in cat['subcategories'])
        }
        
        print(f"转换完成！")
        print(f"统计信息：")
        print(f"  - 一级分类: {stats['categories']} 个")
        print(f"  - 二级分类: {stats['subcategories']} 个")
        print(f"  - 书签数量: {stats['bookmarks']} 个")
        print(f"  - 输出文件: {yaml_file_path}")
        
    except FileNotFoundError:
        print(f"错误：找不到CSV文件 {csv_file_path}")
    except KeyError as e:
        print(f"CSV文件格式错误：缺少必要的列 {e}")
    except Exception as e:
        print(f"发生未知错误：{e}")

def generate_formatted_yaml(data):
    """生成格式化的YAML内容"""
    lines = []
    
    for category in data:
        lines.append(f"- category: {category['category']}")
        lines.append("  subcategories:")
        
        for subcategory in category['subcategories']:
            lines.append(f"    - name: {subcategory['name']}")
            lines.append("      bookmarks:")
            
            for bookmark in subcategory['bookmarks']:
                lines.append(f"        - name: {bookmark['name']}")
                lines.append(f"          url: {bookmark['url']}")
                
                if 'icon' in bookmark:
                    lines.append(f"          icon: {bookmark['icon']}")
                
                if 'tags' in bookmark and bookmark['tags']:
                    # 格式化标签为数组格式
                    tags_str = ", ".join(bookmark['tags'])
                    lines.append(f"          tags: [{tags_str}]")
                
                if 'description' in bookmark:
                    lines.append(f"          description: {bookmark['description']}")
                
                # 在每个书签之间添加空行（除了最后一个）
                if bookmark != subcategory['bookmarks'][-1]:
                    lines.append("")
            
            # 在每个二级分类之间添加空行（除了最后一个）
            if subcategory != category['subcategories'][-1]:
                lines.append("")
        
        # 在每个一级分类之间添加空行（除了最后一个）
        if category != data[-1]:
            lines.append("")
    
    return "\n".join(lines)

def main():
    """主函数"""
    # 文件路径配置
    csv_file = 'bookmarks.csv'    # 输入的CSV文件
    yaml_file = 'bookmarks.yaml'  # 输出的YAML文件
    
    # 执行转换
    csv_to_yaml(csv_file, yaml_file)

if __name__ == "__main__":
    main()