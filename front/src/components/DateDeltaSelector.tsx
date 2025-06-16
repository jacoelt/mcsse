import { InputLabel, Slider, Stack } from "@mui/material";
import React from "react";
import type { DateDelta } from "../types/SearchValuesList";


export function DateDeltaSelector({ label, onChange, valueList }: {
  label: string;
  onChange: (newValue: string) => void;
  valueList: DateDelta[];
}) {

  const [value, setValue] = React.useState<number>(valueList.length - 1); // Default to the last item in the list

  // Convert valueList to an array of indices
  const valueListWithIndices = valueList.map((item, index) => ({
    label: item.label,
    value: index,
  }));

  const valueLabel = (index: number) => {
    return valueList[index]?.label || "";
  }

  const onChangeWrapper = (_: Event, newValue: number | number[]) => {
    if (typeof newValue === 'number') {
      setValue(newValue);
      onChange(valueList[newValue]?.value || ""); // Call onChange with the value of the selected item
    }
  };

  return (
    <Stack direction="row" spacing={3}>
      <InputLabel sx={{ whiteSpace: 'nowrap', overflow: 'visible' }}>{label}</InputLabel>

      <Slider
        value={value}
        min={0}
        max={valueList.length - 1}
        onChange={onChangeWrapper}
        step={null}
        marks={valueListWithIndices}
        aria-labelledby="range-slider"
        getAriaLabel={valueLabel}
        getAriaValueText={valueLabel}
      />
    </Stack>
  );
}