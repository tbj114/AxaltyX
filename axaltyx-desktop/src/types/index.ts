
export interface Variable {
  id: string
  name: string
  label: string
  type: 'numeric' | 'categorical' | 'string' | 'date'
  measurement: 'scale' | 'ordinal' | 'nominal'
  missing: boolean
  values?: Record&lt;string, string&gt;
  decimals?: number
  width?: number
}

export interface DataRow {
  [key: string]: any
}

export interface Dataset {
  id: string
  name: string
  variables: Variable[]
  rows: DataRow[]
  createdAt: Date
  modifiedAt: Date
}

export interface AnalysisResult {
  id: string
  type: string
  title: string
  timestamp: Date
  status: 'pending' | 'running' | 'completed' | 'error'
  data?: any
  error?: string
  plot?: string
}

export interface Project {
  id: string
  name: string
  datasets: Dataset[]
  analyses: AnalysisResult[]
  createdAt: Date
  modifiedAt: Date
}

export interface AppState {
  currentProject: Project | null
  activeDataset: Dataset | null
  recentProjects: Array&lt;{ id: string; name: string; path: string; modifiedAt: Date }&gt;
  isLoading: boolean
  error: string | null
  theme: 'light' | 'dark'
  language: 'zh-CN' | 'en-US'
  hasData: boolean
}

export interface AnalysisConfig {
  module: string
  method: string
  variables: {
    dependent?: string[]
    independent?: string[]
    grouping?: string[]
  }
  options: Record&lt;string, any&gt;
}

export interface PlotConfig {
  type: 'bar' | 'histogram' | 'scatter' | 'line' | 'box' | 'heatmap' | 'pie'
  x?: string
  y?: string
  color?: string
  title?: string
  xLabel?: string
  yLabel?: string
  options: Record&lt;string, any&gt;
}

export interface MenuAction {
  type: string
  payload?: any
}

export interface ElectronAPI {
  ipcRenderer: {
    send: (channel: string, data?: any) =&gt; void
    on: (channel: string, callback: (...args: any[]) =&gt; void) =&gt; () =&gt; void
    once: (channel: string, callback: (...args: any[]) =&gt; void) =&gt; void
    removeListener: (channel: string, callback: (...args: any[]) =&gt; void) =&gt; void
    removeAllListeners: (channel: string) =&gt; void
  }
  dialog: {
    openFile: (filters?: Array&lt;{ name: string; extensions: string[] }&gt;) =&gt; Promise&lt;any&gt;
    saveFile: (filters?: Array&lt;{ name: string; extensions: string[] }&gt;) =&gt; Promise&lt;any&gt;
    selectDirectory: () =&gt; Promise&lt;any&gt;
  }
  app: {
    getVersion: () =&gt; Promise&lt;string&gt;
    getPath: (name: string) =&gt; Promise&lt;string&gt;
  }
}

export interface PythonAPI {
  execute: (command: string, args?: any[]) =&gt; Promise&lt;any&gt;
  loadData: (filePath: string) =&gt; Promise&lt;any&gt;
  saveData: (filePath: string, data: any) =&gt; Promise&lt;any&gt;
  descriptiveStats: (data: any, columns: string[]) =&gt; Promise&lt;any&gt;
  tTest: (data: any, options: any) =&gt; Promise&lt;any&gt;
  anova: (data: any, options: any) =&gt; Promise&lt;any&gt;
  correlation: (data: any, columns: string[], method?: string) =&gt; Promise&lt;any&gt;
  regression: (data: any, options: any) =&gt; Promise&lt;any&gt;
  plot: (plotType: string, data: any, options: any) =&gt; Promise&lt;any&gt;
}

declare global {
  interface Window {
    electronAPI: ElectronAPI
    pythonAPI: PythonAPI
  }
}
