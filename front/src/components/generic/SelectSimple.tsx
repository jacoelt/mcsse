import { FormControl, InputLabel, MenuItem, Select, useTheme, type SelectChangeEvent, type Theme } from "@mui/material";
import React from "react";
import type { SelectItem } from "../../types/SelectItem";


// Dynamic styles based on selection
function getStyles(item: string, selectedItem: string, theme: Theme) {
  return {
    fontWeight: selectedItem == item
      ? theme.typography.fontWeightMedium
      : theme.typography.fontWeightRegular,
  };
}

interface SelectSimpleProps {
  label: string;
  itemList: SelectItem[];
  selection: string;
  onChange: (selection: string) => void;
  sx?: React.CSSProperties;
}

export function SelectSimple({ label, itemList, selection, onChange, sx }: SelectSimpleProps) {
  const theme = useTheme();

  const onChangeWrapper = (event: SelectChangeEvent<typeof selection>) => {
    const {
      target: { value },
    } = event;
    onChange(value);
  };

  return (
    <FormControl sx={{ ...sx }}>
      <InputLabel>{label}</InputLabel>
      <Select
        value={selection}
        label={label}
        onChange={onChangeWrapper}
      >
        {itemList.map((item) => (
          <MenuItem
            key={item.value}
            value={item.value}
            style={getStyles(item.value, selection, theme)}
          >
            {item.label || item.value}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
}