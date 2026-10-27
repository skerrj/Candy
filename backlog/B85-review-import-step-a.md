# B85: Review `import` step A as built

kind: task
state: done
priority: normal
found: self-host-cleanup, 2026-10-18
fixed: carried-reviews
where: `doc/hl_rqmt/self_host_cleanup.md` ("Step A as built")
refs: [[programs.import]]

And its leak (`doc/archive/leaks_self_host_cleanup.md`, fixed since by modules). Carried over in `TODOS.md` for the owner's review.

## Notes

- 2026-10-26, the owner: ticked in review; "Step A as built" now has a *Since:* note
  (its leak fixed by modules, its tech debt on `self-host-cleanup`).
