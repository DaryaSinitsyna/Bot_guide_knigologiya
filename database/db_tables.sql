CREATE TABLE public.bot_user (
	user_id int4 NOT NULL GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE),
	user_telegram_id int8 NOT NULL,
	status bool NOT NULL DEFAULT false,
	score int4 NOT NULL DEFAULT 0,
	current_question int4 NOT NULL DEFAULT 0,
	CONSTRAINT bot_user_user_telegram_id_key UNIQUE (user_telegram_id),
	CONSTRAINT user_pkey PRIMARY KEY (user_id)
);


CREATE TABLE public.question (
	question_id serial4 NOT NULL,
	text_question text NOT NULL,
	number_question int4 NULL,
	image_path text NULL,
	CONSTRAINT pk_question_id PRIMARY KEY (question_id)
);


CREATE TABLE public.test_result (
	result_id serial4 NOT NULL,
	score_range int4range NOT NULL,
	text_result text NOT NULL,
	url text NULL,
	CONSTRAINT pk_test_result PRIMARY KEY (result_id)
);


CREATE TABLE public.answer (
	answer_id serial4 NOT NULL,
	serial_number int4 NOT NULL,
	text_answer text NOT NULL,
	fk_question_id int4 NOT NULL,
	CONSTRAINT pk_answer_id PRIMARY KEY (answer_id),
	CONSTRAINT answer_fk_question_id_fkey FOREIGN KEY (fk_question_id) REFERENCES public.question(question_id)
);


INSERT INTO public.question (text_question,number_question,image_path) VALUES
	 ('Какое изображение пейзажа привлекает вас больше всего?',2,'media/photos/test_2.jpg'),
	 ('Какой тип героя вам ближе всего?',3,'media/photos/test_3.jpg'),
	 ('Что привлекает вас в книжных описаниях?',4,'media/photos/test_4.jpg'),
	 ('Какая среда вам ближе всего?',5,'media/photos/test_5.jpg'),
	 ('Какие качества вам важны в книге?',7,'media/photos/test_7.jpg'),
	 ('Какие концовки вы предпочитаете в книгах?',6,'media/photos/test_6.jpg'),
	 ('Какие фильмы вам нравятся больше всего?',1,'media/photos/test_1.jpg');


INSERT INTO public.answer (serial_number,text_answer,fk_question_id) VALUES
	 (1,'Фантастические и приключенческие фильмы',1),
	 (2,'Драмы и мелодрамы',1),
	 (3,'Комедии и сатира',1),
	 (1,'Космический взгляд на звездное небо',2),
	 (2,'Закат на океанском пляже',2),
	 (3,'Пейзаж с горным озером',2),
	 (1,'Герои, обладающие сверхъестественными способностями',3),
	 (2,'Обычные люди, с их проблемами и радостями',3),
	 (3,'Герои, ведущие активный образ жизни и участвующие в опасных приключениях',3),
	 (1,'Фантастические и миролюбивые места',4);
INSERT INTO public.answer (serial_number,text_answer,fk_question_id) VALUES
	 (2,'Чувства и эмоции главных героев',4),
	 (3,'Описания энергичных событий и волнующих сцен',4),
	 (1,'Будущее со сменой реальностей',5),
	 (2,'Современность с ее проблемами и реалиями',5),
	 (3,'Прошлое, где можно открыть новые исторические тайны',5),
	 (1,'Положительную, счастливый конец',6),
	 (2,'Реалистичную, любой конец, который кажется логичным',6),
	 (3,'Непредсказуемую, с сюрпризом и разочарованиями',6),
	 (1,'Оригинальность сюжета и необычные миры',7),
	 (2,'Глубина эмоций и отношений между героями',7);
INSERT INTO public.answer (serial_number,text_answer,fk_question_id) VALUES
	 (3,'Быстрый темп событий и захватывающая интрига',7);


INSERT INTO public.test_result (score_range,text_result,url) VALUES
	 ('[9,11)','Вам подойдет жанр драмы и мелодрамы. Вам важны чувства и эмоции главных героев, и вы хотите погрузиться в их жизненные истории.','https://www.labirint.ru/genres/2556/'),
	 ('[11,13)','Вам подойдет жанр триллера или детектива. Вас привлекают быстрые темпы событий, захватывающая интрига и неожиданная концовка.','https://www.labirint.ru/genres/2498/'),
	 ('[13,15)','Вам подойдет жанр фантастики и фэнтези. Вам интересны необычные и фантастические миры, герои с сверхъестественными способностями и захватывающие сюжеты.','https://www.labirint.ru/genres/2792/'),
	 ('[0,9)','Вам подойдет жанр романтической или психологической драмы. Вы ищете необычные литературные произведения о людях, отношениях и глубине человеческой психологии.','https://www.labirint.ru/genres/2795/');
