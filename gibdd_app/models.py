from dateutil.relativedelta import relativedelta
from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from dateutil.relativedelta import *
import datetime
from django.urls import reverse


# Create your models here.

# Водитель
class Driver(models.Model):
    passport_number = models.CharField(max_length=11, verbose_name="Номер паспорта")
    driver_surname = models.CharField(max_length=50, verbose_name="Фамилия водителя", blank=True, null=True)
    driver_name = models.CharField(max_length=50, verbose_name="Имя водителя")
    driver_patronymic = models.CharField(max_length=50, verbose_name="Отчество водителя")
    driver_birth = models.DateTimeField(verbose_name="Дата рождения водителя")
    driver_town = models.CharField(max_length=50, verbose_name="Город проживания водителя")

    def __str__(self):
        return "%s %s %s, %s, паспорт: %s" % (
            self.driver_surname, self.driver_name, self.driver_patronymic, self.driver_birth, self.passport_number)

    def get_absolute_url(self):
        return reverse('license_create')


CATEGORY_CHOICES = (
    ('A', 'A'),
    ('A1', 'A1'),
    ('B', 'B'),
    ('B1', 'B1'),
    ('C', 'C'),
    ('C1', 'C1'),
    ('D', 'D'),
    ('D1', 'D1'),
    ('BE', 'BE'),
    ('CE', 'CE'),
    ('C1E', 'C1E'),
    ('DE', 'DE'),
    ('D1E', 'D1E'),
    ('M', 'M'),
    ('Tm', 'Tm'),
    ('Tb', 'Tb'),

)


# Категория прав
class Category(models.Model):
    category_name = models.CharField(max_length=5, verbose_name="Название категории", choices=CATEGORY_CHOICES)
    date_open_category = models.DateField(verbose_name="Дата открытия категории")

    def __str__(self):
        return "%s от %s" % (self.category_name, self.date_open_category)

    def get_absolute_url(self):
        return reverse('lic_cat_create')


MEDICAL_CHOICES = (
    ('6 месяцев', '6 месяцев'),
    ('1 год', '1 год'),
    ('2 года', '2 года'),
    ('другое', 'другое'),
)


# Медицинская справка
class MedicalCertificate(models.Model):
    medical_number = models.CharField(max_length=15, verbose_name="Номер справки")
    medical_date = models.DateField(verbose_name="Дата выдачи")
    diagnosis = models.CharField(max_length=200, verbose_name="Диагноз")
    organization_give = models.CharField(max_length=300, verbose_name="Выдавшая организация")
    validity = models.CharField(max_length=11, verbose_name="Срок действия справки", choices=MEDICAL_CHOICES,
                                blank=True, null=True, default='1 год')
    med_photo_1 = models.ImageField(upload_to='med_photo/',
                                    verbose_name="Скан медицинской справки, лицевая сторона", blank=True, null=True)
    med_photo_2 = models.ImageField(upload_to='med_photo/',
                                    verbose_name="Скан медицинской справки, обратная сторона", blank=True, null=True)

    def __str__(self):
        return self.medical_number

    def get_absolute_url(self):
        return reverse('license_create')

    @property
    def image_url_1(self):
        if self.med_photo_1 and hasattr(self.med_photo_1, 'url'):
            return self.med_photo_1.url

    @property
    def image_url_2(self):
        if self.med_photo_2 and hasattr(self.med_photo_2, 'url'):
            return self.med_photo_2.url


DISQAULIF_CHOICES = (
    ('Действующие', 'Действующие'),
    ('Лишение', 'Лишение'),
    ('Просрочены', 'Просрочены'),
)


class LicenseDisqualification(models.Model):
    # заменить статус на номер
    disqualif_status = models.CharField(verbose_name="Статус прав", max_length=20, choices=DISQAULIF_CHOICES)
    disqualif_time = models.CharField(verbose_name="Срок лишения прав", max_length=10, help_text="18 месяцев",
                                      blank=True, null=True)
    disqualif_date_from = models.DateField(verbose_name="Дата лишения прав", blank=True, null=True)
    disqualif_date_end = models.DateField(verbose_name="Дата окончания лишение прав", blank=True, null=True)
    disqualif_cause = models.CharField(max_length=200, verbose_name="Причина лишения",
                                       default="Вождение автомобиля под воздействием алкоголя", blank=True, null=True)
    disqualif_alcohol_amount = models.FloatField(verbose_name="Промилле алкоголя в крови", blank=True, null=True)
    disqualif_comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)

    def __str__(self):
        return self.disqualif_status

    def get_absolute_url(self):
        return reverse('license_create')


DR_STATUS_CHOICES = (
    ('Действующие', 'Действующие'),
    ('Лишение', 'Лишение'),
    ('Просрочены', 'Просрочены'),
)


def get_deadline():
    return datetime.datetime.today() + timedelta(days=8 * 365) + timedelta(days=2 * 366) + timedelta(days=1)


# Водительское удостоверение(ВУ)
class License(models.Model):
    short_status_license = models.CharField(max_length=50, verbose_name="Статус прав", choices=DR_STATUS_CHOICES,
                                            default='Действующие')
    driver_data = models.OneToOneField(Driver, on_delete=models.CASCADE, verbose_name="Данные о водителе")
    # category_dr_license_data = models.ManyToManyField(Category, verbose_name="Данные о доступных категорях")
    medical_certificate_data = models.OneToOneField(MedicalCertificate, on_delete=models.CASCADE,
                                                    verbose_name="Данные о мед.справках")
    photo_dr_license = models.ImageField(upload_to='driving_license_photo/',
                                         default='driving_license_photo/default_photo_dr_license.jpg',
                                         verbose_name="Фото ВУ")
    series_dr_license = models.CharField(max_length=4, verbose_name="Серия ВУ")
    number_dr_license = models.CharField(max_length=6, verbose_name="Номер ВУ")
    status_dr_license = models.OneToOneField(LicenseDisqualification, on_delete=models.CASCADE,
                                             verbose_name="Подробности лишения прав", blank=True, null=True)
    date_issue_dr_license = models.DateField(verbose_name="Дата выдачи ВУ", default=datetime.datetime.now,
                                             editable=False)
    date_end_dr_license = models.DateField(verbose_name="Дата окончания действия ВУ", blank=True, null=True,
                                           default=get_deadline, editable=False)
    division_give_dr_license = models.CharField(max_length=100, verbose_name="Подразделение ГИБДД, выдавшее ВУ")
    town_dr_license = models.CharField(max_length=100, verbose_name="Город выдачи ВУ")

    # def save(self):
    #     from datetime import datetime, timedelta
    #     d = timedelta(days=8 * 365) + timedelta(days=2 * 366)
    #     if not self.id:
    #         self.datetime = self.date_issue_dr_license + d
    #         super(License,self.save())



    def __str__(self):
        return "%s № %s от %s" % (self.series_dr_license, self.number_dr_license, self.date_issue_dr_license)

    def get_absolute_url(self):
        return reverse('lic_cat_create')

    # фото водителя
    @property
    def image_url(self):
        if self.photo_dr_license and hasattr(self.photo_dr_license, 'url'):
            return self.photo_dr_license.url

            # @property
            # def date_end_license(self):
            #     if self.date_end_dr_license:
            #         # return self.date_issue_dr_license + datetime.timedelta(days=8 * 365) + datetime.timedelta(days=2 * 364)
            #         # return self.date_issue_dr_license+relativedelta(years=10)


# дополнительная таблица для категории и ВУ (разбила связь М:М)
class Lisense_Category(models.Model):
    licen = models.ForeignKey(License, on_delete=models.CASCADE, verbose_name="Все ВУ")
    categ = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Все категории")

    def get_absolute_url(self):
        return reverse('workers')

    class Meta:
        unique_together = ("licen", "categ")

    def __str__(self):
        return "%s, категория - %s " % (self.licen, self.categ)


# Инспектор
class Inspector(models.Model):
    inspector_number_token = models.CharField(max_length=30, verbose_name="Номер жетона")
    photo_inspector = models.ImageField(upload_to='inspector_photo/',
                                        default='inspector_photo/default_photo_inspector.jpg',
                                        verbose_name="Фото инспектора")
    inspector_surname = models.CharField(max_length=50, verbose_name="Фамилия инспектора")
    inspector_name = models.CharField(max_length=50, verbose_name="Имя инспектора")
    inspector_patronymic = models.CharField(max_length=50, verbose_name="Отчество инспектора")
    inspector_status = models.CharField(max_length=50, verbose_name="Звание инспектора")
    inspector_division = models.CharField(max_length=40, verbose_name="Номер отделения")

    def __str__(self):
        return "%s %s %s" % (self.inspector_number_token, self.inspector_surname, self.inspector_name)

    # фото
    @property
    def image_url(self):
        if self.photo_inspector and hasattr(self.photo_inspector, 'url'):
            return self.photo_inspector.url


DECREE_CHOICES = (
    ('Превышение скорости', 'Превышение скорости'),
    ('Проезд на запрещающий сигнал светофора или жест регулировщика',
     'Проезд на запрещающий сигнал светофора или жест регулировщика'),
    ('Выезд на встречную полосу', 'Выезд на встречную полосу'),
    ('Несоблюдение правил остановки, стоянки, парковки', 'Несоблюдение правил остановки, стоянки, парковки'),
    ('Непредоставление преимущества в движении пешеходам', 'Непредоставление преимущества в движении пешеходам '),
    ('Езда в состоянии алкогольного или наркотического опьянения',
     'Езда в состоянии алкогольного или наркотического опьянения'),
    ('Управление незарегистрированным автомобилем', 'Управление незарегистрированным автомобилем'),
    ('Управление ТС с нарушением правил установки на нем государственных регистрационных знаков',
     'Управление ТС с нарушением правил установки на нем государственных регистрационных знаков '),
    ('Управление ТС без документов', 'Управление ТС без документов'),
    ('Управление ТС без прав', 'Управление ТС без прав'),
    ('Несоблюдение правил об обязательном страховании гражданской ответственности владельцев ТС',
     'Несоблюдение правил об обязательном страховании гражданской ответственности владельцев ТС'),
    (
        'Нарушение требований в области технического осмотра ТС',
        'Нарушение требований в области технического осмотра ТС'),
    ('Нарушение правил регистрации', 'Нарушение правил регистрации'),
    ('Превышение уровня шума или токсичности ТС', 'Превышение уровня шума или токсичности ТС'),
    ('Нарушение правил пользования фарами,поворотниками и гудком',
     'Нарушение правил пользования фарами,поворотниками и гудком'),
    ('Выпуск на линию ТС с неисправностями, со спесигналами или спецраскраской без соответствующего на то разрешения',
     'Выпуск на линию ТС с неисправностями, со спесигналами или спецраскраской без соответствующего на то разрешения'),
    ('Нарушение правил применения ремней безопасности или мотошлемов',
     'Нарушение правил применения ремней безопасности или мотошлемов'),
    ('Перевозка грузов и буксировка', 'Перевозка грузов и буксировка'),
    ('Учебная езда', 'Учебная езда'),
    ('Причинение вреда здоровью', 'Причинение вреда здоровью'),
    ('Невыполнение обязанностей в связи с ДТП', 'Невыполнение обязанностей в связи с ДТП'),
    ('Несоблюдение обеспечения безопасности при ремонте, реконструкции, содержании дорог и ж/д переездов',
     'Несоблюдение обеспечения безопасности при ремонте, реконструкции, содержании дорог и ж/д переездов'),
    ('Пользование телефоном за рулём', 'Пользование телефоном за рулём'),
    ('Нарушение правил движения по автомагистрали', 'Нарушение правил движения по автомагистрали'),
    ('Нарушение правил проезда перекрестков', 'Нарушение правил проезда перекрестков'),
    ('Нарушение правил маневрирования', 'Нарушение правил маневрирования'),
    ('Нарушение правил расположения ТС на проезжей части, встречного разъезда или обгона',
     'Нарушение правил расположения ТС на проезжей части, встречного разъезда или обгона'),
    (
        'Непредоставление преимущества в движении маршрутному ТС, ТС с включенными специальным световыми и звуковыми сигналами',
        'Непредоставление преимущества в движении маршрутному ТС, ТС с включенными специальным световыми и звуковыми сигналами'),
    ('Нарушение правил движения в жилых зонах', 'Нарушение правил движения в жилых зонах'),
)

CAMERA_CHOICES = (
    ('Превышение скорости', 'Превышение скорости'),
    ('Проезд на запрещающий сигнал светофора', 'Проезд на запрещающий сигнал светофора'),
    ('Выезд за стоп-линию', 'Выезд за стоп-линию'),
    ('Выезд на перекресток при заторе', 'Выезд на перекресток при заторе'),
    ('Выезд на встречную полосу движения', 'Выезд на встречную полосу движения'),
    ('Проезд под знак "Въезд запрещён', 'Проезд под знак "Въезд запрещён'),
    ('Проезд под знак "Движение грузовых автомобилей запрещено',
     'Проезд под знак "Движение грузовых автомобилей запрещено'),
    ('Выезд на полосу для маршрутных транспортных средств', 'Выезд на полосу для маршрутных транспортных средств'),
    ('Выезд на тротуар', 'Выезд на тротуар'),
    ('Движение грузовиков далее второй полосы на автомагистралях и дорогах для автомобилей(МКАД)',
     'Движение грузовиков далее второй полосы на автомагистралях и дорогах для автомобилей(МКАД)'),
    ('Нарушение требований дорожной разметки', 'Нарушение требований дорожной разметки'),
    ('Выполнение поворота из второго ряда', 'Выполнение поворота из второго ряда'),
    ('Не включенный ближний свет фар или дневные ходовые огни',
     'Не включенный ближний свет фар или дневные ходовые огни'),
    (
        'Нарушение правил оплаты проезда для тяжелых грузовиков',
        'Нарушение правил оплаты проезда для тяжелых грузовиков'),
    ('Непредоставление преимущества пешеходам на пешеходных переходах',
     'Непредоставление преимущества пешеходам на пешеходных переходах'),
    ('Нарушение правил парковки', 'Нарушение правил парковки'),
)

CAMERA_CHOICES1 = (
    ('Радар Стрелка СТ/М', 'Радар Стрелка СТ/М'),
    ('Система Автодория', 'Система Автодория'),
    ('Фоторадарные комплексы КРИС С', 'Фоторадарные комплексы КРИС С'),
    ('Фоторадарные комплексы КРИС П', 'Фоторадарные комплексы КРИС П'),
    ('Радар Кречет-С', 'Радар Кречет-С'),
    ('Радар Перекресток', 'Радар Перекресток'),
    ('Комплекс фотовидеофиксации "Сова"', 'Комплекс фотовидеофиксации "Сова"'),
    ('Комплекс фотовидеофиксации "Одиссей"', 'Комплекс фотовидеофиксации "Одиссей"'),
    ('Паркон', 'Паркон'),
)


class Camera(models.Model):
    camera_number = models.CharField(max_length=30, verbose_name="Номер камеры")
    camera_name = models.CharField(verbose_name="Название камеры", max_length=100, choices=CAMERA_CHOICES1)
    camera_vertification_from = models.DateField(verbose_name="Дата поверки камеры", blank=True, null=True)
    camera_vertification_to = models.DateField(verbose_name="Дата действия поверки камеры до")
    camera_functions = models.CharField(max_length=100, verbose_name="Функции камеры", choices=CAMERA_CHOICES)
    camera_address = models.CharField(max_length=200, verbose_name="Расположение камеры(адрес)")

    def __str__(self):
        return "%s" % (self.camera_number)


# class PDD(models.Model):
#     PDD_paragraph = models.CharField(max_length=8, verbose_name="Пункт ПДД")
#     PDD_paragraph_contents = models.CharField(max_length=300, verbose_name="Содержание пункта ПДД")


# class KOAP(models.Model):
#     KOAP_paragraph = models.CharField(max_length=8, verbose_name="Пункт КОАП")
#     KOAP_paragraph_contents = models.CharField(max_length=300, verbose_name="Содержание пункта КОАП")
#     KOAP_type_of_violation = models.CharField(max_length=50, verbose_name="Вид нарушения", choices=KOAP_CHOICES,
#                                               default='k2')


REGISTRATION_CHOICES = (
    ('легковой', 'легковой'),
    ('грузовой', 'грузовой'),
    ('автобус', 'автобус'),
    ('мотоцикл', 'мотоцикл'),
    ('мопед', 'мопед'),
    ('прицеп', 'прицеп'),
    ('полуприцеп', 'полуприцеп'),
    ('универсал легковой', 'универсал легковой'),
    ('хэтчбек(комби) легковой', 'хэтчбек(комби) легковой'),
    ('легковой прочие', 'легковой прочие'),
    ('бортовой с тентом грузовой', 'бортовой с тентом грузовой'),
    ('грузовой фургон', 'грузовой фургон'),
    ('легковой минивэн', 'легковой минивэн'),
    ('грузовой бортовой', 'грузовой бортовой'),
    ('легковой седан', 'легковой седан'),
    ('легковой купе', 'легковой купе'),
)

REGISTRATION_CHOICES2 = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ('прицеп', 'прицеп'),
)

REGISTRATION_CHOICES3 = (
    ('первый', 'первый'),
    ('второй', 'второй'),
    ('третий', 'третий'),
    ('четвертый', 'четвертый'),
    ('пятый', 'пятый'),
    ('шестой', 'шестой'),
    ('седьмой', 'седьмой')
)


# СТС: Свидетельство о регистрации
class RegistrationCertificate(models.Model):
    registr_certificate_number = models.CharField(max_length=11, verbose_name="Номер СТС", unique=True,
                                                  help_text="Например, 1234№123456")
    registr_certificate_registr_sign = models.CharField(max_length=9, help_text="А111АА777",
                                                        verbose_name="Регистрационный знак")
    registr_certificate_VIN = models.CharField(max_length=17, verbose_name="VIN",
                                               help_text="Например,SAFDYUH12R1234567", unique=True)
    registr_certificate_car_model = models.CharField(max_length=50, verbose_name="Марка, модель")
    registr_certificate_type_car = models.CharField(max_length=60, verbose_name="Тип ТС", choices=REGISTRATION_CHOICES,
                                                    default='легковой')
    registr_certificate_category = models.CharField(max_length=5, verbose_name="Категория ТС",
                                                    choices=REGISTRATION_CHOICES2, default='B')
    registr_certificate_year = models.IntegerField(verbose_name="Год выпуска ТС",
                                                   help_text="Например,2018")
    registr_certificate_chassis = models.CharField(verbose_name="Шасси №", max_length=30)
    registr_certificate_body = models.CharField(max_length=17, verbose_name="Кузов №",
                                                help_text="Например,SAFDYUH12R1234567")
    registr_certificate_colour = models.CharField(max_length=50, verbose_name="Цвет")
    registr_certificate_power = models.CharField(max_length=12, verbose_name="Мощность двигателя,кВт/л.с",
                                                 help_text="Например,86(117)")
    registr_certificate_ecology_class = models.CharField(max_length=20, verbose_name="Экологический класс",
                                                         choices=REGISTRATION_CHOICES3, default='четвертый')
    registr_certificate_passport = models.CharField(max_length=11, verbose_name="Паспорт ТС серия",
                                                    help_text="Например, 12УУ№123456")
    registr_certificate_max_weight = models.IntegerField(verbose_name="Разрешенная max масса,kg")
    registr_certificate_without_load = models.IntegerField(verbose_name="Масса без нагрузки,kg")

    def __str__(self):
        return "№ %s для %s, %s" % (
            self.registr_certificate_number, self.registr_certificate_registr_sign, self.registr_certificate_car_model)

        # def concatenat(self, arg1, arg2):
        #     arg1 = self.registr_certificate_number
        #     arg2 = self.registr_certificate_registr_sign
        #     return arg1 + " " + arg2


# Собственник
class Owner(models.Model):
    owner_number = models.CharField(max_length=10, verbose_name="Номер свидетельства собственника", unique=True)
    owner_surname = models.CharField(max_length=50, verbose_name="Фамилия собственника")
    owner_name = models.CharField(max_length=50, verbose_name="Имя собственника")
    owner_patronymic = models.CharField(max_length=50, verbose_name="Отчество собственника")
    owner_town = models.CharField(max_length=50, verbose_name="Республика,край,область")
    owner_district = models.CharField(max_length=50, verbose_name="Район", blank=True, null=True)
    owner_address = models.CharField(max_length=100, verbose_name="Адрес собственника")
    owner_comment = models.CharField(max_length=400, verbose_name="Особые отметки", blank=True, null=True)
    owner_who_give = models.CharField(max_length=200, verbose_name="Выдано ГИБДД")
    owner_date_give = models.DateField(verbose_name="Дата выдачи свидетельства собственника")

    def __str__(self):
        return "№ %s, собственник: %s, %s" % (
            self.owner_number, self.owner_surname, self.owner_name)


STEALING_CHOICES = (
    ('Не числится в угоне', 'Не числится в угоне'),
    ('Числится в угоне', 'Числится в угоне'),
)


# Угон
class Stealing(models.Model):
    stealing_status = models.CharField(max_length=25, verbose_name="Статус", choices=STEALING_CHOICES, blank=True,
                                       null=True, unique=False)
    stealing_unique_number = models.CharField(max_length=7, verbose_name="Номер угона", unique_for_date=True,
                                              blank=True, null=True)
    stealing_date = models.DateField(verbose_name="Дата угона", blank=True, null=True)
    stealing_town = models.CharField(max_length=50, verbose_name="Город угона", blank=True, null=True)
    stealing_comment = models.TextField(verbose_name="Комментарий об угоне", blank=True, null=True)

    def __str__(self):
        return "%s, %s, %s" % (
            self.stealing_status, self.stealing_date, self.stealing_unique_number)


# Автошкола
class AutoSchool(models.Model):
    student = models.ForeignKey(Driver, verbose_name="Ученик автошколы", on_delete=models.CASCADE)
    school_name = models.CharField(max_length=100, verbose_name="Название автошколы")
    school_photo = models.ImageField(upload_to='autoschool_photo/',
                                     default='autoschool_photo/default.jpg',
                                     verbose_name="Фото автошколы", blank=True, null=True)
    school_address = models.CharField(max_length=100, verbose_name="Адрес автошколы")
    school_phone = models.CharField(max_length=100, verbose_name="Телефон автошколы")
    school_category_dr_license = models.CharField(max_length=10,
                                                  verbose_name="Обучение на категорию")

    def __str__(self):
        return "%s, %s" % (
            self.school_name, self.school_address)

    # фото
    @property
    def image_url(self):
        if self.school_photo and hasattr(self.school_photo, 'url'):
            return self.school_photo.url


CAR_CHOICES = (
    ('Стоит на учете', 'Стоит на учете'),
    ('Снят на учете', 'Снят на учете'),
    ('Числится в угоне', 'Числится в угоне'),

)


# Автомобиль
class Car(models.Model):
    car_status = models.CharField(max_length=20, verbose_name="Статус автомобиля", choices=CAR_CHOICES,
                                  default="Стоит на учете")
    car_photo = models.ImageField(upload_to='car_photo/',
                                  default='car_photo/default_car.jpg',
                                  verbose_name="Фото автомобиля")
    car_model = models.CharField(max_length=100, verbose_name="Модель автомобиля")
    car_colour = models.CharField(max_length=50, verbose_name="Цвет автомобиля")
    car_number = models.CharField(max_length=9, verbose_name="Номер автомобиля")
    car_registr_certificate = models.OneToOneField(RegistrationCertificate, verbose_name="Свидетельство о регистрации",
                                                   on_delete=models.CASCADE, unique=True)
    car_owner = models.OneToOneField(Owner, on_delete=models.CASCADE, verbose_name="Собственник автомобиля",
                                     unique=True)
    car_stealing = models.OneToOneField(Stealing, on_delete=models.CASCADE, verbose_name="Детали угона", unique=True,
                                        blank=True, null=True)

    def __str__(self):
        return "%s" % (self.car_number)

    @property
    def image_url_car(self):
        if self.car_photo and hasattr(self.car_photo, 'url'):
            return self.car_photo.url


KOAP_CHOICES = (
    ('Предупреждение', 'Предупреждение'),
    ('Административный штраф', 'Административный штраф'),
    ('Конфискация орудия совершения или предмета административного нарушения',
     'Конфискация орудия совершения или предмета административного нарушения'),
    ('Лишение специального права, предоставленного лицу', 'Лишение специального права, предоставленного лицу'),
    ('Административный арест', 'Административный арест'),
    ('Дисквалификация', 'Дисквалификация'),
    ('Административное приостановление деятельности', 'Административное приостановление деятельности'),
    ('Обязательные работы', 'Обязательные работы'),
    ('Административный запрет на посещение мест проведения официальных спортивных соревнований в дни их проведения',
     'Административный запрет на посещение мест проведения официальных спортивных соревнований в дни их проведения'),
)


# Постановление
class Decree(models.Model):
    decree_number = models.CharField(max_length=25, verbose_name="Номер постановления")
    decree_date = models.DateField(verbose_name="Дата постановления")
    decree_inspector = models.ForeignKey(Inspector, verbose_name="Инспектор, выписавший постановление", null=True,
                                         blank=True, on_delete=models.CASCADE, unique=False)
    decree_camera = models.ForeignKey(Camera, verbose_name="Средство фиксации нарушения", on_delete=models.CASCADE,
                                      null=True, blank=True, unique=False)
    decree_license_data = models.ForeignKey(License, verbose_name="Данные ВУ для вынесения постановления",
                                            on_delete=models.CASCADE, unique=False)
    decree_car = models.ForeignKey(Car, verbose_name="Данные о нарушевшем автомобиле", on_delete=models.CASCADE,
                                   unique=False)
    decree_violation = models.CharField(max_length=200, verbose_name="Нарушение(смысл)", choices=DECREE_CHOICES,
                                        null=True)
    decree_violation_text = models.TextField(verbose_name="Полное описание нарушения", blank=True, null=True)
    decree_total_speed = models.IntegerField(verbose_name="Скорость движения в момент нарушения", blank=True, null=True)
    decree_photo = models.ImageField(upload_to='decree_photo/',
                                     default='decree_photo/default.jpg',
                                     verbose_name="Фото нарушения")
    decree_KOAP = models.CharField(max_length=110, choices=KOAP_CHOICES,
                                   default='Административный штраф', verbose_name="Нарушенные пункты КОАП")
    decree_PDD = models.CharField(max_length=50, verbose_name="Нарушенные пункты ПДД")

    def __str__(self):
        return "%s" % (self.decree_number)

    @property
    def image_url_decree(self):
        if self.decree_photo and hasattr(self.decree_photo, 'url'):
            return self.decree_photo.url


FINE_STATUS_CHOICES = (
    ('Оплачен', 'Оплачен'),
    ('Не оплачен', 'Не оплачен'),
    ('Просрочен', 'Просрочен')
)


# штраф
class Fine(models.Model):
    fine_amount = models.IntegerField(verbose_name="Первоначальная сумма штрафа")
    fine_discount = models.FloatField(verbose_name="Скидка")
    date_of_payment_fine = models.DateTimeField(verbose_name="Дата оплаты штрафа", blank=True, null=True)
    fine_status = models.CharField(max_length=50, verbose_name="Статус штрафа", choices=FINE_STATUS_CHOICES)
    fine_license_data = models.ForeignKey(License, on_delete=models.CASCADE, verbose_name="Данные о ВУ", unique=False)
    fine_decree_data = models.OneToOneField(Decree, verbose_name="Данные о постановлении", on_delete=models.CASCADE)
    fine_car_data = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name="Штраф для автомобиля", unique=False)

    class Meta:
        unique_together = ("fine_license_data", "fine_decree_data")

    def __str__(self):
        return "Штраф на основании постановления № %s" % (self.fine_decree_data.decree_number)


# Диагностическая карта
class DiagnosticCard(models.Model):
    diagnostic_number = models.CharField(max_length=15, verbose_name="Регистрационный номер", unique=True)
    diagnostic_car = models.OneToOneField(Car, verbose_name="Автомобиль для диагностики", on_delete=models.CASCADE,
                                          unique=True)
    diagnostic_date_from = models.DateField(verbose_name="Дата выдачи")
    diagnostic_date_to = models.DateField(verbose_name="Срок действия до")
    diagnostic_company = models.CharField(max_length=200, verbose_name="Пункт технического осмотра")
    diagnostic_results = models.TextField(verbose_name="Результаты диагностирования")

    def __str__(self):
        return "%s, %s" % (self.diagnostic_number, self.diagnostic_date_from)


INSURANCE_CHOICES = (
    ('ОСАГО', 'ОСАГО'),
    ('КАСКО', 'КАСКО'),
)

INSURANCE_CHOICES2 = (
    ('ОСАГО', 'ОСАГО'),
    ('ОСАГО без ограничений', 'ОСАГО без ограничений'),
    ('открытая страховка ОСАГО', 'открытая страховка ОСАГО'),

)


# Страхововй полис
class Insurance(models.Model):
    insurance_number = models.CharField(max_length=15, verbose_name="Номер полиса", help_text="ЕЕЕ№1234567890")
    insurance_company = models.CharField(max_length=100, verbose_name="Страховая компания")
    insurance_type = models.CharField(max_length=10, verbose_name="Тип полиса", choices=INSURANCE_CHOICES,
                                      default='ОСАГО')
    insurance_date_from = models.DateField(verbose_name="Дата начала действия")
    insurance_date_to = models.DateField(verbose_name="Дата окончания действия")
    insurance_confines = models.CharField(max_length=50, verbose_name="Ограничения", choices=INSURANCE_CHOICES2,
                                          default='ОСАГО')
    insurance_diagnostic_card = models.OneToOneField(DiagnosticCard,
                                                     verbose_name="Диагностическая карта (ТО) о состоянии автомобиля",
                                                     on_delete=models.CASCADE, unique=True)
    # insurance_driving_license = models.ManyToManyField(License,
    #                                                    verbose_name="Допущенные к управления автомобилем по полису")
    insurance_car = models.ForeignKey(Car, verbose_name="Полис на автомобиль", on_delete=models.CASCADE)
    insurance_comments = models.TextField(verbose_name="Комментарий к полису")

    def __str__(self):
        return "%s, %s, %s" % (self.insurance_number, self.insurance_company, self.insurance_type)


class InsuranceLicense(models.Model):
    insur = models.ForeignKey(Insurance, on_delete=models.CASCADE,
                              verbose_name="Все страховки для данного автомобиля (ОСАГО, КАСКО)")
    licen = models.ForeignKey(License, on_delete=models.CASCADE,
                              verbose_name="ВУ, допущенные к управлению автомобилем по полису")

    def get_absolute_url(self):
        return reverse('workers')

    class Meta:
        unique_together = ("insur", "licen")

    def __str__(self):
        return "%s, %s" % (self.insur, self.licen)


# европротокол
class Europrotocol(models.Model):
    europrotocol_date = models.DateField(verbose_name="День составления протокола")
    europrotocol_driver_1 = models.OneToOneField(Driver, related_name='europrotocol_driver_1',
                                                 on_delete=models.CASCADE)
    europrotocol_driver_2 = models.OneToOneField(Driver, related_name='europrotocol_driver_2', on_delete=models.CASCADE)
    europrotocol_license_1 = models.OneToOneField(License, related_name='europrotocol_license_1',
                                                  on_delete=models.CASCADE, )
    europrotocol_license_2 = models.OneToOneField(License, related_name='europrotocol_license_2',
                                                  on_delete=models.CASCADE, )
    europrotocol_car_1 = models.OneToOneField(Car, related_name='europrotocol_car_1', on_delete=models.CASCADE, )
    europrotocol_car_2 = models.OneToOneField(Car, related_name='europrotocol_car_2', on_delete=models.CASCADE, )
    europrotocol_insurance_1 = models.OneToOneField(Insurance, related_name='europrotocol_insurance_1',
                                                    on_delete=models.CASCADE)
    europrotocol_insurance_2 = models.OneToOneField(Insurance, related_name='europrotocol_insurance_2s',
                                                    on_delete=models.CASCADE)
    europrotocol_scan_1 = models.ImageField(verbose_name="Скан лицевой стороны европротокола", blank=True, null=True)
    europrotocol_scan_2 = models.ImageField(verbose_name=" Скан оборотной стороны европротокола", blank=True, null=True)


def __str__(self):
    return "%s, %s до %s" % (self.europrotocol_date, self.europrotocol_car_1, self.europrotocol_car_2)


ACCIDENT_CHOICES = (
    ('легкая', 'легкая'),
    ('средней тяжести', 'средней тяжести'),
    ('тяжкий вред', 'тяжкий вред'),
    ('без вреда здоровью', 'без вреда здоровью'),
    ('не указано', 'не указано'),
)


# авария
class AccidentReport(models.Model):
    accident_date = models.DateField(verbose_name="Дата аварии")
    accident_time = models.TimeField(verbose_name="Время аварии")
    number_accident = models.CharField(max_length=40, verbose_name="Номер протокола аварии")
    accident_paper_date = models.DateField(verbose_name="Дата составления протокола")
    accident_paper_time = models.TimeField(verbose_name="Время составления протокола")
    accident_address = models.CharField(max_length=200, verbose_name="Адрес аварии")
    accident_severity = models.CharField(max_length=50, verbose_name="Тяжесть аварии", choices=ACCIDENT_CHOICES,
                                         blank=True, null=True, default='не указано')
    accident_number_of_people = models.IntegerField(verbose_name="Количество людей в аварии")
    accident_death = models.IntegerField(verbose_name="Смертельный исход, взрослые (количество)", default=0)
    accident_children = models.IntegerField(verbose_name="Из участвовавших в аварии-дети", default=0)
    accident_children_death = models.IntegerField(verbose_name="Смертельный исход, дети(количество)", default=0)
    accident_causer_person = models.OneToOneField(Driver, verbose_name="Виновник аварии", on_delete=models.CASCADE,
                                                  unique=False)
    accident_cause = models.CharField(max_length=250, verbose_name="Причина аварии")
    # accident_participants = models.ManyToManyField(License, verbose_name="Участники аварии")
    # accidents_cars = models.ManyToManyField(Car, verbose_name="Автомобили, участвовавшие в аварии")
    accident_inspector = models.ForeignKey(Inspector, verbose_name="Инспектор, оформивший ДТП",
                                           on_delete=models.CASCADE, unique=False, blank=True, null=True)
    accident_europrotocol = models.OneToOneField(Europrotocol, verbose_name="ДТП по европротоколу",
                                                 on_delete=models.CASCADE, unique=False, blank=True, null=True)
    accident_photo_1 = models.ImageField(upload_to='accident_photo/',
                                         default='accident_photo/default.jpg',
                                         verbose_name="Первое фото аварии", blank=True, null=True)
    accident_photo_2 = models.ImageField(upload_to='accident_photo/',
                                         default='accident_photo/default.jpg',
                                         verbose_name="Второе фото аварии", blank=True, null=True)
    accident_comment = models.TextField(verbose_name="Комментарий к аварии")

    def __str__(self):
        return "%s от %s" % (self.number_accident, self.accident_date)

    @property
    def image_url_1(self):
        if self.accident_photo_1 and hasattr(self.accident_photo_1, 'url'):
            return self.accident_photo_1.url

    @property
    def image_url_2(self):
        if self.accident_photo_2 and hasattr(self.accident_photo_2, 'url'):
            return self.accident_photo_2.url


class Accident_Car(models.Model):
    accid = models.ForeignKey(AccidentReport, on_delete=models.CASCADE,
                              verbose_name="Все аварии с участием данного автомобиля")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name="Автомобили, участвовавшие в ДТП")

    def get_absolute_url(self):
        return reverse('workers')

    class Meta:
        unique_together = ("accid", "car")

    def __str__(self):
        return "%s, %s" % (self.accid, self.car)


# свидетель
class Witness(models.Model):
    witness_accident = models.ForeignKey(AccidentReport, on_delete=models.CASCADE, verbose_name="Свидетель аварии",
                                         unique=False)
    witness_surname = models.CharField(max_length=50, verbose_name="Фамилия свидетеля")
    witness_name = models.CharField(max_length=50, verbose_name="Имя свидетеля")
    witness_patronymic = models.CharField(max_length=50, verbose_name="Отчество свидетеля")
    witness_town = models.CharField(max_length=50, verbose_name="Город проживания свидетеля")
    witness_address = models.CharField(max_length=50, verbose_name="Адрес свидетеля")
    witness_phone = models.CharField(max_length=20, verbose_name="Телефон свидетеля")
    witness_email = models.EmailField(verbose_name="email свидетеля", blank=True, null=True)
    witness_comment = models.TextField(verbose_name="Показания свидетеля")

    def __str__(self):
        return "%s, свидетель: %s %s" % (self.witness_accident, self.witness_surname, self.witness_name)


# дополнительная таблица для аварии и ВУ (участники аварии) (разбила связь М:М)
class Lisense_Accident(models.Model):
    licen = models.ForeignKey(License, on_delete=models.CASCADE, verbose_name="Все ВУ")
    accid = models.ForeignKey(AccidentReport, on_delete=models.CASCADE, verbose_name="Список ДТП")

    def get_absolute_url(self):
        return reverse('workers')

    class Meta:
        unique_together = ("licen", "accid")

    def __str__(self):
        return "%s, %s" % (self.licen, self.accid)


# История владения автомобилем
class CarHistory(models.Model):
    car_item = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name="Автомобиль")
    history_FIO = models.CharField(max_length=100, verbose_name="ФИО владельца")
    history_birth = models.DateField(verbose_name="Дата рождения владельца")
    history_passport = models.CharField(max_length=11, help_text="4444№123456", verbose_name="Номер паспорта владельца")
    history_country = models.CharField(max_length=50, verbose_name="Страна")
    history_town = models.CharField(max_length=50, verbose_name="Город")
    history_date_from = models.DateField(verbose_name="Дата владения от")
    history_date_to = models.DateField(verbose_name="Дата владения до")
    history_document_buy = models.CharField(max_length=250, verbose_name="Документ, подтверждающий приобретение")
    history_document_selling = models.CharField(max_length=250, verbose_name="Документ, подтверждающий продажу")
    history_price_buy = models.BigIntegerField(verbose_name="Сумма покупки")
    history_price_selling = models.BigIntegerField(verbose_name="Сумма продажи")
    history_comments = models.TextField(verbose_name="Особые отметки")

    def __str__(self):
        return "%s, %s до %s" % (self.car_item, self.history_FIO, self.history_date_to)
