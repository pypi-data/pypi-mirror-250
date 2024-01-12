from hoverset.ui.icons import get_icon_image
from hoverset.ui.widgets import Button, Label, Frame
from hoverset.ui.menu import MenuUtils
from studio.feature._base import BaseFeature
from studio.lib.pseudo import PseudoWidget
from studio.ui.tree import MalleableTreeView


class ComponentTreeView(MalleableTreeView):

    class Node(MalleableTreeView.Node):

        def __init__(self, master=None, **config):
            super().__init__(master, **config)
            self.widget: PseudoWidget = config.get("widget")
            self.widget.node = self
            self.name_pad.configure(text=self.widget.id)
            self.icon_pad.configure(image=get_icon_image(self.widget.icon, 15, 15))

        def widget_modified(self, widget):
            self.widget = widget
            self.name_pad.configure(text=self.widget.id)
            self.icon_pad.configure(image=get_icon_image(self.widget.icon, 15, 15))

    def initialize_tree(self):
        super(ComponentTreeView, self).initialize_tree()
        self._empty = Frame(self, **self.style.surface)
        self._empty_text = Label(self._empty, **self.style.text_passive)
        self._empty_text.pack(fill="both", expand=True, pady=30)
        self._show_empty("No items created yet")

    def add(self, node):
        super().add(node)
        self._remove_empty()

    def insert(self, index=None, *nodes):
        super(ComponentTreeView, self).insert(index, *nodes)
        self._remove_empty()

    def remove(self, node):
        super().remove(node)
        if len(self.nodes) == 0:
            self._show_empty("No items created yet")

    def _show_empty(self, text):
        self._empty_text["text"] = text
        self._empty.place(x=0, y=0, relheight=1, relwidth=1)

    def _remove_empty(self):
        self._empty.place_forget()

    def search(self, query):
        if not super().search(query):
            self._show_empty("No items match your search")
        else:
            self._remove_empty()


class ComponentTree(BaseFeature):
    name = "Component Tree"
    icon = "treeview"

    def __init__(self, master, studio=None,  **cnf):
        super().__init__(master, studio, **cnf)
        self._toggle_btn = Button(self._header, image=get_icon_image("chevron_down", 15, 15), **self.style.button,
                                  width=25,
                                  height=25)
        self._toggle_btn.pack(side="right")
        self._toggle_btn.on_click(self._toggle)

        self._search_btn = Button(
            self._header, **self.style.button,
            image=get_icon_image("search", 15, 15), width=25, height=25,
        )
        self._search_btn.pack(side="right")
        self._search_btn.on_click(self.start_search)
        self.body = Frame(self, **self.style.surface)
        self.body.pack(side="top", fill="both", expand=True)
        self._empty_label = Label(self.body, **self.style.text_passive)

        self._selected = None
        self._expanded = False
        self._tree = None

    def on_context_switch(self):
        if self._tree:
            self._tree.pack_forget()

        if self.studio.designer:
            self.show_empty(None)
            if self.studio.designer.node:
                self._tree = self.studio.designer.node
            else:
                self._tree = ComponentTreeView(self.body)
                self._tree.on_select(self._trigger_select)
                self.studio.designer.node = self._tree
            self._tree.pack(fill="both", expand=True)
        else:
            self.show_empty("No active Designer")

    def create_menu(self):
        return (
            ("command", "Expand all", get_icon_image("chevron_down", 14, 14), self._expand, {}),
            ("command", "Collapse all", get_icon_image("chevron_up", 14, 14), self._collapse, {})
        )

    def show_empty(self, text):
        if text:
            self._empty_label.lift()
            self._empty_label.place(x=0, y=0, relwidth=1, relheight=1)
            self._empty_label['text'] = text
        else:
            self._empty_label.place_forget()

    def _expand(self):
        self._tree.expand_all()
        self._toggle_btn.config(image=get_icon_image("chevron_up", 15, 15))
        self._expanded = True

    def _collapse(self):
        self._tree.collapse_all()
        self._toggle_btn.config(image=get_icon_image("chevron_down", 15, 15))
        self._expanded = False

    def _toggle(self, *_):
        if self._expanded:
            self._collapse()
        else:
            self._expand()

    def on_widget_add(self, widget: PseudoWidget, parent=None):
        if parent is None:
            node = self._tree.add_as_node(widget=widget)
        else:
            parent = parent.node
            node = parent.add_as_node(widget=widget)

        # let the designer render the menu for us
        MenuUtils.bind_all_context(
            node,
            lambda e: self.studio.designer.show_menu(e, widget) if self.studio.designer else None
        )

    def _trigger_select(self):
        if self._selected and self._selected.widget == self._tree.get().widget:
            return
        self.studio.select(self._tree.get().widget, self)
        self._selected = self._tree.get()

    def select(self, widget):
        if widget:
            node = widget.node
            self._selected = node
            node.select(None, True)  # Select node silently to avoid triggering a duplicate selection event
        elif widget is None:
            if self._selected:
                self._selected.deselect()
                self._selected = None

    def on_select(self, widget):
        self.select(widget)

    def on_widget_delete(self, widget, silently=False):
        widget.node.remove()

    def on_widget_restore(self, widget):
        widget.layout.node.add(widget.node)

    def on_widget_layout_change(self, widget):
        node = widget.node
        if widget.layout == self.studio.designer:
            parent = self._tree
        else:
            parent = widget.layout.node
        if node.parent_node != parent:
            parent.insert(None, node)

    def on_context_close(self, context):
        if hasattr(context, "designer"):
            # delete context's tree
            if hasattr(context.designer, "node") and context.designer.node:
                context.designer.node.destroy()

    def on_session_clear(self):
        self._tree.clear()

    def on_widget_change(self, old_widget, new_widget=None):
        new_widget = new_widget if new_widget else old_widget
        new_widget.node.widget_modified(new_widget)

    def on_search_query(self, query: str):
        self._tree.search(query)

    def on_search_clear(self):
        self._tree.search("")
        super(ComponentTree, self).on_search_clear()
