from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerSettings(BaseSettings):
    """
    Configuration for the MCP Docker server.
    Loaded from environment variables with prefix MCP_SERVER_.
    Example: MCP_SERVER_LOG_LEVEL=DEBUG
    """

    model_config = SettingsConfigDict(
        env_prefix="mcp_server_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    log_level: str = Field(
        default="WARNING",
        description="Logging level: DEBUG, INFO, WARNING, ERROR",
    )
