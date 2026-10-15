#!/usr/bin/env python3
"""Draw original conceptual research diagrams (not simulation results).

Requires Pillow. Run from any directory to regenerate the four featured PNGs.
"""
from math import cos, sin, pi, exp, hypot
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
S = 2
BLUE, TEAL, COPPER, INK = '#345580', '#598782', '#AE7456', '#304353'


def font(size):
    for path in ('/System/Library/Fonts/Supplemental/Arial.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'):
        if Path(path).exists():
            return ImageFont.truetype(path, size * S)
    return ImageFont.load_default(size=size * S)


class Figure:
    def __init__(self, number, label):
        self.im = Image.new('RGB', (1200 * S, 675 * S), '#EFEEE7')
        self.d = ImageDraw.Draw(self.im)
        self.text(54, 40, number, 22, COPPER)
        self.text(104, 40, label.upper(), 22, BLUE)
        self.line([(54, 85), (1146, 85)], '#D8DAD2', 1)
        self.text(54, 621, 'CONCEPTUAL ILLUSTRATION', 14, '#77817B')

    def line(self, points, color=BLUE, width=2):
        self.d.line([(round(x*S), round(y*S)) for x,y in points], fill=color, width=round(width*S), joint='curve')

    def circle(self, x, y, r, color, outline=None, width=1):
        self.d.ellipse(((x-r)*S,(y-r)*S,(x+r)*S,(y+r)*S),fill=color,outline=outline,width=width*S)

    def text(self,x,y,text,size=24,color=INK):
        if size in (20, 22) and y > 100:
            size = 26
        self.d.text((x*S,y*S),text,font=font(size),fill=color)

    def arrow(self,a,b,color=BLUE,width=3):
        self.line([a,b],color,width)
        dx,dy=b[0]-a[0],b[1]-a[1]
        length=hypot(dx,dy)
        ux,uy=dx/length,dy/length
        self.line([(b[0]-ux*14-uy*7,b[1]-uy*14+ux*7),b,(b[0]-ux*14+uy*7,b[1]-uy*14-ux*7)],color,width)

    def save(self,slug):
        self.im.resize((1200,675),Image.Resampling.LANCZOS).save(ROOT/'content/research'/slug/'featured.png',optimize=True)


def multipoles():
    f=Figure('01','Polarizable electrostatics')
    centers=[(410,255,BLUE),(725,310,COPPER),(555,460,TEAL)]
    for x,y,c in centers:
        for r in (45,70,100,135):
            pts=[(x+r*cos(t*2*pi/180),y+.67*r*sin(t*2*pi/180)) for t in range(181)]
            f.line(pts,c,1.6)
    for a,b in ((0,1),(0,2),(1,2)):
        f.line([centers[a][:2],centers[b][:2]],'#AAB5B4',6)
    for x,y,c in centers:
        f.circle(x,y,23,c)
        f.circle(x-7,y-8,6,'#FFFFFF')
        # Dipoles are located at the atomic sites. Drawing from the center
        # keeps the visible shaft continuous with the atom's circular edge.
        f.arrow((x,y),(x+100,y-70),c)
    f.text(800,187,'Induced dipoles',22)
    f.text(735,495,'Gaussian charge clouds',22)
    f.line([(170+i*1.6,540-105*exp(-((i-85)/30)**2)) for i in range(170)],BLUE,3)
    f.line([(170,540),(440,540)],'#AAB5B4',1)
    f.text(170,565,'Density profile',22)
    f.save('polarizable-gaussian-multipole')


def surfaces():
    f=Figure('02','Learning molecular surfaces')
    for j in range(13):
        v=-pi/2+.1+j*(pi-.2)/12
        pts=[]
        for i in range(121):
            u=i*2*pi/120
            r=1+.13*sin(3*u+v)+.10*cos(4*v-2*u)
            x=410+215*r*cos(v)*cos(u)
            y=335+175*r*sin(v)+50*cos(v)*sin(u)
            pts.append((x,y))
        f.line(pts,TEAL,2)
    for j in range(16):
        u=j*2*pi/16
        pts=[]
        for i in range(61):
            v=-pi/2+i*pi/60
            r=1+.13*sin(3*u+v)+.10*cos(4*v-2*u)
            pts.append((410+215*r*cos(v)*cos(u),335+175*r*sin(v)+50*cos(v)*sin(u)))
        f.line(pts,BLUE,1.5)
    f.arrow((665,335),(760,335),BLUE)
    layers=[[(810,245),(810,335),(810,425)],[(915,210),(915,290),(915,370),(915,450)],[(1020,275),(1020,395)]]
    for left,right in zip(layers,layers[1:]):
        for a in left:
            for b in right:
                f.line([a,b],'#A9BAB8',1.6)
    for layer in layers:
        for x,y in layer:
            f.circle(x,y,12,BLUE)
    f.text(255,565,'Molecular geometry',22)
    f.text(800,565,'Learned representation',22)
    f.save('ml-implicit-solvent')


def binding():
    f=Figure('03','Binding free energies')
    # The same receptor and ligand appear in both states. A visible gap
    # distinguishes a free ligand from a ligand occupying the pocket.
    for receptor_x, ligand_x in ((300, 520), (880, 880)):
        angles=[.65+i*(2*pi-1.3)/200 for i in range(201)]
        pocket=[(receptor_x+130*cos(t),305+90*sin(t)) for t in angles]
        f.line(pocket,TEAL,18)
        if receptor_x == ligand_x:
            # Short dashed contacts indicate noncovalent binding without
            # changing the receptor/ligand identity or drawing a new bond.
            for start,end in ((228,259),(352,383)):
                for y in range(start,end,12):
                    f.line([(ligand_x,y),(ligand_x,min(y+6,end))],'#AAB5B4',2)
        ligand=[(ligand_x+40*cos(pi/6+i*pi/3),305+40*sin(pi/6+i*pi/3)) for i in range(7)]
        f.line(ligand,COPPER,5)
    f.arrow((625,305),(720,305),BLUE)
    f.text(290,450,'Unbound',20)
    f.text(835,450,'Bound',20)
    f.save('binding-free-energy')


def allostery():
    f=Figure('04','Allosteric communication')
    for offset,c,phase in ((0,BLUE,0),(545,TEAL,.8)):
        # Stylized protein ribbons: a conceptual conformational change.
        for band in range(3):
            pts=[]
            for i in range(251):
                t=i/250*5*pi
                pts.append((205+offset+band*57+38*sin(t+phase),185+i*1.05+16*cos(t)))
            f.line(pts,c,8)
        f.circle(240+offset,180,21,COPPER)
        f.circle(335+offset,460,21,c)
        for i in range(7):
            x=245+offset+i*14
            y=215+i*33
            f.circle(x,y,5,COPPER)
    f.arrow((515,330),(665,330),BLUE)
    f.text(498,365,'Dynamics',20)
    f.text(175,525,'Local perturbation',22)
    f.text(720,525,'Distant response',22)
    f.save('allostery')


if __name__=='__main__':
    multipoles()
    surfaces()
    binding()
    allostery()
