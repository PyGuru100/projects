import extcolors


def extract(image_path: str) -> list:
    colors = extcolors.extract_from_path(image_path)
    return [color[0] for color in colors[0]]


print(extract('123.jpg'))
