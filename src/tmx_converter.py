import xml.etree.ElementTree as ET
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import os


def extract_text(seg_elem):
    """
    Извлекает текст xml элемента. Заменяет вложенные теги
    placeholder (<ph x="1" type="1" />) на "@\\{x}"
    """
    fragments = []
    for elem in seg_elem.iter():
        if elem.tag == 'seg' and elem.text:
            fragments.append(elem.text)
        elif elem.tag == 'ph':
            tag_id = elem.attrib.get('x', '')
            tag_text = f' {elem.tail}' if elem.tail else ''
            fragments.append(f'@\\{tag_id}{tag_text}')
    return ' '.join(fragments)


def convert_tmx_to_excel(tmx_path, output_path):
    rows = []
    langs = []

    tree = ET.parse(tmx_path)
    root = tree.getroot()

    for tu in root.iter('tu'):
        segments = {}
        for tuv in tu.findall('tuv'):
            lang = tuv.attrib.get('{http://www.w3.org/XML/1998/namespace}lang')
            if lang is None:
                continue
            if lang not in langs:
                langs.append(lang)

            seg = tuv.find('seg')
            if seg is not None:
                segments[lang] = extract_text(seg)

        rows.append(segments)

    if not rows:
        raise ValueError('Переводы не найдены.')

    df = pd.DataFrame(rows, columns=list(langs))
    df.to_excel(output_path, index=False)


def select_and_convert_file():
    filepath = filedialog.askopenfilename(filetypes=[('TMX files', '*.tmx')])
    if not filepath:
        return

    try:
        output_path = os.path.splitext(filepath)[0] + '_converted.xlsx'
        convert_tmx_to_excel(filepath, output_path)
        messagebox.showinfo(
            'Успех', f'Файл сохранён:\n{output_path}')
    except Exception as e:
        messagebox.showerror('Ошибка', str(e))


def main():
    root = tk.Tk()
    root.title('TMX → Excel Конвертер')
    root.geometry('300x150')

    label = tk.Label(root, text='Выберите TMX файл для конвертации:')
    label.pack(pady=20)

    button = tk.Button(root,
                       text='Выбрать файл',
                       command=select_and_convert_file)
    button.pack()

    root.mainloop()


if __name__ == '__main__':
    main()
