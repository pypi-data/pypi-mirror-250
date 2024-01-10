import sys, re

from .scripts.clear import clear
from .scripts.listenKeyboard import listenKeyboard
from .scripts.showItemList import showItemList
from .scripts.isIterable import isIterable
from .scripts.ternaryOperator import ternaryOperator as terno

class Form:
    
    _display = ""
    _count = 0
    _values = { }

    @property
    def values(self):
        return { key: value for key, value in self.__dict__.items() if key not in [ "_display", "_count", "orderedList", "spacing", "separator", "separatorSize" ] }

    def __init__(self, title: str = "", separator: str = "-", separatorSize: int = 100, orderedList: bool = True, spacing: int = 0):
        
        assert isinstance(title, str), "The title must be a string."
        assert isinstance(separator, str), "The separator must be a string."
        assert isinstance(separatorSize, int), "The separatorSize must be a integer."
        assert isinstance(orderedList, bool), "The orderedList must be a boolean."
        assert isinstance(spacing, int), "The spacing must be a integer."

        self._display = f"{ title }"
        
        if separator != "":
            self._display += f"{ terno(self._display != "", "\n", "") }{ separator * separatorSize }" 

        self.separator = separator
        self.separatorSize = separatorSize
        self.orderedList = orderedList
        self.spacing = spacing

    def __call__(self):

        for key, value in self._values.items():
            value['title'] = key

            if value['type'] == bool:
                self._booleanInput(**value)
                continue
                
            elif "options" in value and isIterable(value['options']):
                self._optionsInput(**value)
                continue
            
            self._input(**value)
        
        self._display += f"\n{ self.separator * self.separatorSize }"
        clear()
        print(self._display)

    def add(self, **kwargs):

        for key, value in kwargs.items():
            assert isinstance(value, dict), f"The { key } must be a dict."
            assert isinstance(value["type"], type), f"The { key } must have a type."
            assert 'description' in value, f"The { key } must have a description."
        
        self._values.update(kwargs)
    
    def _input(self, **properties):

        if "max" in properties and properties['type'] == str:
            properties['default'] = properties['default'][:properties['max']]

        self._count += 1
        clear()
        newEntryText = f"{ showItemList(self._count, self.spacing, self.orderedList) } { properties['description'] if 'description' in properties else '' }"
        
        if ("min" in properties or "max" in properties) and properties['type'] in [ str, int, float ]:
            newEntryText += f" (" \
                f"{ f"min: { terno("min" in properties, properties['min'], "") }"}" \
                f"{ terno("min" in properties and "max" in properties, ", ", "") }" \
                f"{ f"max: { terno("max" in properties, properties['max'], "") }" }" \
                f")"

        if "default" in properties:
            newEntryText += f" (default: { properties['default'] })"

        if self._display != "": print(self._display)

        newEntry = ""

        try:
            newEntry = input(newEntryText + ": ")
            if newEntry != "": newEntry = properties['type'](newEntry)

            if "default" in properties and newEntry == "":
                newEntry = properties['default']
            
            assert newEntry != ""
        
            if properties['type'] == str:
                if "min" in properties and len(newEntry) < properties['min']:
                    raise

                if "max" in properties and len(newEntry) > properties['max']:
                    raise

            elif properties['type'] == int or properties['type'] == float:
                if "min" in properties and newEntry < properties['min']:
                    raise

                if "max" in properties and newEntry > properties['max']:
                    raise

            if "validate" in properties and properties['type'] == str:
                assert re.match(properties['validate'], newEntry)

            self.__dict__[properties['title']] = newEntry
            self._display += f"{ terno(self._display != "", "\n", "") }{ newEntryText }: { newEntry }"
        
        except ( ValueError, TypeError, AssertionError, RuntimeError ):
            self._count -= 1
            self._input(**properties)

        except KeyboardInterrupt:
            sys.exit(0)

    def _booleanInput(self, **properties):
        
        self._count += 1
        clear()

        newEntryText = f"{ showItemList(self._count, self.spacing, self.orderedList) } { terno("description" in properties, properties['description'], '') }"

        print(self._display)
        print(newEntryText + "? (y/n) ", end="")

        print()
        newEntry = listenKeyboard().upper()

        if newEntry not in [ "Y", "N" ]:
            self._count -= 1
            self._booleanInput(**properties)
            return

        self.__dict__[properties['title']] = terno(newEntry == "Y", True, False)

        self._display += f"{ terno(self._display != "", "\n", "") }{ newEntryText }? (y/n) { newEntry }"

    def _optionsInput(self, **properties):

        assert "options" in properties, f"The { properties['title'] } must have a options."
        assert isinstance(properties['options'], properties['type']), f"The { properties['title'] } must have a options with type { properties['type'] }."
        
        self._count += 1
        clear()

        spacing = self.spacing * 4 if self.spacing < 4 else self.spacing * 2

        newEntryText = f"{ showItemList(self._count, self.spacing, self.orderedList) } { terno("description" in properties, properties['description'], "") }"

        options = ""

        if properties['type'] == dict:
            options = "\n".join([ f"{ showItemList(index + 1, spacing, True) } { key } - { value }" for index, ( key, value ) in enumerate(properties['options'].items()) ])

        else:
            options = "\n".join([ f"{ showItemList(index + 1, spacing, True) } { option }" for index, option in enumerate(properties['options']) ])

        print(self._display)
        print(f"{ newEntryText}: \n{ options }", end="")

        print()
        newEntry = listenKeyboard()
        key = None
        
        try:

            newEntry = int(newEntry)
            assert newEntry > 0 and newEntry <= len(properties['options'])

            if properties['type'] == dict:
                key = list(properties['options'].keys())[newEntry - 1]
                newEntry = properties['options'][key]
        
        except ( ValueError, TypeError, AssertionError, RuntimeError ):
            self._count -= 1
            self._optionsInput(**properties)
            return
        
        if properties['type'] == dict:
            self.__dict__[properties['title']] = key
            self._display += f"{ terno(self._display != "", "\n", "") }{ newEntryText }: { key }"
            return

        self.__dict__[properties['title']] = properties['options'][newEntry - 1]
        self._display += f"{ terno(self._display != "", "\n", "") }{ newEntryText }: { properties['options'][newEntry - 1] }"