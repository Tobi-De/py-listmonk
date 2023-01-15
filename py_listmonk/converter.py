from uuid import UUID

from cattrs import Converter
from pendulum import DateTime
from pendulum import parse as pendulum_parse

converter = Converter()

# pendulum datetime
converter.register_unstructure_hook(DateTime, lambda dt: dt.to_iso8601_string())
converter.register_structure_hook(
    DateTime, lambda isostring, _: pendulum_parse(isostring)
)

# uuid
converter.register_unstructure_hook(UUID, lambda uuid: str(uuid))
converter.register_structure_hook(UUID, lambda uuidstring, _: UUID(uuidstring))
