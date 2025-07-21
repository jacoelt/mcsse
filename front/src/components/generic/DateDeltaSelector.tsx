import { InputLabel, Slider, Stack } from "@mui/material";
import type { DateDelta } from "../../types/SearchValuesList";
import { useEffect, useState } from "react";


interface DateDeltaSelectorProps {
  label: string;
  value: number; // Currently selected value
  onChange: (value: number) => void; // Callback to handle the change
  valueList: DateDelta[]; // List of date deltas with labels and values
  sx?: React.CSSProperties;
}


export function DateDeltaSelector({ label, value, onChange, valueList, sx }: DateDeltaSelectorProps) {

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
    <Stack direction="row" spacing={3} sx={{ ...sx, width: 'calc(100% - 30px)' }}>
      <InputLabel sx={{ whiteSpace: 'nowrap', overflow: 'visible' }}>{label}</InputLabel>

      <Slider
        value={currentIndex}
        onChange={onChangeWrapper}
        valueLabelDisplay="on"
        step={1}
        min={0}
        max={valueList.length - 1}
        marks={[...Array(valueList.length).keys()].map(i => ({
          value: i,
          label: "",
        }))}
        aria-labelledby="range-slider"
        getAriaLabel={valueLabel}
        getAriaValueText={valueLabel}
        valueLabelFormat={valueLabel}
      />
    </Stack>
  );
}