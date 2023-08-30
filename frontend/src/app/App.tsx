import React from 'react'
import { QueryClient, QueryClientProvider } from 'react-query'
import { ChakraProvider } from '@chakra-ui/react'
import { RecoilRoot } from 'recoil'
import { useWebsocket } from '@global/hook'
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
  useWebsocket({
    onMessage: (message) => {
      if (!message.msg) return
      console.info({ ...message, time: message.time * 1000 })
    },
  })

  return (
    <QueryClientProvider client={client}>
      <RecoilRoot>
        <ChakraProvider>
          <PageRouter />
        </ChakraProvider>
      </RecoilRoot>
    </QueryClientProvider>
  )
}
export default App
