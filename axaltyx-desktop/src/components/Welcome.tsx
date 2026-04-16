
import React from 'react'
import { Card, Button, Space, Typography, Empty } from '@arco-design/web-react'
import { Database, BarChart, TrendingUp, FileText, Clock, Plus } from 'lucide-react'
import './Welcome.css'

const { Title, Paragraph, Text } = Typography

const Welcome: React.FC = () =&gt; {
  const recentProjects = [
    { id: 1, name: '论文数据分析', date: '2024-04-16' },
    { id: 2, name: '问卷数据统计', date: '2024-04-15' },
    { id: 3, name: '实验数据分析', date: '2024-04-14' }
  ]

  const quickStart = [
    { icon: &lt;Database size={24} /&gt;, title: '导入数据', desc: '支持CSV/Excel/SPSS等多种格式' },
    { icon: &lt;BarChart size={24} /&gt;, title: '描述统计', desc: '频数分析、交叉表、描述性统计' },
    { icon: &lt;TrendingUp size={24} /&gt;, title: '统计检验', desc: 't检验、方差分析、卡方检验' },
    { icon: &lt;FileText size={24} /&gt;, title: '生成报告', desc: '一键导出Word/HTML/PDF报告' }
  ]

  return (
    &lt;div className="welcome-container"&gt;
      &lt;div className="welcome-hero"&gt;
        &lt;div className="hero-content"&gt;
          &lt;Title heading={2} className="hero-title"&gt;
            欢迎使用 AxaltyX
          &lt;/Title&gt;
          &lt;Paragraph className="hero-subtitle"&gt;
            专业学术科研统计分析软件，功能超越SPSS，速度快3倍
          &lt;/Paragraph&gt;
          &lt;Space size="medium" className="hero-actions"&gt;
            &lt;Button type="primary" size="large" icon={&lt;Plus /&gt;}&gt;
              新建项目
            &lt;/Button&gt;
            &lt;Button size="large"&gt;
              打开项目
            &lt;/Button&gt;
          &lt;/Space&gt;
        &lt;/div&gt;
      &lt;/div&gt;

      &lt;div className="welcome-content"&gt;
        &lt;div className="content-section"&gt;
          &lt;Title heading={4} className="section-title"&gt;
            快速开始
          &lt;/Title&gt;
          &lt;div className="quick-start-grid"&gt;
            {quickStart.map((item, index) =&gt; (
              &lt;Card key={index} className="quick-start-card" hoverable&gt;
                &lt;div className="quick-start-icon"&gt;
                  {item.icon}
                &lt;/div&gt;
                &lt;Title heading={6} className="quick-start-title"&gt;
                  {item.title}
                &lt;/Title&gt;
                &lt;Text type="secondary" className="quick-start-desc"&gt;
                  {item.desc}
                &lt;/Text&gt;
              &lt;/Card&gt;
            ))}
          &lt;/div&gt;
        &lt;/div&gt;

        &lt;div className="content-section"&gt;
          &lt;Title heading={4} className="section-title"&gt;
            最近项目
          &lt;/Title&gt;
          &lt;Card className="recent-projects-card"&gt;
            {recentProjects.length &gt; 0 ? (
              &lt;div className="recent-projects-list"&gt;
                {recentProjects.map((project) =&gt; (
                  &lt;div key={project.id} className="recent-project-item"&gt;
                    &lt;div className="project-info"&gt;
                      &lt;Text className="project-name"&gt;{project.name}&lt;/Text&gt;
                      &lt;Text type="secondary" className="project-date"&gt;
                        &lt;Clock size={14} /&gt;
                        {project.date}
                      &lt;/Text&gt;
                    &lt;/div&gt;
                    &lt;Button size="small"&gt;打开&lt;/Button&gt;
                  &lt;/div&gt;
                ))}
              &lt;/div&gt;
            ) : (
              &lt;Empty description="暂无最近项目" /&gt;
            )}
          &lt;/Card&gt;
        &lt;/div&gt;
      &lt;/div&gt;
    &lt;/div&gt;
  )
}

export default Welcome
