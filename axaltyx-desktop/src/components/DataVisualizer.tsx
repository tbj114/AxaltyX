
import React, { useState, useEffect, useRef } from 'react'
import { Card, Select, Button, Space, Form, Message, Spin, Tabs, Input } from '@arco-design/web-react'
import { IconPlayArrow, IconDownload, IconRefresh } from '@arco-design/web-react/icon'
import ReactECharts from 'echarts-for-react'
import { useAppStore } from '../stores/appStore'
import './DataVisualizer.css'

const { Option } = Select
const { TabPane } = Tabs
const FormItem = Form.Item

interface DataVisualizerProps {
  chartType?: string
}

const DataVisualizer: React.FC&lt;DataVisualizerProps&gt; = ({ chartType: initialChartType = 'bar' }) =&gt; {
  const { activeDataset } = useAppStore()
  const [chartType, setChartType] = useState(initialChartType)
  const [selectedX, setSelectedX] = useState&lt;string&gt;('')
  const [selectedY, setSelectedY] = useState&lt;string&gt;('')
  const [selectedColor, setSelectedColor] = useState&lt;string&gt;('')
  const [chartTitle, setChartTitle] = useState('')
  const [loading, setLoading] = useState(false)
  const [chartOption, setChartOption] = useState&lt;any&gt;(null)
  const [activeTab, setActiveTab] = useState('setup')
  const chartRef = useRef&lt;ReactECharts&gt;(null)

  const numericVariables = activeDataset?.variables.filter(
    v =&gt; v.type === 'numeric'
  ) || []

  const categoricalVariables = activeDataset?.variables.filter(
    v =&gt; v.type === 'categorical' || v.type === 'string'
  ) || []

  const allVariables = activeDataset?.variables || []

  const generateChartOption = () =&gt; {
    if (!activeDataset || !selectedX) return null

    const data = activeDataset.rows
    const baseOption: any = {
      title: {
        text: chartTitle || `${chartType.toUpperCase()} 图表`,
        left: 'center'
      },
      tooltip: {
        trigger: chartType === 'pie' ? 'item' : 'axis'
      },
      legend: {
        bottom: '5%',
        left: 'center'
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '15%',
        containLabel: true
      }
    }

    switch (chartType) {
      case 'bar':
        return {
          ...baseOption,
          xAxis: {
            type: 'category',
            data: data.map((d: any) =&gt; d[selectedX]),
            axisLabel: { rotate: 45 }
          },
          yAxis: {
            type: 'value',
            name: selectedY || '值'
          },
          series: [
            {
              name: selectedY || '数值',
              type: 'bar',
              data: data.map((d: any) =&gt; d[selectedY] || 0),
              itemStyle: {
                color: '#165DFF'
              }
            }
          ]
        }

      case 'histogram':
        const histogramData = data.map((d: any) =&gt; d[selectedX]).filter((v: any) =&gt; v != null)
        return {
          ...baseOption,
          xAxis: {
            type: 'category',
            name: selectedX
          },
          yAxis: {
            type: 'value',
            name: '频数'
          },
          series: [
            {
              name: '频数',
              type: 'bar',
              data: histogramData,
              barWidth: '60%',
              itemStyle: {
                color: '#165DFF'
              }
            }
          ]
        }

      case 'scatter':
        return {
          ...baseOption,
          xAxis: {
            type: 'value',
            name: selectedX
          },
          yAxis: {
            type: 'value',
            name: selectedY
          },
          series: [
            {
              symbolSize: 8,
              data: data.map((d: any) =&gt; [d[selectedX], d[selectedY]]),
              type: 'scatter',
              itemStyle: {
                color: '#165DFF'
              }
            }
          ]
        }

      case 'line':
        return {
          ...baseOption,
          xAxis: {
            type: 'category',
            data: data.map((d: any) =&gt; d[selectedX]),
            axisLabel: { rotate: 45 }
          },
          yAxis: {
            type: 'value',
            name: selectedY
          },
          series: [
            {
              name: selectedY,
              type: 'line',
              data: data.map((d: any) =&gt; d[selectedY]),
              smooth: true,
              itemStyle: {
                color: '#165DFF'
              },
              areaStyle: {
                color: {
                  type: 'linear',
                  x: 0,
                  y: 0,
                  x2: 0,
                  y2: 1,
                  colorStops: [
                    { offset: 0, color: 'rgba(22, 93, 255, 0.3)' },
                    { offset: 1, color: 'rgba(22, 93, 255, 0.05)' }
                  ]
                }
              }
            }
          ]
        }

      case 'pie':
        const pieData = data.reduce((acc: any[], d: any) =&gt; {
          const value = d[selectedX]
          const existing = acc.find(item =&gt; item.name === value)
          if (existing) {
            existing.value++
          } else {
            acc.push({ name: String(value), value: 1 })
          }
          return acc
        }, [])
        return {
          ...baseOption,
          tooltip: {
            trigger: 'item',
            formatter: '{a} &lt;br/&gt;{b}: {c} ({d}%)'
          },
          series: [
            {
              name: selectedX,
              type: 'pie',
              radius: ['40%', '70%'],
              avoidLabelOverlap: false,
              itemStyle: {
                borderRadius: 10,
                borderColor: '#fff',
                borderWidth: 2
              },
              label: {
                show: true,
                formatter: '{b}: {d}%'
              },
              emphasis: {
                label: {
                  show: true,
                  fontSize: 16,
                  fontWeight: 'bold'
                }
              },
              data: pieData
            }
          ]
        }

      case 'box':
        return {
          ...baseOption,
          tooltip: {
            trigger: 'item',
            axisPointer: {
              type: 'shadow'
            }
          },
          xAxis: {
            type: 'category',
            data: [selectedX],
            name: '变量'
          },
          yAxis: {
            type: 'value',
            name: '值'
          },
          series: [
            {
              name: selectedX,
              type: 'boxplot',
              data: [data.map((d: any) =&gt; d[selectedX]).filter((v: any) =&gt; v != null)],
              itemStyle: {
                color: '#165DFF'
              }
            }
          ]
        }

      case 'heatmap':
        if (!selectedY) return baseOption
        const heatmapData = data.map((d: any) =&gt; [d[selectedX], d[selectedY], 1])
        return {
          ...baseOption,
          tooltip: {
            position: 'top'
          },
          grid: {
            height: '50%',
            top: '10%'
          },
          xAxis: {
            type: 'category',
            data: [...new Set(data.map((d: any) =&gt; d[selectedX]))],
            splitArea: {
              show: true
            }
          },
          yAxis: {
            type: 'category',
            data: [...new Set(data.map((d: any) =&gt; d[selectedY]))],
            splitArea: {
              show: true
            }
          },
          visualMap: {
            min: 0,
            max: 10,
            calculable: true,
            orient: 'horizontal',
            left: 'center',
            bottom: '5%',
            inRange: {
              color: ['#50a3ba', '#eac736', '#d94e5d']
            }
          },
          series: [
            {
              name: '热力图',
              type: 'heatmap',
              data: heatmapData,
              label: {
                show: true
              },
              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              }
            }
          ]
        }

      default:
        return baseOption
    }
  }

  const handleGenerateChart = async () =&gt; {
    if (!selectedX) {
      Message.warning('请至少选择X轴变量')
      return
    }

    try {
      setLoading(true)
      const option = generateChartOption()
      setChartOption(option)
      setActiveTab('chart')
      Message.success('图表生成成功')
    } catch (error) {
      Message.error('图表生成失败')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () =&gt; {
    setSelectedX('')
    setSelectedY('')
    setSelectedColor('')
    setChartTitle('')
    setChartOption(null)
    setActiveTab('setup')
  }

  const handleDownload = () =&gt; {
    if (chartRef.current) {
      const url = chartRef.current.getEchartsInstance().getDataURL({
        type: 'png',
        pixelRatio: 2
      })
      const link = document.createElement('a')
      link.download = `${chartTitle || 'chart'}.png`
      link.href = url
      link.click()
      Message.success('图表已下载')
    }
  }

  const getVariableOptions = (variables: any[]) =&gt; {
    return variables.map(v =&gt; (
      &lt;Option key={v.id} value={v.name}&gt;
        {v.label || v.name}
      &lt;/Option&gt;
    ))
  }

  return (
    &lt;div className="data-visualizer"&gt;
      &lt;Tabs activeTab={activeTab} onChange={setActiveTab}&gt;
        &lt;TabPane key="setup" title="图表设置"&gt;
          &lt;Card&gt;
            &lt;div className="visualizer-setup"&gt;
              &lt;Form layout="vertical"&gt;
                &lt;div className="setup-row"&gt;
                  &lt;FormItem label="图表类型"&gt;
                    &lt;Select
                      value={chartType}
                      onChange={setChartType}
                      style={{ width: '100%' }}
                      disabled={!activeDataset}
                    &gt;
                      &lt;Option value="bar"&gt;条形图&lt;/Option&gt;
                      &lt;Option value="histogram"&gt;直方图&lt;/Option&gt;
                      &lt;Option value="scatter"&gt;散点图&lt;/Option&gt;
                      &lt;Option value="line"&gt;折线图&lt;/Option&gt;
                      &lt;Option value="pie"&gt;饼图&lt;/Option&gt;
                      &lt;Option value="box"&gt;箱线图&lt;/Option&gt;
                      &lt;Option value="heatmap"&gt;热图&lt;/Option&gt;
                    &lt;/Select&gt;
                  &lt;/FormItem&gt;
                &lt;/div&gt;

                &lt;div className="setup-row"&gt;
                  &lt;FormItem label="X轴变量"&gt;
                    &lt;Select
                      placeholder="请选择X轴变量"
                      value={selectedX}
                      onChange={setSelectedX}
                      style={{ width: '100%' }}
                      disabled={!activeDataset}
                      allowClear
                    &gt;
                      {getVariableOptions(allVariables)}
                    &lt;/Select&gt;
                  &lt;/FormItem&gt;

                  {(chartType === 'bar' || chartType === 'scatter' || chartType === 'line' || chartType === 'heatmap') &amp;&amp; (
                    &lt;FormItem label="Y轴变量"&gt;
                      &lt;Select
                        placeholder="请选择Y轴变量"
                        value={selectedY}
                        onChange={setSelectedY}
                        style={{ width: '100%' }}
                        disabled={!activeDataset}
                        allowClear
                      &gt;
                        {getVariableOptions(numericVariables)}
                      &lt;/Select&gt;
                    &lt;/FormItem&gt;
                  )}
                &lt;/div&gt;

                &lt;FormItem label="图表标题"&gt;
                  &lt;Input
                    placeholder="请输入图表标题"
                    value={chartTitle}
                    onChange={setChartTitle}
                    disabled={!activeDataset}
                  /&gt;
                &lt;/FormItem&gt;

                &lt;div className="setup-actions"&gt;
                  &lt;Space&gt;
                    &lt;Button
                      type="primary"
                      icon={&lt;IconPlayArrow /&gt;}
                      onClick={handleGenerateChart}
                      loading={loading}
                      disabled={!activeDataset || !selectedX}
                      size="large"
                    &gt;
                      生成图表
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
              &lt;/Form&gt;
            &lt;/div&gt;
          &lt;/Card&gt;
        &lt;/TabPane&gt;

        &lt;TabPane key="chart" title="图表" disabled={!chartOption}&gt;
          &lt;Card
            extra={
              &lt;Button icon={&lt;IconDownload /&gt;} onClick={handleDownload}&gt;
                下载图表
              &lt;/Button&gt;
            }
          &gt;
            &lt;div className="chart-container"&gt;
              {loading ? (
                &lt;div className="loading-container"&gt;
                  &lt;Spin size={40} /&gt;
                  &lt;p&gt;正在生成图表...&lt;/p&gt;
                &lt;/div&gt;
              ) : chartOption ? (
                &lt;ReactECharts
                  ref={chartRef}
                  option={chartOption}
                  style={{ height: '600px', width: '100%' }}
                  notMerge={true}
                  lazyUpdate={true}
                /&gt;
              ) : (
                &lt;div className="empty-chart"&gt;
                  &lt;p&gt;请先设置并生成图表&lt;/p&gt;
                &lt;/div&gt;
              )}
            &lt;/div&gt;
          &lt;/Card&gt;
        &lt;/TabPane&gt;
      &lt;/Tabs&gt;
    &lt;/div&gt;
  )
}

export default DataVisualizer
