#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2023.12.25 21:00:00                  #
# ================================================== #

from PySide6.QtCore import Qt, QAbstractItemModel, QModelIndex
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTreeView, QMenu

from pygpt_net.utils import trans


class OptionDict(QWidget):
    def __init__(self, window=None, parent_id: str = None, id: str = None, option: dict = None):
        """
        Settings dictionary items

        :param window: main window
        :param id: option id
        :param parent_id: parent option id
        :param option: option data
        """
        super(OptionDict, self).__init__(window)
        self.window = window
        self.id = id
        self.parent_id = parent_id
        self.option = option
        self.title = ""
        self.real_time = False
        self.keys = {}
        self.items = []

        # init from option data
        if self.option is not None:
            if "label" in self.option:
                self.title = self.option["label"]
            if "value" in self.option:
                self.items = self.option["value"]
            if "keys" in self.option:
                self.keys = self.option["keys"]
            if "items" in self.option:
                self.items = list(self.option["items"])
            if "real_time" in self.option:
                self.real_time = self.option["real_time"]

        # setup dict model
        headers = list(self.keys.keys())

        self.list = OptionDictItems(self)
        self.model = OptionDictModel(self.items, headers)
        self.model.dataChanged.connect(self.model.saveData)

        # append dict model
        self.list.setModel(self.model)

        # add button
        self.add_btn = QPushButton(trans('action.add'), self)
        self.add_btn.setCursor(Qt.PointingHandCursor)
        self.add_btn.clicked.connect(self.add)
        self.add_btn.setAutoDefault(False)

        # layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.add_btn)
        self.layout.addWidget(self.list)
        self.setLayout(self.layout)

        # update model list
        self.update()

    def add(self):
        """
        Add new empty item to settings dict
        """
        # create empty dict
        empty = {header: '' for header in self.model.headers}
        count = self.model.rowCount()

        # add new item
        self.model.items.append(empty)
        self.model.updateData(self.model.items)

        # mark new item
        new_index = self.model.index(count, 0)
        self.list.setCurrentIndex(new_index)
        self.list.scrollTo(new_index)

    def delete_item(self, event):
        """
        Delete item (show confirm)

        :param event: Menu event
        """
        index = self.list.indexAt(event.pos())
        if index.isValid():
            # remove item
            idx = index.row()
            self.window.controller.config.dictionary.delete_item(self, idx)

    def delete_item_execute(self, idx):
        """
        Delete item (execute)

        :param idx: Index of item
        """
        if len(self.model.items) > idx:
            self.model.items.pop(idx)
        self.model.removeRows(idx, 1)

        # update model list
        self.update()
        self.list.updateGeometries()
        self.items = self.model.items
        self.model.updateData(self.items)

    def remove(self):
        """
        Remove all items
        """
        self.model.removeRows(0, self.model.rowCount())

    def update(self):
        """
        Updates list of items
        """
        self.model.removeRows(0, self.model.rowCount())
        i = 0
        for item in list(self.items):
            self.model.insertRow(i)
            j = 0
            for k in self.keys:
                if k in item:
                    # add item to model list
                    self.model.setData(self.model.index(i, j), item[k])
                j += 1
            i += 1


class OptionDictItems(QTreeView):
    NAME = range(1)  # list of columns

    def __init__(self, owner=None):
        """
        Select menu

        :param window: main window
        :param id: input id
        """
        super(OptionDictItems, self).__init__(owner)
        self.parent = owner
        self.setIndentation(0)
        self.setHeaderHidden(False)

    def contextMenuEvent(self, event):
        """
        Context menu event

        :param event: context menu event
        """
        actions = {}
        actions['delete'] = QAction(QIcon.fromTheme("edit-delete"), trans('action.delete'), self)
        actions['delete'].triggered.connect(
            lambda: self.parent.delete_item(event))
        menu = QMenu(self)
        menu.addAction(actions['delete'])

        # get index of item
        item = self.indexAt(event.pos())
        idx = item.row()
        if idx >= 0:
            menu.exec_(event.globalPos())


class OptionDictModel(QAbstractItemModel):
    def __init__(self, items, headers, parent=None):
        super(OptionDictModel, self).__init__(parent)
        self.items = items
        self.headers = headers

    def headerData(self, section, orientation, role):
        """
        Header data
        :param section: Section
        :param orientation: Orientation
        :param role: Role
        :return: Header data
        """
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[section]
        return None

    def rowCount(self, parent=QModelIndex()):
        """
        Row count
        :param parent: Parent
        :return: Row count
        """
        return len(self.items) if not parent.isValid() else 0

    def columnCount(self, parent=QModelIndex()):
        """
        Column count
        :param parent: Parent
        :return: Column count
        """
        return len(self.headers) if not parent.isValid() else 0

    def data(self, index, role=Qt.DisplayRole):
        """
        Data
        :param index: Index
        :param role: Role
        :return: Data
        """
        if not index.isValid():
            return None
        if role == Qt.DisplayRole or role == Qt.EditRole:
            entry = self.items[index.row()]
            key = self.headers[index.column()]
            return entry.get(key, "")
        return None

    def setData(self, index, value, role=Qt.EditRole):
        """
        Set data
        :param index: Index
        :param value: Value
        :param role: Role
        :return: Set data
        """
        if index.isValid() and role == Qt.EditRole:
            entry = self.items[index.row()]
            key = self.headers[index.column()]
            entry[key] = value
            self.dataChanged.emit(index, index, [Qt.EditRole])
            return True
        return False

    def flags(self, index):
        """
        Flags
        :param index: Index
        :return: Flags
        """
        if not index.isValid():
            return Qt.NoItemFlags
        return super(OptionDictModel, self).flags(index) | Qt.ItemIsEditable

    def parent(self, index):
        """
        Parent
        :param index: Index
        :return: Parent
        """
        return QModelIndex()

    def index(self, row, column, parent=QModelIndex()):
        """
        Index
        :param row: Row
        :param column: Column
        :param parent: Parent
        :return: Index
        """
        if parent.isValid() or row >= len(self.items) or column >= len(self.headers):
            return QModelIndex()
        return self.createIndex(row, column)

    def saveData(self):
        """
        Save data
        """
        pass

    def updateData(self, data):
        """
        Update data
        :param new_data_list: New data list
        """
        self.beginResetModel()
        self.items = data
        self.endResetModel()
