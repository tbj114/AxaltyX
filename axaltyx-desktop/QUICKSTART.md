
# AxaltyX 桌面应用 - 快速开始

## 项目概述

AxaltyX是一款专业的桌面统计分析软件，采用字节跳动设计语言（Arco Design），功能全面超越SPSS，速度更快，支持本地离线使用。

## 技术栈

- **前端框架**: React 18 + TypeScript
- **桌面框架**: Electron
- **UI组件库**: Arco Design
- **状态管理**: Zustand
- **构建工具**: Vite
- **数据可视化**: ECharts
- **后端**: Python + 自研统计库 (axaltyx)
- **进程通信**: python-shell

## 项目结构

```
axaltyx-desktop/
├── electron/              # Electron主进程
│   ├── main.ts           # 主进程入口
│   └── preload.ts        # 预加载脚本
├── python_bridge/        # Python桥接层
│   └── bridge.py         # Python与Node.js通信
├── src/
│   ├── components/       # React组件
│   │   ├── Welcome.tsx
│   │   ├── DataManager.tsx
│   │   ├── DescriptiveStats.tsx
│   │   ├── DataVisualizer.tsx
│   │   ├── VariablePanel.tsx
│   │   └── AnalysisWorkspace.tsx
│   ├── stores/          # 状态管理
│   │   └── appStore.ts
│   ├── types/           # TypeScript类型定义
│   │   └── index.ts
│   ├── App.tsx
│   ├── main.tsx
│   └── index.html
├── package.json
├── tsconfig.json
├── tsconfig.electron.json
├── vite.config.ts
└── electron-builder.yml
```

## 环境要求

- Node.js &gt;= 18
- Python &gt;= 3.9
- npm 或 yarn

## 安装步骤

### 1. 安装前端依赖

```bash
cd axaltyx-desktop
npm install
```

### 2. 安装Python依赖

确保你已经安装了Python 3.9+，然后安装axaltyx统计库：

```bash
cd ..
pip install -e .
```

或者直接安装依赖：

```bash
pip install numpy pandas scipy scikit-learn statsmodels matplotlib seaborn plotly
```

## 开发模式

### 启动开发服务器

```bash
cd axaltyx-desktop
npm run dev
```

### 启动Electron应用

在另一个终端窗口中：

```bash
# 首先编译Electron主进程
npm run build:electron

# 然后启动Electron
npm run electron:dev
```

## 功能模块

### 1. 数据管理
- 导入CSV/Excel文件
- 数据查看和编辑
- 数据搜索和筛选
- 数据导出

### 2. 描述统计
- 描述性统计分析
- 频数分析
- 交叉表分析

### 3. 统计检验
- t检验（单样本/独立样本/配对样本）
- 方差分析
- 卡方检验
- 非参数检验

### 4. 回归分析
- 简单线性回归
- 多元线性回归
- Logistic回归

### 5. 多元统计
- 因子分析
- 主成分分析
- 聚类分析
- 判别分析

### 6. 数据可视化
- 条形图
- 直方图
- 散点图
- 折线图
- 饼图
- 箱线图
- 热图

## 构建生产版本

### 构建前端

```bash
npm run build
```

### 编译Electron主进程

```bash
npm run build:electron
```

### 打包安装包

```bash
npm run electron:build
```

打包完成后，安装包将位于 `release/` 目录中。

## 开发路线图

### 第一阶段 (已完成)
- ✅ 项目框架搭建
- ✅ Electron主进程和预加载脚本
- ✅ Python桥接层
- ✅ 基础UI组件
- ✅ 数据管理模块
- ✅ 描述性统计模块
- ✅ 数据可视化模块

### 第二阶段
- 🔄 统计检验模块
- 🔄 回归分析模块
- 🔄 多元统计模块
- 🔄 高级可视化
- 🔄 性能优化
- 🔄 测试和调试

### 第三阶段
- 🔄 安装包优化
- 🔄 用户文档
- 🔄 帮助系统
- 🔄 正式发布

## 技术亮点

1. **字节风格设计**: 使用Arco Design组件库，现代简洁的UI
2. **高性能**: Python统计库 + Numba JIT编译 + 多进程并行
3. **离线优先**: 本地运行，无需联网
4. **跨平台**: 支持Windows/macOS/Linux
5. **完整功能**: 涵盖SPSS标准版的所有功能

## 常见问题

### Q: Python桥接无法启动？
A: 确保已安装Python 3.9+和所需的依赖包。

### Q: 如何添加新的分析模块？
A: 在 `src/components/` 中创建新组件，在 `python_bridge/bridge.py` 中添加对应的Python方法。

### Q: 如何自定义主题？
A: 修改 `src/App.css` 中的CSS变量和样式定义。

## 版权声明

© 2024 TBJ114. 保留所有权利。
