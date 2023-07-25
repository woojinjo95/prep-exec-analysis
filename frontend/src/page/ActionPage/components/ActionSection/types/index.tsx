export interface Block {
  id: number
  title: string
  time: string
  refIdx: number
}

export type ActionStatus = 'RFC' | 'playing' | 'normal'
