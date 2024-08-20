from PIL import Image
import pathlib


image = Image.open("tighnari.jpg")
image.show("tighnari")

width, height = image.size
print('junto:' + str(image.size))
print(f'width: {width}')
print(f'height: {height}')
print('nome: ' + image.filename)
print('formato: ' + image.format)
print('formato desc: ' + image.format_description)


def image_converter(input_file_path, output_file_path):
    image.save(output_file_path)
    original_suffix = pathlib.Path(input_file_path).suffix
    new_suffix = pathlib.Path(output_file_path).suffix
    print(f"Convertendo {input_file_path} de {original_suffix} para {new_suffix}")

if __name__ == "__main__":
    image_converter("tighnari.jpg", "tighnari.png")