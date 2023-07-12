import React, { createContext, useMemo, useState } from "react";
import Navigationbar from "./Navbar";
import { useNavigate } from "react-router-dom";
import { ArrowLeftOutlined } from "@ant-design/icons";

export const Context = createContext("unknown");
const Layout = (props) => {
  const { hasNavigationBack } = props;
  const [toaster, setToaster] = useState({
    title: "",
    show: true,
    message: "",
    type: "",
  });

  const value = useMemo(() => ({ toaster, setToaster }), [toaster]);
  const navigate = useNavigate();
  return (
    <Context.Provider value={value}>
    <div>
      <Navigationbar />
      {hasNavigationBack && (
        <ArrowLeftOutlined
          style={{
            color: "#0D6EFD",
            fontSize: "24px",
            marginLeft: "5%",
            marginTop: "1%",
          }}
          onClick={() => navigate(-1)}
        />
      )}
      <div className="container m-5">{props.children}</div>
    </div>
    </Context.Provider>
  );
};

export default Layout;
