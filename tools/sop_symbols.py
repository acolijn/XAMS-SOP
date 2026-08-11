"""Vector safety symbols for XAMS SOP documents.

Drawn on the canvas rather than loaded from an image, so there is no asset file
to lose track of and the mark stays sharp at any size.

`WarningTriangle` is the ISO 7010 W001 general warning sign: a yellow
equilateral triangle with a black border and an exclamation mark. In ISO 3864-2
this is the *safety-alert symbol* and it means personal injury, which is why
NOTICE - property damage only - must never carry one.
"""

from reportlab.lib import colors
from reportlab.platypus import Flowable

SIGN_YELLOW = colors.HexColor("#f5c518")


class WarningTriangle(Flowable):
    """ISO 7010 W001 general warning sign, drawn `size` points square."""

    def __init__(self, size=13.0, fill=SIGN_YELLOW, stroke=colors.black):
        super().__init__()
        self.size = size
        self.fill = fill
        self.stroke = stroke

    def wrap(self, *_args):
        return self.size, self.size

    def draw(self):
        canvas, size = self.canv, self.size
        inset = size * 0.05
        apex = size * 0.95
        canvas.saveState()
        canvas.setFillColor(self.fill)
        canvas.setStrokeColor(self.stroke)
        canvas.setLineWidth(max(0.7, size * 0.07))
        canvas.setLineJoin(1)          # rounded, so small sizes do not spike
        path = canvas.beginPath()
        path.moveTo(size / 2.0, apex)
        path.lineTo(size - inset, inset)
        path.lineTo(inset, inset)
        path.close()
        canvas.drawPath(path, stroke=1, fill=1)
        # exclamation mark: a bar over a dot, both in the border colour
        canvas.setFillColor(self.stroke)
        bar_w = size * 0.11
        canvas.rect(size / 2.0 - bar_w / 2.0, size * 0.36, bar_w, size * 0.32,
                    stroke=0, fill=1)
        canvas.circle(size / 2.0, size * 0.28, bar_w * 0.6, stroke=0, fill=1)
        canvas.restoreState()
