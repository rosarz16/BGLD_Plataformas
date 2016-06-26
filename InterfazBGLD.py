import Tkinter
from Tkinter import *
from PIL import ImageTk, Image
import tkFileDialog
import os

# Aqui capturo cual es el path del programa. Las imagenes y el .txt tienen que estar en el mismo
# directorio. Las imagenes porque las busca en este path, y el .txt en realidad solo para que
# sea mas rapido encontrarlo :P. Cuando busca el .txt lo puede buscar en cualquier lugar de la compu
mypath = os.path.dirname(os.path.realpath(__file__))

# Esto es para definir las condiciones iniciales de mis variables globales. Al inicio todo esta vacio

# data es la informacion del .txt
data = ""
# son los vectores que se van a enviar a C
vector1 = []
vector2 = []

# Es el resultado del programa de C, es un numero 0, 1, 2 o 3. Hay que verificar si los casos de
# VERY HIGH, HIGH, LOW, VERY LOW tienen sentido con lo que yo puse y lo que supuestamente tira C
input_c = 0

# Esta es la clase que abre la ventana para buscar el .txt. Se activa despues de tocar el boton.
# Adentro, si el archivo no esta vacio, guarda los datos y cambia el icono. Si no se escoge ningun
# archivo y solo se le da "cancelar", entonces el boton no hace nada.

def import_data_file():
    filewindow = Tkinter.Tk()
    filewindow.withdraw()
    file_opened = tkFileDialog.askopenfile(parent=filewindow, mode='rb', title='Choose a file')
    if file_opened is not None:
        global data
        data = file_opened.read()
        file_opened.close()
        global img_status
        global status_pic
        img_status = ImageTk.PhotoImage(Image.open(mypath + '/Green_check.png'))
        status_pic = Tkinter.Label(App, image=img_status)
        status_pic.grid(row=3, column=1, padx=230, sticky=W, columnspan=2)
        # askfordata_button.config(background='green')
    filewindow.destroy()

# Esta es la clase en donde tiene que adjuntarse lo de C. Aqui es donde se trabaja los datos.
# Primero separa las filas y las mete en una lista de strings, luego lo transforma a flotantes
# (no estaba segura si solo eran valores integer) y hace los vectores vector1 y vector2 que son
# los que tiene que recibir C.

def send_data_vectors():
    global data
    global vector1
    global vector2

    rows = data.split('\n')

    for single in range(0, len(rows)):
        if rows[single] != "":
            columns = rows[single].split(',')
            columns = map(float, columns)
            vector1.append(columns[0])
            vector2.append(columns[1])

    print vector2, vector1

    # Aqui va la union con C, yo puse los casos del 0-3 pero sin son del 1-4 solo hay que modificarlos
    global input_c

    input_c = 1
    if input_c == 0:
        g_result = "VERY HIGH"
    if input_c == 1:
        g_result = "HIGH"
    if input_c == 2:
        g_result = "LOw"
    if input_c == 3:
        g_result = "VERY LOW"

    # Imprime el resultado al final de la interfaz

    results_text = Label(App, fg="#4D5C64", text="Your glucose result is: " + g_result, font=("Helvetica", 12))
    results_text.grid(row=5, column=0, padx=200, sticky=W, columnspan=2)
    results_text.config(width=30)

# Aqui comienza la programacion de la Interfaz grafica como tal

# Este es el nombre de la caja grande que contiene toddo, (botones, etiquetas..)
App = Tkinter.Tk()
# Este es el tamanho de la caja que yo decidi
App.geometry("700x450+-10+20")
# Este es el titulo del cuadro jaja. Si quieren lo cambiamos
App.title("BGLD Application")

# Aqui abro y coloco la imagen del logo QUE HAY QUE CAMBIAR
img = Image.open(mypath+'/Intel-logo.png')
img = img.resize((250, 100), Image.ANTIALIAS)
img = ImageTk.PhotoImage(img)
panel = Tkinter.Label(App, image=img)
panel.grid(padx=20, pady=25)

# Aqui abro y coloco la imagen del signo de pregunta. En la clase import_data_file() se sobreescribe
# por el check verde

img_status = Image.open(mypath+'/Question_mark.png')
img_status = ImageTk.PhotoImage(img_status)
status_pic = Tkinter.Label(App, image=img_status)
status_pic.grid(row=3, column=1, padx=230, sticky=W, columnspan=2)

# Aqui esta la programacion del texto polo jaja.

advice = Label(App, fg="#5FABD1", text="Because your health is first," + "\n" + " keep a good control of your glucose!",
               font=("Helvetica", 16))
advice.grid(row=0, column=1)

# Programacion del texto que pide abrir el .txt
askfordata = Label(App, fg="#4D5C64", text="Please select the input file" + "\n" + "with your blood patron:", font=("Helvetica", 12))
askfordata.grid(row=3, column=0, sticky=W, padx=100, columnspan=2)

# Programacion del boton que pide abrir el .txt
askfordata_button = Button(App, text="Click here to search your file", width=20, command=import_data_file)
askfordata_button.grid(row=3, column=1, padx=25, sticky=W, columnspan=2)

#Programacion del boton que inicia con los calculos
askforcalc_button = Button(App, text="Click here to calculate your results", width=20, command=send_data_vectors)
askforcalc_button.grid(row=4, column=0, padx=200, pady=50, sticky=W, columnspan=2)
askforcalc_button.config(width=30)

App.mainloop()
