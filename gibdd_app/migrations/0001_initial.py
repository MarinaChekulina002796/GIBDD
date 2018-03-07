# Generated by Django 2.0.2 on 2018-03-06 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccidentReport',
            fields=[
                ('accident_id', models.AutoField(primary_key=True, serialize=False)),
                ('accident_date', models.DateField(verbose_name='Дата аварии')),
                ('accident_time', models.TimeField(verbose_name='Время аварии')),
                ('number_accident', models.CharField(max_length=40, verbose_name='Номер протокола аварии')),
                ('accident_paper_date', models.DateField(verbose_name='Дата составления протокола')),
                ('accident_paper_time', models.TimeField(verbose_name='Время составления протокола')),
                ('accident_address', models.CharField(max_length=200, verbose_name='Адрес аварии')),
                ('accident_severity', models.CharField(blank=True, choices=[('light', 'легкая'), ('middle', 'средней тяжести'), ('hard', 'тяжкий вред'), ('without', 'без вреда здоровью'), ('not_define', 'не указано')], default='not_define', max_length=50, null=True, verbose_name='Тяжесть аварии')),
                ('accident_number_of_people', models.IntegerField(verbose_name='Количество людей в аварии')),
                ('accident_death', models.IntegerField(default=0, verbose_name='Смертельный исход, взрослые (количество)')),
                ('accident_children', models.IntegerField(default=0, verbose_name='Из участвовавших в аварии-дети')),
                ('accident_children_death', models.IntegerField(default=0, verbose_name='Смертельный исход, дети(количество)')),
                ('accident_cause', models.TextField(verbose_name='Причина аварии')),
                ('accident_comment', models.TextField(verbose_name='Комментарий к аварии')),
                ('accident_photo_1', models.ImageField(blank=True, default='accident_photo/default.jpg', upload_to='accident_photo/', verbose_name='Первое фото аварии')),
                ('accident_photo_2', models.ImageField(blank=True, default='accident_photo/default.jpg', upload_to='accident_photo/', verbose_name='Второе фото аварии')),
            ],
        ),
        migrations.CreateModel(
            name='AutoSchool',
            fields=[
                ('autoschool_id', models.AutoField(primary_key=True, serialize=False)),
                ('school_name', models.CharField(max_length=100, verbose_name='Название автошколы')),
                ('school_photo', models.ImageField(blank=True, default='autoschool_photo/default.jpg', upload_to='autoschool_photo/', verbose_name='Фото автошколы')),
                ('school_address', models.CharField(max_length=100, verbose_name='Адрес автошколы')),
                ('school_phone', models.CharField(max_length=100, verbose_name='Телефон автошколы')),
                ('school_date_from', models.DateField(verbose_name='Дата начала обучения')),
                ('school_date_to', models.DateField(verbose_name='Дата окончания обучения')),
                ('school_category_dr_license', models.CharField(max_length=20, verbose_name='Обучение на данную категорию прав в автошколе')),
            ],
        ),
        migrations.CreateModel(
            name='Camera',
            fields=[
                ('camera_id', models.AutoField(primary_key=True, serialize=False)),
                ('camera_number', models.CharField(max_length=30, verbose_name='Номер камеры')),
                ('camera_name', models.CharField(choices=[('n1', 'Радар Стрелка СТ/М'), ('n2', 'Система Автодория'), ('n3', 'Фоторадарные комплексы КРИС С'), ('n4', 'Фоторадарные комплексы КРИС П'), ('n5', 'Радар Кречет-С'), ('n6', 'Радар Перекресток'), ('n7', 'Комплекс фотовидеофиксации "Сова"'), ('n8', 'Комплекс фотовидеофиксации "Одиссей"'), ('n9', 'Паркон')], max_length=100, verbose_name='Название камеры')),
                ('camera_vertification_from', models.DateField(blank=True, verbose_name='Дата поверки камеры')),
                ('camera_vertification_to', models.DateField(verbose_name='Дата действия поверки камеры до')),
                ('camera_functions', models.CharField(choices=[('f1', 'Превышение скорости'), ('f2', 'Проезд на запрещающий сигнал светофора'), ('f3', 'Выезд за стоп-линию'), ('f4', 'Выезд на перекресток при заторе'), ('f5', 'Выезд на встречную полосу движения'), ('f6', 'Проезд под знак "Въезд запрещён'), ('f7', 'Проезд под знак "Движение грузовых автомобилей запрещено'), ('f8', 'Выезд на полосу для маршрутных транспортных средств'), ('f9', 'Выезд на тротуар'), ('f10', 'Движение грузовиков далее второй полосы на автомагистралях и дорогах для автомобилей(МКАД)'), ('f11', 'Нарушение требований дорожной разметки'), ('f12', 'Выполнение поворота из второго ряда'), ('f13', 'Не включенный ближний свет фар или дневные ходовые огни'), ('f14', 'Нарушение правил оплаты проезда для тяжелых грузовиков'), ('f15', 'Непредоставление преимущества пешеходам на пешеходных переходах'), ('f16', 'Нарушение правил парковки')], max_length=100, verbose_name='Функции камеры')),
                ('camera_address', models.CharField(max_length=200, verbose_name='Расположение камеры(адрес)')),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('car_id', models.AutoField(primary_key=True, serialize=False)),
                ('car_photo', models.ImageField(default='car_photo/default_car.jpg', upload_to='car_photo/', verbose_name='Фото автомобиля')),
                ('car_model', models.CharField(max_length=100, verbose_name='Модель автомобиля')),
                ('car_colour', models.CharField(max_length=50, verbose_name='Цвет автомобиля')),
                ('car_number', models.CharField(max_length=9, verbose_name='Номер автомобиля')),
            ],
        ),
        migrations.CreateModel(
            name='CarHistory',
            fields=[
                ('car_history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_FIO', models.CharField(max_length=100, verbose_name='ФИО владельца')),
                ('history_birth', models.DateField(verbose_name='Дата рождения владельца')),
                ('history_passport', models.CharField(help_text='4444№123456', max_length=11, verbose_name='Номер паспорта владельца')),
                ('history_country', models.CharField(max_length=50, verbose_name='Страна')),
                ('history_town', models.CharField(max_length=50, verbose_name='Город')),
                ('history_date_from', models.DateField(verbose_name='Дата владения от')),
                ('history_date_to', models.DateField(verbose_name='Дата владения до')),
                ('history_document_buy', models.CharField(max_length=250, verbose_name='Документ, подтверждающий приобретение')),
                ('history_document_selling', models.CharField(max_length=250, verbose_name='Документ, подтверждающий продажу')),
                ('history_price_buy', models.BigIntegerField(verbose_name='Сумма покупки')),
                ('history_price_selling', models.BigIntegerField(verbose_name='Сумма продажи')),
                ('history_comments', models.TextField(verbose_name='Особые отметки')),
                ('car_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gibdd_app.Car', verbose_name='Автомобиль')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_dr_license_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Код категории')),
                ('category_name', models.CharField(max_length=5, verbose_name='Название категории')),
                ('contents_category', models.TextField(blank=True, verbose_name='Допустимые для управления ТС')),
                ('date_open_category', models.DateField(verbose_name='Дата открытия категории')),
            ],
        ),
        migrations.CreateModel(
            name='Decree',
            fields=[
                ('decree_id', models.AutoField(primary_key=True, serialize=False)),
                ('decree_number', models.CharField(max_length=25, verbose_name='Номер постановления')),
                ('decree_date', models.DateField(verbose_name='Дата постановления')),
                ('decree_violation', models.CharField(choices=[('type1', 'Превышение скорости'), ('type2', 'Проезд на запрещающий сигнал светофора или жест регулировщика'), ('type3', 'Выезд на встречную полосу'), ('type4', 'Несоблюдение правил остановки, стоянки, парковки'), ('type5', 'Непредоставление преимущества в движении пешеходам '), ('type6', 'Езда в состоянии алкогольного или наркотического опьянения'), ('type7', 'Управление незарегистрированным автомобилем'), ('type8', 'Управление ТС с нарушением правил установки на нем государственных регистрационных знаков '), ('type9', 'Управление ТС без документов'), ('type10', 'Управление ТС без прав'), ('type11', 'Несоблюдение правил об обязательном страховании гражданской ответственности владельцев ТС'), ('type12', 'Нарушение требований в области технического осмотра ТС'), ('type13', 'Нарушение правил регистрации'), ('type14', 'Превышение уровня шума или токсичности ТС'), ('type15', 'Нарушение правил пользования фарами,поворотниками и гудком'), ('type16', 'Выпуск на линию ТС с неисправностями, со спесигналами или спецраскраской без соответствующего на то разрешения'), ('type17', 'Нарушение правил применения ремней безопасности или мотошлемов'), ('type18', 'Перевозка грузов и буксировка'), ('type19', 'Учебная езда'), ('type20', 'Приченение вреда здоровью'), ('type21', 'Невыполнение обязанностей в связи с ДТП'), ('type22', 'Несоблюдение обеспечения безопасности при ремонте, реконструкции, содержании дорог и ж/д переездов'), ('type23', 'Пользование телефоном за рулём'), ('type24', 'Нарушение правил движения по автомагистрали'), ('type25', 'Нарушение правил проезда перекрестков'), ('type26', 'Нарушение правил маневрирования'), ('type27', 'Нарушение правил расположения ТС на проезжей части, встречного разъезда или обгона'), ('type28', 'Непредоставление преимущества в движении маршрутному ТС, ТС с включенными специальным световыми и звуковыми сигналами'), ('type29', 'Нарушение правил движения в жилых зонах')], max_length=200, null=True, verbose_name='Нарушение(смысл)')),
                ('decree_violation_text', models.TextField(blank=True, verbose_name='Полное описание нарушения')),
                ('decree_total_speed', models.IntegerField(blank=True, verbose_name='Скорость движения в момент нарушения')),
                ('decree_photo', models.ImageField(default='decree_photo/default.jpg', upload_to='decree_photo/', verbose_name='Фото нарушения')),
            ],
        ),
        migrations.CreateModel(
            name='DiagnosticCard',
            fields=[
                ('diagnostic_id', models.AutoField(primary_key=True, serialize=False)),
                ('diagnostic_number', models.CharField(max_length=15, verbose_name='Регистрационный номер')),
                ('diagnostic_date_from', models.DateField(verbose_name='Дата выдачи')),
                ('diagnostic_date_to', models.DateField(verbose_name='Срок действия до')),
                ('diagnostic_company', models.TextField(verbose_name='Пункт технического осмотра')),
                ('diagnostic_results', models.TextField(verbose_name='Результаты диагностирования')),
                ('diagnostic_car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gibdd_app.Car', verbose_name='Автомобиль для диагностики')),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('driver_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Код водителя')),
                ('passport_number', models.CharField(max_length=11, verbose_name='Номер паспорта')),
                ('driver_surname', models.CharField(max_length=50, verbose_name='Фамилия водителя')),
                ('driver_name', models.CharField(max_length=50, verbose_name='Имя водителя')),
                ('driver_patronymic', models.CharField(max_length=50, verbose_name='Отчество водителя')),
                ('driver_birth', models.DateField(verbose_name='Дата рождения водителя')),
                ('driver_town', models.CharField(max_length=50, verbose_name='Город проживания водителя')),
            ],
        ),
        migrations.CreateModel(
            name='Fine',
            fields=[
                ('fine_id', models.AutoField(primary_key=True, serialize=False)),
                ('fine_amount', models.IntegerField(verbose_name='Первоначальная сумма штрафа')),
                ('fine_discount', models.FloatField(blank=True, verbose_name='Скидка')),
                ('date_of_payment_fine', models.DateTimeField(blank=True, verbose_name='Дата оплаты штрафа')),
                ('fine_status', models.CharField(max_length=50, verbose_name='Статус штрафа')),
                ('fine_car_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gibdd_app.Car', verbose_name='Штраф для данного автомобиля')),
                ('fine_decree_data', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='gibdd_app.Decree', verbose_name='Данные о постановлении')),
            ],
        ),
        migrations.CreateModel(
            name='Inspector',
            fields=[
                ('inspector_id', models.AutoField(primary_key=True, serialize=False)),
                ('inspector_number_token', models.CharField(max_length=30, verbose_name='Номер жетона')),
                ('photo_inspector', models.ImageField(default='inspector_photo/default_photo_inspector.jpg', upload_to='inspector_photo/', verbose_name='Фото инспектора')),
                ('inspector_surname', models.CharField(max_length=50, verbose_name='Фамилия инспектора')),
                ('inspector_name', models.CharField(max_length=50, verbose_name='Имя инспектора')),
                ('inspector_patronymic', models.CharField(max_length=50, verbose_name='Отчество инспектора')),
                ('inspector_status', models.CharField(max_length=50, verbose_name='Звание инспектора')),
                ('inspector_division', models.CharField(max_length=40, verbose_name='Номер отделения')),
            ],
        ),
        migrations.CreateModel(
            name='Insurance',
            fields=[
                ('insurance_id', models.AutoField(primary_key=True, serialize=False)),
                ('insurance_number', models.CharField(help_text='ЕЕЕ№1234567890', max_length=15, verbose_name='Номер полиса')),
                ('insurance_company', models.CharField(max_length=100, verbose_name='Страховая компания')),
                ('insurance_type', models.CharField(choices=[('type1', 'ОСАГО'), ('type2', 'КАСКО')], default='type1', max_length=10, verbose_name='Тип полиса')),
                ('insurance_date_from', models.DateField(verbose_name='Дата начала действия')),
                ('insurance_date_to', models.DateField(verbose_name='Дата окончания действия')),
                ('insurance_confines', models.CharField(choices=[('type1', 'ОСАГО'), ('type2', 'ОСАГО без ограничений'), ('type3', 'открытая страховка ОСАГО')], default='type1', max_length=50, verbose_name='Ограничения')),
                ('insurance_comments', models.TextField(verbose_name='Комментарий к полису')),
                ('insurance_car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gibdd_app.Car', verbose_name='Полис на автомобиль')),
                ('insurance_diagnostic_card', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='gibdd_app.DiagnosticCard', verbose_name='Диагностическая карта (ТО) о состоянии автомобиля')),
            ],
        ),
        migrations.CreateModel(
            name='KOAP',
            fields=[
                ('KOAP_id', models.AutoField(primary_key=True, serialize=False)),
                ('KOAP_paragraph', models.CharField(max_length=8, verbose_name='Пункт КОАП')),
                ('KOAP_paragraph_contents', models.CharField(max_length=300, verbose_name='Содержание пункта КОАП')),
                ('KOAP_type_of_violation', models.CharField(choices=[('k1', 'Предупреждение'), ('k2', 'Административный штраф'), ('k3', 'Конфискация орудия совершения или предмета административного нарушения'), ('k4', 'Лишение специального права, предоставленного лицу'), ('k5', 'Административный арест'), ('k6', 'Дисквалификация'), ('k7', 'Административное приостановление деятельности'), ('k8', 'Обязательные работы'), ('k9', 'Административный запрет на посещение мест проведения официальных спортивных соревнований в дни их проведения')], default='k2', max_length=50, verbose_name='Вид нарушения')),
            ],
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('dr_license_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Код ВУ')),
                ('photo_dr_license', models.ImageField(default='driving_license_photo/default_photo_dr_license.jpg', upload_to='driving_license_photo/', verbose_name='Фото ВУ')),
                ('series_dr_license', models.CharField(max_length=4, verbose_name='Серия ВУ')),
                ('number_dr_license', models.CharField(max_length=6, verbose_name='Номер ВУ')),
                ('date_issue_dr_license', models.DateField(verbose_name='Дата выдачи ВУ')),
                ('date_end_dr_license', models.DateField(verbose_name='Дата окончания действия ВУ')),
                ('division_give_dr_license', models.CharField(max_length=100, verbose_name='Подразделение ГИБДД, выдавшее ВУ')),
                ('town_dr_license', models.CharField(max_length=100, verbose_name='Город выдачи ВУ')),
                ('category_dr_license_data', models.ManyToManyField(to='gibdd_app.Category', verbose_name='Данные о доступных категорях')),
                ('driver_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gibdd_app.Driver', verbose_name='Данные о водителе')),
            ],
        ),
        migrations.CreateModel(
            name='MedicalCertificate',
            fields=[
                ('medical_id', models.AutoField(primary_key=True, serialize=False)),
                ('medical_number', models.CharField(max_length=15, verbose_name='Номер справки')),
                ('medical_date', models.DateField(verbose_name='Дата выдачи')),
                ('diagnosis', models.CharField(max_length=200, verbose_name='Диагноз')),
                ('organization_give', models.CharField(max_length=300, verbose_name='Выдавшая организация')),
                ('validity', models.CharField(blank=True, choices=[('MONTH6', '6 месяцев'), ('YEAR1', '1 год'), ('YEAR2', '2 года'), ('other', 'другое')], default='YEAR1', max_length=11, null=True, verbose_name='Срок действия справки')),
                ('med_photo_1', models.ImageField(blank=True, default='med_photo/default.jpg', upload_to='med_photo/', verbose_name='Скан медицинской справки, лицевая сторона')),
                ('med_photo_2', models.ImageField(blank=True, default='med_photo/default.jpg', upload_to='med_photo/', verbose_name='Скан медицинской справки, обратная сторона')),
            ],
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('owner_id', models.AutoField(primary_key=True, serialize=False)),
                ('owner_number', models.CharField(max_length=10, verbose_name='Номер свидетельства собственника')),
                ('owner_surname', models.CharField(max_length=50, verbose_name='Фамилия собственника')),
                ('owner_name', models.CharField(max_length=50, verbose_name='Имя собственника')),
                ('owner_patronymic', models.CharField(max_length=50, verbose_name='Отчество собственника')),
                ('owner_town', models.CharField(max_length=50, verbose_name='Республика,край,область')),
                ('owner_district', models.CharField(blank=True, max_length=50, verbose_name='Район')),
                ('owner_address', models.CharField(max_length=100, verbose_name='Адрес собственника')),
                ('owner_comment', models.CharField(blank=True, max_length=400, verbose_name='Особые отметки')),
                ('owner_who_give', models.CharField(max_length=200, verbose_name='Выдано ГИБДД')),
                ('owner_date_give', models.DateField(verbose_name='Дата выдачи свидетельства собственника')),
            ],
        ),
        migrations.CreateModel(
            name='PDD',
            fields=[
                ('PDD_id', models.AutoField(primary_key=True, serialize=False)),
                ('PDD_paragraph', models.CharField(max_length=8, verbose_name='Пункт ПДД')),
                ('PDD_paragraph_contents', models.CharField(max_length=300, verbose_name='Содержание пункта ПДД')),
            ],
        ),
        migrations.CreateModel(
            name='RegistrationCertificate',
            fields=[
                ('registration_cert_id', models.AutoField(primary_key=True, serialize=False)),
                ('registr_certificate_number', models.CharField(help_text='Например, 1234№123456', max_length=11, verbose_name='Номер СТС')),
                ('registr_certificate_registr_sign', models.CharField(help_text='А111АА777', max_length=9, verbose_name='Регистрационный знак')),
                ('registr_certificate_VIN', models.CharField(help_text='Например,SAFDYUH12R1234567', max_length=17, verbose_name='VIN')),
                ('registr_certificate_car_model', models.CharField(max_length=50, verbose_name='Марка, модель')),
                ('registr_certificate_type_car', models.CharField(choices=[('type1', 'легковой'), ('type2', 'грузовой'), ('type3', 'автобус'), ('type4', 'мотоцикл'), ('type5', 'прицеп'), ('type6', 'полуприцеп'), ('type7', 'универсал легковой'), ('type8', 'хэтчбек(комби) легковой '), ('type9', 'легковой прочие'), ('type10', 'бортовой с тентом грузовой'), ('type11', 'грузовой фургон'), ('type12', 'легковой минивэн'), ('type13', 'грузовой бортовой'), ('type14', 'легковой седан'), ('type15', 'легковой купе')], default='type1', max_length=60, verbose_name='Тип ТС')),
                ('registr_certificate_category', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('pricep', 'прицеп')], max_length=5, verbose_name='Категория ТС')),
                ('registr_certificate_year', models.IntegerField(help_text='Например,2018', verbose_name='Год выпуска ТС')),
                ('registr_certificate_chassis', models.CharField(max_length=30, verbose_name='Шасси №')),
                ('registr_certificate_body', models.CharField(help_text='Например,SAFDYUH12R1234567', max_length=17, verbose_name='Кузов №')),
                ('registr_certificate_colour', models.CharField(max_length=50, verbose_name='Цвет')),
                ('registr_certificate_power', models.CharField(help_text='Например,86(117)', max_length=12, verbose_name='Мощность двигателя,кВт/л.с')),
                ('registr_certificate_ecology_class', models.CharField(choices=[('class1', 'первый'), ('class2', 'второй'), ('class3', 'третий'), ('class4', 'четвертый'), ('class5', 'пятиый'), ('class6', 'шестой'), ('class7', 'седьмой')], default='class4', max_length=20, verbose_name='Экологический класс')),
                ('registr_certificate_passport', models.CharField(help_text='Например, 12УУ№123456', max_length=11, verbose_name='Паспорт ТС серия')),
                ('registr_certificate_max_weight', models.IntegerField(verbose_name='Разрешенная max масса,kg')),
                ('registr_certificate_without_load', models.IntegerField(verbose_name='Масса без нагрузки,kg')),
            ],
        ),
        migrations.CreateModel(
            name='Stealing',
            fields=[
                ('stealing_id', models.AutoField(primary_key=True, serialize=False)),
                ('stealing_status', models.CharField(blank=True, choices=[('not_steal', 'Не числится в угоне'), ('steal', 'Числится в угоне')], default='not_steal', max_length=25, null=True, verbose_name='Статус')),
                ('stealing_date', models.DateField(blank=True, null=True, verbose_name='Дата угона')),
                ('stealing_town', models.CharField(blank=True, max_length=50, null=True, verbose_name='Город угона')),
                ('stealing_comment', models.TextField(blank=True, null=True, verbose_name='Комментарий об угоне')),
            ],
        ),
        migrations.CreateModel(
            name='Witness',
            fields=[
                ('witness_id', models.AutoField(primary_key=True, serialize=False)),
                ('witness_surname', models.CharField(max_length=50, verbose_name='Фамилия свидетеля')),
                ('witness_name', models.CharField(max_length=50, verbose_name='Имя свидетеля')),
                ('witness_patronymic', models.CharField(max_length=50, verbose_name='Отчество свидетеля')),
                ('witness_town', models.CharField(max_length=50, verbose_name='Город проживания свидетеля')),
                ('witness_address', models.CharField(max_length=50, verbose_name='Адрес свидетеля')),
                ('witness_phone', models.CharField(max_length=20, verbose_name='Телефон свидетеля')),
                ('witness_email', models.EmailField(blank=True, max_length=254, verbose_name='email свидетеля')),
                ('witness_comment', models.TextField(verbose_name='Показания свидетеля')),
                ('witness_accident', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gibdd_app.AccidentReport', verbose_name='Свидетель аварии')),
            ],
        ),
        migrations.AddField(
            model_name='license',
            name='medical_certificate_data',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='gibdd_app.MedicalCertificate', verbose_name='Данные о мед. справках'),
        ),
        migrations.AddField(
            model_name='insurance',
            name='insurance_driving_license',
            field=models.ManyToManyField(to='gibdd_app.License', verbose_name='Допущенные к управления автомобилем по полису'),
        ),
        migrations.AddField(
            model_name='fine',
            name='fine_license_data',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gibdd_app.License', verbose_name='Данные о ВУ'),
        ),
        migrations.AddField(
            model_name='decree',
            name='decree_KOAP',
            field=models.ManyToManyField(to='gibdd_app.KOAP', verbose_name='Нарушенные пункты КОАП'),
        ),
        migrations.AddField(
            model_name='decree',
            name='decree_PDD',
            field=models.ManyToManyField(to='gibdd_app.PDD', verbose_name='Нарушенные пункты ПДД'),
        ),
        migrations.AddField(
            model_name='decree',
            name='decree_camera',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gibdd_app.Camera', verbose_name='Средство фиксации нарушения'),
        ),
        migrations.AddField(
            model_name='decree',
            name='decree_car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gibdd_app.Car', verbose_name='Данные о нарушевшем автомобиле'),
        ),
        migrations.AddField(
            model_name='decree',
            name='decree_inspector',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gibdd_app.Inspector', verbose_name='Инспектор, выписавший постановление'),
        ),
        migrations.AddField(
            model_name='decree',
            name='decree_license_data',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gibdd_app.License', verbose_name='Данные ВУ для вынесения постановления'),
        ),
        migrations.AddField(
            model_name='car',
            name='car_owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='gibdd_app.Owner', verbose_name='Собственник автомобиля'),
        ),
        migrations.AddField(
            model_name='car',
            name='car_registr_certificate',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='gibdd_app.RegistrationCertificate', verbose_name='Свидетельство о регистрации'),
        ),
        migrations.AddField(
            model_name='car',
            name='car_stealing',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='gibdd_app.Stealing', verbose_name='Угнанный автомобиль'),
        ),
        migrations.AddField(
            model_name='autoschool',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gibdd_app.Driver', verbose_name='Ученик автошколы'),
        ),
        migrations.AddField(
            model_name='accidentreport',
            name='accident_causer_person',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='gibdd_app.Driver', verbose_name='Виновник аварии'),
        ),
        migrations.AddField(
            model_name='accidentreport',
            name='accident_inspector',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gibdd_app.Inspector', verbose_name='Инспектор, оформивший ДТП'),
        ),
        migrations.AddField(
            model_name='accidentreport',
            name='accident_participants',
            field=models.ManyToManyField(to='gibdd_app.License', verbose_name='Участники аварии'),
        ),
        migrations.AddField(
            model_name='accidentreport',
            name='accidents_cars',
            field=models.ManyToManyField(to='gibdd_app.Car', verbose_name='Автомобили, участвовавшие в аварии'),
        ),
    ]