import pytesseract
from PIL import Image
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

folder = r'c:\Users\Brian\Desktop\足球'
outfile = r'c:\Users\Brian\xundao\ocr_seriea.txt'

with open(outfile, 'w', encoding='utf-8') as out:
    for i, f in enumerate(sorted(os.listdir(folder))):
        if not f.endswith('.jpg'):
            continue
        path = os.path.join(folder, f)
        img = Image.open(path)
        w, h = img.size

        # Crop sections for better OCR
        top = img.crop((0, 0, w, int(h * 0.25)))
        mid = img.crop((0, int(h * 0.25), w, int(h * 0.85)))
        bot = img.crop((0, int(h * 0.85), w, h))

        out.write(f'\n===== 图{i+1}: {f} =====\n')

        text_top = pytesseract.image_to_string(top, lang='eng', config='--psm 6')
        out.write('---TOP---\n')
        out.write(text_top)

        text_mid = pytesseract.image_to_string(mid, lang='eng', config='--psm 4')
        out.write('---MID---\n')
        out.write(text_mid)

        text_bot = pytesseract.image_to_string(bot, lang='eng', config='--psm 6')
        out.write('---BOT---\n')
        out.write(text_bot)

        out.write('\n')

print(f'Done: {outfile}')
