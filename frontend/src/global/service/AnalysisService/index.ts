import { Subject } from 'rxjs'

type AnalysisEvent = { msg: 'analysis' }

const startAnalysis$ = new Subject<AnalysisEvent>()

const AnalysisService = {
  onAnalysis$: () => startAnalysis$.asObservable(),

  startAnalysis: (event: AnalysisEvent) => startAnalysis$.next(event),
}

export default AnalysisService
