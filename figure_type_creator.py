from typing import Any, Dict, Literal, Union
from cycler import cycler
import seaborn as sns
from pubplot import Document
from pubplot.document_classes import usenix
from util import in2pt


class FigureTypeCreator():
    """
    Good colors:
    > sns.color_palette("colorblind")
    > sns.color_palette("tab10")
    > palettable.colorbrewer.qualitative.Paired_12.hex_colors
    """

    """
    TODO: consider building a document class based on
    https://www.overleaf.com/learn/latex/Beamer
    """

    def __init__(self,
                 type: Union[Literal['paper'],
                             Literal['presentation']] = 'paper',
                 document_class=usenix,
                 colors=sns.color_palette("colorblind"),
                 use_markers: bool = False,
                 paper_use_small_font: bool = True,
                 num_entries: int = 10
                 ):

        self.type = type
        self.document_class = document_class
        self.num_entries = num_entries
        self.use_markers = use_markers
        self.paper_use_small_font = paper_use_small_font
        self.colors = list(colors)[:self.num_entries]  # type:ignore

        # https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html
        available_linestyles = ['solid', 'dotted', 'dashed', 'dashdot']
        self.linestyles = self.get_entries(
            available_linestyles, self.num_entries)

        # https://matplotlib.org/stable/api/markers_api.html
        available_markers = ['o', '^', 's', '*', 'X', 'd']
        self.markers = self.get_entries(available_markers, self.num_entries)

        # https://matplotlib.org/stable/gallery/shapes_and_collections/hatch_style_reference.html
        available_hatches = ['', '//', '\\\\', '||', '--', '++', 'xx']
        self.hatches = self.get_entries(available_hatches, self.num_entries)

        # Map from colors to hatches, markers and line styles
        # Useful when using manual colors for lines/objects
        colors = self.colors
        self.hatch_map = {colors[i]: hatch for i,
                          hatch in enumerate(self.hatches)}
        self.marker_map = {colors[i]: marker for i,
                           marker in enumerate(self.markers)}
        self.ls_map = {colors[i]: ls for i, ls in enumerate(self.linestyles)}

    @staticmethod
    def get_entries(cycle_list, num_entries):
        n = len(cycle_list)
        m = int(num_entries / n) + 1
        return (cycle_list * m)[:num_entries]

    def get_cycler(self):
        cycling = (cycler('color', self.colors)
                   + cycler('ls', self.linestyles))
        if(self.use_markers):
            cycling += cycler('marker', self.markers)
        return cycling

    def get_figure_type(self):
        style = {
            'pdf.fonttype': 42,
            'axes.prop_cycle': self.get_cycler(),
        }
        style.update(self.get_custom_style())
        style.update(self.get_line_sizes())
        style.update(self.get_font_sizes())
        doc = Document(self.document_class, style=style)

        self.presentation_config(doc)
        self.paper_small_font(doc)

        return doc

    def get_custom_style(self):
        return {
            # https://matplotlib.org/3.5.1/gallery/ticks/auto_ticks.html
            # 'axes.xmargin': 0,
            # 'axes.ymargin': 0,
            # 'axes.autolimit_mode': 'round_numbers'
        }

    def get_line_sizes(self):
        ret: Dict[str, Any] = {
            "grid.linestyle": '--'
        }

        if(self.type == 'paper'):
            ret.update({
                'axes.linewidth': 0.5,
                'xtick.major.width': 0.5,
                'ytick.major.width': 0.5,

                'xtick.minor.width': 0.4,
                'ytick.minor.width': 0.4,

                'lines.linewidth': 0.8,
                'lines.markersize': 1.5,
                'legend.handlelength': 2.5,

                'hatch.linewidth': 0.5,

                "grid.linewidth": 0.25,
            })

        elif(self.type == 'presentation'):
            ret.update({
                # TODO
                # 'axes.linewidth': 1,
                # 'xtick.major.width': 0.5,
                # 'ytick.major.width': 0.5,

                # 'xtick.minor.width': 0.4,
                # 'ytick.minor.width': 0.4,

                # 'lines.linewidth': 0.8,
                # 'lines.markersize': 1.5,
                # 'legend.handlelength': 2.5,

                # 'hatch.linewidth': 0.5,

                # "grid.linewidth": 0.25,
            })
        else:
            raise NotImplementedError

        return ret

    def get_font_sizes(self):
        ret: Dict[str, Any] = {
            'font.family': 'sans-serif',
            'text.latex.preamble':
                "\n".join(
                    [r'\usepackage[cm]{sfmath}',
                     r'\usepackage{amsmath}']),
        }

        # For paper, pubplot automatically sets the appropriate font sizes.

        if(type == 'presentation'):
            big_size = 28
            small_size = 24
            ret.update({
                'font.size': big_size,
                'axes.titlesize': big_size,
                'axes.labelsize': big_size,
                'legend.fontsize': small_size,
                'legend.title_fontsize': big_size,
                'xtick.labelsize': small_size,
                'ytick.labelsize': small_size,
            })
        return ret

    def presentation_config(self, doc):
        # For setting figure sizes
        ppt_sizes = {
            "columnwidth": in2pt(13.33),
            "textwidth": in2pt(7.5)
        }
        doc.__dict__.update(ppt_sizes)

    def paper_small_font(self, doc):
        if(self.paper_use_small_font):
            assert self.type == 'paper'
            # Ideally we should not have any fonts less than footnotesize. Due
            # to some font issue, these fonts are big enough visually.
            # TODO: Fix this, ideally we should set the font sizes precisely.
            big_size = doc.footnotesize - 1
            small_size = doc.footnotesize - 2
            doc.update_style({
                'font.size': big_size,
                'axes.titlesize': big_size,
                'axes.labelsize': big_size,
                'legend.fontsize': small_size,
                'legend.title_fontsize': big_size,
                'xtick.labelsize': small_size,
                'ytick.labelsize': small_size
            })
