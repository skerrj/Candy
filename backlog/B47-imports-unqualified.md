# B47: Only `(import m)`, everything unqualified

kind: leak
state: open
priority: normal
found: modules, 2026-10-19
fixed:
where: `src/cdy/include.cdy`, `src/cdy/core.cdy`
refs: [[programs.import]]

The MVP of `doc/hl_rqmt/modules.md`: no qualified names, `import-as` or `import-from`,
and no private names, so two modules that both define a name can't be imported into the
same file. Fix: "After the MVP" in the HLD. From `doc/archive/leaks_modules.md`.
