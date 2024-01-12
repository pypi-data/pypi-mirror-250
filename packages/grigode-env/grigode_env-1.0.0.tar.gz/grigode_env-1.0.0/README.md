# grigode_env

### Environment variable handler.

Installation:

```bash
pip install grigode_env
```

- **example 1**:

```python
import os

from grigode_env import Env

# Load environment variables
Env(path='.env').load_environ()

# Get environment variables
os.environ.get('VAR0')

```

- **example 2**:

```python
from grigode_env import Env

# Load environment variables
env = Env(path='.env')
variables = env.load_environ(modify=False)

# Get environment variables
variables.get('VAR0')

```

In contrast to **example 1**, **example 2** does not modify the _os.environ_, which is where the operating system's environment variables are stored.
