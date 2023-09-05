export * from './logModule'

export const LogcatLogLevelColors: {
  [log_level: string]: 'pink' | 'red' | 'orange' | 'yellow' | 'navy' | 'green' | 'grey'
} = {
  S: 'pink',
  F: 'red',
  E: 'orange',
  W: 'yellow',
  I: 'navy',
  D: 'green',
  V: 'grey',
}
