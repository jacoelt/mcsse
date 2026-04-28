# CLAUDE.md

## Shell environment

At the start of the session, check the current working directory (`pwd`) and whether the Python venv is already active (`echo $VIRTUAL_ENV`). Reuse that information for the rest of the session:

- Do not prepend `cd` to commands when already in the correct directory.
- Do not re-run `source venv/Scripts/activate` if `$VIRTUAL_ENV` is already set — exported env vars (PATH, VIRTUAL_ENV) are inherited by every Bash subprocess.

## Testing

**Before making any code change**, run the full test suite first.

If any test fails before your change, **stop immediately and report the failure**. Do not proceed with the change.

**After making any code change**, run the full test suite again. If any test fails, keep fixing the code until all tests pass.
