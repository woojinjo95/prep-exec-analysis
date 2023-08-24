import React from 'react'
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'

import { DEFAULT_PAGE_PATH } from '@global/constant/index'
import { ActionPage, AnalysisPage, NotFoundPage } from '@page/index'
import PagePath from '@global/constant/pagePath'
import TerminalPage from '@page/TerminalPage'
import ScenarioPage from '@page/ScenarioPage'

/**
 * 페이지 라우트 컴포넌트
 */
const PageRouter: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="*" element={<NotFoundPage />} />
        <Route index element={<Navigate to={DEFAULT_PAGE_PATH} replace />} />

        <Route path={PagePath.action} element={<ActionPage />} />
        <Route path={PagePath.analysis} element={<AnalysisPage />} />
        <Route path={PagePath.terminal} element={<TerminalPage />} />
        <Route path={PagePath.scenario} element={<ScenarioPage />} />
      </Routes>
    </BrowserRouter>
  )
}

export default PageRouter
