import argparse

from adf_core_python.core.config.config import Config
from adf_core_python.core.launcher.agent_launcher import AgentLauncher
from adf_core_python.core.launcher.config_key import ConfigKey


class Main:
    def __init__(self) -> None:
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
            "--verbose", type=bool, default=False, help="verbose flag", metavar=""
        )
        args = parser.parse_args()
        print(args)
        self.config = Config()
        self.config.set_value(ConfigKey.KEY_KERNEL_HOST, args.host)
        self.config.set_value(ConfigKey.KEY_KERNEL_PORT, args.port)
        self.config.set_value(ConfigKey.KEY_AMBULANCE_CENTRE_COUNT, args.ambulance)
        self.config.set_value(ConfigKey.KEY_FIRE_STATION_COUNT, args.firebrigade)
        self.config.set_value(ConfigKey.KEY_POLICE_OFFICE_COUNT, args.policeforce)
        self.config.set_value(ConfigKey.KEY_PRECOMPUTE, args.precompute)
        self.config.set_value(ConfigKey.KEY_DEBUG_FLAG, args.verbose)

    def launch(self):
        agent_launcher: AgentLauncher = AgentLauncher(
            self.config,
        )
        agent_launcher.init_connector()
        agent_launcher.launch()


if __name__ == "__main__":
    main = Main()
    main.launch()
