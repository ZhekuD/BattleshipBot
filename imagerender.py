from PIL import Image
from io import BytesIO
from pathlib import Path
from BattleshipGame.rules import Ship


FOLDER = Path(__file__).resolve().parent.joinpath('images')

empty_cell = Image.open(FOLDER.joinpath('empty.jpg'))
ship_cell = Image.open(FOLDER.joinpath('ship.jpg'))
miss_cell = Image.open(FOLDER.joinpath('miss.jpg'))
hit_cell = Image.open(FOLDER.joinpath('hit.jpg'))
empty_field = Image.open(FOLDER.joinpath('field.jpg'))


def create_picture(field):
    generator = ((i, k) for k in range(20, 220, 20) for i in range(20, 220, 20))
    new_im = empty_field

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
