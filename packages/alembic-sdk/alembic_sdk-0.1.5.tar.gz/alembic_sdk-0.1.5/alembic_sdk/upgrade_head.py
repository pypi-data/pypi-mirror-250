import sys


def upgrade_head():
    from alembic import config

    alembicArgs = [
        "--raiseerr",
        "upgrade",
        "head",
    ]
    try:
        config.main(argv=alembicArgs)
        return True
    except Exception as e:
        print(e)
        return False


if upgrade_head():
    sys.exit(0)  # Exit with code 0 for success
else:
    sys.exit(1)  # Exit with code 1 (or any non-zero code)
