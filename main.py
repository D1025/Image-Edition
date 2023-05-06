from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QSlider, QFileDialog, QComboBox, QProgressBar
from PySide6.QtGui import QPixmap, QImage
from PIL import Image
from PySide6.QtCore import Qt
import functions
import histogram as hs
import filtr as f

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

        # Przechowaj referencję do obrazu
        self.pil_image = None
        
        
    def SETIMAGE(self, pil_image):
        # Przekonwertuj obraz PIL na format, który może być wyświetlony w etykiecie PySide6
        self.q_image = QPixmap.fromImage(self.convert_pil_to_qimage(pil_image))

        # Wyświetl obraz na etykiecie
        self.image_label.setPixmap(self.q_image)
        
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
        # Konwertuj obraz PIL na format QImage
        image_data = pil_image.convert("RGBA").tobytes("raw", "RGBA")
        q_image = QImage(image_data, pil_image.size[0], pil_image.size[1], QImage.Format_RGBA8888)

        return q_image
    
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
        
            
            
        

    
if __name__ == "__main__":
# Utwórz obiekt aplikacji PySide6
    app = QApplication([])
    
    # Utwórz obiekt głównego okna
    window = MainWindow()
    window.setGeometry(100, 100, 800, 600)
    window.show()

    # Uruchom pętlę zdarzeń aplikacji PySide6
    app.exec()


