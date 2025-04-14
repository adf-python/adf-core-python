import argparse
import resource

from adf_core_python.core.config.config import Config
from adf_core_python.core.launcher.agent_launcher import AgentLauncher
from adf_core_python.core.launcher.config_key import ConfigKey
from adf_core_python.core.logger.logger import configure_logger, get_logger


class Launcher:
    def __init__(
        self,
        launcher_config_file: str,
    ) -> None:
        resource.setrlimit(resource.RLIMIT_NOFILE, (8192, 1048576))

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
            "-ac",
            "--ambulancecenter",
            type=int,
            help="number of ambulance center agents(Default: all ambulance center)",
            metavar="",
        )
        parser.add_argument(
            "-fs",
            "--firestation",
            type=int,
            help="number of fire station agents(Default: all fire station)",
            metavar="",
        )
        parser.add_argument(
            "-po",
            "--policeoffice",
            type=int,
            help="number of police office agents(Default: all police office)",
            metavar="",
        )
        parser.add_argument(
            "--precompute",
            action="store_true",
            help="precompute flag",
        )
        parser.add_argument(
            "--timeout",
            type=int,
            help="timeout in seconds",
            metavar="",
        )
        parser.add_argument("--debug", action="store_true", help="debug flag")
        parser.add_argument(
            "--java",
            action="store_true",
            help="using java module flag",
        )
        args = parser.parse_args()

        config_map = {
            ConfigKey.KEY_KERNEL_HOST: args.host,
            ConfigKey.KEY_KERNEL_PORT: args.port,
            ConfigKey.KEY_AMBULANCE_TEAM_COUNT: args.ambulanceteam,
            ConfigKey.KEY_FIRE_BRIGADE_COUNT: args.firebrigade,
            ConfigKey.KEY_POLICE_FORCE_COUNT: args.policeforce,
            ConfigKey.KEY_AMBULANCE_CENTRE_COUNT: args.ambulancecenter,
            ConfigKey.KEY_FIRE_STATION_COUNT: args.firestation,
            ConfigKey.KEY_POLICE_OFFICE_COUNT: args.policeoffice,
            ConfigKey.KEY_PRECOMPUTE: args.precompute,
            ConfigKey.KEY_KERNEL_TIMEOUT: args.timeout,
            ConfigKey.KEY_DEBUG_FLAG: args.debug,
            ConfigKey.KEY_GATEWAY_FLAG: args.java,
        }

        for key, value in config_map.items():
            if value is not None:
                self.launcher_config.set_value(key, value)

        configure_logger()
        self.logger = get_logger(__name__)

        self.logger.debug(f"launcher_config: {self.launcher_config}")

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
