import boto3
import fitz
import tkinter as tk
import tkinter.filedialog

window = tk.Tk()
window.geometry('400x300')
window.title('PDF --> MP3')
file_path, file_extension, file_name = "", "", ""

# noinspection SpellCheckingInspection
polly_client = boto3.Session(aws_access_key_id='INSERT KEY HERE',
                             aws_secret_access_key='SOME KEY',
                             region_name='us-west-2').client('polly')


def browse():
    global file_path, file_extension, file_name
    file_path = tkinter.filedialog.askopenfilename()
    file_extension, file_name = file_path.split('.')[-1], file_path.split('/')[-1]
    if file_extension != 'pdf':
        file_path, file_extension, file_name = "", "", ""
        button_label['text'] = "Please select a PDF file."
        return
    button_label['text'] = f'PDF File Selected: {file_name}'


button_label = tk.Label(window, text='PDF File Selected: ')
button = tk.Button(window, text='Browse', command=browse)
button_label.pack()
button.pack()


def convert():
    global file_path
    if not file_path:
        button_label['text'] = f"Please select a PDF file."
        return
    if not name_entry.get():
        convert_label['text'] = "Please Input desired audio file name: "
        return
    # Let's grab us some PDF text y'all
    # noinspection PyUnresolvedReferences
    with fitz.open(file_path) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
        # gets rid of auto-hyphenation and and line breaks.
        pdf_text = (text.replace('-\n', '').replace('\n', ''))
    parts = [pdf_text[i: i + 900] for i in range(0, len(pdf_text), 900)]

    for _ in range(len(parts)):
        response = polly_client.synthesize_speech(VoiceId='Joanna',
                                                  OutputFormat='mp3',
                                                  Text=parts[_],
                                                  Engine='neural')
        file = open(f'temp/{name_entry.get()}{_ + 1}.mp3', 'wb')
        file.write(response['AudioStream'].read())
        file.close()


convert_label = tk.Label(window, text="Input desired audio file name: ")
name_entry = tk.Entry(window)
convert_button = tk.Button(window, text="Convert to audio book!", command=convert)
last_label = tk.Label(window, text="Don't panic if it looks frozen during conversion.\n "
                                   "If the MP3 file shows up, you're done.")
convert_label.pack()
name_entry.pack()
convert_button.pack()
last_label.pack()

window.mainloop()
