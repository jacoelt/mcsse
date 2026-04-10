# CLAUDE.md

## Testing

**Before making any code change**, run the full test suite first:

```bash
cd back && source venv/Scripts/activate && python manage.py test core.tests fetcher.tests
```

If any test fails before your change, **stop immediately and report the failure**. Do not proceed with the change.

**After making any code change**, run the full test suite again. If any test fails, keep fixing the code until all tests pass.
