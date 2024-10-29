from rcrs_core.commands.AKClear import AKClear
from rcrs_core.commands.AKClearArea import AKClearArea
from rcrs_core.commands.AKExtinguish import AKExtinguish
from rcrs_core.commands.AKLoad import AKLoad
from rcrs_core.commands.AKMove import AKMove
from rcrs_core.commands.AKRescue import AKRescue
from rcrs_core.commands.AKRest import AKRest
from rcrs_core.commands.AKSay import AKSay
from rcrs_core.commands.AKSpeak import AKSpeak
from rcrs_core.commands.AKSubscribe import AKSubscribe
from rcrs_core.commands.AKTell import AKTell
from rcrs_core.commands.AKUnload import AKUnload
from rcrs_core.commands.Command import Command
from rcrs_core.connection.URN import Command as CommandURN
from rcrs_core.connection.URN import ComponentCommand as ComponentCommandMessageID
from rcrs_core.connection.URN import ComponentControlMSG as ComponentControlMessageID


class CommandFactory:
    @staticmethod
    def create_command(herad_command) -> Command:
        if herad_command.urn == CommandURN.AK_SPEAK:
            return AKSpeak(
                herad_command.components[ComponentControlMessageID.AgentID].entityID,
                herad_command.components[ComponentControlMessageID.Time].intValue,
                herad_command.components[ComponentCommandMessageID.Message].rawData,
                herad_command.components[ComponentCommandMessageID.Channel].intValue,
            )
        return herad_command
        # if herad_command.urn == CommandURN.AK_CLEAR:
        #     return AKClear(
        #         herad_command.agent_id, herad_command.time, herad_command.target
        #     )
        # elif herad_command.urn == CommandURN.AK_CLEAR_AREA:
        #     return AKClearArea(
        #         herad_command.agent_id,
        #         herad_command.time,
        #         herad_command.x,
        #         herad_command.y,
        #     )
        # elif herad_command.urn == CommandURN.AK_EXTINGUISH:
        #     return AKExtinguish(
        #         herad_command.agent_id, herad_command.time, herad_command.target
        #     )
