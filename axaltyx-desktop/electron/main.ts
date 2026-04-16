
import { app, BrowserWindow, ipcMain, dialog, Menu } from 'electron'
import * as path from 'path'
import * as url from 'url'
import { PythonShell } from 'python-shell'

let mainWindow: BrowserWindow | null = null
let pythonShell: PythonShell | null = null

const isDev = process.env.NODE_ENV === 'development'

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1200,
    minHeight: 700,
    show: false,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
      sandbox: false
    },
    titleBarStyle: 'default',
    backgroundColor: '#f7f8fa'
  })

  if (isDev) {
    mainWindow.loadURL('http://localhost:5173')
    mainWindow.webContents.openDevTools()
  } else {
    mainWindow.loadURL(
      url.format({
        pathname: path.join(__dirname, '../index.html'),
        protocol: 'file:',
        slashes: true
      })
    )
  }

  mainWindow.once('ready-to-show', () =&gt; {
    mainWindow?.show()
  })

  mainWindow.on('closed', () =&gt; {
    mainWindow = null
    if (pythonShell) {
      pythonShell.terminate()
      pythonShell = null
    }
  })

  createMenu()
  initPythonBridge()
}

function initPythonBridge() {
  const pythonPath = path.join(__dirname, '../python_bridge/bridge.py')
  
  pythonShell = new PythonShell(pythonPath, {
    pythonPath: 'python3',
    mode: 'text'
  })

  pythonShell.on('message', (message) =&gt; {
    try {
      const result = JSON.parse(message)
      if (result.requestId &amp;&amp; mainWindow) {
        mainWindow.webContents.send(`python:response:${result.requestId}`, result)
      }
    } catch (e) {
      console.error('Error parsing Python message:', e)
    }
  })

  pythonShell.on('error', (error) =&gt; {
    console.error('Python shell error:', error)
  })

  pythonShell.on('close', () =&gt; {
    console.log('Python shell closed')
    pythonShell = null
  })
}

function createMenu() {
  const template = [
    {
      label: '文件',
      submenu: [
        {
          label: '新建项目',
          accelerator: 'CmdOrCtrl+N',
          click: () =&gt; {
            mainWindow?.webContents.send('menu-new-project')
          }
        },
        {
          label: '打开项目',
          accelerator: 'CmdOrCtrl+O',
          click: () =&gt; {
            mainWindow?.webContents.send('menu-open-project')
          }
        },
        {
          type: 'separator'
        },
        {
          label: '保存',
          accelerator: 'CmdOrCtrl+S',
          click: () =&gt; {
            mainWindow?.webContents.send('menu-save')
          }
        },
        {
          label: '另存为',
          accelerator: 'CmdOrCtrl+Shift+S',
          click: () =&gt; {
            mainWindow?.webContents.send('menu-save-as')
          }
        },
        {
          type: 'separator'
        },
        {
          label: '导入数据',
          submenu: [
            { label: 'CSV文件', click: () =&gt; mainWindow?.webContents.send('import-csv') },
            { label: 'Excel文件', click: () =&gt; mainWindow?.webContents.send('import-excel') },
            { label: 'SPSS文件', click: () =&gt; mainWindow?.webContents.send('import-spss') },
            { label: 'Stata文件', click: () =&gt; mainWindow?.webContents.send('import-stata') }
          ]
        },
        {
          label: '导出',
          submenu: [
            { label: '导出为CSV', click: () =&gt; mainWindow?.webContents.send('export-csv') },
            { label: '导出为Excel', click: () =&gt; mainWindow?.webContents.send('export-excel') },
            { label: '导出报告', click: () =&gt; mainWindow?.webContents.send('export-report') }
          ]
        },
        {
          type: 'separator'
        },
        {
          label: '退出',
          accelerator: process.platform === 'darwin' ? 'Cmd+Q' : 'Alt+F4',
          click: () =&gt; {
            app.quit()
          }
        }
      ]
    },
    {
      label: '编辑',
      submenu: [
        { label: '撤销', accelerator: 'CmdOrCtrl+Z', role: 'undo' },
        { label: '重做', accelerator: 'CmdOrCtrl+Shift+Z', role: 'redo' },
        { type: 'separator' },
        { label: '剪切', accelerator: 'CmdOrCtrl+X', role: 'cut' },
        { label: '复制', accelerator: 'CmdOrCtrl+C', role: 'copy' },
        { label: '粘贴', accelerator: 'CmdOrCtrl+V', role: 'paste' },
        { label: '全选', accelerator: 'CmdOrCtrl+A', role: 'selectAll' }
      ]
    },
    {
      label: '视图',
      submenu: [
        { label: '重新加载', accelerator: 'CmdOrCtrl+R', role: 'reload' },
        { label: '强制重新加载', accelerator: 'CmdOrCtrl+Shift+R', role: 'forceReload' },
        { label: '开发者工具', accelerator: 'F12', role: 'toggleDevTools' },
        { type: 'separator' },
        { label: '实际大小', accelerator: 'CmdOrCtrl+0', role: 'resetZoom' },
        { label: '放大', accelerator: 'CmdOrCtrl+Plus', role: 'zoomIn' },
        { label: '缩小', accelerator: 'CmdOrCtrl+-', role: 'zoomOut' },
        { type: 'separator' },
        { label: '全屏', accelerator: 'F11', role: 'togglefullscreen' }
      ]
    },
    {
      label: '分析',
      submenu: [
        { label: '描述统计', click: () =&gt; mainWindow?.webContents.send('analysis-descriptive') },
        { label: '频数分析', click: () =&gt; mainWindow?.webContents.send('analysis-frequency') },
        { label: '交叉表', click: () =&gt; mainWindow?.webContents.send('analysis-crosstab') },
        { type: 'separator' },
        { label: 't检验', click: () =&gt; mainWindow?.webContents.send('analysis-ttest') },
        { label: '方差分析', click: () =&gt; mainWindow?.webContents.send('analysis-anova') },
        { type: 'separator' },
        { label: '相关分析', click: () =&gt; mainWindow?.webContents.send('analysis-correlation') },
        { label: '回归分析', click: () =&gt; mainWindow?.webContents.send('analysis-regression') },
        { type: 'separator' },
        { label: '因子分析', click: () =&gt; mainWindow?.webContents.send('analysis-factor') },
        { label: '聚类分析', click: () =&gt; mainWindow?.webContents.send('analysis-cluster') }
      ]
    },
    {
      label: '图表',
      submenu: [
        { label: '条形图', click: () =&gt; mainWindow?.webContents.send('chart-bar') },
        { label: '直方图', click: () =&gt; mainWindow?.webContents.send('chart-histogram') },
        { label: '散点图', click: () =&gt; mainWindow?.webContents.send('chart-scatter') },
        { label: '折线图', click: () =&gt; mainWindow?.webContents.send('chart-line') },
        { label: '箱线图', click: () =&gt; mainWindow?.webContents.send('chart-boxplot') },
        { label: '热图', click: () =&gt; mainWindow?.webContents.send('chart-heatmap') }
      ]
    },
    {
      label: '帮助',
      submenu: [
        { label: '使用文档', click: () =&gt; mainWindow?.webContents.send('help-docs') },
        { label: '快捷键', click: () =&gt; mainWindow?.webContents.send('help-shortcuts') },
        { type: 'separator' },
        { label: '关于 AxaltyX', click: () =&gt; showAboutDialog() }
      ]
    }
  ]

  const menu = Menu.buildFromTemplate(template as any)
  Menu.setApplicationMenu(menu)
}

function showAboutDialog() {
  dialog.showMessageBox(mainWindow!, {
    type: 'info',
    title: '关于 AxaltyX',
    message: 'AxaltyX',
    detail: '版本: 1.0.0\n\n专业统计分析软件\n© 2024 TBJ114. 保留所有权利。',
    buttons: ['确定']
  })
}

let requestIdCounter = 0

ipcMain.handle('python:execute', async (event, { command, args }) =&gt; {
  return new Promise((resolve) =&gt; {
    const requestId = ++requestIdCounter
    
    const timeout = setTimeout(() =&gt; {
      resolve({
        success: false,
        error: 'Request timeout'
      })
    }, 30000)

    const handleResponse = (result: any) =&gt; {
      clearTimeout(timeout)
      mainWindow?.webContents.removeListener(`python:response:${requestId}`, handleResponse)
      resolve(result)
    }

    mainWindow?.webContents.once(`python:response:${requestId}`, handleResponse)

    if (pythonShell) {
      const request = {
        requestId,
        command,
        args
      }
      pythonShell.send(JSON.stringify(request))
    } else {
      resolve({
        success: false,
        error: 'Python bridge not initialized'
      })
    }
  })
})

ipcMain.handle('python:loadData', async (event, filePath) =&gt; {
  return new Promise((resolve) =&gt; {
    const requestId = ++requestIdCounter
    
    const timeout = setTimeout(() =&gt; {
      resolve({
        success: false,
        error: 'Request timeout'
      })
    }, 30000)

    const handleResponse = (result: any) =&gt; {
      clearTimeout(timeout)
      mainWindow?.webContents.removeListener(`python:response:${requestId}`, handleResponse)
      resolve(result)
    }

    mainWindow?.webContents.once(`python:response:${requestId}`, handleResponse)

    if (pythonShell) {
      const request = {
        requestId,
        command: 'load_data',
        args: [filePath]
      }
      pythonShell.send(JSON.stringify(request))
    } else {
      resolve({
        success: false,
        error: 'Python bridge not initialized'
      })
    }
  })
})

ipcMain.handle('python:saveData', async (event, { filePath, data }) =&gt; {
  return new Promise((resolve) =&gt; {
    const requestId = ++requestIdCounter
    
    const timeout = setTimeout(() =&gt; {
      resolve({
        success: false,
        error: 'Request timeout'
      })
    }, 30000)

    const handleResponse = (result: any) =&gt; {
      clearTimeout(timeout)
      mainWindow?.webContents.removeListener(`python:response:${requestId}`, handleResponse)
      resolve(result)
    }

    mainWindow?.webContents.once(`python:response:${requestId}`, handleResponse)

    if (pythonShell) {
      const request = {
        requestId,
        command: 'save_data',
        args: [filePath, data]
      }
      pythonShell.send(JSON.stringify(request))
    } else {
      resolve({
        success: false,
        error: 'Python bridge not initialized'
      })
    }
  })
})

ipcMain.handle('python:descriptiveStats', async (event, { data, columns }) =&gt; {
  return new Promise((resolve) =&gt; {
    const requestId = ++requestIdCounter
    
    const timeout = setTimeout(() =&gt; {
      resolve({
        success: false,
        error: 'Request timeout'
      })
    }, 30000)

    const handleResponse = (result: any) =&gt; {
      clearTimeout(timeout)
      mainWindow?.webContents.removeListener(`python:response:${requestId}`, handleResponse)
      resolve(result)
    }

    mainWindow?.webContents.once(`python:response:${requestId}`, handleResponse)

    if (pythonShell) {
      const request = {
        requestId,
        command: 'descriptive_stats',
        args: [data, columns]
      }
      pythonShell.send(JSON.stringify(request))
    } else {
      resolve({
        success: false,
        error: 'Python bridge not initialized'
      })
    }
  })
})

ipcMain.handle('python:tTest', async (event, { data, options }) =&gt; {
  return new Promise((resolve) =&gt; {
    const requestId = ++requestIdCounter
    
    const timeout = setTimeout(() =&gt; {
      resolve({
        success: false,
        error: 'Request timeout'
      })
    }, 30000)

    const handleResponse = (result: any) =&gt; {
      clearTimeout(timeout)
      mainWindow?.webContents.removeListener(`python:response:${requestId}`, handleResponse)
      resolve(result)
    }

    mainWindow?.webContents.once(`python:response:${requestId}`, handleResponse)

    if (pythonShell) {
      const request = {
        requestId,
        command: 't_test',
        args: [data, options]
      }
      pythonShell.send(JSON.stringify(request))
    } else {
      resolve({
        success: false,
        error: 'Python bridge not initialized'
      })
    }
  })
})

ipcMain.handle('python:anova', async (event, { data, options }) =&gt; {
  return new Promise((resolve) =&gt; {
    const requestId = ++requestIdCounter
    
    const timeout = setTimeout(() =&gt; {
      resolve({
        success: false,
        error: 'Request timeout'
      })
    }, 30000)

    const handleResponse = (result: any) =&gt; {
      clearTimeout(timeout)
      mainWindow?.webContents.removeListener(`python:response:${requestId}`, handleResponse)
      resolve(result)
    }

    mainWindow?.webContents.once(`python:response:${requestId}`, handleResponse)

    if (pythonShell) {
      const request = {
        requestId,
        command: 'anova',
        args: [data, options]
      }
      pythonShell.send(JSON.stringify(request))
    } else {
      resolve({
        success: false,
        error: 'Python bridge not initialized'
      })
    }
  })
})

ipcMain.handle('python:correlation', async (event, { data, columns, method }) =&gt; {
  return new Promise((resolve) =&gt; {
    const requestId = ++requestIdCounter
    
    const timeout = setTimeout(() =&gt; {
      resolve({
        success: false,
        error: 'Request timeout'
      })
    }, 30000)

    const handleResponse = (result: any) =&gt; {
      clearTimeout(timeout)
      mainWindow?.webContents.removeListener(`python:response:${requestId}`, handleResponse)
      resolve(result)
    }

    mainWindow?.webContents.once(`python:response:${requestId}`, handleResponse)

    if (pythonShell) {
      const request = {
        requestId,
        command: 'correlation',
        args: [data, columns, method || 'pearson']
      }
      pythonShell.send(JSON.stringify(request))
    } else {
      resolve({
        success: false,
        error: 'Python bridge not initialized'
      })
    }
  })
})

ipcMain.handle('python:regression', async (event, { data, options }) =&gt; {
  return new Promise((resolve) =&gt; {
    const requestId = ++requestIdCounter
    
    const timeout = setTimeout(() =&gt; {
      resolve({
        success: false,
        error: 'Request timeout'
      })
    }, 30000)

    const handleResponse = (result: any) =&gt; {
      clearTimeout(timeout)
      mainWindow?.webContents.removeListener(`python:response:${requestId}`, handleResponse)
      resolve(result)
    }

    mainWindow?.webContents.once(`python:response:${requestId}`, handleResponse)

    if (pythonShell) {
      const request = {
        requestId,
        command: 'regression',
        args: [data, options]
      }
      pythonShell.send(JSON.stringify(request))
    } else {
      resolve({
        success: false,
        error: 'Python bridge not initialized'
      })
    }
  })
})

ipcMain.handle('python:plot', async (event, { plotType, data, options }) =&gt; {
  return new Promise((resolve) =&gt; {
    const requestId = ++requestIdCounter
    
    const timeout = setTimeout(() =&gt; {
      resolve({
        success: false,
        error: 'Request timeout'
      })
    }, 30000)

    const handleResponse = (result: any) =&gt; {
      clearTimeout(timeout)
      mainWindow?.webContents.removeListener(`python:response:${requestId}`, handleResponse)
      resolve(result)
    }

    mainWindow?.webContents.once(`python:response:${requestId}`, handleResponse)

    if (pythonShell) {
      const request = {
        requestId,
        command: 'plot',
        args: [plotType, data, options]
      }
      pythonShell.send(JSON.stringify(request))
    } else {
      resolve({
        success: false,
        error: 'Python bridge not initialized'
      })
    }
  })
})

ipcMain.handle('dialog:openFile', async (event, filters) =&gt; {
  const result = await dialog.showOpenDialog(mainWindow!, {
    properties: ['openFile'],
    filters
  })
  return result
})

ipcMain.handle('dialog:saveFile', async (event, filters) =&gt; {
  const result = await dialog.showSaveDialog(mainWindow!, {
    filters
  })
  return result
})

ipcMain.handle('dialog:selectDirectory', async () =&gt; {
  const result = await dialog.showOpenDialog(mainWindow!, {
    properties: ['openDirectory']
  })
  return result
})

ipcMain.handle('app:getVersion', () =&gt; {
  return app.getVersion()
})

ipcMain.handle('app:getPath', (event, name) =&gt; {
  return app.getPath(name as any)
})

app.on('ready', createWindow)

app.on('window-all-closed', () =&gt; {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () =&gt; {
  if (mainWindow === null) {
    createWindow()
  }
})
