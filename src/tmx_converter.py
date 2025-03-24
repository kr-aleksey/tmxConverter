import xml.etree.ElementTree as ET
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import os


def extract_text(seg_elem):
    fragments = []
    for elem in seg_elem.iter():
        if elem.tag == "seg" and elem.text:
            fragments.append(elem.text)
        elif elem.tag == "ph" and elem.tail:
            x_val = elem.attrib.get('x', 'X')
            fragments.append(f'{{x{x_val}}}{elem.tail}')
    return ' '.join(fragments)


def convert_tmx_to_excel(tmx_path, output_path):
    tree = ET.parse(tmx_path)
    root = tree.getroot()

    tu_elements = list(root.iter("tu"))
    rows = []
    lang_set = set()

    for tu in tu_elements:
        segments = {}
        for tuv in tu.findall("tuv"):
            lang = tuv.attrib.get("{http://www.w3.org/XML/1998/namespace}lang",
                                  "unknown")
            seg = tuv.find("seg")
            if seg is not None:
                clean_text = extract_text(seg)
                segments[lang] = clean_text

        if len(segments) >= 2:
            langs = list(segments.keys())
            row = [segments[langs[0]], segments[langs[1]]]
            rows.append(row)
            lang_set.update(langs[:2])

    if not rows:
        raise ValueError("Переводы не найдены.")

    lang_list = list(lang_set)[:2]
    df = pd.DataFrame(rows, columns=lang_list)
    df.to_excel(output_path, index=False)


def select_and_convert_file():
    filepath = filedialog.askopenfilename(filetypes=[("TMX files", "*.tmx")])
    if not filepath:
        return

    try:
        output_path = os.path.splitext(filepath)[0] + "_converted.xlsx"
        convert_tmx_to_excel(filepath, output_path)
        messagebox.showinfo("Успех", f"Файл сохранён:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))


def main():
    root = tk.Tk()
    root.title("TMX → Excel Конвертер")
    root.geometry("300x150")

    label = tk.Label(root, text="Выберите TMX файл для конвертации:")
    label.pack(pady=20)

    button = tk.Button(root, text="Выбрать файл",
                       command=select_and_convert_file)
    button.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
