import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import App from "./App";

afterEach(() => {
  cleanup();
  localStorage.removeItem("kids.admin_locale.v1");
  window.history.pushState({}, "", "/");
});

describe("product shells", () => {
  it("publishes adult-directed bilingual safety and privacy surfaces", async () => {
    window.history.pushState({}, "", "/welcome?lang=es-US");
    render(<App/>);
    expect(await screen.findByRole("heading", { name: /Ideas claras para aprender juntos/ })).toBeTruthy();
    expect(screen.getAllByRole("link", { name: "Seguridad" })[0].getAttribute("href")).toBe("/safety");
    cleanup();
    window.history.pushState({}, "", "/privacy?lang=es-US");
    render(<App/>);
    expect(await screen.findByRole("heading", { name: "Aviso de privacidad del piloto" })).toBeTruthy();
    expect(screen.getByText(/requiere revisión legal cualificada/i)).toBeTruthy();
  });

  it("offers one companion in preparation before opening the adult gate", async () => {
    window.history.pushState({}, "", "/");
    render(<App/>);
    expect(await screen.findByRole("heading", { name: "Una idea clara para aprender juntos." })).toBeTruthy();
    expect(document.querySelectorAll(".companion-fab")).toHaveLength(0);
    fireEvent.click(screen.getByRole("button", { name: "Preparar actividad" }));
    expect(await screen.findByRole("heading", { name: "Revisa y adapta la actividad" })).toBeTruthy();
    expect(document.querySelectorAll(".companion-fab")).toHaveLength(1);
    expect(document.querySelectorAll(".gate-question")).toHaveLength(0);
    fireEvent.click(screen.getByRole("button", { name: "Confirmar presencia adulta e iniciar" }));
    expect(await screen.findByRole("heading", { name: "Confirma las tres asociaciones" })).toBeTruthy();
    expect(document.querySelectorAll(".gate-question")).toHaveLength(3);
  });

  it("starts the exact activity only after all adult-gate answers are submitted", async () => {
    render(<App/>);
    fireEvent.click(await screen.findByRole("button", { name: "Preparar actividad" }));
    await screen.findByRole("heading", { name: "Revisa y adapta la actividad" });
    fireEvent.click(screen.getByRole("button", { name: "Confirmar presencia adulta e iniciar" }));
    await screen.findByRole("heading", { name: "Confirma las tres asociaciones" });
    const questions = document.querySelectorAll(".gate-question");
    questions.forEach(question => fireEvent.click(question.querySelector("input")!));
    fireEvent.click(screen.getByRole("button", { name: "Desbloquear 15 minutos" }));
    expect(await screen.findByText("Versión exacta · ACT-0001@1.0.0")).toBeTruthy();
    expect(document.querySelectorAll(".companion-fab")).toHaveLength(1);
  });

  it("renders the owner workspace and operation routing matrix", async () => {
    window.history.pushState({}, "", "/admin");
    render(<App/>);
    expect(await screen.findByRole("heading", { name: "Resumen" })).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: /Operaciones IA/ }));
    await waitFor(() => expect(document.querySelectorAll(".route-table .table-row")).toHaveLength(14));
    expect(screen.getAllByText("No usa IA").length).toBeGreaterThanOrEqual(2);
  });

  it("switches the complete administrative workspace to English", async () => {
    window.history.pushState({}, "", "/admin?lang=en-US");
    render(<App/>);

    expect(await screen.findByRole("heading", { name: "Overview" })).toBeTruthy();
    expect(screen.getByRole("combobox", { name: "Workspace language" })).toHaveProperty("value", "en-US");
    expect(screen.getByText("12 eligible")).toBeTruthy();
    expect(screen.getByText("There is no eligible Physics activity for ages 5-6.")).toBeTruthy();
    expect(screen.queryByText("Huecos")).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: /AI operations/ }));
    await waitFor(() => expect(document.querySelectorAll(".route-table .table-row")).toHaveLength(14));
    expect(screen.getByRole("heading", { name: "Endpoints and routing" })).toBeTruthy();
    expect(screen.getAllByText("Does not use AI").length).toBeGreaterThanOrEqual(2);
  });
});
