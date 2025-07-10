import React, { useEffect, useState } from "react";
import Cookies from "js-cookie";
import { jwtDecode } from "jwt-decode";
import MyImage from "../Source/bot_avatar.jpg";
import UserImage from "../Source/bot_avatar_2.jpg";
import SpeechRecognition, {
  useSpeechRecognition,
} from "react-speech-recognition";
import microphone from "../Source/microphone.png";
import axios from "axios";

const WebChatComponent = ({ name, token }) => {
  const [name2, setName] = useState("");
  const [isValidOrigin, setIsValidOrigin] = useState(false);
  const token2 = Cookies.get("token");
  const locale = document.documentElement.lang || "en";

  // Load authorized domains from .env
  const authorizedDomains = process.env.REACT_APP_AUTHORIZED_DOMAINS
    ? process.env.REACT_APP_AUTHORIZED_DOMAINS.split(",").map((domain) => domain.trim())
    : ["localhost"];
  if (!process.env.REACT_APP_AUTHORIZED_DOMAINS) {
    console.warn(
      "REACT_APP_AUTHORIZED_DOMAINS not set in .env. Using fallback domains:",
      authorizedDomains
    );
  }

  // Function to validate the origin (referrer, parentUrl, or script origin)
  const validateOrigin = () => {
    const isLocalhost = window.location.hostname === "localhost";
    const referrer = document.referrer;
    const urlParams = new URLSearchParams(window.location.search);
    const parentUrl = urlParams.get("parentUrl");
    const currentHost = window.location.hostname;

    // Debug logs to diagnose validation issues
    console.log("Validation Context:");
    console.log("- Current Host:", currentHost);
    console.log("- Referrer:", referrer);
    console.log("- Parent URL:", parentUrl);
    console.log("- Authorized Domains:", authorizedDomains);
    console.log("- Is Localhost:", isLocalhost);
    console.log("- Window Location:", window.location.href);
    console.log("- Script Origin:", document.currentScript?.src || "Unknown");

    // Check if current host is authorized or a subdomain of an authorized domain
    const isValidDomain = authorizedDomains.some(
      (domain) =>
        currentHost === domain || currentHost.endsWith(`.${domain}`)
    );

    // Check if referrer is from an authorized domain
    let isValidReferrer = false;
    if (referrer) {
      try {
        const referrerUrlObj = new URL(referrer);
        isValidReferrer = authorizedDomains.some(
          (domain) =>
            referrerUrlObj.hostname === domain ||
            referrerUrlObj.hostname.endsWith(`.${domain}`)
        );
      } catch (error) {
        console.error("Invalid referrer:", error);
      }
    }

    // Check if parentUrl is from an authorized domain (for localhost or explicit passing)
    let isValidParentUrl = false;
    if (parentUrl) {
      try {
        const parentUrlObj = new URL(decodeURIComponent(parentUrl));
        isValidParentUrl = authorizedDomains.some(
          (domain) =>
            parentUrlObj.hostname === domain ||
            parentUrlObj.hostname.endsWith(`.${domain}`)
        );
      } catch (error) {
        console.error("Invalid parentUrl:", error);
      }
    }

    // Check script origin (for iframe or embedded contexts)
    let isValidScriptOrigin = false;
    if (document.currentScript?.src) {
      try {
        const scriptUrlObj = new URL(document.currentScript.src);
        isValidScriptOrigin = authorizedDomains.some(
          (domain) =>
            scriptUrlObj.hostname === domain ||
            scriptUrlObj.hostname.endsWith(`.${domain}`)
        );
      } catch (error) {
        console.error("Invalid script origin:", error);
      }
    }

    // In localhost mode, allow parentUrl or referrer validation
    if (isLocalhost) {
      const isValid = isValidParentUrl || isValidReferrer || (!referrer && isValidParentUrl);
      console.log("Localhost Validation Result:", isValid);
      return isValid;
    }

    // In production, allow if any of domain, referrer, or script origin is valid
    const isValid = isValidDomain || isValidReferrer || isValidScriptOrigin;
    console.log("Production Validation Result:", {
      isValid,
      isValidDomain,
      isValidReferrer,
      isValidScriptOrigin
    });
    return isValid;
  };

  // Validate origin on component mount
  useEffect(() => {
    const isValid = validateOrigin();
    setIsValidOrigin(isValid);
    console.log("Final Is Valid Origin:", isValid);
  }, []);

  // Decode token and set name
  useEffect(() => {
    const token = Cookies.get("token");
    if (token) {
      try {
        const decodedToken = jwtDecode(token);
        if (decodedToken && decodedToken.name) {
          setName(decodedToken.name);
        } else {
          console.error("Name not found in token");
        }
      } catch (error) {
        console.error("Error decoding token:", error);
      }
    } else {
      console.warn("No token found in cookies");
    }
  }, []);

  const { transcript, listening, resetTranscript } = useSpeechRecognition();

  const startSpeechToText = () => {
    SpeechRecognition.startListening({
      continuous: false,
      language: locale,
    });
  };

  const stopSpeechToText = () => {
    SpeechRecognition.stopListening();
  };

  useEffect(() => {
    if (!listening && transcript) {
      const inputElement = document.querySelector(
        ".webchat__send-box-text-box__input"
      );
      if (inputElement) {
        const setNativeValue = (element, value) => {
          const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
            Object.getPrototypeOf(element),
            "value"
          )?.set;
          if (nativeInputValueSetter) {
            nativeInputValueSetter.call(element, value);
          }
        };

        const currentText = inputElement.value;
        const updatedText = currentText
          ? `${currentText} ${transcript}`
          : transcript;

        setNativeValue(inputElement, updatedText);

        const inputEvent = new Event("input", { bubbles: true });
        inputElement.dispatchEvent(inputEvent);

        const changeEvent = new Event("change", { bubbles: true });
        inputElement.dispatchEvent(changeEvent);
      }

      resetTranscript();
    }
  }, [listening, transcript]);

  useEffect(() => {
    const webChatContainer = document.querySelector(".webchat__send-box__main");
    if (webChatContainer) {
      const sendButton = document.querySelector(".webchat__send-box__button");
      if (sendButton) {
        sendButton.addEventListener("click", () => {
          const inputElement = document.querySelector(
            ".webchat__send-box-text-box__input"
          );
          if (inputElement) {
            const messageToSend = inputElement.value.trim();
            if (messageToSend) {
              inputElement.value = "";
              inputElement.dispatchEvent(new Event("input"));
            }
          }
        });
      }
    }
  }, []);

  const loadWebChatScript = () => {
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

  const styleOptions = {
    hideUploadButton: false,
    microphoneButtonColorOnDictate: "#000",
    hideTelephoneKeypadButton: true,
    showSpokenText: true,
    avatarSize: 40,
    botAvatarBackgroundColor: undefined,
    botAvatarImage: MyImage,
    botAvatarInitials: "",
    userAvatarBackgroundColor: undefined,
    userAvatarImage: UserImage,
    userAvatarInitials: "",
    sendBoxPlaceholder: "Type a message...",
    sendBoxButtonColor: "#0078d7",
    sendBoxBackground: "#f0f0f0",
    bubbleBackground:
      "linear-gradient(102.77deg, #D0E8FB -19.6%, #86B7E0 141.32%)",
    bubbleTextColor: "#000",
    bubbleStyle: {
      boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
    },
    bubbleBorderRadius: "12px",
    bubbleFromUserBackground: "#E6EAEE80",
    bubbleFromUserTextColor: "#356394",
    bubbleFromUserBorderRadius: "12px",
    bubbleFromUserStyle: {
      boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
    },
  };

  useEffect(() => {
    let styleSheet = document.getElementById("glow-animation-styles");
    if (!styleSheet) {
      styleSheet = document.createElement("style");
      styleSheet.id = "glow-animation-styles";
      document.head.appendChild(styleSheet);
    }

    styleSheet.textContent = `
      @keyframes glow {
        0% {
          box-shadow: 0 0 10px rgba(0, 255, 0, 0.35);
        }
        50% {
          box-shadow: 0 0 20px rgba(0, 255, 0, 0.35), 0 0 30px rgba(0, 255, 0, 0.35);
        }
        100% {
          box-shadow: 0 0 30px rgba(0, 255, 0, 0.35), 0 0 60px rgba(0, 255, 0, 0.35);
        }
      }
    `;

    const customButton = document.getElementsByClassName("custom-button");
    if (customButton[0]) {
      customButton[0].style.boxShadow = listening
        ? "0 0 10px 5px rgba(0, 255, 0, 0.35)"
        : "none";
      customButton[0].style.animation = listening
        ? "glow 1.5s infinite alternate"
        : "none";
    }
  }, [listening]);

  const fetchDirectLineData = async () => {
    const tokenEndpointURL = new URL(
        "<endpoint url of copilot>"
    );
    const apiVersion = tokenEndpointURL.searchParams.get("api-version");

    try {
      const axiosInstance = axios.create({
        timeout: 100000,
      });

      const [directLineData, tokenData] = await Promise.all([
        axiosInstance
          .get(
            new URL(
              `/powervirtualagents/regionalchannelsettings?api-version=${apiVersion}`,
              tokenEndpointURL
            ).toString()
          )
          .then((response) => {
            if (response.status !== 200)
              throw new Error("Failed to retrieve regional channel settings.");
            return response.data.channelUrlsById.directline;
          }),
        axiosInstance.get(tokenEndpointURL.toString()).then((response) => {
          if (response.status !== 200)
            throw new Error("Failed to retrieve Direct Line token.");
          return response.data.token;
        }),
      ]);

      if (!window.WebChat) return;

      const directLine = window.WebChat.createDirectLine({
        domain: new URL("v3/directline", directLineData),
        token: tokenData,
      });

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
                  name: "pvaSetContext", 
                  value: {
                    username: name2,
                    token: token2,
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
                localTimezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
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

      const webChatContainer = document.querySelector(
        ".webchat__send-box__main"
      );
      if (webChatContainer) {
        let customButton = document.querySelector(".custom-button");
        if (!customButton) {
          customButton = document.createElement("button");
          customButton.style.backgroundColor = "white";
          customButton.className = "custom-button";
          customButton.style.color = "black";
          customButton.style.border = "none";
          customButton.style.padding = "10px";
          customButton.style.borderRadius = "50px";
          customButton.style.cursor = "pointer";
          customButton.onclick = () => {
            if (listening) {
              stopSpeechToText();
            } else {
              startSpeechToText();
            }
          };

          customButton.addEventListener("mouseover", () => {
            customButton.style.backgroundColor = "#f0f0f0";
          });

          customButton.addEventListener("mouseout", () => {
            customButton.style.backgroundColor = "white";
          });

          const image = document.createElement("img");
          image.src = microphone;
          image.alt = "Button Icon";
          image.style.width = "20px";
          image.style.height = "20px";

          customButton.appendChild(image);
          webChatContainer.appendChild(customButton);
        }
      }

      return () => {
        if (subscription) subscription.unsubscribe();
      };
    } catch (error) {
      console.error("Error fetching DirectLine data:", error);
    }
  };

  useEffect(() => {
    if (isValidOrigin) {
      loadWebChatScript()
        .then(() => name2 && fetchDirectLineData())
        .catch((error) => console.error(error));
    }
  }, [name2, isValidOrigin]);

  // Render nothing or an error message if the origin is invalid
  if (!isValidOrigin) {
    return (
      <div
        style={{
          height: "calc(100% - 50px)",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          position: "fixed",
          top: "50px",
          width: "100%",
          backgroundColor: "#f8f8f8",
        }}
      >
        <p style={{ color: "red", fontSize: "18px", textAlign: "center" }}>
          Access Denied: This chat can only be accessed from an authorized domain.
        </p>
      </div>
    );
  }

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