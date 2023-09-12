import { AnalysisConfig } from '@page/AnalysisPage/api/entity'

/**
 * localstorage에 저장된 분석설정을 가져오는 함수
 */
export const getRememberedConfig = (types: (keyof AnalysisConfig)[]): AnalysisConfig => {
  return types
    .map((type) => ({
      [type]: localStorage.getItem(type)
        ? (JSON.parse(localStorage.getItem(type) as string) as AnalysisConfig[typeof type])
        : undefined,
    }))
    .reduce((acc, curr) => ({ ...acc, ...curr }), {})
}
