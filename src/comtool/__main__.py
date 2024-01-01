from __future__ import annotations

import logging
from datetime import datetime
from io import StringIO
from typing import Optional

import typer
from prompt_toolkit.application import Application, get_app
from prompt_toolkit.document import Document
from prompt_toolkit.filters import Condition
from prompt_toolkit.formatted_text import HTML, to_formatted_text
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, VSplit, Window, WindowAlign
from prompt_toolkit.layout.dimension import Dimension
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.processors import ConditionalProcessor, Processor, Transformation, TransformationInput
from prompt_toolkit.validation import ConditionalValidator, ValidationError, Validator
from prompt_toolkit.widgets import Label, SearchToolbar, TextArea, ValidationToolbar
from serial import Serial, SerialException
from serial.threaded import Protocol, ReaderThread

from comtool.__about__ import __project_name__, __version__
from comtool.widgets.formatted_text_area import FormattedTextArea

app = typer.Typer(rich_markup_mode="markdown")
context = {
    "hex_mode": False,
    "serial": None,
}


class MyFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):  # noqa: N802
        if not datefmt:
            return super().formatTime(record, datefmt)
        # Convert milliseconds to microseconds
        datefmt = datefmt.replace("%f", "%03d" % (record.msecs))
        return datetime.fromtimestamp(record.created).strftime(datefmt)  # noqa: DTZ006


logging.basicConfig(format="%(message)s", level=logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logs = StringIO()
handler = logging.StreamHandler(logs)
handler.setLevel(logging.INFO)
formatter = MyFormatter("<ansiyellow>[%(asctime)s]</ansiyellow> %(message)s", "%Y-%m-%d %H:%M:%S.%f")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.propagate = False


def get_and_clear_log(log: StringIO) -> str:
    value = log.getvalue()
    log.seek(0)
    log.truncate()
    return value


def update_output_field() -> None:
    output_field.formatted_text += to_formatted_text(HTML(get_and_clear_log(logs)))
    output_field.buffer.cursor_position = len(output_field.buffer.text)


def exit_application() -> None:
    app = get_app()
    if app.is_running:
        app.exit()


class MySerial(Protocol):
    def __init__(self):
        self.transport = None
        self.buffer = bytearray()

    def connection_made(self, transport):
        self.transport = transport
        logger.info("<ansiblue>Port Opened</ansiblue>")
        update_output_field()

    def data_received(self, data):
        self.buffer.extend(data)
        if self.transport.serial.in_waiting:
            return
        decoded_buffer = self.buffer.hex(" ").upper() if context["hex_mode"] else self.buffer.decode()
        logger.info("<ansired>RX:</ansired> %s", decoded_buffer)
        update_output_field()
        self.buffer.clear()

    def connection_lost(self, _):
        exit_application()


class HexStringValidator(Validator):
    def validate(self, document: Document) -> None:
        try:
            bytearray.fromhex(document.text)
        except ValueError as exc:
            raise ValidationError(cursor_position=document.cursor_position, message="Invalid Hex String") from exc


class FormatHexStringProcessor(Processor):
    def apply_transformation(self, transformation_input: TransformationInput) -> Transformation:
        def format_hex_string(text: str) -> str:
            filtered_text = "".join(c for c in text.upper() if c in "0123456789ABCDEF")
            return " ".join(filtered_text[i : i + 2] for i in range(0, len(filtered_text), 2))

        formatted_text = format_hex_string(transformation_input.document.text)
        if formatted_text != transformation_input.document.text:
            new_cursor_position = len(format_hex_string(transformation_input.document.text_before_cursor))
            input_field.document = Document(text=formatted_text, cursor_position=new_cursor_position)

        return Transformation(transformation_input.fragments)


header = VSplit(
    [
        Label(text="COMTool", align=WindowAlign.LEFT),
        Label(text=lambda: f"Hex Mode: {'ON' if context['hex_mode'] else 'OFF'}", align=WindowAlign.CENTER),
        Label(text="Press Control-C to Exit", align=WindowAlign.RIGHT),
    ],
    height=Dimension.exact(1),
    style="reverse",
)

output_field = FormattedTextArea(formatted_text="")

search_field = SearchToolbar()

input_field = TextArea(
    multiline=False,
    validator=ConditionalValidator(validator=HexStringValidator(), filter=Condition(lambda: context["hex_mode"])),
    wrap_lines=False,
    height=Dimension.exact(1),
    search_field=search_field,
    prompt=HTML("<ansibrightblack>>>></ansibrightblack> "),
    input_processors=[
        ConditionalProcessor(processor=FormatHexStringProcessor(), filter=Condition(lambda: context["hex_mode"]))
    ],
)

container = HSplit(
    [
        header,
        output_field,
        Window(height=Dimension.exact(1), style="ansicyan bold", char="-"),
        input_field,
        ValidationToolbar(),
        search_field,
    ]
)


def accept(buffer):
    text = buffer.text
    if context["hex_mode"]:
        context["serial"].write(bytearray.fromhex(text))
    else:
        text += "\n"
        context["serial"].write(f"{text}".encode())
    logger.info("<ansigreen>TX:</ansigreen> %s", text)
    update_output_field()


input_field.accept_handler = accept

kb = KeyBindings()


@kb.add("c-c")
def _(_):
    exit_application()


@kb.add("c-t")
def _(_):
    context["hex_mode"] = not context["hex_mode"]


application = Application(
    layout=Layout(container, focused_element=input_field),
    key_bindings=kb,
    full_screen=True,
    mouse_support=True,
)


def version_callback(value: bool):  # noqa: FBT001
    if value:
        print(f"{__project_name__} {__version__}")  # noqa: T201
        raise typer.Exit


@app.command()
def main(
    version: Optional[bool] = typer.Option(None, "--version", callback=version_callback, is_eager=True),  # noqa: ARG001, UP007
    port: str = typer.Option(show_default=False, prompt=True),
    baudrate: int = typer.Option(show_default=False, prompt=True),
    bytesize: int = typer.Option(8, help="5, 6, 7, 8"),
    parity: str = typer.Option("N", help="N: None, E: Even, O: Odd, M: Mark, S: Space"),
    stopbits: int = typer.Option(1, help="1, 1.5, 2"),
    *,
    xonxoff: bool = typer.Option(False, "--xonxoff"),
    rtscts: bool = typer.Option(False, "--rtscts"),
    dsrdtr: bool = typer.Option(False, "--dsrdtr"),
):
    try:
        with Serial(
            port=port,
            baudrate=baudrate,
            bytesize=bytesize,
            parity=parity,
            stopbits=stopbits,
            xonxoff=xonxoff,
            rtscts=rtscts,
            dsrdtr=dsrdtr,
        ) as s:
            context["serial"] = s
            serial_worker = ReaderThread(s, MySerial)
            serial_worker.start()
            application.run()
            serial_worker.stop()
    except (SerialException, ValueError) as exc:
        logging.error(exc)  # noqa: TRY400
    else:
        logging.info("Port Closed. Exiting...")


if __name__ == "__main__":
    app()
