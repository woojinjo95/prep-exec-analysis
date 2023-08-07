import React from 'react'

interface TitleProps {
  as: 'h1' | 'h2' | 'h3'
  children: React.ReactNode
}

const Title: React.FC<TitleProps> = ({ as = 'h1', children }) => {
  if (as === 'h3') {
    return <h3 className="text-lg">{children}</h3>
  }
  if (as === 'h2') {
    return <h2 className="text-xl">{children}</h2>
  }
  return <h1 className="text-2xl">{children}</h1>
}

export default Title
