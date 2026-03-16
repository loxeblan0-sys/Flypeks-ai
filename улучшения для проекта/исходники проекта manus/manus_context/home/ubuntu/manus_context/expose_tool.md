```python
import dataclasses
from typing import Literal

def expose(
    brief: str,
    port: int,
) -> dict:
  """Expose a local port in the sandbox for temporary public access.

  <instructions>
  - This tool returns a temporary public proxied domain for the specified port in the sandbox
  - Port information is encoded in domain prefix, no additional port specification needed
  - Exposed services MUST NOT bind to specific IP addresses or Host headers
  - DO NOT use for production as services will become unavailable after sandbox shutdown
  </instructions>

  <recommended_usage>
  - Use for providing temporary public access for locally running services
  </recommended_usage>

  Args:
    brief: A one-sentence preamble describing the purpose of this operation
    port: Local port number in the sandbox to expose for public access
  """
```
