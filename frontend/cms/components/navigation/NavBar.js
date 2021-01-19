import React, { useState } from "react";

import { MenuIcon, CloseIcon } from "../icons";
import ActiveLink from "./Link";
import { useCollection, useAPI } from "hooks";

const MutedText = ({ children }) => (
  <span className="text-base text-gray-500">{children}</span>
);

const Link = (props) => {
  return (
    <ActiveLink
      className="hover:underline"
      activeClassName="underline"
      {...props}
    />
  );
};

const AccountNav = () => {
  const { data = {} } = useAPI("/api/rest/v1/auth/");
  const { loginURL = "", logoutURL = "" } = data;
  const { username, email } = data?.user || {};
  return (
    <>
      <MutedText>Account</MutedText>

      <ul>
        {username ? (
          <>
            <li>{username}</li>
            <li>
              <a href={logoutURL}>Logout</a>
            </li>
          </>
        ) : (
          <li>
            <a href={loginURL}>Login</a>
          </li>
        )}
      </ul>
    </>
  );
};

const CollectionNav = ({ collection: { slug, shortName, rootNode } }) => {
  return (
    <ul>
      <li>
        <MutedText>
          <Link href="/">
            <a>← All Collections</a>
          </Link>
        </MutedText>
      </li>
      <li>
        <Link href={`/collections/${slug}/`}>
          <a>{shortName}</a>
        </Link>
      </li>
      <li>
        <Link
          href={`/collections/${slug}/browse/`}
          additionalPaths={[`/collections/${slug}/media/`]}
          exact={false}
        >
          <a>Browse</a>
        </Link>
      </li>
      <li>
        <Link href={`/collections/${slug}/search/`} exact={false}>
          <a>Search</a>
        </Link>
      </li>
    </ul>
  );
};

const GlobalNav = ({ collections = [] }) => {
  return (
    <ul>
      <li>
        <Link href="/">
          <a>Home</a>
        </Link>
        <ul>
          <li>
            <Link href="/cooperation/">
              <a>How to cooperate</a>
            </Link>
          </li>

          <li>
            <Link href="/open-knowledge/">
              <a>License Models</a>
            </Link>
          </li>
        </ul>
      </li>

      <li className="md:mt-2">
        <MutedText>Collections</MutedText>
        <ul>
          {collections.map((c) => (
            <li key={c.slug}>
              <Link href={`/collections/${c.slug}/`}>
                <a>{c.shortName}</a>
              </Link>
            </li>
          ))}
        </ul>
      </li>
    </ul>
  );
};

const NavBar = () => {
  const [navVisible, setNavVisibility] = useState(false);
  const collection_slug = useCollection();
  const { data = [] } = useAPI("/api/collections/");
  const collection = data.find((c) => c.slug === collection_slug);

  return (
    <div className="md:flex md:flex-col md:h-full p-4 text-xl font-serif">
      <div className="flex flex-row justify-between">
        <div className="flex-grow">
          <Link href="/">
            <a>
              <img
                className="block h-8 md:h-20 w-auto md:mx-auto"
                src="/logos/hav.svg"
              />
            </a>
          </Link>
        </div>
        <div className="flex-none text-2xl md:hidden">
          <button onClick={() => setNavVisibility(!navVisible)}>
            {navVisible ? <CloseIcon /> : <MenuIcon />}
          </button>
        </div>
      </div>

      <nav
        className={`md:flex-grow md:flex md:flex-col md:justify-between md:mt-8 md:text-right ${
          navVisible ? "" : "hidden"
        }`}
      >
        {collection ? (
          <CollectionNav collection={collection} />
        ) : (
          <GlobalNav collections={data} />
        )}

        {/* Bottom nav */}
        <div>
          <div className="md-mb-4">
            <AccountNav />
          </div>
          <div className="sm:mt-32 text-base text-gray-500">
            <ul>
              <li className="flex flex-row flex-wrap justify-between">
                <img className="block h-8 w-auto" src="/logos/cirdis.svg" />
                <img className="block h-8 w-auto" src="/logos/univie.svg" />
              </li>
              <li className="flex flex-row flex-wrap justify-between md:mt-10">
                <a
                  className="block"
                  href="https://dsba.univie.ac.at/fileadmin/user_upload/p_dsba/datenschutzerklaerung_websites_V04_26062020_EN.pdf"
                >
                  Privacy Policy
                </a>{" "}
                <Link href="/imprint/">
                  <a className="block">Imprint</a>
                </Link>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </div>
  );
};

export default NavBar;
