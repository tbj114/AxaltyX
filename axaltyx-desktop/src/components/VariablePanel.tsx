
import React from 'react'
import { Card, Typography, Tag } from '@arco-design/web-react'
import { List, ListItem, Hash, Type, Calendar } from 'lucide-react'
import './VariablePanel.css'

const { Title } = Typography

interface Variable {
  id: string
  name: string
  type: 'numeric' | 'categorical' | 'date'
  label?: string
  missingCount: number
}

const VariablePanel: React.FC = () =&gt; {
  const variables: Variable[] = [
    { id: '1', name: 'age', type: 'numeric', label: '年龄', missingCount: 0 },
    { id: '2', name: 'income', type: 'numeric', label: '收入', missingCount: 2 },
    { id: '3', name: 'score', type: 'numeric', label: '分数', missingCount: 0 },
    { id: '4', name: 'gender', type: 'categorical', label: '性别', missingCount: 0 },
    { id: '5', name: 'education', type: 'categorical', label: '教育程度', missingCount: 1 },
    { id: '6', name: 'satisfaction', type: 'numeric', label: '满意度', missingCount: 0 }
  ]

  const getVariableIcon = (type: string) =&gt; {
    switch (type) {
      case 'numeric':
        return &lt;Hash size={16} /&gt;
      case 'categorical':
        return &lt;Type size={16} /&gt;
      case 'date':
        return &lt;Calendar size={16} /&gt;
      default:
        return &lt;Hash size={16} /&gt;
    }
  }

  const getVariableColor = (type: string) =&gt; {
    switch (type) {
      case 'numeric':
        return 'arcoblue'
      case 'categorical':
        return 'green'
      case 'date':
        return 'orange'
      default:
        return 'arcoblue'
    }
  }

  return (
    &lt;div className="variable-panel"&gt;
      &lt;Card className="variable-card" title={
        &lt;div className="variable-panel-header"&gt;
          &lt;List size={18} /&gt;
          &lt;span&gt;变量列表&lt;/span&gt;
        &lt;/div&gt;
      }&gt;
        &lt;div className="variable-list"&gt;
          {variables.map((variable) =&gt; (
            &lt;div key={variable.id} className="variable-item" draggable&gt;
              &lt;div className="variable-icon"&gt;
                {getVariableIcon(variable.type)}
              &lt;/div&gt;
              &lt;div className="variable-info"&gt;
                &lt;div className="variable-name"&gt;
                  {variable.label || variable.name}
                &lt;/div&gt;
                &lt;div className="variable-meta"&gt;
                  &lt;Tag size="small" color={getVariableColor(variable.type)}&gt;
                    {variable.type}
                  &lt;/Tag&gt;
                  {variable.missingCount &gt; 0 &amp;&amp; (
                    &lt;Tag size="small" color="red"&gt;
                      {variable.missingCount}缺失
                    &lt;/Tag&gt;
                  )}
                &lt;/div&gt;
              &lt;/div&gt;
            &lt;/div&gt;
          ))}
        &lt;/div&gt;
      &lt;/Card&gt;
    &lt;/div&gt;
  )
}

export default VariablePanel
