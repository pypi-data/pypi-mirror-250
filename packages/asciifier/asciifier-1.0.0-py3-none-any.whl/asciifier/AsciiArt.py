from requests import get
from io import BytesIO
from PIL import Image
from numpy import array, ndarray

import _constants


def image_to_string(filepath: str, in_place: bool = True, colours: list[str] = _constants.GREYS) -> str | None:
    """
    Convert an image to ASCII art.
    
    :param filepath: Path to the image file.
    :type filepath: str
    :param in_place: If True, prints the ASCII art. If False, returns the ASCII art as a string.
    :type in_place: bool
    :param colours: A list of characters representing greyscale values.
    :type colours: list[str]
    
    :returns ASCII art representation of the image (if in_place is False)
    :rtype str
    """

    image: Image.Image = \
        Image.open(BytesIO(get(filepath).content)) \
        if "https://" in filepath or "http://" in filepath \
        else Image.open(filepath)

    image_array: ndarray = array(image)
    greyscale: bool = len(image_array.shape) == 2

    colour_scale: int = len(colours) - 1
    normalised_image: ndarray = (image_array.mean(axis=2) / 255 * colour_scale if not greyscale
                                 else image_array / 255 * colour_scale).astype(int)

    if in_place:
        for row in normalised_image:
            print("".join(colours[val] * 2 for val in row))
        return None
    else:
        return "\n".join("".join(colours[val] * 2 for val in row) for row in normalised_image)
