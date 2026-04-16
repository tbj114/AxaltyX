@echo off
setlocal enabledelayedexpansion
title AxaltyX 全自动编译工具 v4.0
chcp 65001 >nul
color 0B

:init
cls
echo.
echo ================================================================
echo                      AxaltyX 编译工具 v4.0
echo ================================================================
echo.
echo [信息] 准备开始全自动编译流程...
echo [信息] 专为 Windows 环境优化，解决依赖下载问题
echo.

:check_admin
echo [1/11] 检查管理员权限...
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
echo [2/11] 检查系统环境...
echo [信息] 操作系统: %OS%
echo [信息] 处理器架构: %PROCESSOR_ARCHITECTURE%
echo [信息] 当前目录: %CD%
echo [成功] 系统检查完成
echo.

:check_internet
echo [3/11] 检查网络连接...
ping -n 1 baidu.com >nul 2>&1
if %errorLevel% neq 0 (
    echo [错误] 网络连接失败！
    echo [提示] 请检查网络连接后重试
    pause
    exit /b 1
) else (
    echo [成功] 网络连接正常
)
echo.

:check_nodejs
echo [4/11] 检查 Node.js...
set "NODE_FOUND=0"
set "NODE_VER="

rem 方法1: 直接执行 node --version
echo [调试] 方法1: 直接执行 node --version
node --version >node_version1.txt 2>&1
if %errorLevel% equ 0 (
    set "NODE_FOUND=1"
    set /p NODE_VER=<node_version1.txt
    echo [调试] 方法1成功: %NODE_VER%
) else (
    echo [调试] 方法1失败，错误码: %errorLevel%
    type node_version1.txt 2>nul
)

rem 方法2: 使用 where 命令查找 node.exe
if "%NODE_FOUND%" equ "0" (
    echo [调试] 方法2: 使用 where 命令查找 node.exe
    where node.exe >node_where.txt 2>&1
    if %errorLevel% equ 0 (
        echo [调试] 找到 node.exe:
        type node_where.txt
        rem 尝试使用找到的路径执行 node
        for /f "tokens=*" %%i in (node_where.txt) do (
            "%%i" --version >node_version2.txt 2>&1
            if %errorLevel% equ 0 (
                set "NODE_FOUND=1"
                set /p NODE_VER=<node_version2.txt
                echo [调试] 方法2成功: %NODE_VER%
                goto :node_found
            )
        )
    ) else (
        echo [调试] 方法2失败，错误码: %errorLevel%
    )
)

:node_found

rem 方法3: 检查常见安装路径
if "%NODE_FOUND%" equ "0" (
    echo [调试] 方法3: 检查常见安装路径
    set "node_paths=C:\Program Files\nodejs\node.exe;C:\Program Files (x86)\nodejs\node.exe;%APPDATA%\npm\node.exe;%USERPROFILE%\AppData\Roaming\npm\node.exe"
    
    for %%p in (!node_paths!) do (
        if exist "%%p" (
            echo [调试] 找到 node.exe 在: %%p
            "%%p" --version >node_version3.txt 2>&1
            if %errorLevel% equ 0 (
                set "NODE_FOUND=1"
                set /p NODE_VER=<node_version3.txt
                echo [调试] 方法3成功: %NODE_VER%
                goto :node_found
            )
        )
    )
)

rem 清理临时文件
del node_version1.txt 2>nul
del node_version2.txt 2>nul
del node_version3.txt 2>nul
del node_where.txt 2>nul

if "%NODE_FOUND%" equ "0" (
    echo [警告] 未检测到 Node.js
    echo.
    echo ================================================================
    echo 请按以下步骤安装 Node.js:
    echo 1. 访问 https://nodejs.org/
    echo 2. 下载并安装 LTS 版本 (推荐 v18.x 或 v20.x)
    echo 3. 安装完成后重新运行此脚本
    echo ================================================================
    echo.
    choice /C YN /M "是否现在打开 Node.js 下载页面" /N
    if errorlevel 1 (
        start https://nodejs.org/
    )
    echo.
    pause
    exit /b 1
) else (
    echo [成功] Node.js 版本: %NODE_VER%
)

echo.
echo [检查] npm...
set "NPM_FOUND=0"
set "NPM_VER="

rem 尝试执行 npm 命令
npm --version >npm_version.txt 2>&1
if %errorLevel% equ 0 (
    set "NPM_FOUND=1"
    set /p NPM_VER=<npm_version.txt
    echo [成功] npm 版本: %NPM_VER%
) else (
    echo [警告] 未检测到 npm，尝试使用 node 路径查找
    rem 尝试从 node 路径找到 npm
    for %%i in (node.exe) do (
        set "node_dir=%%~dpi"
        set "npm_path=!node_dir!npm.cmd"
        if exist "!npm_path!" (
            "!npm_path!" --version >npm_version2.txt 2>&1
            if %errorLevel% equ 0 (
                set "NPM_FOUND=1"
                set /p NPM_VER=<npm_version2.txt
                echo [成功] npm 版本: %NPM_VER%
            )
        )
    )
    if "%NPM_FOUND%" equ "0" (
        echo [错误] npm 不可用
        pause
        exit /b 1
    )
)
del npm_version.txt 2>nul
del npm_version2.txt 2>nul
echo.

:check_python
echo [5/11] 检查 Python...
set "PYTHON_FOUND=0"
set "PYTHON_VER="

rem 尝试执行 python 命令
python --version >python_version.txt 2>&1
if %errorLevel% equ 0 (
    set "PYTHON_FOUND=1"
    set /p PYTHON_VER=<python_version.txt
) else (
    rem 尝试 python3 命令
    python3 --version >python_version2.txt 2>&1
    if %errorLevel% equ 0 (
        set "PYTHON_FOUND=1"
        set /p PYTHON_VER=<python_version2.txt
    )
)

del python_version.txt 2>nul
del python_version2.txt 2>nul

if "%PYTHON_FOUND%" equ "0" (
    echo [警告] 未检测到 Python
    echo.
    echo ================================================================
    echo 请按以下步骤安装 Python:
    echo 1. 访问 https://www.python.org/downloads/
    echo 2. 下载并安装 Python 3.9 或更高版本
    echo 3. 重要: 安装时勾选 "Add Python to PATH"
    echo 4. 安装完成后重新运行此脚本
    echo ================================================================
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
    echo [成功] Python 版本: %PYTHON_VER%
    set PYTHON_AVAILABLE=1
)
echo.

:check_git
echo [6/11] 检查 Git（可选）...
set "GIT_FOUND=0"
set "GIT_VER="

rem 尝试执行 git 命令
git --version >git_version.txt 2>&1
if %errorLevel% equ 0 (
    set "GIT_FOUND=1"
    set /p GIT_VER=<git_version.txt
)
del git_version.txt 2>nul

if "%GIT_FOUND%" equ "0" (
    echo [提示] 未检测到 Git，将使用本地文件
    set GIT_AVAILABLE=0
) else (
    echo [成功] Git 版本: %GIT_VER%
    set GIT_AVAILABLE=1
)
echo.

:setup_project
echo [7/11] 设置项目目录...
cd /d "%~dp0"
echo [信息] 当前目录: %CD%

if not exist "axaltyx-desktop" (
    echo [警告] 未找到 axaltyx-desktop 目录
    if !GIT_AVAILABLE! equ 1 (
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
    echo [8/11] 安装 Python 依赖...
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
    echo [8/11] 跳过 Python 依赖安装（未检测到 Python）
)
echo.

:cleanup_old
echo [9/11] 清理旧的编译文件...
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
if exist "yarn.lock" (
    del /f /q yarn.lock
)
echo [成功] 清理完成
echo.

:install_node_deps
echo [10/11] 安装前端依赖...
echo [信息] 选择镜像源以加速下载...
echo.
echo 请选择 npm 镜像源：
echo 1. 清华大学镜像 (推荐)
echo 2. 淘宝镜像
echo 3. 官方源 (不推荐，可能很慢)
echo.
choice /C 123 /M "请选择镜像源: " /N
set "MIRROR_CHOICE=%errorlevel%"

if %MIRROR_CHOICE% equ 1 (
    set "NPM_REGISTRY=https://pypi.tuna.tsinghua.edu.cn/mirrors/npm/"
    echo [信息] 使用清华大学镜像源
) else if %MIRROR_CHOICE% equ 2 (
    set "NPM_REGISTRY=https://registry.npmmirror.com/"
    echo [信息] 使用淘宝镜像源
) else (
    set "NPM_REGISTRY=https://registry.npmjs.org/"
    echo [信息] 使用官方源
)
echo.

rem 设置环境变量加速下载
echo [信息] 设置环境变量加速下载...
set npm_config_registry=%NPM_REGISTRY%
set npm_config_disturl=https://npmmirror.com/mirrors/node
set npm_config_nodedir=%ProgramFiles%\nodejs
set ELECTRON_MIRROR=https://npmmirror.com/mirrors/electron/
set ELECTRON_BUILDER_BINARIES_MIRROR=https://npmmirror.com/mirrors/electron-builder-binaries/
set SASS_BINARY_SITE=https://npmmirror.com/mirrors/node-sass
set PHANTOMJS_CDNURL=https://npmmirror.com/mirrors/phantomjs
set CHROMEDRIVER_CDNURL=https://npmmirror.com/mirrors/chromedriver
set OPERADRIVER_CDNURL=https://npmmirror.com/mirrors/operadriver
set SELENIUM_CDNURL=https://npmmirror.com/mirrors/selenium
set PYTHON_MIRROR=https://npmmirror.com/mirrors/python

echo [信息] 开始安装依赖...
echo [信息] 这可能需要几分钟，请耐心等待...
echo.

:install_attempt
set "INSTALL_SUCCESS=0"

rem 尝试使用 yarn 安装
where yarn >nul 2>&1
if %errorLevel% equ 0 (
    echo [信息] 尝试使用 yarn 安装依赖...
    yarn install --registry %NPM_REGISTRY%
    if errorlevel 0 (
        set "INSTALL_SUCCESS=1"
        goto :install_success
    ) else (
        echo [警告] yarn 安装失败，尝试使用 npm...
    )
)

rem 尝试使用 npm 安装
echo [信息] 尝试使用 npm 安装依赖...
npm install --registry %NPM_REGISTRY% --force --verbose
if errorlevel 0 (
    set "INSTALL_SUCCESS=1"
    goto :install_success
) else (
    echo [错误] npm 安装也失败了
)

:install_failed
echo.
echo [错误] 依赖安装失败！
echo.
echo ================================================================
echo 故障排除:
echo 1. 检查网络连接是否稳定
echo 2. 尝试使用不同的镜像源
echo 3. 手动运行以下命令:
echo    npm install --registry=%NPM_REGISTRY% --force
echo 4. 或者尝试清理缓存:
echo    npm cache clean --force
echo 5. 检查防火墙是否阻止了下载
echo ================================================================
echo.
choice /C YN /M "是否重试安装" /N
if errorlevel 1 (
    goto :install_attempt
) else (
    pause
    exit /b 1
)

:install_success
echo.
echo [成功] 前端依赖安装完成
echo.

:build_project
echo [11/11] 开始编译项目...
echo.
echo ================================================================
echo 编译进行中...
echo 这可能需要 5-15 分钟，具体取决于你的电脑性能
echo 请不要关闭此窗口！
echo ================================================================
echo.

set start_time=%time%

rem 编译前端代码
echo [阶段 1/3] 编译前端代码...
npm run build
if errorlevel 1 (
    echo [错误] 前端编译失败
    pause
    exit /b 1
)
echo [成功] 前端编译完成
echo.

rem 编译 Electron 主进程
echo [阶段 2/3] 编译 Electron 主进程...
npm run build:electron
if errorlevel 1 (
    echo [错误] Electron 主进程编译失败
    pause
    exit /b 1
)
echo [成功] Electron 主进程编译完成
echo.

rem 打包 EXE 安装包
echo [阶段 3/3] 打包 EXE 安装包...
echo [信息] 这是最后一步，也是最耗时的一步...
echo [信息] 再次设置镜像源加速...
set ELECTRON_MIRROR=https://npmmirror.com/mirrors/electron/
set ELECTRON_BUILDER_BINARIES_MIRROR=https://npmmirror.com/mirrors/electron-builder-binaries/
npm run electron:build -- --win
if errorlevel 1 (
    echo.
    echo [错误] 打包失败！
    echo.
    echo ================================================================
    echo 故障排除:
    echo 1. 确保有足够的磁盘空间（至少 10GB）
    echo 2. 检查杀毒软件是否拦截了编译过程
    echo 3. 尝试增加 Node.js 内存: set NODE_OPTIONS=--max-old-space-size=4096
    echo 4. 以管理员身份运行此脚本
    echo 5. 检查网络连接是否稳定
    echo ================================================================
    echo.
    choice /C YN /M "是否重试打包" /N
    if errorlevel 1 (
        goto :build_project
    ) else (
        pause
        exit /b 1
    )
)

set end_time=%time%

:success
cls
echo.
echo ================================================================
echo                    编译成功！
echo ================================================================
echo.
echo [信息] 开始时间: %start_time%
echo [信息] 结束时间: %end_time%
echo.
echo ================================================================
echo 输出文件位置:
echo ================================================================
echo.
echo %CD%\release\
echo.

if exist "release" (
    echo ================================================================
echo 生成的文件:
echo ================================================================
echo.
    dir /b release
echo.
)

echo ================================================================
echo 下一步操作:
echo 1. 按任意键打开输出目录
echo 2. 运行 .exe 文件安装 AxaltyX
echo 3. 分享给其他用户使用！
echo ================================================================
echo.
echo 按任意键打开输出目录...
pause >nul
explorer release

:end
echo.
echo [信息] 感谢使用 AxaltyX 编译工具 v4.0！
echo [信息] 专为 Windows 环境优化，解决依赖下载问题
echo.
pause
exit /b 0