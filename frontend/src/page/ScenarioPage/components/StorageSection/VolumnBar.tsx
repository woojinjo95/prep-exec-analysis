import { contentColors } from '@page/ScenarioPage/constants'
import React, { useEffect, useRef, useState } from 'react'

interface VolumnBarProps {
  storageItems: { name: string; volumn: number; fileNum: number }[]
  total: number
}

const VolumnBar: React.FC<VolumnBarProps> = ({ storageItems, total }) => {
  const barRef = useRef<HTMLDivElement | null>(null)

  const [barWidth, setBarWidh] = useState<number | null>(null)

  useEffect(() => {
    const getBarWidth = () => {
      if (barRef.current) {
        setBarWidh(barRef.current?.offsetWidth)
      }
    }

    getBarWidth()

    window.addEventListener('resize', getBarWidth)

    return () => {
      window.removeEventListener('resize', getBarWidth)
    }
  }, [])

  return (
    <div className="w-full h-3 relative bg-light-grey rounded-md" ref={barRef}>
      {barWidth &&
        storageItems.map((storageItem, idx) => {
          const volumnSum: number = storageItems
            .slice(0, idx + 1)
            .map((item) => item.volumn)
            .reduce((acc, cur) => acc + cur, 0)

          const width = barWidth * (volumnSum / total)

          return (
            <div
              style={{ width, zIndex: 10 - idx }}
              className={`h-full absolute rounded-md top-0 left-0 bg-${contentColors[storageItem.name]}`}
              key={`bar_${storageItem.name}`}
            />
          )
        })}
    </div>
  )
}

export default VolumnBar
