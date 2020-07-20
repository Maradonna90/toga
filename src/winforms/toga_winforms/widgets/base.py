from toga_winforms.libs import Point, Size


class Widget:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

        self._container = None
        self.native = None
        # `winforms_event_handlers` is used to keep track of added
        # native event handlers to remove them when a widget is removed
        self.winforms_event_handlers = []
        self.create()
        self.interface.style.reapply()

    def set_app(self, app):
        pass

    def set_window(self, window):
        pass

    @property
    def container(self):
        return self._container

    @container.setter
    def container(self, container):
        if self.container:
            if container:
                raise RuntimeError('Already have a container')
            else:
                # container is set to None, removing self from the container.native
                self._container.native.Controls.Remove(self.native)
                self._container = None
        elif container:
            # setting container, adding self to container.native
            self._container = container
            self._container.native.Controls.Add(self.native)
            self.native.BringToFront()

        for child in self.interface.children:
            child._impl.container = container

        self.rehint()

    def set_enabled(self, value):
        if self.native:
            self.native.Enabled = self.interface.enabled

    # APPLICATOR

    @property
    def vertical_shift(self):
        return 0

    def set_bounds(self, x, y, width, height):
        if self.native:
            # Root level widgets may require vertical adjustment to
            # account for toolbars, etc.
            if self.interface.parent is None:
                vertical_shift = self.frame.vertical_shift
            else:
                vertical_shift = 0

            self.native.Size = Size(width, height)
            self.native.Location = Point(x, y + vertical_shift)

    def set_alignment(self, alignment):
        # By default, alignment can't be changed
        pass

    def set_hidden(self, hidden):
        if self.native:
            self.native.Visible = not hidden

    def set_font(self, font):
        # By default, font can't be changed
        pass

    def set_color(self, color):
        # By default, color can't be changed
        pass

    def set_background_color(self, color):
        # By default, background color can't be changed.
        pass

    def winforms_remove_event_handlers(self):
        for handler in self.winforms_event_handlers:
            handler['event'] -= handler['handler']

    # INTERFACE

    def add_child(self, child):
        if self.container:
            child.container = self.container

    def delete_child(self, child):
        child.winforms_remove_event_handlers()
        self.native.Controls.Remove(child.native)
        child.native.Dispose()

    def remove_child(self, child):
        child.container = None

    def rehint(self):
        pass
