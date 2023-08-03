import { debounce } from 'lodash'
import { useEffect, useState } from 'react'

/**
 * 현재 window에서 focus중인 element를 가져오는 hook
 */
const useActiveElement = (callback: (el: Element | null) => void) => {
  const [active, setActive] = useState(document.activeElement)

  const changeActiveElement = debounce((activeEl: Element | null) => {
    setActive(activeEl)
    callback?.(activeEl)
  }, 100)

  const handleFocusIn = () => {
    changeActiveElement(document.activeElement)
  }

  const handleFocusOut = () => {
    changeActiveElement(null)
  }

  useEffect(() => {
    document.addEventListener('focusin', handleFocusIn)
    document.addEventListener('focusout', handleFocusOut)
    return () => {
      document.removeEventListener('focusin', handleFocusIn)
      document.removeEventListener('focusout', handleFocusOut)
    }
  }, [callback])

  return active
}

export default useActiveElement
