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

export function SelectSimple({label, itemList, onChange, sx}: {label: string, itemList: SelectItem[], onChange: (selection: SelectItem) => void, sx?: React.CSSProperties}) {
  const theme = useTheme();
  const [selection, setSelection] = React.useState<string>("");

  const onChangeWrapper = (event: SelectChangeEvent<typeof selection>) => {
    const {
      target: { value: stringValue },
    } = event;
    // Find the selected item in the itemList
    const selectedItem = itemList.find(item => item.value === stringValue) || { value: stringValue, label: stringValue } as SelectItem;
    setSelection(selectedItem.value);
    onChange(selectedItem);
  };

  return (
    <FormControl sx={{ ...sx }}>
      <InputLabel>{label}</InputLabel>
      <Select
        value={selection}
        label={label}
        onChange={onChangeWrapper}
      >
        <MenuItem value="" sx={{ fontStyle: "italic" }}>None</MenuItem>

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