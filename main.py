import ctypes
import random
import time
from time import sleep
from tkinter import *
from tkinter import ttk

user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)
window_width = screen_width/1.5
window_height = screen_height/1.5

window = Tk()
window.title("Sorting Algorythms Visualizer")
# icono = PhotoImage(file="images/logobot.png")
# window.iconphoto(True, icono)
window.geometry(str(int(window_width)) + "x" + str(int(window_height)))
# window.configure(background='#023047')
window.resizable(0, 0)
data = []
data_bars = []
data_texts = []

# TODO insercion mirar las notas de mi grupo de whtasapp
# TODO bloquear botones mientras está trabajando
# TODO añadir botón de pausa/cancelar
# TODO hacer el resto de algoritmos

def drawData():
    canvas_data.delete("all")
    window.update()
    canvas_height = canvas_data.winfo_height()
    canvas_width = canvas_data.winfo_width()
    data_element_width = canvas_width / slider_cantidad.get()
    font_size = (9.5 * window_width) / 1280
    if slider_cantidad.get() > 68:
        font_size = (7 * window_width) / 1280
    else:
        font_size = (9.5 * window_width) / 1280
    current_pos_x = 0
    print("canvas_height: " + str(canvas_height))
    for d in data:
        data_height = (canvas_height * 0.99 * d) / 100
        data_bar = canvas_data.create_rectangle(current_pos_x, canvas_height, current_pos_x + data_element_width, canvas_height - data_height, fill='#9CDBFB')
        data_bars.append(data_bar)
        data_text = canvas_data.create_text((current_pos_x + data_element_width / 2, canvas_height * 0.97), text=str(d), font=('Helvetica', str(int(font_size))))
        data_texts.append(data_text)
        current_pos_x = current_pos_x + data_element_width

def newData():
    data.clear()
    data_bars.clear()
    data_texts.clear()
    for x in range(slider_cantidad.get()):
        max_value = 100
        data.append(random.randint(5, max_value))
    drawData()


def swap(e1, e2):
    a, b, c, d = canvas_data.coords(data_bars[e1])
    e, f, g, h = canvas_data.coords(data_bars[e2])
    canvas_data.move(data_bars[e1], e - a, 0)
    canvas_data.move(data_bars[e2], a - e, 0)
    data_bar_aux = data_bars[e1]
    data_bars[e1] = data_bars[e2]
    data_bars[e2] = data_bar_aux

    k, l = canvas_data.coords(data_texts[e1])
    m, n = canvas_data.coords(data_texts[e2])
    canvas_data.coords(data_texts[e1], m, n)
    canvas_data.coords(data_texts[e2], k, l)
    canvas_data.tag_raise(data_texts[e1])
    canvas_data.tag_raise(data_texts[e2])
    text_aux = data_texts[e1]
    data_texts[e1] = data_texts[e2]
    data_texts[e2] = text_aux

    aux = data[e2]
    data[e2] = data[e1]
    data[e1] = aux


def sort():
    algoritmo = tipo_algo.get()
    if algoritmo == "Burbuja":
        bubbleSort()
    elif algoritmo == "Inserción":
        insertionSort()


def bubbleSort():
    encontrado = True
    while encontrado:
        encontrado = False
        for i in range(1, len(data)):
            velocidad = 1 / slider_velocidad.get()
            canvas_data.itemconfig(data_bars[i], fill='red')
            canvas_data.itemconfig(data_bars[i-1], fill='red')
            window.update()
            if data[i - 1] > data[i]:
                time.sleep(velocidad)
                swap(i - 1, i)
                window.update()
                encontrado = True
            time.sleep(velocidad)
            canvas_data.tag_raise(data_texts[i])
            canvas_data.tag_raise(data_texts[i-1])
            canvas_data.itemconfig(data_bars[i], fill='#9CDBFB')
            canvas_data.itemconfig(data_bars[i - 1], fill='#9CDBFB')
            window.update()


def insertionSort2():
    for step in range(1, len(data)):
        velocidad = 1 / slider_velocidad.get()
        time.sleep(velocidad)
        window.update()
        key = data[step]
        canvas_data.itemconfig(data_bars[step], fill='red')
        j = step - 1
        while j >= 0 and key < data[j]:
            data[j+1] = data[j]
            time.sleep(velocidad)
            swap(j, j+1)
            window.update()
            j = j - 1
        data[j+1] = key
        canvas_data.itemconfig(data_bars[step], fill='#9CDBFB')

def insertionSort():
    for step in range(1, len(data)):
        velocidad = 1 / slider_velocidad.get()
        time.sleep(1)
        window.update()
        key = data[step]
        canvas_data.itemconfig(data_bars[step], state='hidden')  # hidden/normal
        k, l, m, n = canvas_data.coords(data_bars[step])
        key_bar = data_bars.pop(step)
        j = step - 1
        while j >= 0 and key < data[j]:
            data[j+1] = data[j]

            a, b, c, d = canvas_data.coords(data_bars[j])
            e, f, g, h = canvas_data.coords(data_bars[j+1])

            canvas_data.move(data_bars[j], e - a, 0)
            data_bars[j+1] = data_bars[j]
            # canvas_data.move(data_bars[j+1], a - e, 0)

            time.sleep(1)

            window.update()
            j = j - 1
        data[j+1] = key
        #canvas_data.itemconfig(data_bars[j+1], state='normal')
        data_bars.insert(j+1, key_bar)
        canvas_data.move(data_bars[step], k - e, 0) # mover desde key_bar hasta j+1
        data_bars[j+1] = key_bar
        window.update()



# Ventana principal
main_frame = LabelFrame(window)
main_frame.pack(fill='both', expand=1)

for x in range(12):
    main_frame.grid_rowconfigure(x, weight=1)
    main_frame.grid_columnconfigure(x, weight=1)

# Botones
button_new_data = Button(main_frame, text="Nuevos datos", command=newData)
button_new_data.configure(background='#A5A5A5')
button_new_data.grid(row=9, column=0, rowspan=2, columnspan=3, sticky='nsew')

slider_cantidad = Scale(main_frame, from_=3, to=100, orient=HORIZONTAL)
slider_cantidad.grid(row=9, column=3, rowspan=2, columnspan=3, sticky='nsew')
slider_cantidad.set(25)

slider_velocidad = Scale(main_frame, from_=1, to=1000, orient=HORIZONTAL)
slider_velocidad.grid(row=10, column=3, rowspan=2, columnspan=3, sticky='nsew')
slider_velocidad.set(500)

tipo_algo = ttk.Combobox(main_frame, state='readonly', values=["Burbuja", "Inserción"])
tipo_algo.current(1)
tipo_algo.grid(row=9, column=6, rowspan=2, columnspan=3, sticky='nsew')

button_sort = Button(main_frame, text="Ordenar", command=sort)
button_sort.configure(background='#A5A5A5')
button_sort.grid(row=9, column=9, rowspan=2, columnspan=3, sticky='nsew')

# Datos
canvas_data = Canvas(main_frame, highlightbackground='black', background="#ECE7EC")
canvas_data.grid(row=0, column=0, rowspan=8, columnspan=12, sticky='nsew')
newData()

window.mainloop()