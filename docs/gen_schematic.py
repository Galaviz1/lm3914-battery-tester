#!/usr/bin/env python3
"""schematic.svg for the LM3914 Li-ion battery tester. Clean zoned layout."""
W, H = 1340, 860
S=[]
def e(x): S.append(x)
def line(x1,y1,x2,y2,c="#222",w=2):
    e(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{c}" stroke-width="{w}"/>')
def rect(x,y,w,h,fill="none",stroke="#222",sw=2,rx=0):
    e(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" rx="{rx}"/>')
def txt(x,y,s,size=15,c="#111",anchor="middle",weight="normal"):
    e(f'<text x="{x:.0f}" y="{y:.0f}" font-family="Helvetica,Arial,sans-serif" font-size="{size}" fill="{c}" text-anchor="{anchor}" font-weight="{weight}">{s}</text>')
def dot(x,y,r=4,c="#111"): e(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{c}"/>')
def resV(xc,yc,label,side="right",h=56,w=18):
    rect(xc-w/2,yc-h/2,w,h,fill="#fff")
    if side=="right": txt(xc+w/2+8,yc+5,label,13,anchor="start")
    else: txt(xc-w/2-8,yc+5,label,13,anchor="end")
def capV(xc,yc,label,c="#555"):
    line(xc-13,yc-4,xc+13,yc-4,c,3); line(xc-13,yc+4,xc+13,yc+4,c,3)
    txt(xc+19,yc+4,label,10,"#777",anchor="start")
def trim(xc,yt,label,setv):
    rect(xc-15,yt,30,70,fill="#f3e8ff",stroke="#8e44ad",rx=3)
    txt(xc,yt-8,label,11,"#8e44ad")
    wy=yt+35
    e(f'<path d="M {xc-15} {wy-7} L {xc-3} {wy} L {xc-15} {wy+7} Z" fill="#8e44ad"/>')
    txt(xc,yt+88,setv,10,"#8e44ad")
    return wy  # wiper exits LEFT

e(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
rect(0,0,W,H,fill="#fbfbf8",stroke="none")
txt(W/2,40,"TP4056 Charger + LM3914 Level Indicator — Schematic",23,"#111",weight="bold")
txt(W/2,64,"USB 5 V charges the 18650 via TP4056; LM3914 reads the cell → 10-segment bar (bar mode)",14,"#555")
VP,GND=100,800
line(60,VP,W-60,VP,"#c0392b",3); txt(70,VP-8,"+5 V (USB)",14,"#c0392b",anchor="start",weight="bold")
line(60,GND,W-60,GND,"#2c3e50",3); txt(70,GND+22,"GND",14,"#2c3e50",anchor="start",weight="bold")

# ---------- chip ----------
CX,CY,CW,CH=620,150,210,560
rect(CX,CY,CW,CH,fill="#eef2f7",rx=10)
txt(CX+CW/2,CY+28,"LM3914",20,"#111",weight="bold"); txt(CX+CW/2,CY+46,"DIP-18",11,"#777")
e(f'<path d="M {CX+CW/2-12} {CY} a12 12 0 0 0 24 0" fill="#fbfbf8" stroke="#222" stroke-width="2"/>')
left=[1,2,3,4,5,6,7,8,9]; right=[18,17,16,15,14,13,12,11,10]
names={1:"LED1",2:"V-",3:"V+",4:"RLO",5:"SIG",6:"RHI",7:"REFO",8:"REFA",9:"MODE",10:"LED10",11:"LED9",12:"LED8",13:"LED7",14:"LED6",15:"LED5",16:"LED4",17:"LED3",18:"LED2"}
p={}; top=CY+78; bot=CY+CH-24
for i,pin in enumerate(left):
    y=top+(bot-top)*i/8; line(CX-24,y,CX,y); dot(CX-24,y,3)
    txt(CX+10,y+5,str(pin),12,"#444",anchor="start"); txt(CX+32,y+5,names[pin],11,"#888",anchor="start"); p[pin]=(CX-24,y)
for i,pin in enumerate(right):
    y=top+(bot-top)*i/8; line(CX+CW,y,CX+CW+24,y); dot(CX+CW+24,y,3)
    txt(CX+CW-10,y+5,str(pin),12,"#444",anchor="end"); txt(CX+CW-32,y+5,names[pin],11,"#888",anchor="end"); p[pin]=(CX+CW+24,y)

# ---------- power ----------
x3,y3=p[3]; line(x3,y3,x3-30,y3); line(x3-30,y3,x3-30,VP,"#c0392b"); dot(x3-30,VP)
x2,y2=p[2]; line(x2,y2,x2-14,y2); line(x2-14,y2,x2-14,GND,"#2c3e50"); dot(x2-14,GND)
x9,y9=p[9]; line(x9,y9,x9-46,y9); line(x9-46,y9,x9-46,VP,"#c0392b"); dot(x9-46,VP); txt(x9-46,y9+18,"MODE→V+ (bar)",10,"#c0392b")
# bypass caps zone (far left, x=250)
BPx=250; line(BPx,VP,BPx,VP+34,"#c0392b"); dot(BPx,VP); capV(BPx,VP+46,"2.2–10 µF"); line(BPx,VP+58,BPx,VP+84); capV(BPx,VP+96,"0.1 µF"); line(BPx,VP+108,BPx,GND,"#2c3e50"); dot(BPx,GND)

# ---------- TP4056 charger -> 18650 -> divider -> SIG ----------
x5,y5=p[5]
GLx=56                                   # left GND bus
# TP4056 module
TPx,TPy,TPw,TPh=74,132,152,84
rect(TPx,TPy,TPw,TPh,fill="#e8f6ef",stroke="#1e8449",rx=8)
txt(TPx+TPw/2,TPy+26,"TP4056",15,"#1e8449",weight="bold")
txt(TPx+TPw/2,TPy+44,"Li-ion charger",10,"#1e8449")
txt(TPx+TPw/2,TPy+64,"CHRG · STDBY LEDs onboard",8,"#777")
# IN+ -> +5V rail (USB) ; IN- -> GND bus
line(TPx+28,TPy,TPx+28,VP,"#c0392b"); dot(TPx+28,VP); txt(TPx+32,TPy-6,"IN+",9,"#c0392b",anchor="start")
line(TPx,TPy+22,GLx,TPy+22,"#2c7fb8"); txt(TPx-2,TPy+18,"IN–",9,"#2c7fb8",anchor="end")
line(GLx,TPy+22,GLx,GND,"#2c7fb8"); dot(GLx,GND)
# BAT+ (bottom) -> cell+ ; BAT- -> GND bus
batpx=TPx+TPw-34
line(batpx,TPy+TPh,batpx,TPy+TPh+26,"#c0392b"); txt(batpx+4,TPy+TPh+16,"BAT+",9,"#c0392b",anchor="start")
line(TPx+40,TPy+TPh,TPx+40,TPy+TPh+12,"#2c7fb8"); line(TPx+40,TPy+TPh+12,GLx,TPy+TPh+12,"#2c7fb8"); txt(TPx+36,TPy+TPh+10,"BAT–",9,"#2c7fb8",anchor="end")
# 18650 cell (battery symbol)
cy0=TPy+TPh+26
line(batpx-22,cy0,batpx+22,cy0,"#111",3)        # + plate (long)
line(batpx-13,cy0+13,batpx+13,cy0+13,"#111",6)  # - plate (short/thick)
txt(batpx+28,cy0+8,"18650",10,"#9a7b00",anchor="start")
line(batpx,cy0+13,batpx,cy0+40,"#2c7fb8"); line(batpx,cy0+40,GLx,cy0+40,"#2c7fb8")  # cell- -> GND
# cell+ node -> ÷3.4 divider -> SIG
DVx=330; By=y5; Cy=y5+130
line(batpx,cy0,DVx,cy0,"#c0392b"); dot(batpx,cy0,3,"#c0392b")   # cell+/BAT+ to divider top
resV(DVx,(cy0+By)/2,"24 kΩ"); line(DVx,cy0,DVx,(cy0+By)/2-28); line(DVx,(cy0+By)/2+28,DVx,By)
dot(DVx,By); line(DVx,By,x5,By)                                 # SIG tap -> pin5
resV(DVx,(By+Cy)/2,"10 kΩ"); line(DVx,By,DVx,(By+Cy)/2-28); line(DVx,(By+Cy)/2+28,DVx,Cy)
line(DVx,Cy,DVx,GND,"#2c7fb8"); dot(DVx,GND)
capV(DVx+58,By+34,"100 nF"); dot(DVx,By); line(DVx,By,DVx+58,By); line(DVx+58,By,DVx+58,By+22); line(DVx+58,By+46,DVx+58,GND,"#999")
txt(DVx+4,cy0-14,"÷3.4 divider (reads cell)",11,"#9a7b00",weight="bold",anchor="start"); txt(DVx+4,cy0+1,"4.2V→1.24V · 3.0V→0.88V",9,"#9a7b00",anchor="start")

# ---------- reference network (trimpots in open area below chip) ----------
# R_prog on REF ADJ (pin 8)
x8,y8=p[8]; line(x8,y8,x8+0,y8); line(x8,y8,x8-26,y8); resV(x8-26,y8+34,"1.2 kΩ","left"); line(x8-26,y8,x8-26,y8+6); line(x8-26,y8+62,x8-26,GND,"#2c3e50"); dot(x8-26,GND); txt(x8-26,y8+88,"R_prog (10 mA/seg)",10,"#777")
# REF OUT bus down into the open band below the chip
x7,y7=p[7]; refx=410; tY=716; tLx=452; tHx=536
line(x7,y7,refx,y7,"#8e44ad"); line(refx,y7,refx,tY,"#8e44ad"); dot(refx,y7,4,"#8e44ad")
txt(x7-38,y7-10,"REF OUT 1.25 V",11,"#8e44ad",weight="bold",anchor="end")
line(refx,tY,tHx,tY,"#8e44ad")                      # bus feeds both trim tops
wyL=trim(tLx,tY,"TRIM-LO 10k","→0.88 V"); line(tLx,tY+70,tLx,GND,"#2c3e50"); dot(tLx,GND)
wyH=trim(tHx,tY,"TRIM-HI 10k","→1.24 V"); line(tHx,tY+70,tHx,GND,"#2c3e50"); dot(tHx,GND)
dot(tLx,tY,3,"#8e44ad"); dot(tHx,tY,3,"#8e44ad")
# wipers (exit left of each trim) up to RLO(4) and RHI(6)
x6,y6=p[6]; line(tHx-15,wyH,tHx-30,wyH,"#8e44ad"); line(tHx-30,wyH,tHx-30,y6,"#8e44ad"); line(tHx-30,y6,x6,y6,"#8e44ad")
x4,y4=p[4]; line(tLx-15,wyL,tLx-26,wyL,"#8e44ad"); line(tLx-26,wyL,tLx-26,y4,"#8e44ad"); line(tLx-26,y4,x4,y4,"#8e44ad")

# ---------- bargraph (x=1050) ----------
BGx,BGy,segw,segh=1050,150,150,42
rect(BGx-12,BGy-12,segw+48,10*segh+66,fill="#fff",stroke="#b03a2e",rx=10)
txt(BGx+segw/2,BGy+6,"2510SR-1 (10-seg)",13,"#b03a2e",weight="bold")
line(BGx+segw+24,VP,BGx+segw+24,BGy+40,"#c0392b"); dot(BGx+segw+24,VP); txt(BGx+segw+28,BGy+26,"anodes→V+",10,"#c0392b",anchor="start")
seg_pin={1:1,2:18,3:17,4:16,5:15,6:14,7:13,8:12,9:11,10:10}
for s in range(10,0,-1):
    sy=BGy+40+(10-s)*segh; col="#e74c3c" if s>3 else ("#f39c12" if s>1 else "#c0392b")
    rect(BGx,sy,segw,segh-9,fill=col,stroke="#7b241c",rx=3); txt(BGx+segw/2,sy+segh-18,f"SEG {s}",12,"#fff",weight="bold")
    cy=sy+(segh-9)/2; line(BGx+segw,cy,BGx+segw+24,cy,"#c0392b")
    line(BGx-36,cy,BGx,cy,"#2980b9"); txt(BGx-40,cy+4,f"pin {seg_pin[s]}",10,"#2980b9",anchor="end")
txt(BGx+segw/2,BGy+10*segh+58,"cathodes → LM3914 LED outputs (no series R)",11,"#2980b9")
txt(CX+CW/2,CY+CH+28,"outputs seg1..10 = pins 1,18,17,16,15,14,13,12,11,10",11,"#2980b9")
txt(W/2,H-14,"Paradox Transistor Lab · calibrate: 4.2 V → seg10 on (TRIM-HI), 3.0 V → seg1 on (TRIM-LO)",12,"#777")
e('</svg>')
open("schematic.svg","w").write("\n".join(S)); print("wrote schematic.svg")
