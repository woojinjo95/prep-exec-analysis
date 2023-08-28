import { useCallback, useEffect, useRef } from 'react'

type IntersectHandler = (entry: IntersectionObserverEntry, observer: IntersectionObserver) => void

const useIntersect = (onIntersect: IntersectHandler, options?: IntersectionObserverInit) => {
  const ref = useRef<HTMLDivElement | null>(null)

  const callback = useCallback(
    (entries: IntersectionObserverEntry[], observer: IntersectionObserver) => {
      entries.forEach((entry) => {
        // 관측이 되면 onIntersect 함수 실행
        if (entry.isIntersecting) onIntersect(entry, observer)
      })
    },
    [onIntersect],
  )

  useEffect(() => {
    if (!ref.current) return undefined

    // 정의한 callback + option으로 observer 등록
    const observer = new IntersectionObserver(callback, options)

    // target을 관찰하기 시작
    observer.observe(ref.current)

    return () => {
      observer.disconnect()
    }
  }, [ref, options, callback])

  return ref
}

export default useIntersect
