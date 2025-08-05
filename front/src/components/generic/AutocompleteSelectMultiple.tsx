import { Autocomplete, Box, Checkbox, Chip, TextField, Tooltip } from "@mui/material";
import React, { type SyntheticEvent } from "react";
import type { SelectItem } from "../../types/SelectItem";

import CheckBoxOutlineBlankIcon from '@mui/icons-material/CheckBoxOutlineBlank';
import CheckBoxIcon from '@mui/icons-material/CheckBox';
import { Cancel } from "@mui/icons-material";


interface AutocompleteSelectMultipleProps {
  label: string;
  isLoading: boolean;
  itemList: SelectItem[];
  selection: string[];
  onChange: (selection: string[]) => void;
  sx?: React.CSSProperties;
}

export default function AutocompleteSelectMultiple({ label, isLoading, itemList, onChange, selection, sx }: AutocompleteSelectMultipleProps) {

  const onChangeWrapper = (_: SyntheticEvent, newValue: SelectItem[]) => {
    onChange(newValue.map(item => item.value));
  };

  return (
    <Autocomplete
      sx={{ ...sx }}
      value={selection.map(value => itemList.find(item => item.value === value) || { value, label: value })}
      onChange={(event, newValue) => { onChangeWrapper(event, newValue) }}
      multiple
      disableCloseOnSelect
      options={isLoading ? [{ label: "Loading...", value: "" }] : itemList}
      getOptionDisabled={() => isLoading}
      getOptionLabel={(option) => option.label || option.value}
      renderInput={(params) => (
        <TextField
          {...params}
          label={label}
          variant="outlined"
          placeholder="Select items"
        />
      )}
      renderValue={(selected) => (
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
          {itemList.filter(item => selected.includes(item)).map((item) => (
            <Tooltip key={item.value} title={item.tooltip || ""} placement="top">
              <Chip
                key={item.value}
                label={item?.chip || item?.label || item.value}
                deleteIcon={
                  <Cancel
                    onMouseDown={(event) => event.stopPropagation()} // Prevents the select from catching the click event when clicking the delete icon
                  />
                }
                onDelete={
                  () => {
                    onChange(selection.filter(value => value !== item.value));
                  }
                }
              />
            </Tooltip>
          ))}
        </Box>
      )}
      renderOption={(props, option, { selected }) => {
        const { key, ...optionProps } = props;
        return (
          <li key={key} {...optionProps}>
            <Checkbox
              icon={<CheckBoxOutlineBlankIcon fontSize="small" />}
              checkedIcon={<CheckBoxIcon fontSize="small" />}
              style={{ marginRight: 8 }}
              checked={selected}
            />
            {option.label || option.value}
          </li>
        );
      }}
    />
  )
  // const theme = useTheme();

  // const onChangeWrapper = (event: SelectChangeEvent<typeof selection>) => {
  //   const {
  //     target: { value },
  //   } = event;
  //   onChange(typeof value === 'string' ? [value] : value);
  // };

  // const getTooltip = (value: string) => {
  //   const item = itemList.find(item => item.value === value);
  //   return item?.tooltip || "";
  // };

  // const getChip = (value: string) => {
  //   const item = itemList.find(item => item.value === value);
  //   return item?.chip || item?.label || value;
  // };

  // return (
  //   <FormControl sx={{ ...sx }}>
  //     <InputLabel>{label}</InputLabel>
  //     <Select
  //       multiple
  //       value={selection}
  //       onChange={onChangeWrapper}
  //       input={<OutlinedInput id="select-multiple-chip" label={label} />}
  //       renderValue={(selected) => (
  //         <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
  //           {selected.map((value) => (
  //             <Tooltip key={value} title={getTooltip(value)} placement="top">
  //               <Chip
  //                 key={value}
  //                 label={getChip(value)}
  //                 deleteIcon={
  //                   <Cancel
  //                     onMouseDown={(event) => event.stopPropagation()} // Prevents the select from catching the click event when clicking the delete icon
  //                   />
  //                 }
  //                 onDelete={
  //                   () => {
  //                     onChange(selection.filter(item => item !== value));
  //                   }
  //                 }
  //               />
  //             </Tooltip>
  //           ))}
  //         </Box>
  //       )}
  //       MenuProps={MenuProps}
  //     >
  //       {isLoading && itemList.length === 0
  //         ? <MenuItem disabled>Loading...</MenuItem>
  //         : itemList.map((item) => (
  //           <MenuItem
  //             key={item.value}
  //             value={item.value}
  //             style={getStyles(item.label || item.value, selection, theme)}
  //           >
  //             {item.label || item.value}
  //           </MenuItem>
  //         ))}
  //     </Select>
  //   </FormControl>
  // )
}