export interface Block {
  id: number
  title: string
  time: string
}

export type ActionStatus = 'RFC' | 'playing' | 'normal'
