import React from "react";

import { ThemeProvider } from "theme-ui";
import theme from "./theme";

export default props => {
  console.log(props);
  return <ThemeProvider theme={theme}>{props.children}</ThemeProvider>;
};
