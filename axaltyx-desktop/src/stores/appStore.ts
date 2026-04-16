
import { create } from 'zustand'
import type { AppState as AppStateType, Dataset, AnalysisResult, Project } from '../types'

interface StoreState extends AppStateType {
  setCurrentProject: (project: Project | null) =&gt; void
  setCurrentDataset: (dataset: Dataset | null) =&gt; void
  addAnalysis: (analysis: AnalysisResult) =&gt; void
  setLoading: (loading: boolean) =&gt; void
  setError: (error: string | null) =&gt; void
  setTheme: (theme: 'light' | 'dark') =&gt; void
  setLanguage: (language: 'zh-CN' | 'en-US') =&gt; void
  addRecentProject: (project: { id: string; name: string; path: string; modifiedAt: Date }) =&gt; void
}

export const useAppStore = create&lt;StoreState&gt;((set, get) =&gt; ({
  currentProject: null,
  activeDataset: null,
  recentProjects: [],
  isLoading: false,
  error: null,
  theme: 'light',
  language: 'zh-CN',
  hasData: false,

  setCurrentProject: (project) =&gt; set({ 
    currentProject: project,
    activeDataset: project?.datasets[0] || null 
  }),
  
  setCurrentDataset: (dataset) =&gt; set({ 
    activeDataset: dataset,
    hasData: !!dataset 
  }),
  
  addAnalysis: (analysis) =&gt; set((state) =&gt; ({
    currentProject: state.currentProject ? {
      ...state.currentProject,
      analyses: [...state.currentProject.analyses, analysis]
    } : null
  })),
  
  setLoading: (loading) =&gt; set({ isLoading: loading }),
  
  setError: (error) =&gt; set({ error }),
  
  setTheme: (theme) =&gt; set({ theme }),
  
  setLanguage: (language) =&gt; set({ language }),
  
  addRecentProject: (project) =&gt; set((state) =&gt; {
    const filtered = state.recentProjects.filter(p =&gt; p.id !== project.id)
    return {
      recentProjects: [project, ...filtered].slice(0, 10)
    }
  })
}))
