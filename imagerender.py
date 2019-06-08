from PIL import Image
from io import BytesIO
from pathlib import Path
from BattleshipGame.rules import Ship

imageFolder = Path(__file__).resolve().parent.joinpath('images')

empty_cell = Image.open(imageFolder.joinpath('empty.png'))
ship_cell = Image.open(imageFolder.joinpath('ship.png'))
miss_cell = Image.open(imageFolder.joinpath('miss.png'))
hit_cell = Image.open(imageFolder.joinpath('hit.png'))


def create_picture(field):
    generator = ((i, k) for k in range(0, 300, 30) for i in range(0, 300, 30))
    new_im = Image.new('RGB', (300, 300))

    for line in field:
        for cell in line:
            if isinstance(cell, Ship):
                new_im.paste(ship_cell, next(generator))
            elif cell == 'miss' or cell == 8:
                new_im.paste(miss_cell, next(generator))
            elif cell == 'hit' or cell == 1 or cell == 2:
                new_im.paste(hit_cell, next(generator))
            else:
                new_im.paste(empty_cell, next(generator))

    output = BytesIO()
    new_im.save(output, format="JPEG")
    return output.getvalue()
