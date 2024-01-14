import colorama
from colorama import Back, Style, Fore
from prettytable import PrettyTable
from ipih.tools import DataTool

class Output(OutputBase, OutputStub):
    
    @contextmanager
    def make_indent(self, value: int, additional: bool = False) -> bool:
        indent: int = self.indent
        try:
            self.set_indent([0, indent][additional] + value)
            yield True
        finally:
            self.set_indent(indent)

    def set_indent(self, value: int) -> None:
        self.indent_value = value
        self.text_before = self.indent_symbol * value

    def bold(self, value: str) -> str:
        return f"\033[1m{value}"

    def italic(self, value: str) -> str:
        return value

    def reset_indent(self) -> None:
        self.indent_value = 0
        self.text_before = ""

    @property
    def indent(self) -> int:
        return self.indent_value

    def restore_indent(self) -> None:
        self.set_indent(self.indent_value)

    def init(self) -> None:
        colorama.init()

    def text_color(self, color: str, text: str) -> str:
        return f"{color}{text}{Fore.RESET}"

    def text_black(self, text: str) -> str:
        return self.text_color(Fore.BLACK, text)

    def text_white(self, text: str) -> str:
        return self.text_color(Fore.WHITE, text)

    def color_str(
        self,
        color: int,
        text: str,
        text_before: str | None = None,
        text_after: str | None = None,
    ) -> str:
        text = f" {text} "
        text_before = text_before or self.text_before
        text_after = text_after or self.text_after
        return f"{text_before}{color}{text}{Back.RESET}{text_after}"

    def color(
        self,
        color: int,
        text: str,
        text_before: str | None = None,
        text_after: str | None = None,
    ) -> None:
        self.write_line(self.color_str(color, text, text_before, text_after))

    def write_line(self, text: str) -> None:
        print(
            jnl(DataTool.map(lambda item: self.text_before + item, text.splitlines()))
        )

    @contextmanager
    def personalized(self) -> bool:
        pass

    def index(self, index: int, text: str, max_index: int = None) -> None:
        indent: str = ""
        if max_index is not None:
            indent = " " * 2 * (len(str(max_index)) - len(str(index)))
        if index is None:
            self.write_line(f"{indent}{text}")
        else:
            self.write_line(f"{index}. {indent}{text}")

    def input(self, caption: str) -> None:
        self.write_line(self.input_str(caption, self.text_before, text_after=":"))

    def input_str(
        self,
        caption: str,
        text_before: str | None = None,
        text_after: str | None = None,
    ) -> str:
        return self.white_str(
            f"{Fore.BLACK}{caption}{Fore.RESET}", text_before, text_after
        )

    def value(self, caption: str, value: str, text_before: str | None = None) -> None:
        text_before = text_before or self.text_before
        self.cyan(caption, text_before, f": {value}")

    def get_action_value(
        self, caption: str, value: str, show: bool = True
    ) -> ActionValue:
        if show:
            self.value(caption, value)
        return ActionValue(caption, value)

    def head(self, caption: str) -> None:
        self.cyan(caption)

    def head1(self, caption: str) -> None:
        self.magenta(caption)

    def head2(self, caption: str) -> None:
        self.yellow(self.text_color(Fore.BLACK, caption))

    def new_line(self) -> None:
        print()

    def separated_line(self) -> None:
        self.new_line()

    def error_str(self, caption: str) -> str:
        return self.red_str(caption)

    def error(self, caption: str) -> None:
        self.write_line(self.error_str(caption))

    def notify_str(self, caption: str) -> str:
        return self.yellow_str(caption)

    def notify(self, caption: str) -> None:
        self.write_line(self.notify_str(caption))

    def good_str(self, caption: str) -> str:
        return self.green_str(caption)

    def good(self, caption: str) -> str:
        self.write_line(self.good_str(self.text_white(caption)))

    def green_str(
        self, text: str, text_before: str | None = None, text_after: str | None = None
    ) -> str:
        return self.color_str(Back.GREEN, text, text_before, text_after)

    def green(
        self, text: str, text_before: str | None = None, text_after: str | None = None
    ) -> None:
        self.write_line(self.green_str(text, text_before, text_after))

    def yellow_str(
        self, text: str, text_before: str | None = None, text_after: str | None = None
    ) -> str:
        return self.color_str(Back.YELLOW, text, text_before, text_after)

    def yellow(
        self, text: str, text_before: str | None = None, text_after: str | None = None
    ) -> None:
        text_before = text_before or self.text_before
        text_after = text_after or self.text_after
        self.write_line(self.yellow_str(text, text_before, text_after))

    def black_str(
        self, text: str, text_before: str | None = None, text_after: str | None = None
    ) -> str:
        return self.color_str(Back.BLACK, text, text_before, text_after)

    def black(
        self, text: str, text_before: str | None = None, text_after: str | None = None
    ) -> None:
        self.write_line(self.black_str(text, text_before, text_after))

    def white_str(
        self, text: str, text_before: str | None = None, text_after: str | None = None
    ) -> str:
        return self.color_str(Back.WHITE, text, text_before, text_after)

    def white(
        self, text: str, text_before: str | None = None, text_after: str | None = None
    ) -> None:
        self.write_line(self.white_str(text, text_before, text_after))

    def draw_line(
        self, color: str = Back.LIGHTBLUE_EX, char: str = " ", width: int = 80
    ) -> None:
        self.write_line("") if color is None else self.color(color, char * width)

    def line(self) -> None:
        self.new_line()
        self.draw_line(Back.WHITE, self.text_color(Fore.BLACK, "_"), width=128)
        self.new_line()

    def magenta_str(
        self, text: str, text_before: str | None = None, text_after: str | None = None
    ) -> str:
        return self.color_str(Back.LIGHTMAGENTA_EX, text, text_before, text_after)

    def magenta(
        self, text: str, text_before: str | None = None, text_after: str | None = None
    ) -> None:
        self.write_line(self.magenta_str(text, text_before, text_after))

    def cyan(
        self, text: str, text_before: str | None = None, text_after: str | None = None
    ) -> None:
        self.write_line(self.cyan_str(text, text_before, text_after))

    def cyan_str(
        self, text: str, text_before: str | None = None, text_after: str | None = None
    ) -> str:
        return self.color_str(Back.CYAN, text, text_before, text_after)

    def red(
        self, text: str, text_before: str | None = None, text_after: str | None = None
    ) -> None:
        self.write_line(self.red_str(text, text_before, text_after))

    def red_str(
        self, text: str, text_before: str | None = None, text_after: str | None = None
    ) -> str:
        return self.color_str(Back.LIGHTRED_EX, text, text_before, text_after)

    def blue(
        self, text: str, text_before: str | None = None, text_after: str | None = None
    ) -> None:
        self.write_line(self.blue_str(text, text_before, text_after))

    def blue_str(
        self, text: str, text_before: str | None = None, text_after: str | None = None
    ) -> str:
        return self.color_str(Back.BLUE, text, text_before, text_after)

    def bright(
        self, text: str, text_before: str | None = None, text_after: str | None = None
    ) -> None:
        self.write_line(self.bright_str(text, text_before, text_after))

    def bright_str(
        self, text: str, text_before: str | None = None, text_after: str | None = None
    ) -> str:
        return self.color_str(Style.BRIGHT, text, text_before, text_after)

    @staticmethod
    def get_number(value: int) -> str:
        return CONST.VISUAL.NUMBER_SYMBOLS[value]

    def header(self, caption: str) -> None:
        self.head2(caption)

    @contextmanager
    def make_separated_lines(self) -> bool:
        yield True

    def write_result(
        self,
        result: Result[T],
        use_index: bool = True,
        item_separator: str = "\n",
        empty_result_text: str = "Не найдено",
        separated_result_item: bool = True,
        label_function: Callable[[Any, int], str | list[str]] | None = None,
        data_label_function: Callable[[int, FieldItem, T, Any], tuple[bool, str]]
        | None = None,
        title: str | None = None,
        separated_all: bool = False,
    ) -> None:
        data: list = DataTool.as_list(result.data)
        result_string_list: list[str] | None = None
        if e(data):
            self.new_line()
            self.write_line(empty_result_text)
        else:
            if ne(title):
                self.write_line(self.b(title))
            with self.make_indent(2, True):
                for index, data_item in enumerate(data):
                    result_string_list = []
                    if use_index and len(data) > 1:
                        result_string_list.append(
                            f"{self.text_before}{str(index + 1)}:"
                        )
                    if n(label_function):
                        for field_item in result.fields.list:
                            field: FieldItem = field_item
                            if not field.visible:
                                continue
                            item_data_value: str | None = None
                            if isinstance(data_item, dict):
                                item_data_value = data_item[field.name]
                            elif dataclasses.is_dataclass(data_item):
                                item_data_value = data_item.__getattribute__(field.name)
                            item_data_value = (
                                item_data_value
                                if e(item_data_value)
                                else PIH.DATA.FORMAT.by_formatter_name(
                                    field.data_formatter, item_data_value
                                )
                                or field.data_formatter.format(data=item_data_value)
                            )
                            if e(item_data_value):
                                if data_label_function is None:
                                    continue
                            default_value_label_function: Callable[
                                [int, FieldItem, Result[T], Any], tuple[bool, str]
                            ] = lambda _, field, __, data_value: (
                                True,
                                f"{self.bold(field.caption)}: {data_value}",
                            )
                            result_data_label_function: Callable[
                                [int, FieldItem, T, Any], tuple[bool, str]
                            ] = (data_label_function or default_value_label_function)
                            label_value_result: tuple[
                                bool, str | None
                            ] = result_data_label_function(
                                index, field, data_item, item_data_value
                            )
                            label_value: str | None = None
                            if nn(label_value_result[0]):
                                if label_value_result[0] == True:
                                    label_value = label_value_result[1]
                                    if n(label_value) and nn(field.default_value):
                                        label_value = field_item.default_value
                                else:
                                    label_value = default_value_label_function(
                                        None, field, None, item_data_value
                                    )[1]
                            if ne(label_value):
                                result_string_list.append(label_value)
                    else:
                        result_string_list += DataTool.as_list(
                            label_function(data_item, index)
                        )
                    if separated_result_item:
                        self.separated_line()
                    if separated_all:
                        with self.make_separated_lines():
                            for line in result_string_list:
                                self.write_line(line)
                    else:
                        self.write_line(j(result_string_list, item_separator))

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def pih_title(self) -> None:
        self.cyan(self.text_color(Fore.WHITE, "███ ███ █┼█"))
        self.cyan(self.text_color(Fore.WHITE, "█▄█ ┼█┼ █▄█"))
        self.cyan(
            self.text_color(Fore.WHITE, "█┼┼ ▄█▄ █┼█")
            + self.text_color(Fore.BLACK, f" {PIH.VERSION.value}")
        )
        self.new_line()

    def rpc_service_header(self, host: str, port: int, description: str) -> None:
        self.blue("PIH service")
        self.blue(f"Version: {PIH.VERSION.value}")
        self.green(f"Service host: {host}")
        self.green(f"Service port: {port}")
        self.green(f"Service name: {description}")

    def service_header(self, information: ServiceInformation) -> None:
        self.write_line("")
        self.pih_title()
        self.blue("Service starting...")
        self.write_line("")
        self.green(f"Service name: {information.name}")
        self.set_indent(1)
        if information.isolated:
            self.blue(f"[Isolate]")
        self.value("Host", PIH.DATA.FORMAT.donain(information.host))
        self.value("Port", information.port)
        self.value("PID process", information.pid)
        self.set_indent(0)

    def free_marks(
        self,
        show_guest_marks: bool,
        use_index: bool = False,
        sort_by_tab_number: bool = True,
    ) -> None:
        def sort_function(item: Mark) -> Any:
            return item.TabNumber if sort_by_tab_number else item.GroupName

        self.table_with_caption_first_title_is_centered(
            ResultTool.sort(sort_function, PIH.RESULT.MARK.free_list(show_guest_marks)),
            "Свободные карты доступа:",
            use_index,
        )

    def guest_marks(self, use_index: bool = False) -> None:
        mark_list_result: Result[list[Mark]] = PIH.RESULT.MARK.free_list(True)
        mark_list_result.fields.visible(FIELD_NAME_COLLECTION.GROUP_NAME, False)

        def filter_function(item: Mark) -> bool:
            return EnumTool.get(MarkType, item.type) == MarkType.GUEST

        ResultTool.filter(filter_function, mark_list_result)
        self.table_with_caption_first_title_is_centered(
            mark_list_result, "Гостевые карты доступа:", use_index
        )

    def temporary_candidate_for_mark(self, mark: Mark) -> None:
        self.mark.result(
            Result(FIELD_COLLECTION.ORION.FREE_MARK, [mark]), "Временная карта"
        )

    def free_marks_group_statistics(
        self, use_index: bool = False, show_guest_marks: bool | None = None
    ) -> None:
        self.free_marks_group_statistics_for_result(
            PIH.RESULT.MARK.free_marks_group_statistics(show_guest_marks), use_index
        )

    def free_marks_by_group(self, group: dict, use_index: bool = False) -> None:
        self.free_marks_by_group_for_result(
            PIH.RESULT.MARK.free_marks_by_group_id(group), group, use_index
        )

    def free_marks_group_statistics_for_result(
        self, result: Result, use_index: bool
    ) -> None:
        self.table_with_caption_last_title_is_centered(
            result, "Свободные карты доступа:", use_index
        )

    def free_marks_by_group_for_result(
        self, group: MarkGroup, result: Result, use_index: bool
    ) -> None:
        group_name: str = group.GroupName
        self.table_with_caption_last_title_is_centered(
            result,
            js(("Свободные карты доступа для группы доступа", j((b(group_name), ":")))),
            use_index,
        )

    def temporary_marks(
        self,
        use_index: bool = False,
    ) -> None:
        def modify_table(table: PrettyTable, caption_list: list[str]):
            table.align[caption_list[0]] = "c"
            table.align[caption_list[1]] = "c"

        self.table_with_caption(
            PIH.RESULT.MARK.temporary_list(),
            "Список временных карт:",
            use_index,
            modify_table,
        )

    def containers_for_result(self, result: Result, use_index: bool = False) -> None:
        self.table_with_caption(result, "Подразделение:", use_index)

    def table_with_caption_first_title_is_centered(
        self,
        result: Result,
        caption: str,
        use_index: bool = False,
        label_function: Callable = None,
    ) -> None:
        def modify_table(table: PrettyTable, caption_list: list[str]):
            table.align[caption_list[int(use_index)]] = "c"

        self.table_with_caption(
            result, caption, use_index, modify_table, label_function
        )

    def table_with_caption_last_title_is_centered(
        self,
        result: Result,
        caption: str,
        use_index: bool = False,
        label_function: Callable = None,
    ) -> None:
        def modify_table(table: PrettyTable, caption_list: list[str]):
            table.align[caption_list[-1]] = "c"

        self.table_with_caption(
            result, caption, use_index, modify_table, label_function
        )

    def table_with_caption(
        self,
        result: Any,
        caption: str | None = None,
        use_index: bool = False,
        modify_table_function: Callable | None = None,
        label_function: Callable | None = None,
    ) -> None:
        if caption is not None:
            self.cyan(caption)
        is_result_type: bool = isinstance(result, Result)
        field_list = (
            result.fields if is_result_type else ResultTool.unpack_fields(result)
        )
        data: Any = result.data if is_result_type else ResultTool.unpack_data(result)
        if e(data):
            self.error("Не найдено!")
        else:
            if not isinstance(data, list):
                data = [data]
            if len(data) == 1:
                use_index = False
            if use_index:
                field_list.list.insert(0, FIELD_COLLECTION.INDEX)
            caption_list: list = field_list.get_caption_list()

            def create_table(caption_list: list[str]) -> PrettyTable:
                from prettytable.colortable import ColorTable, Themes

                table: ColorTable = ColorTable(caption_list, theme=Themes.OCEAN)
                table.align = "l"
                if use_index:
                    table.align[caption_list[0]] = "c"
                return table

            table: PrettyTable = create_table(caption_list)
            if modify_table_function is not None:
                modify_table_function(table, caption_list)
            for index, item in enumerate(data):
                row_data: list = []
                for field_item_obj in field_list.get_list():
                    field_item: FieldItem = field_item_obj
                    if field_item.visible:
                        if field_item.name == FIELD_COLLECTION.INDEX.name:
                            row_data.append(str(index + 1))
                        elif not isinstance(item, dict):
                            if label_function is not None:
                                modified_item_data = label_function(field_item, item)
                                if modified_item_data is None:
                                    modified_item_data = getattr(item, field_item.name)
                                row_data.append(
                                    DataTool.check(
                                        modified_item_data,
                                        lambda: modified_item_data,
                                        "",
                                    )
                                    if modified_item_data is None
                                    else modified_item_data
                                )
                            else:
                                item_data = getattr(item, field_item.name)
                                row_data.append(
                                    DataTool.check(item_data, lambda: item_data, "")
                                )
                        elif field_item.name in item:
                            item_data = item[field_item.name]
                            if label_function is not None:
                                modified_item_data = label_function(field_item, item)
                                row_data.append(
                                    item_data
                                    if modified_item_data is None
                                    else modified_item_data
                                )
                            else:
                                row_data.append(item_data)
                table.add_row(row_data)
            print(table)
            table.clear()

    def template_users_for_result(self, data: dict, use_index: bool = False) -> None:
        def data_handler(field_item: FieldItem, item: User) -> Any:
            filed_name = field_item.name
            if filed_name == FIELD_NAME_COLLECTION.DESCRIPTION:
                return item.description
            return None

        self.table_with_caption(
            data,
            "Шаблоны для создания аккаунта пользователя:",
            use_index,
            None,
            data_handler,
        )

