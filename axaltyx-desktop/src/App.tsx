
import React, { useState } from 'react'
import { Layout, Menu, Breadcrumb, Button, Space, Dropdown, Message } from '@arco-design/web-react'
import {
  IconHome,
  IconFile,
  IconBarChart,
  IconSettings,
  IconUser,
  IconSave,
  IconDownload,
  IconPlus,
  IconFolderOpen
} from '@arco-design/web-react/icon'
import { Database, BarChart3, TrendingUp, Layers, Brain } from 'lucide-react'
import Welcome from './components/Welcome'
import VariablePanel from './components/VariablePanel'
import AnalysisWorkspace from './components/AnalysisWorkspace'
import DataManager from './components/DataManager'
import { useAppStore } from './stores/appStore'
import './App.css'

const { Header, Sider, Content } = Layout
const MenuItem = Menu.Item

const App: React.FC = () =&gt; {
  const [activeModule, setActiveModule] = useState('welcome')
  const { currentProject, hasData } = useAppStore()

  const menuItems = [
    {
      key: 'welcome',
      title: '欢迎',
      icon: &lt;IconHome /&gt;
    },
    {
      key: 'data',
      title: '数据管理',
      icon: &lt;Database size={18} /&gt;
    },
    {
      key: 'descriptive',
      title: '描述统计',
      icon: &lt;BarChart3 size={18} /&gt;
    },
    {
      key: 'inference',
      title: '统计检验',
      icon: &lt;TrendingUp size={18} /&gt;
    },
    {
      key: 'regression',
      title: '回归分析',
      icon: &lt;Layers size={18} /&gt;
    },
    {
      key: 'multivariate',
      title: '多元统计',
      icon: &lt;Brain size={18} /&gt;
    }
  ]

  const handleNewProject = () =&gt; {
    Message.info('新建项目功能')
  }

  const handleOpenProject = () =&gt; {
    Message.info('打开项目功能')
  }

  const handleSaveProject = () =&gt; {
    Message.success('项目已保存')
  }

  return (
    &lt;Layout className="app-layout"&gt;
      &lt;Header className="app-header"&gt;
        &lt;div className="header-left"&gt;
          &lt;div className="logo"&gt;
            &lt;span className="logo-icon"&gt;A&lt;/span&gt;
            &lt;span className="logo-text"&gt;AxaltyX&lt;/span&gt;
          &lt;/div&gt;
          &lt;Breadcrumb className="breadcrumb"&gt;
            &lt;Breadcrumb.Item&gt;{currentProject || '未命名项目'}&lt;/Breadcrumb.Item&gt;
          &lt;/Breadcrumb&gt;
        &lt;/div&gt;
        &lt;div className="header-right"&gt;
          &lt;Space&gt;
            &lt;Button type="primary" icon={&lt;IconPlus /&gt;} onClick={handleNewProject}&gt;
              新建项目
            &lt;/Button&gt;
            &lt;Button icon={&lt;IconFolderOpen /&gt;} onClick={handleOpenProject}&gt;
              打开
            &lt;/Button&gt;
            &lt;Button icon={&lt;IconSave /&gt;} onClick={handleSaveProject}&gt;
              保存
            &lt;/Button&gt;
            &lt;Button icon={&lt;IconDownload /&gt;}&gt;
              导出
            &lt;/Button&gt;
            &lt;Button icon={&lt;IconSettings /&gt;} /&gt;
            &lt;Dropdown droplist={
              &lt;Menu&gt;
                &lt;Menu.Item key="1"&gt;个人中心&lt;/Menu.Item&gt;
                &lt;Menu.Item key="2"&gt;设置&lt;/Menu.Item&gt;
                &lt;Menu.Item key="3"&gt;退出登录&lt;/Menu.Item&gt;
              &lt;/Menu&gt;
            }&gt;
              &lt;Button icon={&lt;IconUser /&gt;}&gt;账户&lt;/Button&gt;
            &lt;/Dropdown&gt;
          &lt;/Space&gt;
        &lt;/div&gt;
      &lt;/Header&gt;
      &lt;Layout&gt;
        &lt;Sider width={240} className="app-sider"&gt;
          &lt;Menu
            mode="vertical"
            selectedKeys={[activeModule]}
            onClickMenuItem={(key) =&gt; setActiveModule(key)}
          &gt;
            {menuItems.map(item =&gt; (
              &lt;MenuItem key={item.key}&gt;
                {item.icon}
                &lt;span style={{ marginLeft: 10 }}&gt;{item.title}&lt;/span&gt;
              &lt;/MenuItem&gt;
            ))}
          &lt;/Menu&gt;
        &lt;/Sider&gt;
        &lt;Layout className="main-layout"&gt;
          {hasData &amp;&amp; &lt;VariablePanel /&gt;}
          &lt;Content className="app-content"&gt;
            {activeModule === 'welcome' &amp;&amp; &lt;Welcome /&gt;}
            {activeModule === 'data' &amp;&amp; &lt;DataManager /&gt;}
            {activeModule !== 'welcome' &amp;&amp; activeModule !== 'data' &amp;&amp; &lt;AnalysisWorkspace module={activeModule} /&gt;}
          &lt;/Content&gt;
        &lt;/Layout&gt;
      &lt;/Layout&gt;
    &lt;/Layout&gt;
  )
}

export default App
