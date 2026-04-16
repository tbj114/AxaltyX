
import { contextBridge, ipcRenderer } from 'electron'

contextBridge.exposeInMainWorld('electronAPI', {
  ipcRenderer: {
    send: (channel: string, data?: any) =&gt; {
      ipcRenderer.send(channel, data)
    },
    on: (channel: string, callback: (...args: any[]) =&gt; void) =&gt; {
      const subscription = (_event: any, ...args: any[]) =&gt; callback(...args)
      ipcRenderer.on(channel, subscription)
      return () =&gt; {
        ipcRenderer.removeListener(channel, subscription)
      }
    },
    once: (channel: string, callback: (...args: any[]) =&gt; void) =&gt; {
      ipcRenderer.once(channel, (_event: any, ...args: any[]) =&gt; callback(...args))
    },
    removeListener: (channel: string, callback: (...args: any[]) =&gt; void) =&gt; {
      ipcRenderer.removeListener(channel, callback)
    },
    removeAllListeners: (channel: string) =&gt; {
      ipcRenderer.removeAllListeners(channel)
    }
  },

  dialog: {
    openFile: (filters?: Electron.FileFilter[]) =&gt; {
      return ipcRenderer.invoke('dialog:openFile', filters)
    },
    saveFile: (filters?: Electron.FileFilter[]) =&gt; {
      return ipcRenderer.invoke('dialog:saveFile', filters)
    },
    selectDirectory: () =&gt; {
      return ipcRenderer.invoke('dialog:selectDirectory')
    }
  },

  app: {
    getVersion: () =&gt; {
      return ipcRenderer.invoke('app:getVersion')
    },
    getPath: (name: string) =&gt; {
      return ipcRenderer.invoke('app:getPath', name)
    }
  }
})

contextBridge.exposeInMainWorld('pythonAPI', {
  execute: async (command: string, args: any[] = []) =&gt; {
    return ipcRenderer.invoke('python:execute', { command, args })
  },
  loadData: async (filePath: string) =&gt; {
    return ipcRenderer.invoke('python:loadData', filePath)
  },
  saveData: async (filePath: string, data: any) =&gt; {
    return ipcRenderer.invoke('python:saveData', { filePath, data })
  },
  descriptiveStats: async (data: any, columns: string[]) =&gt; {
    return ipcRenderer.invoke('python:descriptiveStats', { data, columns })
  },
  tTest: async (data: any, options: any) =&gt; {
    return ipcRenderer.invoke('python:tTest', { data, options })
  },
  anova: async (data: any, options: any) =&gt; {
    return ipcRenderer.invoke('python:anova', { data, options })
  },
  correlation: async (data: any, columns: string[], method: string = 'pearson') =&gt; {
    return ipcRenderer.invoke('python:correlation', { data, columns, method })
  },
  regression: async (data: any, options: any) =&gt; {
    return ipcRenderer.invoke('python:regression', { data, options })
  },
  plot: async (plotType: string, data: any, options: any) =&gt; {
    return ipcRenderer.invoke('python:plot', { plotType, data, options })
  }
})
