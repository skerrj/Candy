# bin

Checked-in Candy translators, one directory per target (`bin/py/` for Python; later
targets get their own, see `doc/hl_rqmt/multi_target.md`). Empty for now. The first one to
land here is the self-hosted translator once it reaches the T1 = T2 fixpoint (see
`doc/hl_rqmt/self_hosting_primo.md`), so that Candy can be rebuilt without the Python
translator, as smz did. Until then, T1 and T2 are generated into `output/` (git-ignored).
