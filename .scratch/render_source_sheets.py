from pathlib import Path
import sys
import pypdfium2 as pdfium
from PIL import Image, ImageDraw
root=Path(__file__).resolve().parents[1]
out=root/'.scratch/source-images'
out.mkdir(exist_ok=True)
for name in sys.argv[1:]:
    doc=pdfium.PdfDocument(root/'LGU_HUB_ECE2050'/name)
    for start in range(0,len(doc),8):
        sheet=Image.new('RGB',(1400,2000),'#dddddd'); draw=ImageDraw.Draw(sheet)
        for j in range(min(8,len(doc)-start)):
            page=doc[start+j]; im=page.render(scale=1.2).to_pil().convert('RGB')
            im.thumbnail((690,465))
            x=(j%2)*700; y=(j//2)*500
            sheet.paste(im,(x+(690-im.width)//2,y+25))
            draw.text((x+10,y+5),f'{name} p{start+j+1}',fill='black')
            page.close()
        path=out/(Path(name).stem+f'-{start+1:03}.jpg')
        sheet.save(path,quality=90)
    doc.close()
    print(name,'rendered')
