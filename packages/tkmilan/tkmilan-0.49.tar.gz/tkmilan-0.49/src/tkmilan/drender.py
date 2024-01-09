'''Renderer for `diagrams <diagram.Diagram>`.

Can support multiple backends, only one implemented so far.
'''
import typing
import logging
import numbers
from functools import singledispatchmethod
import tkinter as tk

from . import diagram
from . import exception
from . import util
if typing.TYPE_CHECKING:
    from . import Canvas

logger = logging.getLogger(__name__)


TKCANVAS_COLORMAP_TEXT = {
    'fill': 'fill',
}
TKCANVAS_COLORMAP_MULTILINE = {
    'outline': 'fill',
}


def tkcanvas_width(**options: typing.Optional[int]) -> typing.Mapping:
    '''Generate ``Tk`` canvas width arguments'''
    rval = {}
    for oname, option in options.items():
        if option is not None:
            rval[oname] = float(option)
    return rval


def tkcanvas_dash(**options: typing.Optional[diagram.D]) -> typing.Mapping:
    '''Generate related `diagram.D` ``Tk`` canvas dash arguments'''
    rval = {}
    for oname, option in options.items():
        if option is not None:
            rval[oname] = option.pattern
            if oname == 'dash':
                rval['dashoffset'] = option.offset  # type: ignore[assignment]
            # TODO: Implement missing offsets?
    return rval


def tkcanvas_arrow(option: typing.Optional[diagram.A]) -> typing.Mapping:
    '''Generate related `diagram.A` ``Tk`` canvas arrow arguments'''
    if option is None:
        return {}
    else:
        assert (option.atStart, option.atEnd) != (False, False)
        return {
            'arrow': {
                (True, False): tk.FIRST,
                (False, True): tk.LAST,
                (True, True): tk.BOTH,
            }[option.atStart, option.atEnd],
            'arrowshape': (option.d1, option.d2, option.d3),
        }


def tkcanvas_smooth(option: typing.Optional[diagram.Smooth]) -> typing.Mapping:
    '''Generate related `diagram.Smooth` ``Tk`` canvas smooth arguments'''
    if option is None:
        return {}
    else:
        return {
            'smooth': True,  # TODO: Implement Bézier selection? Use `cnf`
            'splinesteps': option.steps,
        }


def tkcanvas_colors(noprefix: diagram.C,
                    cnames: typing.Optional[typing.Mapping[str, str]] = None,
                    **poptions: diagram.C) -> typing.Mapping:
    '''Generate related `diagram.C` ``Tk`` canvas color arguments.

    Args:
        noprefix: The color without prefix. Required.
        poptions: Mapping between prefix and color oboject.
        cnames: A mapping between color object option name, and ``Tk`` argument.
            Optional, defaults to ``fill`` and ``outline`` mapping to the
            corresponding names.
    '''
    assert '' not in poptions
    poptions[''] = noprefix
    rval = {}
    for oprefix, option in poptions.items():
        for cname, oname in (cnames or {s: s for s in ('fill', 'outline')}).items():
            cvalue = getattr(option, cname, None)
            if cvalue is not None:
                rval[f'{oprefix}{oname}'] = cvalue
    return rval


def tkcanvas_text_angle(angle: numbers.Real) -> typing.Mapping:
    '''Generate ``Tk`` `Text <diagram.Text>` ``angle`` arguments.

    This feature is only supported on later Tk versions.

    Args:
        angle: The angle value. Required.
    '''
    rval = {}
    if util.TK_VERSION >= (8, 6):
        rval['angle'] = str(angle)
    else:
        assert angle == 0.0, f'Unsupported Text.angle @ Tk {util.TK_VERSION}'
    return rval


# Renderer Implementation
class Renderer_TkCanvas:
    '''Renderer object for the ``Tk`` canvas backend.

    This is just a holding for the rendering process. No "automatic" draws
    happens when creating this object, all must go through the `redraw`
    function.

    Args:
        canvas: The ``Tk`` canvas object to use.
            Should be an internal `Canvas`.
        diagram: The diagram to render.
    '''
    def __init__(self, canvas: 'Canvas', diagram: diagram.Diagram):
        self._previous_size: typing.Tuple[int, int] = (-1, -1)
        self._e_clickelement: typing.Optional[str] = None
        self.diagram = diagram
        self.cv = canvas

    def redraw(self, _a1: typing.Any = None, _a2: typing.Any = None, *,
               width: typing.Optional[int] = None,
               height: typing.Optional[int] = None,
               force: bool = False,
               ):
        '''Redraw the canvas.

        The canvas consists in three layers, as explained in `diagram.Diagram`.

        If the canvas size changed, all layers are redrawn. Othewise, only the
        foreground is redrawn. Note that redrawing implies removing the old
        elements and creating new ones, this is done automatically.

        When the foreground is redrawn, it is pushed behing the background
        front layer.

        Unless ``force`` is given, the first "weird" event (when width and
        height are both ``1``) is skipped, since this does not make sense to
        redraw.

        Args:
            width: Use this canvas width, instead of getting this information
                from the ``canvas`` object.
            height: Use this canvas height, instead of getting this information
                from the ``canvas`` object.
            force: Force redrawing of background and foreground elements.

            _a1: Optional, unused. This exists for API compatibility with
                bindings.
            _a2: Optional, unused. This exists for API compatibility with
                traces.
        '''
        cv = self.cv
        cwidth = width or cv.winfo_width()
        cheight = height or cv.winfo_height()
        current_size = (cwidth, cheight)
        if not force and current_size == (1, 1):
            # The first weird Configure
            assert len(cv.find_all()) == 0
            if __debug__:
                logger.debug('Skip first weird `Configure` event: Size %s', current_size)
            return
        logger.debug('| Size: %s', current_size)
        to_skip = False
        minwidth, minheight = self.diagram.MIN_SIZE
        if not force:
            if minwidth is not None:
                if __debug__:
                    if cwidth < minwidth:
                        logger.debug('- Min Width: %d', minwidth)
                to_skip = to_skip or (cwidth < minwidth)
            if minheight is not None:
                if __debug__:
                    if cheight < minheight:
                        logger.debug('- Min Height: %d', minheight)
                to_skip = to_skip or (cheight < minheight)
        redraw_bg: bool = force or (current_size != self._previous_size)
        redraw_fg: bool = force or True  # TODO: Implement state tracker
        if to_skip:
            redraw_bg = redraw_fg = False
        if to_skip or (redraw_bg and redraw_fg):
            if __debug__:
                logger.debug('- Clean BG+FG (%d+%d)', len(cv.find_withtag(':bg')), len(cv.find_withtag(':fg')))
            assert set(cv.find_withtag(':bg || :fg')) == set(cv.find_all())
            cv.delete(tk.ALL)
        elif redraw_fg:
            if __debug__:
                logger.debug('- Clean FG (%d)', len(cv.find_withtag(':fg')))
            assert redraw_bg is False
            cv.delete(':fg')
        else:
            # Skip redraw
            assert redraw_bg is False and redraw_fg is False
        drew_fg = False
        if __debug__:
            drew_bg_b, drew_bg_f = False, False
        # TODO: Add `:latest` tag everywhere
        if redraw_bg:
            if __debug__:
                logger.debug('- Redraw BG:Back')
            tags_bg = [':bg', ':bg:b']
            for eraw in self.diagram.setup_bg_b(cwidth=cwidth, cheight=cheight):
                for element in eraw.iterate():
                    eid = self.render(element, extratags=tags_bg)
                    if eid is None:
                        if __debug__:
                            logger.warning('  - %s', element)
                        else:
                            raise exception.InvalidRender(element)
                    else:
                        logger.debug('  - %d: %s', eid, element)
                        if __debug__:
                            drew_bg_b = True
        if redraw_fg:
            if __debug__:
                logger.debug('- Redraw FG')
            tags_fg = [':fg']
            for eraw in self.diagram.setup_fg(cwidth=cwidth, cheight=cheight):
                for element in eraw.iterate():
                    eid = self.render(element, extratags=tags_fg)
                    if eid is None:
                        if __debug__:
                            logger.warning('  - %s', element)
                        else:
                            raise exception.InvalidRender(element)
                    else:
                        logger.debug('  - %d: %s', eid, element)
                        drew_fg = True
        if redraw_bg:
            if __debug__:
                logger.debug('- Redraw BG:Front')
            tags_bg = [':bg', ':bg:f']
            for eraw in self.diagram.setup_bg_f(cwidth=cwidth, cheight=cheight):
                for element in eraw.iterate():
                    eid = self.render(element, extratags=tags_bg)
                    if eid is None:
                        if __debug__:
                            logger.warning('  - %s', element)
                        else:
                            raise exception.InvalidRender(element)
                    else:
                        logger.debug('  - %d: %s', eid, element)
                        if __debug__:
                            drew_bg_f = True
        if drew_fg and len(cv.find_withtag(':bg:f')):
            if __debug__:
                logger.debug('- Lower "FG" below "BG:Front"')
            cv.tag_lower(':fg', ':bg:f')
        if __debug__:
            drew_map = {
                'BG:Back': drew_bg_b,
                'FG': drew_fg,
                'BG:Front': drew_bg_f,
            }
            drew_list = [lbl for lbl, b in drew_map.items() if b]
            logger.debug('Drew %d elements: %s', len(drew_list), ' '.join(drew_list))
            logger.debug('| Current Elements: %d', len(cv.find_all()))
        # TODO. Remove `:latest` tag, after logging the count
        # Setup Bindings
        e_clickelement = self.cv.tag_bind(tk.ALL, '<Button-1>', self.cv.onClickElement,
                                          add=False)  # Replace existing binding
        # Store information
        self._previous_size = current_size
        self._e_clickelement = e_clickelement

    @singledispatchmethod
    def render(self, de: diagram.DiagramElement, *, extratags: typing.Sequence[str] = tuple()) -> int:
        '''Render a diagram element, with some internal ``extratags``.

        This function is defined as a `single dispatch method
        <functools.singledispatchmethod>` for each supported diagram element.

        Args:
            de: The diagram element to render.
                Supported for the given diagram element types.
            extratags: Additional internal tags to consider, besides the
                element tags.
        '''
        # Fallback method for missing classes
        cls = de.__class__.__qualname__
        if __debug__:
            logger.critical('Missing render implementation for "%s"', cls)
            return -1
        else:
            raise NotImplementedError(f'Canvas: Missing render implementation for {cls}')

    @render.register
    def render_MultiLine(self, de: diagram.MultiLine, *, extratags: typing.Sequence[str] = tuple()) -> int:
        assert all(t not in de.tags for t in extratags)  # Do not alias "real" tags
        return self.cv.create_line(
            [p.tuple for p in de.points],
            tags=(*de.tags, *extratags),
            **tkcanvas_smooth(de.smooth),
            **tkcanvas_arrow(de.arrow),
            capstyle=de.cap.value, joinstyle=de.join.value,
            # Dash
            **tkcanvas_dash(dash=de.dash,
                            activedash=de.dashActive,
                            disableddash=de.dashDisabled),
            # Width
            **tkcanvas_width(width=de.width,
                             activewidth=de.widthActive,
                             disabledwidth=de.widthDisabled),
            # Colours
            **tkcanvas_colors(de.color, TKCANVAS_COLORMAP_MULTILINE,
                              active=de.colorActive,
                              disabled=de.colorDisabled)
        )

    @render.register
    def render_Polygon(self, de: diagram.Polygon, *, extratags: typing.Sequence[str] = tuple()) -> int:
        assert all(t not in de.tags for t in extratags)  # Do not alias "real" tags
        return self.cv.create_polygon(
            [p.tuple for p in de.points],
            tags=(*de.tags, *extratags),
            **tkcanvas_smooth(de.smooth),
            # Dash
            **tkcanvas_dash(dash=de.dash,
                            activedash=de.dashActive,
                            disableddash=de.dashDisabled),
            # Width
            **tkcanvas_width(width=de.width,
                             activewidth=de.widthActive,
                             disabledwidth=de.widthDisabled),
            # Colours
            **tkcanvas_colors(de.color,
                              active=de.colorActive,
                              disabled=de.colorDisabled)
        )

    @render.register
    def render_Rectangle(self, de: diagram.Rectangle, *, extratags: typing.Sequence[str] = tuple()) -> int:
        assert all(t not in de.tags for t in extratags)  # Do not alias "real" tags
        return self.cv.create_rectangle(
            de.topleft.tuple, de.botright.tuple,
            tags=(*de.tags, *extratags),
            # Dash
            **tkcanvas_dash(dash=de.dash,
                            activedash=de.dashActive,
                            disableddash=de.dashDisabled),
            # Width
            **tkcanvas_width(width=de.width,
                             activewidth=de.widthActive,
                             disabledwidth=de.widthDisabled),
            # Colours
            **tkcanvas_colors(de.color,
                              active=de.colorActive,
                              disabled=de.colorDisabled)
        )

    @render.register
    def render_Ellipse(self, de: diagram.Ellipse, *, extratags: typing.Sequence[str] = tuple()) -> int:
        assert all(t not in de.tags for t in extratags)  # Do not alias "real" tags
        return self.cv.create_oval(
            de.topleft.tuple, de.botright.tuple,
            tags=(*de.tags, *extratags),
            # Dash
            **tkcanvas_dash(dash=de.dash,
                            activedash=de.dashActive,
                            disableddash=de.dashDisabled),
            # Width
            **tkcanvas_width(width=de.width,
                             activewidth=de.widthActive,
                             disabledwidth=de.widthDisabled),
            # Colours
            **tkcanvas_colors(de.color,
                              active=de.colorActive,
                              disabled=de.colorDisabled)
        )

    @render.register
    def render_Text(self, de: diagram.Text, *, extratags: typing.Sequence[str] = tuple()) -> int:
        assert all(t not in de.tags for t in extratags)  # Do not alias "real" tags
        # Type Checking: `angle` is missing
        #                See https://github.com/python/typeshed/pull/10404
        return self.cv.create_text(
            list(de.point.tuple), text=de.text,
            tags=(*de.tags, *extratags),
            # # Alignment
            anchor=de.anchor.value, justify=de.justify.value,
            **tkcanvas_text_angle(de.angle),
            # Font Configuration
            font=de.font,
            # Colours
            **tkcanvas_colors(de.color, TKCANVAS_COLORMAP_TEXT,
                              active=de.colorActive,
                              disabled=de.colorDisabled)
        )
