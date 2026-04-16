
@echo off
setlocal enabledelayedexpansion
title AxaltyX 全自动编译工具 v2.0
chcp 65001 >nul
color 0B

:init
cls
echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                                                                   ║
echo ║         █████╗ ██╗  ██╗ █████╗ ██╗  ████████╗██╗   ██╗        ║
echo ║        ██╔══██╗╚██╗██╔╝██╔══██╗██║  ╚══██╔══╝╚██╗ ██╔╝        ║
echo ║        ███████║ ╚███╔╝ ███████║██║     ██║    ╚████╔╝         ║
echo ║        ██╔══██║ ██╔██╗ ██╔══██║██║     ██║     ╚██╔╝          ║
echo ║        ██║  ██║██╔╝ ██╗██║  ██║███████╗██║      ██║           ║
echo ║        ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝      ╚═╝           ║
echo ║                                                                   ║
echo ║                    专业统计分析软件 - 全自动编译工具            ║
echo ║                              v2.0                                ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
echo [信息] 准备开始全自动编译流程...
echo.

:check_admin
echo [1/10] 检查管理员权限...
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [提示] 未检测到管理员权限，部分功能可能受限
    echo [提示] 建议右键选择"以管理员身份运行"
    echo.
    choice /C YN /M "是否继续运行" /N
    if errorlevel 2 (
        echo [信息] 请以管理员身份重新运行此脚本
        pause
        exit /b 0
    )
) else (
    echo [成功] 已获得管理员权限
)
echo.

:check_system
echo [2/10] 检查系统环境...
echo [信息] 操作系统: %OS%
echo [信息] 处理器架构: %PROCESSOR_ARCHITECTURE%
echo [成功] 系统检查完成
echo.

:check_nodejs
echo [3/10] 检查 Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo [警告] 未检测到 Node.js
    echo.
    echo ╔═══════════════════════════════════════════════════════════════╗
    echo ║  请按以下步骤安装 Node.js:                                      ║
    echo ║  1. 访问 https://nodejs.org/                                    ║
    echo ║  2. 下载并安装 LTS 版本 (推荐 v18.x 或 v20.x)                   ║
    echo ║  3. 安装完成后重新运行此脚本                                    ║
    echo ╚═══════════════════════════════════════════════════════════════╝
    echo.
    choice /C YN /M "是否现在打开 Node.js 下载页面" /N
    if errorlevel 1 (
        start https://nodejs.org/
    )
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('node --version') do set NODE_VER=%%i
echo [成功] Node.js 版本: %NODE_VER%

echo.
echo [检查] npm...
npm --version >nul 2>&1
if errorlevel 1 (
    echo [错误] npm 不可用
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('npm --version') do set NPM_VER=%%i
echo [成功] npm 版本: %NPM_VER%
echo.

:check_python
echo [4/10] 检查 Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [警告] 未检测到 Python
    echo.
    echo ╔═══════════════════════════════════════════════════════════════╗
    echo ║  请按以下步骤安装 Python:                                       ║
    echo ║  1. 访问 https://www.python.org/downloads/                      ║
    echo ║  2. 下载并安装 Python 3.9 或更高版本                            ║
    echo ║  3. 重要: 安装时勾选 "Add Python to PATH"                       ║
    echo ║  4. 安装完成后重新运行此脚本                                    ║
    echo ╚═══════════════════════════════════════════════════════════════╝
    echo.
    choice /C YN /M "是否现在打开 Python 下载页面" /N
    if errorlevel 1 (
        start https://www.python.org/downloads/
    )
    echo.
    choice /C YN /M "是否继续编译（Python功能将不可用）" /N
    if errorlevel 2 (
        pause
        exit /b 1
    )
    set PYTHON_AVAILABLE=0
) else (
    for /f "tokens=*" %%i in ('python --version') do set PYTHON_VER=%%i
    echo [成功] Python 版本: %PYTHON_VER%
    set PYTHON_AVAILABLE=1
)
echo.

:check_git
echo [5/10] 检查 Git（可选）...
git --version >nul 2>&1
if errorlevel 1 (
    echo [提示] 未检测到 Git，将使用本地文件
    set GIT_AVAILABLE=0
) else (
    for /f "tokens=*" %%i in ('git --version') do set GIT_VER=%%i
    echo [成功] Git 版本: %GIT_VER%
    set GIT_AVAILABLE=1
)
echo.

:setup_project
echo [6/10] 设置项目目录...
cd /d "%~dp0"
echo [信息] 当前目录: %CD%

if not exist "axaltyx-desktop" (
    echo [警告] 未找到 axaltyx-desktop 目录
    if %GIT_AVAILABLE% equ 1 (
        echo [信息] 尝试从 GitHub 克隆...
        git clone https://github.com/tbj114/AxaltyX.git
        if errorlevel 1 (
            echo [错误] 克隆失败
            pause
            exit /b 1
        )
        cd AxaltyX
    ) else (
        echo [错误] 请确保在正确的目录中运行此脚本
        pause
        exit /b 1
    )
)

if exist "axaltyx-desktop" (
    cd axaltyx-desktop
    echo [成功] 项目目录: %CD%
) else (
    echo [错误] 无法定位项目目录
    pause
    exit /b 1
)
echo.

:install_python_deps
if %PYTHON_AVAILABLE% equ 1 (
    echo [7/10] 安装 Python 依赖...
    cd ..
    echo [信息] 安装 axaltyx 统计库...
    pip install -e . -i https://pypi.tuna.tsinghua.edu.cn/simple
    if errorlevel 1 (
        echo [警告] Python 依赖安装可能有问题，但继续...
    ) else (
        echo [成功] Python 依赖安装完成
    )
    cd axaltyx-desktop
) else (
    echo [7/10] 跳过 Python 依赖安装（未检测到 Python）
)
echo.

:cleanup_old
echo [8/10] 清理旧的编译文件...
if exist "node_modules" (
    echo [信息] 清理 node_modules...
    rmdir /s /q node_modules
)
if exist "dist" (
    echo [信息] 清理 dist...
    rmdir /s /q dist
)
if exist "release" (
    echo [信息] 清理 release...
    rmdir /s /q release
)
if exist "package-lock.json" (
    del /f /q package-lock.json
)
echo [成功] 清理完成
echo.

:install_node_deps
echo [9/10] 安装前端依赖...
echo [信息] 使用清华大学镜像源加速...
echo [信息] 这可能需要几分钟，请耐心等待...
echo.

set npm_config_registry=https://registry.npmmirror.com
set ELECTRON_MIRROR=https://npmmirror.com/mirrors/electron/
set ELECTRON_BUILDER_BINARIES_MIRROR=https://npmmirror.com/mirrors/electron-builder-binaries/

call npm install
if errorlevel 1 (
    echo.
    echo [错误] 依赖安装失败！
    echo.
    echo ╔═══════════════════════════════════════════════════════════════╗
    echo ║  故障排除:                                                      ║
    echo ║  1. 检查网络连接                                               ║
    echo ║  2. 尝试删除 node_modules 和 package-lock.json 后重试           ║
    echo ║  3. 或者手动运行: npm install --registry=https://registry.npmmirror.com ║
    echo ╚═══════════════════════════════════════════════════════════════╝
    echo.
    pause
    exit /b 1
)
echo.
echo [成功] 前端依赖安装完成
echo.

:build_project
echo [10/10] 开始编译项目...
echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                        编译进行中...                            ║
echo ║  这可能需要 5-15 分钟，具体取决于你的电脑性能                   ║
echo ║  请不要关闭此窗口！                                             ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

set start_time=%time%

echo [阶段 1/3] 编译前端代码...
call npm run build
if errorlevel 1 (
    echo [错误] 前端编译失败
    pause
    exit /b 1
)
echo [成功] 前端编译完成
echo.

echo [阶段 2/3] 编译 Electron 主进程...
call npm run build:electron
if errorlevel 1 (
    echo [错误] Electron 主进程编译失败
    pause
    exit /b 1
)
echo [成功] Electron 主进程编译完成
echo.

echo [阶段 3/3] 打包 EXE 安装包...
echo [信息] 这是最后一步，也是最耗时的一步...
call npm run electron:build -- --win
if errorlevel 1 (
    echo.
    echo [错误] 打包失败！
    echo.
    echo ╔═══════════════════════════════════════════════════════════════╗
    echo ║  故障排除:                                                      ║
    echo ║  1. 确保有足够的磁盘空间（至少 10GB）                          ║
    echo ║  2. 检查杀毒软件是否拦截了编译过程                              ║
    echo ║  3. 尝试增加 Node.js 内存: set NODE_OPTIONS=--max-old-space-size=4096 ║
    echo ╚═══════════════════════════════════════════════════════════════╝
    echo.
    pause
    exit /b 1
)

set end_time=%time%

:success
cls
echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                                                                   ║
echo ║                        ✅  编译成功！                            ║
echo ║                                                                   ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
echo [信息] 开始时间: %start_time%
echo [信息] 结束时间: %end_time%
echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                        输出文件位置:                              ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
echo %CD%\release\
echo.

if exist "release" (
    echo ╔═══════════════════════════════════════════════════════════════╗
    echo ║                        生成的文件:                                ║
    echo ╚═══════════════════════════════════════════════════════════════╝
    echo.
    dir /b release
    echo.
)

echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                        下一步操作:                                ║
echo ║  1. 按任意键打开输出目录                                        ║
echo ║  2. 运行 .exe 文件安装 AxaltyX                                   ║
echo ║  3. 分享给其他用户使用！                                         ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
echo 按任意键打开输出目录...
pause >nul
explorer release

:end
echo.
echo [信息] 感谢使用 AxaltyX 编译工具！
echo.
pause
exit /b 0
