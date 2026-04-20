import { useState } from 'react'

function resolveIdx(steps, value, fallback) {
  if (value === undefined || value === null || value === '') return fallback
  const i = steps.indexOf(Number(value))
  return i === -1 ? fallback : i
}

export default function LogRangeSlider({ label, steps, minValue, maxValue, onCommit }) {
  const lastIdx = steps.length - 1
  const extMin = resolveIdx(steps, minValue, 0)
  const extMax = resolveIdx(steps, maxValue, lastIdx)

  const [minIdx, setMinIdx] = useState(extMin)
  const [maxIdx, setMaxIdx] = useState(extMax)
  const [syncedMin, setSyncedMin] = useState(extMin)
  const [syncedMax, setSyncedMax] = useState(extMax)

  if (syncedMin !== extMin || syncedMax !== extMax) {
    setSyncedMin(extMin)
    setSyncedMax(extMax)
    setMinIdx(extMin)
    setMaxIdx(extMax)
  }

  function commit(nextMin, nextMax) {
    onCommit({
      min: nextMin === 0 ? undefined : String(steps[nextMin]),
      max: nextMax === lastIdx ? undefined : String(steps[nextMax]),
    })
  }

  function handleMinChange(e) {
    const v = Math.min(Number(e.target.value), maxIdx)
    setMinIdx(v)
  }
  function handleMaxChange(e) {
    const v = Math.max(Number(e.target.value), minIdx)
    setMaxIdx(v)
  }
  function handleRelease() {
    commit(minIdx, maxIdx)
  }

  const minPct = (minIdx / lastIdx) * 100
  const maxPct = (maxIdx / lastIdx) * 100

  const minLabel = minIdx === 0 ? 'Any' : steps[minIdx].toLocaleString()
  const maxLabel = maxIdx === lastIdx
    ? `${steps[lastIdx].toLocaleString()}+`
    : steps[maxIdx].toLocaleString()

  return (
    <div>
      <label className="block text-xs font-medium text-gray-400 mb-1">{label}</label>
      <div className="flex justify-between text-xs text-gray-300 mb-2 tabular-nums">
        <span>{minLabel}</span>
        <span>{maxLabel}</span>
      </div>
      <div className="relative h-5 select-none">
        <div className="absolute left-0 right-0 top-1/2 -translate-y-1/2 h-1 bg-gray-600 rounded" />
        <div
          className="absolute top-1/2 -translate-y-1/2 h-1 bg-emerald-500 rounded"
          style={{ left: `${minPct}%`, right: `${100 - maxPct}%` }}
        />
        <input
          type="range"
          min={0}
          max={lastIdx}
          step={1}
          value={minIdx}
          onChange={handleMinChange}
          onMouseUp={handleRelease}
          onTouchEnd={handleRelease}
          onKeyUp={handleRelease}
          className="log-range-thumb absolute inset-0 w-full h-full appearance-none bg-transparent"
          aria-label={`${label} minimum`}
        />
        <input
          type="range"
          min={0}
          max={lastIdx}
          step={1}
          value={maxIdx}
          onChange={handleMaxChange}
          onMouseUp={handleRelease}
          onTouchEnd={handleRelease}
          onKeyUp={handleRelease}
          className="log-range-thumb absolute inset-0 w-full h-full appearance-none bg-transparent"
          aria-label={`${label} maximum`}
        />
      </div>
    </div>
  )
}
