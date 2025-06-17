import { Box, Chip, FormControl, InputLabel, MenuItem, OutlinedInput, Select, Tooltip, useTheme, type SelectChangeEvent, type Theme } from "@mui/material";
import React from "react";
import type { SelectItem } from "../../types/SelectItem";


const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
  PaperProps: {
    style: {
      maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
      width: 250,
    },
  },
};

// Dynamic styles based on selection
function getStyles(item: string, selectedItems: readonly string[], theme: Theme) {
  return {
    fontWeight: selectedItems.includes(item)
      ? theme.typography.fontWeightMedium
      : theme.typography.fontWeightRegular,
  };
}


export default function SelectMultiple({label, itemList, onChange, sx}: {label: string, itemList: SelectItem[], onChange: (selection: SelectItem[]) => void, sx?: React.CSSProperties}) {
  const theme = useTheme();
  const [selection, setSelection] = React.useState<string[]>([]);

  const onChangeWrapper = (event: SelectChangeEvent<typeof selection>) => {
    const {
      target: { value },
    } = event;
    const valueArray = typeof value === 'string' ? value.split(',') : value;
    setSelection(valueArray);
    // Convert valueArray to SelectItem[]
    const selectedItems = valueArray.map((val) => {
      const item = itemList.find(item => item.value === val);
      return item ? { label: item.label, value: item.value } : { label: val, value: val };
    });
    onChange(selectedItems);
  };

  const getTooltip = (value: string) => {
    const item = itemList.find(item => item.value === value);
    return item?.tooltip || "";
  };

  const getChip = (value: string) => {
    const item = itemList.find(item => item.value === value);
    return item?.chip || item?.label || value;
  };

  return (
    <FormControl sx={{ ...sx }}>
      <InputLabel>{label}</InputLabel>
      <Select
        multiple
        value={selection}
        onChange={onChangeWrapper}
        input={<OutlinedInput id="select-multiple-chip" label={label} />}
        renderValue={(selected) => (
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
            {selected.map((value) => (
              <Tooltip key={value} title={getTooltip(value)} placement="top">
                <Chip key={value} label={getChip(value)} />
              </Tooltip>
            ))}
          </Box>
        )}
        MenuProps={MenuProps}
      >
        {itemList.map((item) => (
          <MenuItem
            key={item.value}
            value={item.value}
            style={getStyles(item.label || item.value, selection, theme)}
          >
            {item.label || item.value}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  )
}