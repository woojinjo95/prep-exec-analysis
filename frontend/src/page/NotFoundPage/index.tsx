import React from 'react'
import { useNavigate } from 'react-router-dom'
import { DEFAULT_PAGE_PATH } from '@global/constant/index'

/**
 * 존재하지 않는 페이지(404)에 접근할 경우 표시하는 페이지
 */
const NotFoundPage: React.FC = () => {
  const navigate = useNavigate()

  return (
    <div className="fixed top-0 left-0 w-screen h-screen bg-white flex flex-col justify-center items-center">
      <h1>404</h1>
      <h2>Page not found.</h2>

      <button
        type="button"
        className="mt-8"
        onClick={() => {
          navigate(DEFAULT_PAGE_PATH, { replace: true })
        }}
      >
        Go to main page
      </button>
    </div>
  )
}

export default NotFoundPage
