from typing import Any, Callable
from enum import Enum

from ipih.collection import (
    R,
    T,
    FieldItem,
    FieldItemList,
    Result,
)

def one(
    value: Result[T | list[T]] | T | list[T], default_value: Any | None = None
) -> T:
    return (
        ResultTool.get_first_item(value, default_value)
        if isinstance(value, Result)
        else DataTool.get_first_item(value, default_value)
    )
    
def nl(
    value: str = "", count: int = 1, reversed: bool | None = False, normal: bool = True
) -> str:
    nl_text: str = ["<br>", "\n"][int(normal)] * count
    return DataTool.triple_bool(
        reversed, j((value, nl_text)), j((nl_text, value)), j((nl_text, value, nl_text))
    )


def j(value: tuple[Any | None] | list[Any | None], splitter: str = "") -> str:
    return splitter.join(list(map(lambda item: str(item), list(filter(nn, value)))))


def jnl(value: tuple[Any | None] | list[Any | None]) -> str:
    return j(value, nl())


def js(
    value: tuple[Any | None] | list[Any | None], aditional_splitter: str = ""
) -> str:
    return j(value, j((aditional_splitter or "", " ")))

class DataTool:
    @staticmethod
    def every(
        action_function: Callable[[T, int | None], None],
        data: list[T],
        use_index: bool = False,
    ) -> list[T]:
        if use_index:
            for index, item in enumerate(data):
                action_function(item, index)
        else:
            for item in data:
                action_function(item)
        return data

    @staticmethod
    def fields(value: object) -> list[str]:
        if dataclasses.is_dataclass(value):
            return [field.name for field in dataclasses.fields(value)]
        return []

    @staticmethod
    def map(function: Callable[[Any], Any], value: list[Any] | Any) -> list[Any]:
        return list(map(function, DataTool.as_list(value)))

    @staticmethod
    def filter(function: Callable[[Any], Any], value: list[Any] | Any) -> list[Any]:
        return list(filter(function, DataTool.as_list(value)))

    @staticmethod
    def as_value(
        function_or_value: Callable[[None], str] | str | None,
        parameters: Any | None = None,
    ) -> str:
        return (
            (function_or_value() if n(parameters) else function_or_value(parameters))
            if callable(function_or_value)
            else function_or_value
        ) or ""

    @staticmethod
    def as_bitmask_value(
        value: int | tuple[Enum] | Enum | list[Enum] | list[int],
    ) -> int:
        value_list: list[Enum | int] = None
        if isinstance(value, (list, tuple)):
            value_list = value
        elif isinstance(value, (int, Enum)):
            value_list = [value]
        return BitMask.set(value_list)

    @staticmethod
    def by_index(data: list | None, index: int, default_value: Any = None) -> Any:
        if data is None:
            return default_value
        if len(data) <= index:
            return default_value
        return data[index]

    @staticmethod
    def rpc_represent(data: dict | None, ensure_ascii: bool = True) -> str | None:
        return (
            json.dumps(data, cls=PIHEncoder, ensure_ascii=ensure_ascii)
            if data is not None
            else None
        )

    @staticmethod
    def rpc_unrepresent(value: str | None) -> dict | None:
        return None if e(value) else json.loads(value)

    @staticmethod
    def to_result(
        result_string: str,
        class_type_holder: Any | Callable[[Any], Any] | None = None,
        first_data_item: bool = False,
    ) -> Result:
        result_object: dict = DataTool.rpc_unrepresent(result_string)
        if result_object is None:
            return Result(None, None)
        data: dict = result_object["data"]
        data = DataTool.get_first_item(data) if first_data_item else data

        def fill_data_with(item: Any) -> Any:
            if e(class_type_holder):
                return item
            return (
                class_type_holder(item)
                if callable(class_type_holder)
                and not inspect.isclass(class_type_holder)
                else DataTool.fill_data_from_source(
                    class_type_holder()
                    if inspect.isclass(class_type_holder)
                    else class_type_holder,
                    item,
                )
            )

        def obtain_data() -> Any | None:
            return (
                list(map(fill_data_with, data))
                if isinstance(data, list)
                else fill_data_with(data)
            )

        if "fields_alias" in result_object:
            return Result(
                FieldItemList(
                    EnumTool.get(
                        FieldCollectionAliases, result_object["fields_alias"]
                    ).value
                ),
                obtain_data(),
            )
        else:
            fields = None if "fields" not in result_object else result_object["fields"]
        field_list: list[FieldItem] = None
        if fields is not None:
            field_list = []
            for field_item in fields:
                for field_name in field_item:
                    field_list.append(
                        DataTool.fill_data_from_source(
                            FieldItem(), field_item[field_name]
                        )
                    )
        return Result(FieldItemList(field_list) if field_list else None, obtain_data())

    @staticmethod
    def as_list(value: Any) -> list[Any]:
        if e(value):
            return []
        if isinstance(value, (list, Tuple)):
            return value
        if isinstance(value, dict):
            return list(value.values())
        try:
            if issubclass(value, Enum):
                return [EnumTool.get(item) for item in value]
        except TypeError:
            pass
        return [value]

    @staticmethod
    def to_list(value: dict | Enum, key_as_value: bool | None = False) -> list[Any]:
        if isinstance(value, dict):
            return [key if key_as_value else item for key, item in value.items()]
        result: list[Any | str] = []
        for item in value:
            result.append(
                [item.name, item.value]
                if n(key_as_value)
                else (item.name if key_as_value else item.value)
            )
        return result

    @staticmethod
    def triple_bool(
        value: bool | None, false_result: Any, true_result: Any, none_result: Any
    ) -> Any:
        if n(value):
            return none_result
        return true_result if value else false_result

    @staticmethod
    def to_result_with_fields(
        data: str, fields: FieldItemList, cls=None, first_data_item: bool = False
    ) -> Result:
        return Result(fields, DataTool.to_result(data, cls, first_data_item))

    @staticmethod
    def to_string(obj: object, join_symbol: str = "") -> str:
        return j(obj.__dict__.values(), join_symbol)

    @staticmethod
    def to_data(obj: object) -> dict:
        return obj.__dict__

    @staticmethod
    def fill_data_from_source(
        destination: object,
        source: dict | object,
        copy_by_index: bool = False,
        skip_not_none: bool = False,
    ) -> object | None:
        if dataclasses.is_dataclass(source):
            source = source.__dict__
        if source is None:
            return None
        else:
            if copy_by_index:
                [
                    setattr(
                        destination, key.name, [source[key] for key in source][index]
                    )
                    for index, key in enumerate(dataclasses.fields(destination))
                ]
            else:
                if dataclasses.is_dataclass(source):
                    for field in destination.__dataclass_fields__:
                        if field in source:
                            if not skip_not_none or e(
                                destination.__getattribute__(field)
                            ):
                                destination.__setattr__(field, source[field])
                else:
                    is_dict: bool = isinstance(source, dict)
                    for field in destination.__dataclass_fields__:
                        if field in source if is_dict else hasattr(source, field):
                            if not skip_not_none or e(
                                destination.__getattribute__(field)
                            ):
                                destination.__setattr__(
                                    field,
                                    source[field]
                                    if is_dict
                                    else source.__getattribute__(field),
                                )
        return destination

    @staticmethod
    def fill_data_from_list_source(
        class_type, source: list[Any] | dict[str, Any]
    ) -> Any | None:
        if n(source):
            return None
        return list(
            map(
                lambda item: DataTool.fill_data_from_source(class_type(), item),
                source if isinstance(source, list) else source.values(),
            )
        )

    @staticmethod
    def fill_data_from_rpc_str(data: T, source: str) -> T:
        return DataTool.fill_data_from_source(data, DataTool.rpc_unrepresent(source))

    @staticmethod
    def get_first_item(
        value: list[T] | T | dict[str, Any], default_value: Any | None = None
    ) -> T | Any | None:
        if e(value):
            return default_value
        if isinstance(value, dict):
            for _, item in value.items():
                return item
        return value[0] if isinstance(value, (list, tuple)) else value

    @staticmethod
    def get_last_item(
        value: list[T] | T | dict[str, Any], default_value: Any | None = None
    ) -> T | Any | None:
        if e(value):
            return default_value
        if isinstance(value, dict):
            for _, item in reversed(value.items()):
                return item
        return value[len(value) - 1] if isinstance(value, (list, tuple)) else value

    @staticmethod
    def if_is_in(
        value: Any,
        arg_name: Any,
        default_value: Any | Callable[[None], Any | None] | None = None,
    ) -> Any | None:
        return DataTool.check(
            DataTool.is_in(value, arg_name), lambda: value[arg_name], default_value
        )

    @staticmethod
    def is_in(value: Any, arg_name: Any) -> bool:
        if isinstance(value, (list, tuple)) and isinstance(arg_name, int):
            return arg_name < len(value)
        try:
            if issubclass(value, Enum):
                return arg_name in value.__members__
        except TypeError:
            pass
        return arg_name in value

    @staticmethod
    def check(
        check_value: bool,
        true_value: Callable[[None], Any | None] | Any,
        false_value: Callable[[None], Any | None] | Any = None,
    ) -> Any | None:
        return if_else(check_value, true_value, false_value)

    @staticmethod
    def check_not_none(
        check_value: Any | list[Any] | tuple[Any] | None,
        true_value: Callable[[None], Any | None] | Any,
        false_value: Callable[[None], Any | None] | Any | None = None,
        check_all: bool = False,
    ) -> Any | None:
        check: bool = False
        if isinstance(check_value, (list, tuple)):
            for item in check_value:
                check = not n(item)
                if (not check_all and check) or (check_all and not check):
                    break
        else:
            check = not n(check_value)
        return (
            (true_value() if callable(true_value) else true_value)
            if check
            else false_value()
            if not n(false_value) and callable(false_value)
            else false_value
        )

    @staticmethod
    def if_not_empty(
        check_value: Any | None,
        return_value: Callable[[Any], Any],
        default_value: Any | None = None,
    ) -> Any | None:
        return default_value if e(check_value) else return_value(check_value)

    @staticmethod
    def is_empty(value: list | str | dict | tuple | Any | None) -> bool:
        return n(value) or (
            isinstance(value, (list, str, dict, tuple)) and len(value) == 0
        )

    @staticmethod
    def is_not_none(value: Any | None) -> bool:
        return not n(value)

    @staticmethod
    def is_none(value: Any | None) -> bool:
        return value is None


class BitMask:
    @staticmethod
    def add(
        value: int | None, bit: int | tuple[Enum] | Enum | list[Enum] | list[int]
    ) -> int:
        value = value or 0
        bits: list[int | Enum] = bit if isinstance(bit, (list, tuple)) else [bit]
        for bit in bits:
            if isinstance(bit, int):
                value |= bit
            elif isinstance(bit, Enum):
                value |= bit.value
        return value

    @staticmethod
    def set(bit: int | tuple[Enum] | Enum | list[Enum] | list[int]) -> int:
        return BitMask.add(0, bit)

    @staticmethod
    def value(bit: int | tuple[Enum] | Enum | list[Enum] | list[int]) -> int:
        return BitMask.add(0, bit)

    @staticmethod
    def has(value: int, bit: int | tuple[Enum] | Enum | list[Enum] | list[int]) -> bool:
        if value is None:
            return False
        bits: list[int] = bit if isinstance(bit, (list, tuple)) else [bit]
        result: bool = False
        if len(bits) > 1:
            for bit in bits:
                result = BitMask.has(value, bit)
                if result:
                    break
        else:
            if isinstance(bit, int):
                result = (value & bit) == bit
            elif isinstance(bit, Enum):
                result = BitMask.has(value, bit.value)
        return result

    @staticmethod
    def has_index(value: int, index: int) -> bool:
        return BitMask.has(value, pow(2, index))

    @staticmethod
    def remove(value: int, bit: int | Enum) -> int:
        if isinstance(bit, Enum):
            bit = bit.value
        if BitMask.has(value, bit):
            value ^= bit
        return value
    
class ResultTool:
    @staticmethod
    def pack(fields: Any, data: Any) -> dict[str, Any]:
        result: dict[str, Any] = {"data": data}
        if isinstance(fields, FieldCollectionAliases):
            result["fields_alias"] = fields.name
        else:
            result["fields"] = fields
        return result

    @staticmethod
    def unpack(result: dict) -> tuple[FieldItemList, Any]:
        return ResultTool.unpack_fields(result), ResultTool.unpack_data(result)

    @staticmethod
    def unpack_fields(data: dict) -> Any:
        if "fields_alias" in data:
            return (FieldCollectionAliases._member_map_[data["fields_alias"]].value,)
        return data["fields"]

    @staticmethod
    def unpack_data(result: dict) -> Any:
        return result["data"]

    @staticmethod
    def is_empty(result: Result | None) -> bool:
        return n(result) or e(result.data)

    @staticmethod
    def get_first_item(
        result: Result[list[T] | T], default_value: Any | None = None
    ) -> T | Any | None:
        return DataTool.get_first_item(result.data, default_value)

    @staticmethod
    def with_first_item(
        result: Result[list[T] | T], default_value: Any | None = None
    ) -> Result[T]:
        result.data = ResultTool.get_first_item(result, default_value)
        return result

    @staticmethod
    def to_string(
        result: Result[T],
        use_index: bool = True,
        item_separator: str = "\n",
        value_separator: str | None = None,
        show_caption: bool = True,
    ) -> str:
        result_string_list: list[str] = []
        data: list = DataTool.as_list(result.data)
        item_result_string_list: list[str] = None
        for index, data_item in enumerate(data):
            if use_index and len(data) > 1:
                result_string_list.append(f"*{str(index + 1)}*:")
            if value_separator is not None:
                item_result_string_list = []
            for field_item in result.fields.list:
                field: FieldItem = field_item
                if not field.visible:
                    continue
                data_value: str | None = None
                if isinstance(data_item, dict):
                    data_value = data_item[field.name]
                elif dataclasses.is_dataclass(data_item):
                    data_value = data_item.__getattribute__(field.name)
                data_value = data_value or "Нет"
                if value_separator is None:
                    if show_caption:
                        result_string_list.append(f"{field.caption}: {data_value}")
                    else:
                        result_string_list.append(data_value)
                else:
                    if show_caption:
                        item_result_string_list.append(f"{field.caption}: {data_value}")
                    else:
                        item_result_string_list.append(data_value)
            if value_separator is not None:
                result_string_list.append(value_separator.join(item_result_string_list))
        return item_separator.join(result_string_list)

    @staticmethod
    def as_list(result: Result[T]) -> Result[list[T]]:
        return Result(
            result.fields,
            []
            if result.data is None
            else [result.data]
            if not isinstance(result.data, list)
            else result.data,
        )

    @staticmethod
    def filter(
        filter_function: Callable[[T], bool],
        result: Result[list[T]],
        as_new_result: bool = False,
    ) -> Result[list[T]]:
        try:
            data: list[T] = DataTool.filter(filter_function, result.data)
            if as_new_result:
                return Result(result.fields, data)
            result.data = data
        except StopIteration:
            pass
        return result

    @staticmethod
    def sort(
        sort_function: Callable, result: Result[list[T]], reverse: bool = False
    ) -> Result[list[T]]:
        if nn(sort_function):
            result.data.sort(key=sort_function, reverse=reverse)
        return result

    @staticmethod
    def every(
        action_function: Callable[[T, int | None], None],
        result: Result[list[T]],
        use_index: bool = False,
    ) -> Result[list[T]]:
        result.data = DataTool.every(action_function, result.data, use_index)
        return result

    @staticmethod
    def do_while(
        result: Result[list[T]], check_function: Callable[[T], bool]
    ) -> Any | None:
        result_data: Any | None = None
        for item in result.data:
            if check_function(item):
                result_data = item
                break
        return result_data

    @staticmethod
    def map(
        map_function_or_class: Callable[[T], R] | R,
        result: Result[list[T]],
        map_on_each_data_item: bool = True,
        as_new_result: bool = False,
    ) -> Result[list[R]]:
        map_function: Callable[[T], R] = None
        if not isfunction(map_function_or_class):
            map_function = lambda item: DataTool.fill_data_from_source(
                map_function_or_class(), item
            )
        else:
            map_function = map_function_or_class
        data: list[R] = (
            list(map(map_function, result.data))
            if map_on_each_data_item
            else map_function_or_class(result.data)
        )
        if as_new_result:
            return Result(result.fields, data)
        else:
            result.data = data
        return result




n = DataTool.is_none
nn = DataTool.is_not_none


def e(value: Any | Result[Any]) -> bool:
    return (
        ResultTool.is_empty(value)
        if isinstance(value, Result)
        else DataTool.is_empty(value)
    )


ne = lambda item: not e(item)