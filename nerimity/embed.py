from pathlib import Path
from nerimity._enums import EmbedTypes


class Embed():
	"""
	Represents a Nerimity embed payload.

	The current implementation supports HTML embeds.

	type: Embed type, see EmbedTypes.
	html: Raw HTML that will be sent as htmlEmbed.

	construct(html): static | Creates an Embed from raw HTML.
	from_file(file_path, encoding): static | Creates an Embed by reading an HTML file.
	to_payload(): Converts this embed to an API payload fragment.
	"""

	def __init__(self, html: str = "", embed_type: int = EmbedTypes.HTML) -> None:
		self.type: int = embed_type
		self.html: str = str(html)

	# Public Static: Creates an Embed from raw HTML.
	@staticmethod
	def construct(html: str) -> 'Embed':
		"""static | Creates an Embed from raw HTML."""

		return Embed(html=html)

	# Public Static: Creates an Embed by reading an HTML file.
	@staticmethod
	def from_file(file_path: str | Path, encoding: str = "utf-8") -> 'Embed':
		"""static | Creates an Embed by reading an HTML file."""

		resolved_path = Path(file_path)
		with resolved_path.open("r", encoding=encoding) as html_file:
			return Embed(html=html_file.read())

	# Public: Converts this embed to an API payload fragment.
	def to_payload(self) -> dict:
		"""Converts this embed to an API payload fragment."""

		return {
			"htmlEmbed": str(self),
		}

	def __str__(self) -> str:
		return self.html
