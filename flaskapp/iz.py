print("Hello world")
from flask import Flask
app = Flask(__name__)
#декоратор для вывода страницы по умолчанию
@app.route("/")
def hello():
 return " <html><head></head> <body> Hello World! </body></html>"

from flask import render_template
#наша новая функция сайта

# модули работы с формами и полями в формах
from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField
# модули валидации полей формы
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
# используем csrf токен, можете генерировать его сами
SECRET_KEY = 'secret'
app.config['SECRET_KEY'] = SECRET_KEY
# используем капчу и полученные секретные ключи с сайта google 
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LeALygbAAAAALLJeEC62I8tjIzP3yvYESstb4lD'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LeALygbAAAAAN3EQJQefVaFcVF9XSBaBU2lKPqq'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}
# обязательно добавить для работы со стандартными шаблонами
from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)
# создаем форму для загрузки файла
class NetForm(FlaskForm):
 # поле для введения строки, валидируется наличием данных
 # валидатор проверяет введение данных после нажатия кнопки submit
 # и указывает пользователю ввести данные если они не введены
 # или неверны
 cho = StringField('Введите значение яркости:', validators = [DataRequired()])
 # поле загрузки файла
 # здесь валидатор укажет ввести правильные файлы
 upload = FileField('Load image', validators=[
 FileRequired(),
 FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
 # поле формы с capture
 recaptcha = RecaptchaField()
 #кнопка submit, для пользователя отображена как send
 submit = SubmitField('send')
# функция обработки запросов на адрес 127.0.0.1:5000/net
# модуль проверки и преобразование имени файла
# для устранения в имени символов типа / и т.д.
from werkzeug.utils import secure_filename
import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns

## функция для оброботки изображения 
def brightness(filename,cho):
 ##открываем изображение 
 print(filename)
 img= Image.open(filename)
 imgstart = img
 cho=int(cho)
 
##делаем график
 fig = plt.figure(figsize=(6, 4))
 ax = fig.add_subplot()
 data = np.random.randint(0, 255, (100, 100))
 ax.imshow(img, cmap='plasma')
 b = ax.pcolormesh(data, edgecolors='black', cmap='plasma')
 fig.colorbar(b, ax=ax)
 gr_path = "./static/newgr.png"
 sns.displot(data)
 #plt.show()
 plt.savefig(gr_path)
 plt.close()

##изменяем яркость

 img = np.int16(img)
 img = img * (10/127+1) + cho
 img = np.clip(img, 0, 255)
 img = np.uint8(img)
 img = Image.fromarray(img, 'RGB')
 output_filename = filename
 img.save(output_filename)
 imgend = img
 
##делаем график 2
 fig1 = plt.figure(figsize=(6, 4))
 ax = fig.add_subplot()
 data1 = np.random.randint(0, 255, (100, 100))
 ax.imshow(img, cmap='plasma')
 b1 = ax.pcolormesh(data1, edgecolors='black', cmap='plasma')
 fig1.colorbar(b1, ax=ax)
 gr_path1 = "./static/newgr1.png"
 sns.displot(data1)
 #plt.show()
 plt.savefig(gr_path1)
 plt.close()
 
##делаем график 3
 r1sum = 0
 r2sum = 0
 g1sum = 0
 g2sum = 0
 b1sum = 0
 b2sum = 0
 px = imgstart.load()
 px1 = imgend.load()
 for i in range(img.size[0]): # for every pixel:
  for j in range(img.size[1]):
   pixel = px[x, y]
   r, g, b = pixel[0], pixel[1], pixel[2]
   r1sum = r1sum + r
   g1sum = g1sum + g
   b1sum = b1sum + b
   pixel1 = px1[x, y]
   r, g, b = pixel1[0], pixel1[1], pixel1[2]
   r2sum = r2sum + r
   g2sum = g2sum + g
   b2sum = b2sum + b
 r1mean = r1sum / (img.size[0] * img.size[1])
 r2mean = r2sum / (img.size[0] * img.size[1])
 g1mean = g1sum / (img.size[0] * img.size[1])
 g2mean = g2sum / (img.size[0] * img.size[1])
 b1mean = b1sum / (img.size[0] * img.size[1])
 b2mean = b2sum / (img.size[0] * img.size[1])

 r2sum = r2mean - r1mean
 g2sum = g2mean - g1mean
 b2sum = b2mean - b1mean
 diff = np.array([r2sum, g2sum, b2sum])
 
 rgb = np.arange(1, 4)
 fig2, axes = plt.subplots(1, 1)
 axes.bar(rgb, diff)
 #axes[0].set_color('r')
 #axes[1].set_color('g')
 #axes[2].set_color('b')
 fig2.set_facecolor('floralwhite')
 fig2.set_figwidth(12)    #  ширина Figure
 fig2.set_figheight(6)    #  высота Figure

 gr_path2 = "./static/newgr2.png"
 plt.savefig(gr_path2)
 plt.close()
   
 return output_filename,gr_path,gr_path1,gr_path2



# метод обработки запроса GET и POST от клиента
@app.route("/net",methods=['GET', 'POST'])
def net():
 # создаем объект формы
 form = NetForm()
 # обнуляем переменные передаваемые в форму
 filename=None
 newfilename=None
 grname=None
 grname1=None
 grname2=None
 # проверяем нажатие сабмит и валидацию введенных данных
 if form.validate_on_submit():
  # файлы с изображениями читаются из каталога static
  filename = os.path.join('./static', secure_filename(form.upload.data.filename))
  ch=form.cho.data
 
  form.upload.data.save(filename)
  newfilename,grname,grname1,grname2 = brightness(filename,ch)
 # передаем форму в шаблон, так же передаем имя файла и результат работы нейронной
 # сети если был нажат сабмит, либо передадим falsy значения
 
 return render_template('net.html',form=form,image_name=newfilename,gr_name=grname,gr_name1=grname1,gr_name2=grname2)


if __name__ == "__main__":
 app.run(host='127.0.0.1',port=5000)
