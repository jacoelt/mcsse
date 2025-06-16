import { FormControl, InputLabel, MenuItem, Select, useTheme, type SelectChangeEvent, type Theme } from "@mui/material";
import React from "react";


// Dynamic styles based on selection
function getStyles(item: string, selectedItem: string, theme: Theme) {
  return {
    fontWeight: selectedItem == item
      ? theme.typography.fontWeightMedium
      : theme.typography.fontWeightRegular,
  };
}

export function SelectSimple({label, itemList, onChange}: {label: string, itemList: string[], onChange: (selection: string) => void}) {
  const theme = useTheme();
  const [selection, setSelection] = React.useState<string>("");

  const onChangeWrapper = (event: SelectChangeEvent<typeof selection>) => {
    const {
      target: { value },
    } = event;
    setSelection(value);
    onChange(value);
  };

  return (
    <FormControl>
      <InputLabel>{label}</InputLabel>
      <Select
        value={selection}
        label={label}
        onChange={onChangeWrapper}
      >
        <MenuItem value="" sx={{ fontStyle: "italic" }}>None</MenuItem>

        {itemList.map((item) => (
          <MenuItem
            key={item}
            value={item}
            style={getStyles(item, selection, theme)}
          >
            {item}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
}