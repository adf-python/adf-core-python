import logging
import os
import sys
from datetime import datetime

import structlog
from structlog.dev import ConsoleRenderer
from structlog.processors import JSONRenderer

from adf_core_python.core.agent.info.agent_info import AgentInfo


def get_logger(name: str) -> structlog.BoundLogger:
  """
  Get a logger with the given name.
  For kernel logging, use this function to get a logger.

  Parameters
  ----------
  name : str
      The name of the logger.

  Returns
  -------
  structlog.BoundLogger
      The logger with the given name.
  """
  return structlog.get_logger(name)


def get_agent_logger(name: str, agent_info: AgentInfo) -> structlog.BoundLogger:
  """
  Get a logger with the given name and agent information.
  For agent logging, use this function to get a logger.

  Parameters
  ----------
  name : str
      The name of the logger.
  agent_info : AgentInfo
      The agent information.

  Returns
  -------
  structlog.BoundLogger
      The logger with the given name and agent information.
  """
  agent = agent_info.get_myself()
  if agent is None:
    raise ValueError("Agent information is not available")

  return structlog.get_logger(name).bind(
    agent_id=str(agent_info.get_entity_id()),
    agent_type=str(agent.get_urn().name),
  )


def configure_logger() -> None:
  # 既存のログファイルが存在する場合、日付付きでバックアップする
  log_file = "agent.log"
  if os.path.exists(log_file):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"agent_{timestamp}.log"
    os.rename(log_file, backup_file)

  structlog.configure(
    processors=[
      structlog.stdlib.add_log_level,
      structlog.stdlib.add_logger_name,
      structlog.stdlib.PositionalArgumentsFormatter(),
      structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M.%S", utc=False),
      structlog.processors.StackInfoRenderer(),
      structlog.processors.UnicodeDecoder(),
      structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
  )

  handler_stdout = logging.StreamHandler(sys.stdout)
  handler_stdout.setFormatter(
    structlog.stdlib.ProcessorFormatter(processor=ConsoleRenderer())
  )
  handler_stdout.setLevel(logging.INFO)

  handler_file = logging.FileHandler(log_file)
  handler_file.setFormatter(
    structlog.stdlib.ProcessorFormatter(processor=JSONRenderer())
  )
  handler_file.setLevel(logging.DEBUG)

  root_logger = logging.getLogger()
  root_logger.addHandler(handler_stdout)
  root_logger.addHandler(handler_file)
  root_logger.setLevel(logging.DEBUG)
