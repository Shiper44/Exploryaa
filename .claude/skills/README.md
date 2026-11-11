# Skills de Claude Code del proyecto

Claude Code carga automáticamente las skills de esta carpeta en cualquier sesión abierta con este repositorio.

| Skill | Origen | Licencia |
|-------|--------|----------|
| `frontend-design` | [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/frontend-design) (commit `2c5958e`) | Apache 2.0 |
| `ui-ux-pro-max` | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) v2.15.0 (commit `6ae86f6`) | MIT |

Cambios locales en `ui-ux-pro-max/SKILL.md`: las rutas `${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/...` se han sustituido por `.claude/skills/ui-ux-pro-max/...` (relativas a la raíz del repositorio), porque la skill se instala aquí y no como plugin. Su buscador necesita Python 3 y no usa dependencias externas.

Para actualizarlas, vuelve a copiar la carpeta desde su repositorio de origen.
