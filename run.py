"""The development server.

`STORYBOOK_PASSWORD` defaults to `dev` here and only here. Without it a
bare checkout would start unclaimed (F60) and print a claim code, which is
right for a real install and pointless friction for someone running the
test server for the fifth time today.
"""

import os

from app import create_app

os.environ.setdefault("STORYBOOK_PASSWORD", "dev")

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
