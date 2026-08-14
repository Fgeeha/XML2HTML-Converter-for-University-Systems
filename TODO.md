Using "zeep" or analogs to take data from the system directly

The DUO135 warning from flake8 is suppressed with an explicit `# noqa` in
`src/list_priority.py`: all `forbid_*` defenses are enabled on the shared
`XMLParser`, but dlint cannot trace them through the variable. Revisit if
dlint ever learns to follow the parser object.
