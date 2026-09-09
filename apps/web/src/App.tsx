import AdminApp from "./AdminApp";
import FamilyApp from "./FamilyExperienceApp";
import PublicSite from "./PublicSite";

export default function App() {
  const path = window.location.pathname.replace(/\/$/, "") || "/";
  const publicPage = ({ "/welcome": "welcome", "/privacy": "privacy", "/terms": "terms", "/safety": "safety" } as const)[path as "/welcome" | "/privacy" | "/terms" | "/safety"];
  if (publicPage) return <PublicSite page={publicPage}/>;
  const admin = path.startsWith("/admin") || new URLSearchParams(window.location.search).get("view") === "admin";
  return admin ? <AdminApp/> : <FamilyApp/>;
}
