"""ANSI 3D spinning donut (ASCII torus).

Run in a terminal. Stop with Ctrl+C.
"""

import math
import os
import shutil
import sys
import time


PALETTE = [
	("\x1b[38;5;240m", "·"),
	("\x1b[38;5;244m", ","),
	("\x1b[38;5;248m", "-"),
	("\x1b[38;5;250m", "~"),
	("\x1b[38;5;252m", ":"),
	("\x1b[38;5;255m", ";"),
	("\x1b[38;5;153m", "="),
	("\x1b[38;5;117m", "!"),
	("\x1b[38;5;51m", "*"),
	("\x1b[38;5;50m", "#"),
	("\x1b[38;5;48m", "$"),
	("\x1b[38;5;46m", "@"),
]


def clear_screen() -> None:
	sys.stdout.write("\x1b[2J\x1b[H")
	sys.stdout.flush()


def terminal_size(default_width: int = 80, default_height: int = 24) -> tuple[int, int]:
	size = shutil.get_terminal_size(fallback=(default_width, default_height))
	return size.columns, max(20, size.lines - 2)


def render_frame(A: float, B: float, width: int, height: int) -> str:
	z_buffer = [0.0] * (width * height)
	char_buffer = [" "] * (width * height)
	color_buffer = ["\x1b[0m"] * (width * height)

	for theta in frange(0.0, 2 * math.pi, 0.07):
		cost, sint = math.cos(theta), math.sin(theta)
		for phi in frange(0.0, 2 * math.pi, 0.02):
			cosp, sinp = math.cos(phi), math.sin(phi)

			circle_x = 1.0 + 0.5 * cosp
			circle_y = 0.5 * sinp

			x = circle_x * (cost * math.cos(A) + sint * math.sin(A))
			y = circle_x * (cost * math.sin(A) - sint * math.cos(A))
			z = 2.0 + circle_y * math.sin(B) + x * math.sin(B)
			ooz = 1.0 / z

			xp = int(width / 2 + 30 * ooz * (circle_y * math.cos(B) + x * math.cos(B)))
			yp = int(height / 2 + 15 * ooz * y)

			nx = cosp * cost
			ny = cosp * sint
			nz = sinp
			luminance = nx * math.sin(B) + ny * math.sin(A) + nz * math.cos(B)
			lum_idx = max(0, min(len(PALETTE) - 1, int((luminance + 1) * (len(PALETTE) - 1) / 2)))

			idx = xp + yp * width
			if 0 <= xp < width and 0 <= yp < height and ooz > z_buffer[idx]:
				z_buffer[idx] = ooz
				color_buffer[idx], char_buffer[idx] = PALETTE[lum_idx]

	rows = []
	for row_start in range(0, width * height, width):
		row_chars = []
		last_color = "\x1b[0m"
		for i in range(row_start, row_start + width):
			color = color_buffer[i]
			if color != last_color:
				row_chars.append(color)
				last_color = color
			row_chars.append(char_buffer[i])
		if last_color != "\x1b[0m":
			row_chars.append("\x1b[0m")
		rows.append("".join(row_chars))
	return "\n".join(rows)


def frange(start: float, end: float, step: float):
	while start < end:
		yield start
		start += step


def main():
	A = 0.0
	B = 0.0
	clear_screen()
	try:
		while True:
			width, height = terminal_size()
			frame = render_frame(A, B, width, height)
			clear_screen()
			sys.stdout.write(frame)
			sys.stdout.flush()
			A += 0.07
			B += 0.03
			time.sleep(0.03)
	except KeyboardInterrupt:
		clear_screen()
		print("Thanks for watching the 3D donut! 🍩")


if __name__ == "__main__":
	main()
