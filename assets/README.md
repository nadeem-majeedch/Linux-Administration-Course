# assets/

Diagrams, figures, and other visual material used by the modules.

## Planned figures (added with content in the next phase)

| Asset | Used by | Description |
|---|---|---|
| `architecture-layers.png` | M01, M03 | Hardware → kernel → userland → shell → GUI stack diagram |
| `fhs-tree.png` | M06 | Annotated filesystem hierarchy tree |
| `pipe-flow.png` | M09 | stdin/stdout/stderr through a 4-stage pipeline |
| `permission-matrix.png` | M12, M13 | rwx across user/group/other; setgid directory diagram |
| `storage-topology.png` | M17 | Disk → partition → filesystem → mount point mapping |
| `service-stack.png` | M29, M30 | nginx → API → PostgreSQL request path with logs marked |

## Conventions

- Vector sources (SVG/draw.io) are preferred; export PNG at 2x for readability.
- Filename: lowercase, hyphenated, no spaces.
- Every diagram must render its labels from the module's own vocabulary — no new
  terms introduced only in a figure.
- Attribution: original diagrams are part of the MIT-licensed course content; if a
  figure is adapted from external material, note the source and its license here.
