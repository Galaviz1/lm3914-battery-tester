#!/usr/bin/env python3
"""breadboard.svg — LM3914 Li-ion battery tester, hole-by-hole breadboard layout."""

PITCH=26; NC=42
LX=70; TOPY=120
S=[]
def e(x): S.append(x)
def line(x1,y1,x2,y2,c="#222",w=3,cap="round"):
    e(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{c}" stroke-width="{w}" stroke-linecap="{cap}"/>')
def rect(x,y,w,h,fill="none",stroke="#222",sw=2,rx=0,op=1):
    e(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" rx="{rx}" opacity="{op}"/>')
def txt(x,y,s,size=13,c="#111",anchor="middle",weight="normal"):
    e(f'<text x="{x:.0f}" y="{y:.0f}" font-family="Helvetica,Arial,sans-serif" font-size="{size}" fill="{c}" text-anchor="{anchor}" font-weight="{weight}">{s}</text>')
def hole(x,y,r=5,c="#b9bcc2"):
    e(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#fff" stroke="{c}" stroke-width="1.5"/>')

# ---- row y-coordinates ----
rows={}
y=TOPY
rows['P+']=y; y+=PITCH
rows['P-']=y; y+=PITCH*1.6
for r in "ABCDE": rows[r]=y; y+=PITCH
TRENCH=y+PITCH*0.2; y+=PITCH*1.2
for r in "FGHIJ": rows[r]=y; y+=PITCH
y+=PITCH*0.6
rows['Q+']=y; y+=PITCH
rows['Q-']=y
BW=LX+ (NC+1)*PITCH
BH=rows['Q-']+PITCH

def hx(col): return LX+col*PITCH
def hy(row): return rows[row]

W,H=BW+70, BH+470
e(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
rect(0,0,W,H,fill="#fbfbf8",stroke="none")
txt(W/2,40,"LM3914 Li-ion Battery Tester — Breadboard Layout",23,"#111",weight="bold")
txt(W/2,64,"18650 (3.0–4.2 V) · 5 V powered · bar mode · 2510SR-1 10-seg",14,"#555")

# ---- board body ----
rect(LX-34, TOPY-26, BW-LX+68, BH-TOPY+52, fill="#f4f1ea", stroke="#d8d3c6", sw=2, rx=14)
# power rail lines
line(LX-10, hy('P+')-9, hx(NC)+10, hy('P+')-9, "#e74c3c", 2)
line(LX-10, hy('P-')+9, hx(NC)+10, hy('P-')+9, "#2c7fb8", 2)
line(LX-10, hy('Q+')-9, hx(NC)+10, hy('Q+')-9, "#e74c3c", 2)
line(LX-10, hy('Q-')+9, hx(NC)+10, hy('Q-')+9, "#2c7fb8", 2)
txt(LX-46, hy('P+')+5,"+",16,"#e74c3c",weight="bold"); txt(LX-46, hy('P-')+5,"–",16,"#2c7fb8",weight="bold")
txt(LX-46, hy('Q+')+5,"+",16,"#e74c3c",weight="bold"); txt(LX-46, hy('Q-')+5,"–",16,"#2c7fb8",weight="bold")
# column numbers
for col in range(1,NC+1):
    if col%5==0 or col==1: txt(hx(col), TOPY-34, str(col), 11, "#999")
# row letters
for r in "ABCDE"+"FGHIJ": txt(LX-20, hy(r)+5, r, 12, "#aaa")
# holes
for col in range(1,NC+1):
    hole(hx(col), hy('P+')); hole(hx(col), hy('P-'))
    hole(hx(col), hy('Q+')); hole(hx(col), hy('Q-'))
    for r in "ABCDE"+"FGHIJ": hole(hx(col), hy(r))
# trench
e(f'<rect x="{LX-10:.0f}" y="{TRENCH-6:.0f}" width="{BW-LX+20:.0f}" height="12" fill="#e8e4da"/>')

# ---------------------------------------------------------------------------
# helper to drop a jumper between two holes
def jump(c1,r1,c2,r2,color):
    x1,y1,x2,y2=hx(c1),hy(r1),hx(c2),hy(r2)
    e(f'<circle cx="{x1:.0f}" cy="{y1:.0f}" r="4" fill="{color}"/>')
    e(f'<circle cx="{x2:.0f}" cy="{y2:.0f}" r="4" fill="{color}"/>')
    if r1==r2:
        line(x1,y1,x2,y2,color,3)
    else:
        line(x1,y1,x1,(y1+y2)/2,color,3); line(x1,(y1+y2)/2,x2,(y1+y2)/2,color,3); line(x2,(y1+y2)/2,x2,y2,color,3)

# ---------------------------------------------------------------------------
# LM3914 DIP-18 : cols 6..14. row E = pins 18..10, row F = pins 1..9
C0=6
rect(hx(C0)-10, hy('E')-8, (8)*PITCH+20, hy('F')-hy('E')+16, fill="#2b2b2b", stroke="#000", rx=6, op=0.92)
txt(hx(C0+4), (hy('E')+hy('F'))/2-4, "LM3914", 14, "#fff", weight="bold")
e(f'<path d="M {hx(C0)-10} {(hy("E")+hy("F"))/2-10} a10 10 0 0 0 0 20" fill="#111"/>')  # notch left
Etop={}; Fbot={}
for i in range(9):
    pin_top=[18,17,16,15,14,13,12,11,10][i]; pin_bot=[1,2,3,4,5,6,7,8,9][i]
    Etop[pin_top]=C0+i; Fbot[pin_bot]=C0+i
    txt(hx(C0+i), hy('E')-12, str(pin_top), 9, "#f1c40f")
    txt(hx(C0+i), hy('F')+18, str(pin_bot), 9, "#f1c40f")

# 2510SR-1 DIP-20 : cols 23..32. row F = cathodes seg1..10, row E = anodes
B0=23
rect(hx(B0)-10, hy('E')-8, (9)*PITCH+20, hy('F')-hy('E')+16, fill="#7b241c", stroke="#000", rx=6, op=0.95)
txt(hx(B0+4.5), (hy('E')+hy('F'))/2-18, "2510SR-1", 13, "#fff", weight="bold")
txt(hx(B0+4.5), (hy('E')+hy('F'))/2+2, "10-seg bar", 10, "#f5b7b1")
# segment tick marks inside
for i in range(10):
    cx=hx(B0+i); rect(cx-6, (hy('E')+hy('F'))/2+8, 12, 10, fill="#e74c3c", stroke="#922", sw=1, rx=2)
segA={}; segK={}
for i in range(10):
    seg=i+1
    segK[seg]=B0+i   # cathode row F
    segA[seg]=B0+i   # anode row E
    txt(hx(B0+i), hy('F')+18, f"{seg}", 9, "#f5b7b1")
txt(hx(B0+4.5), hy('F')+34, "row F = cathodes (seg 1..10) · row E = anodes", 10, "#9a7b00")

# ---------------------------------------------------------------------------
# PASSIVES drawn as labeled parts bridging holes (place in free columns)
def partH(c1,c2,row,label,fill="#d9c08a"):
    x1,x2=hx(c1),hx(c2); yy=hy(row)
    e(f'<circle cx="{x1:.0f}" cy="{yy:.0f}" r="4" fill="#555"/>'); e(f'<circle cx="{x2:.0f}" cy="{yy:.0f}" r="4" fill="#555"/>')
    line(x1,yy,x1+10,yy,"#888",2); line(x2-10,yy,x2,yy,"#888",2)
    rect(x1+10, yy-9, x2-x1-20, 18, fill=fill, stroke="#7a6a3a", rx=4)
    txt((x1+x2)/2, yy+4, label, 10, "#3a2f13")
def partV(col,r1,r2,label,fill="#d9c08a"):
    x=hx(col); y1,y2=hy(r1),hy(r2)
    e(f'<circle cx="{x:.0f}" cy="{y1:.0f}" r="4" fill="#555"/>'); e(f'<circle cx="{x:.0f}" cy="{y2:.0f}" r="4" fill="#555"/>')
    line(x,y1,x,y1+10,"#888",2); line(x,y2-10,x,y2,"#888",2)
    rect(x-9, y1+10, 18, y2-y1-20, fill=fill, stroke="#7a6a3a", rx=4)
    txt(x+14, (y1+y2)/2+4, label, 10, "#3a2f13", anchor="start")

# input divider: cell+ rail area. Use cols 2-3 (left). 24k from A2->A4? Simplify: put divider off to left using rows A..E col 2
# PASSIVES — each bridges DIFFERENT column groups (never within one A-E/F-J group)
# Input divider (left): 24k col1->col3, 10k col3->col5.  SIG node = col3 group.
partH(1,3,'B',"24 kΩ")
partH(3,5,'C',"10 kΩ")
# V+ bypass caps across the top rails (+ to -)
def railcap(col,label):
    x=hx(col); ym=(hy('P+')+hy('P-'))/2
    e(f'<circle cx="{x:.0f}" cy="{hy("P+"):.0f}" r="4" fill="#555"/>'); e(f'<circle cx="{x:.0f}" cy="{hy("P-"):.0f}" r="4" fill="#555"/>')
    line(x,hy('P+'),x,ym-6,"#888",2); line(x,ym+6,x,hy('P-'),"#888",2)
    line(x-9,ym-6,x+9,ym-6,"#555",3); line(x-9,ym+6,x+9,ym+6,"#555",3)
    txt(x+13,ym+4,label,9,"#777",anchor="start")
railcap(39,"2.2µF"); railcap(41,"0.1µF")
# R_prog 1.2k (right zone), cols 34->36
partH(34,36,'H',"1.2 kΩ")
# trimpots (3 columns each) in the middle zone
def trimpot(colL,label,setv):
    x=hx(colL); yy=hy('H')
    rect(x-8, yy-10, PITCH*2+16, 42, fill="#6c3483", stroke="#4a235a", rx=5)
    txt(x+PITCH, yy-16, label, 10, "#8e44ad", weight="bold")
    for k in range(3):
        e(f'<circle cx="{hx(colL+k):.0f}" cy="{hy("J"):.0f}" r="4" fill="#4a235a"/>')
        line(hx(colL+k), yy+32, hx(colL+k), hy('J'),"#4a235a",3)
    txt(x+PITCH, yy+56, setv, 9, "#8e44ad")
    return (colL, colL+1, colL+2)
tlo=trimpot(15,"TRIM-LO","→0.88 V")   # cols 15(endA→REFO) 16(wiper→RLO) 17(endB→GND)
thi=trimpot(19,"TRIM-HI","→1.24 V")   # cols 19(endA→REFO) 20(wiper→RHI) 21(endB→GND)

# ---------------------------------------------------------------------------
# JUMPERS
RED="#c0392b"; BLU="#2c7fb8"; PUR="#8e44ad"; GRN="#1e8449"; BLK="#333"
# power
jump(Fbot[3],'G', Fbot[3],'Q+', RED)   # V+  (pin3,col8) -> + rail
jump(Fbot[2],'G', Fbot[2],'Q-', BLU)   # V-  (pin2,col7) -> - rail
jump(14,'G', 14,'Q+', RED)             # MODE(pin9,col14) -> + rail
# SIG node (col3 top group) -> pin5 (col10 bottom)
jump(3,'D', Fbot[5],'G', BLK)
jump(5,'D', 5,'Q-', BLU)               # divider bottom (col5) -> GND
# reference network
jump(Fbot[7],'G', 15,'J', PUR)         # REFO(pin7,col12) -> TRIM-LO endA
jump(15,'J', 19,'J', PUR)              # tie REFO across to TRIM-HI endA
jump(Fbot[4],'G', 16,'J', PUR)         # RLO(pin4,col9)  -> TRIM-LO wiper
jump(Fbot[6],'G', 20,'J', PUR)         # RHI(pin6,col11) -> TRIM-HI wiper
jump(17,'J', 17,'Q-', BLU)             # TRIM-LO endB -> GND
jump(21,'J', 21,'Q-', BLU)             # TRIM-HI endB -> GND
jump(Fbot[8],'G', 34,'H', BLK)         # REFA(pin8,col13) -> R_prog
jump(36,'H', 36,'Q-', BLU)             # R_prog -> GND
# LED outputs -> bargraph cathodes (shown as arrow + table to avoid 10 crossing wires)
e('<defs><marker id="ar" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#1e8449"/></marker></defs>')
txt((hx(14)+hx(23))/2, hy('E')-44, "LED outputs → bargraph cathodes (see table)", 11, GRN, weight="bold")
e(f'<path d="M {hx(15):.0f} {hy("E")-34} L {hx(22):.0f} {hy("E")-34}" stroke="#1e8449" stroke-width="2" marker-end="url(#ar)"/>')
# tie both + rails and both - rails together (far right, clear of parts)
jump(42,'P+',42,'Q+',RED); jump(42,'P-',42,'Q-',BLU)

# ---- input terminals (cell under test) ----
rect(LX-34, BH+24, 196, 84, fill="#fff7e6", stroke="#e0a800", rx=8)
txt(LX+64, BH+48,"CELL UNDER TEST (18650)",11,"#9a7b00",weight="bold")
txt(LX+24, BH+84,"＋",18,"#c0392b"); txt(LX+104, BH+84,"－",16,"#2c3e50")
line(hx(1), BH+24, hx(1), hy('A'), "#c0392b", 3)       # + -> col1 (24k top)
line(hx(2), BH+24, hx(2), hy('Q-'), "#2c3e50", 3)      # - -> GND rail (col2)
txt(hx(1), hy('A')-10,"+cell",9,"#c0392b"); txt(hx(2), BH+118,"–cell→GND",9,"#2c3e50")

# ---- wiring table ----
TBx=300; TBy=BH+30
txt(TBx, TBy, "Wiring (LM3914 pin → net)", 14, "#111", anchor="start", weight="bold")
rows_tbl=[
 ("3  V+","→ + rail (5 V)"),("2  V-","→ – rail (GND)"),("9  MODE","→ + rail (bar mode)"),
 ("5  SIG","→ divider node (24k/10k)"),("7  REFO","→ top of both trimpots"),
 ("8  REFA","→ 1.2k → – rail"),("6  RHI","→ TRIM-HI wiper"),("4  RLO","→ TRIM-LO wiper"),
 ("1,18..10","→ bargraph cathodes seg1..10"),
 ("bargraph anodes","→ + rail (5 V)"),
]
for i,(a,b) in enumerate(rows_tbl):
    yy=TBy+24+i*22
    txt(TBx, yy, a, 12, "#8e44ad" if ("REF" in a or "RHI" in a or "RLO" in a) else "#111", anchor="start", weight="bold")
    txt(TBx+140, yy, b, 12, "#333", anchor="start")
# segment->pin map
MPx=TBx+430
txt(MPx, TBy, "Segment → LM3914 output pin", 14, "#111", anchor="start", weight="bold")
seg_pin={1:1,2:18,3:17,4:16,5:15,6:14,7:13,8:12,9:11,10:10}
for i in range(10):
    yy=TBy+24+i*22; s=i+1
    txt(MPx, yy, f"seg {s}", 12, "#111", anchor="start")
    txt(MPx+70, yy, f"→ pin {seg_pin[s]}", 12, GRN, anchor="start", weight="bold")

# note about bargraph pinout
NTx=TBx; NTy=TBy+24+len(rows_tbl)*22+24
rect(NTx-6, NTy-16, 620, 56, fill="#fff3cd", stroke="#e0a800", rx=6)
txt(NTx, NTy+2, "⚠ 10-segment bargraph pinouts differ by maker. Verify which row of the", 11, "#7a5b00", anchor="start")
txt(NTx, NTy+20, "2510SR-1 is anodes vs cathodes before wiring (anodes → +5 V, cathodes → LM3914 outputs).", 11, "#7a5b00", anchor="start")

txt(W/2, H-14, "Paradox Transistor Lab · calibrate: 4.2 V → seg10 (TRIM-HI), 3.0 V → seg1 (TRIM-LO)", 12, "#777")
e('</svg>')
open("breadboard.svg","w").write("\n".join(S)); print("wrote breadboard.svg")
