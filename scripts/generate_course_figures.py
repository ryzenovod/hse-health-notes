"""Deterministic, accessible SVG figures for the October course notes.

Coordinates are calculated from the stated models; no source photographs are used.
"""
from pathlib import Path
from html import escape
from math import sqrt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/assets/oct-2026'
OLD = ROOT / 'docs/assets/eos-materials'
INK, MUTED, GRID = '#18213a', '#54627a', '#e0e5ee'
BLUE, ORANGE, TEAL, RED = '#3859b5', '#dd5a24', '#178477', '#b23b54'

class SVG:
    def __init__(self, title, desc, w=760, h=580):
        self.w, self.h = w, h
        self.items = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">',
                      f'<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>',
                      '<style>text{font-family:system-ui,-apple-system,Segoe UI,sans-serif;fill:#18213a;font-size:18px} .small{font-size:16px;fill:#54627a} .heading{font-size:23px;font-weight:650}</style>',
                      f'<rect width="{w}" height="{h}" rx="10" fill="#fff"/>']
        self.text(32, 38, title, cls='heading')
    def text(self, x, y, value, color=INK, anchor='start', cls='', size=None):
        size_attr = f'font-size:{size}px;' if size else ''
        self.items.append(f'<text x="{x:.2f}" y="{y:.2f}" text-anchor="{anchor}" class="{cls}" style="{size_attr}fill:{color}">{escape(str(value))}</text>')
    def line(self, x1, y1, x2, y2, color=INK, width=2, dash=False):
        self.items.append(f'<path d="M{x1:.3f},{y1:.3f} L{x2:.3f},{y2:.3f}" fill="none" stroke="{color}" stroke-width="{width}"'+(' stroke-dasharray="6 6"' if dash else '')+'/>')
    def poly(self, points, color, fill='none', width=3, opacity=1):
        coords = ' '.join(f'{x:.3f},{y:.3f}' for x,y in points)
        self.items.append(f'<polyline points="{coords}" fill="{fill}" fill-opacity="{opacity}" stroke="{color}" stroke-width="{width}" stroke-linejoin="round"/>')
    def dot(self, x, y, color=INK, r=4):
        self.items.append(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{r}" fill="{color}"/>')
    def rect(self,x,y,w,h,fill,rx=0):
        self.items.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"/>')
    def legend(self, rows, y, x=70, step=28):
        for i,(color,label) in enumerate(rows):
            self.line(x, y+i*step-5, x+28, y+i*step-5, color, 4)
            self.text(x+40,y+i*step,label,cls='small')
    def save(self, name, old=False):
        path=(OLD if old else OUT)/name
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text('\n'.join(self.items+['</svg>'])+'\n',encoding='utf-8')

class Plot:
    def __init__(self, s, xmax, ymax, x=90, y=78, w=570, h=330, xlabel='Q', ylabel='P'):
        self.s,self.xmax,self.ymax,self.x,self.y,self.w,self.h=s,xmax,ymax,x,y,w,h
        s.line(x,y+h,x+w+10,y+h)
        s.line(x,y+h,x,y-10)
        s.text(x+w+18,y+h+6,xlabel)
        s.text(x-20,y-15,ylabel)
    def point(self,q,p): return self.x+self.w*q/self.xmax,self.y+self.h*(1-p/self.ymax)
    def line(self, points,color=BLUE,width=3,dash=False):
        coords=[self.point(q,p) for q,p in points]
        if dash and len(coords)==2: self.s.line(*coords[0],*coords[1],color,width,True)
        else:self.s.poly(coords,color,width=width)
    def curve(self,fn,color=BLUE,start=0,end=None):
        end=self.xmax if end is None else end
        vals=[(start+(end-start)*i/160,fn(start+(end-start)*i/160)) for i in range(161)]
        self.line([(q,p) for q,p in vals if 0<=p<=self.ymax],color)
    def area(self,points,fill,opacity=.2):self.s.poly([self.point(q,p) for q,p in points],fill,fill,0,opacity)
    def dot(self,q,p,color=INK):self.s.dot(*self.point(q,p),color)
    def label(self,q,p,txt,color=INK,dx=8,dy=-10,anchor='start'):
        x,y=self.point(q,p);self.s.text(x+dx,y+dy,txt,color,anchor)
    def guides(self,q,p,qlabel=None,plabel=None):
        self.line([(0,p),(q,p)],MUTED,1,True)
        self.line([(q,0),(q,p)],MUTED,1,True)
        if qlabel:self.label(q,0,qlabel,dx=0,dy=26,anchor='middle')
        if plabel:self.label(0,p,plabel,dx=-12,dy=6,anchor='end')
    def ticks(self,qticks=(),pticks=()):
        for q in qticks:
            x,y=self.point(q,0);self.s.line(x,y,x,y+5);self.s.text(x,y+26,q,anchor='middle',cls='small')
        for p in pticks:
            x,y=self.point(0,p);self.s.line(x-5,y,x,y);self.s.text(x-12,y+6,p,anchor='end',cls='small')

def numerical(surplus=False):
    title='Налог 5: цены и объём рынка' if not surplus else 'Излишки и потери после налога'
    s=SVG(title,'Спрос P=150−Q/2, предложение P=200/3+Q/3. До налога P=100,Q=100; после Pd=103,Ps=98,Q=94.',h=620)
    p=Plot(s,150,160,h=325)
    if surplus:
        p.area([(0,150),(94,103),(0,103)],BLUE,.17)
        p.area([(0,200/3),(94,98),(0,98)],TEAL,.20)
        p.area([(0,98),(94,98),(94,103),(0,103)],ORANGE,.65)
        p.area([(94,98),(100,100),(94,103)],RED,.7)
    p.curve(lambda q:150-.5*q,BLUE)
    p.curve(lambda q:200/3+q/3,TEAL)
    p.curve(lambda q:200/3+q/3+5,ORANGE)
    p.guides(100,100,'100',None);p.guides(94,103,None,None)
    for q,v,c in [(100,100,INK),(94,103,ORANGE),(94,98,TEAL)]:p.dot(q,v,c)
    p.label(140,80,'D',BLUE);p.label(135,117,'S',TEAL,dy=18);p.label(135,128,'S + 5',ORANGE)
    p.ticks([0,50,150],[0,50,150]);p.label(94,0,'94',dx=-12,dy=48,anchor='end')
    if surplus:
        s.legend([(BLUE,'CS = 2 209'),(TEAL,'PS = 4 418 / 3 ≈ 1 472,67'),(ORANGE,'Бюджет: 5 × 94 = 470'),(RED,'DWL: ½ × 5 × (100 − 94) = 15')],475)
    else:
        s.text(90,481,'До налога: P = 100, Q = 100')
        s.text(90,515,'После: покупатель платит 103, продавец получает 98')
        s.text(90,549,'На единицу: покупатель несёт 3, продавец — 2')
        s.text(90,583,'Клин 5 = 103 − 98; продажи сокращаются до 94',cls='small')
    s.save('tax-numerical-surplus.svg' if surplus else 'tax-numerical-equilibrium.svg')

def generic_wedge():
    s=SVG('Налоговый клин и потери благосостояния','Линейный конкурентный рынок: D=100−Q, S=20+Q, налог20. До Q40,P60; после Q30,Pd70,Ps50. Потери100.',h=605)
    p=Plot(s,70,110)
    p.area([(0,50),(30,50),(30,70),(0,70)],ORANGE,.3)
    p.area([(30,50),(40,60),(30,70)],RED,.5)
    for f,c in [(lambda q:100-q,BLUE),(lambda q:20+q,TEAL),(lambda q:40+q,ORANGE)]:p.curve(f,c)
    p.guides(40,60,'Q₀','P₀');p.guides(30,70,'Qₜ','Pᵈ');p.guides(30,50,None,'Pˢ')
    for q,v in [(40,60),(30,70),(30,50)]:p.dot(q,v)
    p.label(64,36,'D',BLUE);p.label(65,85,'S',TEAL);p.label(53,96,'S + t',ORANGE)
    s.legend([(ORANGE,'Прямоугольник: поступления T = t × Qₜ'),(RED,'Треугольник: DWL = ½ × t × (Q₀ − Qₜ)')],480)
    s.text(70,563,'Клин: t = Pᵈ − Pˢ',cls='small')
    s.save('tax-incidence-dwl.svg',True)

def extreme(kind,compact=None):
    titles=['Спрос фиксирован','Цена спроса фиксирована','Предложение фиксировано','Цена предложения фиксирована']
    desc=['Вертикальный спрос. Налог целиком у покупателей, количество сохраняется.',
          'Горизонтальный спрос. Налог целиком у продавцов, количество сокращается.',
          'Вертикальное предложение. Налог целиком у продавцов, количество сохраняется.',
          'Горизонтальное предложение. Налог целиком у покупателей, количество сокращается.'][kind]
    s=SVG(titles[kind],desc,h=560)
    p=Plot(s,80,110,h=300)
    if kind==0:
        p.line([(40,0),(40,105)],BLUE);p.curve(lambda q:20+q,TEAL);p.curve(lambda q:40+q,ORANGE)
        p.guides(40,60,'Q₀ = Qₜ','P₀ = Pˢ');p.guides(40,80,None,'Pᵈ')
        p.dot(40,60);p.dot(40,80);p.label(40,102,'D',BLUE);p.label(68,88,'S',TEAL,dy=15);p.label(63,103,'S + t',ORANGE)
        message=['Количество сохраняется → DWL = 0','Покупатель: 100% налога; продавец: 0%']
    elif kind==1:
        p.line([(0,60),(80,60)],BLUE);p.curve(lambda q:20+q,TEAL);p.curve(lambda q:40+q,ORANGE)
        p.area([(20,40),(40,60),(20,60)],RED,.25)
        p.guides(40,60,'Q₀','P₀ = Pᵈ');p.guides(20,40,'Qₜ','Pˢ');p.dot(20,60);p.dot(20,40);p.dot(40,60)
        p.label(72,60,'D',BLUE);p.label(65,85,'S',TEAL,dy=12);p.label(63,103,'S + t',ORANGE)
        message=['Количество сокращается → DWL > 0','Покупатель: 0%; продавец: 100% налога']
    elif kind==2:
        p.line([(40,0),(40,105)],TEAL);p.curve(lambda q:100-q,BLUE)
        p.guides(40,60,'Q₀ = Qₜ','P₀ = Pᵈ');p.guides(40,40,None,'Pˢ');p.dot(40,60);p.dot(40,40)
        p.label(40,102,'S',TEAL);p.label(68,32,'D',BLUE)
        message=['Количество сохраняется → DWL = 0','Покупатель: 0%; продавец: 100% налога']
    else:
        p.line([(0,40),(80,40)],TEAL);p.line([(0,60),(80,60)],ORANGE);p.curve(lambda q:100-q,BLUE)
        p.area([(40,40),(60,40),(40,60)],RED,.25)
        p.guides(60,40,'Q₀','P₀ = Pˢ');p.guides(40,60,'Qₜ','Pᵈ');p.dot(40,60);p.dot(60,40)
        p.label(72,40,'S',TEAL,dy=24);p.label(72,60,'S + t',ORANGE);p.label(68,32,'D',BLUE)
        message=['Количество сокращается → DWL > 0','Покупатель: 100% налога; продавец: 0%']
    for i,m in enumerate(message):s.text(70,470+32*i,m)
    s.text(70,539,'Стандартная конкурентная модель с поштучным налогом',cls='small')
    names=['tax-extreme-demand-fixed.svg','tax-extreme-demand-flat.svg','tax-extreme-supply-fixed.svg','tax-extreme-supply-flat.svg']
    s.save(names[kind]);return s

def combined_extremes():
    # Stack the four full-width models so axis labels remain readable on phones.
    svg=SVG('Четыре предельных случая эластичности','Вертикальный спрос и предложение дают нулевые потери объёма; горизонтальные кривые дают сокращение торговли.',h=2185)
    for k in range(4):
        part=extreme(k)
        svg.items.append(f'<g transform="translate(0,{65+k*525})">')
        svg.items.extend(part.items[4:])
        svg.items.append('</g>')
    svg.save('tax-incidence-elasticity-extremes.svg',True)

def rates():
    s=SVG('Средняя и предельная ставки','Доходы2,4,6,8,10; налог1.14,2.41,3.95,5.28,6.84. Средние57,60.25,65.8333,66,68.4%; предельные по интервалам63.5,77,66.5,78%.',h=570)
    p=Plot(s,11,85,ylabel='%',xlabel='w')
    wages=[2,4,6,8,10];taxes=[1.14,2.41,3.95,5.28,6.84]
    atr=[100*t/w for t,w in zip(taxes,wages)]
    p.line(list(zip(wages,atr)),BLUE)
    for w,a in zip(wages,atr):p.dot(w,a,BLUE)
    for i in range(4):
        m=100*(taxes[i+1]-taxes[i])/(wages[i+1]-wages[i]);p.line([(wages[i],m),(wages[i+1],m)],ORANGE)
    p.ticks(wages,[0,20,40,60,80])
    s.legend([(BLUE,'ATR = T(w) / w: ставка на весь доход'),(ORANGE,'MTR = ΔT / Δw: ставка на прирост дохода')],482)
    s.save('tax-rates.svg')

def sacrifice():
    s=SVG('Налоги и критерий Роулза','Общий налог6. UA=5−TA/2, UB=2+TA. Максимум минимальной полезности при TA2,TB4; обе полезности4.',h=610)
    p=Plot(s,6,8,xlabel='Tₐ',ylabel='U')
    p.line([(0,5),(6,2)],BLUE);p.line([(0,2),(6,8)],TEAL)
    p.line([(0,2),(2,4),(6,2)],ORANGE,6)
    p.guides(2,4,'2','4');p.dot(2,4,ORANGE)
    p.guides(4,3,'4',None);p.dot(4,3,BLUE);p.dot(4,6,TEAL)
    p.ticks([0,6],[0,2,6,8]);p.label(5.3,7.3,'Uᵦ',TEAL);p.label(5.3,2.35,'Uₐ',BLUE,dy=24)
    s.legend([(ORANGE,'min(Uₐ, Uᵦ): максимум 4 при Tₐ = 2'),(BLUE,'Равная абсолютная жертва: Tₐ = 4, Tᵦ = 2')],490)
    s.text(70,572,'При равной жертве: Uₐ = 3, Uᵦ = 6',cls='small')
    s.save('tax-sacrifice.svg')

def labor(fixed):
    s=SVG('Налог при фиксированном предложении труда' if fixed else 'Налог при эластичном предложении труда',
          'Спрос L=34−2w. Налог составляет треть брутто-зарплаты. При фиксированном L22 gross6/net4; при эластичном предложении занятость сокращается, gross растёт, net снижается.',h=600)
    p=Plot(s,34,18,xlabel='L',ylabel='w')
    p.curve(lambda l:17-.5*l,BLUE)
    p.curve(lambda l:(2/3)*(17-.5*l),ORANGE)
    if fixed:
        p.line([(22,0),(22,18)],TEAL);p.guides(22,6,'22','6');p.guides(22,4,None,'4');p.dot(22,6);p.dot(22,4)
        p.label(22,17,'S',TEAL)
    else:
        p.curve(lambda l:.5+.25*l,TEAL)
        l=130/7;gross=54/7;net=36/7
        p.guides(22,6,'L₀','w₀');p.guides(l,gross,None,'wᵍ');p.guides(l,net,None,'wⁿ')
        p.label(l,0,'Lₜ',dx=-6,dy=46,anchor='end');p.dot(22,6);p.dot(l,gross);p.dot(l,net)
        p.label(29,7.75,'S',TEAL,dy=23)
    p.label(7,13.5,'D: брутто',BLUE);p.label(4,10,'D: нетто',ORANGE,dy=18)
    s.text(70,489,'wⁿ = (1 − ⅓) × wᵍ = ⅔wᵍ')
    s.text(70,523,'Налог на работника: wᵍ − wⁿ = ⅓wᵍ')
    s.text(70,559,'L = 22; wᵍ = 6; wⁿ = 4; налог = 2' if fixed else 'Lₜ < L₀; wᵍ > w₀; wⁿ < w₀',cls='small')
    s.save('labor-tax-fixed.svg' if fixed else 'labor-tax-elastic.svg')

def vodka():
    s=SVG('Один налог при разной эластичности спроса','Одинаковые исходные P80,Q60 и S=20+Q. Водка D=200−2Q, шоколад D=110−Q/2. Налог20: доля покупателя2/3 против1/3; потери66.67 против133.33.',h=1060)
    for k in range(2):
        b=2 if k==0 else .5;a=200 if k==0 else 110
        q=(a-40)/(b+1);pd=a-b*q;ps=20+q
        y=95+k*480
        s.text(90,y-20,'Водка: менее эластичный спрос' if k==0 else 'Шоколад: более эластичный спрос',size=20)
        p=Plot(s,100,150,y=y,h=280)
        p.area([(q,ps),(60,80),(q,pd)],RED,.28)
        p.curve(lambda v:a-b*v,BLUE);p.curve(lambda v:20+v,TEAL);p.curve(lambda v:40+v,ORANGE)
        p.guides(60,80,'60','80');p.guides(q,pd,None,'Pᵈ');p.guides(q,ps,None,'Pˢ')
        p.label(q,0,'Qₜ',dx=-8,dy=46,anchor='end')
        for v,z in [(60,80),(q,pd),(q,ps)]:p.dot(v,z)
        p.label(83,min(140,20+83),'S',TEAL,dy=20);p.label(85,125,'S + 20',ORANGE)
        s.text(90,y+355,'Покупатель: ⅔; продавец: ⅓; DWL = 66⅔' if k==0 else 'Покупатель: ⅓; продавец: ⅔; DWL = 133⅓')
        s.text(90,y+388,'Цена покупателя 93⅓; цена продавца 73⅓' if k==0 else 'Цена покупателя 86⅔; цена продавца 66⅔',cls='small')
    s.save('tax-incidence-vodka-chocolate.svg',True)

def specific_advalorem():
    s=SVG('Поштучный и стоимостной налог','Предложение без налога Ps=2+Q/5. Поштучный налог2 даёт Pd=4+Q/5. Стоимостной налог25% от нетто-цены даёт Pd=2.5+Q/4.',h=625)
    p=Plot(s,35,13)
    p.curve(lambda q:2+.2*q,TEAL);p.curve(lambda q:4+.2*q,ORANGE);p.curve(lambda q:1.25*(2+.2*q),BLUE)
    p.ticks([0,10,20,30],[0,2,4,6,8,10,12])
    p.label(26,7.2,'S',TEAL,dy=23);p.label(26,9.2,'S + 2',ORANGE);p.label(26,10.25,'1,25S',BLUE)
    s.legend([(TEAL,'Нетто-цена предложения: Pˢ = 2 + Q/5'),(ORANGE,'Поштучный: Pᵈ = Pˢ + 2'),(BLUE,'25% от нетто-цены: Pᵈ = 1,25Pˢ')],485)
    s.text(70,589,'При ненулевом пересечении меняются наклон и интерсепт',cls='small')
    s.save('tax-specific-vs-advalorem.svg',True)

def budget():
    s=SVG('Бюджет интеграции: 30 млн ₽','Обучение и развитие12млн, мотивация и адаптация10млн, условия труда5млн, приёмное отделение3млн.',h=475)
    rows=[('Обучение и развитие',12,BLUE),('Мотивация и адаптация',10,TEAL),('Условия труда',5,ORANGE),('Приёмное отделение',3,RED)]
    for i,(name,value,color) in enumerate(rows):
        y=105+i*83;s.text(35,y,name);s.rect(35,y+12,value/12*480,25,color,4)
        s.text(550,y+34,f'{value} млн · {value/30*100:.1f}%'.replace('.',','))
    s.text(35,454,'Распределение средств из разбора кейса',cls='small');s.save('integration-budget.svg')

def governance():
    s=SVG('Управление сетью из 11 клиник','Учредители определяют стратегию и инвестиции; функциональные директора отвечают за операции, качество и финансы; главные врачи принимают решения в пределах бюджета.',h=700)
    def box(y,title,lines,color):
        s.rect(65,y,630,120,'#f1f4fa',8);s.rect(65,y,6,120,color)
        s.text(88,y+32,title,size=21)
        for i,line in enumerate(lines):s.text(88,y+63+i*26,line,cls='small')
    box(75,'Учредители',['Стратегия · инвестиции · бренд','Утверждение бюджета и решений за его пределами'],BLUE)
    box(275,'Функциональные директора',['Операции · медицинское качество · финансы','Общие стандарты, ресурсы и показатели сети'],TEAL)
    box(475,'Главные врачи 11 филиалов',['Текущая работа и команда клиники','Самостоятельные решения в рамках полномочий'],ORANGE)
    for y in [195,395]:
        s.line(380,y,380,y+75,MUTED);s.poly([(372,y+65),(380,y+75),(388,y+65)],MUTED,width=2)
        s.text(410,y+44,'Цели, лимиты, поддержка',cls='small')
    s.text(65,650,'Обратная связь: результаты, отклонения и вопросы для эскалации',cls='small')
    s.save('clinic-governance.svg')

def bayes():
    s=SVG('Положительный тест и распространённость','Чувствительность и специфичность95%,10000 обследованных. При распространённости1%:95 истинных и495 ложных положительных;10%:950 и450;50%:4750 и250.',h=555)
    rows=[(1,95,495),(10,950,450),(50,4750,250)]
    for i,(prevalence,tp,fp) in enumerate(rows):
        y=105+i*128;ppv=tp/(tp+fp);s.text(35,y,f'Распространённость {prevalence}% · PPV {ppv*100:.1f}%'.replace('.',','))
        s.rect(35,y+18,660*ppv,32,TEAL);s.rect(35+660*ppv,y+18,660*(1-ppv),32,ORANGE)
        s.text(35,y+78,f'Истинно положительные: {tp}; ложноположительные: {fp}',cls='small')
    s.legend([(TEAL,'Болезнь есть среди положительных результатов'),(ORANGE,'Болезни нет среди положительных результатов')],494,x=35)
    s.save('diagnostic-bayes.svg')

def roc():
    s=SVG('ROC: выбор порога теста','Учебная кривая Se=sqrt(1−Sp). Точки(.04,.20),(.16,.40),(.64,.80) показывают рост чувствительности при росте ложноположительной доли.',h=575)
    p=Plot(s,1,1,xlabel='1 − Sp',ylabel='Se',w=510,h=325)
    p.line([(0,0),(1,1)],MUTED,1,True);p.curve(sqrt,BLUE)
    for x,y,label in [(.04,.2,'Строгий'),(.16,.4,'Средний'),(.64,.8,'Мягкий')]:p.dot(x,y);p.label(x,y,label,dx=12,dy=10)
    p.ticks([0,.2,.4,.6,.8,1],[0,.2,.4,.6,.8,1])
    s.text(90,486,'Порог мягче → Se выше, ложноположительных больше')
    s.text(90,524,'Учебная зависимость: Se = √(1 − Sp)',cls='small');s.save('diagnostic-roc.svg')

def leadtime():
    s=SVG('Смещение времени опережения','Болезнь начинается в50лет, скрининг обнаруживает в55, симптомы приводят к диагнозу в60; смерть в70 в обоих сценариях. Наблюдаемая выживаемость15 и10лет.',h=505)
    x=lambda age:100+(age-50)*26
    for y,name,diagnosis in [(170,'Диагноз по симптомам',60),(340,'Диагноз при скрининге',55)]:
        s.text(35,y-73,name,size=21);s.line(x(50),y,x(70),y,MUTED,2)
        s.line(x(diagnosis),y,x(70),y,TEAL,7)
        for age,label in [(50,'Начало'),(diagnosis,'Диагноз'),(70,'Смерть')]:
            s.dot(x(age),y);s.text(x(age),y+29,str(age),anchor='middle');s.text(x(age),y+57,label,anchor='middle',cls='small')
        s.text((x(diagnosis)+x(70))/2,y-24,f'{70-diagnosis} лет',TEAL,anchor='middle')
    s.text(35,469,'Одинаковый возраст смерти; разное время отсчёта выживаемости',cls='small');s.save('screening-lead-time.svg')

def externality():
    s=SVG('Внешний ущерб и налог Пигу','MB=100−Q,MPC=20+Q,MEC20,MSC=40+Q. РынокQ40,P60, общественный оптимумQ30; налог20 реализует его, исходная потеря100.',h=620)
    p=Plot(s,70,110)
    p.area([(30,70),(40,80),(40,60)],RED,.30)
    p.curve(lambda q:100-q,BLUE);p.curve(lambda q:20+q,TEAL);p.curve(lambda q:40+q,ORANGE)
    p.guides(40,60,'40','60');p.guides(30,70,'30','70');p.guides(30,50,None,'50')
    for q,z in [(40,60),(30,70),(30,50)]:p.dot(q,z)
    p.label(65,35,'MB',BLUE);p.label(61,81,'MPC',TEAL,dy=18);p.label(52,92,'MSC',ORANGE)
    s.text(70,491,'Избыточное производство: 40 − 30 = 10')
    s.text(70,525,'Исходная потеря: ½ × 10 × 20 = 100')
    s.text(70,559,'Корректирующий налог t = MEC = 20 реализует Q = 30')
    s.text(70,593,'Цена покупателя 70; продавец получает 50',cls='small');s.save('eos-externalities.svg')

def lorenz():
    s=SVG('Кривая Лоренца и коэффициент Джини','Пять равных групп имеют доходы10,20,30,40,100,внутри групп доходы одинаковы. Накопленные доли5,15,30,50,100%. Площадь под кривой.30, Джини.40.',h=810)
    s.items.append('<style>text{font-size:22px}.small{font-size:20px}</style>')
    # Equal physical scales keep the equality diagonal at 45 degrees.
    p=Plot(s,100,100,x=130,y=105,w=500,h=500,xlabel='',ylabel='')
    s.text(130,80,'Доля дохода, %')
    points=[(0,0),(20,5),(40,15),(60,30),(80,50),(100,100)]
    p.area([(0,0),(100,100)]+list(reversed(points)),ORANGE,.15)
    p.line([(0,0),(100,100)],MUTED,2);p.line(points,BLUE)
    for x,y in points:p.dot(x,y,BLUE)
    p.ticks([0,20,40,60,80,100],[0,20,40,60,80,100])
    s.text(380,662,'Доля населения, %',anchor='middle')
    s.legend([(BLUE,'Лоренц: накопленная доля дохода'),(MUTED,'Диагональ равенства')],708,step=32)
    s.text(90,785,'G = 1 − 2 × 0,30 = 0,40');s.save('eos-lorenz-gini.svg')

def trap():
    s=SVG('Резкое и постепенное снятие пособия','Учебная налоговая ставка13%,пособие12тыс. При резком снятии после заработка20 доход падает с29.4 до18.27 при заработке21. Постепенное сокращение на30% даёт предельную нагрузку43%.',h=610)
    p=Plot(s,50,48,xlabel='E',ylabel='D')
    p.line([(0,12),(20,29.4)],ORANGE)
    p.line([(20,17.4),(50,43.5)],ORANGE)
    p.line([(20,17.4),(20,29.4)],ORANGE,1,True)
    p.line([(0,12),(40,34.8),(50,43.5)],TEAL)
    p.dot(20,29.4,ORANGE);p.dot(21,18.27,ORANGE)
    p.ticks([0,10,20,30,40,50],[0,10,20,30,40])
    s.legend([(ORANGE,'Резкое снятие 12 тыс. при E > 20 тыс.'),(TEAL,'Плавное снятие: пособие = max(0; 12 − 0,30E)')],488)
    s.text(70,565,'E: заработок; D: располагаемый доход; тыс. денежных единиц',cls='small')
    s.text(70,594,'Налог 13% — параметр учебной модели',cls='small');s.save('eos-poverty-trap.svg')

def lindahl():
    s=SVG('Равновесие Линдаля','Индивидуальные предельные выгодыMB1=60−Q,MB2=40−Q. Их вертикальная сумма100−2Q равнаMC40 приQ30. Персональные цены30 и10 суммируются до40.',h=620)
    p=Plot(s,48,110)
    p.curve(lambda q:60-q,BLUE);p.curve(lambda q:40-q,TEAL,end=40);p.curve(lambda q:100-2*q,ORANGE)
    p.line([(0,40),(48,40)],MUTED,2)
    p.guides(30,40,'Q* = 30',None);p.dot(30,40,ORANGE);p.dot(30,30,BLUE);p.dot(30,10,TEAL)
    p.label(30,30,'p₁ = 30',BLUE);p.label(30,10,'p₂ = 10',TEAL)
    p.label(46,40,'MC',MUTED);p.label(7,86,'MB₁ + MB₂',ORANGE)
    s.legend([(BLUE,'Индивидуальная предельная выгода первого участника'),(TEAL,'Индивидуальная предельная выгода второго участника'),(ORANGE,'Общественная выгода: вертикальная сумма')],489)
    s.text(70,600,'Одно количество общественного блага, разные доли оплаты',cls='small');s.save('welfare-lindahl.svg',True)

def deduction():
    s=SVG('Вычет на медицинские расходы','При полном использовании вычета с коэффициентом τ пациент оплачивает (1−τ)Ps. В координатах цены поставщика спрос D(Q)/(1−τ) выше исходного. Услуг больше, цена поставщика выше, расходы пациента на единицу ниже.',h=620)
    p=Plot(s,80,140,ylabel='Pˢ')
    p.curve(lambda q:100-q,BLUE);p.curve(lambda q:(100-q)/.8,ORANGE);p.curve(lambda q:20+q,TEAL)
    q=140/3;ps=200/3;net=160/3
    p.guides(40,60,'Q₀','P₀');p.guides(q,ps,None,None);p.guides(q,net,None,None)
    p.label(q,0,'Qₗ',dx=4,dy=46,anchor='middle');p.dot(40,60);p.dot(q,ps);p.dot(q,net)
    p.label(67,33,'D',BLUE);p.label(62,47.5,'Dₗ',ORANGE);p.label(67,87,'S',TEAL)
    s.legend([(BLUE,'Исходный спрос: готовность платить за услугу'),(ORANGE,'Спрос с вычетом: Dₗ(Q) = D(Q) / (1 − τ)'),(TEAL,'Предложение услуг: цена поставщика')],485)
    s.text(70,594,'Pˢₗ > P₀; (1 − τ)Pˢₗ < P₀; Qₗ > Q₀',cls='small')
    s.save('medical-tax-deduction.svg')

if __name__=='__main__':
    numerical();numerical(True);generic_wedge();combined_extremes();rates();sacrifice()
    labor(True);labor(False);vodka();specific_advalorem();budget();governance()
    bayes();roc();leadtime();externality();lorenz();trap();lindahl();deduction()
    print('Generated',len(list(OUT.glob('*.svg'))),'new and 5 replacement SVG figures.')
