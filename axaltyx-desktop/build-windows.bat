
@echo off
chcp 65001 &gt;nul
echo ========================================
echo   AxaltyX Windows编译脚本
echo ========================================
echo.

REM 检查管理员权限
net session &gt;nul 2&gt;&amp;1
if %errorLevel% neq 0 (
    echo [提示] 建议以管理员身份运行此脚本
    echo.
)

echo [1/6] 检查Node.js...
node --version &gt;nul 2&gt;&amp;1
if errorlevel 1 (
    echo [错误] 未找到Node.js，请先安装Node.js v18或更高版本
    echo 下载地址: https://nodejs.org/
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('node --version') do set NODE_VER=%%i
echo [成功] Node.js版本: %NODE_VER%

echo.
echo [2/6] 检查Python...
python --version &gt;nul 2&gt;&amp;1
if errorlevel 1 (
    echo [警告] 未找到Python，统计分析功能可能不可用
    echo 建议安装Python 3.9或更高版本
) else (
    for /f "tokens=*" %%i in ('python --version') do set PYTHON_VER=%%i
    echo [成功] Python版本: %PYTHON_VER%
)

echo.
echo [3/6] 切换到axaltyx-desktop目录...
if not exist "axaltyx-desktop" (
    echo [错误] 未找到axaltyx-desktop目录
    echo 请确保在AxaltyX项目根目录运行此脚本
    echo.
    pause
    exit /b 1
)
cd axaltyx-desktop
echo [成功] 当前目录: %CD%

echo.
echo [4/6] 安装前端依赖...
echo 正在使用国内镜像源加速下载...
call npm install --registry=https://registry.npmmirror.com
if errorlevel 1 (
    echo.
    echo [错误] 依赖安装失败
    echo 尝试删除node_modules后重试...
    if exist "node_modules" rmdir /s /q node_modules
    if exist "package-lock.json" del /f /q package-lock.json
    echo.
    pause
    exit /b 1
)
echo [成功] 依赖安装完成

echo.
echo [5/6] 编译前端代码...
call npm run build
if errorlevel 1 (
    echo [错误] 前端编译失败
    echo.
    pause
    exit /b 1
)
echo [成功] 前端编译完成

echo.
echo [6/6] 打包EXE安装包...
echo 这可能需要几分钟，请耐心等待...
echo.
set ELECTRON_MIRROR=https://npmmirror.com/mirrors/electron/
call npm run electron:build -- --win
if errorlevel 1 (
    echo.
    echo [错误] 打包失败
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   ✅ 编译完成！
echo ========================================
echo.
echo 安装包位置: %CD%\release\
echo.
dir /b release
echo.
echo 按任意键打开输出目录...
pause &gt;nul
explorer release
exit /b 0
