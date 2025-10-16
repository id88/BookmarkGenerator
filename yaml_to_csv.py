import yaml
import csv

def yaml_to_csv(yaml_file_path, csv_file_path):
    """
    将YAML书签文件转换为CSV格式
    
    Args:
        yaml_file_path (str): 输入的YAML文件路径
        csv_file_path (str): 输出的CSV文件路径
    """
    
    try:
        # 读取YAML文件
        with open(yaml_file_path, 'r', encoding='utf-8') as yaml_file:
            bookmarks_data = yaml.safe_load(yaml_file)
        
        # 准备CSV数据
        csv_data = []
        
        # 遍历所有分类和书签
        for category in bookmarks_data:
            category_name = category['category']
            
            for subcategory in category['subcategories']:
                subcategory_name = subcategory['name']
                
                for bookmark in subcategory['bookmarks']:
                    # 处理标签数组，转换为逗号分隔的字符串
                    tags_str = ', '.join(bookmark['tags'])
                    
                    # 构建CSV行数据
                    csv_row = {
                        '一级分类': category_name,
                        '二级分类': subcategory_name,
                        '网站名称': bookmark['name'],
                        '网址': bookmark['url'],
                        '图标URL': bookmark.get('icon', ''),
                        '标签': tags_str,
                        '简介': bookmark.get('description', '')
                    }
                    
                    csv_data.append(csv_row)
        
        # 写入CSV文件
        if csv_data:
            # 定义CSV列的顺序
            fieldnames = ['一级分类', '二级分类', '网站名称', '网址', '图标URL', '标签', '简介']
            
            with open(csv_file_path, 'w', newline='', encoding='utf-8-sig') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                
                # 写入表头
                writer.writeheader()
                
                # 写入数据行
                for row in csv_data:
                    writer.writerow(row)
            
            print(f"成功导出 {len(csv_data)} 条书签到 {csv_file_path}")
        else:
            print("未找到书签数据")
            
    except FileNotFoundError:
        print(f"错误：找不到YAML文件 {yaml_file_path}")
    except yaml.YAMLError as e:
        print(f"YAML解析错误：{e}")
    except KeyError as e:
        print(f"数据格式错误：缺少必要的键 {e}")
    except Exception as e:
        print(f"发生未知错误：{e}")

def main():
    """主函数"""
    # 文件路径配置
    yaml_file = 'bookmarks.yaml'  # 输入的YAML文件
    csv_file = 'bookmarks.csv'    # 输出的CSV文件
    
    # 执行转换
    yaml_to_csv(yaml_file, csv_file)

if __name__ == "__main__":
    main()