from PIL import Image
import io
import PySimpleGUI as sg

def load_image(path):
    img = Image.open(path)
    img.thumbnail((600, 600))
    bio = io.BytesIO()
    img.save(bio, format = 'PNG')
    return bio.getvalue()

menu_def = [['Open File', ['Open']], ['Help', ['About']],]

layout = [[sg.Menu(menu_def)],
          [sg.Text("PhotoXpress")],
          [sg.Image(key = 'image')]]

window = sg.Window("Menu", layout, size=(700, 600))

while True:
    event, values = window.read()

    if event == 'Open':
        imgdata = sg.popup_get_file("Selecione uma imagem", file_types=(("Image Files", "*.jpg;" "*.png;" "*.bmp;" "*.jpeg;"),))
        if imgdata:
            img = load_image(imgdata)
            window['image'].update(data=img)
    if event == 'Abbout':
        sg.popup("São Paulo Futebol Clube")
    if event == sg.WIN_CLOSED:
      break

window.close() 