import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import "./styles.css";
import "./proposal.css";
import "./login.css";
import "./family.css";
import "./admin.css";
import "./family-runtime.css";
import "./admin-runtime.css";
import "./public.css";

createRoot(document.getElementById("root")!).render(<StrictMode><App/></StrictMode>);

if ("serviceWorker" in navigator && import.meta.env.PROD) navigator.serviceWorker.register("/sw.js");
