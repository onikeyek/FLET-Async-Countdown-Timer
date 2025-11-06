import flet as ft
import asyncio


class TimerState:
    def __init__(self, duration_seconds):
        self.duration = duration_seconds
        self.remaining = duration_seconds
        self.is_running = False
        self.is_paused = False
        self.task = None


def main(page: ft.Page):
    page.title = "🌿 FocusFlow"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0a0e1a"
    page.padding = 0
    
    # Timer states
    timers = {
        "focus": TimerState(25 * 60),
        "short": TimerState(5 * 60),
        "long": TimerState(15 * 60)
    }
    
    current_timer = "focus"
    
    # Timer colors
    colors = {
        "focus": "#3b82f6",
        "short": "#22c55e",
        "long": "#a855f7"
    }
    
    # UI References
    progress_ring = ft.ProgressRing(
        width=240,
        height=240,
        stroke_width=12,
        value=0,
        color=colors["focus"],
        bgcolor="#1e293b"
    )
    
    time_display = ft.Text(
        "25:00",
        size=56,
        weight=ft.FontWeight.BOLD,
        color="#ffffff"
    )
    
    timer_title = ft.Text(
        "Focus Session",
        size=18,
        color="#64748b",
        weight=ft.FontWeight.W_500
    )
    
    start_btn = ft.Container(
        content=ft.Text("Start", size=16, weight=ft.FontWeight.W_500, color="#ffffff"),
        bgcolor=colors["focus"],
        border_radius=12,
        padding=ft.padding.symmetric(horizontal=80, vertical=15),
        on_click=lambda _: start_timer(),
        ink=True,
    )
    
    pause_btn = ft.Container(
        content=ft.Icon(ft.Icons.PAUSE, color="#ffffff", size=28),
        width=56,
        height=56,
        border_radius=28,
        bgcolor="#1e293b",
        alignment=ft.alignment.center,
        on_click=lambda _: toggle_pause(),
        visible=False,
        ink=True,
    )
    
    reset_btn = ft.Container(
        content=ft.Icon(ft.Icons.REFRESH, color="#64748b", size=28),
        width=56,
        height=56,
        border_radius=28,
        bgcolor="#1e293b",
        alignment=ft.alignment.center,
        on_click=lambda _: reset_timer(),
        ink=True,
    )
    
    skip_btn = ft.Container(
        content=ft.Icon(ft.Icons.SKIP_NEXT, color="#64748b", size=28),
        width=56,
        height=56,
        border_radius=28,
        bgcolor="#1e293b",
        alignment=ft.alignment.center,
        visible=False,
        ink=True,
    )
    
    def format_time(seconds):
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins:02d}:{secs:02d}"
    
    def update_ui():
        timer = timers[current_timer]
        time_display.value = format_time(timer.remaining)
        
        if timer.duration > 0:
            progress_ring.value = 1 - (timer.remaining / timer.duration)
        else:
            progress_ring.value = 0
        
        if timer.remaining == 0 and timer.is_running:
            timer.is_running = False
            start_btn.visible = True
            pause_btn.visible = False
            skip_btn.visible = False
        
        # Update button visibility based on state
        if timer.is_running:
            start_btn.visible = False
            pause_btn.visible = True
            skip_btn.visible = True
            pause_btn.content = ft.Icon(
                ft.Icons.PLAY_ARROW if timer.is_paused else ft.Icons.PAUSE,
                color="#ffffff",
                size=28
            )
        else:
            start_btn.visible = True
            pause_btn.visible = False
            skip_btn.visible = False
        
        page.update()
    
    async def countdown_task(timer_key):
        timer = timers[timer_key]
        while timer.is_running and timer.remaining > 0:
            if not timer.is_paused:
                await asyncio.sleep(1)
                timer.remaining -= 1
                if timer_key == current_timer:
                    update_ui()
            else:
                await asyncio.sleep(0.1)
        
        if timer.remaining == 0 and timer_key == current_timer:
            update_ui()
    
    def start_timer():
        timer = timers[current_timer]
        if not timer.is_running:
            timer.is_running = True
            timer.is_paused = False
            timer.task = page.run_task(countdown_task, current_timer)
            update_ui()
    
    def toggle_pause():
        timer = timers[current_timer]
        if timer.is_running:
            timer.is_paused = not timer.is_paused
            update_ui()
    
    def reset_timer():
        timer = timers[current_timer]
        timer.is_running = False
        timer.is_paused = False
        timer.remaining = timer.duration
        update_ui()
    
    def switch_timer(timer_key, title):
        nonlocal current_timer
        current_timer = timer_key
        progress_ring.color = colors[timer_key]
        start_btn.bgcolor = colors[timer_key]
        timer_title.value = title
        
        timer = timers[current_timer]
        update_ui()
        page.close(drawer)
        page.update()
    
    # Bottom Navigation Bar
    nav_bar = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.Icons.TIMER_OUTLINED, color=colors["focus"], size=24),
                            ft.Text("Timer", size=12, color=colors["focus"])
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=4,
                    ),
                    expand=1,
                    ink=True,
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.Icons.GRID_VIEW_OUTLINED, color="#64748b", size=24),
                            ft.Text("Projects", size=12, color="#64748b")
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=4,
                    ),
                    expand=1,
                    ink=True,
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.Icons.BAR_CHART_OUTLINED, color="#64748b", size=24),
                            ft.Text("Stats", size=12, color="#64748b")
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=4,
                    ),
                    expand=1,
                    ink=True,
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.Icons.SETTINGS_OUTLINED, color="#64748b", size=24),
                            ft.Text("Settings", size=12, color="#64748b")
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=4,
                    ),
                    expand=1,
                    ink=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        ),
        bgcolor="#0f172a",
        padding=ft.padding.symmetric(vertical=12),
        border=ft.border.only(top=ft.BorderSide(1, "#1e293b"))
    )
    
    # Navigation Drawer
    drawer = ft.NavigationDrawer(
        bgcolor="#0f172a",
        controls=[
            ft.Container(height=20),
            ft.Row(
                controls=[
                    ft.Icon(ft.Icons.CIRCLE, color=colors["focus"], size=24),
                    ft.Text("FocusFlow", size=24, weight=ft.FontWeight.BOLD, color="#ffffff"),
                    ft.Container(expand=1),
                    ft.IconButton(
                        icon=ft.Icons.CLOSE,
                        icon_color="#64748b",
                        on_click=lambda _: page.close(drawer),
                    ),
                ],
                spacing=10,
            ),
            ft.Container(height=30),
            ft.Text("Timers", size=14, color="#64748b", weight=ft.FontWeight.W_500),
            ft.Container(height=10),
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.CIRCLE, color=colors["focus"], size=20),
                        ft.Text("Focus Session", size=16, color="#ffffff")
                    ],
                    spacing=12,
                ),
                bgcolor="#1e293b",
                border_radius=8,
                padding=12,
                ink=True,
                on_click=lambda _: switch_timer("focus", "Focus Session")
            ),
            ft.Container(height=8),
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.COFFEE_OUTLINED, color="#64748b", size=20),
                        ft.Text("Short Break", size=16, color="#94a3b8")
                    ],
                    spacing=12,
                ),
                border_radius=8,
                padding=12,
                ink=True,
                on_click=lambda _: switch_timer("short", "Short Break")
            ),
            ft.Container(height=8),
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.NIGHTLIGHT_OUTLINED, color="#64748b", size=20),
                        ft.Text("Long Break", size=16, color="#94a3b8")
                    ],
                    spacing=12,
                ),
                border_radius=8,
                padding=12,
                ink=True,
                on_click=lambda _: switch_timer("long", "Long Break")
            ),
            ft.Container(height=30),
            ft.Divider(color="#1e293b"),
            ft.Container(height=10),
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.PAUSE_CIRCLE_OUTLINE, color="#64748b", size=20),
                        ft.Text("Pause Timer", size=16, color="#94a3b8")
                    ],
                    spacing=12,
                ),
                border_radius=8,
                padding=12,
                ink=True,
                on_click=lambda _: (toggle_pause(), page.close(drawer))
            ),
        ],
    )
    
    page.drawer = drawer
    
    # Main content
    content = ft.Column(
        controls=[
            # Top bar
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.MENU,
                            icon_color="#ffffff",
                            on_click=lambda _: page.open(drawer),
                        ),
                        ft.Container(expand=1),
                        timer_title,
                        ft.Container(expand=1),
                        ft.Container(width=48),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                padding=ft.padding.only(left=8, right=8, top=8, bottom=0),
            ),
            # Timer display
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Stack(
                                controls=[
                                    progress_ring,
                                    ft.Container(
                                        content=time_display,
                                        alignment=ft.alignment.center,
                                        width=240,
                                        height=240,
                                    )
                                ],
                                alignment=ft.alignment.center,
                            ),
                            margin=ft.margin.only(top=80),
                        ),
                        ft.Container(height=60),
                        # Control buttons
                        ft.Row(
                            controls=[
                                reset_btn,
                                pause_btn,
                                skip_btn,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=20,
                            visible=False,
                        ),
                        start_btn,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                expand=True,
            ),
            nav_bar,
        ],
        spacing=0,
        expand=True,
    )
    
    # Show/hide control buttons row
    controls_row = content.controls[1].content.controls[2]
    
    def update_ui_enhanced():
        timer = timers[current_timer]
        time_display.value = format_time(timer.remaining)
        
        if timer.duration > 0:
            progress_ring.value = 1 - (timer.remaining / timer.duration)
        else:
            progress_ring.value = 0
        
        if timer.remaining == 0 and timer.is_running:
            timer.is_running = False
            start_btn.visible = True
            controls_row.visible = False
        
        if timer.is_running:
            start_btn.visible = False
            controls_row.visible = True
            pause_btn.content = ft.Icon(
                ft.Icons.PLAY_ARROW if timer.is_paused else ft.Icons.PAUSE,
                color="#ffffff",
                size=28
            )
        else:
            start_btn.visible = True
            controls_row.visible = False
        
        page.update()
    
    # Override update_ui
    update_ui = update_ui_enhanced
    
    page.add(content)


ft.app(target=main)