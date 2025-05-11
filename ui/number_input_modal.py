import discord
from discord import ui


class ProceedButton(ui.View):
    def __init__(self, next_modal: ui.Modal):
        super().__init__(timeout=None)
        self.next_modal = next_modal
        self.interaction: discord.Interaction = None

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if self.interaction is None or interaction.user == self.interaction.user:
            self.interaction = interaction
            return True
        await interaction.response.send_message("This button is not for you.", ephemeral=True)
        return False

    @discord.ui.button(label="Proceed to Build #2", style=discord.ButtonStyle.primary)
    async def proceed(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(self.next_modal)
        self.stop()


class Build1DetailsModal(ui.Modal, title='Enter Build #1 Details'):
    scaling_stat_b1 = ui.TextInput(label='TotalATK', placeholder='Enter total ATK')
    dmg_bonus_percent_b1 = ui.TextInput(label='DMGBonus (%)', placeholder='Enter damage bonus percentage (e.g., 50)')
    crit_rate_percent_b1 = ui.TextInput(label='CritRate (%)', placeholder='Enter critical rate percentage (e.g., 70)')
    crit_dmg_percent_b1 = ui.TextInput(label='CritDmg (%)', placeholder='Enter critical damage percentage (e.g., 120)')
    build1_details_raw = {}
    submitted = False

    async def on_submit(self, interaction: discord.Interaction):
        try:
            atk = float(self.scaling_stat_b1.value)
            dmg_bonus_percent = float(self.dmg_bonus_percent_b1.value)
            crit_rate_percent = min(float(self.crit_rate_percent_b1.value), 100)
            crit_dmg_percent = float(self.crit_dmg_percent_b1.value)
            self.build1_details_raw = {
                'atk': atk,
                'dmg_bonus_percent': dmg_bonus_percent,
                'crit_rate_percent': crit_rate_percent,
                'crit_dmg_percent': crit_dmg_percent,
            }
            self.submitted = True
            view = ProceedButton(Build2DetailsModal(self.build1_details_raw))  # Pass raw build 1 data
            details_string = f"ATK: {atk}, DMGBonus: {dmg_bonus_percent}%, CritRate: {crit_rate_percent}%, CritDmg: {crit_dmg_percent}%"
            await interaction.response.send_message(
                f'Build #1 details received: {details_string}\nClick the button to enter Build #2 details.', view=view,
                ephemeral=True)
        except ValueError:
            await interaction.response.send_message('Invalid number format. Please enter numbers for all fields.',
                                                    ephemeral=True)
            self.stop()

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(f'Oops! Something went wrong in Build #1 modal: {error}',
                                                ephemeral=True)
        import traceback
        traceback.print_tb(error.__traceback__)


class Build2DetailsModal(ui.Modal, title='Enter Build #2 Details'):
    scaling_stat_b2 = ui.TextInput(label='TotalATK', placeholder='Enter total ATK')
    dmg_bonus_percent_b2 = ui.TextInput(label='DMGBonus (%)', placeholder='Enter damage bonus percentage (e.g., 50)')
    crit_rate_percent_b2 = ui.TextInput(label='CritRate (%)', placeholder='Enter critical rate percentage (e.g., 70)')
    crit_dmg_percent_b2 = ui.TextInput(label='CritDmg (%)', placeholder='Enter critical damage percentage (e.g., 120)')
    build1_data_raw = {}
    build2_details_raw = {}
    submitted = False

    def __init__(self, build1_data_raw: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.build1_data_raw = build1_data_raw

    async def on_submit(self, interaction: discord.Interaction):
        try:
            atk = float(self.scaling_stat_b2.value)
            dmg_bonus_percent = float(self.dmg_bonus_percent_b2.value)
            crit_rate_percent = min(float(self.crit_rate_percent_b2.value), 100)
            crit_dmg_percent = float(self.crit_dmg_percent_b2.value)
            self.build2_details_raw = {
                'atk': atk,
                'dmg_bonus_percent': dmg_bonus_percent,
                'crit_rate_percent': crit_rate_percent,
                'crit_dmg_percent': crit_dmg_percent,
            }
            self.submitted = True
            await self.compare_damage(interaction)
        except ValueError:
            await interaction.response.send_message('Invalid number format. Please enter numbers for all fields.',
                                                    ephemeral=True)
            self.stop()

    async def compare_damage(self, interaction: discord.Interaction):
        def calculate_avg_dmg(build_raw):
            atk = build_raw['atk']
            dmg_bonus = build_raw['dmg_bonus_percent'] / 100
            crit_rate = build_raw['crit_rate_percent'] / 100
            crit_dmg = build_raw['crit_dmg_percent'] / 100
            return atk * (1 + dmg_bonus) * (1 + crit_rate * crit_dmg)

        dmg1 = calculate_avg_dmg(self.build1_data_raw)
        dmg2 = calculate_avg_dmg(self.build2_details_raw)

        if dmg1 > dmg2:
            lower_dmg = dmg2
            higher_dmg = dmg1
            lower_build_name = "Build #2"
            higher_build_name = "Build #1"
            lower_build_raw = self.build2_details_raw
            higher_build_raw = self.build1_data_raw
        else:
            lower_dmg = dmg1
            higher_dmg = dmg2
            lower_build_name = "Build #1"
            higher_build_name = "Build #2"
            lower_build_raw = self.build1_data_raw
            higher_build_raw = self.build2_details_raw

        normalised_higher_dmg = (higher_dmg / lower_dmg) * 100

        higher_build_stats = f"ATK: {higher_build_raw['atk']}, DMGBonus: {higher_build_raw['dmg_bonus_percent']}%, CR: {higher_build_raw['crit_rate_percent']}%, CDMG: {higher_build_raw['crit_dmg_percent']}%"
        lower_build_stats = f"ATK: {lower_build_raw['atk']}, DMGBonus: {lower_build_raw['dmg_bonus_percent']}%, CR: {lower_build_raw['crit_rate_percent']}%, CDMG: {lower_build_raw['crit_dmg_percent']}%"

        comparison_message = (
            f"**{higher_build_name}**: {higher_build_stats} - **{normalised_higher_dmg:.2f}%**\n"
            f"**{lower_build_name}**: {lower_build_stats} - **100%**"
        )
        await interaction.response.send_message(comparison_message, ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(f'Oops! Something went wrong in Build #2 modal: {error}',
                                                ephemeral=True)
        import traceback
        traceback.print_tb(error.__traceback__)
