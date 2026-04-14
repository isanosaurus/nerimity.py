from pathlib import Path
import base64
import zlib
import json
from nerimity._enums import EmbedTypes


class Embed():
	"""
	Represents a Nerimity embed payload.

	The current implementation supports HTML embeds and standard embeds (not yet implemented in Nerimity).

	type: The type of the embed (e.g., HTML, standard).
	body: The body of the embed, which can be raw HTML or a string representation of a standard embed.

	construct(html): static | Creates an Embed from raw HTML.
	from_file(file_path, encoding): static | Creates an Embed by reading an HTML file.
	to_payload(): Converts this embed to an API payload fragment.
	_decode(data): private static | Unzips the Base64, zipped data from the Websocket into a JSON object.
	"""

	def __init__(self, data: str = "", type: int = EmbedTypes.HTML) -> None:
		self.type: int = type
		self.body: str = Embed._decode(data) if type == EmbedTypes.HTML and data else data

	# Public Static: Creates an Embed from raw HTML.
	@staticmethod
	def construct(data: str, type: int = EmbedTypes.HTML) -> 'Embed':
		"""static | Creates an Embed from raw HTML."""

		return Embed(data=data, type=type)

	# Public Static: Creates an Embed by reading an HTML file.
	@staticmethod
	def from_file(file_path: str | Path, encoding: str = "utf-8") -> 'Embed':
		"""static | Creates an Embed by reading an HTML file."""

		resolved_path = Path(file_path)
		with resolved_path.open("r", encoding=encoding) as html_file:
			return Embed(body=html_file.read())

	# Public: Converts this embed to an API payload fragment.
	def to_payload(self) -> dict:
		"""Converts this embed to an API payload fragment."""

		return {
			"htmlEmbed": str(self),
		}

	def __str__(self) -> str:
		return self.body
	
	# Private Static: Unzips the Base64, zipped data from the Websocket into a JSON object.
	@staticmethod
	def _decode(data: str) -> dict:
		"""private static | Unzips the Base64, zipped data from the Websocket into a JSON object."""
		decoded_data = base64.b64decode(data)
		decompressed_data = zlib.decompress(decoded_data)
		return json.loads(decompressed_data.decode("utf-8"))
	
	# Static: Deserialize a JSON object to an Embed object.
	@staticmethod
	def deserialize(json: dict) -> 'Embed':
		"""static | Deserialize a JSON object to an Embed object."""

		if not isinstance(json, dict):
			raise TypeError(f"Invalid JSON object for deserialization: {json}")
	
		if "htmlEmbed" in json and json["htmlEmbed"] is not None:
			return Embed(body=Embed._decode(json["htmlEmbed"]), type=EmbedTypes.HTML)
		
		if "embed" in json and json["embed"] is not None:
			return Embed(body=str(json["embed"]), type=EmbedTypes.STANDARD)

		raise ValueError(f"Invalid JSON object for deserialization: {json}")