import { AreaChartData } from '../types'

function getRandomInt(_min: number, _max: number) {
  const min = Math.ceil(_min)
  const max = Math.floor(_max)
  return Math.floor(Math.random() * (max - min)) + min
}

export const sampleData: AreaChartData = [
  {
    date: new Date('2023-07-20T05:35:00.000Z'),
    value: getRandomInt(0, 100),
  },
  {
    date: new Date('2023-07-20T06:35:00.000Z'),
    value: getRandomInt(0, 100),
  },
  {
    date: new Date('2023-07-20T07:35:00.000Z'),
    value: getRandomInt(0, 100),
  },
  {
    date: new Date('2023-07-20T08:35:00.000Z'),
    value: getRandomInt(0, 100),
  },
  {
    date: new Date('2023-07-20T09:35:00.000Z'),
    value: getRandomInt(0, 100),
  },
  {
    date: new Date('2023-07-20T10:35:00.000Z'),
    value: getRandomInt(0, 100),
  },
  {
    date: new Date('2023-07-20T11:35:00.000Z'),
    value: getRandomInt(0, 100),
  },
  {
    date: new Date('2023-07-20T12:35:00.000Z'),
    value: getRandomInt(0, 100),
  },
  {
    date: new Date('2023-07-20T13:35:00.000Z'),
    value: getRandomInt(0, 100),
  },
  {
    date: new Date('2023-07-20T14:35:00.000Z'),
    value: getRandomInt(0, 100),
  },
  {
    date: new Date('2023-07-20T15:35:00.000Z'),
    value: getRandomInt(0, 100),
  },
  {
    date: new Date('2023-07-20T16:35:00.000Z'),
    value: getRandomInt(0, 100),
  },
  {
    date: new Date('2023-07-20T17:35:00.000Z'),
    value: getRandomInt(0, 100),
  },
  {
    date: new Date('2023-07-20T18:35:00.000Z'),
    value: getRandomInt(0, 100),
  },
  {
    date: new Date('2023-07-20T19:35:00.000Z'),
    value: getRandomInt(0, 100),
  },
  {
    date: new Date('2023-07-20T20:35:00.000Z'),
    value: getRandomInt(0, 100),
  },
  {
    date: new Date('2023-07-20T21:35:00.000Z'),
    value: getRandomInt(0, 100),
  },
  {
    date: new Date('2023-07-20T22:35:00.000Z'),
    value: getRandomInt(0, 100),
  },
  {
    date: new Date('2023-07-20T23:35:00.000Z'),
    value: getRandomInt(0, 100),
  },
  {
    date: new Date('2023-07-21T00:35:00.000Z'),
    value: getRandomInt(0, 100),
  },
  {
    date: new Date('2023-07-21T01:35:00.000Z'),
    value: getRandomInt(0, 100),
  },
  {
    date: new Date('2023-07-21T02:35:00.000Z'),
    value: getRandomInt(0, 100),
  },
  {
    date: new Date('2023-07-21T03:35:00.000Z'),
    value: getRandomInt(0, 100),
  },
]
