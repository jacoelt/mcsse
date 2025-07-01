import { InputLabel, Slider, Stack } from "@mui/material";
import React from "react";

interface RangeSliderProps {
  label: string;
  value: number[];
  onChange: (value: number[]) => void;
  min: number;
  max: number;
  sx?: React.CSSProperties;
}


export function RangeSlider({ label, value, onChange, min, max, sx }: RangeSliderProps) {

  const onChangeWrapper = (_: Event, newValue: number[]) => {
    if (Array.isArray(newValue)) {
      onChange(newValue);
    }
  }

  return (
    <Stack direction="row" spacing={3} sx={{ ...sx }}>
      <InputLabel sx={{ whiteSpace: 'nowrap', overflow: 'visible' }}>{label}</InputLabel>

      <Slider
        value={value}
        onChange={onChangeWrapper}
        valueLabelDisplay="on"
        min={min}
        max={max}
        aria-labelledby="range-slider"
        getAriaLabel={() => label}
      />
    </Stack>
  );
}