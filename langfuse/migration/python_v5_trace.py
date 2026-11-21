"""LF-16 reference only. Run in a protected environment after installing langfuse>=5."""
import os
from langfuse import get_client

# LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_BASE_URL come from a protected env.
langfuse = get_client()

with langfuse.start_as_current_observation(as_type="span", name="lf16-migration-smoke") as span:
    span.update(input={"case": "redacted-smoke"})
    with langfuse.start_as_current_observation(
        as_type="generation", name="example-generation", model="model-from-config"
    ) as generation:
        generation.update(output={"result": "redacted"})
    span.update(output={"status": "completed"})

# Required for short-lived processes.
langfuse.flush()
