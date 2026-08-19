> **Histórico — documento en español.** Archivado el 18 de agosto de 2026. La especificación vigente está en [English canonical document](../../../../docs/04-ux/activity-facilitation-model.md); no agregar requisitos, decisiones ni cambios nuevos a este registro.

# SPEC-UX-04 — Modelo de facilitación de actividades

**Estado:** Review
**Versión:** 0.1
**Propietario:** Producto/UX/Pedagogía/Contenido

## 1. Propósito

Definir cómo la aplicación transforma una `ActivityVersion` extensa en una guía móvil que conserva intención pedagógica, precisión, participación de todos los niños y seguridad sin copiar el documento editorial completo a la pantalla.

La interfaz no resume eliminando significado. Organiza la misma información en tres momentos:

1. **Comprender antes:** qué aprenderán, por qué funciona y qué decisión pertenece a los niños.
2. **Facilitar durante:** qué hace el adulto, qué dice, qué hace cada participante y qué observar.
3. **Registrar después:** una señal contextual por niño sobre su foco principal.

Las pantallas no son el origen del procedimiento. Se derivan del [Contrato narrativo de la experiencia](../02-content/activity-narrative-contract.md), ya validado por contenido y pedagogía.

## 2. Dos modelos conectados

La biblioteca conserva términos técnicos como `roleTemplate`, `skillId`, `conceptId`, restricciones y mappings. La aplicación familiar traduce esos objetos a lenguaje de facilitación:

| Modelo editorial/interno | Presentación familiar |
|---|---|
| `roleTemplate` | **Aporte sugerido** dentro del proyecto |
| `primaryObjectiveSkillId` | **Foco de aprendizaje de hoy** |
| `exposureSkillIds` | **También tendrá oportunidades de…** |
| `cycleStage` | **Fase** y propósito de la fase |
| `adaptation` + `commonProblem` | **Ayuda para este paso** con problema y cambio concretos |

La palabra “rol” puede usarse editorialmente, pero no es el encabezado principal de la asignación familiar. El adulto no debe configurar el motor pedagógico para empezar una actividad normal.

## 3. Resumen educativo previo

Antes de la preparación material, `SCR-005` muestra un resumen escaneable con:

- **Propósito educativo:** qué experiencia intenta producir, no solo qué objeto construirán.
- **Área principal** y **áreas secundarias**.
- **Conceptos clave** explicados con lenguaje adulto breve.
- **Habilidades practicables**, distinguiendo foco principal y exposiciones.
- **Mecanismo de aprendizaje:** por qué las acciones de la actividad permiten practicar esas habilidades.
- **Decisión infantil real:** qué pueden decidir los niños sin que la aplicación entregue la respuesta.
- **Éxito educativo:** qué cuenta como una experiencia válida aunque el resultado físico sea inesperado.

El resumen usa divulgación progresiva: propósito, área principal, conceptos y decisión aparecen abiertos; explicación detallada, taxonomía completa y referencias editoriales aparecen bajo `Entender la actividad`.

## 4. Foco sugerido por niño

Cada participante activo recibe:

- Nombre o alias.
- Foco principal redactado como acción observable.
- Aporte sugerido dentro del proyecto.
- Razón de la selección: edad/rango permitido, primera exploración, evidencia previa, interés, variedad o crecimiento.
- Exposiciones secundarias probables, condicionadas a participación real.

La UI dice `Sugerido para [nombre]`, no `nivel de [nombre]`. Si no existe evidencia, la razón es `primera oportunidad para observar`, nunca una predicción de capacidad.

No se muestra un control de intercambio como acción normal. Si la participación real cambia, el adulto puede registrarlo desde un flujo de excepción (`No está participando como esperábamos`) sin tener que comprender roles técnicos ni reasignar objetivos en medio de la actividad.

## 5. Contrato de una fase

Cada fase infantil renderiza estos bloques, en este orden:

1. **Para qué sirve esta fase** — una oración y 1–3 conceptos/habilidades relacionados.
2. **Haz esto** — acciones del adulto, numeradas y físicamente precisas.
3. **Diles** — lenguaje literal o preguntas que el adulto puede pronunciar.
4. **Ahora cada uno** — una acción concreta para cada participante, resuelta desde su asignación y mostrada con su nombre.
5. **Decisión de los niños** — cuando exista; especifica qué pueden elegir y qué permanece fijo.
6. **Observa sin interrumpir** — señales relacionadas con los focos principales; no obliga a evaluar durante la sesión.
7. **Resultado para continuar** — estado visible que permite avanzar aunque no coincida con una expectativa.
8. **Seguridad durante este paso** — control localizado, antes de la acción de riesgo.
9. **Ayuda con este paso** — problemas concretos, respuesta segura y punto exacto de reanudación.

`Resultado para continuar` no es una promesa física. Puede ser un resultado válido, un resultado inesperado documentado o una razón honesta de por qué la prueba no fue comparable.

Cada fase muestra además una continuidad compacta: `Llegan con…` y `Al terminar tendrán…`. Esos textos provienen de `entryStateId` y `exitStateId`; no se redactan libremente en UI.

## 6. Resolución nominal de participantes

La `ActivityVersion` no contiene nombres infantiles. Define acciones por aporte/rol o para todo el grupo. La sesión combina:

```text
participantActionTemplate.roleTemplateId
+ Assignment.actualRoleTemplateIds
+ Learner.alias
→ “Mateo baja un crayón, cuenta y espera la señal.”
```

Reglas:

- Toda fase infantil nombra a todos los participantes activos.
- Cuando la narrativa declara `individual_cycles` o `hybrid`, cada niño realiza su propia instancia de las acciones esenciales señaladas; los focos no dividen el ciclo en monopolios.
- Si dos niños comparten un aporte, la UI distribuye turnos o presenta una acción compartida explícita.
- Con un niño, se combinan acciones compatibles y el adulto realiza siempre los pasos exclusivos.
- Un niño que solo observa no recibe automáticamente exposición ni valoración.
- El texto nunca convierte al mayor en ayudante permanente del menor.

## 7. Ayuda contextual

Se elimina el control genérico `Ajustar ritmo` del camino principal. La ayuda aparece porque existe un problema reconocible, por ejemplo:

- `No saben qué forma elegir` → mostrar opciones aprobadas y pedir elegir una.
- `Plegar resulta difícil` → marcar guías o estabilizar el papel; explicar qué deja de ser evaluable si el adulto pliega.
- `El vaso se inclina` → distinguir montaje inválido de deformación y reiniciar desde la verificación adulta.
- `Necesitan terminar` → cerrar después de una prueba completa y conservar el estado de reanudación.

Cada opción declara:

- problema observado;
- cambio exacto;
- qué no cambia;
- impacto en el foco/evidencia;
- instrucción de reanudación;
- límite de seguridad.

La IA puede seleccionar o explicar opciones publicadas, pero no redacta una modificación libre del procedimiento.

## 8. Jerarquía móvil

La guía se usa con atención dividida. En la vista base permanecen visibles:

- propósito de la fase;
- acciones del adulto;
- frase para los niños;
- acciones nominales;
- decisión infantil;
- advertencia relevante.

Se mantienen bajo demanda:

- explicación científica detallada;
- taxonomía completa e IDs;
- problemas no presentes;
- extensiones;
- razones editoriales y gates.

El scroll vertical es aceptable; la omisión de información necesaria para ejecutar o facilitar no lo es.

## 9. Requisitos

- **UX-FAC-001:** Antes de iniciar, la familia ve propósito, área principal, áreas secundarias, conceptos, habilidades, mecanismo, decisión infantil y éxito educativo.
- **UX-FAC-002:** Cada participante activo ve un foco principal y aporte sugerido con razón explicable.
- **UX-FAC-003:** La UI familiar presenta aportes/focos; los roles técnicos permanecen como contrato interno.
- **UX-FAC-004:** No existe intercambio de roles como control primario durante el camino normal.
- **UX-FAC-005:** Cada fase infantil muestra acciones adultas numeradas y lenguaje literal sugerido.
- **UX-FAC-006:** Cada fase infantil nombra a todos los participantes activos y su acción concreta.
- **UX-FAC-007:** Las decisiones infantiles y condiciones fijas se distinguen visualmente.
- **UX-FAC-008:** Cada fase indica qué observar sin pedir una calificación en vivo.
- **UX-FAC-009:** Toda ayuda contextual nombra problema, cambio, impacto, reanudación y límite de seguridad.
- **UX-FAC-010:** El producto no usa `Ajustar ritmo` o etiquetas genéricas sin explicar qué cambia.
- **UX-FAC-011:** Las vistas de 1–4 niños se generan desde mappings de contenido y asignaciones, no desde copy específico de una familia.
- **UX-FAC-012:** El adulto puede continuar con un resultado inesperado o no comparable sin inventar datos ni atribuir la falla al niño.
- **UX-FAC-013:** Cada fase comunica su estado de entrada y salida y respeta el orden del contrato narrativo.
- **UX-FAC-014:** En actividades individuales o híbridas, la guía ofrece a cada participante su propia acción de proponer, hacer/probar y observar según el ciclo declarado.

## 10. Criterios de aceptación

1. Un adulto que no conoce estructuras puede explicar el propósito del puente y ejecutar una prueba comparable usando solo la app.
2. En una sesión de tres niños, el adulto puede decir qué hará cada uno en cada fase sin abrir un editor de roles.
3. Otra actividad —clasificación, circuito, naturaleza o vida práctica— puede llenar el mismo contrato sin añadir componentes especiales.
4. Ningún bloque familiar expone IDs técnicos como condición para comprender la actividad.
5. Una revisión de contenido puede detectar automáticamente fases sin guion adulto, acción de participante, observación o ayuda segura.
