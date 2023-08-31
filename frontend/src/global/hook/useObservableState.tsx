import { useEffect, useState } from 'react'
import { Observable, Subscription } from 'rxjs'

interface ObservableStateProps<T, K> {
  obs$: Observable<T>
  input$?: (input$: Observable<T>) => Observable<K>
  initialState?: T | (() => T)
  callback?: (state: T | K | undefined) => void
}

interface ObservableState {
  <T, K = T>(props: ObservableStateProps<T, K> & { initialState?: undefined }): T | K | undefined
  <T, K = T>(props: ObservableStateProps<T, K>): T | K
}

/**
 * observable에 구독하여 값을 가져오는 hook
 *
 * @param obs$ 구독하고자 하는 observable
 * @param input$ 값을 변환하는 pipe
 * @param initialState 값의 초기값 설정
 * @param callback 값이 변경되었을 때 실행할 callback
 * @returns 구독한 state
 */
const useObservableState: ObservableState = <T, K>({
  obs$,
  input$,
  initialState,
  callback,
}: ObservableStateProps<T, K>) => {
  const [state, setState] = useState<T | K | undefined>(
    initialState instanceof Function ? initialState() : initialState,
  )

  useEffect(() => {
    let observableState$: Subscription
    if (input$) {
      observableState$ = obs$.pipe(input$).subscribe(setState)
    } else {
      observableState$ = obs$.subscribe(setState)
    }
    return () => observableState$?.unsubscribe()
  }, [obs$, input$])

  useEffect(() => {
    callback?.(state)
  }, [state])

  return state
}

export default useObservableState
