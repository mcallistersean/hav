import React from "react";

export default props => {
  return <button>{props.title || "Button"}</button>;
};
