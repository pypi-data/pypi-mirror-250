from typing import List
import subprocess

class Command:
	def __init__(self, args: str | List[str]):
		self.args = []
		self.add(args)

	def run(self):
		subprocess.run(self.args)

	def add(self, args: str | List[str]):
		if isinstance(args, str):
			self.args.extend(args.split())
		elif isinstance(args, list):
			self.args.extend(args)
		else:
			raise TypeError(f'args must be str or list, not {type(args)}')
	
	def __str__(self):
		return ' '.join(self.args)
	
	def __repr__(self):
		return f'Command({self.args})'