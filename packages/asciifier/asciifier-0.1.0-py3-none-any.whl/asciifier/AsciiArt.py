import requests
from PIL import Image
from numpy import array, ndarray

greys = (' ', '.', '-', '"', 'r', '/', '>', ')', '[', 'I', 'Y', 'Z', 'h', '#', '8', '@')
IMAGE_STORE_FP = "../imageStore/image.jpg"


def image_to_string(filepath: str, in_place: object = True, colours: list[str] = greys) -> str | None:
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

    if "https://" in filepath or "http://" in filepath:
        response = requests.get(filepath)

        with open(IMAGE_STORE_FP, "wb") as f:
            f.write(response.content)
        filepath = IMAGE_STORE_FP

    image: Image.Image = Image.open(filepath)
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
