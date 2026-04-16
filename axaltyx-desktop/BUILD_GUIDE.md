
# AxaltyX 编译指南

本指南将帮助你将AxaltyX编译成Windows的EXE安装包。

## 📋 前置要求

### 1. 系统要求
- Windows 10 或更高版本
- 至少 4GB RAM
- 至少 10GB 可用磁盘空间

### 2. 软件要求
- **Node.js**: v18 或更高版本
- **Python**: 3.9 或更高版本
- **npm**: 随Node.js一起安装
- **Git**: 可选，用于克隆仓库

### 3. 验证安装
打开命令提示符（CMD）或PowerShell，运行以下命令验证：

```bash
node --version
npm --version
python --version
```

## 🚀 编译步骤

### 第一步：获取源代码

如果你还没有代码，先克隆GitHub仓库：

```bash
git clone https://github.com/tbj114/AxaltyX.git
cd AxaltyX
```

### 第二步：安装Python依赖

```bash
# 进入项目根目录
cd AxaltyX

# 安装axaltyx Python库（开发模式）
pip install -e .

# 或者安装核心依赖
pip install numpy pandas scipy scikit-learn statsmodels matplotlib seaborn plotly
```

### 第三步：安装前端依赖

```bash
# 进入桌面应用目录
cd axaltyx-desktop

# 安装依赖（使用国内镜像加速）
npm install --registry=https://registry.npmmirror.com
```

### 第四步：准备资源文件（可选但推荐）

创建以下目录结构来放置图标和Python运行时：

```
axaltyx-desktop/
├── resources/
│   ├── icons/
│   │   ├── icon.ico      (Windows图标, 256x256)
│   │   ├── icon.icns     (macOS图标)
│   │   └── icon.png      (Linux图标, 512x512)
│   └── python/          (嵌入式Python运行时，可选)
```

**注意**: 如果没有图标，electron-builder会使用默认图标。

### 第五步：编译前端代码

```bash
# 在axaltyx-desktop目录中
npm run build
```

这将：
1. 使用Vite编译React前端代码到 `dist/` 目录
2. 编译Electron主进程TypeScript代码

### 第六步：编译Electron主进程

```bash
npm run build:electron
```

### 第七步：打包EXE安装包

```bash
# 只打包Windows版本
npm run electron:build -- --win

# 或者打包所有平台（Windows/macOS/Linux）
npm run electron:build
```

## 📁 输出文件

编译完成后，安装包将位于：

```
axaltyx-desktop/release/
├── AxaltyX Setup 1.0.0.exe          (Windows NSIS安装包)
├── AxaltyX-1.0.0-win.zip             (Windows便携版)
└── (其他平台的安装包...)
```

## 🔧 配置说明

### 修改应用信息

编辑 `package.json` 文件：

```json
{
  "name": "axaltyx-desktop",
  "version": "1.0.0",           // 修改版本号
  "description": "AxaltyX - 专业统计分析软件",
  "copyright": "Copyright © 2024 TBJ114"
}
```

### 修改electron-builder配置

编辑 `electron-builder.yml` 文件：

```yaml
appId: com.tbj114.axaltyx
productName: AxaltyX              // 修改应用名称
directories:
  output: release                // 输出目录
win:
  target:
    - nsis                      // 生成NSIS安装包
    - portable                  // 生成便携版
  icon: resources/icons/icon.ico
```

### NSIS安装包配置

```yaml
nsis:
  oneClick: false                // 不使用一键安装
  allowToChangeInstallationDirectory: true  // 允许修改安装目录
  createDesktopShortcut: true     // 创建桌面快捷方式
  createStartMenuShortcut: true   // 创建开始菜单项
  installerIcon: resources/icons/icon.ico
  uninstallerIcon: resources/icons/icon.ico
```

## ⚡ 快速编译命令（推荐）

创建一个批处理文件 `build-windows.bat`：

```batch
@echo off
echo ========================================
echo   AxaltyX Windows编译脚本
echo ========================================
echo.

echo [1/5] 检查Node.js...
node --version
if errorlevel 1 (
    echo 错误: 未找到Node.js，请先安装Node.js
    pause
    exit /b 1
)

echo.
echo [2/5] 检查Python...
python --version
if errorlevel 1 (
    echo 警告: 未找到Python，部分功能可能不可用
)

echo.
echo [3/5] 安装前端依赖...
cd axaltyx-desktop
call npm install --registry=https://registry.npmmirror.com
if errorlevel 1 (
    echo 错误: 依赖安装失败
    pause
    exit /b 1
)

echo.
echo [4/5] 编译前端代码...
call npm run build
if errorlevel 1 (
    echo 错误: 前端编译失败
    pause
    exit /b 1
)

echo.
echo [5/5] 打包EXE安装包...
call npm run electron:build -- --win
if errorlevel 1 (
    echo 错误: 打包失败
    pause
    exit /b 1
)

echo.
echo ========================================
echo   ✅ 编译完成！
echo ========================================
echo.
echo 安装包位置: axaltyx-desktop\release\
echo.
pause
```

## 🎯 常见问题

### Q1: npm install 速度太慢？

**A**: 使用国内镜像源：

```bash
npm install --registry=https://registry.npmmirror.com

# 或者永久设置
npm config set registry https://registry.npmmirror.com
```

### Q2: Electron下载失败？

**A**: 设置Electron镜像：

```bash
# Windows (PowerShell)
$env:ELECTRON_MIRROR="https://npmmirror.com/mirrors/electron/"
npm install

# Windows (CMD)
set ELECTRON_MIRROR=https://npmmirror.com/mirrors/electron/
npm install
```

### Q3: 编译时内存不足？

**A**: 增加Node.js内存限制：

```bash
# Windows
set NODE_OPTIONS=--max-old-space-size=4096
npm run electron:build
```

### Q4: 如何只打包便携版？

**A**: 修改electron-builder.yml：

```yaml
win:
  target: portable
```

### Q5: 打包后Python功能不可用？

**A**: 需要将Python运行时打包进去。这比较复杂，推荐：
1. 要求用户预先安装Python
2. 或者使用PyInstaller将Python部分打包成独立exe

## 📝 开发模式测试

在正式打包前，建议先在开发模式下测试：

```bash
# 启动开发服务器（终端1）
cd axaltyx-desktop
npm run dev

# 编译Electron主进程（终端2）
npm run build:electron

# 启动Electron应用（终端2）
npm run electron:dev
```

## 🔐 签名安装包（可选）

为了让Windows SmartScreen信任你的应用，可以对安装包进行数字签名：

```yaml
win:
  signingHashAlgorithms:
    - sha256
  certificateFile: certificate.pfx
  certificatePassword: your_password
```

## 📚 更多资源

- [Electron Builder文档](https://www.electron.build/)
- [Electron官方文档](https://www.electronjs.org/docs)
- [Arco Design组件库](https://arco.design/react)

---

**版权所有 © 2024 TBJ114**
