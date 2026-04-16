
import React, { useState, useEffect } from 'react'
import { Card, Table, Button, Select, Space, Message, Spin, Tabs } from '@arco-design/web-react'
import { IconPlayArrow, IconRefresh } from '@arco-design/web-react/icon'
import { useAppStore } from '../stores/appStore'
import type { Variable } from '../types'
import './DescriptiveStats.css'

const { Option } = Select
const TabPane = Tabs.TabPane

interface DescriptiveStatsProps {
  onResultsChange?: (results: any) =&gt; void
}

const DescriptiveStats: React.FC&lt;DescriptiveStatsProps&gt; = ({ onResultsChange }) =&gt; {
  const { activeDataset } = useAppStore()
  const [selectedVariables, setSelectedVariables] = useState&lt;string[]&gt;([])
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState&lt;any&gt;(null)
  const [activeTab, setActiveTab] = useState('setup')

  const numericVariables = activeDataset?.variables.filter(
    v =&gt; v.type === 'numeric'
  ) || []

  const handleRunAnalysis = async () =&gt; {
    if (!activeDataset || selectedVariables.length === 0) {
      Message.warning('请至少选择一个数值变量')
      return
    }

    try {
      setLoading(true)
      const pythonResult = await window.pythonAPI.descriptiveStats(
        activeDataset.rows,
        selectedVariables
      )

      if (pythonResult.success) {
        setResults(pythonResult.result)
        setActiveTab('results')
        if (onResultsChange) {
          onResultsChange(pythonResult.result)
        }
        Message.success('描述性统计分析完成')
      } else {
        Message.error(pythonResult.error || '分析失败')
      }
    } catch (error) {
      Message.error('分析过程中出错')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () =&gt; {
    setSelectedVariables([])
    setResults(null)
    setActiveTab('setup')
  }

  const renderResultsTable = () =&gt; {
    if (!results) return null

    const columns = [
      {
        title: '统计量',
        dataIndex: 'statistic',
        key: 'statistic',
        width: 150,
        fontWeight: 600
      },
      ...selectedVariables.map(varName =&gt; ({
        title: varName,
        dataIndex: varName,
        key: varName,
        width: 150
      }))
    ]

    const tableData = Object.keys(results).map(statistic =&gt; ({
      key: statistic,
      statistic: getStatisticLabel(statistic),
      ...selectedVariables.reduce((acc, varName) =&gt; ({
        ...acc,
        [varName]: formatValue(results[statistic]?.[varName])
      }), {})
    }))

    return (
      &lt;Table
        columns={columns}
        data={tableData}
        pagination={false}
        border
        size="small"
      /&gt;
    )
  }

  const getStatisticLabel = (stat: string): string =&gt; {
    const labels: Record&lt;string, string&gt; = {
      count: '样本数',
      mean: '均值',
      std: '标准差',
      min: '最小值',
      '25%': '25%分位数',
      '50%': '中位数',
      '75%': '75%分位数',
      max: '最大值',
      variance: '方差',
      skewness: '偏度',
      kurtosis: '峰度'
    }
    return labels[stat] || stat
  }

  const formatValue = (value: any): string =&gt; {
    if (value === null || value === undefined) return '-'
    if (typeof value === 'number') {
      return value.toFixed(4)
    }
    return String(value)
  }

  return (
    &lt;div className="descriptive-stats"&gt;
      &lt;Tabs activeTab={activeTab} onChange={setActiveTab}&gt;
        &lt;TabPane key="setup" title="分析设置"&gt;
          &lt;Card&gt;
            &lt;div className="analysis-setup"&gt;
              &lt;div className="setup-section"&gt;
                &lt;h3&gt;选择变量&lt;/h3&gt;
                &lt;p className="section-desc"&gt;选择要进行描述性统计分析的数值变量&lt;/p&gt;
                &lt;Select
                  multiple
                  placeholder="请选择变量"
                  value={selectedVariables}
                  onChange={setSelectedVariables}
                  style={{ width: '100%', minHeight: 100 }}
                  disabled={!activeDataset}
                &gt;
                  {numericVariables.map(variable =&gt; (
                    &lt;Option key={variable.id} value={variable.name}&gt;
                      {variable.label || variable.name}
                    &lt;/Option&gt;
                  ))}
                &lt;/Select&gt;
              &lt;/div&gt;

              &lt;div className="setup-actions"&gt;
                &lt;Space&gt;
                  &lt;Button
                    type="primary"
                    icon={&lt;IconPlayArrow /&gt;}
                    onClick={handleRunAnalysis}
                    loading={loading}
                    disabled={!activeDataset || selectedVariables.length === 0}
                    size="large"
                  &gt;
                    运行分析
                  &lt;/Button&gt;
                  &lt;Button
                    icon={&lt;IconRefresh /&gt;}
                    onClick={handleReset}
                    size="large"
                  &gt;
                    重置
                  &lt;/Button&gt;
                &lt;/Space&gt;
              &lt;/div&gt;
            &lt;/div&gt;
          &lt;/Card&gt;
        &lt;/TabPane&gt;

        &lt;TabPane key="results" title="分析结果" disabled={!results}&gt;
          &lt;Card&gt;
            &lt;div className="analysis-results"&gt;
              {loading ? (
                &lt;div className="loading-container"&gt;
                  &lt;Spin size={40} /&gt;
                  &lt;p&gt;正在分析数据...&lt;/p&gt;
                &lt;/div&gt;
              ) : results ? (
                &lt;div className="results-content"&gt;
                  &lt;div className="results-header"&gt;
                    &lt;h3&gt;描述性统计结果&lt;/h3&gt;
                    &lt;Button type="primary" onClick={handleRunAnalysis}&gt;
                      重新计算
                    &lt;/Button&gt;
                  &lt;/div&gt;
                  {renderResultsTable()}
                &lt;/div&gt;
              ) : (
                &lt;div className="empty-results"&gt;
                  &lt;p&gt;请先运行分析以查看结果&lt;/p&gt;
                &lt;/div&gt;
              )}
            &lt;/div&gt;
          &lt;/Card&gt;
        &lt;/TabPane&gt;

        &lt;TabPane key="charts" title="图表" disabled={!results}&gt;
          &lt;Card&gt;
            &lt;div className="charts-container"&gt;
              &lt;p&gt;图表功能开发中...&lt;/p&gt;
            &lt;/div&gt;
          &lt;/Card&gt;
        &lt;/TabPane&gt;
      &lt;/Tabs&gt;
    &lt;/div&gt;
  )
}

export default DescriptiveStats
