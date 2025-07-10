// src/App.js
import React from "react";
import WebChatComponent from "./components/WebChat";
import Navbar from "./components/Navbar";
import { useKeycloak } from "@react-keycloak/web";
import { useEffect } from "react";
import "./App.css";

// function App() {
//   const { keycloak } = useKeycloak();

  // const setToken = () => {
  //   const token = keycloak?.token;
  //   api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  // };

  // useEffect(() => {
  //   if (keycloak?.authenticated) {
  //     setToken();
  //   }
  // }, [keycloak, keycloak?.authenticated]);

//   return keycloak?.authenticated ? (
//     <div>
//       <Navbar />
//       {/* <WebChatComponent /> */}
//     </div>
//   ) : null;
// }

function App() {
  return (
    <div>
      <Navbar />
      {/* <WebChatComponent /> */}
    </div>
  );
}

export default App;
