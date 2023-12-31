import React from 'react'
import SoundBarBackground from './SoundBarBackground'

interface SoundBarProps {
  value: number
}

const SoundBar: React.FC<SoundBarProps> = ({ value }) => {
  return (
    <div className="flex flex-col justify-between relative h-full">
      <div
        className="absolute top-0 left-0 w-full bg-black z-20 transition-all ease-linear duration-500 opacity-80"
        style={{
          height: `${((Math.abs(value) > 70 ? 70 : Math.abs(value)) / 70) * 100}%`,
        }}
      />
      <SoundBarBackground />
    </div>
  )
}

export default SoundBar
