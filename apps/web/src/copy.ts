import type { Locale } from "./types";

export const copy = {
  "en-US": {
    loading: "Loading the activity guide…", unavailable: "Activity unavailable", today: "Today’s workshop", minutes: "minutes", children: "children", safety: "safety level", privatePilot: "Private pilot", companion: "Activity companion", happening: "What’s happening?", note: "Describe the problem or ask to adapt this activity. An adult confirms every change.", message: "Your message", placeholder: "The bridge keeps falling…", ask: "Ask companion", checking: "Checking the activity…", choose: "Choose one approved option", confirm: "Confirm change", keep: "Keep current", updated: "Your activity has been updated.", unchanged: "No changes were made.", basedOn: "Based on", close: "Close", signIn: "Adult sign in", email: "Email address", sendLink: "Send magic link", sent: "Check your email for the private sign-in link."
  },
  "es-US": {
    loading: "Cargando la guía…", unavailable: "Actividad no disponible", today: "Taller de hoy", minutes: "minutos", children: "niños", safety: "nivel de seguridad", privatePilot: "Piloto privado", companion: "Asistente de actividad", happening: "¿Qué está pasando?", note: "Describe el problema o pide adaptar esta actividad. Un adulto confirma cada cambio.", message: "Tu mensaje", placeholder: "El puente se sigue cayendo…", ask: "Preguntar al asistente", checking: "Revisando la actividad…", choose: "Elige una opción aprobada", confirm: "Confirmar cambio", keep: "Mantener actual", updated: "La actividad fue actualizada.", unchanged: "No se hicieron cambios.", basedOn: "Basado en", close: "Cerrar", signIn: "Acceso para adultos", email: "Correo electrónico", sendLink: "Enviar enlace", sent: "Revisa tu correo para abrir el enlace privado."
  }
} satisfies Record<Locale, Record<string, string>>;
