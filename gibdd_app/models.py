from django.db import models


# Create your models here.
# Водитель
class Driver(models.Model):
    driver_id = models.AutoField(primary_key=True, verbose_name="Код водителя")
    passport_number = models.CharField(max_length=11, verbose_name="Номер паспорта")
    driver_surname = models.CharField(max_length=50, verbose_name="Фамилия водителя")
    driver_name = models.CharField(max_length=50, verbose_name="Имя водителя")
    driver_patronymic = models.CharField(max_length=50, verbose_name="Отчество водителя")
    driver_birth = models.DateField(verbose_name="Дата рождения водителя")
    driver_town = models.CharField(max_length=50, verbose_name="Город проживания водителя")

    def __str__(self):
        return "%s %s %s %s %s" % (
            self.driver_surname, self.driver_name, self.driver_patronymic, self.driver_birth, self.passport_number)


# Категория прав
class Category(models.Model):
    category_dr_license_id = models.AutoField(primary_key=True, verbose_name="Код категории")
    category_name = models.CharField(max_length=5, verbose_name="Название категории")
    contents_category = models.TextField(verbose_name="Допустимые для управления ТС", blank=True)
    date_open_category = models.DateField(verbose_name="Дата открытия категории")

    def __str__(self):
        return "%s от %s" % (self.category_name, self.date_open_category)


MEDICAL_CHOICES = (
    ('MONTH6', '6 месяцев'),
    ('YEAR1', '1 год'),
    ('YEAR2', '2 года'),
    ('other', 'другое'),
)


# Медицинская справка
class MedicalCertificate(models.Model):
    medical_id = models.AutoField(primary_key=True)
    medical_number = models.CharField(max_length=15, verbose_name="Номер справки")
    medical_date = models.DateField(verbose_name="Дата выдачи")
    diagnosis = models.CharField(max_length=200, verbose_name="Диагноз")
    organization_give = models.CharField(max_length=300, verbose_name="Выдавшая организация")
    validity = models.CharField(max_length=11, verbose_name="Срок действия справки", choices=MEDICAL_CHOICES,
                                blank=True, null=True, default='YEAR1')
    med_photo_1 = models.ImageField(upload_to='med_photo/',
                                    default='med_photo/default.jpg',
                                    verbose_name="Скан медицинской справки, лицевая сторона", blank=True)
    med_photo_2 = models.ImageField(upload_to='med_photo/',
                                    default='med_photo/default.jpg',
                                    verbose_name="Скан медицинской справки, обратная сторона", blank=True)

    def __str__(self):
        return self.medical_number


DISQAULIF_CHOICES = (
    ('type1', 'Действующие'),
    ('type2', 'Лишение'),
    ('type3', 'Просрочены'),
)


class LicenseDisqualification(models.Model):
    disqualif_id = models.AutoField(primary_key=True, verbose_name="Код лишения прав")
    disqualif_status = models.CharField(verbose_name="Статус прав", max_length=20, choices=DISQAULIF_CHOICES,
                                        default='type1')
    disqualif_time = models.CharField(verbose_name="Срок лишения прав", max_length=10, help_text="18 месяцев")
    disqualif_date_from = models.DateField(verbose_name="Дата лишения прав")
    disqualif_date_end = models.DateField(verbose_name="Дата окончания лишение прав")
    disqualif_cause = models.CharField(max_length=200, verbose_name="Причина лишения",
                                       default="Вождение автомобиля под воздействием алкоголя")
    disqualif_alcohol_amount = models.FloatField(verbose_name="Промилле алкоголя в крови")
    disqualif_comment = models.TextField(verbose_name="Комментарий")

    def __str__(self):
        return self.disqualif_status


# Водительское удостоверение(ВУ)
class License(models.Model):
    dr_license_id = models.AutoField(primary_key=True, verbose_name="Код ВУ")
    driver_data = models.ForeignKey(Driver, on_delete=models.CASCADE, verbose_name="Данные о водителе")
    category_dr_license_data = models.ManyToManyField(Category, verbose_name="Данные о доступных категорях")
    medical_certificate_data = models.OneToOneField(MedicalCertificate, on_delete=models.CASCADE,
                                                    verbose_name="Данные о мед. справках")
    photo_dr_license = models.ImageField(upload_to='driving_license_photo/',
                                         default='driving_license_photo/default_photo_dr_license.jpg',
                                         verbose_name="Фото ВУ")
    series_dr_license = models.CharField(max_length=4, verbose_name="Серия ВУ")
    number_dr_license = models.CharField(max_length=6, verbose_name="Номер ВУ")
    status_dr_license = models.OneToOneField(LicenseDisqualification, on_delete=models.CASCADE,
                                             verbose_name="Лишение прав")
    date_issue_dr_license = models.DateField(verbose_name="Дата выдачи ВУ")
    date_end_dr_license = models.DateField(verbose_name="Дата окончания действия ВУ")
    division_give_dr_license = models.CharField(max_length=100, verbose_name="Подразделение ГИБДД, выдавшее ВУ")
    town_dr_license = models.CharField(max_length=100, verbose_name="Город выдачи ВУ")

    # фото водителя

    def __str__(self):
        return "%s %s от %s" % (self.series_dr_license, self.number_dr_license, self.date_issue_dr_license)


# Инспектор
class Inspector(models.Model):
    inspector_id = models.AutoField(primary_key=True)
    inspector_number_token = models.CharField(max_length=30, verbose_name="Номер жетона")
    photo_inspector = models.ImageField(upload_to='inspector_photo/',
                                        default='inspector_photo/default_photo_inspector.jpg',
                                        verbose_name="Фото инспектора")
    inspector_surname = models.CharField(max_length=50, verbose_name="Фамилия инспектора")
    inspector_name = models.CharField(max_length=50, verbose_name="Имя инспектора")
    inspector_patronymic = models.CharField(max_length=50, verbose_name="Отчество инспектора")
    inspector_status = models.CharField(max_length=50, verbose_name="Звание инспектора")
    inspector_division = models.CharField(max_length=40, verbose_name="Номер отделения")


DECREE_CHOICES = (
    ('type1', 'Превышение скорости'),
    ('type2', 'Проезд на запрещающий сигнал светофора или жест регулировщика'),
    ('type3', 'Выезд на встречную полосу'),
    ('type4', 'Несоблюдение правил остановки, стоянки, парковки'),
    ('type5', 'Непредоставление преимущества в движении пешеходам '),
    ('type6', 'Езда в состоянии алкогольного или наркотического опьянения'),
    ('type7', 'Управление незарегистрированным автомобилем'),
    ('type8', 'Управление ТС с нарушением правил установки на нем государственных регистрационных знаков '),
    ('type9', 'Управление ТС без документов'),
    ('type10', 'Управление ТС без прав'),
    ('type11', 'Несоблюдение правил об обязательном страховании гражданской ответственности владельцев ТС'),
    ('type12', 'Нарушение требований в области технического осмотра ТС'),
    ('type13', 'Нарушение правил регистрации'),
    ('type14', 'Превышение уровня шума или токсичности ТС'),
    ('type15', 'Нарушение правил пользования фарами,поворотниками и гудком'),
    ('type16',
     'Выпуск на линию ТС с неисправностями, со спесигналами или спецраскраской без соответствующего на то разрешения'),
    ('type17', 'Нарушение правил применения ремней безопасности или мотошлемов'),
    ('type18', 'Перевозка грузов и буксировка'),
    ('type19', 'Учебная езда'),
    ('type20', 'Приченение вреда здоровью'),
    ('type21', 'Невыполнение обязанностей в связи с ДТП'),
    ('type22', 'Несоблюдение обеспечения безопасности при ремонте, реконструкции, содержании дорог и ж/д переездов'),
    ('type23', 'Пользование телефоном за рулём'),
    ('type24', 'Нарушение правил движения по автомагистрали'),
    ('type25', 'Нарушение правил проезда перекрестков'),
    ('type26', 'Нарушение правил маневрирования'),
    ('type27', 'Нарушение правил расположения ТС на проезжей части, встречного разъезда или обгона'),
    ('type28',
     'Непредоставление преимущества в движении маршрутному ТС, ТС с включенными специальным световыми и звуковыми сигналами'),
    ('type29', 'Нарушение правил движения в жилых зонах'),
)

CAMERA_CHOICES = (
    ('f1', 'Превышение скорости'),
    ('f2', 'Проезд на запрещающий сигнал светофора'),
    ('f3', 'Выезд за стоп-линию'),
    ('f4', 'Выезд на перекресток при заторе'),
    ('f5', 'Выезд на встречную полосу движения'),
    ('f6', 'Проезд под знак "Въезд запрещён'),
    ('f7', 'Проезд под знак "Движение грузовых автомобилей запрещено'),
    ('f8', 'Выезд на полосу для маршрутных транспортных средств'),
    ('f9', 'Выезд на тротуар'),
    ('f10', 'Движение грузовиков далее второй полосы на автомагистралях и дорогах для автомобилей(МКАД)'),
    ('f11', 'Нарушение требований дорожной разметки'),
    ('f12', 'Выполнение поворота из второго ряда'),
    ('f13', 'Не включенный ближний свет фар или дневные ходовые огни'),
    ('f14', 'Нарушение правил оплаты проезда для тяжелых грузовиков'),
    ('f15', 'Непредоставление преимущества пешеходам на пешеходных переходах'),
    ('f16', 'Нарушение правил парковки'),
)

CAMERA_CHOICES1 = (
    ('n1', 'Радар Стрелка СТ/М'),
    ('n2', 'Система Автодория'),
    ('n3', 'Фоторадарные комплексы КРИС С'),
    ('n4', 'Фоторадарные комплексы КРИС П'),
    ('n5', 'Радар Кречет-С'),
    ('n6', 'Радар Перекресток'),
    ('n7', 'Комплекс фотовидеофиксации "Сова"'),
    ('n8', 'Комплекс фотовидеофиксации "Одиссей"'),
    ('n9', 'Паркон'),
)


class Camera(models.Model):
    camera_id = models.AutoField(primary_key=True)
    camera_number = models.CharField(max_length=30, verbose_name="Номер камеры")
    camera_name = models.CharField(verbose_name="Название камеры", max_length=100, choices=CAMERA_CHOICES1)
    camera_vertification_from = models.DateField(verbose_name="Дата поверки камеры", blank=True)
    camera_vertification_to = models.DateField(verbose_name="Дата действия поверки камеры до")
    camera_functions = models.CharField(max_length=100, verbose_name="Функции камеры", choices=CAMERA_CHOICES)
    camera_address = models.CharField(max_length=200, verbose_name="Расположение камеры(адрес)")


class PDD(models.Model):
    PDD_id = models.AutoField(primary_key=True)
    PDD_paragraph = models.CharField(max_length=8, verbose_name="Пункт ПДД")
    PDD_paragraph_contents = models.CharField(max_length=300, verbose_name="Содержание пункта ПДД")


KOAP_CHOICES = (
    ('k1', 'Предупреждение'),
    ('k2', 'Административный штраф'),
    ('k3', 'Конфискация орудия совершения или предмета административного нарушения'),
    ('k4', 'Лишение специального права, предоставленного лицу'),
    ('k5', 'Административный арест'),
    ('k6', 'Дисквалификация'),
    ('k7', 'Административное приостановление деятельности'),
    ('k8', 'Обязательные работы'),
    ('k9',
     'Административный запрет на посещение мест проведения официальных спортивных соревнований в дни их проведения'),
)


class KOAP(models.Model):
    KOAP_id = models.AutoField(primary_key=True)
    KOAP_paragraph = models.CharField(max_length=8, verbose_name="Пункт КОАП")
    KOAP_paragraph_contents = models.CharField(max_length=300, verbose_name="Содержание пункта КОАП")
    KOAP_type_of_violation = models.CharField(max_length=50, verbose_name="Вид нарушения", choices=KOAP_CHOICES,
                                              default='k2')


REGISTRATION_CHOICES = (
    ('type1', 'легковой'),
    ('type2', 'грузовой'),
    ('type3', 'автобус'),
    ('type4', 'мотоцикл'),
    ('type5', 'прицеп'),
    ('type6', 'полуприцеп'),
    ('type7', 'универсал легковой'),
    ('type8', 'хэтчбек(комби) легковой '),
    ('type9', 'легковой прочие'),
    ('type10', 'бортовой с тентом грузовой'),
    ('type11', 'грузовой фургон'),
    ('type12', 'легковой минивэн'),
    ('type13', 'грузовой бортовой'),
    ('type14', 'легковой седан'),
    ('type15', 'легковой купе'),
)

REGISTRATION_CHOICES2 = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ('pricep', 'прицеп'),
)

REGISTRATION_CHOICES3 = (
    ('class1', 'первый'),
    ('class2', 'второй'),
    ('class3', 'третий'),
    ('class4', 'четвертый'),
    ('class5', 'пятый'),
    ('class6', 'шестой'),
    ('class7', 'седьмой')
)


# СТС: Свидетельство о регистрации
class RegistrationCertificate(models.Model):
    registration_cert_id = models.AutoField(primary_key=True)
    registr_certificate_number = models.CharField(max_length=11, verbose_name="Номер СТС",
                                                  help_text="Например, 1234№123456")
    registr_certificate_registr_sign = models.CharField(max_length=9, help_text="А111АА777",
                                                        verbose_name="Регистрационный знак")
    registr_certificate_VIN = models.CharField(max_length=17, verbose_name="VIN",
                                               help_text="Например,SAFDYUH12R1234567")
    registr_certificate_car_model = models.CharField(max_length=50, verbose_name="Марка, модель")
    registr_certificate_type_car = models.CharField(max_length=60, verbose_name="Тип ТС", choices=REGISTRATION_CHOICES,
                                                    default='type1')
    registr_certificate_category = models.CharField(max_length=5, verbose_name="Категория ТС",
                                                    choices=REGISTRATION_CHOICES2)
    registr_certificate_year = models.IntegerField(verbose_name="Год выпуска ТС",
                                                   help_text="Например,2018")
    registr_certificate_chassis = models.CharField(verbose_name="Шасси №", max_length=30)
    registr_certificate_body = models.CharField(max_length=17, verbose_name="Кузов №",
                                                help_text="Например,SAFDYUH12R1234567")
    registr_certificate_colour = models.CharField(max_length=50, verbose_name="Цвет")
    registr_certificate_power = models.CharField(max_length=12, verbose_name="Мощность двигателя,кВт/л.с",
                                                 help_text="Например,86(117)")
    registr_certificate_ecology_class = models.CharField(max_length=20, verbose_name="Экологический класс",
                                                         choices=REGISTRATION_CHOICES3, default='class4')
    registr_certificate_passport = models.CharField(max_length=11, verbose_name="Паспорт ТС серия",
                                                    help_text="Например, 12УУ№123456")
    registr_certificate_max_weight = models.IntegerField(verbose_name="Разрешенная max масса,kg")
    registr_certificate_without_load = models.IntegerField(verbose_name="Масса без нагрузки,kg")


# Собственник
class Owner(models.Model):
    owner_id = models.AutoField(primary_key=True)
    owner_number = models.CharField(max_length=10, verbose_name="Номер свидетельства собственника")
    owner_surname = models.CharField(max_length=50, verbose_name="Фамилия собственника")
    owner_name = models.CharField(max_length=50, verbose_name="Имя собственника")
    owner_patronymic = models.CharField(max_length=50, verbose_name="Отчество собственника")
    owner_town = models.CharField(max_length=50, verbose_name="Республика,край,область")
    owner_district = models.CharField(max_length=50, verbose_name="Район", blank=True)
    owner_address = models.CharField(max_length=100, verbose_name="Адрес собственника")
    owner_comment = models.CharField(max_length=400, verbose_name="Особые отметки", blank=True)
    owner_who_give = models.CharField(max_length=200, verbose_name="Выдано ГИБДД")
    owner_date_give = models.DateField(verbose_name="Дата выдачи свидетельства собственника")


STEALING_CHOICES = (
    ('not_steal', 'Не числится в угоне'),
    ('steal', 'Числится в угоне'),
)


# Угон
class Stealing(models.Model):
    stealing_id = models.AutoField(primary_key=True)
    stealing_status = models.CharField(max_length=25, verbose_name="Статус", choices=STEALING_CHOICES, blank=True,
                                       null=True, default='not_steal')
    stealing_date = models.DateField(verbose_name="Дата угона", blank=True, null=True)
    stealing_town = models.CharField(max_length=50, verbose_name="Город угона", blank=True, null=True)
    stealing_comment = models.TextField(verbose_name="Комментарий об угоне", blank=True, null=True)


# Автошкола
class AutoSchool(models.Model):
    autoschool_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Driver, verbose_name="Ученик автошколы", on_delete=models.CASCADE)
    school_name = models.CharField(max_length=100, verbose_name="Название автошколы")
    school_photo = models.ImageField(upload_to='autoschool_photo/',
                                     default='autoschool_photo/default.jpg',
                                     verbose_name="Фото автошколы", blank=True)
    school_address = models.CharField(max_length=100, verbose_name="Адрес автошколы")
    school_phone = models.CharField(max_length=100, verbose_name="Телефон автошколы")
    school_date_from = models.DateField(verbose_name="Дата начала обучения")
    school_date_to = models.DateField(verbose_name="Дата окончания обучения")
    school_category_dr_license = models.CharField(max_length=20,
                                                  verbose_name="Обучение на данную категорию прав в автошколе")


# Автомобиль
class Car(models.Model):
    car_id = models.AutoField(primary_key=True)
    car_photo = models.ImageField(upload_to='car_photo/',
                                  default='car_photo/default_car.jpg',
                                  verbose_name="Фото автомобиля")
    car_model = models.CharField(max_length=100, verbose_name="Модель автомобиля")
    car_colour = models.CharField(max_length=50, verbose_name="Цвет автомобиля")
    car_number = models.CharField(max_length=9, verbose_name="Номер автомобиля")
    car_registr_certificate = models.OneToOneField(RegistrationCertificate, verbose_name="Свидетельство о регистрации",
                                                   on_delete=models.CASCADE)
    car_owner = models.OneToOneField(Owner, on_delete=models.CASCADE, verbose_name="Собственник автомобиля")
    car_stealing = models.OneToOneField(Stealing, on_delete=models.CASCADE, verbose_name="Угнанный автомобиль")


# Постановление
class Decree(models.Model):
    decree_id = models.AutoField(primary_key=True)
    decree_number = models.CharField(max_length=25, verbose_name="Номер постановления")
    decree_date = models.DateField(verbose_name="Дата постановления")
    decree_inspector = models.ForeignKey(Inspector, verbose_name="Инспектор, выписавший постановление", null=True,
                                         blank=True, on_delete=models.CASCADE)
    decree_camera = models.ForeignKey(Camera, verbose_name="Средство фиксации нарушения", on_delete=models.CASCADE,
                                      null=True, blank=True, )
    decree_license_data = models.ForeignKey(License, verbose_name="Данные ВУ для вынесения постановления",
                                            on_delete=models.CASCADE)
    decree_car = models.ForeignKey(Car, verbose_name="Данные о нарушевшем автомобиле", on_delete=models.CASCADE)
    decree_violation = models.CharField(max_length=200, verbose_name="Нарушение(смысл)", choices=DECREE_CHOICES,
                                        null=True)
    decree_violation_text = models.TextField(verbose_name="Полное описание нарушения", blank=True)
    decree_total_speed = models.IntegerField(verbose_name="Скорость движения в момент нарушения", blank=True)
    decree_photo = models.ImageField(upload_to='decree_photo/',
                                     default='decree_photo/default.jpg',
                                     verbose_name="Фото нарушения")
    decree_KOAP = models.ManyToManyField(KOAP, verbose_name="Нарушенные пункты КОАП")
    decree_PDD = models.ManyToManyField(PDD, verbose_name="Нарушенные пункты ПДД")


# штраф
class Fine(models.Model):
    fine_id = models.AutoField(primary_key=True)
    fine_amount = models.IntegerField(verbose_name="Первоначальная сумма штрафа")
    fine_discount = models.FloatField(verbose_name="Скидка", blank=True)
    date_of_payment_fine = models.DateTimeField(verbose_name="Дата оплаты штрафа", blank=True)
    fine_status = models.CharField(max_length=50, verbose_name="Статус штрафа")
    fine_license_data = models.ForeignKey(License, on_delete=models.CASCADE, verbose_name="Данные о ВУ")
    fine_decree_data = models.OneToOneField(Decree, verbose_name="Данные о постановлении", on_delete=models.CASCADE)
    fine_car_data = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name="Штраф для данного автомобиля")


ACCIDENT_CHOICES = (
    ('light', 'легкая'),
    ('middle', 'средней тяжести'),
    ('hard', 'тяжкий вред'),
    ('without', 'без вреда здоровью'),
    ('not_define', 'не указано'),
)


# авария
class AccidentReport(models.Model):
    accident_id = models.AutoField(primary_key=True)
    accident_date = models.DateField(verbose_name="Дата аварии")
    accident_time = models.TimeField(verbose_name="Время аварии")
    number_accident = models.CharField(max_length=40, verbose_name="Номер протокола аварии")
    accident_paper_date = models.DateField(verbose_name="Дата составления протокола")
    accident_paper_time = models.TimeField(verbose_name="Время составления протокола")
    accident_address = models.CharField(max_length=200, verbose_name="Адрес аварии")
    accident_severity = models.CharField(max_length=50, verbose_name="Тяжесть аварии", choices=ACCIDENT_CHOICES,
                                         blank=True, null=True, default='not_define')
    accident_number_of_people = models.IntegerField(verbose_name="Количество людей в аварии")
    accident_death = models.IntegerField(verbose_name="Смертельный исход, взрослые (количество)", default=0)
    accident_children = models.IntegerField(verbose_name="Из участвовавших в аварии-дети", default=0)
    accident_children_death = models.IntegerField(verbose_name="Смертельный исход, дети(количество)", default=0)
    accident_causer_person = models.OneToOneField(Driver, verbose_name="Виновник аварии", on_delete=models.CASCADE)
    accident_cause = models.TextField(verbose_name="Причина аварии")
    accident_comment = models.TextField(verbose_name="Комментарий к аварии")
    accident_participants = models.ManyToManyField(License, verbose_name="Участники аварии")
    accidents_cars = models.ManyToManyField(Car, verbose_name="Автомобили, участвовавшие в аварии")
    accident_inspector = models.ForeignKey(Inspector, verbose_name="Инспектор, оформивший ДТП",
                                           on_delete=models.CASCADE)
    accident_photo_1 = models.ImageField(upload_to='accident_photo/',
                                         default='accident_photo/default.jpg',
                                         verbose_name="Первое фото аварии", blank=True)
    accident_photo_2 = models.ImageField(upload_to='accident_photo/',
                                         default='accident_photo/default.jpg',
                                         verbose_name="Второе фото аварии", blank=True)


# свидетель
class Witness(models.Model):
    witness_id = models.AutoField(primary_key=True)
    witness_accident = models.ForeignKey(AccidentReport, on_delete=models.CASCADE, verbose_name="Свидетель аварии")
    witness_surname = models.CharField(max_length=50, verbose_name="Фамилия свидетеля")
    witness_name = models.CharField(max_length=50, verbose_name="Имя свидетеля")
    witness_patronymic = models.CharField(max_length=50, verbose_name="Отчество свидетеля")
    witness_town = models.CharField(max_length=50, verbose_name="Город проживания свидетеля")
    witness_address = models.CharField(max_length=50, verbose_name="Адрес свидетеля")
    witness_phone = models.CharField(max_length=20, verbose_name="Телефон свидетеля")
    witness_email = models.EmailField(verbose_name="email свидетеля", blank=True)
    witness_comment = models.TextField(verbose_name="Показания свидетеля")


INSURANCE_CHOICES = (
    ('type1', 'ОСАГО'),
    ('type2', 'КАСКО'),
)

INSURANCE_CHOICES2 = (
    ('type1', 'ОСАГО'),
    ('type2', 'ОСАГО без ограничений'),
    ('type3', 'открытая страховка ОСАГО'),

)


# Диагностическая карта
class DiagnosticCard(models.Model):
    diagnostic_id = models.AutoField(primary_key=True)
    diagnostic_number = models.CharField(max_length=15, verbose_name="Регистрационный номер")
    diagnostic_car = models.ForeignKey(Car, verbose_name="Автомобиль для диагностики", on_delete=models.CASCADE)
    diagnostic_date_from = models.DateField(verbose_name="Дата выдачи")
    diagnostic_date_to = models.DateField(verbose_name="Срок действия до")
    diagnostic_company = models.TextField(verbose_name="Пункт технического осмотра")
    diagnostic_results = models.TextField(verbose_name="Результаты диагностирования")


# Страхововй полис
class Insurance(models.Model):
    insurance_id = models.AutoField(primary_key=True)
    insurance_number = models.CharField(max_length=15, verbose_name="Номер полиса", help_text="ЕЕЕ№1234567890")
    insurance_company = models.CharField(max_length=100, verbose_name="Страховая компания")
    insurance_type = models.CharField(max_length=10, verbose_name="Тип полиса", choices=INSURANCE_CHOICES,
                                      default='type1')
    insurance_date_from = models.DateField(verbose_name="Дата начала действия")
    insurance_date_to = models.DateField(verbose_name="Дата окончания действия")
    insurance_confines = models.CharField(max_length=50, verbose_name="Ограничения", choices=INSURANCE_CHOICES2,
                                          default='type1')
    insurance_diagnostic_card = models.OneToOneField(DiagnosticCard,
                                                     verbose_name="Диагностическая карта (ТО) о состоянии автомобиля",
                                                     on_delete=models.CASCADE)
    insurance_driving_license = models.ManyToManyField(License,
                                                       verbose_name="Допущенные к управления автомобилем по полису")
    insurance_car = models.ForeignKey(Car, verbose_name="Полис на автомобиль", on_delete=models.CASCADE)
    insurance_comments = models.TextField(verbose_name="Комментарий к полису")


# История владения автомобилем
class CarHistory(models.Model):
    car_history_id = models.AutoField(primary_key=True)
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
