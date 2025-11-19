import flet as ft
from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw, ImageFont
import io
import base64



def main(page: ft.Page):
    page.title = "Redactor Pro"
    page.theme_mode = ft.ThemeMode.DARK
    
    original_image = None
    current_image = None
    image_path = None
    
    image_display = ft.Image(
        width=600,
        height=400,
        fit=ft.ImageFit.CONTAIN,
        visible=False
    )
    
    
    
    def buttons_on():
        blur_slider.disabled= False
        contrast_slider.disabled = False
        brightness_slider.disabled = False
        saturation_slider.disabled = False
        
        sepia_btn.disabled = False
        emboss_btn.disabled = False
        sharpen_btn.disabled = False
        countour_btn.disabled = False
        black_white_btn.disabled = False
        rotate_on_90_btn.disabled = False
        rotate_180_btn.disabled = False
        resize_btn.disabled = False
        flip_vertical_btn.disabled = False
        flip_horizontal_btn.disabled = False
        vignette_btn.disabled = False
        reset_btn.disabled = False
    
    
    
    def update_display():
        if current_image:
            buffered = io.BytesIO()
            img_to_save = current_image
                
            img_to_save.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()
            image_display.src_base64 = img_base64
            image_display.visible = True
            buttons_on()
            page.update()


    
    
    def on_file_picker_result(e: ft.FilePickerResultEvent):
        nonlocal original_image, current_image, image_path
        if e.files:
            image_path = e.files[0].path
            original_image = Image.open(image_path)
            current_image = original_image.copy()
            update_display()
            
            page.snack_bar = ft.SnackBar(content=ft.Text("Изображение загружено!"))
            page.snack_bar.open = True
            page.update()

    
    file_picker = ft.FilePicker(on_result=on_file_picker_result)
    page.overlay.append(file_picker)
    
    
    def open_image(e):
        file_picker.pick_files(
            allow_multiple=False, 
            allowed_extensions=["jpg", "jpeg", "png", "bmp", "gif"]
        )
    
    
    def save_image(e):
        if current_image:
                
                current_image.save("edited_image.png")
                page.snack_bar = ft.SnackBar(content=ft.Text("Изображение сохранено как edited_image.png!"))
                page.snack_bar.open = True
                
                page.update()


    
    def apply_grayscale(e):
        nonlocal current_image
        if current_image:
            current_image = ImageOps.grayscale(current_image)
            update_display()
    
    
    def apply_sepia(e):
        nonlocal current_image
        if current_image:
            # Создаем сепию-фильтр
            width, height = current_image.size
            pixels = current_image.load()
            
            for py in range(height):
                for px in range(width):
                    r, g, b = current_image.getpixel((px, py))
                    
                    tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                    tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                    tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                    
                    pixels[px, py] = (
                        min(255, tr),
                        min(255, tg), 
                        min(255, tb)
                    )
            update_display()
    


    def apply_sharpen(e):
        nonlocal current_image
        if current_image:
            current_image = current_image.filter(ImageFilter.SHARPEN)
            update_display()
    
    def apply_emboss(e):
        nonlocal current_image
        if current_image:
            current_image = current_image.filter(ImageFilter.EMBOSS)
            update_display()
    
    def apply_contour(e):
        nonlocal current_image
        if current_image:
            current_image = current_image.filter(ImageFilter.CONTOUR)
            update_display()
    

    
    def adjust_brightness(e):
        nonlocal current_image
        if current_image:
            value = e.control.value
            factor = value / 50.0
            enhancer = ImageEnhance.Brightness(original_image)
            bright_image = enhancer.enhance(factor)
            buf = io.BytesIO()
            bright_image.save(buf, format='JPEG')
            img_bytes = buf.getvalue()
            current_image = bright_image
            update_display()
    
    
    def adjust_contrast(e):
        nonlocal current_image
        if current_image:
            contrast_level = e.control.value / 100.0
            enhancer = ImageEnhance.Contrast(original_image)
            current_image = enhancer.enhance(contrast_level)
            update_display()
    
    
    def adjust_saturation(e):
        nonlocal current_image
        if current_image:
            saturation_level = e.control.value / 100.
            enhancer = ImageEnhance.Color(original_image)
            current_image = enhancer.enhance(saturation_level)
            update_display()

    
    def adjust_blur(e):
        nonlocal current_image
        if current_image:
            blur_radius = e.control.value
            if blur_radius == 0:
                current_image = original_image.copy()
            else:
                current_image = original_image.filter(
                    ImageFilter.GaussianBlur(radius=blur_radius)
                )
            update_display()


    

    
    def rotate_90(e):
        nonlocal current_image
        if current_image:
            current_image = current_image.rotate(90, expand=True)
            update_display()
    
    
    def rotate_180(e):
        nonlocal current_image
        if current_image:
            current_image = current_image.rotate(180, expand=True)
            update_display()
    
    
    def flip_horizontal(e):
        nonlocal current_image
        if current_image:
            current_image = current_image.transpose(Image.FLIP_LEFT_RIGHT)
            update_display()
    
    
    def flip_vertical(e):
        nonlocal current_image
        if current_image:
            current_image = current_image.transpose(Image.FLIP_TOP_BOTTOM)
            update_display()
     
    
    def add_vignette(e):
        nonlocal current_image
        if current_image:
            # Создаем маску для виньетки
            width, height = current_image.size
            mask = Image.new('L', (width, height), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse([-100, -100, width+100, height+100], fill=255)
            mask = mask.filter(ImageFilter.GaussianBlur(100))
            dark = Image.new('RGB', (width, height), (0, 0, 0))
            current_image = Image.composite(current_image, dark, mask)
            update_display()
    

    
    
    
    
    def reset_image(e):
        nonlocal current_image
        if original_image:
            current_image = original_image.copy()
            brightness_slider.value = 100
            contrast_slider.value = 100
            saturation_slider.value = 100
            blur_slider.value = 0
            update_display()
    
    def resize_image_func(e):
        nonlocal current_image
        if current_image:
            width, height = current_image.size
            new_size = (width // 2, height // 2)
            current_image = current_image.resize(new_size, Image.Resampling.LANCZOS)
            update_display()
    
    
    
    
    
    
    brightness_slider = ft.Slider(
        min=10, 
        max=200, 
        value=100,
        divisions=190,
        label="Яркость: {value}",
        on_change=adjust_brightness,
        width=200,
        disabled=True
    )
    
    contrast_slider = ft.Slider(
        min=0, 
        max=200, 
        value=100,
        divisions=200,
        label="Контраст: {value}",
        on_change=adjust_contrast,
        width=200,
        disabled=True
    )
    
    saturation_slider = ft.Slider(
        min=0, 
        max=200, 
        value=100,
        divisions=190,
        label="Насыщенность: {value}",
        on_change=adjust_saturation,
        width=200,
        disabled=True
    )
    
    blur_slider = ft.Slider(
        min=0,          
        max=20,           
        value=0,         
        divisions=200,    
        label="Размытие: {value}",
        on_change=adjust_blur,
        width=200,
        disabled=True
    )
    

    open_btn = ft.ElevatedButton("Открыть", icon = ft.Icons.FILE_OPEN, on_click=open_image)
    save_btn = ft.ElevatedButton("Сохранить", icon=ft.Icons.SAVE_AS, on_click=save_image, disabled=True)
    black_white_btn = ft.ElevatedButton("Ч/Б", icon = ft.Icons.BALANCE, on_click=apply_grayscale, disabled=True)
    sepia_btn = ft.ElevatedButton("Сепия", color=ft.Colors.BROWN, on_click=apply_sepia, disabled=True)
    sharpen_btn = ft.ElevatedButton("🔍 Резкость", on_click=apply_sharpen, disabled=True)
    emboss_btn = ft.ElevatedButton("🏔️ Тиснение", on_click=apply_emboss, disabled=True)
    countour_btn = ft.ElevatedButton("📐 Контур", on_click=apply_contour, disabled=True)
    rotate_on_90_btn = ft.ElevatedButton("90°", icon = ft.Icons.ROTATE_90_DEGREES_CCW, on_click=rotate_90, disabled=True)
    rotate_180_btn = ft.ElevatedButton("180°",icon = ft.Icons.ROTATE_90_DEGREES_CCW, on_click=rotate_180, disabled=True)
    flip_horizontal_btn = ft.ElevatedButton("↔ Отразить", on_click=flip_horizontal, disabled=True)
    flip_vertical_btn = ft.ElevatedButton("↕ Перевернуть", on_click=flip_vertical, disabled=True)
    vignette_btn = ft.ElevatedButton("Виньетка", on_click=add_vignette, disabled=True)
    resize_btn = ft.ElevatedButton("Уменьшить", icon=ft.Icons.DONUT_SMALL, on_click=resize_image_func, disabled=True)
    reset_btn = ft.ElevatedButton("Сбросить все",icon=ft.Icons.REPEAT, on_click=reset_image, disabled=True)
    
    
    
    tools_column = ft.Column([
        ft.Text("Фоторедактор", size=20, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        
        
        
        ft.Text("Файл:", weight=ft.FontWeight.BOLD),
        ft.Row([
            open_btn,
            save_btn
        ]),
        
        
        
        ft.Text("Фильтры:", weight=ft.FontWeight.BOLD),
        ft.Row([
            black_white_btn,
            sepia_btn
        ]),
        
        
        
        ft.Row([
            sharpen_btn,
            vignette_btn
        ]),
        ft.Row([
            emboss_btn,
            countour_btn
        ]),
        
        
        
        ft.Text("Коррекция:", weight=ft.FontWeight.BOLD),
        brightness_slider,
        contrast_slider,
        saturation_slider,
        blur_slider,
        
        
        
        ft.Text("Трансформации:", weight=ft.FontWeight.BOLD),
        ft.Row([
            rotate_on_90_btn,
            rotate_180_btn
        ]),
        ft.Row([
            flip_horizontal_btn,
            flip_vertical_btn
        ]),
        ft.Row([resize_btn]),
        ft.Row([reset_btn])
        
        
    ], scroll=ft.ScrollMode.ADAPTIVE, height=700)
    

    
    
    
    page.add(
        ft.Row([
            ft.Container(
                content=tools_column,
                width=300,
                padding=15,
                bgcolor=ft.Colors.GREY_900,
                border_radius=10,
            ),
            
            
            
            ft.Column([
                ft.Container(
                    content=image_display,
                    alignment=ft.alignment.center,
                    padding=20,
                    bgcolor=ft.Colors.GREY_900,
                    border_radius=10,
                    expand=True,
                )
            ], expand=True)
        ], expand=True)
    )




if __name__ == "__main__":
    ft.app(
        target=main,
        view=ft.WEB_BROWSER,
        port=8500
    )