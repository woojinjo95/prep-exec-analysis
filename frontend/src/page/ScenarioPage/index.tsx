import { PageContainer } from '@global/ui'
import React from 'react'
import FilesSection from './components/FilesSection'
import StorageSection from './components/StorageSection'

const ScenarioPage: React.FC = () => {
  return (
    <PageContainer className="grid grid-cols-[70%_30%] bg-black">
      <FilesSection />
      <StorageSection />
    </PageContainer>
  )
}

export default ScenarioPage
