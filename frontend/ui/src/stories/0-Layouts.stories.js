/** @jsx jsx */
import { jsx } from "theme-ui";

import Wrapper from "../layout/wrapper";
import Main, { StickyHeaderMain } from "../layout/main";
import LoremIpsum from "../dev/loremipsum";
import { ExampleMenu as Nav } from "./2-MainMenu.stories";

export default {
  title: "Layouts",
};

const SBWrapper = ({ children }) => <Wrapper nav={<Nav />}>{children}</Wrapper>;

const DummyText = ({ paragraphs = 30 }) => (
  <LoremIpsum paragraphs={paragraphs} />
);
const Header = () => <h1>I am the header</h1>;
const Footer = () => <h3>I am the footer</h3>;

export const main = () => {
  return (
    <SBWrapper>
      <Main
        header={<Header />}
        footer={<Footer />}
        content_variant="layout.text_content"
      >
        <LoremIpsum paragraphs={10} />
      </Main>
    </SBWrapper>
  );
};

export const stickyHeaderAndFooter = () => {
  return (
    <SBWrapper>
      <StickyHeaderMain header={<Header />} footer={<Footer />}>
        <DummyText />
      </StickyHeaderMain>
    </SBWrapper>
  );
};
