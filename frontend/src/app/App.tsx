import React from 'react'
import { QueryClient, QueryClientProvider } from 'react-query'
import PageRouter from './router'

/**
 * react query
 */
const client = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
    },
  },
})

const App: React.FC = () => {
  return (
    <QueryClientProvider client={client}>
      <PageRouter />
    </QueryClientProvider>
  )
}
export default App
