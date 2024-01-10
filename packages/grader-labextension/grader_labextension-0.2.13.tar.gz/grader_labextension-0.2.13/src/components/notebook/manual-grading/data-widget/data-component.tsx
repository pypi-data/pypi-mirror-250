// Copyright (c) 2022, TU Wien
// All rights reserved.
//
// This source code is licensed under the BSD-style license found in the
// LICENSE file in the root directory of this source tree.

import * as React from 'react';
import { Cell } from '@jupyterlab/cells';
import { Box, createTheme, Divider, Grid, Typography } from '@mui/material';
import { CellModel } from '../../model';
import { GradeBook } from '../../../../services/gradebook';
import CssBaseline from '@mui/material/CssBaseline';
import { GlobalObjects } from '../../../../index';
import { ThemeProvider } from '@mui/system';

export interface IDataComponentProps {
  cell: Cell;
  gradebook: GradeBook;
  nbname: string;
}

export const DataComponent = (props: IDataComponentProps) => {
  const nbgraderData = CellModel.getNbgraderData(props.cell.model.metadata);
  const toolData = CellModel.newToolData(nbgraderData, props.cell.model.type);

  const gradableCell =
    toolData.type !== 'readonly' &&
    toolData.type !== 'solution' &&
    toolData.type !== '';

  const [theme, setTheme] = React.useState(
    createTheme({
      palette: { mode: (GlobalObjects.themeManager.isLight(GlobalObjects.themeManager.theme)) ? 'light' : 'dark' }
    })
  );

  GlobalObjects.themeManager.themeChanged.connect(() => {
    const palette = (GlobalObjects.themeManager.isLight(GlobalObjects.themeManager.theme)) ? 'light' : 'dark';
    setTheme(createTheme({ palette: { mode: palette } }));
  }, this);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box>
        <Divider />
        <Box sx={{ mt: 2, mb: 1, ml: 3 }}>
          <Grid container spacing={2}>
            <Grid item>
              <Typography>Type: {toolData.type}</Typography>
            </Grid>

            <Grid item>
              <Typography>ID: {toolData.id}</Typography>
            </Grid>

            {toolData.type === 'tests' && (
              <Grid item>
                <Typography>
                  Autograded Points:{' '}
                  {props.gradebook.getAutoGradeScore(props.nbname, toolData.id)}
                </Typography>
              </Grid>
            )}

            {gradableCell && (
              <Grid item>
                <Typography>Max Points: {toolData.points}</Typography>
              </Grid>
            )}
          </Grid>
        </Box>
      </Box>
    </ThemeProvider>
  );
};
