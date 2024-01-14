from dataclasses import dataclass
from typing import Any, Generic, Tuple, TypeVar

@dataclass
class PasswordSettings:
    length: int
    special_characters: str
    order_list: list[str]
    special_characters_count: int
    alphabets_lowercase_count: int
    alphabets_uppercase_count: int
    digits_count: int = 1
    shuffled: bool = False


@dataclass
class NameCaption:
    name: str
    caption: str | None = None


@dataclass
class NameCaptionDescription(NameCaption):
    description: str | None = None


@dataclass
class OrderedNameCaptionDescription(NameCaptionDescription):
    order: int | None = None


@dataclass
class IconedOrderedNameCaptionDescription(OrderedNameCaptionDescription):
    icon: str | None = None


@dataclass
class ParamItem(NameCaptionDescription):
    optional: bool = False


@dataclass
class FieldItem:
    name: str | None = None
    caption: str | None = None
    visible: bool = True
    class_type: Any | None = None
    default_value: str | None = None
    data_formatter: str = "{data}"


class FieldItemList:
    list: list[FieldItem]

    def copy_field_item(self, value: FieldItem) -> FieldItem:
        return FieldItem(
            value.name,
            value.caption,
            value.visible,
            value.class_type,
            value.default_value,
            value.data_formatter,
        )

    def __init__(self, *args):
        self.list = []
        arg_list = list(args)
        for arg_item in arg_list:
            if isinstance(arg_item, FieldItem):
                item: FieldItem = self.copy_field_item(arg_item)
                self.list.append(item)
            elif isinstance(arg_item, FieldItemList):
                for item in arg_item.list:
                    self.list.append(self.copy_field_item(item))
            elif isinstance(arg_item, list):
                self.list.extend(arg_item)

    def get_list(self) -> list[FieldItem]:
        return self.list

    def get_item_and_index_by_name(self, value: str) -> Tuple[FieldItem, int]:
        index: int = -1
        result: FieldItem | None = None
        for item in self.list:
            index += 1
            if item.name == value:
                result = item
                break
        return result, -1 if result is None else index

    def get_item_by_name(self, value: str) -> FieldItem:
        result, _ = self.get_item_and_index_by_name(value)
        return result

    def position(self, name: str, position: int):
        _, index = self.get_item_and_index_by_name(name)
        if index != -1:
            self.list.insert(position, self.list.pop(index))
        return self

    def get_name_list(self):
        return list(map(lambda item: str(item.name), self.list))

    def get_caption_list(self):
        return list(
            map(lambda x: str(x.caption), filter(lambda y: y.visible, self.list))
        )

    def visible(self, name: str, value: bool):
        item, _ = self.get_item_and_index_by_name(name)
        if item is not None:
            item.visible = value
        return self

    def caption(self, name: str, value: bool):
        item, _ = self.get_item_and_index_by_name(name)
        if item is not None:
            item.caption = value
        return self

    def length(self) -> int:
        return len(self.list)


T = TypeVar("T")
R = TypeVar("R")


@dataclass
class Result(Generic[T]):
    fields: FieldItemList | None = None
    data: T | None = None

    def __len__(self):
        return len(self.data)

    def __iadd__(self, value):
        if (
            isinstance(value, Result)
            and isinstance(self.data, list)
            and isinstance(value.data, list)
        ):
            self.data += value.data
        return self

    def __add__(self, value):
        if (
            isinstance(value, Result)
            and isinstance(self.data, list)
            and isinstance(value.data, list)
        ):
            self.data += value.data
        return self


@dataclass
class FullName:
    last_name: str = ""
    first_name: str = ""
    middle_name: str = ""

    def as_list(self) -> list[str]:
        return [self.last_name, self.first_name, self.middle_name]
    
@dataclass
class UserBase:
    name: str | None = None
    description: str | None = None
    distinguishedName: str | None = None


@dataclass
class User(UserBase):
    samAccountName: str | None = None
    mail: str | None = None
    telephoneNumber: str | None = None
    userAccountControl: int | None = None
