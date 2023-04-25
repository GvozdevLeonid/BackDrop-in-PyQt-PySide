# BackDrop effect in PySide6

So far this is working on Pyside6 and possibly PySide2 as well. Does not work on PyQt6, I will fix the error in the future

This repository contains two classes: BackDrop is a graphical effect in which you need to set a list of backgrounds, blur and a border radius. BackDropWrapper - a handy wrapper for displaying and animation the backdrop effect.

	BackDrop(blur: int = 0, radius: int = 0, backgrounds: list[dict] = None)
	BackDropWrapper(widget: QtWidgets.QObject , blur: int = 0, radius: int = 0, backgrounds: list[dict] = None, shine_animation: list = None, move_animation: tuple = None)
The backgrounds is set as follows:

	grad = QtGui.QLinearGradient(0, 0, 1, 1)
	grad.setCoordinateMode(QtGui.QLinearGradient.CoordinateMode.ObjectMode)
	grad.setStops([(0, QtGui.QColor(255, 255, 255, 255)), (0.35, QtGui.QColor(255, 255, 255, 125)), (0.65, QtGui.QColor(255, 255, 255, 125)), (1,QtGui.QColor(255, 255, 255, 255))])
	backgrounds=[{"background-color": grad, "border": QtGui.QColor("#FFFFFF"),"border-width": 2, "opacity": .4}]

Animations run when you hover over the widget and also run in reverse again when you leave the mouse.
All animations are disabled by default, but you can enable them by passing the following arguments:

	shine_animation = (duration: int, forward: bool, angle: int, width: int, color: QtGui.QColor)
	move_animation = (duration: int, offset: tuple, forward: bool)
	
or you can create BackDropWrapper element and set:
		
	bdw = BackDropWrapper(QtWidgets.QLabel("Hello World!"), blur=10, radius=25, backgrounds=backgrounds)
	bdw.enable_shine_animation(color=QtGui.QColor(255, 255, 255, 90))
	bdw.enable_move_animation(offset=(0, -30))

# Example file preview

<img width="710" alt="normal" src="https://user-images.githubusercontent.com/87101242/209816702-e57d5f4b-f15d-41d1-9761-4d13c4414484.png">
<img width="711" alt="hovered" src="https://user-images.githubusercontent.com/87101242/209816709-4d53ed29-7fba-49f0-900e-9113a2bc2898.png">

![animation](https://user-images.githubusercontent.com/87101242/209816714-2ab1e36e-94c6-4a59-a92d-0a73fc1b1939.gif)
