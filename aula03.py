import PySimpleGUI as sg
from PIL import Image
import PIL.ExifTags 
import webbrowser 
import io
import os

image_atual = None
image_path = None
max_width = None
max_height = None

def resize_image(img):
    global image_atual
    global max_width
    global max_height

    try: 
        if image_atual:
            width, height = image_atual.size
            aspect_ratio = width / height

            new_widht = max_width
            new_height = int(max_width / aspect_ratio)
            img = img.resize((new_widht, new_height), Image.LANCZOS)

            new_height = max_height
            new_widht = int(max_height / aspect_ratio)
            img = img.resize((new_height, new_height), Image.LANCZOS)            

            return img
    except Exception as e:
        sg.popup("Nenhuma imagem encontrada")


    # img = img.resize((800, 600), Image.Resampling.LANCZOS) 
    # return img

def show_image(resized_img):
    img_bytes = io.BytesIO() #Permite criar objetos semelhantes a arquivos na memória RAM
    resized_img.save(img_bytes, format='PNG')
    window['-IMAGE-'].update(data=img_bytes.getvalue())

def open_image(filename):
    global image_atual
    global image_path
    global max_width
    global max_height
    image_path = filename
    image_atual = Image.open(filename)  
    max_height, max_width = image_atual.size  
    
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

def openLink(x, y):
    webbrowser.open(f'https://www.google.com.br/maps/@{x},{y},20z?entry=ttu')

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
                        if(value[3] == 'W'):
                            p2 = p2*-1

                        openLink(p1, p2)

                        # print(p1, " ", p2)
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
            ['Arquivo', ['Abrir', 'Salvar', 'Fechar',]],
            ['Sobre a image', ['Informacoes']],
            ['Edit', ['PB']],
            ['Sobre', ['Desenvolvedor']]
        ])],
    [sg.Image(key='-IMAGE-', size=(800, 600))],
]

window = sg.Window('Aplicativo de image', layout, finalize=True)

def gray_scale():
    global image_atual
    global previous_state
    try:
        if image_atual:
            width, height = image_atual.size
            pixels = image_atual.load()
            previous_state = image_atual.copy()

            for w in range(width):
                for h in range(height):
                    r, g, b = image_atual.getpixel((w, h))
                    gray = int(0.3 * r + 0.6 * g + 0.1 * b)
                    pixels[w, h] = (gray, gray, gray)

            show_image(resize_image(image_atual))

        else:
            sg.popup("Nenhuma imagem aberta")

    except:
        print("sim")

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
    elif event == 'PB':
        gray_scale()
    elif event == 'Informacoes':
        info_image()
        get_exif_data(arquivo)
    elif event == 'Desenvolvedor':
        sg.popup('Desenvolvido por Tais Arantes - BCC 6º Semestre')
    




window.close()