
import React, { useState, useEffect } from 'react'
import { Table, Button, Space, Message, Input, Select, Popconfirm, Tag } from '@arco-design/web-react'
import { IconUpload, IconDownload, IconEdit, IconDelete, IconSearch } from '@arco-design/web-react/icon'
import { useAppStore } from '../stores/appStore'
import type { Variable, DataRow } from '../types'
import './DataManager.css'

const { Option } = Select

const DataManager: React.FC = () =&gt; {
  const { currentDataset, setCurrentDataset } = useAppStore()
  const [searchText, setSearchText] = useState('')
  const [selectedRows, setSelectedRows] = useState&lt;string[]&gt;([])
  const [loading, setLoading] = useState(false)

  const handleImportData = async () =&gt; {
    try {
      setLoading(true)
      const result = await window.electronAPI.dialog.openFile([
        { name: 'CSV文件', extensions: ['csv'] },
        { name: 'Excel文件', extensions: ['xlsx', 'xls'] },
        { name: '所有文件', extensions: ['*'] }
      ])

      if (!result.canceled &amp;&amp; result.filePaths.length &gt; 0) {
        const filePath = result.filePaths[0]
        const pythonResult = await window.pythonAPI.loadData(filePath)
        
        if (pythonResult.success) {
          const variables: Variable[] = pythonResult.columns.map((col: string, idx: number) =&gt; ({
            id: `var_${idx}`,
            name: col,
            label: col,
            type: 'numeric',
            measurement: 'scale',
            missing: false
          }))

          const newDataset = {
            id: `dataset_${Date.now()}`,
            name: filePath.split('/').pop() || '未命名数据集',
            variables,
            rows: pythonResult.data,
            createdAt: new Date(),
            modifiedAt: new Date()
          }

          setCurrentDataset(newDataset)
          Message.success('数据导入成功')
        } else {
          Message.error(pythonResult.error || '数据导入失败')
        }
      }
    } catch (error) {
      Message.error('导入数据时出错')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const handleSaveData = async () =&gt; {
    if (!currentDataset) return

    try {
      setLoading(true)
      const result = await window.electronAPI.dialog.saveFile([
        { name: 'CSV文件', extensions: ['csv'] },
        { name: 'Excel文件', extensions: ['xlsx'] }
      ])

      if (!result.canceled &amp;&amp; result.filePath) {
        const pythonResult = await window.pythonAPI.saveData(
          result.filePath,
          currentDataset.rows
        )
        
        if (pythonResult.success) {
          Message.success('数据保存成功')
        } else {
          Message.error(pythonResult.error || '数据保存失败')
        }
      }
    } catch (error) {
      Message.error('保存数据时出错')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const filteredRows = currentDataset?.rows.filter(row =&gt; {
    if (!searchText) return true
    return Object.values(row).some(val =&gt; 
      String(val).toLowerCase().includes(searchText.toLowerCase())
    )
  }) || []

  const columns = currentDataset?.variables.map(variable =&gt; ({
    title: variable.label,
    dataIndex: variable.name,
    key: variable.id,
    width: 150,
    render: (value: any) =&gt; {
      if (value === null || value === undefined) {
        return &lt;Tag color="gray"&gt;缺失&lt;/Tag&gt;
      }
      return String(value)
    }
  })) || []

  return (
    &lt;div className="data-manager"&gt;
      &lt;div className="data-manager-toolbar"&gt;
        &lt;Space&gt;
          &lt;Button 
            type="primary" 
            icon={&lt;IconUpload /&gt;}
            onClick={handleImportData}
            loading={loading}
          &gt;
            导入数据
          &lt;/Button&gt;
          &lt;Button 
            icon={&lt;IconDownload /&gt;}
            onClick={handleSaveData}
            disabled={!currentDataset}
            loading={loading}
          &gt;
            保存数据
          &lt;/Button&gt;
          {selectedRows.length &gt; 0 &amp;&amp; (
            &lt;&gt;
              &lt;Button icon={&lt;IconEdit /&gt;}&gt;
                编辑 ({selectedRows.length})
              &lt;/Button&gt;
              &lt;Popconfirm
                title="确认删除"
                content={`确定要删除选中的 ${selectedRows.length} 行吗？`}
                onOk={() =&gt; {
                  Message.info('删除功能待实现')
                  setSelectedRows([])
                }}
              &gt;
                &lt;Button icon={&lt;IconDelete /&gt;} status="danger"&gt;
                  删除
                &lt;/Button&gt;
              &lt;/Popconfirm&gt;
            &lt;/&gt;
          )}
        &lt;/Space&gt;
        &lt;Space&gt;
          &lt;Input
            placeholder="搜索数据..."
            prefix={&lt;IconSearch /&gt;}
            value={searchText}
            onChange={setSearchText}
            style={{ width: 250 }}
            allowClear
          /&gt;
        &lt;/Space&gt;
      &lt;/div&gt;

      {currentDataset ? (
        &lt;div className="data-manager-content"&gt;
          &lt;div className="data-manager-info"&gt;
            &lt;Space&gt;
              &lt;Tag color="blue"&gt;变量: {currentDataset.variables.length}&lt;/Tag&gt;
              &lt;Tag color="green"&gt;样本: {currentDataset.rows.length}&lt;/Tag&gt;
              &lt;Tag color="orange"&gt;数据集: {currentDataset.name}&lt;/Tag&gt;
            &lt;/Space&gt;
          &lt;/div&gt;
          &lt;Table
            columns={columns}
            data={filteredRows}
            rowKey={(record, index) =&gt; index.toString()}
            rowSelection={{
              type: 'checkbox',
              selectedRowKeys: selectedRows,
              onChange: setSelectedRows
            }}
            pagination={{
              pageSize: 50,
              showTotal: true,
              showPageSize: true,
              pageSizeOptions: ['20', '50', '100', '200']
            }}
            scroll={{ x: true }}
            size="small"
            border
          /&gt;
        &lt;/div&gt;
      ) : (
        &lt;div className="data-manager-empty"&gt;
          &lt;div className="empty-content"&gt;
            &lt;div className="empty-icon"&gt;📊&lt;/div&gt;
            &lt;h3&gt;暂无数据&lt;/h3&gt;
            &lt;p&gt;点击"导入数据"按钮开始分析您的数据&lt;/p&gt;
            &lt;Button 
              type="primary" 
              size="large"
              icon={&lt;IconUpload /&gt;}
              onClick={handleImportData}
            &gt;
              导入数据
            &lt;/Button&gt;
          &lt;/div&gt;
        &lt;/div&gt;
      )}
    &lt;/div&gt;
  )
}

export default DataManager
