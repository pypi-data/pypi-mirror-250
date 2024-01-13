from dataclasses import dataclass, field
import dbt.exceptions  # noqa
import subprocess
from dbt.adapters.snowflake import SnowflakeCredentials
import json

@dataclass
class ConveyorSnowflakeAdapterCredentials(SnowflakeCredentials):
    # We need to set the default to empty string, otherwise dbt run will complain user is not set and fail
    user: str = field(default='')
    def __post_init__(self):
        token_output = subprocess.run(
            [
                "conveyor", "ide", "snowflake-token",
                f"--snowflake-client-id={self.oauth_client_id}",
                f"--snowflake-client-secret={self.oauth_client_secret}",
                f"--snowflake-account={self.account}",
                "--quiet",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        self.token = json.loads(token_output.stdout.rstrip().decode())["refresh_token"]
        self.user = json.loads(token_output.stdout.rstrip().decode())["username"]
        super().__post_init__()

    @property
    def type(self):
        return "conveyorsnowflake"
