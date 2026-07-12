# log-to-test

A dependency-free CLI that clusters structured failure logs and emits Python unittest reproduction skeletons.

## Quick start

```bash
python log_to_test.py failures.json
```

Logs are grouped by exception and operation. The output includes one redacted context example per root cause and a test skeleton that captures the expected failure condition.

## Test

```bash
python -m unittest discover -v
```

## License

MIT.
