#!/usr/bin/env python3
"""Export the author's daily-life update and a labelled adjacency schematic."""
from pathlib import Path
from html import escape
import re
import shutil

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.graphics.shapes import Drawing, Rect, String, Line
from reportlab.graphics import renderSVG

ROOT=Path(__file__).resolve().parent
MD=ROOT/'Fiango_Life_and_Characters_Update_2026-10-30.md'
PDF=MD.with_suffix('.pdf')
SVG=ROOT/'Fiango_Neighbourhood_Adjacency_2026-10-30.svg'
PAPER=colors.HexColor('#FAF8F2');INK=colors.HexColor('#183C39');MUTED=colors.HexColor('#586863');GOLD=colors.HexColor('#BD8D42');LINE=colors.HexColor('#CDD8D0');PALE=colors.HexColor('#E8EEE7')
W,H=A4

def fonts():
    p=Path('/usr/share/fonts/truetype/dejavu')
    for n,f in [('UpdateBody','DejaVuSans.ttf'),('UpdateBold','DejaVuSans-Bold.ttf'),('UpdateTitle','DejaVuSerif-Bold.ttf')]:pdfmetrics.registerFont(TTFont(n,str(p/f)))
    pdfmetrics.registerFontFamily('UpdateBody',normal='UpdateBody',bold='UpdateBold')

def rich(s):return re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',escape(s).replace('`',''))

def schematic():
    d=Drawing(510,380)
    d.add(Rect(0,0,510,380,fillColor=PAPER,strokeColor=LINE))
    nodes={'home':(210,182,'ZINO’S COMPOUND','well / mango / shared rooms'), 'ayuk':(210,315,'AYUK','one house north'), 'noge':(42,315,'NOGE','next to Ayuk'), 'arey':(380,315,'AREY','Ayuk’s cousin'), 'bismark':(210,45,'BISMARK','south / next to TV house'), 'robi':(42,45,'ROBI','next to Bismark'), 'tv':(380,182,'TV HOUSE','adjacent to compound')}
    def link(a,b,text,tx,ty):
        ax,ay,_,_=nodes[a];bx,by,_,_=nodes[b]
        d.add(Line(ax+62,ay+22,bx+62,by+22,strokeColor=GOLD,strokeWidth=1.1))
        d.add(String(tx,ty,text,textAnchor='middle',fontName='UpdateBody',fontSize=6.5,fillColor=MUTED))
    link('home','ayuk','north',277,276)
    link('ayuk','noge','next',188,345)
    link('ayuk','arey','cousins',357,345)
    link('home','bismark','south',277,129)
    link('bismark','robi','next',188,75)
    link('home','tv','adjacent; side unknown',333,236)
    link('bismark','tv','next to TV house',390,112)
    for key,(x,y,title,desc)in nodes.items():
        d.add(Rect(x,y,124,46,rx=5,ry=5,fillColor=PALE if key!='home'else INK,strokeColor=LINE))
        colour=colors.white if key=='home'else INK
        d.add(String(x+62,y+29,title,textAnchor='middle',fontName='UpdateBold',fontSize=7.4,fillColor=colour))
        d.add(String(x+62,y+13,desc,textAnchor='middle',fontName='UpdateBody',fontSize=6.2,fillColor=colour))
    d.add(String(14,365,'RELATIONSHIPS / NOT A MEASURED FLOOR PLAN',fontName='UpdateBold',fontSize=8,fillColor=INK))
    d.add(String(14,14,'Only north/south labels are directional facts; other links show adjacency or kinship.',fontName='UpdateBody',fontSize=7,fillColor=MUTED))
    return d

def route_diagram():
    d=Drawing(510,230)
    d.add(Rect(0,0,510,230,fillColor=PAPER,strokeColor=LINE))
    items=[(10,158,130,'COMPOUND','Zino / Mother'),(185,158,130,'TARRED ROAD','taxi pickup'),(360,158,140,'AZI MOTEL','five storeys'),(360,40,140,'GREAT-AUNT','house + poultry farm')]
    for x,y,w,title,desc in items:
        d.add(Rect(x,y,w,48,rx=5,ry=5,fillColor=PALE,strokeColor=LINE))
        d.add(String(x+w/2,y+29,title,fontName='UpdateBold',fontSize=8,textAnchor='middle',fillColor=INK))
        d.add(String(x+w/2,y+12,desc,fontName='UpdateBody',fontSize=7,textAnchor='middle',fillColor=MUTED))
    for x1,y1,x2,y2 in [(140,182,185,182),(315,182,360,182),(430,158,430,88)]:d.add(Line(x1,y1,x2,y2,strokeColor=GOLD,strokeWidth=1.2))
    d.add(String(162,213,'5 houses behind',textAnchor='middle',fontName='UpdateBody',fontSize=7,fillColor=MUTED))
    d.add(String(338,213,'nearby',textAnchor='middle',fontName='UpdateBody',fontSize=7,fillColor=MUTED))
    d.add(String(440,121,'next to',fontName='UpdateBody',fontSize=7,fillColor=MUTED))
    d.add(String(14,18,'Diagram placement does not assign a compass bearing to “behind” or “nearby”.',fontName='UpdateBody',fontSize=7,fillColor=MUTED))
    return d

def chrome(c,doc):
    c.setFillColor(PAPER);c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(MUTED);c.setFont('UpdateBold',7.2);c.drawString(42,H-30,'GRAND-CHUKUCHUKU / FIANGO LIFE + CHARACTER UPDATE')
    c.setStrokeColor(LINE);c.line(42,H-39,W-42,H-39);c.line(42,42,W-42,42)
    c.setFont('UpdateBody',7);c.drawString(42,28,'AUTHOR-SUPPLIED CONTEXT / UPDATED 31 OCTOBER 2026')
    c.drawRightString(W-42,28,f'UPDATE {doc.page:02d}')

def main():
    fonts();flow=[]
    styles={k:ParagraphStyle(k,fontName=font,fontSize=size,leading=leading,textColor=colour,spaceBefore=before,spaceAfter=after,keepWithNext=k in ['title','h2','h3'])for k,font,size,leading,colour,before,after in [
        ('title','UpdateTitle',23,28,INK,0,10),('h2','UpdateBold',14,19,INK,12,8),('h3','UpdateBold',10.7,14.5,GOLD,9,5),('body','UpdateBody',9.3,13.3,INK,0,6),('small','UpdateBody',8.2,11.7,MUTED,0,5)]}
    flow += [Paragraph('Fiango: who lives where',styles['title']),Paragraph('An adjacency guide from Zino’s recollections. This diagram does not invent compass directions, addresses, room measurements or a home for Arey.',styles['body']),Spacer(1,16),schematic(),Spacer(1,15),Paragraph('Room correction: Zino’s room is two apartments away from Mother’s front room. The tenants share two bathrooms. A separate detailed compound plan needs the doorway/room arrangement and ages confirmed.',styles['body']),Paragraph('Football correction: Ayuk, Arey, Noge, Bismark and Robi play with Zino. Gideon watches and banters. Luc evangelises or chats. None of these names has been identified as a later crypto associate.',styles['body']),PageBreak()]
    flow += [Paragraph('The pickup, motel and poultry trade',styles['title']),Paragraph('The road and hotel belong to the weekday geography. This great-aunt is Mother’s aunt, not the maternal aunt later killed.',styles['body']),Spacer(1,16),route_diagram(),Spacer(1,16),Paragraph('School budget: 200 CFA = 100 taxi + 100 at school. A single morning ride costs 100; taxis are taken on three mornings a week. Walking early preserves the full 200 for school spending.',styles['body']),Paragraph('Daytime uniform: light sky-blue short sleeves; dark-blue trousers for boys, skirts for girls. Night revision: house/casual clothes for every student; some dress to impress. No student uniforms at night. Boarding uniform remains unconfirmed.',styles['body']),Paragraph('Working ages: Form One about 10–11, Two 11–12, Three 12–13, Four 13–14, Five 14–15. These author-authorized estimates do not establish exact birthdays.',styles['body']),PageBreak()]
    lines=iter(MD.read_text().splitlines())
    for raw in lines:
        line=raw.strip()
        if not line:flow.append(Spacer(1,3));continue
        if line.startswith('|'):
            rows=[line]
            for next_line in lines:
                if not next_line.strip():break
                if not next_line.strip().startswith('|'):
                    raise ValueError('Separate a Markdown table from its next paragraph with a blank line')
                rows.append(next_line.strip())
            cells=[]
            for row in rows:
                values=[v.strip() for v in row.strip('|').split('|')]
                if all(re.fullmatch(r':?-+:?',v) for v in values):continue
                cells.append([Paragraph(rich(v),styles['small'])for v in values])
            table=Table(cells,colWidths=[245,133,133],repeatRows=1,hAlign='LEFT')
            table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),PALE),('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.4,LINE),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
            flow += [table,Spacer(1,8)]
            continue
        if line.startswith('# '):flow.append(Paragraph(rich(line[2:]),styles['title']))
        elif line.startswith('## '):
            title=line[3:]
            if re.match(r'^(?:[2-9]|[1-9][0-9]+)\. ',title):flow.append(PageBreak())
            flow.append(Paragraph(rich(title),styles['h2']))
        elif line.startswith('### '):flow.append(Paragraph(rich(line[4:]),styles['h3']))
        else:flow.append(Paragraph(rich('• '+line[2:]if line.startswith('- ')else line),styles['body']))
    SimpleDocTemplate(str(PDF),pagesize=A4,leftMargin=42,rightMargin=42,topMargin=58,bottomMargin=56,title='Grand-Chukuchuku | Fiango life and characters update',author='Based on recollections of Nkeh Nkengzincho').build(flow,onFirstPage=chrome,onLaterPages=chrome)
    renderSVG.drawToFile(schematic(),str(SVG))
    renderSVG.drawToFile(route_diagram(),str(ROOT/'Fiango_Taxi_Motel_Poultry_2026-10-30.svg'))
    out=ROOT.parents[2]/'output'/'grand-chukuchuku';out.mkdir(parents=True,exist_ok=True)
    shutil.copy2(PDF,out/PDF.name)
    print(PDF);print(SVG)

if __name__=='__main__':main()
