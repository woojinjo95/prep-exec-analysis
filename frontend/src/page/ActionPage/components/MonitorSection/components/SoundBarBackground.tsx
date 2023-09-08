import React from 'react'

const calculateLKFSColor = (index: number): string => {
  const startValue = index * 2
  const endValue = startValue + 2

  if (endValue <= 10) {
    return '#b93a3a' // red
  }
  if (endValue <= 22) {
    return '#f2cf78' // yellow
  }
  if (endValue <= 26) {
    return '#349137' // green
  }
  if (endValue <= 36) {
    return '#456fd1' // blue, not exist in tailwind config
  }
  return '#89928f' // grey
}

const SoundBarBackground: React.FC = () => (
  <>
    {Array.from(Array(35)).map((_, index) => (
      <div
        className="w-full h-[2%]"
        key={`lkfs-cell-${index}`}
        style={{
          backgroundColor: calculateLKFSColor(index),
        }}
      />
    ))}
  </>
)

export default SoundBarBackground
