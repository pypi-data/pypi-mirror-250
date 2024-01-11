from dbt.adapters.snowflake import SnowflakeConnectionManager

from dbt.adapters.conveyorsnowflake.connections import ConveyorSnowflakeAdapterCredentials
from dbt.adapters.snowflake.impl import SnowflakeAdapter

from dbt.adapters.base import AdapterPlugin
from dbt.include import conveyorsnowflake


class ConveyorSnowflakeConnectionManager(SnowflakeConnectionManager):
    TYPE = "conveyorsnowflake"


class ConveyorSnowflakeAdapter(SnowflakeAdapter):
    ConnectionManager = ConveyorSnowflakeConnectionManager


Plugin = AdapterPlugin(
    adapter=ConveyorSnowflakeAdapter,
    credentials=ConveyorSnowflakeAdapterCredentials,
    include_path=conveyorsnowflake.PACKAGE_PATH,
    dependencies=["snowflake"]
)
