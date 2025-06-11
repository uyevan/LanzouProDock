# LanzouDir

🚀 蓝奏云文件夹解析 API 服务

## 项目简介

LanzouDir 是一个用于解析蓝奏云分享链接的 API 服务，可以获取文件夹内容、文件信息，以及生成直接下载链接。本项目现已开源，欢迎社区共同维护和改进。

## 🌟 功能特性

- 获取文件夹列表（JSON）
- 获取文件信息（JSON）
- 获取文件和文件夹的混合列表（JSON）
- 生成文件直接下载链接（JSON）
- 文件搜索功能（JSON）
- 支持多个版本的 API（V1, V2, V3）

## ⚙️ 项目架构

项目基于 Flask 框架构建，采用分层架构设计：

### 1. 核心组件

- **application.py**: 应用程序入口，导入和注册所有 API 路由
- **router.py**: 初始化 Flask 应用和会话配置
- **api/**: 包含所有 API 实现的目录

### 2. API 版本演进

项目支持三个主要版本的 API，每个版本针对蓝奏云不同的接口或解析方式：

- **V1**: 基于网页内容解析，使用正则表达式提取关键参数
- **V2**: 在 V1 基础上优化，采用 RESTful 风格 API 设计
- **V3**: 使用新的 API 接口（api.ilanzou.com），支持优享版和专业版功能

### 3. 主要模块功能

- **获取文件夹列表**: 解析文件夹内容，获取子文件夹列表
- **获取文件列表**: 获取指定文件夹内的所有文件
- **搜索文件**: 在指定文件夹中搜索文件
- **解析下载链接**: 生成直接可用的文件下载链接

### 4. 部署相关

- 支持 Docker 容器化部署
- 支持 uWSGI/Gunicorn 作为 WSGI 服务器
- 包含 Nginx 配置文件

## 🚀 快速开始

### 本地运行

1. 克隆仓库:
   ```bash
   git clone https://github.com/uyevan/LanzouDir.git
   cd LanzouDir
   ```

2. 安装依赖:
   ```bash
   pip install -r requirements.txt
   ```

3. 启动服务:
   ```bash
   python application.py
   ```

4. 访问 API:
   ```
   http://localhost:3307/
   ```

### Docker 部署

```bash
docker build -t lanzoudir .
docker run -p 3307:3307 lanzoudir
```

## 📚 API 文档

### V1 API 示例

- 获取文件夹内容: `/v1/getDirectory?url=https://www.lanzoux.com/xxx`
- 获取文件列表: `/v1/getFiles?url=https://www.lanzoux.com/xxx&page=1`
- 通过 URL 解析下载链接: `/v1/parse?url=https://www.lanzoux.com/xxx`

### V2 API 示例

- 获取文件夹内容: `/v2/getDirectory/xxx/1`
- 获取文件列表: `/v2/getFiles/xxx/1`
- 通过 ID 解析下载链接: `/v2/parseById/xxx`

### V3 API 示例 (优享版/专业版)

- 获取文件夹 ID: `/v3/iGetFolderId/{shareId}/{page}/{limit}`
- 获取文件列表: `/v3/iGetFiles/{shareId}/{folderId}/{page}/{limit}`
- 解析下载链接: `/v3/iParse/{fileId}`

## 🔧 已知问题与修复

目前 V3 API 中的一些接口可能存在问题，特别是获取文件夹 ID 的接口。我们正在努力修复这些问题，欢迎社区贡献解决方案。

常见问题:
1. V3 获取文件夹 ID 接口返回空列表
2. 部分解析接口可能需要更新适应蓝奏云最新变化

## 🤝 贡献指南

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交你的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启一个 Pull Request

## 📝 许可证

本项目采用 MIT 许可证 - 详情请参见 LICENSE 文件

## 📮 联系方式

- 作者: Evan
- 邮箱: uyevan@163.com
- 项目官网: [https://lanzou.uyclouds.com](https://lanzou.uyclouds.com)

## 🌐 相关链接

- [蓝奏云 Pro API 文档](https://lanzou.uyclouds.com)