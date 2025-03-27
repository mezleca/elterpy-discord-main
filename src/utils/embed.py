import discord
from typing import Optional, Union

class EmbedBuilder:
    def __init__(self):
        self._embed = discord.Embed()
        self.default_colors = {
            'blue': 0x3498db,
            'light_blue': 0x00b0f4,
            'dark_blue': 0x206694,
            'success': 0x2ecc71,
            'error': 0xe74c3c,
            'warning': 0xf1c40f
        }
        self.set_color('blue')

    def set_title(self, title: str) -> 'EmbedBuilder':
        self._embed.title = title
        return self

    def set_description(self, description: str) -> 'EmbedBuilder':
        self._embed.description = description
        return self

    def add_field(self, name: str, value: str, inline: bool = False) -> 'EmbedBuilder':
        self._embed.add_field(name=name, value=value, inline=inline)
        return self

    def set_color(self, color: Union[str, int]) -> 'EmbedBuilder':
        if isinstance(color, str):
            color = self.default_colors.get(color.lower(), self.default_colors['blue'])
        self._embed.color = color
        return self

    def set_footer(self, text: str, icon_url: Optional[str] = None) -> 'EmbedBuilder':
        self._embed.set_footer(text=text, icon_url=icon_url)
        return self

    def set_thumbnail(self, url: str) -> 'EmbedBuilder':
        self._embed.set_thumbnail(url=url)
        return self

    def set_image(self, url: str) -> 'EmbedBuilder':
        self._embed.set_image(url=url)
        return self

    def clear_fields(self) -> 'EmbedBuilder':
        self._embed.clear_fields()
        return self

    def build(self) -> discord.Embed:
        return self._embed

    @classmethod
    def create_queue_embed(cls, current_song: Optional[dict] = None, songs: list = None) -> discord.Embed:
        builder = cls()
        builder.set_title("🎵 song queue")
        
        queue_text = ""
        if current_song:
            queue_text += f"**now playing:**\n{current_song['title']}\n\n"
        
        if songs:
            queue_text += "**next song(s):**\n"
            for i, song in enumerate(songs, 1):
                queue_text += f"{i}. {song['data']['title']}\n"
        
        if not queue_text:
            queue_text = "no songs in queue"
            
        builder.set_description(queue_text)
        return builder.build()