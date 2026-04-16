
import React from 'react'
import { Card, Typography, Button, Space, Message } from '@arco-design/web-react'
import { Settings, Save } from 'lucide-react'
import DescriptiveStats from './DescriptiveStats'
import { useAppStore } from '../stores/appStore'
import './AnalysisWorkspace.css'

const { Title } = Typography

interface AnalysisWorkspaceProps {
  module: string
}

const AnalysisWorkspace: React.FC&lt;AnalysisWorkspaceProps&gt; = ({ module }) =&gt; {
  const { activeDataset } = useAppStore()

  const moduleConfig: Record&lt;string, { title: string; component: React.ReactNode }&gt; = {
    descriptive: {
      title: '描述统计',
      component: &lt;DescriptiveStats /&gt;
    },
    inference: {
      title: '统计检验',
      component: (
        &lt;Card&gt;
          &lt;div style={{ textAlign: 'center', padding: '60px 20px' }}&gt;
            &lt;Title heading={4}&gt;统计检验模块&lt;/Title&gt;
            &lt;p style={{ color: '#86909c', marginTop: '16px' }}&gt;
              此模块开发中，敬请期待...
            &lt;/p&gt;
          &lt;/div&gt;
        &lt;/Card&gt;
      )
    },
    regression: {
      title: '回归分析',
      component: (
        &lt;Card&gt;
          &lt;div style={{ textAlign: 'center', padding: '60px 20px' }}&gt;
            &lt;Title heading={4}&gt;回归分析模块&lt;/Title&gt;
            &lt;p style={{ color: '#86909c', marginTop: '16px' }}&gt;
              此模块开发中，敬请期待...
            &lt;/p&gt;
          &lt;/div&gt;
        &lt;/Card&gt;
      )
    },
    multivariate: {
      title: '多元统计',
      component: (
        &lt;Card&gt;
          &lt;div style={{ textAlign: 'center', padding: '60px 20px' }}&gt;
            &lt;Title heading={4}&gt;多元统计模块&lt;/Title&gt;
            &lt;p style={{ color: '#86909c', marginTop: '16px' }}&gt;
              此模块开发中，敬请期待...
            &lt;/p&gt;
          &lt;/div&gt;
        &lt;/Card&gt;
      )
    }
  }

  const config = moduleConfig[module] || moduleConfig.descriptive

  const handleSave = () =&gt; {
    Message.info('保存功能待实现')
  }

  const handleSettings = () =&gt; {
    Message.info('设置功能待实现')
  }

  if (!activeDataset) {
    return (
      &lt;div className="analysis-workspace"&gt;
        &lt;Card&gt;
          &lt;div style={{ textAlign: 'center', padding: '60px 20px' }}&gt;
            &lt;Title heading={4}&gt;请先导入数据&lt;/Title&gt;
            &lt;p style={{ color: '#86909c', marginTop: '16px' }}&gt;
              在"数据管理"模块中导入您的数据文件，然后再进行统计分析
            &lt;/p&gt;
          &lt;/div&gt;
        &lt;/Card&gt;
      &lt;/div&gt;
    )
  }

  return (
    &lt;div className="analysis-workspace"&gt;
      &lt;div className="workspace-header"&gt;
        &lt;div className="workspace-title"&gt;
          &lt;Title heading={4}&gt;{config.title}&lt;/Title&gt;
        &lt;/div&gt;
        &lt;Space&gt;
          &lt;Button icon={&lt;Settings /&gt;} onClick={handleSettings}&gt;设置&lt;/Button&gt;
          &lt;Button icon={&lt;Save /&gt;} onClick={handleSave}&gt;保存&lt;/Button&gt;
        &lt;/Space&gt;
      &lt;/div&gt;

      &lt;div className="workspace-content"&gt;
        {config.component}
      &lt;/div&gt;
    &lt;/div&gt;
  )
}

export default AnalysisWorkspace
