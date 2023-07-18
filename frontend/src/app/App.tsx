import React from 'react'
import { QueryClient, QueryClientProvider } from 'react-query'
import { ChakraProvider } from '@chakra-ui/react'
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
      <ChakraProvider>
        <PageRouter />
      </ChakraProvider>
    </QueryClientProvider>
  )
}
export default App
