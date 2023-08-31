import React, { useEffect, useRef } from 'react'

interface UseOutsideRefProps {
  isOpen: boolean
  closeHook: () => void
}

const useOutSideRef: (props: UseOutsideRefProps) => { ref: React.RefObject<HTMLDivElement> } = ({
  isOpen,
  closeHook,
}) => {
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const handleClick = (e: MouseEvent) => {
      if (!ref.current) return
      if (!ref.current.contains(e.target as Node)) {
        closeHook()
      }
    }

    if (isOpen) {
      document.addEventListener('mousedown', handleClick)
    }

    return () => {
      if (isOpen) {
        document.removeEventListener('mousedown', handleClick)
      }
    }
  }, [closeHook, ref])

  return { ref }
}

export default useOutSideRef
