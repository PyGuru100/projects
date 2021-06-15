import tkinter as tk
import tkinter.filedialog
from PIL import Image, ImageDraw, ImageFont


window = tk.Tk()
window.title('Coffee-Mark')
window.geometry('500x500')


icon_or_text = tk.IntVar()
icon_or_text.set(1)
radio_icon = tk.Radiobutton(window,
                            text='Superimpose watermark', variable=icon_or_text, value=1)
radio_text = tk.Radiobutton(window,
                            text='Add Text', variable=icon_or_text, value=2)
radio_icon.pack()
radio_text.pack()


chosen_file = ""
chosen_icon = ""

browse_var = tk.IntVar()
browse_var.set(1)
radio_browse_image = tk.Radiobutton(window, text='Browse for image',
                                    variable=browse_var, value=1)
radio_browse_icon = tk.Radiobutton(window, text='Browse for watermark',
                                   variable=browse_var, value=2)


chosen_label = tk.Label(window, text='Chosen Image: None')
chosen_label.pack()

chosen_icon_label = tk.Label(window, text='Chosen Watermark: None')
chosen_icon_label.pack()


def browse():
    file_finder = tkinter.filedialog
    global chosen_file, chosen_icon
    if browse_var.get() == 1:
        chosen_file = file_finder.askopenfilename()
        chosen_label['text'] = f'Chosen Image: {chosen_file.split("/")[-1]}'
    else:
        chosen_icon = file_finder.askopenfilename()
        chosen_icon_label['text'] = f'Chosen Icon: {chosen_icon.split("/")[-1]}'


browse_button = tk.Button(window, text='Browse', command=browse)
browse_button.pack()
# I kept the radio button pack calls right here so they'd be in the right place in the GUI
# I had to define them before the browse function since it references the variable browse_var.
radio_browse_image.pack()
radio_browse_icon.pack()

missing_info_label = tk.Label(window, text="")

text_box_label = tk.Label(window,
                          text="Text you'd like to add (e.g. Copyright © Protected): ")
text_box_label.pack()
text_box = tk.Entry(window)
text_box.pack()

font_box_label = tk.Label(window, text='Font file name (e.g. Ramaraja-Regular.ttf)')
font_size_label = tk.Label(window, text="Font size")
font_box = tk.Entry(window)
font_size = tk.Scale(window, from_=1, to=78, orient='horizontal')
text_color_label = tk.Label(window, text='Text color (R, G, B)')
text_color_r = tk.Entry(window)
text_color_g = tk.Entry(window)
text_color_b = tk.Entry(window)


def add_mark():
    if icon_or_text.get() == 2:
        return add_text()
    if not chosen_file:
        missing_info_label['text'] = "No image selected."
        return
    if not chosen_icon:
        missing_info_label['text'] = "No watermark selected"
        return
    old_image = Image.open(chosen_file)
    icon_image = Image.open(chosen_icon)
    old_image.paste(icon_image, (0, 0))
    path = f'{chosen_file.split("/")[-1]}_icon_marked.png'
    old_image.save(path)
    missing_info_label['text'] = ""
    return path


def add_text():
    if not chosen_file:
        missing_info_label['text'] = "No image selected."
        return
    if not text_box.get():
        missing_info_label['text'] = "No text to add."
        return
    image = Image.open(chosen_file)
    width, height = image.size
    text_image = Image.new(image.mode, (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(text_image)
    # Ramaraja-Regular.ttf
    font = ImageFont.truetype(font_box.get(), font_size.get())
    r, g, b = (text_color_r.get(), text_color_g.get(), text_color_b.get())
    try:
        r, g, b = int(r), int(g), int(b)
    except ValueError:
        missing_info_label['text'] = "Invalid Color."
        return
    if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
        missing_info_label['text'] = "Invalid Color: values must be between 0 and 255"
        return
    for sample_width in [width//6 + _ * width // 2 for _ in range(0, 2)]:
        for sample_height in [height//6 + _ * height // 2 for _ in range(0, 2)]:
            print(sample_height, sample_width)
            draw.text(xy=(sample_height, sample_width),
                      text=text_box.get(), fill=(r, g, b), font=font)
            text_image.save('temp.png')
    image.paste(text_image, (0, 0), text_image.rotate(45))
    image.save('marked_image.png')
    missing_info_label['text'] = ""


font_box_label.pack()
font_box.pack()
font_size_label.pack()
font_size.pack()
text_color_label.pack()
text_color_r.pack()
text_color_g.pack()
text_color_b.pack()

mark_button = tk.Button(window, text='Add!', command=add_mark)
mark_button.pack()

missing_info_label.pack()

window.mainloop()
