import Cookies from "js-cookie";
import { jwtDecode } from "jwt-decode";
import {
  Stack,
  AppBar,
  Toolbar,
  IconButton,
  Avatar,
  Typography,
  Popover,
  Box,
} from "@mui/material";
import WebChatComponent from "./WebChatV2";
import { styled } from "@mui/material/styles";
import LogoutIcon from "@mui/icons-material/Logout";
import { useState, useEffect } from "react";

const DrawerHeader = styled("div")(({ theme }) => ({
  display: "flex",
  alignItems: "center",
  justifyContent: "flex-end",
  padding: theme.spacing(0, 1),
  ...theme.mixins.toolbar,
}));

const Navbar = () => {
  const [name, setName] = useState("Guest");
  const [anchorEl, setAnchorEl] = useState(null);
  const token = Cookies.get("token");
  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  console.log("at startno name", name)
  const extractToken = async () =>{
    try {
      const decodedToken = await jwtDecode(token);
      if (decodedToken && decodedToken?.name) {
        await setName(decodedToken.name);
      } else {
        console.error("Name not found in token");
      }
    } catch (error) {
      console.error("Error decoding token:", error);
    }
  }
  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    console.log("Logout clicked");
  };

  useEffect(() => {
    if (token) {
      extractToken();
    } else {
      console.warn("No token found in cookies");
    }
  }, [token]);

  console.log("extraced name", name)
  const open = Boolean(anchorEl);
  const id = open ? "simple-popover" : undefined;

  const extractInitials = (fullName = "") => {
    if (!fullName) return "N/A";
    const nameParts = fullName.split(" ");
    if (nameParts.length > 1) {
      const firstNameInitial = nameParts[0].charAt(0).toUpperCase();
      const lastNameInitial = nameParts[1].charAt(0).toUpperCase();
      return `${firstNameInitial}${lastNameInitial}`;
    }
    return nameParts[0].charAt(0).toUpperCase();
  };

  return (
    <>
      <DrawerHeader className="hidden-on-print">
        <AppBar position="fixed" sx={{ bgcolor: "#fff" }}>
          <Toolbar sx={{ px: 2 }}>
            <Stack direction="row" alignItems="center">
              <p
                style={{
                  color: "black",
                  fontFamily: "Poppins, sans-serif !important",
                  fontSize: "18px",
                  margin: 0,
                  width: "max-content",
                  fontWeight: 600,
                }}
              >
                Smart Bot
              </p>
            </Stack>
            <Stack
              direction="row"
              justifyContent="flex-end"
              width={"100%"}
              alignItems="center"
            >
              <IconButton
                size="large"
                onClick={handleLogout}
                sx={{
                  ".MuiSvgIcon-root": {
                    color: "#000 !important",
                  },
                }}
              >
                <LogoutIcon />
              </IconButton>
              <IconButton onClick={handleClick}>
                <Avatar
                  sx={{
                    background: "#0078d75e",
                    fontSize: "14px",
                    height: "34px",
                    width: "34px",
                    color: "black",
                    padding: "2px",
                  }}
                  alt={extractInitials(name)}
                >
                  {extractInitials(name)}
                </Avatar>
              </IconButton>
              <Popover
                id={id}
                open={open}
                anchorEl={anchorEl}
                onClose={handleClose}
                anchorOrigin={{
                  vertical: "bottom",
                  horizontal: "center",
                }}
                transformOrigin={{
                  vertical: "top",
                  horizontal: "center",
                }}
              >
                <Box sx={{ p: 2, minWidth: 150, textAlign: "center" }}>
                  <Typography variant="body1">
                    Hello {extractInitials(name)}!
                  </Typography>
                </Box>
              </Popover>
            </Stack>
          </Toolbar>
        </AppBar>
      </DrawerHeader>
      <WebChatComponent name={name} token={token} />
    </>
  );
};

export default Navbar;

