# 📚 书签导航网站生成器

一个基于Python的书签管理系统，可以将YAML格式的书签数据转换为美观的导航网站，支持CSV和YAML格式之间的相互转换。

## ✨ 功能特性

### 🎨 导航网站生成
- **现代化设计**: 采用van-nav风格的卡片布局，支持明暗主题切换
- **响应式布局**: 自适应不同屏幕尺寸，移动端友好
- **智能搜索**: 支持按书签名称、标签、描述进行实时搜索
- **分类导航**: 一级分类和二级分类的层级导航，点击筛选显示
- **统计信息**: 显示书签总数、分类数量等统计信息
- **图标支持**: 自动加载网站图标，失败时显示首字母fallback

### 🔄 格式转换
- **YAML ↔ CSV**: 支持YAML和CSV格式之间的双向转换
- **数据完整性**: 保持所有书签信息（名称、URL、图标、标签、描述）
- **批量处理**: 一次性处理大量书签数据

## 📁 项目结构

```
BookmarkGenerator/
├── bookmarks.yaml          # 书签数据文件（YAML格式）
├── bookmarks.csv           # 书签数据文件（CSV格式）
├── generate_nav.py         # 导航网站生成器
├── yaml_to_csv.py         # YAML转CSV工具
├── csv_to_yaml.py         # CSV转YAML工具
├── requirements.txt        # Python依赖包
└── index.html             # 生成的导航网站
```

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone https://github.com/id88/BookmarkGenerator
cd BookmarkGenerator

# 安装依赖
pip install -r requirements.txt
```

### 2. 生成导航网站

```bash
# 从YAML文件生成导航网站
python generate_nav.py
```

生成的`index.html`文件可以直接在浏览器中打开使用。

### 3. 格式转换

```bash
# YAML转CSV
python yaml_to_csv.py

# CSV转YAML
python csv_to_yaml.py
```

## 📝 数据格式

### YAML格式示例

```yaml
- category: 开发工具
  subcategories:
    - name: 版本控制
      bookmarks:
        - name: GitHub
          url: https://github.com
          icon: https://github.com/favicon.ico
          tags: [代码托管, 版本控制, 开源]
          description: 全球最大的代码托管平台
```

### CSV格式示例

```csv
一级分类,二级分类,网站名称,网址,图标URL,标签,简介
开发工具,版本控制,GitHub,https://github.com,https://github.com/favicon.ico,"代码托管, 版本控制, 开源",全球最大的代码托管平台
```

## 🎯 使用说明

### 导航网站功能

1. **搜索功能**
   - 在搜索框中输入关键词，实时筛选书签
   - 支持搜索书签名称、标签、描述
   - 快捷键：`Ctrl/Cmd + K` 聚焦搜索框，`ESC` 清空搜索

2. **分类导航**
   - 点击一级分类标签，显示对应的二级分类
   - 点击二级分类标签，筛选显示特定子分类的书签
   - 点击"全部"显示所有内容

3. **主题切换**
   - 点击右上角的主题切换按钮
   - 支持明暗两种主题，设置会自动保存

4. **统计信息**
   - 顶部显示书签总数、分类数量等统计信息

### 数据管理

1. **添加书签**
   - 编辑`bookmarks.yaml`文件，按照现有格式添加新的书签
   - 运行`python generate_nav.py`重新生成网站

2. **批量导入**
   - 将书签数据整理为CSV格式
   - 使用`python csv_to_yaml.py`转换为YAML格式
   - 运行生成器更新网站

3. **数据导出**
   - 使用`python yaml_to_csv.py`将YAML数据导出为CSV格式
   - 便于在Excel等工具中编辑

## 🛠️ 技术栈

- **后端**: Python 3.6+
- **依赖**: PyYAML
- **前端**: HTML5, CSS3, JavaScript (ES6+)
- **样式**: CSS Grid, Flexbox, CSS Variables
- **图标**: Favicon自动加载 + 首字母fallback

## 📋 依赖要求

```
PyYAML>=6.0
```

## 🎨 自定义样式

生成的网站使用CSS变量，可以轻松自定义主题：

```css
:root {
    --bg-primary: #f5f7fa;      /* 主背景色 */
    --bg-secondary: #ffffff;    /* 次背景色 */
    --text-primary: #2c3e50;    /* 主文字色 */
    --accent-color: #409eff;    /* 强调色 */
    /* 更多变量... */
}
```

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- 感谢所有贡献者的支持
- 灵感来源于现代导航网站设计
- 使用了开源图标和资源

---

**享受你的个性化书签导航网站！** 🎉
