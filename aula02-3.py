import PySimpleGUI as sg
from PIL import Image
import PIL.ExifTags 
import io
import os

image_atual = None
image_path = None

def resize_image(img):
    img = img.resize((800, 600), Image.Resampling.LANCZOS) 
    return img

def open_image(filename):
    global image_atual
    global image_path
    image_path = filename
    image_atual = Image.open(filename)    
    
    resized_img = resize_image(image_atual)
    #Converte a image PIL para o formato que o PySimpleGUI
    img_bytes = io.BytesIO() #Permite criar objetos semelhantes a arquivos na memória RAM
    resized_img.save(img_bytes, format='PNG')
    window['-IMAGE-'].update(data=img_bytes.getvalue())

def save_image(filename):
    global image_path
    if image_path:
        image_atual = Image.open(image_path)
        with open(filename, 'wb') as file:
            image_atual.save(file)

def get_exif_data(image_path):
    img = Image.open(image_path)
    if hasattr(img, '_getexif'):
        exif_data = img._getexif()

        if exif_data:
                # Obtenha tags EXIF e seus nomes legíveis
                exif_tags = {v: k for k, v in PIL.ExifTags.TAGS.items()}

                for tag_id, value in exif_data.items():
                    tag_name = exif_tags.get(tag_id, tag_id)
                    if(tag_name == 34853):
                        x = value[2]
                        p1 = convert_to_degress(x)
                        y = value[4]
                        p2 = convert_to_degress(y)

                        print(p1, " ", p2)
                        # https://www.google.com.br/maps/@20.6480833,-156.4424444,20z?entry=ttu -> resultado
                        # print(value[1], " ",  value[2])
                        # print(value[3], " ", value[4])
                    # print(f"{tag_name}: {value}")
                    
        else:
                print("Nenhum metadado EXIF encontrado.")
    else:
        print("A imagem não possui suporte a EXIF.")

def convert_to_degress(value):
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
    a, b, c = value
    return float(a) + (float(b) / 60.0) + (float(c) / 3600.0)

def info_image():
    global image_atual
    global image_path
    image_atual = Image.open(image_path)
    if image_atual:
        largura, altura = image_atual.size
        formato = image_atual.format
        tamanho_bytes = os.path.getsize(image_path)
        tamanho_mb = tamanho_bytes / (1024 * 1024)
        sg.popup(f"Tamanho: {largura} x {altura}\nFormato: {formato}\nTamanho em MB: {tamanho_mb:.2f}")

layout = [
    [sg.Menu([
            ['Arquivo', ['Abrir', 'Salvar', 'Fechar']],
            ['Sobre a image', ['Informacoes']], 
            ['Sobre', ['Desenvolvedor']]
        ])],
    [sg.Image(key='-IMAGE-', size=(800, 600))],
]

window = sg.Window('Aplicativo de image', layout, finalize=True)

while True:
    event, values = window.read()

    if event in (sg.WINDOW_CLOSED, 'Fechar'):
        break
    elif event == 'Abrir':
        arquivo = sg.popup_get_file('Selecionar image', file_types=(("Imagens", "*.png;*.jpg;*.jpeg;*.gif"),))
        if arquivo:
            open_image(arquivo)
    elif event == 'Salvar':
        if image_atual:
            arquivo = sg.popup_get_file('Salvar image como', save_as=True, file_types=(("Imagens", "*.png;*.jpg;*.jpeg;*.gif"),))
            if arquivo:
                save_image(arquivo)
    elif event == 'Informacoes':
        info_image()
        get_exif_data(arquivo)
    elif event == 'Desenvolvedor':
        sg.popup('Desenvolvido por Tais Arantes - BCC 6º Semestre')




window.close()