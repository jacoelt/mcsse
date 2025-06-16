import { InputLabel, Slider, Stack } from "@mui/material";
import React from "react";


export function RangeSlider({ label, onChange, min, max }: {
  label: string;
  onChange: (newValue: number[]) => void;
  min: number;
  max: number;
}) {

  const [value, setValue] = React.useState<number[]>([min, max]);

  const onChangeWrapper = (_: Event, newValue: number[]) => {
    if (Array.isArray(newValue)) {
      setValue(newValue);
      onChange(newValue);
    }
  }

  return (
    <Stack direction="row" spacing={3}>
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