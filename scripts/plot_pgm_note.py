#!/usr/bin/env python3
"""Original, reproducible illustrations for the pGM explainer.

Requires matplotlib and numpy. Curves are evaluations of the equations in
the note, not fitted parameters or simulation results from Wei et al.
"""
from math import erf, pi, sqrt
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle
import numpy as np

OUT = Path(__file__).resolve().parents[1] / 'content/post/2026-10-15-what-is-pgm'
BLUE, TEAL, COPPER, INK, PAPER = '#345580', '#598782', '#AE7456', '#304353', '#F6F1E7'
plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': 12, 'text.color': INK,
    'axes.labelcolor': INK, 'xtick.color': INK, 'ytick.color': INK,
    'axes.edgecolor': '#A6AAA1', 'axes.spines.top': False, 'axes.spines.right': False,
    'axes.facecolor': PAPER, 'figure.facecolor': PAPER, 'savefig.facecolor': PAPER,
    'svg.fonttype': 'none', 'mathtext.fontset': 'dejavusans',
})


def save(fig, name):
    svg = OUT / f'{name}.svg'
    fig.savefig(svg, bbox_inches='tight', pad_inches=.18)
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines()) + '\n')
    fig.savefig(OUT / f'{name}.png', dpi=200, bbox_inches='tight', pad_inches=.18)
    plt.close(fig)


def densities():
    x = np.linspace(-3, 3, 801)
    mono = np.exp(-x*x)
    dip = x*mono
    fig, axs = plt.subplots(1, 2, figsize=(10, 4.2), layout='constrained')
    for ax in axs:
        ax.axhline(0, color='#A6AAA1', lw=.9)
        ax.axvline(0, color='#CECEC3', lw=.9, linestyle=':')
        ax.set_xlabel(r'$\beta(r_x-R_x)$')
        ax.set_xlim(-3, 3)
    axs[0].plot(x, mono, color=BLUE, lw=2.5)
    axs[0].fill_between(x, mono, color=BLUE, alpha=.10)
    axs[0].set_title('a  Gaussian monopole', loc='left', fontsize=14, pad=14)
    axs[0].set_ylabel(r'$\rho^{(0)}/[q(\beta/\sqrt{\pi})^3]$')
    axs[0].set_ylim(-.06, 1.18)
    axs[0].text(-2.8, .92, 'Charge spread around\nthe atomic center', fontsize=10)
    axs[1].plot(x, dip, color=COPPER, lw=2.5)
    axs[1].fill_between(x, dip, where=x>=0, color=COPPER, alpha=.16)
    axs[1].fill_between(x, dip, where=x<=0, color=BLUE, alpha=.12)
    axs[1].set_title('b  Gaussian dipole along x', loc='left', fontsize=14, pad=14)
    axs[1].set_ylabel(r'$\rho^{(1)}/[2\beta\mu_x(\beta/\sqrt{\pi})^3]$')
    axs[1].set_ylim(-.57, .57)
    axs[1].text(-2.85, .40, 'Signed density:\nzero net charge', fontsize=10)
    save(fig, 'gaussian-densities')


def kernel():
    x = np.linspace(.02, 4, 900)
    erfs = np.array([erf(float(t)) for t in x])
    k = erfs/x
    field = erfs/x**2 - 2/np.sqrt(pi)*np.exp(-x*x)/x
    fig, axs = plt.subplots(1, 2, figsize=(10, 4.3), layout='constrained')
    for ax in axs:
        ax.set_xlim(0, 4)
        ax.set_xlabel(r'$\beta_{12}R^{12}$')
        ax.grid(axis='y', color='#DAD9D0', lw=.7)
    axs[0].plot(x, 1/x, '--', color='#929589', lw=1.8, label='Point-charge limit')
    axs[0].plot(x, k, color=BLUE, lw=2.5, label='Gaussian monopoles')
    axs[0].plot(0, 2/sqrt(pi), 'o', color=BLUE, markersize=5, clip_on=False)
    axs[0].set_ylim(0, 2.6)
    axs[0].set_ylabel(r'$\phi^{effective}/(q_2\beta_{12})$')
    axs[0].set_title('a  Effective potential', loc='left', fontsize=14, pad=14)
    axs[0].legend(frameon=False, fontsize=10, loc='upper right')
    axs[0].annotate(r'$2/\sqrt{\pi}$ at $R^{12}=0$', xy=(0, 2/sqrt(pi)),
                    xytext=(.75, 1.55), fontsize=11,
                    arrowprops={'arrowstyle':'-', 'color':BLUE})
    axs[1].plot(x, 1/x**2, '--', color='#929589', lw=1.8, label='Point-charge limit')
    axs[1].plot(x, field, color=TEAL, lw=2.5, label='Gaussian monopoles')
    axs[1].plot(0, 0, 'o', color=TEAL, markersize=5, clip_on=False)
    axs[1].set_ylim(0, 1.5)
    axs[1].set_ylabel(r'$|\vec{E}^{effective}|/(|q_2|\beta_{12}^{2})$')
    axs[1].set_title('b  Effective field magnitude', loc='left', fontsize=14, pad=14)
    axs[1].legend(frameon=False, fontsize=9.5, loc='upper right')
    save(fig, 'gaussian-kernel')


def cbv():
    fig, axs = plt.subplots(1, 2, figsize=(10, 4.4), layout='constrained')
    atoms = {'A':np.array([0., 0.]), 'B':np.array([-.90, 1.15]), 'C':np.array([1.08, 1.])}
    for ax in axs:
        ax.set_aspect('equal'); ax.axis('off')
        ax.set_xlim(-1.5,1.7); ax.set_ylim(-.65,1.7)
        for h in ('B','C'):
            ax.plot(*np.array([atoms['A'],atoms[h]]).T, color='#B4B9B2', lw=3, zorder=1)
        for name, position in atoms.items():
            color=BLUE if name=='A' else TEAL
            ax.add_patch(Circle(position,.09,facecolor=color,zorder=4))
            offset=np.array([-.28,-.02]) if name=='B' else np.array([.13,-.07])
            if name=='A': offset=np.array([-.05,-.30])
            ax.text(*(position+offset),name,fontsize=13)
    def arrow(ax,start,end,color,label,offset):
        a=atoms[start]; b=a+.78*(atoms[end]-a)
        ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=16,
                                    linewidth=2,color=color,zorder=5,shrinkA=0,shrinkB=0))
        ax.text(*((a+b)/2+np.array(offset)),label,color=color,fontsize=12)
    arrow(axs[0],'A','B',BLUE,r'$\vec{e}^{BA}$',(-.53,-.02))
    arrow(axs[0],'A','C',COPPER,r'$\vec{e}^{CA}$',(.08,-.03))
    axs[0].set_title('a  Basis at A (oxygen)',loc='left',fontsize=14,pad=12)
    axs[1].plot(*np.array([atoms['B'],atoms['C']]).T, '--',color='#AEB2A9',lw=1.6,zorder=1)
    arrow(axs[1],'C','A',BLUE,r'$\vec{e}^{AC}$',(.03,-.25))
    arrow(axs[1],'C','B',COPPER,r'$\vec{e}^{BC}$',(-.18,.20))
    axs[1].text(-.55,1.50,'Virtual direction; not a chemical bond',fontsize=9,color='#65736A')
    axs[1].set_title('b  Basis at C (hydrogen)',loc='left',fontsize=14,pad=12)
    save(fig,'covalent-basis')


if __name__ == '__main__':
    OUT.mkdir(parents=True,exist_ok=True)
    densities(); kernel(); cbv()
