#!/usr/bin/env python3
"""Reproducible source for the six manuscript figures of main_jisa.tex.
Run:  python3 make_figures.py   (needs matplotlib).
Outputs figure1.png ... figure6.png next to this script.
Benchmark numbers for figure6 live in BENCH below: update them after a
re-measurement and re-run this script."""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

HERE = os.path.dirname(os.path.abspath(__file__))
BLUE=('#dce8f7','#1b4a8b'); ORANGE=('#fbe6cc','#d9881d'); GREEN=('#d8ece1','#317d5c')
RED=('#f6d9d4','#ab4335'); GRAY=('white','#5a5a5a'); KEY=('#f2f2f2','#8a8a8a')

def save(fig,name):
    fig.savefig(os.path.join(HERE,name),dpi=200,bbox_inches='tight',pad_inches=0.05)
    plt.close(fig); print("wrote",name)

def newax(w=10,h=5):
    fig,ax=plt.subplots(figsize=(w,h),dpi=130); ax.set_xlim(0,100); ax.set_ylim(0,50)
    ax.axis('off'); return fig,ax

def box(ax,x,y,w,h,l1,l2,col,dashed=False,fs1=10,fs2=9,align='c'):
    fc,ec=col
    ax.add_patch(FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.2,rounding_size=1.2",
                 fc=fc,ec=ec,lw=1.3,ls='--' if dashed else '-'))
    if l2:
        ax.text(x,y+h*0.18,l1,ha='center',va='center',fontsize=fs1,color='#222')
        ax.text(x,y-h*0.22,l2,ha='center',va='center',fontsize=fs2,color='#333')
    else:
        ax.text(x,y,l1,ha='center',va='center',fontsize=fs1,color='#222')

def arr(ax,p1,p2,dashed=False,color='#444',rad=0.0,scale=12,lw=1.2,zorder=3):
    ax.add_patch(FancyArrowPatch(p1,p2,arrowstyle='-|>',mutation_scale=scale,lw=lw,
                 color=color,ls='--' if dashed else '-',connectionstyle=f"arc3,rad={rad}",zorder=zorder))

def border(ax):
    ax.add_patch(FancyBboxPatch((1.5,1.5),97,47,boxstyle="round,pad=0.2,rounding_size=2",
                fc='none',ec='#444',lw=1.3,ls=(0,(6,4))))

def fig_border(fig):
    # figure-level dashed rounded frame so chart figures match the box-diagram style
    fig.add_artist(FancyBboxPatch((0.018,0.03),0.966,0.94,boxstyle="round,pad=0,rounding_size=0.02",
                   transform=fig.transFigure,fc='none',ec='#444',lw=1.3,ls=(0,(6,4)),clip_on=False))

# ---------------- Figure 1: threat-boundary map ----------------
def fig1():
    fig,ax=newax(10,5); border(ax)
    box(ax,50,25,20,9,'Hybrid PQ-OPAQUE','claim surface',('white','#222'),fs1=11,fs2=11)
    ax.text(20,46,"inside the paper's claims",ha='center',fontsize=10,color='#317d5c',style='italic')
    ax.text(80,46,'requires separate analysis',ha='center',fontsize=10,color='#ab4335',style='italic')
    left=['active network control','passive database disclosure','post-session long-term keys','quantum recovery of classical DH']
    right=[r'$\sigma_{\mathrm{oprf}}$ compromise','live endpoint compromise','malicious RNG and side channels','resource-exhaustion availability']
    ys=[40,32,24,16]
    for t,y in zip(left,ys):
        box(ax,19,y,30,5.5,t,'',GREEN,fs1=8.5)
        arr(ax,(34,y),(40,25),color='#444',rad=0.05)
    for t,y in zip(right,ys):
        box(ax,81,y,30,5.5,t,'',RED,dashed=True,fs1=8.5)
        arr(ax,(60,25),(66,y),dashed=True,color='#ab4335',rad=0.05)
    save(fig,'figure1.png')

# ---------------- Figure 2: protocol flow ----------------
def fig2():
    fig,ax=newax(11,6.2); border(ax)
    xc,xs=18,82
    # phase bands
    ax.add_patch(FancyBboxPatch((5.5,31),89,9,boxstyle="round,pad=0.2,rounding_size=1.5",
                 fc='#eef4fb',ec='#cdddf0',lw=1.0,zorder=0))
    ax.add_patch(FancyBboxPatch((5.5,8.5),89,19,boxstyle="round,pad=0.2,rounding_size=1.5",
                 fc='#eef6f1',ec='#cfe6da',lw=1.0,zorder=0))
    ax.text(8,38.5,'Registration',ha='left',va='center',fontsize=11,weight='bold',color='#1b4a8b')
    ax.text(8,26,'Authentication',ha='left',va='center',fontsize=11,weight='bold',color='#317d5c')
    # lifelines
    for x in (xc,xs): ax.plot([x,x],[6.5,43],color='#9bb0c6',lw=1.2,ls=(0,(4,3)),zorder=1)
    # actor headers
    box(ax,xc,45.5,24,5,r'Initiator $\mathcal{C}$','',('#dce8f7','#1b4a8b'),fs1=12)
    box(ax,xs,45.5,34,5,r'Record-holding responder $\mathcal{S}$','',('#d8ece1','#317d5c'),fs1=11)
    def msg(y,x1,x2,label,fs=10):
        arr(ax,(x1,y),(x2,y),color='#2b2b2b',scale=15,lw=1.8,zorder=4)
        ax.text((x1+x2)/2,y+2.1,label,ha='center',va='center',fontsize=fs,color='#111',
                bbox=dict(boxstyle='round,pad=0.35',fc='white',ec='#bbb',lw=0.8),zorder=6)
    # registration
    msg(37,xc,xs,r'$B$')
    msg(33,xs,xc,r'$Z \| PK_S$')
    ax.text(xc-2,29.2,r'sealed envelope and $PK_C$',ha='left',va='center',fontsize=9,color='#555',
            bbox=dict(boxstyle='round,pad=0.3',fc='white',ec='#bbb',lw=0.8),zorder=6)
    # authentication
    msg(23,xc,xs,r'KE1: $B \| E_C \| n_C \| pk_{\mathrm{kem}}$')
    msg(17.5,xs,xc,r'KE2: $n_S \| E_S \| \mathrm{CredResp} \| \mathrm{MAC}_S \| ct_{\mathrm{kem}}$',fs=9)
    msg(12,xc,xs,r'KE3: $\mathrm{MAC}_C$')
    # bottom context
    ax.text(50,5,r'$\mathrm{acct}\to\eta$,   $(pk_{\mathrm{kem}}, ct_{\mathrm{kem}}, \eta)\subset\tau$,   $\tau\to\tau_H$',
            ha='center',va='center',fontsize=9,color='#444',
            bbox=dict(boxstyle='round,pad=0.4',fc='#fbfbfb',ec='#ccc',lw=0.8))
    save(fig,'figure2.png')

# ---------------- Figure 3: wire-size growth ----------------
def fig3():
    fig,ax=plt.subplots(figsize=(7,3.6),dpi=130)
    groups=['KE1','KE2','KE3']; classical=[88,288,64]; hybrid=[1273,1377,65]
    import numpy as np
    x=np.arange(3); w=0.36
    ax.bar(x-w/2,classical,w,label='Classical payload',color=BLUE[0],edgecolor=BLUE[1])
    b=ax.bar(x+w/2,hybrid,w,label='Hybrid wire format',color=ORANGE[0],edgecolor=ORANGE[1])
    for i,v in enumerate(hybrid):
        ax.text(x[i]+w/2,v+25,str(v),ha='center',fontsize=8.5,color=ORANGE[1])
    ax.set_xticks(x); ax.set_xticklabels(groups); ax.set_ylabel('Bytes'); ax.set_ylim(0,1550)
    ax.set_xlabel('Message'); ax.legend(frameon=False,fontsize=9)
    for s in ('top','right'): ax.spines[s].set_visible(False)
    fig_border(fig)
    save(fig,'figure3.png')

# ---------------- Figure 5: hybrid-condition surface ----------------
def fig5():
    fig,ax=newax(10,5); border(ax)
    ax.text(54,46,r'classical source $\mathrm{IKM_{cl}}$',ha='center',fontsize=11,color='#1b4a8b')
    ax.text(9,24,r'ML-KEM source $\mathrm{IKM_{pq}}$',ha='center',va='center',rotation=90,fontsize=11,color='#d9881d')
    ax.text(36,40,'hidden',ha='center',fontsize=10,weight='bold')
    ax.text(72,40,'recoverable',ha='center',fontsize=10,weight='bold')
    ax.text(18,33,'hidden',ha='center',va='center',rotation=90,fontsize=10,weight='bold')
    ax.text(18,16,'recoverable',ha='center',va='center',rotation=90,fontsize=10,weight='bold')
    cells=[(36,33,'both sources hidden','PRK pseudorandom',GREEN),
           (72,33,'ML-KEM hidden','PRK pseudorandom',GREEN),
           (36,16,'classical hidden','PRK pseudorandom',GREEN),
           (72,16,'both recoverable','outside the bound',RED)]
    for x,y,a,b,col in cells: box(ax,x,y,30,11,a,b,col,fs1=10,fs2=9.5)
    box(ax,54,6.5,60,5,r'Extractor loss in all cases: $\mathrm{Adv}^{\mathrm{ext}}_{\mathrm{HKDF}}$','',('#f5f5f5','#888'),fs1=10)
    save(fig,'figure5.png')

# ---------------- Figure 6: runtime profile ----------------
# values in microseconds; (label, value_us, display, color)
BENCH=[('4DH profile',257.79,r'257.79 $\mu$s',BLUE),
       ('ML-KEM round',333.22,r'333.22 $\mu$s',ORANGE),
       ('KE2 generation',568.03,r'568.03 $\mu$s',GREEN),
       ('Argon2id',784600.0,'784.60 ms',RED),
       ('KE3 generation',794720.0,'794.72 ms',('#efd9d4','#9c6b63')),
       ('End-to-end auth',798740.0,'798.74 ms',GRAY)]
def fig6():
    fig,ax=plt.subplots(figsize=(7.2,3.8),dpi=130)
    labels=[b[0] for b in BENCH][::-1]; vals=[b[1] for b in BENCH][::-1]
    disp=[b[2] for b in BENCH][::-1]; cols=[b[3] for b in BENCH][::-1]
    y=range(len(labels))
    for yi,v,c in zip(y,vals,cols): ax.barh(yi,v,color=c[0],edgecolor=c[1],height=0.6)
    for yi,v,d in zip(y,vals,disp): ax.text(v*1.15,yi,d,va='center',fontsize=8.5,color='#333')
    ax.set_xscale('log'); ax.set_yticks(list(y)); ax.set_yticklabels(labels,fontsize=9)
    ax.set_xlim(1,3_000_000); ax.set_xlabel('time')
    ax.set_xticks([1,10,100,1000,10000,100000,1000000])
    ax.set_xticklabels([r'1 $\mu$s',r'10 $\mu$s',r'100 $\mu$s','1 ms','10 ms','100 ms','1 s'],fontsize=8)
    ax.set_title('log-scale, Criterion mean on the Linux/Xeon benchmark platform',fontsize=9.5)
    for s in ('top','right'): ax.spines[s].set_visible(False)
    fig_border(fig)
    save(fig,'figure6.png')

# ---------------- Figure 4: hybrid key schedule ----------------
def fig4():
    fig,ax=newax(10,5); border(ax)
    box(ax,26,43,15,5.5,r'$\mathrm{acct}\to\eta$','account context',GREEN,fs1=10,fs2=8.5)
    box(ax,48,43,15,5.5,r'$\tau\to\tau_H$','extended transcript',GREEN,fs1=10,fs2=8.5)
    box(ax,70,43,15,5.5,r'$\mathrm{salt}_{\tau}$',r'$L_{\mathrm{comb}}\|\tau_H$',GREEN,fs1=10,fs2=9)
    arr(ax,(33.5,43),(40.5,43),dashed=True,color='#317d5c')
    arr(ax,(55.5,43),(62.5,43),dashed=True,color='#317d5c')
    for i,yy in enumerate([33,27,21,15]): box(ax,9,yy,9,4.6,rf'$dh_{i+1}$','',BLUE,fs1=11)
    box(ax,26,24,15,7.5,r'$\mathrm{IKM_{cl}}$',r'$dh_1\|dh_2\|dh_3\|dh_4$',BLUE,fs1=11,fs2=9)
    box(ax,26,13,15,6.5,r'$\mathrm{IKM_{pq}}$',r'$ss_{\mathrm{kem}}$',ORANGE,fs1=11,fs2=9.5)
    box(ax,46,24,13,7.5,r'$\mathrm{IKM_{hyb}}$',r'$\mathrm{IKM_{cl}}\|\mathrm{IKM_{pq}}$',GRAY,dashed=True,fs1=10,fs2=8.5)
    box(ax,63,24,13,7.5,'HKDF-Extract','PRK',GRAY,dashed=True,fs1=10,fs2=9)
    box(ax,80,24,13,7.5,'HKDF-Expand','derived keys',GRAY,dashed=True,fs1=10,fs2=9)
    for lbl,yy in [(r'$K_s$',33),(r'$K_m$',27),(r'$K_{\mathrm{mac}}^{S}$',21),(r'$K_{\mathrm{mac}}^{C}$',15)]:
        box(ax,92,yy,9,4.6,lbl,'',KEY,dashed=True,fs1=11)
    for yy in [33,27,21,15]: arr(ax,(13.5,yy),(18.5,24),color='#1b4a8b')
    arr(ax,(33.5,24),(39.5,24.6),color='#1b4a8b')
    arr(ax,(33.5,13),(39.5,22),color='#d9881d',rad=-0.15)
    arr(ax,(52.5,24),(56.5,24),color='#444'); arr(ax,(69.5,24),(73.5,24),color='#444')
    arr(ax,(70,40.2),(63,27.8),dashed=True,color='#317d5c',rad=0.1)
    for yy in [33,27,21,15]: arr(ax,(86.5,24),(87.5,yy),color='#5a5a5a')
    save(fig,'figure4.png')

if __name__=='__main__':
    fig1(); fig2(); fig3(); fig4(); fig5(); fig6()
    print('all figures regenerated')
