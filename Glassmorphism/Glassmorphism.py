#MIT License
#
#Copyright (c) 2022 GvozdevLeonid
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.


try:
    from PySide6 import (
        QtWidgets,
        QtCore,
        QtGui
    )
except ImportError:
    try:
        from PySide2 import (
            QtWidgets,
            QtCore,
            QtGui
        )
    except ImportError:
        try:
            from PyQt6 import (
                QtWidgets,
                QtCore,
                QtGui
            )
        except ImportError:
            try:
                from PyQt5 import (
                    QtWidgets,
                    QtCore,
                    QtGui
                )
            except ImportError:
                pass
import math


class BackDrop(QtWidgets.QGraphicsEffect):
    def __init__(self, blur: int = 0, radius: int = 0,
                 backgrounds: list[dict] = None):
        QtWidgets.QGraphicsEffect.__init__(self)
        self._blur = blur
        self._radius = radius
        self._backgrounds = backgrounds

        self._size = QtCore.QSize(0, 0)

        self._animation_pixmap = None
        self._forward_animation = False
        self._animation_position = QtCore.QPointF(0, 0)
        self._animation = QtCore.QPropertyAnimation(self,
                                                    b"animation_position")

        self._check_backgrounds()
    try:
        @QtCore.Property(QtCore.QPointF)
        def animation_position(self):
            return self._animation_position
    except AttributeError:
        @QtCore.pyqtProperty(QtCore.QPointF)
        def animation_position(self):
            return self._animation_position

    @animation_position.setter
    def animation_position(self, value: QtCore.QPointF):
        self._animation_position = value
        self.update()

    @staticmethod
    def _blur_pixmap(src, blur_radius):
        w, h = src.width(), src.height()

        effect = QtWidgets.QGraphicsBlurEffect(blurRadius=blur_radius)

        scene = QtWidgets.QGraphicsScene()
        item = QtWidgets.QGraphicsPixmapItem()
        item.setPixmap(QtGui.QPixmap(src))
        item.setGraphicsEffect(effect)
        scene.addItem(item)

        res = QtGui.QImage(QtCore.QSize(w, h),
                           QtGui.QImage.Format.Format_ARGB32)
        res.fill(QtCore.Qt.GlobalColor.transparent)

        ptr = QtGui.QPainter(res)
        ptr.setRenderHints(QtGui.QPainter.RenderHint.Antialiasing |
                           QtGui.QPainter.RenderHint.SmoothPixmapTransform)
        scene.render(ptr, QtCore.QRectF(), QtCore.QRectF(0, 0, w, h))
        ptr.end()

        return QtGui.QPixmap(res)

    @staticmethod
    def _cut_pixmap(pixmap, mask, width, height):
        painter = QtGui.QPainter(pixmap)
        painter.setTransform(QtGui.QTransform())
        painter.setRenderHints(QtGui.QPainter.RenderHint.Antialiasing |
                               QtGui.QPainter.RenderHint.SmoothPixmapTransform)
        painter.setCompositionMode(
                QtGui.QPainter.CompositionMode.CompositionMode_DestinationIn)
        painter.drawPixmap(0, 0, width, height, mask)
        painter.end()

    @staticmethod
    def _get_colored_pixmap(brush_color, pen_color,
                            pen_width, width, height, radius):
        pixmap = QtGui.QPixmap(width, height)
        pixmap.fill(QtCore.Qt.GlobalColor.transparent)
        painter = QtGui.QPainter(pixmap)
        painter.setRenderHints(QtGui.QPainter.RenderHint.Antialiasing |
                               QtGui.QPainter.RenderHint.SmoothPixmapTransform)
        painter.setBrush(brush_color)
        painter.setPen(QtGui.QPen(pen_color, pen_width))
        painter.drawRoundedRect(QtCore.QRectF(0.0, 0.0, width, height),
                                radius, radius)
        painter.end()

        return pixmap

    def _get_blur_background(self, source):
        source_rect = self.boundingRectFor(
                self.sourceBoundingRect(
                        QtCore.Qt.CoordinateSystem.DeviceCoordinates)).toRect()
        x, y, w, h = source_rect.getRect()
        scale = int(source.devicePixelRatioF())

        background_expanded = source.copy(x * scale - self._blur,
                                          y * scale - self._blur,
                                          w * scale + self._blur * 2,
                                          h * scale + self._blur * 2)

        blurred_background_expanded = self._blur_pixmap(background_expanded,
                                                        self._blur)

        blurred_background = blurred_background_expanded.copy(self._blur // 2,
                                                              self._blur // 2,
                                                              w, h)

        return blurred_background

    def _check_backgrounds(self):
        for bg in self._backgrounds:
            if "background-color" not in bg.keys():
                bg["background-color"] = QtGui.QColor(255, 255, 255, 0)
            if "border" not in bg.keys():
                bg["border"] = QtGui.QColor(255, 255, 255, 0)
            if "border-width" not in bg.keys():
                bg["border-width"] = 1
            if "opacity" not in bg.keys():
                bg["opacity"] = 0

    def _create_animation_pixmap(self, angle: int, line_width: int,
                                 color: QtGui.QColor):

        height = self._size.height()
        diagonal = height / math.sin(math.radians(angle))
        width = int(math.sqrt(diagonal ** 2 - height ** 2))
        offset = int(math.sqrt(line_width ** 2 + line_width ** 2))

        if angle in (0, 180):
            width = self._size.height()
            start_pos = QtCore.QPointF(0, height)
            end_pos = QtCore.QPointF(width * 2 + offset * 2, height)
        elif angle == 90:
            width = line_width
            start_pos = QtCore.QPointF(width + offset, 0)
            end_pos = QtCore.QPointF(width + offset, height * 2)
        else:
            if angle < 90:
                start_pos = QtCore.QPointF(offset, height * 2)
                end_pos = QtCore.QPointF(width * 2 + offset, 0)
            else:
                start_pos = QtCore.QPointF(offset, 0)
                end_pos = QtCore.QPointF(width * 2 + offset, height * 2)

        self._animation_pixmap = QtGui.QPixmap(width * 2 + offset * 2,
                                               height * 2)
        self._animation_pixmap.fill(QtCore.Qt.GlobalColor.transparent)

        painter = QtGui.QPainter(self._animation_pixmap)
        painter.setRenderHints(QtGui.QPainter.RenderHint.Antialiasing |
                               QtGui.QPainter.RenderHint.SmoothPixmapTransform)
        painter.setPen(QtGui.QPen(color, line_width * 2))
        painter.drawLine(start_pos, end_pos)
        painter.end()

    def draw(self, painter):

        painter.setRenderHints(QtGui.QPainter.RenderHint.Antialiasing |
                               QtGui.QPainter.RenderHint.SmoothPixmapTransform)
        restoreTransform = painter.worldTransform()

        source_rect = self.boundingRectFor(self.sourceBoundingRect(
                QtCore.Qt.CoordinateSystem.DeviceCoordinates)).toRect()
        x, y, w, h = source_rect.getRect()

        source = self.sourcePixmap(QtCore.Qt.CoordinateSystem.DeviceCoordinates)
        if isinstance(source, tuple):
            source = source[0]
        scale = int(source.devicePixelRatioF())

        if self._size.width() != w or self._size.height() != h:
            self._size = QtCore.QSize(w, h)

        main_background = self._get_blur_background(painter.device())

        painter.setTransform(QtGui.QTransform())
        painter.setPen(QtCore.Qt.PenStyle.NoPen)

        mask = self._get_colored_pixmap(QtGui.QColor("#FFFFFF"),
                                        QtGui.QColor("#FFFFFF"),
                                        1, w * scale, h * scale,
                                        self._radius * scale)

        self._cut_pixmap(main_background, mask, w, h)

        backgrounds = []
        for i, bg in enumerate(self._backgrounds):
            background = bg["opacity"], self._get_colored_pixmap(
                    bg["background-color"],
                    bg["border"],
                    bg["border-width"] * scale,
                    w * scale, h * scale
                    , self._radius * scale)
            self._cut_pixmap(background[1], mask, w * 2, h * 2)
            backgrounds.append(background)

        self._cut_pixmap(source, mask, w, h)

        painter.drawPixmap(x, y, w, h, main_background)

        for bg in backgrounds:
            painter.setOpacity(bg[0])
            painter.drawPixmap(x, y, w, h, bg[1])

        painter.setOpacity(1)
        painter.drawPixmap(x, y, source)

        if self._animation.state() == QtCore.QPropertyAnimation.State.Running:
            pixmap = QtGui.QPixmap(w, h)
            pixmap.fill(QtCore.Qt.GlobalColor.transparent)
            pixmap_painter = QtGui.QPainter(pixmap)
            pixmap_painter.setRenderHints(
                    QtGui.QPainter.RenderHint.Antialiasing |
                    QtGui.QPainter.RenderHint.SmoothPixmapTransform)
            pixmap_painter.drawPixmap(int(self._animation_position.x()),
                                      int(self._animation_position.y()),
                                      self._animation_pixmap.width() // 2,
                                      self._animation_pixmap.height() // 2,
                                      self._animation_pixmap)
            pixmap_painter.end()
            self._cut_pixmap(pixmap, mask, w, h)
            painter.drawPixmap(x, y, w, h, pixmap)

        painter.setWorldTransform(restoreTransform)
        painter.end()

    def shine_animation(self, duration: int = 300, forward: bool = True,
                         angle: int = 135, width: int = 40,
                  color: QtGui.QColor = QtGui.QColor(255, 255, 255, 125)):
        if self._animation.state() != QtCore.QPropertyAnimation.State.Running:
            self._create_animation_pixmap(angle, width, color)
            if forward:
                start_point = QtCore.QPointF(
                        -self._animation_pixmap.width() / 2, 0)
                end_point = QtCore.QPointF(self._size.width(), 0)
            else:
                start_point = QtCore.QPointF(self._size.width(), 0)
                end_point = QtCore.QPointF(
                        -self._animation_pixmap.width() / 2, 0)

            if forward:
                self._forward_animation = True
            else:
                self._forward_animation = False

            self._animation.setStartValue(start_point)
            self._animation.setEndValue(end_point)
            self._animation.setDuration(duration)
            self._animation.start()

        elif self._animation.state() == \
                QtCore.QPropertyAnimation.State.Running and \
                not self._forward_animation:
            self._forward_animation = False

            self._animation.stop()
            end_point = QtCore.QPointF(self._size.width(), 0)
            self._animation.setStartValue(self._animation_position)
            self._animation.setEndValue(end_point)
            self._animation.setDuration(
                    duration - self._animation.currentTime())
            self._animation.start()

        elif self._animation.state() == \
                QtCore.QPropertyAnimation.State.Running and\
                self._forward_animation:
            self._forward_animation = False

            self._animation.stop()
            end_point = QtCore.QPointF(-self._animation_pixmap.width() / 2, 0)
            self._animation.setStartValue(self._animation_position)
            self._animation.setEndValue(end_point)
            self._animation.setDuration(
                    duration - self._animation.currentTime())
            self._animation.start()


class BackDropWrapper(QtWidgets.QWidget):
    def __init__(self, widget, blur: int = 0, radius: int = 0,
                 backgrounds: list[dict] = None, shine_animation: list = None,
                 move_animation: tuple = None):
        QtWidgets.QWidget.__init__(self)
        self._widget = widget

        self.mLayout = QtWidgets.QVBoxLayout()
        self.mLayout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.mLayout)
        self.mLayout.addWidget(self._widget)

        self.boxShadow = BackDrop(blur, radius, backgrounds)
        self.setGraphicsEffect(self.boxShadow)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_Hover)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_NoMousePropagation)

        self._animation = QtCore.QPropertyAnimation(self, b"pos")
        self._normal_pos = None
        self._forward_animation = False

        self._shine_animation_info = None
        self._move_animation_info = None

        if shine_animation is not None:
            self.enable_shine_animation(shine_animation=shine_animation)
        if move_animation is not None:
            self.enable_move_animation(move_animation=move_animation)

    def enable_shine_animation(self, duration: int = 300, forward: bool = True,
                               angle: int = 135, width: int = 40,
                               color: QtGui.QColor = QtGui.QColor(255, 255,
                                                                  255, 125),
                               shine_animation: tuple = None):
        if shine_animation is None:
            self._shine_animation_info = (duration, forward,
                                          angle, width, color)
        else:
            self._shine_animation_info = shine_animation

    def enable_move_animation(self, duration: int = 300,
                              offset: tuple = (0, 0),
                              forward: bool = True,
                              move_animation: tuple = None):
        if move_animation is None:
            self._move_animation_info = (duration, offset, forward)
        else:
            self._move_animation_info = move_animation

    def event(self, event: QtCore.QEvent) -> bool:
        if event.type() == QtGui.QHideEvent.Type.HoverEnter:
            if self._shine_animation_info is not None:
                duration, forward, angle, width, color = \
                    self._shine_animation_info
                self.boxShadow.shine_animation(duration, forward,
                                                angle, width, color)

            if self._move_animation_info is not None:
                duration, offset, forward = self._move_animation_info
                self._move_animation(duration, offset, forward)
            return True
        if event.type() == QtGui.QHideEvent.Type.HoverLeave:
            if self._shine_animation_info is not None:
                duration, forward, angle, width, color = \
                    self._shine_animation_info
                self.boxShadow.shine_animation(duration, not forward,
                                                angle, width, color)

            if self._move_animation_info is not None:
                duration, offset, forward = self._move_animation_info
                self._move_animation(duration, offset, not forward)
            return True
        return False

    def _move_animation(self, duration: int = 300, offset: tuple = (0, 0),
                        forward: bool = True):
        if self._normal_pos is None:
            self._normal_pos = self.property("pos")

        if self._animation.state() != QtCore.QPropertyAnimation.State.Running:
            if forward:
                self._normal_pos = self.property("pos")
                self._forward_animation = True
                end_pos = QtCore.QPointF(self.property("pos").x() + offset[0],
                                         self.property("pos").y() + offset[1])
            else:
                self._forward_animation = False
                end_pos = self._normal_pos

            self._animation.setStartValue(self.property("pos"))
            self._animation.setEndValue(end_pos)
            self._animation.setDuration(duration)
            self._animation.start()

        elif self._animation.state() == \
                QtCore.QPropertyAnimation.State.Running and \
                not self._forward_animation:

            self._forward_animation = True
            end_pos = QtCore.QPointF(self._normal_pos.x() + offset[0],
                                     self._normal_pos.y() + offset[1])

            self._animation.stop()
            self._animation.setStartValue(self._animation.currentValue())
            self._animation.setEndValue(end_pos)
            self._animation.setDuration(
                    duration - self._animation.currentTime())
            self._animation.start()

        elif self._animation.state() == \
                QtCore.QPropertyAnimation.State.Running \
                and self._forward_animation:
            self._forward_animation = False

            self._animation.stop()
            self._animation.setStartValue(self._animation.currentValue())
            self._animation.setEndValue(self._normal_pos)
            self._animation.setDuration(
                    duration - self._animation.currentTime())
            self._animation.start()
