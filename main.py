import random
import time

import flet as ft

from src.td4_flet import Cpu


def main(page: ft.Page):
    page.auto_scroll = True
    # page.vertical_alignment = ft.MainAxisAlignment.START
    page.window_height = 980
    page.window_width = 1000
    page.window_min_width = 600
    page.window_max_width = 600
    leds = [ft.icons.LIGHTBULB_OUTLINE, ft.icons.LIGHTBULB]

    cpu = Cpu()
    output_values = [0] * 4
    input_values = ft.Row(controls=[ft.Checkbox(value=False) for _ in range(4)])

    def output():
        for i in range(4):
            outputs_view.controls[i] = ft.Icon(leds[int(cpu.port.output[i])], size=50)
        for i in range(4):
            register_a_view.controls[i] = ft.Icon(
                leds[cpu.register.a >> (4 - i - 1) & 1], size=50
            )
            register_b_view.controls[i] = ft.Icon(
                leds[cpu.register.b >> (4 - i - 1) & 1], size=50
            )
        pc_text.value = f"Programm Counter: {cpu.pc:04b}"
        carry_text.value = f"Carry flag: {int(cpu.carry)}"
        return

    def execute(e):
        cpu.execute()
        output()
        page.update()

    def load_rom(e):
        # global cpu
        # cpu = Cpu()
        cpu.register.a = 0b0000
        cpu.register.b = 0b0000
        cpu.port.output = "0000"
        cpu.pc = 0
        cpu.carry = False
        # output()
        total = []
        for i in range(16):
            tmp = []
            for j, bit in enumerate(roms[i].controls[:8]):
                if bit.value:
                    tmp.append("1")
                else:
                    tmp.append("0")
            total.append("".join(tmp))
        input_str = ""
        for i in range(4):
            if input_values.controls[i].value:
                input_str += "1"
            else:
                input_str += "0"
        cpu.port.input = int(input_str, 2)

        cpu.rom.load_bin(total)
        output()
        page.update()

        # print(cpu.rom.memory)

    def run_auto(e):
        for _ in range(300):
            time.sleep(0.2)
            # output_randomize("")
            # cpu.execute()
            execute(e)

    def button_clicked(e):
        # print(e)
        total = []
        for i in range(16):
            tmp = []
            for j, bit in enumerate(roms[i].controls):
                if bit.value:
                    tmp.append("1")
                else:
                    tmp.append("0")
            total.append("".join(tmp))
        # page.update()

    def clear_all(e):
        global cpu
        cpu = Cpu()
        for i in range(16):
            for j in range(8):
                roms[i].controls[j].value = False
        load_rom("")
        page.update()

    page.title = "TD4 Emulator"

    roms = [
        ft.Row(controls=[ft.Checkbox(value=False) for _ in range(8)]) for _ in range(16)
    ]
    rom_labels = [ft.Text(f"r{i:02}") for i in range(16)]
    label_and_rom = [ft.Row(controls=[rom_labels[i], roms[i]]) for i in range(16)]

    check_bits = ft.ElevatedButton(text="check", on_click=load_rom)
    clear_bits = ft.ElevatedButton(
        text="clear", on_click=clear_all, color=ft.colors.BLUE_GREY_900
    )
    label = ft.Row(
        controls=[
            ft.Text("       "),
            ft.Row(controls=[ft.Text(f" b{i:02} ") for i in range(7, -1, -1)]),
        ]
    )
    buttons = ft.Row(controls=[check_bits, clear_bits])
    view_roms = ft.Column(controls=label_and_rom)
    outputs_view = ft.Row(
        controls=[ft.Icon(leds[output_values[i]], size=50) for i in range(4)]
    )
    register_a_view = ft.Row(
        controls=[ft.Icon(leds[cpu.register.a >> i & 1], size=50) for i in range(4)]
    )
    register_b_view = ft.Row(
        controls=[ft.Icon(leds[cpu.register.b >> i & 1], size=50) for i in range(4)]
    )
    clock_button = ft.TextButton(text="CLOCK", opacity=100, on_click=execute)
    run_button = ft.TextButton(text="RUN", opacity=100, on_click=run_auto)
    pc_text = ft.Text(f"Programm Counter: {cpu.pc:04b}", size=30)
    carry_text = ft.Text(f"Carry flag: {int(cpu.carry)}", size=30)

    # 組合せ
    col1 = ft.Column(
        controls=[
            ft.Text("ROM", size=50),
            label,
            view_roms,
            ft.Text("INPUTS", size=50),
            input_values,
            buttons,
        ]
    )

    col2 = ft.Column(
        controls=[
            clock_button,
            run_button,
            pc_text,
            carry_text,
            ft.Text("OUTPUTS", size=50),
            outputs_view,
            ft.Text("REGISTER A", size=50),
            register_a_view,
            ft.Text("REGISTER B", size=50),
            register_b_view,
        ],
        alignment=ft.MainAxisAlignment.START,
    )

    page.add(
        ft.Row(
            controls=[
                col1,
                ft.Container(
                    col2,
                    padding=30,
                    ink=True,
                    alignment=ft.alignment.top_center,
                    height=900,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=100,
        )
    )


ft.app(target=main)
