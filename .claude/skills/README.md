# Skills de Claude Code del proyecto

Claude Code carga automáticamente las skills de esta carpeta en cualquier sesión abierta con este repositorio.

| Skill | Origen | Licencia |
|-------|--------|----------|
| `frontend-design` | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/frontend-design) (commit `2c5958e`) | Apache 2.0 |
| `ui-ux-pro-max` | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) v2.15.0 (commit `6ae86f6`) | MIT |
| `banner-design` | mismo repositorio que `ui-ux-pro-max` (commit `6ae86f6`) | MIT |
| `brand` | mismo repositorio que `ui-ux-pro-max` (commit `6ae86f6`) | MIT |
| `design` | mismo repositorio que `ui-ux-pro-max` (commit `6ae86f6`) | MIT |
| `design-system` | mismo repositorio que `ui-ux-pro-max` (commit `6ae86f6`) | MIT |
| `slides` | mismo repositorio que `ui-ux-pro-max` (commit `6ae86f6`) | MIT |
| `ui-styling` | mismo repositorio que `ui-ux-pro-max` (commit `6ae86f6`) | MIT |

Cambios locales en `ui-ux-pro-max/SKILL.md`: las rutas `${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/...` se han sustituido por `.claude/skills/ui-ux-pro-max/...` (relativas a la raíz del repositorio), porque la skill se instala aquí y no como plugin. Su buscador necesita Python 3 y no usa dependencias externas.

Las seis skills añadidas de `ui-ux-pro-max-skill` se han copiado sin cambios. Sus scripts usan rutas relativas a la carpeta de cada skill (`design` y `slides` llaman a `../design-system/scripts/`), así que deben seguir juntas en esta carpeta.

Requisitos opcionales:
- `design` genera logos, iconos e imágenes de identidad corporativa con IA externa: necesita `pip install google-genai` y `GEMINI_API_KEY`, o bien `ATLASCLOUD_API_KEY` o `MUAPI_API_KEY`. Sin clave, solo funcionan sus buscadores locales.
- `brand` y `design-system` usan Node.js para sus scripts `.cjs`.
- `ui-styling` ejecuta la CLI de shadcn (`npx shadcn`) para añadir componentes.

Para actualizarlas, vuelve a copiar la carpeta desde su repositorio de origen.
