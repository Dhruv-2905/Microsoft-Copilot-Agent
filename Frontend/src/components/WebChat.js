// src/WebChatComponent.js
import React, { useEffect, useState } from "react";
import styleOptions from "./styleOptions";

const WebChatComponent = ({ name, token }) => {
  const [decryptedUsername, setDecryptedUsername] = useState(name || "Unknown");
  const [keycloaktoken, setKeycloakToken] = useState(token || "Invalid token");
  useEffect(() => {
    const loadWebChatScript = () => {
      // console.log("Name1:", name);
      // console.log("Keycloak1", token);
      // console.log("name2:", decryptedUsername);
      // console.log("keycloak2", keycloaktoken);

      return new Promise((resolve, reject) => {
        const script = document.createElement("script");
        script.src =
          "https://cdn.botframework.com/botframework-webchat/latest/webchat.js";
        script.async = true;
        script.onload = () => resolve();
        script.onerror = () => reject("Failed to load WebChat script");
        document.head.appendChild(script);
      });
    };

    const tokenEndpointURL = new URL(
      "<public endpoint url>"
    );


    const locale = document.documentElement.lang || "en";
    const apiVersion = tokenEndpointURL.searchParams.get("api-version");

    const fetchDirectLineData = async () => {
      try {
        setDecryptedUsername(name);
        setKeycloakToken(token);
        // console.log(
        //   "Using decryptedUsername inside fetchDirectLineData:",
        //   decryptedUsername
        // );
        // console.log(
        //   "using decryptkeycloak inside fetchdirectlinedata:",
        //   keycloaktoken
        // );
        const [directLineData, tokenData] = await Promise.all([
          fetch(
            new URL(
              `/powervirtualagents/regionalchannelsettings?api-version=${apiVersion}`,
              tokenEndpointURL
            )
          )
            .then((response) => {
              if (!response.ok)
                throw new Error(
                  "Failed to retrieve regional channel settings."
                );
              return response.json();
            })
            .then(({ channelUrlsById: { directline } }) => directline),
          fetch(tokenEndpointURL)
            .then((response) => {
              if (!response.ok)
                throw new Error("Failed to retrieve Direct Line token.");
              return response.json();
            })
            .then(({ token }) => token),
        ]);

        // Ensure WebChat object is available
        if (!window.WebChat) {
          console.error("WebChat is not loaded properly");
          return;
        }

        const directLine = window.WebChat.createDirectLine({
          domain: new URL("v3/directline", directLineData),
          token: tokenData,
        });

        const decryptToken = (encryptedToken) => {
          try {
            const decoded = atob(encryptedToken.split(".")[1]); 
            return JSON.parse(decoded).username || "Unknown"; 
          } catch (error) {
            console.error("Failed to decrypt token:", error);
            return "Unknown";
          }
        };

        const getCookie = (name) => {
          const match = document.cookie.match(
            new RegExp("(^| )" + name + "=([^;]+)")
          );
          return match ? match[2] : null;
        };

        const jwtToken = getCookie("jwtToken");
        // const decryptedUsername = jwtToken ? decryptToken(jwtToken) : 'Unknown';

        console.log("Decrypt name", decryptedUsername);
        console.log("token inside the function", keycloaktoken);

        const store = window.WebChat.createStore(
          {
            globalVariables: {},
          },
          ({ dispatch }) =>
            (next) =>
            (action) => {
              if (action.type === "DIRECT_LINE/CONNECT_FULFILLED") {
                dispatch({
                  type: "WEB_CHAT/SEND_EVENT",
                  payload: {
                    name: `pvaSetContext`,
                    value: {
                      username: decryptedUsername,
                      token: keycloaktoken,
                    },
                  },
                });
              }
              return next(action);
            }
        );

        const subscription = directLine.connectionStatus$.subscribe({
          next(value) {
            if (value === 2) {
              directLine
                .postActivity({
                  localTimezone:
                    Intl.DateTimeFormat().resolvedOptions().timeZone,
                  locale,
                  name: "startConversation",
                  type: "event",
                })
                .subscribe();

              subscription.unsubscribe();
            }
          },
        });

        window.WebChat.renderWebChat(
          { directLine, locale, styleOptions, store },
          document.getElementById("webchat")
        );

        // Cleanup on component unmount
        return () => {
          if (subscription) {
            subscription.unsubscribe();
          }
        };
      } catch (error) {
        console.error("Error fetching DirectLine data:", error);
      }
    };

    loadWebChatScript()
      .then(() => fetchDirectLineData())
      .catch((error) => console.error(error));
  }, [decryptedUsername]);
  console.log("nameee", name);
  return (
    <div>

      <div
        id="webchat"
        role="main"
        style={{
          height: "calc(100% - 50px)",
          overflow: "hidden",
          position: "fixed",
          top: "50px",
          width: "100%",
        }}
      ></div>
    </div>
  );
};

export default WebChatComponent;
