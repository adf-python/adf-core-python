import argparse

from adf_core_python.core.config.config import Config
from adf_core_python.core.launcher.agent_launcher import AgentLauncher
from adf_core_python.core.launcher.config_key import ConfigKey
from adf_core_python.core.logger.logger import configure_logger, get_logger


class Launcher:
    def __init__(
        self,
        launcher_config_file: str,
    ) -> None:
        configure_logger()

        self.logger = get_logger(__name__)
        self.launcher_config = Config(launcher_config_file)

        parser = argparse.ArgumentParser(description="Agent Launcher")

        parser.add_argument(
            "--host",
            type=str,
            help="host name(Default: localhost)",
            metavar="",
        )
        parser.add_argument(
            "--port",
            type=int,
            help="port number(Default: 27931)",
            metavar="",
        )
        parser.add_argument(
            "-a",
            "--ambulanceteam",
            type=int,
            help="number of ambulance agents(Default: all ambulance)",
            metavar="",
        )
        parser.add_argument(
            "-f",
            "--firebrigade",
            type=int,
            help="number of firebrigade agents(Default: all firebrigade)",
            metavar="",
        )
        parser.add_argument(
            "-p",
            "--policeforce",
            type=int,
            help="number of policeforce agents(Default: all policeforce)",
            metavar="",
        )
        parser.add_argument(
            "--precompute",
            type=bool,
            help="precompute flag",
            metavar="",
        )
        parser.add_argument(
            "--debug", type=bool, default=False, help="debug flag", metavar=""
        )
        args = parser.parse_args()
        self.logger.info(f"Arguments: {args}")

        config_map = {
            args.host: ConfigKey.KEY_KERNEL_HOST,
            args.port: ConfigKey.KEY_KERNEL_PORT,
            args.ambulance: ConfigKey.KEY_AMBULANCE_TEAM_COUNT,
            args.firebrigade: ConfigKey.KEY_FIRE_BRIGADE_COUNT,
            args.policeforce: ConfigKey.KEY_POLICE_FORCE_COUNT,
            args.precompute: ConfigKey.KEY_PRECOMPUTE,
            args.debug: ConfigKey.KEY_DEBUG_FLAG,
        }

        for arg, key in config_map.items():
            if arg is not None:
                self.launcher_config.set_value(key, arg)

        self.logger.info(f"Config: {self.launcher_config}")

    def launch(self) -> None:
        agent_launcher: AgentLauncher = AgentLauncher(
            self.launcher_config,
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
    launcher = Launcher(
        "config/launcher.yaml",
    )

    launcher.launch()
