"""
Drag drop designer for the studio
"""

# ======================================================================= #
# Copyright (C) 2019 Hoverset Group.                                      #
# ======================================================================= #
import os.path
import time
from tkinter import filedialog, ttk

from hoverset.data import actions
from hoverset.data.keymap import KeyMap
from hoverset.data.images import get_tk_image
from hoverset.ui.widgets import Label, Text, FontStyle, Checkbutton, CompoundList
from hoverset.ui.dialogs import MessageDialog
from hoverset.ui.icons import get_icon_image as icon
from hoverset.ui.menu import MenuUtils, LoadLater, EnableIf
from hoverset.util.execution import Action, as_thread

from studio.lib import NameGenerator
from studio.lib.layouts import PlaceLayoutStrategy
from studio.lib.pseudo import PseudoWidget, Container, Groups
from studio.parsers.loader import DesignBuilder, BaseStudioAdapter
from studio.ui import geometry
from studio.ui.highlight import HighLight
from studio.ui.widgets import DesignPad, CoordinateIndicator
from studio.context import BaseContext
from studio import __version__

from formation.formats import get_file_types


class DesignLayoutStrategy(PlaceLayoutStrategy):
    name = "DesignLayout"

    def add_new(self, widget, x, y):
        self.container.add(widget, x, y, layout=self.container)

    def _move(self, widget, bounds):
        self.container.position(widget, self.container.canvas_bounds(bounds))

    def add_widget(self, widget, bounds=None, **kwargs):
        super(PlaceLayoutStrategy, self).add_widget(widget, bounds=None, **kwargs)
        super(PlaceLayoutStrategy, self).remove_widget(widget)
        if bounds is None:
            x = kwargs.get("x", 10)
            y = kwargs.get("y", 10)
            width = kwargs.get("width", 20)
            height = kwargs.get("height", 20)
            self.container.place_child(widget, x=x, y=y, width=width, height=height)
        else:
            x1, y1, x2, y2 = self.container.canvas_bounds(bounds)
            self.container.place_child(widget, x=x1, y=y1, width=x2 - x1, height=y2 - y1)
        self.children.append(widget)

    def remove_widget(self, widget):
        super().remove_widget(widget)
        self.container.forget_child(widget)

    def apply(self, prop, value, widget):
        if value == '':
            return
        self.container.config_child(widget, **{prop: value})

    def restore_widget(self, widget, data=None):
        data = widget.recent_layout_info if data is None else data
        self.children.append(widget)
        widget.layout = self.container
        widget.level = self.level + 1
        self.container.place_child(widget, **data.get("info", {}))

    def get_restore(self, widget):
        return {
            "info": self.container.config_child(widget),
            "container": self,
        }

    def get_def(self, widget):
        definition = dict(self.DEFINITION)
        # We don't need bordermode
        definition.pop("bordermode")
        return definition

    def info(self, widget):
        bounds = self.container.bbox(widget)
        width, height = geometry.dimensions(bounds)
        return {
            "x": bounds[0],
            "y": bounds[1],
            "width": width,
            "height": height,
        }


class Designer(DesignPad, Container):
    MOVE = 0x2
    RESIZE = 0x3
    WIDGET_INIT_PADDING = 20
    WIDGET_INIT_HEIGHT = 25
    name = "Designer"
    pane = None
    _coord_indicator = None

    def __init__(self, master, studio):
        super().__init__(master)
        self.id = None
        self.context = master
        self.studio = studio
        self.name_generator = NameGenerator(self.studio.pref)
        self.setup_widget()
        self.parent = self
        self.config(**self.style.bright, takefocus=True)
        self.objects = []
        self.root_obj = None
        self.layout_strategy = DesignLayoutStrategy(self)
        self.highlight = HighLight(self)
        self.highlight.on_resize(self._on_size_changed)
        self.highlight.on_move(self._on_move)
        self.highlight.on_release(self._on_release)
        self.highlight.on_start(self._on_start)
        self._update_throttling()
        self.studio.pref.add_listener(
            "designer::frame_skip",
            self._update_throttling
        )
        self.current_obj = None
        self.current_container = None
        self.current_action = None
        self._displace_active = False
        self._last_displace = time.time()
        self._frame.bind("<Button-1>", lambda _: self.focus_set(), '+')
        self._frame.bind("<Button-1>", self.set_pos, '+')
        self._frame.bind('<Motion>', self.on_motion, '+')
        self._frame.bind('<KeyRelease>', self._stop_displace, '+')
        self._padding = 30
        self.design_path = None
        self.builder = DesignBuilder(self)
        self._shortcut_mgr = KeyMap(self._frame)
        self._set_shortcuts()
        self._last_click_pos = None

        self._empty = Label(
            self,
            image=get_tk_image("paint", 30, 30), compound="top", text=" ",
            **self.style.text_passive
        )
        self._empty.config(**self.style.bright)
        self._show_empty(True)

        # create the dynamic menu
        self._context_menu = MenuUtils.make_dynamic(
            self.studio.menu_template +
            (LoadLater(self.studio.tool_manager.get_tool_menu), ) +
            (LoadLater(lambda: self.current_obj.create_menu() if self.current_obj else ()),),
            self.studio,
            self.style
        )
        design_menu = (
            EnableIf(
                lambda: self.studio._clipboard is not None,
                ("command", "paste", icon("clipboard", 14, 14),
                 lambda: self.paste(self.studio._clipboard, paste_to=self), {})
            ),)
        self.set_up_context(design_menu)
        self._empty.set_up_context(design_menu)
        if Designer._coord_indicator is None:
            Designer._coord_indicator = self.studio.install_status_widget(CoordinateIndicator)
        self._text_editor = Text(self, wrap='none')
        self._text_editor.on_change(self._text_change)
        self._text_editor.bind("<FocusOut>", self._text_hide)
        self._base_font = FontStyle()

    def _get_designer(self):
        return self

    def focus_set(self):
        self._frame.focus_force()

    def set_pos(self, event):
        # store the click position for effective widget pasting
        self._last_click_pos = event.x_root, event.y_root

    def _update_throttling(self, *_):
        self.highlight.set_skip_max(self.studio.pref.get("designer::frame_skip"))

    def _show_empty(self, flag, **kw):
        if flag:
            kw['image'] = kw.get('image', get_tk_image('paint', 30, 30))
            kw['text'] = kw.get('text', "Drag or paste a container here to start")
            self._empty.configure(**kw, wraplength=max(400, self.width))
            self._empty.place(relwidth=1, relheight=1)
        else:
            self._empty.place_forget()

    def _set_shortcuts(self):
        shortcut_mgr = self._shortcut_mgr
        shortcut_mgr.bind()
        shortcut_mgr.add_routines(
            actions.get('STUDIO_COPY'),
            actions.get('STUDIO_CUT'),
            actions.get('STUDIO_DELETE'),
            actions.get('STUDIO_PASTE'),
            actions.get('STUDIO_DUPLICATE'),
        )
        # allow control of widget position using arrow keys
        shortcut_mgr.add_shortcut(
            (lambda: self.displace('right'), KeyMap.RIGHT),
            (lambda: self.displace('left'), KeyMap.LEFT),
            (lambda: self.displace('up'), KeyMap.UP),
            (lambda: self.displace('down'), KeyMap.DOWN),
        )

    def _open_default(self):
        self.update_idletasks()
        from studio.lib import legacy
        width = max(self.width - self._padding * 2, 300)
        height = max(self.height - self._padding * 2, 300)
        self.add(
            legacy.Tk, self._padding, self._padding,
            width=width, height=height
        )
        self.builder.generate()
        self.design_path = None

    @property
    def _ids(self):
        return [i.id for i in self.objects]

    def has_changed(self):
        # check if design has changed since last save or loading so we can prompt user to save changes
        builder = self.builder
        if self.root_obj:
            builder = DesignBuilder(self)
            builder.generate()
        return builder != self.builder

    def open_new(self):
        # open a blank design
        self.open_file(None)

    def to_tree(self):
        """ Generate node form of current design state without needing to save"""
        builder = DesignBuilder(self)
        builder.generate()
        return builder.root

    def save_prompt(self):
        return MessageDialog.builder(
            {"text": "Save", "value": True, "focus": True},
            {"text": "Don't save", "value": False},
            {"text": "Cancel", "value": None},
            wait=True,
            title="Save design",
            message=f"Design file \"{self.context.name}\" has unsaved changes. Do you want to save them?",
            parent=self.studio,
            icon=MessageDialog.ICON_INFO
        )

    def open_file(self, path=None):
        if self.has_changed():
            save = self.save_prompt()
            if save:
                # user opted to save
                saved_to = self.save()
                if saved_to is None:
                    # User did not complete saving and opted to cancel
                    return
            elif save is None:
                # user made no choice or basically selected cancel
                return
        if path:
            self.builder = DesignBuilder(self)
            progress = MessageDialog.show_progress(
                mode=MessageDialog.INDETERMINATE,
                message='Loading design file to studio...',
                parent=self.studio
            )
            self._load_design(path, progress)
        else:
            # if no path is supplied the default behaviour is to open a blank design
            self._open_default()

    def clear(self):
        # Warning: this method deletes elements irreversibly
        # remove the current root objects and their descendants
        self.studio.select(None)
        # create a copy since self.objects will mostly change during iteration
        # remove root and dangling objects
        for widget in self.objects:
            widget.destroy()
        self.objects.clear()
        self.root_obj = None

    def _verify_version(self):
        if self.builder.metadata.get("version"):
            _, major, __ = __version__.split(".")
            if major < self.builder.metadata["version"].get("major", 0):
                MessageDialog.show_warning(
                    parent=self.studio,
                    message=(
                        "Design was made using a higher version of the studio. \n"
                        "Some features may not be supported on this version. \n"
                        "Update to a new version of Formation for proper handling. \n"
                        "Note that saving may irreversibly strip off any unsupported features"
                    )
                )

    @as_thread
    def _load_design(self, path, progress=None):
        # Loading designs is elaborate so better do it on its own thread
        # Capture any errors that occur while loading
        # This helps the user single out syntax errors and other value errors
        try:
            self.design_path = path
            self.root_obj = self.builder.load(path, self)
            self.context.on_load_complete()
        except Exception as e:
            self.clear()
            self.studio.on_session_clear(self)
            accelerator = actions.get_routine("STUDIO_RELOAD").accelerator
            text = f"{str(e)}\nPress {accelerator} to reload" if accelerator else f"{str(e)} \n reload design"
            self._show_empty(True, text=text, image=get_tk_image("dialog_error", 50, 50))
            # MessageDialog.show_error(parent=self.studio, title='Error loading design', message=str(e))
        finally:
            if progress:
                progress.destroy()
            self._verify_version()

    def reload(self, *_):
        if not self.design_path or self.studio.context != self.context:
            return
        if self.has_changed():
            okay = MessageDialog.ask_okay_cancel(
                title="Confirm reload",
                message="All changes made will be lost",
                parent=self.studio
            )
            if not okay:
                # user made no choice or basically selected cancel
                return
        self.clear()
        self.studio.on_session_clear(self)
        self.open_file(self.design_path)

    def save(self, new_path=False):
        if not self.design_path or new_path:
            path = filedialog.asksaveasfilename(parent=self, filetypes=get_file_types(),
                                                defaultextension='.xml')
            if not path:
                return None
            self.design_path = path
        self.builder.write(self.design_path)
        return self.design_path

    def as_node(self, widget):
        builder = self.builder
        if builder is None:
            builder = DesignBuilder(self)
        return builder.to_tree(widget)

    def paste(self, node, silently=False, paste_to=None):
        if paste_to is None:
            paste_to = self.current_obj
        if paste_to is None:
            return
        obj_class = BaseStudioAdapter._get_class(node)
        if obj_class.is_toplevel and paste_to != self:
            self._show_toplevel_warning()
            return
        if obj_class.group != Groups.container and self.root_obj is None:
            self._show_root_widget_warning()
            return

        layout = paste_to if isinstance(paste_to, Container) else paste_to.layout
        width = int(node["layout"].get("width", 10))
        height = int(node["layout"].get("height", 10))
        x, y = self._last_click_pos or (self.winfo_rootx() + 50, self.winfo_rooty() + 50)
        self._last_click_pos = x + 5, y + 5  # slightly displace click position so multiple pastes are still visible
        bounds = geometry.resolve_bounds((x, y, x + width, y + height), self)
        obj = self.builder.load_section(node, layout, bounds)
        restore_point = layout.get_restore(obj)
        # Create an undo redo point if add is not silent
        if not silently:
            self.studio.new_action(Action(
                # Delete silently to prevent adding the event to the undo/redo stack
                lambda _: self.delete(obj, True),
                lambda _: self.restore(obj, restore_point, obj.layout)
            ))
        return obj

    def _get_unique(self, obj_class):
        """
        Generate a unique id for widget belonging to a given class
        """
        return self.name_generator.generate(obj_class, self._ids)

    def on_motion(self, event):
        self.highlight.resize(event)
        geometry.make_event_relative(event, self)
        self._coord_indicator.set_coord(
            self._frame.canvasx(event.x),
            self._frame.canvasy(event.y)
        )

    def _attach(self, obj):
        # bind events for context menu and object selection
        # all widget additions call this method so clear empty message
        self._show_empty(False)
        MenuUtils.bind_all_context(obj, lambda e: self.show_menu(e, obj), add='+')
        obj.bind_all('<Shift-ButtonPress-1>', lambda e: self.highlight.set_function(self.highlight.move, e), add='+')
        obj.bind_all('<Motion>', self.on_motion, '+')
        obj.bind_all('<ButtonRelease>', self.highlight.clear_resize, '+')
        obj.bind_all('<KeyRelease>', self._stop_displace, '+')
        if "text" in obj.keys():
            obj.bind_all("<Double-Button-1>", lambda _: self._show_text_editor(obj))
        self.objects.append(obj)
        if self.root_obj is None:
            self.root_obj = obj
        obj.bind_all("<Button-1>", lambda e: self._handle_select(obj, e), add='+')
        # bind shortcuts
        self._shortcut_mgr.bind_widget(obj)

    def show_menu(self, event, obj=None):
        # select object generating the context menu event first
        if obj is not None:
            self.select(obj)
        MenuUtils.popup(event, self._context_menu)

    def _handle_select(self, obj, event):
        # store the click position for effective widget pasting
        self._last_click_pos = event.x_root, event.y_root
        self.select(obj)

    def load(self, obj_class, name, container, attributes, layout, bounds=None):
        obj = obj_class(self, name)
        obj.configure(**attributes)
        self._attach(obj)
        if bounds is not None:
            container.add_widget(obj, bounds)
        else:
            container.add_widget(obj, **layout)
        if container == self:
            container = None
        self.studio.add(obj, container)
        return obj

    def _show_root_widget_warning(self):
        MessageDialog.show_warning(title='Invalid root widget', parent=self.studio,
                                   message='Only containers are allowed as root widgets')

    def _show_toplevel_warning(self):
        MessageDialog.show_warning(
            title='Invalid parent',
            parent=self.studio,
            message='Toplevel widgets cannot be placed inside other widgets'
        )

    def add(self, obj_class: PseudoWidget.__class__, x, y, **kwargs):
        layout = kwargs.get("layout")
        if obj_class.is_toplevel and layout not in (self, None):
            self._show_toplevel_warning()
            return
        if obj_class.group != Groups.container and self.root_obj is None:
            # We only need a container as the root widget
            self._show_root_widget_warning()
            return
        silent = kwargs.get("silently", False)
        name = self._get_unique(obj_class)
        obj = obj_class(self, name)
        width, height = getattr(obj, "initial_dimensions", (
            self._base_font.measure(name) + self.WIDGET_INIT_PADDING,
            self.WIDGET_INIT_HEIGHT
        ))
        width = kwargs.get("width", width)
        height = kwargs.get("height", height)

        obj.layout = kwargs.get("intended_layout", None)
        self._attach(obj)  # apply extra bindings required
        # If the object has a layout which actually the layout at the point of creation prepare and pass it
        # to the layout
        if isinstance(layout, Container):
            bounds = (x, y, x + width, y + height)
            bounds = geometry.resolve_bounds(bounds, self)
            layout.add_widget(obj, bounds)
            self.studio.add(obj, layout)
            restore_point = layout.get_restore(obj)
            # Create an undo redo point if add is not silent
            if not silent:
                self.studio.new_action(Action(
                    # Delete silently to prevent adding the event to the undo/redo stack
                    lambda _: self.delete(obj, True),
                    lambda _: self.restore(obj, restore_point, obj.layout)
                ))
        elif obj.layout is None:
            # This only happens when adding the main layout. We dont need to add this action to the undo/redo stack
            # This main layout is attached directly to the designer
            obj.layout = self
            self.layout_strategy.add_widget(obj, x=x, y=y, width=width, height=height)
            self.studio.add(obj, None)

        return obj

    def select_layout(self, layout: Container):
        pass

    def restore(self, widget, restore_point, container):
        container.restore_widget(widget, restore_point)
        self.studio.on_restore(widget)
        self._replace_all(widget)

    def _replace_all(self, widget):
        # Recursively add widget and all its children to objects
        self.objects.append(widget)
        if self.root_obj is None:
            self.root_obj = widget
        if isinstance(widget, Container):
            for child in widget._children:
                self._replace_all(child)

    def delete(self, widget, silently=False):
        if not widget:
            return
        if not silently:
            restore_point = widget.layout.get_restore(widget)
            self.studio.new_action(Action(
                lambda _: self.restore(widget, restore_point, widget.layout),
                lambda _: self.studio.delete(widget, True)
            ))
        else:
            self.studio.delete(widget, self)
        widget.layout.remove_widget(widget)
        if widget == self.root_obj:
            # try finding another toplevel widget that can be a root obj otherwise leave it as none
            self.root_obj = None
            for w in self.layout_strategy.children:
                if isinstance(w, Container) or w.group == Groups.container:
                    self.root_obj = w
                    break
        self._uproot_widget(widget)
        if not self.objects:
            self._show_empty(True)

    def _uproot_widget(self, widget):
        # Recursively remove widgets and all its children
        if widget in self.objects:
            self.objects.remove(widget)
        if isinstance(widget, Container):
            for child in widget._children:
                self._uproot_widget(child)

    def set_active_container(self, container):
        if self.current_container is not None:
            self.current_container.clear_highlight()
        self.current_container = container

    def compute_overlap(self, bound1, bound2):
        return geometry.compute_overlap(bound1, bound2)

    def layout_at(self, bounds):
        for container in sorted(filter(lambda x: isinstance(x, Container) and x != self.current_obj, self.objects),
                                key=lambda x: len(self.objects) - x.level):
            if isinstance(self.current_obj, Container) and self.current_obj.level < container.level:
                continue
            if self.compute_overlap(geometry.bounds(container), bounds):
                return container
        return None

    def parse_bounds(self, bounds):
        return {
            "x": bounds[0],
            "y": bounds[1],
            "width": bounds[2] - bounds[0],
            "height": bounds[3] - bounds[1]
        }

    def position(self, widget, bounds):
        self.place_child(widget, **self.parse_bounds(bounds))

    def select(self, obj, explicit=False):
        if obj is None:
            self.clear_obj_highlight()
            self.studio.select(None, self)
            self.highlight.clear()
            return
        self.focus_set()
        if self.current_obj == obj:
            return
        self.clear_obj_highlight()
        self.current_obj = obj
        self.draw_highlight(obj)
        if not explicit:
            # The event is originating from the designer
            self.studio.select(obj, self)

    def draw_highlight(self, obj):
        self.highlight.surround(obj)

    def _stop_displace(self, _):
        if self._displace_active:
            # this ensures event is added to undo redo stack
            self._on_release(geometry.bounds(self.current_obj))
            # mark the latest action as designer displace
            latest = self.studio.last_action()
            if latest is not None:
                latest.key = "designer_displace"
            self._displace_active = False

    def displace(self, side):
        if not self.current_obj:
            return
        if time.time() - self._last_displace < .5:
            self.studio.pop_last_action("designer_displace")

        self._on_start()
        self._displace_active = True
        self._last_displace = time.time()
        bounds = geometry.bounds(self.current_obj)
        x1, y1, x2, y2 = bounds
        if side == 'right':
            bounds = x1 + 1, y1, x2 + 1, y2
        elif side == 'left':
            bounds = x1 - 1, y1, x2 - 1, y2
        elif side == 'up':
            bounds = x1, y1 - 1, x2, y2 - 1
        elif side == 'down':
            bounds = x1, y1 + 1, x2, y2 + 1
        self._on_move(bounds)

    def clear_obj_highlight(self):
        if self.highlight is not None:
            self.highlight.clear()
            self.current_obj = None
            if self.current_container is not None:
                self.current_container.clear_highlight()
                self.current_container = None

    def _on_start(self):
        obj = self.current_obj
        if obj is not None:
            obj.layout.change_start(obj)

    def _on_release(self, bound):
        obj = self.current_obj
        container = self.current_container
        if obj is None:
            return
        if container is not None and container != obj:
            container.clear_highlight()
            if self.current_action == self.MOVE:
                if container != self and obj.is_toplevel:
                    self._show_toplevel_warning()
                    return
                container.add_widget(obj, bound)
                # If the enclosed widget was initially the root object, make the container the new root object
                if obj == self.root_obj and obj != self:
                    self.root_obj = self.current_container
            else:
                obj.layout.widget_released(obj)
            self.studio.widget_layout_changed(obj)
            self.current_action = None
            self.create_restore(obj)
        elif obj.layout == self and self.current_action == self.MOVE:
            self.create_restore(obj)
        elif self.current_action == self.RESIZE:
            obj.layout.widget_released(obj)
            self.current_action = None
            self.create_restore(obj)

    def create_restore(self, widget):
        prev_restore_point = widget.recent_layout_info
        cur_restore_point = widget.layout.get_restore(widget)
        if prev_restore_point == cur_restore_point:
            return
        prev_container = prev_restore_point["container"]
        container = widget.layout

        def undo(_):
            container.remove_widget(widget)
            prev_container.restore_widget(widget, prev_restore_point)

        def redo(_):
            prev_container.remove_widget(widget)
            container.restore_widget(widget, cur_restore_point)

        self.studio.new_action(Action(undo, redo))

    def _on_move(self, new_bound):
        obj = self.current_obj
        current = self.current_container
        if obj is None:
            return
        self.current_action = self.MOVE
        container: Container = self.layout_at(new_bound)
        if container is not None and obj != container:
            if container != current:
                if current is not None:
                    current.clear_highlight()
                container.show_highlight()
                self.current_container = container
            container.move_widget(obj, new_bound)
        else:
            if current is not None:
                current.clear_highlight()
                self.current_container = self
            obj.level = 0
            obj.layout = self
            self.move_widget(obj, new_bound)
        if obj.layout.layout_strategy.realtime_support:
            self.studio.widget_layout_changed(obj)

    def _on_size_changed(self, new_bound):
        obj = self.current_obj
        if obj is None:
            return
        self.current_action = self.RESIZE
        if self.current_obj.max_size or self.current_obj.min_size:
            b = geometry.constrain_bounds(
                new_bound,
                self.current_obj.max_size,
                self.current_obj.min_size
            )
            new_bound = b

        if isinstance(obj.layout, Container):
            obj.layout.resize_widget(obj, new_bound)

        if obj.layout.layout_strategy.realtime_support:
            self.studio.widget_layout_changed(obj)

    def _text_change(self):
        self.studio.style_pane.apply_style("text", self._text_editor.get_all(), self.current_obj)

    def _show_text_editor(self, widget):
        assert widget == self.current_obj
        self._text_editor.lift(widget)
        cnf = self._collect_text_config(widget)
        self._text_editor.config(**cnf)
        self._text_editor.place(in_=widget, relwidth=1, relheight=1, x=0, y=0)
        self._text_editor.clear()
        self._text_editor.focus_set()
        self._text_editor.insert("1.0", widget["text"])

    def _collect_text_config(self, widget):
        s = ttk.Style()
        config = dict(
            background="#ffffff",
            foreground="#000000",
            font="TkDefaultFont"
        )
        keys = widget.keys()
        for opt in config:
            if opt in keys:
                config[opt] = (widget[opt] or config[opt])
            else:
                config[opt] = (s.lookup(widget.winfo_class(), opt) or config[opt])
        config["insertbackground"] = config["foreground"]
        return config

    def _text_hide(self, *_):
        self._text_editor.place_forget()

    def on_select(self, widget):
        self.select(widget)

    def on_widget_change(self, old_widget, new_widget=None):
        pass

    def on_widget_add(self, widget, parent):
        pass

    def show_highlight(self, *_):
        pass

    def save_window_pos(self):
        pass

    def on_app_close(self):
        if self.has_changed():
            save = self.save_prompt()
            if save:
                save_to = self.save()
                if save_to is None:
                    return False
            elif save is None:
                return False
        return True


class DesignContext(BaseContext):
    _untitled_count = 0

    def __init__(self, master, studio, path=None):
        super(DesignContext, self).__init__(master, studio)
        self.designer = Designer(self, studio)
        self.designer.pack(fill="both", expand=True)
        self.path = path
        self.icon = get_tk_image("paint", 15, 15)
        self.name = self.name_from_path(path) if path else self._create_name()
        self._loaded = False

    def _create_name(self):
        DesignContext._untitled_count += 1
        return f"untitled_{DesignContext._untitled_count}"

    def name_from_path(self, path):
        return os.path.basename(path)

    def save(self, new_path=None):
        path = self.designer.save(new_path)
        if path:
            self.path = path
            self.name = self.name_from_path(path)
            self.tab_handle.config_tab(text=self.name, **self.style.text)

            if self.tab_view._selected == self.tab_handle:
                # re-apply selection style
                self.tab_handle.on_select()
        return path

    def on_context_set(self):
        # lazy loading, only load when tab is brought into view for first time
        if not self._loaded:
            if self.path:
                self.designer.open_file(self.path)
            else:
                self.designer.open_new()
            self._loaded = True
        self.studio.set_path(self.path)

    def on_load_complete(self):
        # the design load thread is done
        self.update_save_status()

    def get_tab_menu(self):
        return (
            EnableIf(
                lambda: self.studio.context == self and self.designer.design_path,
                ("command", "Reload", icon("rotate_clockwise", 14, 14), self.designer.reload, {})
            ),
        )

    def serialize(self):
        data = super().serialize()
        data["args"] = (self.path, )
        return data

    def update_save_status(self):
        if self.designer:
            if self.designer.has_changed():
                self.tab_handle.config_tab(text=f"*{self.name}", **self.style.text_italic)
            else:
                self.tab_handle.config_tab(text=self.name, **self.style.text)

            if self.tab_view._selected == self.tab_handle:
                # re-apply selection style
                self.tab_handle.on_select()

    def new_action(self, action: Action):
        super(DesignContext, self).new_action(action)
        self.update_save_status()

    def pop_last_action(self, key=None):
        super(DesignContext, self).pop_last_action(key)
        self.update_save_status()

    def last_action(self):
        self.update_save_status()
        return super().last_action()

    def undo(self):
        super(DesignContext, self).undo()
        self.update_save_status()

    def redo(self):
        super(DesignContext, self).redo()
        self.update_save_status()

    def can_persist(self):
        return self.path is not None

    def on_context_unset(self):
        pass

    def on_app_close(self):
        return self.designer.on_app_close()

    def on_context_close(self):
        return self.designer.on_app_close()


class MultiSaveDialog(MessageDialog):

    class CheckedItem(CompoundList.BaseItem):

        def render(self):
            self.check = Checkbutton(
                self, **self.style.checkbutton, text=self.value.name
            )
            self.config_all(**self.style.bright)
            self.check.set(True)
            self.check.pack(fill="both")

        def checked(self):
            return self.check.get()

        def on_hover(self, *_):
            self.config_all(**self.style.surface)

        def on_hover_ended(self, *_):
            self.config_all(**self.style.bright)

    def __init__(self, master, studio, contexts=None):
        self.studio = studio
        self.check_contexts = contexts
        super(MultiSaveDialog, self).__init__(master, self.render)
        self.title("Save dialog")
        self.value = None

    def cancel(self, *_):
        self.destroy()

    def discard(self, *_):
        self.value = []
        self.destroy()

    def save(self, *_):
        self.value = [i.value for i in self.context_choice.items if i.checked()]
        self.destroy()

    @classmethod
    def ask_save(cls, parent, studio, contexts=None):
        dialog = cls(parent, studio, contexts)
        dialog.wait_window()
        return dialog.value

    def render(self, window):
        contexts = self.check_contexts if self.check_contexts is not None else self.studio.contexts
        self.contexts = [
            i for i in contexts if isinstance(i, DesignContext) and i.designer.has_changed()
        ]
        self.geometry("500x250")
        self._message("Some files have changes. Select files to save", self.ICON_INFO)
        self.context_choice = CompoundList(window)
        self.context_choice.config(padx=2, height=200)
        self.context_choice.set_item_class(MultiSaveDialog.CheckedItem)
        self.context_choice.set_values(self.contexts)
        self.context_choice.config_all(**self.style.hover)
        self._make_button_bar()
        self.cancel_btn = self._add_button(text="Cancel", command=self.cancel)
        self.save_btn = self._add_button(text="Don't save", command=self.discard)
        self.discard_btn = self._add_button(text="Save", command=self.save, focus=True)
        self.context_choice.pack(fill="both", expand=True, padx=10, pady=5)
