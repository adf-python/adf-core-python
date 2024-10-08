import argparse

from adf_core_python.core.config.config import Config
from adf_core_python.core.launcher.agent_launcher import AgentLauncher
from adf_core_python.core.launcher.config_key import ConfigKey
from adf_core_python.core.logger.logger import configure_logger, get_logger


class Main:
    def __init__(self) -> None:
        self.logger = get_logger(__name__)
        parser = argparse.ArgumentParser(description="Agent Launcher")

        parser.add_argument(
            "--host",
            type=str,
            default="localhost",
            help="host name(Default: localhost)",
            metavar="",
        )
        parser.add_argument(
            "--port",
            type=int,
            default=27931,
            help="port number(Default: 27931)",
            metavar="",
        )
        parser.add_argument(
            "-a",
            "--ambulance",
            type=int,
            default=-1,
            help="number of ambulance agents(Default: -1 means all ambulance)",
            metavar="",
        )
        parser.add_argument(
            "-f",
            "--firebrigade",
            type=int,
            default=-1,
            help="number of firebrigade agents(Default: -1 means all firebrigade)",
            metavar="",
        )
        parser.add_argument(
            "-p",
            "--policeforce",
            type=int,
            default=-1,
            help="number of policeforce agents(Default: -1 means all policeforce)",
            metavar="",
        )
        parser.add_argument(
            "--precompute",
            type=bool,
            default=False,
            help="precompute flag",
            metavar="",
        )
        parser.add_argument(
            "--debug", type=bool, default=False, help="debug flag", metavar=""
        )
        args = parser.parse_args()
        self.logger.info(f"Arguments: {args}")

        self.config = Config()
        self.config.set_value(ConfigKey.KEY_KERNEL_HOST, args.host)
        self.config.set_value(ConfigKey.KEY_KERNEL_PORT, args.port)
        self.config.set_value(ConfigKey.KEY_AMBULANCE_CENTRE_COUNT, args.ambulance)
        self.config.set_value(ConfigKey.KEY_FIRE_STATION_COUNT, args.firebrigade)
        self.config.set_value(ConfigKey.KEY_POLICE_OFFICE_COUNT, args.policeforce)
        self.config.set_value(ConfigKey.KEY_PRECOMPUTE, args.precompute)
        self.config.set_value(ConfigKey.KEY_DEBUG_FLAG, args.debug)
        self.logger.info(f"Config: {self.config}")

    def launch(self) -> None:
        agent_launcher: AgentLauncher = AgentLauncher(
            self.config,
        )
        agent_launcher.init_connector()

        try:
            agent_launcher.launch()
        except KeyboardInterrupt:
            self.logger.info("Agent launcher interrupted")
        except Exception as e:
            self.logger.exception("Agent launcher failed", exc_info=e)
            raise e
        self.logger.info("Agent launcher finished")


if __name__ == "__main__":
    configure_logger()
    logger = get_logger(__name__)
    logger.info("Starting the agent launcher")

    main = Main()
    main.launch()
