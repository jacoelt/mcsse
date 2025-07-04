import { InputLabel, Slider, Stack } from "@mui/material";
import React, { useEffect } from "react";

interface RangeSliderProps {
  label: string;
  value: number[];
  onChange: (value: number[]) => void;
  min: number;
  max: number;
  sx?: React.CSSProperties;
}


export function RangeSlider({ label, value, onChange, min, max, sx }: RangeSliderProps) {

  const scale = function (val: number) {
    if (val <= 0) {
      return 0;
    }
    return Math.ceil(Math.log10(val))
  }

  const unscale = function (val: number) {
    return Math.pow(10, val);
  }

  const [internalValue, setInternalValue] = React.useState(value.map(scale));

  useEffect(() => setInternalValue(value.map(scale)), [value])

  const valueLabelFormat = (val: number) => {
    if (val <= 1) {
      return '0';
    }
    return val.toLocaleString();
  }

  const onChangeWrapper = (_: Event, newValue: number[]) => {
    if (Array.isArray(newValue)) {
      const newUnscaledValue = newValue.map((v) => {
        if (v <= 0) {
          return 0;  // Lowest value appears as 1 because of logarithm scaling, but actually should be 0
        }
        return unscale(v);
      });
      setInternalValue(newValue);
      onChange(newUnscaledValue);
    }
  }

  return (
    <Stack direction="row" spacing={3} sx={{ ...sx }}>
      <InputLabel sx={{ whiteSpace: 'nowrap', overflow: 'visible' }}>{label}</InputLabel>

      <Slider
        value={internalValue}
        onChange={onChangeWrapper}
        valueLabelDisplay="on"
        min={scale(min)}
        max={scale(max)}
        step={1}
        scale={unscale}
        aria-labelledby="range-slider"
        getAriaLabel={() => label}
        getAriaValueText={valueLabelFormat}
        valueLabelFormat={valueLabelFormat}
      />
    </Stack>
  );
}