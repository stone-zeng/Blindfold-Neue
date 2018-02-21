# encoding: utf-8

###########################################################################################################
#
#
#	Reporter Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Reporter
#
#
###########################################################################################################

from GlyphsApp.plugins import *
import math


class BlindFold(ReporterPlugin):

	def settings(self):
		self.name = 'Blindfold'
		self.thisMenuTitle = {"name": u"%s:" % self.name, "action": None }
		self.toggleNames = [u"x-Height", u"Cap-Height"]
		self.toggleShadeNames = [u"White", u"Black"]
		self.generalContextMenus = [
			self.thisMenuTitle,
			{"name": u"%s" % self.toggleNames[0], "action": self.toggleHeight },
			#{"name": u"%s" % self.toggleShadeNames[0], "action": self.toggleShade },
		]

		# self.menuName = Glyphs.localize({'en': u'* Blindfold 🙈', 'de': u'* Blindfold 🙈'})
		self.menuName = Glyphs.localize({'en': u'Blindfold'})
		self.showXHeight = True
		self.paintBlack = True

	def toggleHeight(self):
		switch = bool(self.showXHeight)
		self.generalContextMenus = [
			self.thisMenuTitle,
			{"name": u"%s" % self.toggleNames[switch], "action": self.toggleHeight },
			#{"name": u"%s" % self.toggleShadeNames[self.getIntValue(self.paintBlack)], "action": self.toggleShade },
		]
		self.showXHeight = not self.showXHeight
		self.RefreshView()

	def toggleShade(self):
		switch = bool(self.paintBlack)
		self.generalContextMenus = [
			self.thisMenuTitle,
			{"name": u"%s" % self.toggleNames[self.getIntValue(self.showXHeight)], "action": self.toggleHeight },
			#{"name": u"%s" % self.toggleShadeNames[switch], "action": self.toggleShade },
		]
		self.paintBlack = not self.paintBlack
		self.RefreshView()


	def getIntValue(self, boolVar):
		if boolVar is not True:
			return 1
		else:
			return 0


	def foreground(self, layer): # def background(self, layer):
		self.drawRect(layer, self.getScale())

	def inactiveLayers(self, layer):
		self.drawRect(layer, self.getScale())
	
	def preview(self, layer):
		pass
	
	# Keep original drawing for inactive layers:
	def needsExtraMainOutlineDrawingForInactiveLayer_(self, Layer):
		return True

	def drawRect(self, layer, scale):
		view = self.controller.graphicView()
		Visible = view.visibleRect()
		activePosition = view.activePosition()

		UcLcCompensator = -600 / scale # avoid weird gap when a line starts with an UC and LC follow
		relativePosition = NSMakePoint(math.floor((Visible.origin.x - activePosition.x) / scale), math.floor((NSMinY(Visible) - activePosition.y + Visible.size.height) / scale))

		moreBlack = 70  # Optional: Additional Buffer to top and bottom

		try:
			if self.paintBlack is True:
				NSColor.blackColor().set()
			else:
				NSColor.whiteColor().set()
			
			'''	Rect 1: Descender '''
			y = layer.glyphMetrics()[3] - moreBlack  # descender
			height = (y * -1) + 1 # +1 closes the tiny gap
			NSBezierPath.fillRect_( ( (relativePosition[0] + UcLcCompensator, y), ( ( math.floor((Visible.size.width - UcLcCompensator + activePosition.x) / scale) , height ) ) ) )
			
			''' Rect 2: Ascender '''
			# if self.sliderMenuView.group.PUButton.getTitle() == "Cap-Height":
			# if self.sliderMenuView.group.PUButton.get() == 1:
			if self.showXHeight:
				y = layer.glyphMetrics()[2] # capHeight
			# if self.sliderMenuView.group.PUButton.getTitle() == "x-Height":
			else:
				y = layer.glyphMetrics()[4] # xHeight
			
			height = layer.glyphMetrics()[1] + moreBlack - y + moreBlack # ascender - y			
			NSBezierPath.fillRect_( ( (relativePosition[0] + UcLcCompensator, y), ( ( math.floor((Visible.size.width - UcLcCompensator + activePosition.x) / scale) , height ) ) ) )
		except: pass
	
	def RefreshView(self):
		try:
			Glyphs = NSApplication.sharedApplication()
			currentTabView = Glyphs.font.currentTab
			if currentTabView:
				currentTabView.graphicView().setNeedsDisplay_(True)
		except:
			pass

