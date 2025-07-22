import { InputLabel, Slider, Stack } from "@mui/material";
import React, { useEffect } from "react";

interface RangeSliderLogProps {
  label: string;
  value: number[];
  onChange: (value: number[]) => void;
  min: number;
  max: number;
  sx?: React.CSSProperties;
}


export function RangeSliderLog({ label, value, onChange, min, max, sx }: RangeSliderLogProps) {

  const scale = function (val: number) {
    if (val <= 0) {
      return 0;
    }
    return Math.ceil(Math.log10(val))
  }

  const unscale = function (val: number) {
    if (val <= 0) {
      return 0;  // 10**0 is 1 but lowest value should be 0
    }
    return Math.pow(10, val);
  }

  const valueLabelFormat = (val: number) => {
    if (val <= 1) {
      return '0';
    }
    return val.toLocaleString();
  }

  const onChangeWrapper = (_: Event, newValue: number[]) => {
    if (Array.isArray(newValue)) {
      const newUnscaledValue = newValue.map((v) => unscale(v));
      onChange(newUnscaledValue);
    }
  }

  return (
    <Stack direction="row" spacing={3} sx={{ ...sx, width: 'calc(100% - 30px)' }}>
      <InputLabel sx={{ whiteSpace: 'nowrap', overflow: 'visible' }}>{label}</InputLabel>

      <Slider
        value={value.map(scale)}
        onChange={onChangeWrapper}
        valueLabelDisplay="on"
        min={scale(min)}
        max={scale(max)}
        step={1}
        marks
        scale={unscale}
        aria-labelledby="range-slider"
        getAriaLabel={() => label}
        getAriaValueText={valueLabelFormat}
        valueLabelFormat={valueLabelFormat}
      />
    </Stack>
  );
}