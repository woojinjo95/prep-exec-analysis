import { useCallback, useEffect, useRef } from 'react'

/**
 * @param mode node: 하위 노드인지 체크, position: 마우스가 영역 밖의 좌표로 클릭하였는지 체크
 * @param onClickOutside ref 밖 영역을 클릭하였을 경우 실행할 callback
 * @returns ref 밖 영역을 확인하는 hook
 */
const useOutsideClick = ({
  mode = 'position',
  onClickOutside,
}: {
  mode?: 'node' | 'position'
  onClickOutside: () => void
}) => {
  const ref = useRef<HTMLDivElement>(null)

  const handleOutsideClick = useCallback(
    (e: MouseEvent) => {
      if (!ref.current || !(e.target instanceof Node)) return

      if (mode === 'node' && !ref.current.contains(e.target)) {
        onClickOutside()
      }
      if (
        mode === 'position' &&
        (e.pageX < ref.current.offsetLeft + window.scrollX ||
          e.pageX > ref.current.offsetLeft + ref.current.offsetWidth + window.scrollX ||
          e.pageY < ref.current.offsetTop + window.scrollY ||
          e.pageY > ref.current.offsetTop + ref.current.offsetHeight + window.scrollY)
      ) {
        onClickOutside()
      }
    },
    [onClickOutside, ref],
  )

  useEffect(() => {
    document.addEventListener('mousedown', handleOutsideClick)

    return () => document.removeEventListener('mousedown', handleOutsideClick)
  }, [handleOutsideClick])

  return { ref }
}

export default useOutsideClick
