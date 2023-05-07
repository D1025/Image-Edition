from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QSlider, QFileDialog, QComboBox, QProgressBar
from PySide6.QtGui import QPixmap, QImage
from PIL import Image, ImageQt
from PySide6.QtCore import Qt
import functions
import histogram as hs
import filtr as f
import statyczne as s

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.alpha = 100
        self.brightness = 0
        self.mieszanie = 0
        self.kierunek = 10
        self.tryb = 0
        self.filtrtryb = 0
        self.filtrlist = ['Robets', 'Prewitt', 'Sobel', 'Laprace']
        self.blendlist = ['Additive', 'Subtractive', 'Difference', 'Multiply', 'Screen',
                               'Negation', 'Darken', 'Lighten', 'Exclusion', 'Overlay', 
                               'Hard light', 'Soft light', 'Color dodge', 'Color burn',
                               'Reflect', 'Transparency']
        self.tryblist = ['Liniowa', 'Kwadratowa']
        self.mask_size = 3

        self.pil_image = None
        self.second_image = None
        
        
        
        # Utwórz etykietę, która będzie wyświetlać obraz
        self.image_label = QLabel(self)
        self.setCentralWidget(self.image_label)

        # Utwórz przycisk i przypisz mu funkcję obsługi zdarzeń
        self.button = QPushButton("Otwórz obraz", self)
        self.button.clicked.connect(self.load_image)
        
        self.btn_negatyw = QPushButton("Negatyw", self)
        self.btn_negatyw.clicked.connect(self.btn_negatyw_click)
        
        self.btn_hist = QPushButton("Histogram", self)
        self.btn_hist.clicked.connect(self.btn_hist_click)
        
        
        self.options = QComboBox(self)
        self.options.addItems(self.blendlist)
        self.options.currentIndexChanged.connect(self.handle_option_changed)
        
        self.filtr_options = QComboBox(self)
        self.filtr_options.addItems(self.filtrlist)
        self.filtr_options.currentIndexChanged.connect(self.filtr_options_changed)
        
        self.bright_options = QComboBox(self)
        self.bright_options.addItems(self.tryblist)
        self.bright_options.currentIndexChanged.connect(self.bright_handle_option_changed)

        self.apply_button = QPushButton('2 obraz', self)
        self.apply_button.clicked.connect(self.apply_option)

        # Utwórz slider i przypisz mu funkcję obsługi zdarzeń
        self.create_slider()
        
        self.slider_alpha = QSlider(Qt.Horizontal, self)
        self.slider_alpha.setRange(0, 100)
        self.slider_alpha.setValue(100)
        self.slider_alpha.setTickPosition(QSlider.TicksBothSides)
        self.slider_alpha.setTickInterval(1)
        self.slider_alpha.valueChanged.connect(self.set_alpha)
        self.slider_alpha.setVisible(False)
        
        self.slider_kierunek = QSlider(Qt.Vertical, self)
        self.slider_kierunek.setRange(-10,10)
        self.slider_kierunek.setValue(10)
        self.slider_kierunek.setTickInterval(1)
        self.slider_kierunek.valueChanged.connect(self.set_kierunek)
        
        self.btn_pion = QPushButton('Pionowy', self)
        self.btn_poz = QPushButton('Poziomy', self)
        self.btn_pion.clicked.connect(self.btn_pion_clicked)
        self.btn_poz.clicked.connect(self.btn_poz_clicked)
        
        self.btn_set = QPushButton('Uzyj aktualnego', self)
        self.btn_set.clicked.connect(self.USEACTUAL)
        
        self.btn_save = QPushButton('Save', self)
        self.btn_save.clicked.connect(self.save_qimage_dialog)
        
        self.btn_min = QPushButton('Min', self)
        self.btn_min.clicked.connect(self.static_min)
        
        self.btn_max = QPushButton('Max', self)
        self.btn_max.clicked.connect(self.static_max)
        
        
        self.btn_median = QPushButton('Median', self)
        self.btn_median.clicked.connect(self.static_median)
        
        
        self.static_filter_slider = QSlider(Qt.Horizontal, self)
        self.static_filter_slider.setRange(3,20)
        self.static_filter_slider.setValue(3)
        self.static_filter_slider.setTickInterval(1)
        self.static_filter_slider.valueChanged.connect(self.mask_value_change)
        
        self.contrast_slider = QSlider(Qt.Horizontal, self)
        self.contrast_slider.setRange(1,100)
        self.contrast_slider.setValue(1)
        self.contrast_slider.setTickInterval(1)
        self.contrast_slider.valueChanged.connect(self.contrast_changed)
        
        
        

        # Dodaj przycisk i slider do interfejsu użytkownika
        self.button.move(10, 10)
        self.slider.move(10, 90)
        self.bright_options.move(10, 50)
        self.btn_negatyw.move(10, 130)
        self.options.move(120, 10)
        self.apply_button.move(230, 10)
        self.slider_alpha.move(120, 50)
        self.slider_kierunek.move(120,90)
        self.btn_hist.move(10, 170)
        self.filtr_options.move(10, 210)
        self.btn_pion.move(120, 210)
        self.btn_poz.move(120, 250)
        self.btn_set.move(340, 10)
        self.btn_save.move(450, 10)
        self.btn_min.move(10, 290)
        self.btn_max.move(120, 290)
        self.btn_median.move(230, 290)
        self.static_filter_slider.move(10, 250)
        self.contrast_slider.move(10, 370)
        
        
        
        
        

        # Przechowaj referencję do obrazu
        self.pil_image = None
        
    def mask_value_change(self, value):
        self.mask_size = value
        
    def contrast_changed(self, value):
        if not self.pil_image:
            return
        pil_image = f.adjust_contrast(self.pil_image, value)
        self.SETIMAGE(pil_image)
        
    def SETIMAGE(self, pil_image):
        # Przekonwertuj obraz PIL na format, który może być wyświetlony w etykiecie PySide6
        self.q_image = QPixmap.fromImage(self.convert_pil_to_qimage(pil_image))

        # Wyświetl obraz na etykiecie
        self.image_label.setPixmap(self.q_image)
        
    
        
        
    def USEACTUAL(self):
        if self.pil_image == None:
            return
        self.pil_image = self.convert_qimage_to_pil(self.q_image)
        
        
    def filtr_options_changed(self, value):
        self.filtrtryb = value
        if self.filtrtryb == 3:
            self.btn_pion.setVisible(False)
            self.btn_poz.setText("Do Laprace")
            self.btn_poz.move(120,210)
        else:
            self.btn_pion.setVisible(True)
            self.btn_poz.setText("Poziomy")
            self.btn_poz.move(120,250)
            
            
            
    def static_min(self):
        if not self.pil_image:
            return
        pil_image = s.static_min_filter(self.pil_image, self.mask_size)
        self.SETIMAGE(pil_image)
    
    
    def static_max(self):
        if not self.pil_image:
            return
        pil_image = s.static_max_filter(self.pil_image, self.mask_size)
        self.SETIMAGE(pil_image)
        
    def static_median(self):
        if not self.pil_image:
            return
        pil_image = s.median_filter(self.pil_image, self.mask_size)
        self.SETIMAGE(pil_image)
                
    def btn_pion_clicked(self):
        if not self.pil_image:
            return
        pil_image = f.filtrRPS(self.pil_image, self.filtrtryb)

        self.SETIMAGE(pil_image)
    
    def btn_poz_clicked(self):
        if not self.pil_image:
            return
        pil_image = f.filtrRPS(self.pil_image, self.filtrtryb+3)

        self.SETIMAGE(pil_image)
        
    def set_alpha(self, value):
        self.alpha = value
        if not self.pil_image or not self.second_image:
            return
        pil_image = functions.merge_images_additive(self.pil_image, self.second_image, self.mieszanie, self.alpha/100)

        self.SETIMAGE(pil_image)



    def load_image(self):
        # Wywołaj okno dialogowe, aby użytkownik wybrał plik obrazu
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")

        # Wczytaj plik obrazu za pomocą PIL
        self.pil_image = Image.open(file_path)
        self.button.setText(file_path.split("/")[-1][0:14]+"...")
        

        # Przekonwertuj obraz PIL na format, który może być wyświetlony w etykiecie PySide6
        self.q_image = QPixmap.fromImage(self.convert_pil_to_qimage(self.pil_image))

        # Wyświetl obraz na etykiecie
        self.image_label.setPixmap(self.q_image)



    def convert_pil_to_qimage(self, pil_image):
        image_data = pil_image.convert("RGBA").tobytes("raw", "RGBA")
        q_image = QImage(image_data, pil_image.size[0], pil_image.size[1], QImage.Format_RGBA8888)

        return q_image
    
    def convert_qimage_to_pil(self, qimage):
        image = ImageQt.fromqimage(qimage)
        return image.convert("RGB")
    
    def adjust_brightness(self, value):
        self.brightness = value

    def adjust_brightness_finished(self):
        # Jeśli obraz nie jest wczytany, nie wykonuj operacji
        if self.pil_image is None:
            return

        # Skoryguj jasność obrazu na podstawie wartości slidera
        pil_image = functions.linear_transform(self.pil_image, 1, self.brightness)

        self.SETIMAGE(pil_image)
        
    def new_adjust_brightness(self, value):
        self.brightness = value
        if self.pil_image is None:
            return
        if self.tryb == 0:
            pil_image = functions.better_linear_transform(self.pil_image, float(self.kierunek/10), self.brightness)
        elif self.tryb == 1:
            pil_image = functions.better_power_transform(self.pil_image, float(self.kierunek/10), self.brightness)
        self.SETIMAGE(pil_image)
        
    def set_kierunek(self, value):
        self.kierunek = value
        if self.pil_image is None:
            return
        if self.tryb == 0:
            pil_image = functions.better_linear_transform(self.pil_image, float(self.kierunek/10), self.brightness)
        elif self.tryb == 1:
            pil_image = functions.better_power_transform(self.pil_image, float(self.kierunek/10), self.brightness)
        self.SETIMAGE(pil_image)
        
        
    def btn_negatyw_click(self):
        if self.pil_image is None:
            return

        # Skoryguj jasność obrazu na podstawie wartości slidera
        pil_image = functions.better_negative_image(self.pil_image)

        self.SETIMAGE(pil_image)


    def handle_option_changed(self, value):
        self.mieszanie = value
        self.slider_alpha.setVisible(False)
        if value == 15:
            self.slider_alpha.setVisible(True)
        if not self.second_image:
            return
        pil_image = functions.merge_images_additive(self.pil_image, self.second_image, self.mieszanie, self.alpha/100)

        self.SETIMAGE(pil_image)
        
    def bright_handle_option_changed(self, value):
        self.tryb = value
        if self.tryb == 0:
            self.slider.setRange(-100, 100)
            self.slider.setValue(0)
        elif self.tryb == 1:
            self.slider.setRange(0, 200)
            self.slider.setValue(100)
        if not self.pil_image or not self.second_image:
            return
        if self.tryb == 0:
            pil_image = functions.better_linear_transform(self.pil_image, float(self.kierunek/10), self.brightness)
        elif self.tryb == 1:
            pil_image = functions.better_power_transform(self.pil_image, float(self.kierunek/10), self.brightness)
        
        self.SETIMAGE(pil_image)

    def apply_option(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")
        self.second_image = Image.open(file_path)
        self.apply_button.setText(file_path.split("/")[-1][0:14]+"...")
        if not self.pil_image:
            return
        pil_image = functions.merge_images_additive(self.pil_image, self.second_image, self.mieszanie, self.alpha/100)

        self.SETIMAGE(pil_image)
        
    def btn_hist_click(self):
        if not self.pil_image:
            return
        pil_image = hs.histogram(self.pil_image)

        self.SETIMAGE(pil_image)
        
        
    def create_slider(self):
        # Utwórz slider jasności
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setRange(-100, 100)
        self.slider.setValue(0)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.setTickInterval(10)


        # Stara jasnosc
        # self.slider.sliderReleased.connect(self.adjust_brightness_finished)
        # self.slider.valueChanged.connect(self.adjust_brightness)
        # nowa jasnosc
        self.slider.valueChanged.connect(self.new_adjust_brightness)
    
    
    
    def save_qimage_dialog(self):
        
        if self.pil_image==None:
            return
        
        save_dialog = QFileDialog()
        save_dialog.setWindowTitle("Save Image")
        save_dialog.setAcceptMode(QFileDialog.AcceptSave)
        save_dialog.setNameFilter("Images (*.png *.jpg *.bmp)")

        if save_dialog.exec():
            selected_file = save_dialog.selectedFiles()[0]
            self.q_image.save(selected_file)
        
            
            
        

    
if __name__ == "__main__":
# Utwórz obiekt aplikacji PySide6
    app = QApplication([])
    
    # Utwórz obiekt głównego okna
    window = MainWindow()
    window.setGeometry(100, 100, 800, 600)
    window.show()

    # Uruchom pętlę zdarzeń aplikacji PySide6
    app.exec()


