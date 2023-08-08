export interface RemoconCode {
  name: string
  code_name: string
  pronto_code: string
  coordinate: [number, number, number, number] // x1, y1, x2, y2
  hotkey: string[]
}

export interface CustomKey {
  id: string
  name: string
  custom_code: string[]
  order: number
}

export interface Remocon {
  name: string
  image_path: string
  image_resolution: [number, number] // width, height
  remocon_codes: RemoconCode[]

  custom_keys: CustomKey[]
}
