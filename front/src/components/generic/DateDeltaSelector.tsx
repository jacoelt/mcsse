import { InputLabel, Slider, Stack } from "@mui/material";
import type { DateDelta } from "../../types/SearchValuesList";
import { useEffect, useState } from "react";


interface DateDeltaSelectorProps {
  label: string;
  value: number; // Currently selected value
  onChange: (value: number) => void; // Callback to handle the change
  valueList: DateDelta[]; // List of date deltas with labels and values
}


export function DateDeltaSelector({ label, value, onChange, valueList }: DateDeltaSelectorProps) {

  const [currentIndex, setCurrentIndex] = useState<number>(valueList.length - 1); // Default to the last item in the list);

  useEffect(() => {
    // Update the current index when the value changes
    const index = valueList.findIndex(item => item.value === value);
    if (index !== -1) {
      setCurrentIndex(index);
    }
  }, [value, valueList]);

  const valueLabel = (index: number) => {
    return valueList[index]?.label || "";
  }

  const onChangeWrapper = (_: Event, newValue: number) => {
    setCurrentIndex(newValue);
    onChange(valueList[newValue]?.value)
  };

  return (
    <Stack direction="row" spacing={3}>
      <InputLabel sx={{ whiteSpace: 'nowrap', overflow: 'visible' }}>{label}</InputLabel>

      <Slider
        value={currentIndex}
        onChange={onChangeWrapper}
        step={1}
        min={0}
        max={valueList.length - 1}
        marks={valueList.map((item, index) => ({
          value: index,
          label: item.label,
        }))}
        aria-labelledby="range-slider"
        // scale={calculateValue}
        getAriaLabel={valueLabel}
        getAriaValueText={valueLabel}
      />
    </Stack>
  );
}