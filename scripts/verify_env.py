"""Environment sanity check. Run from the repo root:  python -m scripts.verify_env"""
import importlib
import sys

REQUIRED = ["numpy", "pandas", "pyarrow", "scipy", "plotly", "dotenv", "yaml", "pytest"]


def in_virtualenv() -> bool:
    # Inside a venv, sys.prefix points to .venv while sys.base_prefix points to system Python.
    return sys.prefix != sys.base_prefix


def main() -> int:
    ok = in_virtualenv()
    print(f"Python      : {sys.version.split()[0]}")
    print(f"Executable  : {sys.executable}")
    print(f"In venv     : {ok}")

    for name in REQUIRED:
        try:
            module = importlib.import_module(name)
            print(f"{name:<12}: {getattr(module, '__version__', 'ok')}")
        except ImportError:
            print(f"{name:<12}: MISSING")
            ok = False

    from src import config

    for label, path in [("raw", config.RAW_DIR), ("interim", config.INTERIM_DIR),
                        ("processed", config.PROCESSED_DIR)]:
        exists = path.exists()
        print(f"data/{label:<8}: {'ok' if exists else 'MISSING'}")
        ok = ok and exists

    print("\nRESULT:", "environment OK" if ok else "environment has problems")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())