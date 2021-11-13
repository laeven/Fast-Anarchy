import unrealsdk
from unrealsdk import *
from ..ModManager import EnabledSaveType, RegisterMod, OptionManager
from ..OptionManager import Options
from typing import Dict
# from Mods.UserFeedback import ShowHUDMessage
from ..ModMenu import Game, Hook
from typing import ClassVar, Dict, List

class FastAnarchy(unrealsdk.BL2MOD):
    Name: ClassVar[str] = "Fast Anarchy"
    Author: ClassVar[str] = "Laeven"
    Description: ClassVar[str] = (
        "Updates the Ration Architect Skill to give higher initial Anarchy Stacks."
    )
    Types: ClassVar[List[unrealsdk.ModTypes]] = [unrealsdk.ModTypes.Utility]
    Version: ClassVar[str] = "1.0"
    SupportedGames = Game.BL2
    SaveEnabledState = EnabledSaveType.LoadOnMainMenu

    # Status: str
    SettingsInputs: Dict[str, str]

    def __init__(self) -> None:
        self.Author += "\nVersion: " + str(self.Version)  # type: ignore

        # self.Status = "Enabled"
        self.SettingsInputs = {
            "Enter": "Enable",
        }

        # Add menu options
        self.anarchyBonusConfig = Options.Spinner("Initial Anarchy", "Sets power of the Rational Anarchist skill for Gaige.", "25", ["25", "75", "125", "250", "400", "600"])

        self.Options = [
            self.anarchyBonusConfig
        ]

    def Enable(self) -> None:
        super().Enable()
    
    def Disable(self) -> None:
        super().Disable()

    # Load for initial load of player
    @Hook("WillowGame.PlayerSkillTree.Initialize")
    def InitSkillChange(self, caller: UObject, function: UFunction, params: FStruct) -> bool:
        # unrealsdk.Log(f"Updating anarchy bonus to {self.anarchyBonusConfig.CurrentValue}")
        self.UpdateAnarchySkill(float(self.anarchyBonusConfig.CurrentValue))
        return True
    
    # Every other time it matters would be handled here
    def ModOptionChanged(self, option: OptionManager.Options.Base, new_value: any) -> None:
        if option == self.anarchyBonusConfig:
            # unrealsdk.Log(f"Updating anarchy to {new_value}")
            self.UpdateAnarchySkill(float(new_value))

    def UpdateAnarchySkill(self, value: float):
        PC = unrealsdk.GetEngine().GamePlayers[0].Actor
        # unrealsdk.Log("Updating Rational Anarchist")
        if unrealsdk.FindObject("SkillDefinition", "GD_Tulip_Mechromancer_Skills.EmbraceChaos.RationalAnarchist"):
            skill_description = f'If you have 0 stacks of [skill]Anarchy[-skill], then the next time you would gain an [skill]Anarchy[-skill] stack you gain {int(value)} instead.'
            flavor_text = f"Get {int(value)} [skill]Anarchy[-skill] stacks for the price of 1. It's like free breakfast, a nice start!"

            # Try to avoid creating the objects because they don't always exist (only while in game)
            PC.ServerRCon(f"set {PC.PathName(unrealsdk.FindObject('SkillDefinition', 'GD_Tulip_Mechromancer_Skills.EmbraceChaos.RationalAnarchist'))} SkillDescription {skill_description}")
            PC.ServerRCon(f"set {PC.PathName(unrealsdk.FindObject('ConstantAttributeValueResolver', 'GD_Tulip_Mechromancer_Skills.Misc.Att_RationalAnarchist_NumberOfStacks:ConstantAttributeValueResolver_1'))} ConstantValue {value}")
            PC.ServerRCon(f"set {PC.PathName(unrealsdk.FindObject('AttributePresentationDefinition', 'GD_Tulip_Mechromancer_Skills.EmbraceChaos.RationalAnarchist:AttributePresentationDefinition_0'))} Description {flavor_text}")

RegisterMod(FastAnarchy())