BEGIN TRANSACTION;
CREATE TABLE "accounts_employeedocument" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "document_type" varchar(50) NOT NULL, "title" varchar(200) NOT NULL, "description" text NOT NULL, "file" varchar(100) NOT NULL, "file_size" integer unsigned NULL CHECK ("file_size" >= 0), "issue_date" date NULL, "expiry_date" date NULL, "is_active" bool NOT NULL, "notes" text NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "uploaded_by_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "accounts_historicalemployeedocument" ("id" bigint NOT NULL, "document_type" varchar(50) NOT NULL, "title" varchar(200) NOT NULL, "description" text NOT NULL, "file" text NOT NULL, "file_size" integer unsigned NULL CHECK ("file_size" >= 0), "issue_date" date NULL, "expiry_date" date NULL, "is_active" bool NOT NULL, "notes" text NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "history_user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "uploaded_by_id" bigint NULL, "user_id" bigint NULL);
CREATE TABLE "accounts_historicalprofile" ("id" bigint NOT NULL, "date_of_birth" date NULL, "hire_date" date NULL, "education_level" varchar(100) NOT NULL, "specialization" varchar(200) NOT NULL, "work_email" varchar(254) NOT NULL, "work_phone" varchar(20) NOT NULL, "address" text NOT NULL, "language_preference" varchar(10) NOT NULL, "email_notifications" bool NOT NULL, "sms_notifications" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "history_user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NULL, "city" varchar(100) NOT NULL, "contract_end_date" date NULL, "contract_start_date" date NULL, "contract_type" varchar(50) NOT NULL, "emergency_contact_name" varchar(200) NOT NULL, "emergency_contact_phone" varchar(20) NOT NULL, "emergency_contact_relationship" varchar(100) NOT NULL, "graduation_year" integer unsigned NULL CHECK ("graduation_year" >= 0), "health_insurance_number" varchar(100) NOT NULL, "health_insurance_provider" varchar(200) NOT NULL, "marital_status" varchar(20) NOT NULL, "national_id" varchar(50) NOT NULL, "nationality" varchar(100) NOT NULL, "number_of_children" integer unsigned NOT NULL CHECK ("number_of_children" >= 0), "pension_insurance_number" varchar(100) NOT NULL, "personal_email" varchar(254) NOT NULL, "personal_phone" varchar(20) NOT NULL, "place_of_birth" varchar(200) NOT NULL, "postal_code" varchar(20) NOT NULL, "probation_end_date" date NULL, "tax_id" varchar(50) NOT NULL, "termination_date" date NULL, "termination_reason" text NOT NULL, "university" varchar(200) NOT NULL);
INSERT INTO "accounts_historicalprofile" VALUES(1,NULL,NULL,'','','','','','az',1,0,'2025-10-09 06:34:12.114500','2025-10-09 06:34:12.114517',1,'2025-10-09 06:34:12.115956',NULL,'+',NULL,1,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(1,NULL,NULL,'','','','','','az',1,0,'2025-10-09 06:34:12.114500','2025-10-09 06:34:12.122140',2,'2025-10-09 06:34:12.129719',NULL,'~',NULL,1,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(1,NULL,NULL,'','','','','','az',1,0,'2025-10-09 06:34:12.114500','2025-10-09 06:44:53.438552',3,'2025-10-09 06:44:53.447410',NULL,'~',1,1,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(1,NULL,'2025-10-09','','','','','','az',1,0,'2025-10-09 06:34:12.114500','2025-10-09 06:45:59.990441',4,'2025-10-09 06:45:59.992646',NULL,'~',1,1,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(1,NULL,'2025-10-09','','','','','','az',1,0,'2025-10-09 06:34:12.114500','2025-10-09 07:20:04.089868',5,'2025-10-09 07:20:04.090375',NULL,'~',1,1,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(1,NULL,'2025-10-09','','','','','','az',1,0,'2025-10-09 06:34:12.114500','2025-10-09 10:57:25.507700',6,'2025-10-09 10:57:25.508294',NULL,'~',1,1,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(1,NULL,'2025-10-09','','','','','','az',1,0,'2025-10-09 06:34:12.114500','2025-10-09 10:57:59.642825',7,'2025-10-09 10:57:59.643448',NULL,'~',1,1,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(1,NULL,'2025-10-09','','','','','','az',1,0,'2025-10-09 06:34:12.114500','2025-10-09 11:33:49.780157',8,'2025-10-09 11:33:49.788951',NULL,'~',1,1,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(1,NULL,'2025-10-09','Ali','İT','','','','az',1,0,'2025-10-09 06:34:12.114500','2025-10-09 12:08:46.374379',9,'2025-10-09 12:08:46.376672',NULL,'~',1,1,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(1,NULL,'2025-10-09','Ali','İT','muradoffcode@gmail.com','0605536990','Nakhchivan City
Nakhchivan City','az',1,0,'2025-10-09 06:34:12.114500','2025-10-09 12:09:02.262115',10,'2025-10-09 12:09:02.264144',NULL,'~',1,1,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(1,NULL,'2025-10-09','Ali','İT','muradoffcode@gmail.com','0605536990','Nakhchivan City
Nakhchivan City','az',1,0,'2025-10-09 06:34:12.114500','2025-10-09 21:55:38.796433',11,'2025-10-09 21:55:38.807357',NULL,'~',1,1,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(1,NULL,'2025-10-09','Ali','İT','muradoffcode@gmail.com','0605536990','Nakhchivan City
Nakhchivan City','az',1,0,'2025-10-09 06:34:12.114500','2025-10-09 22:13:22.929087',12,'2025-10-09 22:13:22.939415',NULL,'~',1,1,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(1,NULL,'2025-10-09','Ali','İT','muradoffcode@gmail.com','0605536990','Nakhchivan City
Nakhchivan City','az',1,0,'2025-10-09 06:34:12.114500','2025-10-10 09:32:56.914990',13,'2025-10-10 09:32:56.921424',NULL,'~',NULL,1,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(1,NULL,'2025-10-09','Ali','İT','muradoffcode@gmail.com','0605536990','Nakhchivan City
Nakhchivan City','az',1,0,'2025-10-09 06:34:12.114500','2025-10-10 09:32:56.954528',14,'2025-10-10 09:32:56.961262',NULL,'~',1,1,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(2,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:39:44.540839','2025-10-10 15:39:44.540854',15,'2025-10-10 15:39:44.542049',NULL,'+',NULL,2,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(2,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:39:44.540839','2025-10-10 15:39:44.548901',16,'2025-10-10 15:39:44.556214',NULL,'~',NULL,2,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(3,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:39:44.859181','2025-10-10 15:39:44.859196',17,'2025-10-10 15:39:44.860524',NULL,'+',NULL,3,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(3,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:39:44.859181','2025-10-10 15:39:44.866932',18,'2025-10-10 15:39:44.873644',NULL,'~',NULL,3,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(4,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:39:45.173928','2025-10-10 15:39:45.173944',19,'2025-10-10 15:39:45.174946',NULL,'+',NULL,4,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(4,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:39:45.173928','2025-10-10 15:39:45.180596',20,'2025-10-10 15:39:45.186539',NULL,'~',NULL,4,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(5,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:39:45.492251','2025-10-10 15:39:45.492265',21,'2025-10-10 15:39:45.493331',NULL,'+',NULL,5,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(5,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:39:45.492251','2025-10-10 15:39:45.499655',22,'2025-10-10 15:39:45.506445',NULL,'~',NULL,5,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(6,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:39:45.818591','2025-10-10 15:39:45.818606',23,'2025-10-10 15:39:45.819789',NULL,'+',NULL,6,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(6,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:39:45.818591','2025-10-10 15:39:45.825908',24,'2025-10-10 15:39:45.832199',NULL,'~',NULL,6,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(7,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:56.921316','2025-10-10 15:54:56.921330',25,'2025-10-10 15:54:56.922285',NULL,'+',NULL,7,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(7,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:56.921316','2025-10-10 15:54:56.928494',26,'2025-10-10 15:54:56.935374',NULL,'~',NULL,7,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(8,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:57.256400','2025-10-10 15:54:57.256413',27,'2025-10-10 15:54:57.257459',NULL,'+',NULL,8,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(8,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:57.256400','2025-10-10 15:54:57.263922',28,'2025-10-10 15:54:57.270510',NULL,'~',NULL,8,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(9,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:57.577120','2025-10-10 15:54:57.577133',29,'2025-10-10 15:54:57.578048',NULL,'+',NULL,9,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(9,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:57.577120','2025-10-10 15:54:57.583556',30,'2025-10-10 15:54:57.589991',NULL,'~',NULL,9,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(10,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:57.909668','2025-10-10 15:54:57.909682',31,'2025-10-10 15:54:57.910584',NULL,'+',NULL,10,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(10,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:57.909668','2025-10-10 15:54:57.916639',32,'2025-10-10 15:54:57.922676',NULL,'~',NULL,10,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(11,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:58.243019','2025-10-10 15:54:58.243034',33,'2025-10-10 15:54:58.244073',NULL,'+',NULL,11,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(11,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:58.243019','2025-10-10 15:54:58.250693',34,'2025-10-10 15:54:58.257131',NULL,'~',NULL,11,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(12,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:58.575053','2025-10-10 15:54:58.575068',35,'2025-10-10 15:54:58.576162',NULL,'+',NULL,12,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(12,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:58.575053','2025-10-10 15:54:58.582337',36,'2025-10-10 15:54:58.588568',NULL,'~',NULL,12,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(13,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:58.902725','2025-10-10 15:54:58.902739',37,'2025-10-10 15:54:58.903690',NULL,'+',NULL,13,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(13,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:58.902725','2025-10-10 15:54:58.909633',38,'2025-10-10 15:54:58.916559',NULL,'~',NULL,13,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(14,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:59.242331','2025-10-10 15:54:59.242347',39,'2025-10-10 15:54:59.243398',NULL,'+',NULL,14,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(14,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:59.242331','2025-10-10 15:54:59.250173',40,'2025-10-10 15:54:59.256365',NULL,'~',NULL,14,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(15,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:59.581247','2025-10-10 15:54:59.581263',41,'2025-10-10 15:54:59.582296',NULL,'+',NULL,15,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(15,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:59.581247','2025-10-10 15:54:59.588261',42,'2025-10-10 15:54:59.594425',NULL,'~',NULL,15,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(16,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:59.928557','2025-10-10 15:54:59.928573',43,'2025-10-10 15:54:59.929625',NULL,'+',NULL,16,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(16,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:59.928557','2025-10-10 15:54:59.935824',44,'2025-10-10 15:54:59.942596',NULL,'~',NULL,16,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(17,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:55:00.251437','2025-10-10 15:55:00.251452',45,'2025-10-10 15:55:00.253230',NULL,'+',NULL,17,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(17,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:55:00.251437','2025-10-10 15:55:00.259138',46,'2025-10-10 15:55:00.267324',NULL,'~',NULL,17,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(18,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:55:00.587340','2025-10-10 15:55:00.587354',47,'2025-10-10 15:55:00.588333',NULL,'+',NULL,18,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(18,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:55:00.587340','2025-10-10 15:55:00.594321',48,'2025-10-10 15:55:00.600286',NULL,'~',NULL,18,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(19,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:55:00.916312','2025-10-10 15:55:00.916328',49,'2025-10-10 15:55:00.917561',NULL,'+',NULL,19,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(19,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:55:00.916312','2025-10-10 15:55:00.924760',50,'2025-10-10 15:55:00.931155',NULL,'~',NULL,19,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(7,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:56.921316','2025-10-10 15:55:00.951732',51,'2025-10-10 15:55:00.958321',NULL,'~',NULL,7,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(8,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:57.256400','2025-10-10 15:55:00.979437',52,'2025-10-10 15:55:00.986344',NULL,'~',NULL,8,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(9,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:57.577120','2025-10-10 15:55:01.008573',53,'2025-10-10 15:55:01.014810',NULL,'~',NULL,9,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(10,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:57.909668','2025-10-10 15:55:01.038414',54,'2025-10-10 15:55:01.045458',NULL,'~',NULL,10,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(11,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:58.243019','2025-10-10 15:55:01.067599',55,'2025-10-10 15:55:01.074776',NULL,'~',NULL,11,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(12,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:58.575053','2025-10-10 15:55:01.095322',56,'2025-10-10 15:55:01.102078',NULL,'~',NULL,12,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(13,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:58.902725','2025-10-10 15:55:01.124188',57,'2025-10-10 15:55:01.130641',NULL,'~',NULL,13,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(14,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:59.242331','2025-10-10 15:55:01.153867',58,'2025-10-10 15:55:01.160732',NULL,'~',NULL,14,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(15,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:59.581247','2025-10-10 15:55:01.185358',59,'2025-10-10 15:55:01.192242',NULL,'~',NULL,15,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(16,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:59.928557','2025-10-10 15:55:01.214344',60,'2025-10-10 15:55:01.221821',NULL,'~',NULL,16,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(17,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:55:00.251437','2025-10-10 15:55:01.243859',61,'2025-10-10 15:55:01.252295',NULL,'~',NULL,17,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(18,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:55:00.587340','2025-10-10 15:55:01.277550',62,'2025-10-10 15:55:01.284632',NULL,'~',NULL,18,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(19,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:55:00.916312','2025-10-10 15:55:01.307060',63,'2025-10-10 15:55:01.314660',NULL,'~',NULL,19,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(7,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:56.921316','2025-10-10 15:57:26.734702',64,'2025-10-10 15:57:26.741905',NULL,'~',NULL,7,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(8,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:57.256400','2025-10-10 15:57:26.766614',65,'2025-10-10 15:57:26.773074',NULL,'~',NULL,8,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(9,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:57.577120','2025-10-10 15:57:26.795382',66,'2025-10-10 15:57:26.801609',NULL,'~',NULL,9,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(10,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:57.909668','2025-10-10 15:57:26.824641',67,'2025-10-10 15:57:26.830961',NULL,'~',NULL,10,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(11,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:58.243019','2025-10-10 15:57:26.855451',68,'2025-10-10 15:57:26.861954',NULL,'~',NULL,11,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(12,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:58.575053','2025-10-10 15:57:26.885898',69,'2025-10-10 15:57:26.892188',NULL,'~',NULL,12,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(13,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:58.902725','2025-10-10 15:57:26.914955',70,'2025-10-10 15:57:26.921333',NULL,'~',NULL,13,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(14,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:59.242331','2025-10-10 15:57:26.946135',71,'2025-10-10 15:57:26.952226',NULL,'~',NULL,14,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(15,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:59.581247','2025-10-10 15:57:26.975625',72,'2025-10-10 15:57:26.982392',NULL,'~',NULL,15,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(16,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:59.928557','2025-10-10 15:57:27.005168',73,'2025-10-10 15:57:27.011818',NULL,'~',NULL,16,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(17,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:55:00.251437','2025-10-10 15:57:27.035863',74,'2025-10-10 15:57:27.042207',NULL,'~',NULL,17,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(18,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:55:00.587340','2025-10-10 15:57:27.065415',75,'2025-10-10 15:57:27.071603',NULL,'~',NULL,18,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(19,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:55:00.916312','2025-10-10 15:57:27.094367',76,'2025-10-10 15:57:27.100723',NULL,'~',NULL,19,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(1,NULL,'2025-10-09','Ali','İT','muradoffcode@gmail.com','0605536990','Nakhchivan City
Nakhchivan City','az',1,0,'2025-10-09 06:34:12.114500','2025-10-10 20:34:09.695426',77,'2025-10-10 20:34:09.701534',NULL,'~',1,1,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(19,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:55:00.916312','2025-10-10 20:40:15.826661',78,'2025-10-10 20:40:15.827230',NULL,'~',1,19,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(1,NULL,'2025-10-09','Ali','İT','muradoffcode@gmail.com','0605536990','Nakhchivan City
Nakhchivan City','az',1,0,'2025-10-09 06:34:12.114500','2025-10-10 20:43:12.016961',79,'2025-10-10 20:43:12.017390',NULL,'~',1,1,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(1,NULL,'2025-10-09','Ali','İT','muradoffcode@gmail.com','0605536990','Nakhchivan City
Nakhchivan City','az',1,0,'2025-10-09 06:34:12.114500','2025-10-10 20:44:02.572421',80,'2025-10-10 20:44:02.572694',NULL,'~',1,1,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(1,NULL,'2025-10-09','Ali','İT','muradoffcode@gmail.com','0605536990','Nakhchivan City
Nakhchivan City','az',1,0,'2025-10-09 06:34:12.114500','2025-10-10 20:44:22.167897',81,'2025-10-10 20:44:22.168221',NULL,'~',1,1,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(1,NULL,'2025-10-09','Ali','İT','muradoffcode@gmail.com','0605536990','Nakhchivan City
Nakhchivan City','az',1,0,'2025-10-09 06:34:12.114500','2025-10-10 20:55:10.458224',82,'2025-10-10 20:55:10.458779',NULL,'~',1,1,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(15,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:59.581247','2025-10-10 21:07:55.720065',83,'2025-10-10 21:07:55.728997',NULL,'~',1,15,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(15,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:59.581247','2025-10-10 21:08:34.595393',84,'2025-10-10 21:08:34.596081',NULL,'~',1,15,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(15,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:59.581247','2025-10-10 21:09:20.114092',85,'2025-10-10 21:09:20.114640',NULL,'~',1,15,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(15,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:59.581247','2025-10-10 21:09:40.924841',86,'2025-10-10 21:09:40.936730',NULL,'~',15,15,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(1,NULL,'2025-10-09','Ali','İT','muradoffcode@gmail.com','0605536990','Nakhchivan City
Nakhchivan City','az',1,0,'2025-10-09 06:34:12.114500','2025-10-10 22:47:07.475377',87,'2025-10-10 22:47:07.486395',NULL,'~',1,1,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(20,NULL,NULL,'','','','','','az',1,0,'2025-10-11 19:13:57.033655','2025-10-11 19:13:57.033680',88,'2025-10-11 19:13:57.038707',NULL,'+',NULL,20,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(20,NULL,NULL,'','','','','','az',1,0,'2025-10-11 19:13:57.033655','2025-10-11 19:13:57.050775',89,'2025-10-11 19:13:57.072949',NULL,'~',NULL,20,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(1,NULL,'2025-10-09','Ali','İT','muradoffcode@gmail.com','0605536990','Nakhchivan City
Nakhchivan City','az',1,0,'2025-10-09 06:34:12.114500','2025-10-14 22:16:27.485174',90,'2025-10-14 22:16:27.487792',NULL,'~',1,1,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(1,NULL,'2025-10-09','Ali','İT','muradoffcode@gmail.com','0605536990','Nakhchivan City
Nakhchivan City','az',1,0,'2025-10-09 06:34:12.114500','2025-10-14 22:16:47.812790',91,'2025-10-14 22:16:47.813268',NULL,'~',1,1,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(20,NULL,NULL,'','','','','','az',1,0,'2025-10-11 19:13:57.033655','2025-10-14 22:17:55.674264',92,'2025-10-14 22:17:55.674940',NULL,'~',1,20,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(21,NULL,NULL,'','','','','','az',1,0,'2025-10-15 07:47:47.375179','2025-10-15 07:47:47.375200',93,'2025-10-15 07:47:47.375579',NULL,'+',NULL,21,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(21,NULL,NULL,'','','','','','az',1,0,'2025-10-15 07:47:47.375179','2025-10-15 07:47:47.377434',94,'2025-10-15 07:47:47.377882',NULL,'~',NULL,21,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(21,NULL,NULL,'','','','','','az',1,0,'2025-10-15 07:47:47.375179','2025-10-15 07:47:47.775881',95,'2025-10-15 07:47:47.784614',NULL,'~',NULL,21,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(22,NULL,NULL,'','','','','','az',1,0,'2025-10-15 07:47:47.825362','2025-10-15 07:47:47.825379',96,'2025-10-15 07:47:47.825603',NULL,'+',NULL,22,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(22,NULL,NULL,'','','','','','az',1,0,'2025-10-15 07:47:47.825362','2025-10-15 07:47:47.826747',97,'2025-10-15 07:47:47.827344',NULL,'~',NULL,22,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(22,NULL,NULL,'','','','','','az',1,0,'2025-10-15 07:47:47.825362','2025-10-15 07:47:48.198514',98,'2025-10-15 07:47:48.205289',NULL,'~',NULL,22,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(23,NULL,NULL,'','','','','','az',1,0,'2025-10-15 07:47:48.220389','2025-10-15 07:47:48.220407',99,'2025-10-15 07:47:48.220743',NULL,'+',NULL,23,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(23,NULL,NULL,'','','','','','az',1,0,'2025-10-15 07:47:48.220389','2025-10-15 07:47:48.222411',100,'2025-10-15 07:47:48.222751',NULL,'~',NULL,23,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(23,NULL,NULL,'','','','','','az',1,0,'2025-10-15 07:47:48.220389','2025-10-15 07:47:48.611812',101,'2025-10-15 07:47:48.622593',NULL,'~',NULL,23,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(24,NULL,NULL,'','','','','','az',1,0,'2025-10-15 07:58:54.016903','2025-10-15 07:58:54.016918',102,'2025-10-15 07:58:54.018065',NULL,'+',NULL,24,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(24,NULL,NULL,'','','','','','az',1,0,'2025-10-15 07:58:54.016903','2025-10-15 07:58:54.024131',103,'2025-10-15 07:58:54.030474',NULL,'~',NULL,24,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(24,NULL,NULL,'','','','','','az',1,0,'2025-10-15 07:58:54.016903','2025-10-15 07:58:54.052435',104,'2025-10-15 07:58:54.059010',NULL,'~',NULL,24,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(25,NULL,NULL,'','','','','','az',1,0,'2025-10-15 07:58:54.364673','2025-10-15 07:58:54.364687',105,'2025-10-15 07:58:54.366070',NULL,'+',NULL,25,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(25,NULL,NULL,'','','','','','az',1,0,'2025-10-15 07:58:54.364673','2025-10-15 07:58:54.372161',106,'2025-10-15 07:58:54.378342',NULL,'~',NULL,25,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(25,NULL,NULL,'','','','','','az',1,0,'2025-10-15 07:58:54.364673','2025-10-15 07:58:54.398228',107,'2025-10-15 07:58:54.404270',NULL,'~',NULL,25,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(26,NULL,NULL,'','','','','','az',1,0,'2025-10-15 07:58:54.716263','2025-10-15 07:58:54.716279',108,'2025-10-15 07:58:54.719364',NULL,'+',NULL,26,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(26,NULL,NULL,'','','','','','az',1,0,'2025-10-15 07:58:54.716263','2025-10-15 07:58:54.725965',109,'2025-10-15 07:58:54.732711',NULL,'~',NULL,26,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(26,NULL,NULL,'','','','','','az',1,0,'2025-10-15 07:58:54.716263','2025-10-15 07:58:54.755624',110,'2025-10-15 07:58:54.762243',NULL,'~',NULL,26,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(27,NULL,NULL,'','','','','','az',1,0,'2025-10-15 07:58:55.088957','2025-10-15 07:58:55.088975',111,'2025-10-15 07:58:55.090191',NULL,'+',NULL,27,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(27,NULL,NULL,'','','','','','az',1,0,'2025-10-15 07:58:55.088957','2025-10-15 07:58:55.096295',112,'2025-10-15 07:58:55.102877',NULL,'~',NULL,27,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(27,NULL,NULL,'','','','','','az',1,0,'2025-10-15 07:58:55.088957','2025-10-15 07:58:55.126553',113,'2025-10-15 07:58:55.133478',NULL,'~',NULL,27,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(28,NULL,NULL,'','','','','','az',1,0,'2025-10-15 07:58:55.440704','2025-10-15 07:58:55.440719',114,'2025-10-15 07:58:55.441720',NULL,'+',NULL,28,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(28,NULL,NULL,'','','','','','az',1,0,'2025-10-15 07:58:55.440704','2025-10-15 07:58:55.447306',115,'2025-10-15 07:58:55.453829',NULL,'~',NULL,28,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(29,NULL,NULL,'','','','','','az',1,0,'2025-10-15 07:58:55.760786','2025-10-15 07:58:55.760801',116,'2025-10-15 07:58:55.762008',NULL,'+',NULL,29,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(29,NULL,NULL,'','','','','','az',1,0,'2025-10-15 07:58:55.760786','2025-10-15 07:58:55.768192',117,'2025-10-15 07:58:55.774528',NULL,'~',NULL,29,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(29,NULL,NULL,'','','','','','az',1,0,'2025-10-15 07:58:55.760786','2025-10-15 07:58:55.795573',118,'2025-10-15 07:58:55.801498',NULL,'~',NULL,29,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(15,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:59.581247','2025-10-15 11:43:22.046910',119,'2025-10-15 11:43:22.047565',NULL,'~',1,15,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(1,NULL,'2025-10-09','Ali','İT','muradoffcode@gmail.com','0605536990','Nakhchivan City
Nakhchivan City','az',1,0,'2025-10-09 06:34:12.114500','2025-10-15 13:49:19.682957',120,'2025-10-15 13:49:19.691150',NULL,'~',1,1,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(16,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:59.928557','2025-10-16 00:52:15.932866',121,'2025-10-16 00:52:15.933418',NULL,'~',1,16,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(7,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:56.921316','2025-10-16 13:24:16.602508',122,'2025-10-16 13:24:16.609508',NULL,'~',NULL,7,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(8,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:57.256400','2025-10-16 13:24:16.632538',123,'2025-10-16 13:24:16.638983',NULL,'~',NULL,8,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(9,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:57.577120','2025-10-16 13:24:16.661608',124,'2025-10-16 13:24:16.668813',NULL,'~',NULL,9,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(10,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:57.909668','2025-10-16 13:24:16.693553',125,'2025-10-16 13:24:16.700051',NULL,'~',NULL,10,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(11,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:58.243019','2025-10-16 13:24:16.723380',126,'2025-10-16 13:24:16.729762',NULL,'~',NULL,11,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(12,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:58.575053','2025-10-16 13:24:16.752496',127,'2025-10-16 13:24:16.758554',NULL,'~',NULL,12,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(13,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:58.902725','2025-10-16 13:24:16.781324',128,'2025-10-16 13:24:16.787651',NULL,'~',NULL,13,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(14,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:59.242331','2025-10-16 13:24:16.810181',129,'2025-10-16 13:24:16.816744',NULL,'~',NULL,14,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(15,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:59.581247','2025-10-16 13:24:16.841994',130,'2025-10-16 13:24:16.849106',NULL,'~',NULL,15,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(16,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:59.928557','2025-10-16 13:24:16.872904',131,'2025-10-16 13:24:16.880062',NULL,'~',NULL,16,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(17,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:55:00.251437','2025-10-16 13:24:16.907621',132,'2025-10-16 13:24:16.913983',NULL,'~',NULL,17,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(18,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:55:00.587340','2025-10-16 13:24:16.938728',133,'2025-10-16 13:24:16.945005',NULL,'~',NULL,18,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(19,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:55:00.916312','2025-10-16 13:24:16.968275',134,'2025-10-16 13:24:16.974967',NULL,'~',NULL,19,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(7,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:56.921316','2025-10-16 13:40:16.464519',135,'2025-10-16 13:40:16.471456',NULL,'~',NULL,7,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(8,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:57.256400','2025-10-16 13:40:16.495630',136,'2025-10-16 13:40:16.503154',NULL,'~',NULL,8,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(9,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:57.577120','2025-10-16 13:40:16.527240',137,'2025-10-16 13:40:16.534093',NULL,'~',NULL,9,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(10,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:57.909668','2025-10-16 13:40:16.559966',138,'2025-10-16 13:40:16.566643',NULL,'~',NULL,10,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(11,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:58.243019','2025-10-16 13:40:16.591303',139,'2025-10-16 13:40:16.598311',NULL,'~',NULL,11,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(12,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:58.575053','2025-10-16 13:40:16.623247',140,'2025-10-16 13:40:16.630089',NULL,'~',NULL,12,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(13,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:58.902725','2025-10-16 13:40:16.654196',141,'2025-10-16 13:40:16.660718',NULL,'~',NULL,13,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(14,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:59.242331','2025-10-16 13:40:16.686641',142,'2025-10-16 13:40:16.693345',NULL,'~',NULL,14,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(15,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:59.581247','2025-10-16 13:40:16.718474',143,'2025-10-16 13:40:16.725955',NULL,'~',NULL,15,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(16,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:59.928557','2025-10-16 13:40:16.751714',144,'2025-10-16 13:40:16.759851',NULL,'~',NULL,16,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(17,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:55:00.251437','2025-10-16 13:40:16.785972',145,'2025-10-16 13:40:16.792891',NULL,'~',NULL,17,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(18,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:55:00.587340','2025-10-16 13:40:16.819462',146,'2025-10-16 13:40:16.826131',NULL,'~',NULL,18,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(19,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:55:00.916312','2025-10-16 13:40:16.852416',147,'2025-10-16 13:40:16.859280',NULL,'~',NULL,19,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(30,NULL,NULL,'','','','','','az',1,0,'2025-10-16 16:35:53.360471','2025-10-16 16:35:53.360514',148,'2025-10-16 16:35:53.363623',NULL,'+',NULL,30,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(30,NULL,NULL,'','','','','','az',1,0,'2025-10-16 16:35:53.360471','2025-10-16 16:35:53.375224',149,'2025-10-16 16:35:53.386363',NULL,'~',NULL,30,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(30,'2025-10-01',NULL,'','','','','','az',1,0,'2025-10-16 16:35:53.360471','2025-10-16 16:35:53.401139',150,'2025-10-16 16:35:53.411254',NULL,'~',NULL,30,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(30,'2025-10-01',NULL,'','','','','','az',1,0,'2025-10-16 16:35:53.360471','2025-10-16 16:36:09.701906',151,'2025-10-16 16:36:09.713154',NULL,'~',30,30,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(1,NULL,'2025-10-09','Ali','İT','muradoffcode@gmail.com','0605536990','Nakhchivan City
Nakhchivan City','az',1,0,'2025-10-09 06:34:12.114500','2025-10-16 16:39:10.686921',152,'2025-10-16 16:39:10.696340',NULL,'~',1,1,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(1,NULL,'2025-10-09','Ali','İT','muradoffcode@gmail.com','0605536990','Nakhchivan City
Nakhchivan City','az',1,0,'2025-10-09 06:34:12.114500','2025-10-16 18:52:11.454762',153,'2025-10-16 18:52:11.461560',NULL,'~',1,1,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(1,NULL,'2025-10-09','','İT','muradoffcode@gmail.com','0605536990','Nakhchivan City
Nakhchivan City','az',1,0,'2025-10-09 06:34:12.114500','2025-10-16 21:21:23.147270',154,'2025-10-16 21:21:23.148171',NULL,'~',1,1,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(1,NULL,'2025-10-09','','İT','muradoffcode@gmail.com','0605536990','Nakhchivan City
Nakhchivan City','az',1,0,'2025-10-09 06:34:12.114500','2025-10-16 21:21:23.152665',155,'2025-10-16 21:21:23.153330',NULL,'~',1,1,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(31,NULL,NULL,'','','','','','az',1,0,'2025-10-17 17:11:47.864018','2025-10-17 17:11:47.864095',156,'2025-10-17 17:11:47.864532',NULL,'+',NULL,31,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(31,NULL,NULL,'','','','','','az',1,0,'2025-10-17 17:11:47.864018','2025-10-17 17:11:47.866258',157,'2025-10-17 17:11:47.866660',NULL,'~',NULL,31,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(31,NULL,NULL,'','','','','','az',1,0,'2025-10-17 17:11:47.864018','2025-10-17 17:11:48.201047',158,'2025-10-17 17:11:48.207613',NULL,'~',NULL,31,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(32,NULL,NULL,'','','','','','az',1,0,'2025-10-17 18:51:01.922460','2025-10-17 18:51:01.922474',159,'2025-10-17 18:51:01.924147',NULL,'+',NULL,32,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(32,NULL,NULL,'','','','','','az',1,0,'2025-10-17 18:51:01.922460','2025-10-17 18:51:01.931072',160,'2025-10-17 18:51:01.937925',NULL,'~',NULL,32,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(32,NULL,NULL,'','','','','','az',1,0,'2025-10-17 18:51:01.922460','2025-10-17 18:51:01.977780',161,'2025-10-17 18:51:01.984527',NULL,'~',NULL,32,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(33,NULL,NULL,'','','','','','az',1,0,'2025-10-17 18:51:02.299230','2025-10-17 18:51:02.299246',162,'2025-10-17 18:51:02.301148',NULL,'+',NULL,33,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(33,NULL,NULL,'','','','','','az',1,0,'2025-10-17 18:51:02.299230','2025-10-17 18:51:02.309800',163,'2025-10-17 18:51:02.316933',NULL,'~',NULL,33,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(33,NULL,NULL,'','','','','','az',1,0,'2025-10-17 18:51:02.299230','2025-10-17 18:51:02.341412',164,'2025-10-17 18:51:02.348634',NULL,'~',NULL,33,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(32,NULL,NULL,'','','','','','az',1,0,'2025-10-17 18:51:01.922460','2025-10-17 18:51:02.709496',165,'2025-10-17 18:51:02.716123',NULL,'~',NULL,32,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(34,NULL,NULL,'','','','','','az',1,0,'2025-10-17 19:11:19.118121','2025-10-17 19:11:19.118144',166,'2025-10-17 19:11:19.120997',NULL,'+',NULL,34,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(34,NULL,NULL,'','','','','','az',1,0,'2025-10-17 19:11:19.118121','2025-10-17 19:11:19.131170',167,'2025-10-17 19:11:19.146239',NULL,'~',NULL,34,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(34,NULL,NULL,'','','','','','az',1,0,'2025-10-17 19:11:19.118121','2025-10-17 19:11:19.228894',168,'2025-10-17 19:11:19.257838',NULL,'~',NULL,34,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_historicalprofile" VALUES(34,NULL,NULL,'','','','','','az',1,0,'2025-10-17 19:11:19.118121','2025-10-17 19:11:19.980383',169,'2025-10-17 19:11:19.995503',NULL,'~',NULL,34,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
CREATE TABLE "accounts_historicalrole" ("id" bigint NOT NULL, "name" varchar(50) NOT NULL, "display_name" varchar(100) NOT NULL, "description" text NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "history_user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "accounts_historicalrole" VALUES(1,'superadmin','baş admin','','2025-10-09 06:46:54.247720','2025-10-09 06:46:54.247743',1,'2025-10-09 06:46:54.249424',NULL,'+',1);
INSERT INTO "accounts_historicalrole" VALUES(1,'superadmin','baş admin','','2025-10-09 06:46:54.247720','2025-10-10 20:48:20.504550',2,'2025-10-10 20:48:20.505876',NULL,'~',1);
INSERT INTO "accounts_historicalrole" VALUES(2,'employee','İşçi','','2025-10-10 21:06:01.868478','2025-10-10 21:06:01.868551',3,'2025-10-10 21:06:01.871370',NULL,'+',1);
INSERT INTO "accounts_historicalrole" VALUES(3,'admin','Admin','','2025-10-10 21:06:28.207986','2025-10-10 21:06:28.208009',4,'2025-10-10 21:06:28.209831',NULL,'+',1);
INSERT INTO "accounts_historicalrole" VALUES(4,'manager','Rəhbər','','2025-10-10 21:07:05.999881','2025-10-10 21:07:05.999905',5,'2025-10-10 21:07:06.001909',NULL,'+',1);
CREATE TABLE "accounts_historicaluser" ("id" bigint NOT NULL, "password" varchar(128) NOT NULL, "is_superuser" bool NOT NULL, "username" varchar(150) NOT NULL, "first_name" varchar(150) NOT NULL, "last_name" varchar(150) NOT NULL, "email" varchar(254) NOT NULL, "is_staff" bool NOT NULL, "role" varchar(20) NOT NULL, "position" varchar(100) NOT NULL, "middle_name" varchar(150) NOT NULL, "phone_number" varchar(20) NOT NULL, "employee_id" varchar(50) NULL, "profile_picture" text NULL, "bio" text NOT NULL, "is_active" bool NOT NULL, "date_joined" datetime NOT NULL, "last_login" datetime NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "department_id" bigint NULL, "history_user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "supervisor_id" bigint NULL);
INSERT INTO "accounts_historicaluser" VALUES(1,'pbkdf2_sha256$600000$eEw98pR4WY7KKg11dgJeeb$JVc5HtsjwtusxtK8rhWK+CO5DK1+4KUV9O2tQKmPyW8=',1,'admin','Admin','User','admin@q360.gov.az',1,'employee','','','',NULL,'','',1,'2025-10-09 06:34:12.095047',NULL,1,'2025-10-09 06:34:12.105197',NULL,'+',NULL,NULL,NULL);
INSERT INTO "accounts_historicaluser" VALUES(1,'pbkdf2_sha256$600000$eEw98pR4WY7KKg11dgJeeb$JVc5HtsjwtusxtK8rhWK+CO5DK1+4KUV9O2tQKmPyW8=',1,'admin','Admin','User','admin@q360.gov.az',1,'employee','','','',NULL,'','',1,'2025-10-09 06:34:12.095047','2025-10-09 06:44:53.423786',2,'2025-10-09 06:44:53.430652',NULL,'~',NULL,1,NULL);
INSERT INTO "accounts_historicaluser" VALUES(1,'pbkdf2_sha256$600000$eEw98pR4WY7KKg11dgJeeb$JVc5HtsjwtusxtK8rhWK+CO5DK1+4KUV9O2tQKmPyW8=',1,'admin','Admin','User','admin@q360.gov.az',1,'superadmin','müdür','','0605536990','0001','','Tahmaz',1,'2025-10-09 06:34:12.095047','2025-10-09 06:44:53.423786',3,'2025-10-09 07:20:04.088622',NULL,'~',NULL,1,1);
INSERT INTO "accounts_historicaluser" VALUES(1,'pbkdf2_sha256$600000$eEw98pR4WY7KKg11dgJeeb$JVc5HtsjwtusxtK8rhWK+CO5DK1+4KUV9O2tQKmPyW8=',1,'Tahmaz','Admin','User','admin@q360.gov.az',1,'superadmin','müdür','','0605536990','0001','','Tahmaz',1,'2025-10-09 06:34:12.095047','2025-10-09 06:44:53.423786',4,'2025-10-09 10:57:25.506000',NULL,'~',NULL,1,1);
INSERT INTO "accounts_historicaluser" VALUES(1,'pbkdf2_sha256$600000$eEw98pR4WY7KKg11dgJeeb$JVc5HtsjwtusxtK8rhWK+CO5DK1+4KUV9O2tQKmPyW8=',1,'Tahmaz','Tahmaz','Muradov','admin@q360.gov.az',1,'superadmin','müdür','Seyran','0605536990','0001','','Tahmaz',1,'2025-10-09 06:34:12.095047','2025-10-09 06:44:53.423786',5,'2025-10-09 10:57:59.641232',NULL,'~',NULL,1,1);
INSERT INTO "accounts_historicaluser" VALUES(1,'pbkdf2_sha256$600000$eEw98pR4WY7KKg11dgJeeb$JVc5HtsjwtusxtK8rhWK+CO5DK1+4KUV9O2tQKmPyW8=',1,'Tahmaz','Tahmaz','Muradov','admin@q360.gov.az',1,'superadmin','müdür','Seyran','0605536990','0001','','Tahmaz',1,'2025-10-09 06:34:12.095047','2025-10-09 11:33:49.756655',6,'2025-10-09 11:33:49.765958',NULL,'~',NULL,1,1);
INSERT INTO "accounts_historicaluser" VALUES(1,'pbkdf2_sha256$600000$eEw98pR4WY7KKg11dgJeeb$JVc5HtsjwtusxtK8rhWK+CO5DK1+4KUV9O2tQKmPyW8=',1,'Tahmaz','Tahmaz','Muradov','admin@q360.gov.az',1,'superadmin','müdür','Seyran','0605536990','0001','','Tahmaz',1,'2025-10-09 06:34:12.095047','2025-10-09 21:55:38.770148',7,'2025-10-09 21:55:38.779849',NULL,'~',NULL,1,1);
INSERT INTO "accounts_historicaluser" VALUES(1,'pbkdf2_sha256$600000$eEw98pR4WY7KKg11dgJeeb$JVc5HtsjwtusxtK8rhWK+CO5DK1+4KUV9O2tQKmPyW8=',1,'Tahmaz','Tahmaz','Muradov','admin@q360.gov.az',1,'superadmin','müdür','Seyran','0605536990','0001','','Tahmaz',1,'2025-10-09 06:34:12.095047','2025-10-09 22:13:22.902242',8,'2025-10-09 22:13:22.913062',NULL,'~',NULL,1,1);
INSERT INTO "accounts_historicaluser" VALUES(1,'pbkdf2_sha256$870000$55Rtqbij2pb2iQmfZSlwaw$f4jkRvmNoWoMMg7opXGVH2yc58BqLEoyyHI98r6NkoA=',1,'Tahmaz','Tahmaz','Muradov','admin@q360.gov.az',1,'superadmin','müdür','Seyran','0605536990','0001','','Tahmaz',1,'2025-10-09 06:34:12.095047','2025-10-09 22:13:22.902242',9,'2025-10-10 09:32:56.906256',NULL,'~',NULL,NULL,1);
INSERT INTO "accounts_historicaluser" VALUES(1,'pbkdf2_sha256$870000$55Rtqbij2pb2iQmfZSlwaw$f4jkRvmNoWoMMg7opXGVH2yc58BqLEoyyHI98r6NkoA=',1,'Tahmaz','Tahmaz','Muradov','admin@q360.gov.az',1,'superadmin','müdür','Seyran','0605536990','0001','','Tahmaz',1,'2025-10-09 06:34:12.095047','2025-10-10 09:32:56.940166',10,'2025-10-10 09:32:56.947531',NULL,'~',NULL,1,1);
INSERT INTO "accounts_historicaluser" VALUES(2,'pbkdf2_sha256$870000$56YneD4tq44pKaBGs9tfLp$ua2goaHR4AS7kQskyxiyEAKQRHVX4TfMyeXbO2YIOS0=',1,'admin','Admin','İstifadəçi','admin@q360.az',1,'superadmin','Sistem Administratoru','','',NULL,'','',1,'2025-10-10 15:39:44.521098',NULL,11,'2025-10-10 15:39:44.531673',NULL,'+',1,NULL,NULL);
INSERT INTO "accounts_historicaluser" VALUES(3,'pbkdf2_sha256$870000$SYAipiqJ4GXohz0lZq573L$IKkDxmO1ow3Viq4582OD+SDhVHjdGlxNUepdHnkflEI=',0,'manager','Rəşad','Məmmədov','manager@q360.az',0,'manager','HR Meneceri','','',NULL,'','',1,'2025-10-10 15:39:44.841519',NULL,12,'2025-10-10 15:39:44.850447',NULL,'+',1,NULL,NULL);
INSERT INTO "accounts_historicaluser" VALUES(4,'pbkdf2_sha256$870000$4qVdVfnUOjhFLTKEAStQWw$I9U3TFY0vJuXuXh7TVpeOmAhQf3LjLMym6wb+ZjQj3w=',0,'employee1','Aynur','Əliyeva','employee1@q360.az',0,'employee','HR Mütəxəssisi','','',NULL,'','',1,'2025-10-10 15:39:45.156561',NULL,13,'2025-10-10 15:39:45.165665',NULL,'+',1,NULL,NULL);
INSERT INTO "accounts_historicaluser" VALUES(5,'pbkdf2_sha256$870000$d8iMGg1EBWF9UeGsmIRwOk$z4vVTHZB+eBVDICB30FGOe3rZYPsyjjRe86jf1P+NJw=',0,'employee2','Elçin','Həsənov','employee2@q360.az',0,'employee','Proqramçı','','',NULL,'','',1,'2025-10-10 15:39:45.476098',NULL,14,'2025-10-10 15:39:45.483898',NULL,'+',2,NULL,NULL);
INSERT INTO "accounts_historicaluser" VALUES(6,'pbkdf2_sha256$870000$3zckyIz3mYPEC9lzie5Fct$Ho2+K5jmSa++5mc0CMy5oYewkULhk0O81dNn5lMr2i4=',0,'employee3','Günel','İsmayılova','employee3@q360.az',0,'employee','Sistem Analitiki','','',NULL,'','',1,'2025-10-10 15:39:45.802946',NULL,15,'2025-10-10 15:39:45.810114',NULL,'+',2,NULL,NULL);
INSERT INTO "accounts_historicaluser" VALUES(7,'pbkdf2_sha256$870000$8JpYXlPFZgePktgqH0vtAO$MeSwek6Npsj30YxqL2plcKTpmA8ePuUWjo4osP26lIA=',0,'rashad','Rəşad','Məmmədov','rashad@q360.az',0,'manager','HR Meneceri','','',NULL,'','',1,'2025-10-10 15:54:56.903567',NULL,16,'2025-10-10 15:54:56.913097',NULL,'+',1,NULL,NULL);
INSERT INTO "accounts_historicaluser" VALUES(8,'pbkdf2_sha256$870000$T0w0YxwXnhO7W44xdwNiAn$2dnZEKfcWBiE8CpDki/cnCi/CJvPdzd4zM23oAbObyU=',0,'elvin','Elvin','Quliyev','elvin@q360.az',0,'manager','IT Meneceri','','',NULL,'','',1,'2025-10-10 15:54:57.238382',NULL,17,'2025-10-10 15:54:57.248032',NULL,'+',2,NULL,NULL);
INSERT INTO "accounts_historicaluser" VALUES(9,'pbkdf2_sha256$870000$SiqYfQdaFK7M6QfmgScyF8$vXbrwzzSk3HI9J/Z+jVsPhY5zooxzZY8/Tb8MqQayuA=',0,'leyla','Leyla','Həsənova','leyla@q360.az',0,'manager','Maliyyə Meneceri','','',NULL,'','',1,'2025-10-10 15:54:57.561516',NULL,18,'2025-10-10 15:54:57.569442',NULL,'+',3,NULL,NULL);
INSERT INTO "accounts_historicaluser" VALUES(10,'pbkdf2_sha256$870000$LowPGlRzHG6dB7Q07nnzgP$rFaWQQQKLuI7zfx/+zEkEgasSPV8grb82iQ81Ysc+v4=',0,'aynur','Aynur','Əliyeva','aynur@q360.az',0,'employee','HR Mütəxəssisi','','',NULL,'','',1,'2025-10-10 15:54:57.891311',NULL,19,'2025-10-10 15:54:57.901882',NULL,'+',1,NULL,NULL);
INSERT INTO "accounts_historicaluser" VALUES(11,'pbkdf2_sha256$870000$F8UpUBMAjn3nyIBZohXgLg$+cNXk5KuEBB+P5G4aj5CP6e0BlMwQ/CqC3uy2Yh9sYA=',0,'kamran','Kamran','Əliyev','kamran@q360.az',0,'employee','HR Mütəxəssisi','','',NULL,'','',1,'2025-10-10 15:54:58.225285',NULL,20,'2025-10-10 15:54:58.234226',NULL,'+',1,NULL,NULL);
INSERT INTO "accounts_historicaluser" VALUES(12,'pbkdf2_sha256$870000$EHa9dh9uU7XAXfxQoKo8tV$db/TZ7H6kGp5zgCbT2+IiMWST7Y9fJJQui0RTASihzc=',0,'elchin','Elçin','Həsənov','elchin@q360.az',0,'employee','Proqramçı','','',NULL,'','',1,'2025-10-10 15:54:58.557737',NULL,21,'2025-10-10 15:54:58.566590',NULL,'+',2,NULL,NULL);
INSERT INTO "accounts_historicaluser" VALUES(13,'pbkdf2_sha256$870000$oYKCeYEPIcZSbLav2rdBPx$vJypvbZPNFu9HXdxHlJuV5jAc/ZZjqoG0QRA80Xo8mg=',0,'gunel','Günəl','İsmayılova','gunel@q360.az',0,'employee','Proqramçı','','',NULL,'','',1,'2025-10-10 15:54:58.886818',NULL,22,'2025-10-10 15:54:58.894994',NULL,'+',2,NULL,NULL);
INSERT INTO "accounts_historicaluser" VALUES(14,'pbkdf2_sha256$870000$wjZNsgN3wwx3rDGOrnUwoy$6hR78tM8sVPy2uk8zt54Uq3lFGSnVJ41R0EtimcxTQk=',0,'nigar','Nigar','Məmmədova','nigar@q360.az',0,'employee','Sistem Administratoru','','',NULL,'','',1,'2025-10-10 15:54:59.224189',NULL,23,'2025-10-10 15:54:59.233820',NULL,'+',2,NULL,NULL);
INSERT INTO "accounts_historicaluser" VALUES(15,'pbkdf2_sha256$870000$dcLYAuI49MBfxHRla3SNh5$pbJANncQoSYIFC2Zn3xKdZc3B6wSf/yvB1mnW5qayg8=',0,'farid','Farid','Abdullayev','farid@q360.az',0,'employee','Mühasib','','',NULL,'','',1,'2025-10-10 15:54:59.562356',NULL,24,'2025-10-10 15:54:59.571850',NULL,'+',3,NULL,NULL);
INSERT INTO "accounts_historicaluser" VALUES(16,'pbkdf2_sha256$870000$rRG52Kr18fg2dXo36588Al$G7EGbwJ0NVUILeLXSCi/wpr3WrMOXoxDT4UDpFb5HLo=',0,'sevinc','Sevinc','Qasımova','sevinc@q360.az',0,'employee','Mühasib','','',NULL,'','',1,'2025-10-10 15:54:59.911287',NULL,25,'2025-10-10 15:54:59.920047',NULL,'+',3,NULL,NULL);
INSERT INTO "accounts_historicaluser" VALUES(17,'pbkdf2_sha256$870000$k7nLd6WSmzCPJnxCLQEyDs$Klws9xTaoB1d0SORyr6qa/9yjmDxXY2kCb9v1IYbpB0=',0,'tural','Tural','Cəfərov','tural@q360.az',0,'employee','Hüquqşünas','','',NULL,'','',1,'2025-10-10 15:55:00.234951',NULL,26,'2025-10-10 15:55:00.243204',NULL,'+',4,NULL,NULL);
INSERT INTO "accounts_historicaluser" VALUES(18,'pbkdf2_sha256$870000$yXrrUM7OFt8UL5SpiC4vCg$o+xhOvj39bdOxUXf/Dz2xJcI7NvbDIGbKl9pdMBkPA4=',0,'aysel','Aysel','Rəhimova','aysel@q360.az',0,'employee','PR Mütəxəssisi','','',NULL,'','',1,'2025-10-10 15:55:00.569894',NULL,27,'2025-10-10 15:55:00.578929',NULL,'+',5,NULL,NULL);
INSERT INTO "accounts_historicaluser" VALUES(19,'pbkdf2_sha256$870000$cWNOca0FFuNObv3ZYRlQ6R$5U06si/aAYSwGeLDNurAYwC6/qqFJFkERJTb7h37n7M=',0,'murad','Murad','Süleymanov','murad@q360.az',0,'employee','PR Mütəxəssisi','','',NULL,'','',1,'2025-10-10 15:55:00.897865',NULL,28,'2025-10-10 15:55:00.908192',NULL,'+',5,NULL,NULL);
INSERT INTO "accounts_historicaluser" VALUES(7,'pbkdf2_sha256$870000$8JpYXlPFZgePktgqH0vtAO$MeSwek6Npsj30YxqL2plcKTpmA8ePuUWjo4osP26lIA=',0,'rashad','Rəşad','Məmmədov','rashad@q360.az',0,'manager','HR Meneceri','','',NULL,'','',1,'2025-10-10 15:54:56.903567',NULL,29,'2025-10-10 15:55:00.944797',NULL,'~',1,NULL,2);
INSERT INTO "accounts_historicaluser" VALUES(8,'pbkdf2_sha256$870000$T0w0YxwXnhO7W44xdwNiAn$2dnZEKfcWBiE8CpDki/cnCi/CJvPdzd4zM23oAbObyU=',0,'elvin','Elvin','Quliyev','elvin@q360.az',0,'manager','IT Meneceri','','',NULL,'','',1,'2025-10-10 15:54:57.238382',NULL,30,'2025-10-10 15:55:00.972459',NULL,'~',2,NULL,2);
INSERT INTO "accounts_historicaluser" VALUES(9,'pbkdf2_sha256$870000$SiqYfQdaFK7M6QfmgScyF8$vXbrwzzSk3HI9J/Z+jVsPhY5zooxzZY8/Tb8MqQayuA=',0,'leyla','Leyla','Həsənova','leyla@q360.az',0,'manager','Maliyyə Meneceri','','',NULL,'','',1,'2025-10-10 15:54:57.561516',NULL,31,'2025-10-10 15:55:01.001050',NULL,'~',3,NULL,2);
INSERT INTO "accounts_historicaluser" VALUES(10,'pbkdf2_sha256$870000$LowPGlRzHG6dB7Q07nnzgP$rFaWQQQKLuI7zfx/+zEkEgasSPV8grb82iQ81Ysc+v4=',0,'aynur','Aynur','Əliyeva','aynur@q360.az',0,'employee','HR Mütəxəssisi','','',NULL,'','',1,'2025-10-10 15:54:57.891311',NULL,32,'2025-10-10 15:55:01.030687',NULL,'~',1,NULL,7);
INSERT INTO "accounts_historicaluser" VALUES(11,'pbkdf2_sha256$870000$F8UpUBMAjn3nyIBZohXgLg$+cNXk5KuEBB+P5G4aj5CP6e0BlMwQ/CqC3uy2Yh9sYA=',0,'kamran','Kamran','Əliyev','kamran@q360.az',0,'employee','HR Mütəxəssisi','','',NULL,'','',1,'2025-10-10 15:54:58.225285',NULL,33,'2025-10-10 15:55:01.059575',NULL,'~',1,NULL,7);
INSERT INTO "accounts_historicaluser" VALUES(12,'pbkdf2_sha256$870000$EHa9dh9uU7XAXfxQoKo8tV$db/TZ7H6kGp5zgCbT2+IiMWST7Y9fJJQui0RTASihzc=',0,'elchin','Elçin','Həsənov','elchin@q360.az',0,'employee','Proqramçı','','',NULL,'','',1,'2025-10-10 15:54:58.557737',NULL,34,'2025-10-10 15:55:01.088450',NULL,'~',2,NULL,8);
INSERT INTO "accounts_historicaluser" VALUES(13,'pbkdf2_sha256$870000$oYKCeYEPIcZSbLav2rdBPx$vJypvbZPNFu9HXdxHlJuV5jAc/ZZjqoG0QRA80Xo8mg=',0,'gunel','Günəl','İsmayılova','gunel@q360.az',0,'employee','Proqramçı','','',NULL,'','',1,'2025-10-10 15:54:58.886818',NULL,35,'2025-10-10 15:55:01.116312',NULL,'~',2,NULL,8);
INSERT INTO "accounts_historicaluser" VALUES(14,'pbkdf2_sha256$870000$wjZNsgN3wwx3rDGOrnUwoy$6hR78tM8sVPy2uk8zt54Uq3lFGSnVJ41R0EtimcxTQk=',0,'nigar','Nigar','Məmmədova','nigar@q360.az',0,'employee','Sistem Administratoru','','',NULL,'','',1,'2025-10-10 15:54:59.224189',NULL,36,'2025-10-10 15:55:01.145775',NULL,'~',2,NULL,8);
INSERT INTO "accounts_historicaluser" VALUES(15,'pbkdf2_sha256$870000$dcLYAuI49MBfxHRla3SNh5$pbJANncQoSYIFC2Zn3xKdZc3B6wSf/yvB1mnW5qayg8=',0,'farid','Farid','Abdullayev','farid@q360.az',0,'employee','Mühasib','','',NULL,'','',1,'2025-10-10 15:54:59.562356',NULL,37,'2025-10-10 15:55:01.177123',NULL,'~',3,NULL,9);
INSERT INTO "accounts_historicaluser" VALUES(16,'pbkdf2_sha256$870000$rRG52Kr18fg2dXo36588Al$G7EGbwJ0NVUILeLXSCi/wpr3WrMOXoxDT4UDpFb5HLo=',0,'sevinc','Sevinc','Qasımova','sevinc@q360.az',0,'employee','Mühasib','','',NULL,'','',1,'2025-10-10 15:54:59.911287',NULL,38,'2025-10-10 15:55:01.207329',NULL,'~',3,NULL,9);
INSERT INTO "accounts_historicaluser" VALUES(17,'pbkdf2_sha256$870000$k7nLd6WSmzCPJnxCLQEyDs$Klws9xTaoB1d0SORyr6qa/9yjmDxXY2kCb9v1IYbpB0=',0,'tural','Tural','Cəfərov','tural@q360.az',0,'employee','Hüquqşünas','','',NULL,'','',1,'2025-10-10 15:55:00.234951',NULL,39,'2025-10-10 15:55:01.236402',NULL,'~',4,NULL,2);
INSERT INTO "accounts_historicaluser" VALUES(18,'pbkdf2_sha256$870000$yXrrUM7OFt8UL5SpiC4vCg$o+xhOvj39bdOxUXf/Dz2xJcI7NvbDIGbKl9pdMBkPA4=',0,'aysel','Aysel','Rəhimova','aysel@q360.az',0,'employee','PR Mütəxəssisi','','',NULL,'','',1,'2025-10-10 15:55:00.569894',NULL,40,'2025-10-10 15:55:01.268668',NULL,'~',5,NULL,2);
INSERT INTO "accounts_historicaluser" VALUES(19,'pbkdf2_sha256$870000$cWNOca0FFuNObv3ZYRlQ6R$5U06si/aAYSwGeLDNurAYwC6/qqFJFkERJTb7h37n7M=',0,'murad','Murad','Süleymanov','murad@q360.az',0,'employee','PR Mütəxəssisi','','',NULL,'','',1,'2025-10-10 15:55:00.897865',NULL,41,'2025-10-10 15:55:01.299403',NULL,'~',5,NULL,2);
INSERT INTO "accounts_historicaluser" VALUES(7,'pbkdf2_sha256$870000$8JpYXlPFZgePktgqH0vtAO$MeSwek6Npsj30YxqL2plcKTpmA8ePuUWjo4osP26lIA=',0,'rashad','Rəşad','Məmmədov','rashad@q360.az',0,'manager','HR Meneceri','','',NULL,'','',1,'2025-10-10 15:54:56.903567',NULL,42,'2025-10-10 15:57:26.726162',NULL,'~',1,NULL,2);
INSERT INTO "accounts_historicaluser" VALUES(8,'pbkdf2_sha256$870000$T0w0YxwXnhO7W44xdwNiAn$2dnZEKfcWBiE8CpDki/cnCi/CJvPdzd4zM23oAbObyU=',0,'elvin','Elvin','Quliyev','elvin@q360.az',0,'manager','IT Meneceri','','',NULL,'','',1,'2025-10-10 15:54:57.238382',NULL,43,'2025-10-10 15:57:26.757665',NULL,'~',2,NULL,2);
INSERT INTO "accounts_historicaluser" VALUES(9,'pbkdf2_sha256$870000$SiqYfQdaFK7M6QfmgScyF8$vXbrwzzSk3HI9J/Z+jVsPhY5zooxzZY8/Tb8MqQayuA=',0,'leyla','Leyla','Həsənova','leyla@q360.az',0,'manager','Maliyyə Meneceri','','',NULL,'','',1,'2025-10-10 15:54:57.561516',NULL,44,'2025-10-10 15:57:26.787108',NULL,'~',3,NULL,2);
INSERT INTO "accounts_historicaluser" VALUES(10,'pbkdf2_sha256$870000$LowPGlRzHG6dB7Q07nnzgP$rFaWQQQKLuI7zfx/+zEkEgasSPV8grb82iQ81Ysc+v4=',0,'aynur','Aynur','Əliyeva','aynur@q360.az',0,'employee','HR Mütəxəssisi','','',NULL,'','',1,'2025-10-10 15:54:57.891311',NULL,45,'2025-10-10 15:57:26.816547',NULL,'~',1,NULL,7);
INSERT INTO "accounts_historicaluser" VALUES(11,'pbkdf2_sha256$870000$F8UpUBMAjn3nyIBZohXgLg$+cNXk5KuEBB+P5G4aj5CP6e0BlMwQ/CqC3uy2Yh9sYA=',0,'kamran','Kamran','Əliyev','kamran@q360.az',0,'employee','HR Mütəxəssisi','','',NULL,'','',1,'2025-10-10 15:54:58.225285',NULL,46,'2025-10-10 15:57:26.846138',NULL,'~',1,NULL,7);
INSERT INTO "accounts_historicaluser" VALUES(12,'pbkdf2_sha256$870000$EHa9dh9uU7XAXfxQoKo8tV$db/TZ7H6kGp5zgCbT2+IiMWST7Y9fJJQui0RTASihzc=',0,'elchin','Elçin','Həsənov','elchin@q360.az',0,'employee','Proqramçı','','',NULL,'','',1,'2025-10-10 15:54:58.557737',NULL,47,'2025-10-10 15:57:26.877578',NULL,'~',2,NULL,8);
INSERT INTO "accounts_historicaluser" VALUES(13,'pbkdf2_sha256$870000$oYKCeYEPIcZSbLav2rdBPx$vJypvbZPNFu9HXdxHlJuV5jAc/ZZjqoG0QRA80Xo8mg=',0,'gunel','Günəl','İsmayılova','gunel@q360.az',0,'employee','Proqramçı','','',NULL,'','',1,'2025-10-10 15:54:58.886818',NULL,48,'2025-10-10 15:57:26.907097',NULL,'~',2,NULL,8);
INSERT INTO "accounts_historicaluser" VALUES(14,'pbkdf2_sha256$870000$wjZNsgN3wwx3rDGOrnUwoy$6hR78tM8sVPy2uk8zt54Uq3lFGSnVJ41R0EtimcxTQk=',0,'nigar','Nigar','Məmmədova','nigar@q360.az',0,'employee','Sistem Administratoru','','',NULL,'','',1,'2025-10-10 15:54:59.224189',NULL,49,'2025-10-10 15:57:26.937353',NULL,'~',2,NULL,8);
INSERT INTO "accounts_historicaluser" VALUES(15,'pbkdf2_sha256$870000$dcLYAuI49MBfxHRla3SNh5$pbJANncQoSYIFC2Zn3xKdZc3B6wSf/yvB1mnW5qayg8=',0,'farid','Farid','Abdullayev','farid@q360.az',0,'employee','Mühasib','','',NULL,'','',1,'2025-10-10 15:54:59.562356',NULL,50,'2025-10-10 15:57:26.966796',NULL,'~',3,NULL,9);
INSERT INTO "accounts_historicaluser" VALUES(16,'pbkdf2_sha256$870000$rRG52Kr18fg2dXo36588Al$G7EGbwJ0NVUILeLXSCi/wpr3WrMOXoxDT4UDpFb5HLo=',0,'sevinc','Sevinc','Qasımova','sevinc@q360.az',0,'employee','Mühasib','','',NULL,'','',1,'2025-10-10 15:54:59.911287',NULL,51,'2025-10-10 15:57:26.996852',NULL,'~',3,NULL,9);
INSERT INTO "accounts_historicaluser" VALUES(17,'pbkdf2_sha256$870000$k7nLd6WSmzCPJnxCLQEyDs$Klws9xTaoB1d0SORyr6qa/9yjmDxXY2kCb9v1IYbpB0=',0,'tural','Tural','Cəfərov','tural@q360.az',0,'employee','Hüquqşünas','','',NULL,'','',1,'2025-10-10 15:55:00.234951',NULL,52,'2025-10-10 15:57:27.027484',NULL,'~',4,NULL,2);
INSERT INTO "accounts_historicaluser" VALUES(18,'pbkdf2_sha256$870000$yXrrUM7OFt8UL5SpiC4vCg$o+xhOvj39bdOxUXf/Dz2xJcI7NvbDIGbKl9pdMBkPA4=',0,'aysel','Aysel','Rəhimova','aysel@q360.az',0,'employee','PR Mütəxəssisi','','',NULL,'','',1,'2025-10-10 15:55:00.569894',NULL,53,'2025-10-10 15:57:27.057179',NULL,'~',5,NULL,2);
INSERT INTO "accounts_historicaluser" VALUES(19,'pbkdf2_sha256$870000$cWNOca0FFuNObv3ZYRlQ6R$5U06si/aAYSwGeLDNurAYwC6/qqFJFkERJTb7h37n7M=',0,'murad','Murad','Süleymanov','murad@q360.az',0,'employee','PR Mütəxəssisi','','',NULL,'','',1,'2025-10-10 15:55:00.897865',NULL,54,'2025-10-10 15:57:27.086068',NULL,'~',5,NULL,2);
INSERT INTO "accounts_historicaluser" VALUES(1,'pbkdf2_sha256$870000$55Rtqbij2pb2iQmfZSlwaw$f4jkRvmNoWoMMg7opXGVH2yc58BqLEoyyHI98r6NkoA=',1,'Tahmaz','Tahmaz','Muradov','admin@q360.gov.az',1,'superadmin','müdür','Seyran','0605536990','0001','','Tahmaz',1,'2025-10-09 06:34:12.095047','2025-10-10 20:34:09.674564',55,'2025-10-10 20:34:09.681850',NULL,'~',NULL,1,1);
INSERT INTO "accounts_historicaluser" VALUES(19,'pbkdf2_sha256$870000$cWNOca0FFuNObv3ZYRlQ6R$5U06si/aAYSwGeLDNurAYwC6/qqFJFkERJTb7h37n7M=',0,'murad','Murad','Süleymanov','murad@q360.az',0,'employee','PR Mütəxəssisi','','','0003','','',1,'2025-10-10 15:55:00.897865',NULL,56,'2025-10-10 20:40:15.825181',NULL,'~',5,1,2);
INSERT INTO "accounts_historicaluser" VALUES(1,'pbkdf2_sha256$870000$55Rtqbij2pb2iQmfZSlwaw$f4jkRvmNoWoMMg7opXGVH2yc58BqLEoyyHI98r6NkoA=',1,'Tahmaz','Tahmaz','Muradov','admin@q360.gov.az',1,'superadmin','müdür','Seyran','0605536990','0001','profiles/IMG-20250426-WA0048_bsVsgAX.jpg','Tahmaz',1,'2025-10-09 06:34:12.095047','2025-10-10 20:34:09.674564',57,'2025-10-10 20:43:12.015901',NULL,'~',NULL,1,1);
INSERT INTO "accounts_historicaluser" VALUES(1,'pbkdf2_sha256$870000$55Rtqbij2pb2iQmfZSlwaw$f4jkRvmNoWoMMg7opXGVH2yc58BqLEoyyHI98r6NkoA=',1,'Tahmaz','Tahmaz','Muradov','admin@q360.gov.az',1,'superadmin','müdür','Seyran','0605536990','0001','profiles/IMG-20250426-WA0048_bsVsgAX.jpg','Tahmaz',1,'2025-10-09 06:34:12.095047','2025-10-10 20:34:09.674564',58,'2025-10-10 20:44:02.571424',NULL,'~',NULL,1,1);
INSERT INTO "accounts_historicaluser" VALUES(1,'pbkdf2_sha256$870000$55Rtqbij2pb2iQmfZSlwaw$f4jkRvmNoWoMMg7opXGVH2yc58BqLEoyyHI98r6NkoA=',1,'Tahmaz','Tahmaz','Muradov','admin@q360.gov.az',1,'superadmin','müdür','Seyran','0605536990','0001','profiles/IMG-20250426-WA0048_bsVsgAX.jpg','Tahmaz',1,'2025-10-09 06:34:12.095047','2025-10-10 20:34:09.674564',59,'2025-10-10 20:44:22.167079',NULL,'~',1,1,1);
INSERT INTO "accounts_historicaluser" VALUES(1,'pbkdf2_sha256$870000$55Rtqbij2pb2iQmfZSlwaw$f4jkRvmNoWoMMg7opXGVH2yc58BqLEoyyHI98r6NkoA=',1,'Tahmaz','Tahmaz','Muradov','admin@q360.gov.az',1,'superadmin','müdür','Seyran','0605536990','0001','profiles/IMG-20250426-WA0048_bsVsgAX.jpg','Tahmaz',1,'2025-10-09 06:34:12.095047','2025-10-10 20:34:09.674564',60,'2025-10-10 20:55:10.456535',NULL,'~',1,1,1);
INSERT INTO "accounts_historicaluser" VALUES(15,'pbkdf2_sha256$870000$DvVPlXGgbDc4W9qF5LJOEI$bhKZtPlXl8Kwug5zLnEHCkDsTP99TwjU5hl4NSMTHqc=',0,'farid','Farid','Abdullayev','farid@q360.az',0,'employee','Mühasib','','',NULL,'','',1,'2025-10-10 15:54:59.562356',NULL,61,'2025-10-10 21:07:55.701197',NULL,'~',3,1,9);
INSERT INTO "accounts_historicaluser" VALUES(15,'pbkdf2_sha256$870000$DvVPlXGgbDc4W9qF5LJOEI$bhKZtPlXl8Kwug5zLnEHCkDsTP99TwjU5hl4NSMTHqc=',0,'farid','Farid','Abdullayev','farid@q360.az',0,'employee','Mühasib','','',NULL,'profiles/amal.jpg','',1,'2025-10-10 15:54:59.562356',NULL,62,'2025-10-10 21:08:34.593928',NULL,'~',3,1,9);
INSERT INTO "accounts_historicaluser" VALUES(15,'pbkdf2_sha256$870000$DvVPlXGgbDc4W9qF5LJOEI$bhKZtPlXl8Kwug5zLnEHCkDsTP99TwjU5hl4NSMTHqc=',0,'farid','Farid','Abdullayev','farid@q360.az',0,'employee','Mühasib','','',NULL,'profiles/amal.jpg','',1,'2025-10-10 15:54:59.562356',NULL,63,'2025-10-10 21:09:20.112250',NULL,'~',3,1,9);
INSERT INTO "accounts_historicaluser" VALUES(15,'pbkdf2_sha256$870000$DvVPlXGgbDc4W9qF5LJOEI$bhKZtPlXl8Kwug5zLnEHCkDsTP99TwjU5hl4NSMTHqc=',0,'farid','Farid','Abdullayev','farid@q360.az',0,'employee','Mühasib','','',NULL,'profiles/amal.jpg','',1,'2025-10-10 15:54:59.562356','2025-10-10 21:09:40.899180',64,'2025-10-10 21:09:40.909476',NULL,'~',3,15,9);
INSERT INTO "accounts_historicaluser" VALUES(1,'pbkdf2_sha256$870000$55Rtqbij2pb2iQmfZSlwaw$f4jkRvmNoWoMMg7opXGVH2yc58BqLEoyyHI98r6NkoA=',1,'Tahmaz','Tahmaz','Muradov','admin@q360.gov.az',1,'superadmin','müdür','Seyran','0605536990','0001','profiles/IMG-20250426-WA0048_bsVsgAX.jpg','Tahmaz',1,'2025-10-09 06:34:12.095047','2025-10-10 22:47:07.450935',65,'2025-10-10 22:47:07.459460',NULL,'~',1,1,1);
INSERT INTO "accounts_historicaluser" VALUES(20,'pbkdf2_sha256$870000$0VobTjWJkmRpTyvNlLgkDK$+rJyAHNCibpNAzeWAx7I673hNTB95D803cuBOR4vsN8=',1,'tahmaz','','','tahmaz@gmail.com',1,'employee','','','',NULL,'','',1,'2025-10-11 19:13:56.972223',NULL,66,'2025-10-11 19:13:56.996784',NULL,'+',NULL,NULL,NULL);
INSERT INTO "accounts_historicaluser" VALUES(1,'pbkdf2_sha256$870000$55Rtqbij2pb2iQmfZSlwaw$f4jkRvmNoWoMMg7opXGVH2yc58BqLEoyyHI98r6NkoA=',1,'Tahmaz','Tahmaz','Muradov','admin@q360.gov.az',1,'superadmin','müdür','Seyran','0605536990','0001','profiles/IMG-20250426-WA0048_bsVsgAX.jpg','Tahmaz',1,'2025-10-09 06:34:12.095047','2025-10-10 22:47:07.450935',67,'2025-10-14 22:16:27.483629',NULL,'~',1,1,1);
INSERT INTO "accounts_historicaluser" VALUES(1,'pbkdf2_sha256$870000$55Rtqbij2pb2iQmfZSlwaw$f4jkRvmNoWoMMg7opXGVH2yc58BqLEoyyHI98r6NkoA=',1,'Tahmaz','Tahmaz','Muradov','admin@q360.gov.az',1,'superadmin','müdür','Seyran','0605536990','0001','profiles/IMG-20250426-WA0048_bsVsgAX.jpg','Tahmaz',1,'2025-10-09 06:34:12.095047','2025-10-10 22:47:07.450935',68,'2025-10-14 22:16:47.811432',NULL,'~',2,1,1);
INSERT INTO "accounts_historicaluser" VALUES(20,'pbkdf2_sha256$870000$0VobTjWJkmRpTyvNlLgkDK$+rJyAHNCibpNAzeWAx7I673hNTB95D803cuBOR4vsN8=',1,'tahmaz','Tahmaz','Muradov','tahmaz@gmail.com',1,'manager','PR Mütəxəssisi','Seyran','0605536990','0005','','',1,'2025-10-11 19:13:56.972223',NULL,69,'2025-10-14 22:17:55.672885',NULL,'~',2,1,1);
INSERT INTO "accounts_historicaluser" VALUES(21,'',0,'rashad.mammadov','Rəşad','Məmmədov','rashad.mammadov@mincom.gov.az',1,'admin','Departament direktoru','Elçin','','EMP002','','',1,'2025-10-15 07:47:47.367788',NULL,70,'2025-10-15 07:47:47.371995',NULL,'+',6,NULL,NULL);
INSERT INTO "accounts_historicaluser" VALUES(21,'pbkdf2_sha256$600000$qdTDUMYzc0jQLufxh74NI2$VmEXIh8CC/s0evtlhbtNWho7peU3JY7U1w9s3LtY8i8=',0,'rashad.mammadov','Rəşad','Məmmədov','rashad.mammadov@mincom.gov.az',1,'admin','Departament direktoru','Elçin','','EMP002','','',1,'2025-10-15 07:47:47.367788',NULL,71,'2025-10-15 07:47:47.764999',NULL,'~',6,NULL,NULL);
INSERT INTO "accounts_historicaluser" VALUES(22,'',0,'leyla.huseynova','Leyla','Hüseynova','leyla.huseynova@mincom.gov.az',0,'manager','Şöbə müdiri','Vaqif','','EMP003','','',1,'2025-10-15 07:47:47.820029',NULL,72,'2025-10-15 07:47:47.823308',NULL,'+',7,NULL,21);
INSERT INTO "accounts_historicaluser" VALUES(22,'pbkdf2_sha256$600000$CKueHa4TYy82cecJv63a10$yGMkXSKpPirK3sxD8kVOEjn0WN+c65vwdR05LPdg9Dc=',0,'leyla.huseynova','Leyla','Hüseynova','leyla.huseynova@mincom.gov.az',0,'manager','Şöbə müdiri','Vaqif','','EMP003','','',1,'2025-10-15 07:47:47.820029',NULL,73,'2025-10-15 07:47:48.191149',NULL,'~',7,NULL,21);
INSERT INTO "accounts_historicaluser" VALUES(23,'',0,'murad.aliyev','Murad','Əliyev','murad.aliyev@mincom.gov.az',0,'employee','Baş mütəxəssis','Təbriz','','EMP004','','',1,'2025-10-15 07:47:48.217040',NULL,74,'2025-10-15 07:47:48.218139',NULL,'+',7,NULL,22);
INSERT INTO "accounts_historicaluser" VALUES(23,'pbkdf2_sha256$600000$WVScpHpZfJ7dmvtaiOYGqg$V1tnEAYptxoEZTZezaYZFpRFtYcHIeIYqqMJZYtEfTk=',0,'murad.aliyev','Murad','Əliyev','murad.aliyev@mincom.gov.az',0,'employee','Baş mütəxəssis','Təbriz','','EMP004','','',1,'2025-10-15 07:47:48.217040',NULL,75,'2025-10-15 07:47:48.599990',NULL,'~',7,NULL,22);
INSERT INTO "accounts_historicaluser" VALUES(24,'pbkdf2_sha256$870000$pm5rhwhjkOFsyuNtRGeh8w$K9kYT8CjHVm0wx2AfIX/ET/buFAA3b6hUQBS24zn488=',0,'nigar.hasanova','Nigar','Həsənova','nigar.hasanova@mincom.gov.az',0,'employee','Aparıcı mütəxəssis','Ramiz','','EMP005','','',1,'2025-10-15 07:58:53.995135',NULL,76,'2025-10-15 07:58:54.008507',NULL,'+',7,NULL,NULL);
INSERT INTO "accounts_historicaluser" VALUES(24,'pbkdf2_sha256$870000$pm5rhwhjkOFsyuNtRGeh8w$K9kYT8CjHVm0wx2AfIX/ET/buFAA3b6hUQBS24zn488=',0,'nigar.hasanova','Nigar','Həsənova','nigar.hasanova@mincom.gov.az',0,'employee','Aparıcı mütəxəssis','Ramiz','','EMP005','','',1,'2025-10-15 07:58:53.995135',NULL,77,'2025-10-15 07:58:54.044978',NULL,'~',7,NULL,22);
INSERT INTO "accounts_historicaluser" VALUES(25,'pbkdf2_sha256$870000$xTV7VPNkSMVkXhk6zBjt0j$NMh6GGVWHrS1/UGvB/WThl9u5fWd04bQR6EY4wRgLd0=',0,'elvin.quliyev','Elvin','Quliyev','elvin.quliyev@mincom.gov.az',0,'employee','Mütəxəssis','Məhəmməd','','EMP006','','',1,'2025-10-15 07:58:54.347862',NULL,78,'2025-10-15 07:58:54.356780',NULL,'+',7,NULL,NULL);
INSERT INTO "accounts_historicaluser" VALUES(25,'pbkdf2_sha256$870000$xTV7VPNkSMVkXhk6zBjt0j$NMh6GGVWHrS1/UGvB/WThl9u5fWd04bQR6EY4wRgLd0=',0,'elvin.quliyev','Elvin','Quliyev','elvin.quliyev@mincom.gov.az',0,'employee','Mütəxəssis','Məhəmməd','','EMP006','','',1,'2025-10-15 07:58:54.347862',NULL,79,'2025-10-15 07:58:54.391795',NULL,'~',7,NULL,22);
INSERT INTO "accounts_historicaluser" VALUES(26,'pbkdf2_sha256$870000$rBiVtLTU4vACOym77tiWuL$tT1KJkMdVc+OdD/zb6CQ1fH1vxzvBWrW9Q9qzr/LT4Y=',0,'farid.ismayilov','Farid','İsmayılov','farid.ismayilov@mincom.gov.az',0,'manager','Şöbə müdiri (Kibertəhlükəsizlik)','Əli','','EMP007','','',1,'2025-10-15 07:58:54.696104',NULL,80,'2025-10-15 07:58:54.707418',NULL,'+',8,NULL,NULL);
INSERT INTO "accounts_historicaluser" VALUES(26,'pbkdf2_sha256$870000$rBiVtLTU4vACOym77tiWuL$tT1KJkMdVc+OdD/zb6CQ1fH1vxzvBWrW9Q9qzr/LT4Y=',0,'farid.ismayilov','Farid','İsmayılov','farid.ismayilov@mincom.gov.az',0,'manager','Şöbə müdiri (Kibertəhlükəsizlik)','Əli','','EMP007','','',1,'2025-10-15 07:58:54.696104',NULL,81,'2025-10-15 07:58:54.748321',NULL,'~',8,NULL,21);
INSERT INTO "accounts_historicaluser" VALUES(27,'pbkdf2_sha256$870000$q7pwGJncFeJBYsVDS9IWnW$y8p+Az+P/LY1Uig40v6DOPlK0l1QUtl/S9WeEvIlXGk=',0,'aysel.memmedova','Aysel','Məmmədova','aysel.memmedova@mincom.gov.az',0,'employee','Kibertəhlükəsizlik mütəxəssisi','İlham','','EMP008','','',1,'2025-10-15 07:58:55.070605',NULL,82,'2025-10-15 07:58:55.079596',NULL,'+',8,NULL,NULL);
INSERT INTO "accounts_historicaluser" VALUES(27,'pbkdf2_sha256$870000$q7pwGJncFeJBYsVDS9IWnW$y8p+Az+P/LY1Uig40v6DOPlK0l1QUtl/S9WeEvIlXGk=',0,'aysel.memmedova','Aysel','Məmmədova','aysel.memmedova@mincom.gov.az',0,'employee','Kibertəhlükəsizlik mütəxəssisi','İlham','','EMP008','','',1,'2025-10-15 07:58:55.070605',NULL,83,'2025-10-15 07:58:55.118833',NULL,'~',8,NULL,26);
INSERT INTO "accounts_historicaluser" VALUES(28,'pbkdf2_sha256$870000$59u3AoVZL3ongUMctcFmLi$ScWojOEIp4Y2+ono8ul13rsxfvhlbf8/EuNrxWsGCu0=',0,'kamran.bashirov','Kamran','Bəşirov','kamran.bashirov@mincom.gov.az',1,'admin','İnsan Resursları Direktoru','Rəhim','','EMP009','','',1,'2025-10-15 07:58:55.424328',NULL,84,'2025-10-15 07:58:55.432906',NULL,'+',9,NULL,NULL);
INSERT INTO "accounts_historicaluser" VALUES(29,'pbkdf2_sha256$870000$kt4e9nYbXopALipofzjsE1$BFJ9NuYUULpM88qC3BT0Oa1uQLGiZGyGvtGC8xT3Dow=',0,'sevinc.huseynli','Sevinc','Hüseynli','sevinc.huseynli@mincom.gov.az',0,'employee','HR Business Partner','Ağa','','EMP010','','',1,'2025-10-15 07:58:55.744128',NULL,85,'2025-10-15 07:58:55.753049',NULL,'+',9,NULL,NULL);
INSERT INTO "accounts_historicaluser" VALUES(29,'pbkdf2_sha256$870000$kt4e9nYbXopALipofzjsE1$BFJ9NuYUULpM88qC3BT0Oa1uQLGiZGyGvtGC8xT3Dow=',0,'sevinc.huseynli','Sevinc','Hüseynli','sevinc.huseynli@mincom.gov.az',0,'employee','HR Business Partner','Ağa','','EMP010','','',1,'2025-10-15 07:58:55.744128',NULL,86,'2025-10-15 07:58:55.788847',NULL,'~',9,NULL,28);
INSERT INTO "accounts_historicaluser" VALUES(15,'pbkdf2_sha256$870000$DvVPlXGgbDc4W9qF5LJOEI$bhKZtPlXl8Kwug5zLnEHCkDsTP99TwjU5hl4NSMTHqc=',0,'farid','Farid','Abdullayev','farid@q360.az',0,'employee','Mühasib','','',NULL,'profiles/amal.jpg','',1,'2025-10-10 15:54:59.562356','2025-10-10 21:09:40.899180',87,'2025-10-15 11:43:22.045375',NULL,'~',4,1,9);
INSERT INTO "accounts_historicaluser" VALUES(1,'pbkdf2_sha256$870000$55Rtqbij2pb2iQmfZSlwaw$f4jkRvmNoWoMMg7opXGVH2yc58BqLEoyyHI98r6NkoA=',1,'Tahmaz','Tahmaz','Muradov','admin@q360.gov.az',1,'superadmin','müdür','Seyran','0605536990','0001','profiles/IMG-20250426-WA0048_bsVsgAX.jpg','Tahmaz',1,'2025-10-09 06:34:12.095047','2025-10-15 13:49:19.667136',88,'2025-10-15 13:49:19.673526',NULL,'~',2,1,1);
INSERT INTO "accounts_historicaluser" VALUES(16,'pbkdf2_sha256$870000$rRG52Kr18fg2dXo36588Al$G7EGbwJ0NVUILeLXSCi/wpr3WrMOXoxDT4UDpFb5HLo=',0,'sevinc','Sevinc','Qasımova','sevinc@q360.az',0,'employee','Mühasib','','',NULL,'','',1,'2025-10-10 15:54:59.911287',NULL,89,'2025-10-16 00:52:15.929401',NULL,'~',3,1,9);
INSERT INTO "accounts_historicaluser" VALUES(7,'pbkdf2_sha256$870000$8JpYXlPFZgePktgqH0vtAO$MeSwek6Npsj30YxqL2plcKTpmA8ePuUWjo4osP26lIA=',0,'rashad','Rəşad','Məmmədov','rashad@q360.az',0,'manager','HR Meneceri','','',NULL,'','',1,'2025-10-10 15:54:56.903567',NULL,90,'2025-10-16 13:24:16.592853',NULL,'~',1,NULL,2);
INSERT INTO "accounts_historicaluser" VALUES(8,'pbkdf2_sha256$870000$T0w0YxwXnhO7W44xdwNiAn$2dnZEKfcWBiE8CpDki/cnCi/CJvPdzd4zM23oAbObyU=',0,'elvin','Elvin','Quliyev','elvin@q360.az',0,'manager','IT Meneceri','','',NULL,'','',1,'2025-10-10 15:54:57.238382',NULL,91,'2025-10-16 13:24:16.624250',NULL,'~',2,NULL,2);
INSERT INTO "accounts_historicaluser" VALUES(9,'pbkdf2_sha256$870000$SiqYfQdaFK7M6QfmgScyF8$vXbrwzzSk3HI9J/Z+jVsPhY5zooxzZY8/Tb8MqQayuA=',0,'leyla','Leyla','Həsənova','leyla@q360.az',0,'manager','Maliyyə Meneceri','','',NULL,'','',1,'2025-10-10 15:54:57.561516',NULL,92,'2025-10-16 13:24:16.653600',NULL,'~',3,NULL,2);
INSERT INTO "accounts_historicaluser" VALUES(10,'pbkdf2_sha256$870000$LowPGlRzHG6dB7Q07nnzgP$rFaWQQQKLuI7zfx/+zEkEgasSPV8grb82iQ81Ysc+v4=',0,'aynur','Aynur','Əliyeva','aynur@q360.az',0,'employee','HR Mütəxəssisi','','',NULL,'','',1,'2025-10-10 15:54:57.891311',NULL,93,'2025-10-16 13:24:16.685081',NULL,'~',1,NULL,7);
INSERT INTO "accounts_historicaluser" VALUES(11,'pbkdf2_sha256$870000$F8UpUBMAjn3nyIBZohXgLg$+cNXk5KuEBB+P5G4aj5CP6e0BlMwQ/CqC3uy2Yh9sYA=',0,'kamran','Kamran','Əliyev','kamran@q360.az',0,'employee','HR Mütəxəssisi','','',NULL,'','',1,'2025-10-10 15:54:58.225285',NULL,94,'2025-10-16 13:24:16.714943',NULL,'~',1,NULL,7);
INSERT INTO "accounts_historicaluser" VALUES(12,'pbkdf2_sha256$870000$EHa9dh9uU7XAXfxQoKo8tV$db/TZ7H6kGp5zgCbT2+IiMWST7Y9fJJQui0RTASihzc=',0,'elchin','Elçin','Həsənov','elchin@q360.az',0,'employee','Proqramçı','','',NULL,'','',1,'2025-10-10 15:54:58.557737',NULL,95,'2025-10-16 13:24:16.744693',NULL,'~',2,NULL,8);
INSERT INTO "accounts_historicaluser" VALUES(13,'pbkdf2_sha256$870000$oYKCeYEPIcZSbLav2rdBPx$vJypvbZPNFu9HXdxHlJuV5jAc/ZZjqoG0QRA80Xo8mg=',0,'gunel','Günəl','İsmayılova','gunel@q360.az',0,'employee','Proqramçı','','',NULL,'','',1,'2025-10-10 15:54:58.886818',NULL,96,'2025-10-16 13:24:16.773309',NULL,'~',2,NULL,8);
INSERT INTO "accounts_historicaluser" VALUES(14,'pbkdf2_sha256$870000$wjZNsgN3wwx3rDGOrnUwoy$6hR78tM8sVPy2uk8zt54Uq3lFGSnVJ41R0EtimcxTQk=',0,'nigar','Nigar','Məmmədova','nigar@q360.az',0,'employee','Sistem Administratoru','','',NULL,'','',1,'2025-10-10 15:54:59.224189',NULL,97,'2025-10-16 13:24:16.802381',NULL,'~',2,NULL,8);
INSERT INTO "accounts_historicaluser" VALUES(15,'pbkdf2_sha256$870000$DvVPlXGgbDc4W9qF5LJOEI$bhKZtPlXl8Kwug5zLnEHCkDsTP99TwjU5hl4NSMTHqc=',0,'farid','Farid','Abdullayev','farid@q360.az',0,'employee','Mühasib','','',NULL,'profiles/amal.jpg','',1,'2025-10-10 15:54:59.562356','2025-10-10 21:09:40.899180',98,'2025-10-16 13:24:16.833469',NULL,'~',4,NULL,2);
INSERT INTO "accounts_historicaluser" VALUES(16,'pbkdf2_sha256$870000$rRG52Kr18fg2dXo36588Al$G7EGbwJ0NVUILeLXSCi/wpr3WrMOXoxDT4UDpFb5HLo=',0,'sevinc','Sevinc','Qasımova','sevinc@q360.az',0,'employee','Mühasib','','',NULL,'','',1,'2025-10-10 15:54:59.911287',NULL,99,'2025-10-16 13:24:16.863728',NULL,'~',3,NULL,9);
INSERT INTO "accounts_historicaluser" VALUES(17,'pbkdf2_sha256$870000$k7nLd6WSmzCPJnxCLQEyDs$Klws9xTaoB1d0SORyr6qa/9yjmDxXY2kCb9v1IYbpB0=',0,'tural','Tural','Cəfərov','tural@q360.az',0,'employee','Hüquqşünas','','',NULL,'','',1,'2025-10-10 15:55:00.234951',NULL,100,'2025-10-16 13:24:16.897172',NULL,'~',4,NULL,2);
INSERT INTO "accounts_historicaluser" VALUES(18,'pbkdf2_sha256$870000$yXrrUM7OFt8UL5SpiC4vCg$o+xhOvj39bdOxUXf/Dz2xJcI7NvbDIGbKl9pdMBkPA4=',0,'aysel','Aysel','Rəhimova','aysel@q360.az',0,'employee','PR Mütəxəssisi','','',NULL,'','',1,'2025-10-10 15:55:00.569894',NULL,101,'2025-10-16 13:24:16.930539',NULL,'~',5,NULL,2);
INSERT INTO "accounts_historicaluser" VALUES(19,'pbkdf2_sha256$870000$cWNOca0FFuNObv3ZYRlQ6R$5U06si/aAYSwGeLDNurAYwC6/qqFJFkERJTb7h37n7M=',0,'murad','Murad','Süleymanov','murad@q360.az',0,'employee','PR Mütəxəssisi','','','0003','','',1,'2025-10-10 15:55:00.897865',NULL,102,'2025-10-16 13:24:16.960256',NULL,'~',5,NULL,2);
INSERT INTO "accounts_historicaluser" VALUES(7,'pbkdf2_sha256$870000$8JpYXlPFZgePktgqH0vtAO$MeSwek6Npsj30YxqL2plcKTpmA8ePuUWjo4osP26lIA=',0,'rashad','Rəşad','Məmmədov','rashad@q360.az',0,'manager','HR Meneceri','','',NULL,'','',1,'2025-10-10 15:54:56.903567',NULL,103,'2025-10-16 13:40:16.455080',NULL,'~',1,NULL,2);
INSERT INTO "accounts_historicaluser" VALUES(8,'pbkdf2_sha256$870000$T0w0YxwXnhO7W44xdwNiAn$2dnZEKfcWBiE8CpDki/cnCi/CJvPdzd4zM23oAbObyU=',0,'elvin','Elvin','Quliyev','elvin@q360.az',0,'manager','IT Meneceri','','',NULL,'','',1,'2025-10-10 15:54:57.238382',NULL,104,'2025-10-16 13:40:16.487079',NULL,'~',2,NULL,2);
INSERT INTO "accounts_historicaluser" VALUES(9,'pbkdf2_sha256$870000$SiqYfQdaFK7M6QfmgScyF8$vXbrwzzSk3HI9J/Z+jVsPhY5zooxzZY8/Tb8MqQayuA=',0,'leyla','Leyla','Həsənova','leyla@q360.az',0,'manager','Maliyyə Meneceri','','',NULL,'','',1,'2025-10-10 15:54:57.561516',NULL,105,'2025-10-16 13:40:16.518436',NULL,'~',3,NULL,2);
INSERT INTO "accounts_historicaluser" VALUES(10,'pbkdf2_sha256$870000$LowPGlRzHG6dB7Q07nnzgP$rFaWQQQKLuI7zfx/+zEkEgasSPV8grb82iQ81Ysc+v4=',0,'aynur','Aynur','Əliyeva','aynur@q360.az',0,'employee','HR Mütəxəssisi','','',NULL,'','',1,'2025-10-10 15:54:57.891311',NULL,106,'2025-10-16 13:40:16.550698',NULL,'~',1,NULL,7);
INSERT INTO "accounts_historicaluser" VALUES(11,'pbkdf2_sha256$870000$F8UpUBMAjn3nyIBZohXgLg$+cNXk5KuEBB+P5G4aj5CP6e0BlMwQ/CqC3uy2Yh9sYA=',0,'kamran','Kamran','Əliyev','kamran@q360.az',0,'employee','HR Mütəxəssisi','','',NULL,'','',1,'2025-10-10 15:54:58.225285',NULL,107,'2025-10-16 13:40:16.582111',NULL,'~',1,NULL,7);
INSERT INTO "accounts_historicaluser" VALUES(12,'pbkdf2_sha256$870000$EHa9dh9uU7XAXfxQoKo8tV$db/TZ7H6kGp5zgCbT2+IiMWST7Y9fJJQui0RTASihzc=',0,'elchin','Elçin','Həsənov','elchin@q360.az',0,'employee','Proqramçı','','',NULL,'','',1,'2025-10-10 15:54:58.557737',NULL,108,'2025-10-16 13:40:16.614258',NULL,'~',2,NULL,8);
INSERT INTO "accounts_historicaluser" VALUES(13,'pbkdf2_sha256$870000$oYKCeYEPIcZSbLav2rdBPx$vJypvbZPNFu9HXdxHlJuV5jAc/ZZjqoG0QRA80Xo8mg=',0,'gunel','Günəl','İsmayılova','gunel@q360.az',0,'employee','Proqramçı','','',NULL,'','',1,'2025-10-10 15:54:58.886818',NULL,109,'2025-10-16 13:40:16.645608',NULL,'~',2,NULL,8);
INSERT INTO "accounts_historicaluser" VALUES(14,'pbkdf2_sha256$870000$wjZNsgN3wwx3rDGOrnUwoy$6hR78tM8sVPy2uk8zt54Uq3lFGSnVJ41R0EtimcxTQk=',0,'nigar','Nigar','Məmmədova','nigar@q360.az',0,'employee','Sistem Administratoru','','',NULL,'','',1,'2025-10-10 15:54:59.224189',NULL,110,'2025-10-16 13:40:16.676447',NULL,'~',2,NULL,8);
INSERT INTO "accounts_historicaluser" VALUES(15,'pbkdf2_sha256$870000$DvVPlXGgbDc4W9qF5LJOEI$bhKZtPlXl8Kwug5zLnEHCkDsTP99TwjU5hl4NSMTHqc=',0,'farid','Farid','Abdullayev','farid@q360.az',0,'employee','Mühasib','','',NULL,'profiles/amal.jpg','',1,'2025-10-10 15:54:59.562356','2025-10-10 21:09:40.899180',111,'2025-10-16 13:40:16.709574',NULL,'~',4,NULL,2);
INSERT INTO "accounts_historicaluser" VALUES(16,'pbkdf2_sha256$870000$rRG52Kr18fg2dXo36588Al$G7EGbwJ0NVUILeLXSCi/wpr3WrMOXoxDT4UDpFb5HLo=',0,'sevinc','Sevinc','Qasımova','sevinc@q360.az',0,'employee','Mühasib','','',NULL,'','',1,'2025-10-10 15:54:59.911287',NULL,112,'2025-10-16 13:40:16.742961',NULL,'~',3,NULL,9);
INSERT INTO "accounts_historicaluser" VALUES(17,'pbkdf2_sha256$870000$k7nLd6WSmzCPJnxCLQEyDs$Klws9xTaoB1d0SORyr6qa/9yjmDxXY2kCb9v1IYbpB0=',0,'tural','Tural','Cəfərov','tural@q360.az',0,'employee','Hüquqşünas','','',NULL,'','',1,'2025-10-10 15:55:00.234951',NULL,113,'2025-10-16 13:40:16.776815',NULL,'~',4,NULL,2);
INSERT INTO "accounts_historicaluser" VALUES(18,'pbkdf2_sha256$870000$yXrrUM7OFt8UL5SpiC4vCg$o+xhOvj39bdOxUXf/Dz2xJcI7NvbDIGbKl9pdMBkPA4=',0,'aysel','Aysel','Rəhimova','aysel@q360.az',0,'employee','PR Mütəxəssisi','','',NULL,'','',1,'2025-10-10 15:55:00.569894',NULL,114,'2025-10-16 13:40:16.810712',NULL,'~',5,NULL,2);
INSERT INTO "accounts_historicaluser" VALUES(19,'pbkdf2_sha256$870000$cWNOca0FFuNObv3ZYRlQ6R$5U06si/aAYSwGeLDNurAYwC6/qqFJFkERJTb7h37n7M=',0,'murad','Murad','Süleymanov','murad@q360.az',0,'employee','PR Mütəxəssisi','','','0003','','',1,'2025-10-10 15:55:00.897865',NULL,115,'2025-10-16 13:40:16.843096',NULL,'~',5,NULL,2);
INSERT INTO "accounts_historicaluser" VALUES(30,'pbkdf2_sha256$870000$8Cw6s97bAWo32dZOK8bc7H$dg4rRgAkWhdtLA/NF/lBpDRszrBBtOUyCVQaJl7sX/Y=',0,'tako','Tariyel','Vəliyev','tako01@gmail.com',0,'employee','Kassir','Aftandil','+994511231212',NULL,'','',1,'2025-10-16 16:35:53.327566',NULL,116,'2025-10-16 16:35:53.342415',NULL,'+',3,NULL,NULL);
INSERT INTO "accounts_historicaluser" VALUES(30,'pbkdf2_sha256$870000$8Cw6s97bAWo32dZOK8bc7H$dg4rRgAkWhdtLA/NF/lBpDRszrBBtOUyCVQaJl7sX/Y=',0,'tako','Tariyel','Vəliyev','tako01@gmail.com',0,'employee','Kassir','Aftandil','+994511231212',NULL,'','',1,'2025-10-16 16:35:53.327566','2025-10-16 16:36:09.677024',117,'2025-10-16 16:36:09.687853',NULL,'~',3,30,NULL);
INSERT INTO "accounts_historicaluser" VALUES(1,'pbkdf2_sha256$870000$55Rtqbij2pb2iQmfZSlwaw$f4jkRvmNoWoMMg7opXGVH2yc58BqLEoyyHI98r6NkoA=',1,'Tahmaz','Tahmaz','Muradov','admin@q360.gov.az',1,'superadmin','müdür','Seyran','0605536990','0001','profiles/IMG-20250426-WA0048_bsVsgAX.jpg','Tahmaz',1,'2025-10-09 06:34:12.095047','2025-10-16 16:39:10.665767',118,'2025-10-16 16:39:10.674393',NULL,'~',2,1,1);
INSERT INTO "accounts_historicaluser" VALUES(1,'pbkdf2_sha256$870000$55Rtqbij2pb2iQmfZSlwaw$f4jkRvmNoWoMMg7opXGVH2yc58BqLEoyyHI98r6NkoA=',1,'Tahmaz','Tahmaz','Muradov','admin@q360.gov.az',1,'superadmin','müdür','Seyran','0605536990','0001','profiles/IMG-20250426-WA0048_bsVsgAX.jpg','Tahmaz',1,'2025-10-09 06:34:12.095047','2025-10-16 18:52:11.438267',119,'2025-10-16 18:52:11.445297',NULL,'~',2,1,1);
INSERT INTO "accounts_historicaluser" VALUES(1,'pbkdf2_sha256$870000$55Rtqbij2pb2iQmfZSlwaw$f4jkRvmNoWoMMg7opXGVH2yc58BqLEoyyHI98r6NkoA=',1,'Tahmaz','Tahmaz','Muradov','admin@q360.gov.az',1,'superadmin','müdür','','0605536990','0001','profiles/IMG-20250426-WA0048_bsVsgAX.jpg','Tahmaz',1,'2025-10-09 06:34:12.095047','2025-10-16 18:52:11.438267',120,'2025-10-16 21:21:23.144211',NULL,'~',2,1,1);
INSERT INTO "accounts_historicaluser" VALUES(31,'',0,'test_notification_user','Test','User','test@example.com',0,'employee','','','',NULL,'','',1,'2025-10-17 17:11:47.855244',NULL,121,'2025-10-17 17:11:47.859633',NULL,'+',NULL,NULL,NULL);
INSERT INTO "accounts_historicaluser" VALUES(31,'pbkdf2_sha256$870000$t9gVruLliJM1RmOoSUsF4v$XatZyf8H6fqxmMgiX2bT7m4ML7u49pSHNWPju0WG3B8=',0,'test_notification_user','Test','User','test@example.com',0,'employee','','','',NULL,'','',1,'2025-10-17 17:11:47.855244',NULL,122,'2025-10-17 17:11:48.193406',NULL,'~',NULL,NULL,NULL);
INSERT INTO "accounts_historicaluser" VALUES(32,'pbkdf2_sha256$870000$I6aSIJxylN03nU8Hr5ooHe$nNumtsNfY0wZGBJicqapwUJsISSGz7cpgWKgebB6wXs=',0,'debug_admin','Admin','User','admin@example.com',0,'admin','','','',NULL,'','',1,'2025-10-17 18:51:01.904370',NULL,123,'2025-10-17 18:51:01.913442',NULL,'+',11,NULL,NULL);
INSERT INTO "accounts_historicaluser" VALUES(32,'pbkdf2_sha256$870000$I6aSIJxylN03nU8Hr5ooHe$nNumtsNfY0wZGBJicqapwUJsISSGz7cpgWKgebB6wXs=',0,'debug_admin','Admin','User','admin@example.com',1,'admin','','','',NULL,'','',1,'2025-10-17 18:51:01.904370',NULL,124,'2025-10-17 18:51:01.970315',NULL,'~',11,NULL,NULL);
INSERT INTO "accounts_historicaluser" VALUES(33,'pbkdf2_sha256$870000$cLbOYUAHmTKmlPF03RlWI8$gQa9cLwz5R20neHnhQRFYVLcnoTiNdATLjYxxdqNf5E=',0,'debug_employee','Emp','Loyee','emp@example.com',0,'employee','','','',NULL,'','',1,'2025-10-17 18:51:02.281796',NULL,125,'2025-10-17 18:51:02.290920',NULL,'+',11,NULL,NULL);
INSERT INTO "accounts_historicaluser" VALUES(33,'pbkdf2_sha256$870000$cLbOYUAHmTKmlPF03RlWI8$gQa9cLwz5R20neHnhQRFYVLcnoTiNdATLjYxxdqNf5E=',0,'debug_employee','Emp','Loyee','emp@example.com',0,'employee','','','',NULL,'','',1,'2025-10-17 18:51:02.281796',NULL,126,'2025-10-17 18:51:02.333687',NULL,'~',11,NULL,NULL);
INSERT INTO "accounts_historicaluser" VALUES(32,'pbkdf2_sha256$870000$I6aSIJxylN03nU8Hr5ooHe$nNumtsNfY0wZGBJicqapwUJsISSGz7cpgWKgebB6wXs=',0,'debug_admin','Admin','User','admin@example.com',1,'admin','','','',NULL,'','',1,'2025-10-17 18:51:01.904370','2025-10-17 18:51:02.694795',127,'2025-10-17 18:51:02.701182',NULL,'~',11,NULL,NULL);
INSERT INTO "accounts_historicaluser" VALUES(34,'pbkdf2_sha256$870000$c76It1qLbYL6BQWBA45iZW$d6H9NeQqFKXbR2AIRuaQKg6SijtVUyKDbQfjMzNBapI=',0,'dash_user','','','',0,'admin','','','',NULL,'','',1,'2025-10-17 19:11:19.080363',NULL,128,'2025-10-17 19:11:19.097244',NULL,'+',12,NULL,NULL);
INSERT INTO "accounts_historicaluser" VALUES(34,'pbkdf2_sha256$870000$c76It1qLbYL6BQWBA45iZW$d6H9NeQqFKXbR2AIRuaQKg6SijtVUyKDbQfjMzNBapI=',0,'dash_user','','','',1,'admin','','','',NULL,'','',1,'2025-10-17 19:11:19.080363',NULL,129,'2025-10-17 19:11:19.215559',NULL,'~',12,NULL,NULL);
INSERT INTO "accounts_historicaluser" VALUES(34,'pbkdf2_sha256$870000$c76It1qLbYL6BQWBA45iZW$d6H9NeQqFKXbR2AIRuaQKg6SijtVUyKDbQfjMzNBapI=',0,'dash_user','','','',1,'admin','','','',NULL,'','',1,'2025-10-17 19:11:19.080363','2025-10-17 19:11:19.948880',130,'2025-10-17 19:11:19.960072',NULL,'~',12,NULL,NULL);
CREATE TABLE "accounts_historicalworkhistory" ("id" bigint NOT NULL, "change_type" varchar(50) NOT NULL, "effective_date" date NOT NULL, "old_position" varchar(200) NOT NULL, "new_position" varchar(200) NOT NULL, "reason" text NOT NULL, "notes" text NOT NULL, "created_at" datetime NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "approved_by_id" bigint NULL, "created_by_id" bigint NULL, "history_user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "new_department_id" bigint NULL, "old_department_id" bigint NULL, "user_id" bigint NULL);
CREATE TABLE "accounts_profile" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "date_of_birth" date NULL, "hire_date" date NULL, "education_level" varchar(100) NOT NULL, "specialization" varchar(200) NOT NULL, "work_email" varchar(254) NOT NULL, "work_phone" varchar(20) NOT NULL, "address" text NOT NULL, "language_preference" varchar(10) NOT NULL, "email_notifications" bool NOT NULL, "sms_notifications" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "user_id" bigint NOT NULL UNIQUE REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "city" varchar(100) NOT NULL, "contract_end_date" date NULL, "contract_start_date" date NULL, "contract_type" varchar(50) NOT NULL, "emergency_contact_name" varchar(200) NOT NULL, "emergency_contact_phone" varchar(20) NOT NULL, "emergency_contact_relationship" varchar(100) NOT NULL, "graduation_year" integer unsigned NULL CHECK ("graduation_year" >= 0), "health_insurance_number" varchar(100) NOT NULL, "health_insurance_provider" varchar(200) NOT NULL, "marital_status" varchar(20) NOT NULL, "national_id" varchar(50) NOT NULL, "nationality" varchar(100) NOT NULL, "number_of_children" integer unsigned NOT NULL CHECK ("number_of_children" >= 0), "pension_insurance_number" varchar(100) NOT NULL, "personal_email" varchar(254) NOT NULL, "personal_phone" varchar(20) NOT NULL, "place_of_birth" varchar(200) NOT NULL, "postal_code" varchar(20) NOT NULL, "probation_end_date" date NULL, "tax_id" varchar(50) NOT NULL, "termination_date" date NULL, "termination_reason" text NOT NULL, "university" varchar(200) NOT NULL);
INSERT INTO "accounts_profile" VALUES(1,NULL,'2025-10-09','','İT','muradoffcode@gmail.com','0605536990','Nakhchivan City
Nakhchivan City','az',1,0,'2025-10-09 06:34:12.114500','2025-10-16 21:21:23.152665',1,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_profile" VALUES(2,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:39:44.540839','2025-10-10 15:39:44.548901',2,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_profile" VALUES(3,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:39:44.859181','2025-10-10 15:39:44.866932',3,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_profile" VALUES(4,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:39:45.173928','2025-10-10 15:39:45.180596',4,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_profile" VALUES(5,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:39:45.492251','2025-10-10 15:39:45.499655',5,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_profile" VALUES(6,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:39:45.818591','2025-10-10 15:39:45.825908',6,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_profile" VALUES(7,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:56.921316','2025-10-16 13:40:16.464519',7,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_profile" VALUES(8,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:57.256400','2025-10-16 13:40:16.495630',8,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_profile" VALUES(9,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:57.577120','2025-10-16 13:40:16.527240',9,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_profile" VALUES(10,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:57.909668','2025-10-16 13:40:16.559966',10,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_profile" VALUES(11,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:58.243019','2025-10-16 13:40:16.591303',11,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_profile" VALUES(12,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:58.575053','2025-10-16 13:40:16.623247',12,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_profile" VALUES(13,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:58.902725','2025-10-16 13:40:16.654196',13,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_profile" VALUES(14,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:59.242331','2025-10-16 13:40:16.686641',14,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_profile" VALUES(15,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:59.581247','2025-10-16 13:40:16.718474',15,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_profile" VALUES(16,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:54:59.928557','2025-10-16 13:40:16.751714',16,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_profile" VALUES(17,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:55:00.251437','2025-10-16 13:40:16.785972',17,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_profile" VALUES(18,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:55:00.587340','2025-10-16 13:40:16.819462',18,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_profile" VALUES(19,NULL,NULL,'','','','','','az',1,0,'2025-10-10 15:55:00.916312','2025-10-16 13:40:16.852416',19,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_profile" VALUES(20,NULL,NULL,'','','','','','az',1,0,'2025-10-11 19:13:57.033655','2025-10-14 22:17:55.674264',20,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_profile" VALUES(21,NULL,NULL,'','','','','','az',1,0,'2025-10-15 07:47:47.375179','2025-10-15 07:47:47.775881',21,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_profile" VALUES(22,NULL,NULL,'','','','','','az',1,0,'2025-10-15 07:47:47.825362','2025-10-15 07:47:48.198514',22,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_profile" VALUES(23,NULL,NULL,'','','','','','az',1,0,'2025-10-15 07:47:48.220389','2025-10-15 07:47:48.611812',23,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_profile" VALUES(24,NULL,NULL,'','','','','','az',1,0,'2025-10-15 07:58:54.016903','2025-10-15 07:58:54.052435',24,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_profile" VALUES(25,NULL,NULL,'','','','','','az',1,0,'2025-10-15 07:58:54.364673','2025-10-15 07:58:54.398228',25,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_profile" VALUES(26,NULL,NULL,'','','','','','az',1,0,'2025-10-15 07:58:54.716263','2025-10-15 07:58:54.755624',26,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_profile" VALUES(27,NULL,NULL,'','','','','','az',1,0,'2025-10-15 07:58:55.088957','2025-10-15 07:58:55.126553',27,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_profile" VALUES(28,NULL,NULL,'','','','','','az',1,0,'2025-10-15 07:58:55.440704','2025-10-15 07:58:55.447306',28,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_profile" VALUES(29,NULL,NULL,'','','','','','az',1,0,'2025-10-15 07:58:55.760786','2025-10-15 07:58:55.795573',29,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_profile" VALUES(30,'2025-10-01',NULL,'','','','','','az',1,0,'2025-10-16 16:35:53.360471','2025-10-16 16:36:09.701906',30,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_profile" VALUES(31,NULL,NULL,'','','','','','az',1,0,'2025-10-17 17:11:47.864018','2025-10-17 17:11:48.201047',31,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_profile" VALUES(32,NULL,NULL,'','','','','','az',1,0,'2025-10-17 18:51:01.922460','2025-10-17 18:51:02.709496',32,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_profile" VALUES(33,NULL,NULL,'','','','','','az',1,0,'2025-10-17 18:51:02.299230','2025-10-17 18:51:02.341412',33,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
INSERT INTO "accounts_profile" VALUES(34,NULL,NULL,'','','','','','az',1,0,'2025-10-17 19:11:19.118121','2025-10-17 19:11:19.980383',34,'',NULL,NULL,'permanent','','','',NULL,'','','','','',0,'','','','','',NULL,'',NULL,'','');
CREATE TABLE "accounts_role" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(50) NOT NULL UNIQUE, "display_name" varchar(100) NOT NULL, "description" text NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL);
INSERT INTO "accounts_role" VALUES(1,'superadmin','baş admin','','2025-10-09 06:46:54.247720','2025-10-10 20:48:20.504550');
INSERT INTO "accounts_role" VALUES(2,'employee','İşçi','','2025-10-10 21:06:01.868478','2025-10-10 21:06:01.868551');
INSERT INTO "accounts_role" VALUES(3,'admin','Admin','','2025-10-10 21:06:28.207986','2025-10-10 21:06:28.208009');
INSERT INTO "accounts_role" VALUES(4,'manager','Rəhbər','','2025-10-10 21:07:05.999881','2025-10-10 21:07:05.999905');
CREATE TABLE "accounts_role_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "role_id" bigint NOT NULL REFERENCES "accounts_role" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "accounts_role_permissions" VALUES(1,1,1);
INSERT INTO "accounts_role_permissions" VALUES(2,1,2);
INSERT INTO "accounts_role_permissions" VALUES(3,1,3);
INSERT INTO "accounts_role_permissions" VALUES(4,1,4);
INSERT INTO "accounts_role_permissions" VALUES(5,1,5);
INSERT INTO "accounts_role_permissions" VALUES(6,1,6);
INSERT INTO "accounts_role_permissions" VALUES(7,1,7);
INSERT INTO "accounts_role_permissions" VALUES(8,1,8);
INSERT INTO "accounts_role_permissions" VALUES(9,1,9);
INSERT INTO "accounts_role_permissions" VALUES(10,1,10);
INSERT INTO "accounts_role_permissions" VALUES(11,1,11);
INSERT INTO "accounts_role_permissions" VALUES(12,1,12);
INSERT INTO "accounts_role_permissions" VALUES(13,1,13);
INSERT INTO "accounts_role_permissions" VALUES(14,1,14);
INSERT INTO "accounts_role_permissions" VALUES(15,1,15);
INSERT INTO "accounts_role_permissions" VALUES(16,1,16);
INSERT INTO "accounts_role_permissions" VALUES(17,1,17);
INSERT INTO "accounts_role_permissions" VALUES(18,1,18);
INSERT INTO "accounts_role_permissions" VALUES(19,1,19);
INSERT INTO "accounts_role_permissions" VALUES(20,1,20);
INSERT INTO "accounts_role_permissions" VALUES(21,1,21);
INSERT INTO "accounts_role_permissions" VALUES(22,1,22);
INSERT INTO "accounts_role_permissions" VALUES(23,1,23);
INSERT INTO "accounts_role_permissions" VALUES(24,1,24);
INSERT INTO "accounts_role_permissions" VALUES(25,1,25);
INSERT INTO "accounts_role_permissions" VALUES(26,1,26);
INSERT INTO "accounts_role_permissions" VALUES(27,1,27);
INSERT INTO "accounts_role_permissions" VALUES(28,1,28);
INSERT INTO "accounts_role_permissions" VALUES(29,1,29);
INSERT INTO "accounts_role_permissions" VALUES(30,1,30);
INSERT INTO "accounts_role_permissions" VALUES(31,1,31);
INSERT INTO "accounts_role_permissions" VALUES(32,1,32);
INSERT INTO "accounts_role_permissions" VALUES(33,1,33);
INSERT INTO "accounts_role_permissions" VALUES(34,1,34);
INSERT INTO "accounts_role_permissions" VALUES(35,1,35);
INSERT INTO "accounts_role_permissions" VALUES(36,1,36);
INSERT INTO "accounts_role_permissions" VALUES(37,1,37);
INSERT INTO "accounts_role_permissions" VALUES(38,1,38);
INSERT INTO "accounts_role_permissions" VALUES(39,1,39);
INSERT INTO "accounts_role_permissions" VALUES(40,1,40);
INSERT INTO "accounts_role_permissions" VALUES(41,1,41);
INSERT INTO "accounts_role_permissions" VALUES(42,1,42);
INSERT INTO "accounts_role_permissions" VALUES(43,1,43);
INSERT INTO "accounts_role_permissions" VALUES(44,1,44);
INSERT INTO "accounts_role_permissions" VALUES(45,1,45);
INSERT INTO "accounts_role_permissions" VALUES(46,1,46);
INSERT INTO "accounts_role_permissions" VALUES(47,1,47);
INSERT INTO "accounts_role_permissions" VALUES(48,1,48);
INSERT INTO "accounts_role_permissions" VALUES(49,1,49);
INSERT INTO "accounts_role_permissions" VALUES(50,1,50);
INSERT INTO "accounts_role_permissions" VALUES(51,1,51);
INSERT INTO "accounts_role_permissions" VALUES(52,1,52);
INSERT INTO "accounts_role_permissions" VALUES(53,1,53);
INSERT INTO "accounts_role_permissions" VALUES(54,1,54);
INSERT INTO "accounts_role_permissions" VALUES(55,1,55);
INSERT INTO "accounts_role_permissions" VALUES(56,1,56);
INSERT INTO "accounts_role_permissions" VALUES(57,1,57);
INSERT INTO "accounts_role_permissions" VALUES(58,1,58);
INSERT INTO "accounts_role_permissions" VALUES(59,1,59);
INSERT INTO "accounts_role_permissions" VALUES(60,1,60);
INSERT INTO "accounts_role_permissions" VALUES(61,1,61);
INSERT INTO "accounts_role_permissions" VALUES(62,1,62);
INSERT INTO "accounts_role_permissions" VALUES(63,1,63);
INSERT INTO "accounts_role_permissions" VALUES(64,1,64);
INSERT INTO "accounts_role_permissions" VALUES(65,1,65);
INSERT INTO "accounts_role_permissions" VALUES(66,1,66);
INSERT INTO "accounts_role_permissions" VALUES(67,1,67);
INSERT INTO "accounts_role_permissions" VALUES(68,1,68);
INSERT INTO "accounts_role_permissions" VALUES(69,1,69);
INSERT INTO "accounts_role_permissions" VALUES(70,1,70);
INSERT INTO "accounts_role_permissions" VALUES(71,1,71);
INSERT INTO "accounts_role_permissions" VALUES(72,1,72);
INSERT INTO "accounts_role_permissions" VALUES(73,1,73);
INSERT INTO "accounts_role_permissions" VALUES(74,1,74);
INSERT INTO "accounts_role_permissions" VALUES(75,1,75);
INSERT INTO "accounts_role_permissions" VALUES(76,1,76);
INSERT INTO "accounts_role_permissions" VALUES(77,1,77);
INSERT INTO "accounts_role_permissions" VALUES(78,1,78);
INSERT INTO "accounts_role_permissions" VALUES(79,1,79);
INSERT INTO "accounts_role_permissions" VALUES(80,1,80);
INSERT INTO "accounts_role_permissions" VALUES(81,1,81);
INSERT INTO "accounts_role_permissions" VALUES(82,1,82);
INSERT INTO "accounts_role_permissions" VALUES(83,1,83);
INSERT INTO "accounts_role_permissions" VALUES(84,1,84);
INSERT INTO "accounts_role_permissions" VALUES(85,1,85);
INSERT INTO "accounts_role_permissions" VALUES(86,1,86);
INSERT INTO "accounts_role_permissions" VALUES(87,1,87);
INSERT INTO "accounts_role_permissions" VALUES(88,1,88);
INSERT INTO "accounts_role_permissions" VALUES(89,1,89);
INSERT INTO "accounts_role_permissions" VALUES(90,1,90);
INSERT INTO "accounts_role_permissions" VALUES(91,1,91);
INSERT INTO "accounts_role_permissions" VALUES(92,1,92);
INSERT INTO "accounts_role_permissions" VALUES(93,1,93);
INSERT INTO "accounts_role_permissions" VALUES(94,1,94);
INSERT INTO "accounts_role_permissions" VALUES(95,1,95);
INSERT INTO "accounts_role_permissions" VALUES(96,1,96);
INSERT INTO "accounts_role_permissions" VALUES(97,1,97);
INSERT INTO "accounts_role_permissions" VALUES(98,1,98);
INSERT INTO "accounts_role_permissions" VALUES(99,1,99);
INSERT INTO "accounts_role_permissions" VALUES(100,1,100);
INSERT INTO "accounts_role_permissions" VALUES(101,1,101);
INSERT INTO "accounts_role_permissions" VALUES(102,1,102);
INSERT INTO "accounts_role_permissions" VALUES(103,1,103);
INSERT INTO "accounts_role_permissions" VALUES(104,1,104);
INSERT INTO "accounts_role_permissions" VALUES(105,1,105);
INSERT INTO "accounts_role_permissions" VALUES(106,1,106);
INSERT INTO "accounts_role_permissions" VALUES(107,1,107);
INSERT INTO "accounts_role_permissions" VALUES(108,1,108);
INSERT INTO "accounts_role_permissions" VALUES(109,1,109);
INSERT INTO "accounts_role_permissions" VALUES(110,1,110);
INSERT INTO "accounts_role_permissions" VALUES(111,1,111);
INSERT INTO "accounts_role_permissions" VALUES(112,1,112);
INSERT INTO "accounts_role_permissions" VALUES(113,1,113);
INSERT INTO "accounts_role_permissions" VALUES(114,1,114);
INSERT INTO "accounts_role_permissions" VALUES(115,1,115);
INSERT INTO "accounts_role_permissions" VALUES(116,1,116);
INSERT INTO "accounts_role_permissions" VALUES(117,1,117);
INSERT INTO "accounts_role_permissions" VALUES(118,1,118);
INSERT INTO "accounts_role_permissions" VALUES(119,1,119);
INSERT INTO "accounts_role_permissions" VALUES(120,1,120);
INSERT INTO "accounts_role_permissions" VALUES(121,1,121);
INSERT INTO "accounts_role_permissions" VALUES(122,1,122);
INSERT INTO "accounts_role_permissions" VALUES(123,1,123);
INSERT INTO "accounts_role_permissions" VALUES(124,1,124);
INSERT INTO "accounts_role_permissions" VALUES(125,1,125);
INSERT INTO "accounts_role_permissions" VALUES(126,1,126);
INSERT INTO "accounts_role_permissions" VALUES(127,1,127);
INSERT INTO "accounts_role_permissions" VALUES(128,1,128);
INSERT INTO "accounts_role_permissions" VALUES(129,1,129);
INSERT INTO "accounts_role_permissions" VALUES(130,1,130);
INSERT INTO "accounts_role_permissions" VALUES(131,1,131);
INSERT INTO "accounts_role_permissions" VALUES(132,1,132);
INSERT INTO "accounts_role_permissions" VALUES(133,1,133);
INSERT INTO "accounts_role_permissions" VALUES(134,1,134);
INSERT INTO "accounts_role_permissions" VALUES(135,1,135);
INSERT INTO "accounts_role_permissions" VALUES(136,1,136);
INSERT INTO "accounts_role_permissions" VALUES(137,1,137);
INSERT INTO "accounts_role_permissions" VALUES(138,1,138);
INSERT INTO "accounts_role_permissions" VALUES(139,1,139);
INSERT INTO "accounts_role_permissions" VALUES(140,1,140);
INSERT INTO "accounts_role_permissions" VALUES(141,1,141);
INSERT INTO "accounts_role_permissions" VALUES(142,1,142);
INSERT INTO "accounts_role_permissions" VALUES(143,1,143);
INSERT INTO "accounts_role_permissions" VALUES(144,1,144);
INSERT INTO "accounts_role_permissions" VALUES(145,2,32);
INSERT INTO "accounts_role_permissions" VALUES(146,3,1);
INSERT INTO "accounts_role_permissions" VALUES(147,3,2);
INSERT INTO "accounts_role_permissions" VALUES(148,3,3);
INSERT INTO "accounts_role_permissions" VALUES(149,3,4);
INSERT INTO "accounts_role_permissions" VALUES(150,3,5);
INSERT INTO "accounts_role_permissions" VALUES(151,3,6);
INSERT INTO "accounts_role_permissions" VALUES(152,3,7);
INSERT INTO "accounts_role_permissions" VALUES(153,3,8);
INSERT INTO "accounts_role_permissions" VALUES(154,3,9);
INSERT INTO "accounts_role_permissions" VALUES(155,3,10);
INSERT INTO "accounts_role_permissions" VALUES(156,3,11);
INSERT INTO "accounts_role_permissions" VALUES(157,3,12);
INSERT INTO "accounts_role_permissions" VALUES(158,3,13);
INSERT INTO "accounts_role_permissions" VALUES(159,3,14);
INSERT INTO "accounts_role_permissions" VALUES(160,3,15);
INSERT INTO "accounts_role_permissions" VALUES(161,3,16);
INSERT INTO "accounts_role_permissions" VALUES(162,3,17);
INSERT INTO "accounts_role_permissions" VALUES(163,3,18);
INSERT INTO "accounts_role_permissions" VALUES(164,3,19);
INSERT INTO "accounts_role_permissions" VALUES(165,3,20);
INSERT INTO "accounts_role_permissions" VALUES(166,3,21);
INSERT INTO "accounts_role_permissions" VALUES(167,3,22);
INSERT INTO "accounts_role_permissions" VALUES(168,3,23);
INSERT INTO "accounts_role_permissions" VALUES(169,3,24);
INSERT INTO "accounts_role_permissions" VALUES(170,3,25);
INSERT INTO "accounts_role_permissions" VALUES(171,3,26);
INSERT INTO "accounts_role_permissions" VALUES(172,3,27);
INSERT INTO "accounts_role_permissions" VALUES(173,3,28);
INSERT INTO "accounts_role_permissions" VALUES(174,3,29);
INSERT INTO "accounts_role_permissions" VALUES(175,3,30);
INSERT INTO "accounts_role_permissions" VALUES(176,3,31);
INSERT INTO "accounts_role_permissions" VALUES(177,3,32);
INSERT INTO "accounts_role_permissions" VALUES(178,3,33);
INSERT INTO "accounts_role_permissions" VALUES(179,3,34);
INSERT INTO "accounts_role_permissions" VALUES(180,3,35);
INSERT INTO "accounts_role_permissions" VALUES(181,3,36);
INSERT INTO "accounts_role_permissions" VALUES(182,3,37);
INSERT INTO "accounts_role_permissions" VALUES(183,3,38);
INSERT INTO "accounts_role_permissions" VALUES(184,3,39);
INSERT INTO "accounts_role_permissions" VALUES(185,3,40);
INSERT INTO "accounts_role_permissions" VALUES(186,3,41);
INSERT INTO "accounts_role_permissions" VALUES(187,3,42);
INSERT INTO "accounts_role_permissions" VALUES(188,3,43);
INSERT INTO "accounts_role_permissions" VALUES(189,3,44);
INSERT INTO "accounts_role_permissions" VALUES(190,3,45);
INSERT INTO "accounts_role_permissions" VALUES(191,3,46);
INSERT INTO "accounts_role_permissions" VALUES(192,3,47);
INSERT INTO "accounts_role_permissions" VALUES(193,3,48);
INSERT INTO "accounts_role_permissions" VALUES(194,3,49);
INSERT INTO "accounts_role_permissions" VALUES(195,3,50);
INSERT INTO "accounts_role_permissions" VALUES(196,3,51);
INSERT INTO "accounts_role_permissions" VALUES(197,3,52);
INSERT INTO "accounts_role_permissions" VALUES(198,3,53);
INSERT INTO "accounts_role_permissions" VALUES(199,3,54);
INSERT INTO "accounts_role_permissions" VALUES(200,3,55);
INSERT INTO "accounts_role_permissions" VALUES(201,3,56);
INSERT INTO "accounts_role_permissions" VALUES(202,3,57);
INSERT INTO "accounts_role_permissions" VALUES(203,3,58);
INSERT INTO "accounts_role_permissions" VALUES(204,3,59);
INSERT INTO "accounts_role_permissions" VALUES(205,3,60);
INSERT INTO "accounts_role_permissions" VALUES(206,3,61);
INSERT INTO "accounts_role_permissions" VALUES(207,3,62);
INSERT INTO "accounts_role_permissions" VALUES(208,3,63);
INSERT INTO "accounts_role_permissions" VALUES(209,3,64);
INSERT INTO "accounts_role_permissions" VALUES(210,3,65);
INSERT INTO "accounts_role_permissions" VALUES(211,3,66);
INSERT INTO "accounts_role_permissions" VALUES(212,3,67);
INSERT INTO "accounts_role_permissions" VALUES(213,3,68);
INSERT INTO "accounts_role_permissions" VALUES(214,3,69);
INSERT INTO "accounts_role_permissions" VALUES(215,3,70);
INSERT INTO "accounts_role_permissions" VALUES(216,3,71);
INSERT INTO "accounts_role_permissions" VALUES(217,3,72);
INSERT INTO "accounts_role_permissions" VALUES(218,3,73);
INSERT INTO "accounts_role_permissions" VALUES(219,3,74);
INSERT INTO "accounts_role_permissions" VALUES(220,3,75);
INSERT INTO "accounts_role_permissions" VALUES(221,3,76);
INSERT INTO "accounts_role_permissions" VALUES(222,3,77);
INSERT INTO "accounts_role_permissions" VALUES(223,3,78);
INSERT INTO "accounts_role_permissions" VALUES(224,3,79);
INSERT INTO "accounts_role_permissions" VALUES(225,3,80);
INSERT INTO "accounts_role_permissions" VALUES(226,3,81);
INSERT INTO "accounts_role_permissions" VALUES(227,3,82);
INSERT INTO "accounts_role_permissions" VALUES(228,3,83);
INSERT INTO "accounts_role_permissions" VALUES(229,3,84);
INSERT INTO "accounts_role_permissions" VALUES(230,3,85);
INSERT INTO "accounts_role_permissions" VALUES(231,3,86);
INSERT INTO "accounts_role_permissions" VALUES(232,3,87);
INSERT INTO "accounts_role_permissions" VALUES(233,3,88);
INSERT INTO "accounts_role_permissions" VALUES(234,3,89);
INSERT INTO "accounts_role_permissions" VALUES(235,3,90);
INSERT INTO "accounts_role_permissions" VALUES(236,3,91);
INSERT INTO "accounts_role_permissions" VALUES(237,3,92);
INSERT INTO "accounts_role_permissions" VALUES(238,3,93);
INSERT INTO "accounts_role_permissions" VALUES(239,3,94);
INSERT INTO "accounts_role_permissions" VALUES(240,3,95);
INSERT INTO "accounts_role_permissions" VALUES(241,3,96);
INSERT INTO "accounts_role_permissions" VALUES(242,3,97);
INSERT INTO "accounts_role_permissions" VALUES(243,3,98);
INSERT INTO "accounts_role_permissions" VALUES(244,3,99);
INSERT INTO "accounts_role_permissions" VALUES(245,3,100);
INSERT INTO "accounts_role_permissions" VALUES(246,3,101);
INSERT INTO "accounts_role_permissions" VALUES(247,3,102);
INSERT INTO "accounts_role_permissions" VALUES(248,3,103);
INSERT INTO "accounts_role_permissions" VALUES(249,3,104);
INSERT INTO "accounts_role_permissions" VALUES(250,3,105);
INSERT INTO "accounts_role_permissions" VALUES(251,3,106);
INSERT INTO "accounts_role_permissions" VALUES(252,3,107);
INSERT INTO "accounts_role_permissions" VALUES(253,3,108);
INSERT INTO "accounts_role_permissions" VALUES(254,3,109);
INSERT INTO "accounts_role_permissions" VALUES(255,3,110);
INSERT INTO "accounts_role_permissions" VALUES(256,3,111);
INSERT INTO "accounts_role_permissions" VALUES(257,3,112);
INSERT INTO "accounts_role_permissions" VALUES(258,3,113);
INSERT INTO "accounts_role_permissions" VALUES(259,3,114);
INSERT INTO "accounts_role_permissions" VALUES(260,3,115);
INSERT INTO "accounts_role_permissions" VALUES(261,3,116);
INSERT INTO "accounts_role_permissions" VALUES(262,3,117);
INSERT INTO "accounts_role_permissions" VALUES(263,3,118);
INSERT INTO "accounts_role_permissions" VALUES(264,3,119);
INSERT INTO "accounts_role_permissions" VALUES(265,3,120);
INSERT INTO "accounts_role_permissions" VALUES(266,3,121);
INSERT INTO "accounts_role_permissions" VALUES(267,3,122);
INSERT INTO "accounts_role_permissions" VALUES(268,3,123);
INSERT INTO "accounts_role_permissions" VALUES(269,3,124);
INSERT INTO "accounts_role_permissions" VALUES(270,3,125);
INSERT INTO "accounts_role_permissions" VALUES(271,3,126);
INSERT INTO "accounts_role_permissions" VALUES(272,3,127);
INSERT INTO "accounts_role_permissions" VALUES(273,3,128);
INSERT INTO "accounts_role_permissions" VALUES(274,3,129);
INSERT INTO "accounts_role_permissions" VALUES(275,3,130);
INSERT INTO "accounts_role_permissions" VALUES(276,3,131);
INSERT INTO "accounts_role_permissions" VALUES(277,3,132);
INSERT INTO "accounts_role_permissions" VALUES(278,3,133);
INSERT INTO "accounts_role_permissions" VALUES(279,3,134);
INSERT INTO "accounts_role_permissions" VALUES(280,3,135);
INSERT INTO "accounts_role_permissions" VALUES(281,3,136);
INSERT INTO "accounts_role_permissions" VALUES(282,3,137);
INSERT INTO "accounts_role_permissions" VALUES(283,3,138);
INSERT INTO "accounts_role_permissions" VALUES(284,3,139);
INSERT INTO "accounts_role_permissions" VALUES(285,3,140);
INSERT INTO "accounts_role_permissions" VALUES(286,3,141);
INSERT INTO "accounts_role_permissions" VALUES(287,3,142);
INSERT INTO "accounts_role_permissions" VALUES(288,3,143);
INSERT INTO "accounts_role_permissions" VALUES(289,3,144);
INSERT INTO "accounts_role_permissions" VALUES(290,3,145);
INSERT INTO "accounts_role_permissions" VALUES(291,3,146);
INSERT INTO "accounts_role_permissions" VALUES(292,3,147);
INSERT INTO "accounts_role_permissions" VALUES(293,3,148);
INSERT INTO "accounts_role_permissions" VALUES(294,3,149);
INSERT INTO "accounts_role_permissions" VALUES(295,3,150);
INSERT INTO "accounts_role_permissions" VALUES(296,3,151);
INSERT INTO "accounts_role_permissions" VALUES(297,3,152);
INSERT INTO "accounts_role_permissions" VALUES(298,4,5);
INSERT INTO "accounts_role_permissions" VALUES(299,4,6);
INSERT INTO "accounts_role_permissions" VALUES(300,4,7);
INSERT INTO "accounts_role_permissions" VALUES(301,4,8);
INSERT INTO "accounts_role_permissions" VALUES(302,4,9);
INSERT INTO "accounts_role_permissions" VALUES(303,4,10);
INSERT INTO "accounts_role_permissions" VALUES(304,4,11);
INSERT INTO "accounts_role_permissions" VALUES(305,4,12);
INSERT INTO "accounts_role_permissions" VALUES(306,4,13);
INSERT INTO "accounts_role_permissions" VALUES(307,4,14);
INSERT INTO "accounts_role_permissions" VALUES(308,4,15);
INSERT INTO "accounts_role_permissions" VALUES(309,4,16);
INSERT INTO "accounts_role_permissions" VALUES(310,4,145);
INSERT INTO "accounts_role_permissions" VALUES(311,4,146);
INSERT INTO "accounts_role_permissions" VALUES(312,4,147);
INSERT INTO "accounts_role_permissions" VALUES(313,4,148);
INSERT INTO "accounts_role_permissions" VALUES(314,4,149);
INSERT INTO "accounts_role_permissions" VALUES(315,4,150);
INSERT INTO "accounts_role_permissions" VALUES(316,4,151);
INSERT INTO "accounts_role_permissions" VALUES(317,4,152);
INSERT INTO "accounts_role_permissions" VALUES(318,4,25);
INSERT INTO "accounts_role_permissions" VALUES(319,4,26);
INSERT INTO "accounts_role_permissions" VALUES(320,4,30);
INSERT INTO "accounts_role_permissions" VALUES(321,4,45);
INSERT INTO "accounts_role_permissions" VALUES(322,4,46);
INSERT INTO "accounts_role_permissions" VALUES(323,4,47);
INSERT INTO "accounts_role_permissions" VALUES(324,4,48);
INSERT INTO "accounts_role_permissions" VALUES(325,4,49);
INSERT INTO "accounts_role_permissions" VALUES(326,4,50);
INSERT INTO "accounts_role_permissions" VALUES(327,4,51);
CREATE TABLE "accounts_user" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "password" varchar(128) NOT NULL, "is_superuser" bool NOT NULL, "username" varchar(150) NOT NULL UNIQUE, "first_name" varchar(150) NOT NULL, "last_name" varchar(150) NOT NULL, "email" varchar(254) NOT NULL, "is_staff" bool NOT NULL, "role" varchar(20) NOT NULL, "position" varchar(100) NOT NULL, "middle_name" varchar(150) NOT NULL, "phone_number" varchar(20) NOT NULL, "employee_id" varchar(50) NULL UNIQUE, "profile_picture" varchar(100) NULL, "bio" text NOT NULL, "is_active" bool NOT NULL, "date_joined" datetime NOT NULL, "last_login" datetime NULL, "department_id" bigint NULL REFERENCES "departments_department" ("id") DEFERRABLE INITIALLY DEFERRED, "supervisor_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "accounts_user" VALUES(1,'pbkdf2_sha256$870000$55Rtqbij2pb2iQmfZSlwaw$f4jkRvmNoWoMMg7opXGVH2yc58BqLEoyyHI98r6NkoA=',1,'Tahmaz','Tahmaz','Muradov','admin@q360.gov.az',1,'superadmin','müdür','','0605536990','0001','profiles/IMG-20250426-WA0048_bsVsgAX.jpg','Tahmaz',1,'2025-10-09 06:34:12.095047','2025-10-16 18:52:11.438267',2,1);
INSERT INTO "accounts_user" VALUES(2,'pbkdf2_sha256$870000$56YneD4tq44pKaBGs9tfLp$ua2goaHR4AS7kQskyxiyEAKQRHVX4TfMyeXbO2YIOS0=',1,'admin','Admin','İstifadəçi','admin@q360.az',1,'superadmin','Sistem Administratoru','','',NULL,'','',1,'2025-10-10 15:39:44.521098',NULL,1,NULL);
INSERT INTO "accounts_user" VALUES(3,'pbkdf2_sha256$870000$SYAipiqJ4GXohz0lZq573L$IKkDxmO1ow3Viq4582OD+SDhVHjdGlxNUepdHnkflEI=',0,'manager','Rəşad','Məmmədov','manager@q360.az',0,'manager','HR Meneceri','','',NULL,'','',1,'2025-10-10 15:39:44.841519',NULL,1,NULL);
INSERT INTO "accounts_user" VALUES(4,'pbkdf2_sha256$870000$4qVdVfnUOjhFLTKEAStQWw$I9U3TFY0vJuXuXh7TVpeOmAhQf3LjLMym6wb+ZjQj3w=',0,'employee1','Aynur','Əliyeva','employee1@q360.az',0,'employee','HR Mütəxəssisi','','',NULL,'','',1,'2025-10-10 15:39:45.156561',NULL,1,NULL);
INSERT INTO "accounts_user" VALUES(5,'pbkdf2_sha256$870000$d8iMGg1EBWF9UeGsmIRwOk$z4vVTHZB+eBVDICB30FGOe3rZYPsyjjRe86jf1P+NJw=',0,'employee2','Elçin','Həsənov','employee2@q360.az',0,'employee','Proqramçı','','',NULL,'','',1,'2025-10-10 15:39:45.476098',NULL,2,NULL);
INSERT INTO "accounts_user" VALUES(6,'pbkdf2_sha256$870000$3zckyIz3mYPEC9lzie5Fct$Ho2+K5jmSa++5mc0CMy5oYewkULhk0O81dNn5lMr2i4=',0,'employee3','Günel','İsmayılova','employee3@q360.az',0,'employee','Sistem Analitiki','','',NULL,'','',1,'2025-10-10 15:39:45.802946',NULL,2,NULL);
INSERT INTO "accounts_user" VALUES(7,'pbkdf2_sha256$870000$8JpYXlPFZgePktgqH0vtAO$MeSwek6Npsj30YxqL2plcKTpmA8ePuUWjo4osP26lIA=',0,'rashad','Rəşad','Məmmədov','rashad@q360.az',0,'manager','HR Meneceri','','',NULL,'','',1,'2025-10-10 15:54:56.903567',NULL,1,2);
INSERT INTO "accounts_user" VALUES(8,'pbkdf2_sha256$870000$T0w0YxwXnhO7W44xdwNiAn$2dnZEKfcWBiE8CpDki/cnCi/CJvPdzd4zM23oAbObyU=',0,'elvin','Elvin','Quliyev','elvin@q360.az',0,'manager','IT Meneceri','','',NULL,'','',1,'2025-10-10 15:54:57.238382',NULL,2,2);
INSERT INTO "accounts_user" VALUES(9,'pbkdf2_sha256$870000$SiqYfQdaFK7M6QfmgScyF8$vXbrwzzSk3HI9J/Z+jVsPhY5zooxzZY8/Tb8MqQayuA=',0,'leyla','Leyla','Həsənova','leyla@q360.az',0,'manager','Maliyyə Meneceri','','',NULL,'','',1,'2025-10-10 15:54:57.561516',NULL,3,2);
INSERT INTO "accounts_user" VALUES(10,'pbkdf2_sha256$870000$LowPGlRzHG6dB7Q07nnzgP$rFaWQQQKLuI7zfx/+zEkEgasSPV8grb82iQ81Ysc+v4=',0,'aynur','Aynur','Əliyeva','aynur@q360.az',0,'employee','HR Mütəxəssisi','','',NULL,'','',1,'2025-10-10 15:54:57.891311',NULL,1,7);
INSERT INTO "accounts_user" VALUES(11,'pbkdf2_sha256$870000$F8UpUBMAjn3nyIBZohXgLg$+cNXk5KuEBB+P5G4aj5CP6e0BlMwQ/CqC3uy2Yh9sYA=',0,'kamran','Kamran','Əliyev','kamran@q360.az',0,'employee','HR Mütəxəssisi','','',NULL,'','',1,'2025-10-10 15:54:58.225285',NULL,1,7);
INSERT INTO "accounts_user" VALUES(12,'pbkdf2_sha256$870000$EHa9dh9uU7XAXfxQoKo8tV$db/TZ7H6kGp5zgCbT2+IiMWST7Y9fJJQui0RTASihzc=',0,'elchin','Elçin','Həsənov','elchin@q360.az',0,'employee','Proqramçı','','',NULL,'','',1,'2025-10-10 15:54:58.557737',NULL,2,8);
INSERT INTO "accounts_user" VALUES(13,'pbkdf2_sha256$870000$oYKCeYEPIcZSbLav2rdBPx$vJypvbZPNFu9HXdxHlJuV5jAc/ZZjqoG0QRA80Xo8mg=',0,'gunel','Günəl','İsmayılova','gunel@q360.az',0,'employee','Proqramçı','','',NULL,'','',1,'2025-10-10 15:54:58.886818',NULL,2,8);
INSERT INTO "accounts_user" VALUES(14,'pbkdf2_sha256$870000$wjZNsgN3wwx3rDGOrnUwoy$6hR78tM8sVPy2uk8zt54Uq3lFGSnVJ41R0EtimcxTQk=',0,'nigar','Nigar','Məmmədova','nigar@q360.az',0,'employee','Sistem Administratoru','','',NULL,'','',1,'2025-10-10 15:54:59.224189',NULL,2,8);
INSERT INTO "accounts_user" VALUES(15,'pbkdf2_sha256$870000$DvVPlXGgbDc4W9qF5LJOEI$bhKZtPlXl8Kwug5zLnEHCkDsTP99TwjU5hl4NSMTHqc=',0,'farid','Farid','Abdullayev','farid@q360.az',0,'employee','Mühasib','','',NULL,'profiles/amal.jpg','',1,'2025-10-10 15:54:59.562356','2025-10-10 21:09:40.899180',4,2);
INSERT INTO "accounts_user" VALUES(16,'pbkdf2_sha256$870000$rRG52Kr18fg2dXo36588Al$G7EGbwJ0NVUILeLXSCi/wpr3WrMOXoxDT4UDpFb5HLo=',0,'sevinc','Sevinc','Qasımova','sevinc@q360.az',0,'employee','Mühasib','','',NULL,'','',1,'2025-10-10 15:54:59.911287',NULL,3,9);
INSERT INTO "accounts_user" VALUES(17,'pbkdf2_sha256$870000$k7nLd6WSmzCPJnxCLQEyDs$Klws9xTaoB1d0SORyr6qa/9yjmDxXY2kCb9v1IYbpB0=',0,'tural','Tural','Cəfərov','tural@q360.az',0,'employee','Hüquqşünas','','',NULL,'','',1,'2025-10-10 15:55:00.234951',NULL,4,2);
INSERT INTO "accounts_user" VALUES(18,'pbkdf2_sha256$870000$yXrrUM7OFt8UL5SpiC4vCg$o+xhOvj39bdOxUXf/Dz2xJcI7NvbDIGbKl9pdMBkPA4=',0,'aysel','Aysel','Rəhimova','aysel@q360.az',0,'employee','PR Mütəxəssisi','','',NULL,'','',1,'2025-10-10 15:55:00.569894',NULL,5,2);
INSERT INTO "accounts_user" VALUES(19,'pbkdf2_sha256$870000$cWNOca0FFuNObv3ZYRlQ6R$5U06si/aAYSwGeLDNurAYwC6/qqFJFkERJTb7h37n7M=',0,'murad','Murad','Süleymanov','murad@q360.az',0,'employee','PR Mütəxəssisi','','','0003','','',1,'2025-10-10 15:55:00.897865',NULL,5,2);
INSERT INTO "accounts_user" VALUES(20,'pbkdf2_sha256$870000$0VobTjWJkmRpTyvNlLgkDK$+rJyAHNCibpNAzeWAx7I673hNTB95D803cuBOR4vsN8=',1,'tahmaz','Tahmaz','Muradov','tahmaz@gmail.com',1,'manager','PR Mütəxəssisi','Seyran','0605536990','0005','','',1,'2025-10-11 19:13:56.972223',NULL,2,1);
INSERT INTO "accounts_user" VALUES(21,'pbkdf2_sha256$600000$qdTDUMYzc0jQLufxh74NI2$VmEXIh8CC/s0evtlhbtNWho7peU3JY7U1w9s3LtY8i8=',0,'rashad.mammadov','Rəşad','Məmmədov','rashad.mammadov@mincom.gov.az',1,'admin','Departament direktoru','Elçin','','EMP002','','',1,'2025-10-15 07:47:47.367788',NULL,6,NULL);
INSERT INTO "accounts_user" VALUES(22,'pbkdf2_sha256$600000$CKueHa4TYy82cecJv63a10$yGMkXSKpPirK3sxD8kVOEjn0WN+c65vwdR05LPdg9Dc=',0,'leyla.huseynova','Leyla','Hüseynova','leyla.huseynova@mincom.gov.az',0,'manager','Şöbə müdiri','Vaqif','','EMP003','','',1,'2025-10-15 07:47:47.820029',NULL,7,21);
INSERT INTO "accounts_user" VALUES(23,'pbkdf2_sha256$600000$WVScpHpZfJ7dmvtaiOYGqg$V1tnEAYptxoEZTZezaYZFpRFtYcHIeIYqqMJZYtEfTk=',0,'murad.aliyev','Murad','Əliyev','murad.aliyev@mincom.gov.az',0,'employee','Baş mütəxəssis','Təbriz','','EMP004','','',1,'2025-10-15 07:47:48.217040',NULL,7,22);
INSERT INTO "accounts_user" VALUES(24,'pbkdf2_sha256$870000$pm5rhwhjkOFsyuNtRGeh8w$K9kYT8CjHVm0wx2AfIX/ET/buFAA3b6hUQBS24zn488=',0,'nigar.hasanova','Nigar','Həsənova','nigar.hasanova@mincom.gov.az',0,'employee','Aparıcı mütəxəssis','Ramiz','','EMP005','','',1,'2025-10-15 07:58:53.995135',NULL,7,22);
INSERT INTO "accounts_user" VALUES(25,'pbkdf2_sha256$870000$xTV7VPNkSMVkXhk6zBjt0j$NMh6GGVWHrS1/UGvB/WThl9u5fWd04bQR6EY4wRgLd0=',0,'elvin.quliyev','Elvin','Quliyev','elvin.quliyev@mincom.gov.az',0,'employee','Mütəxəssis','Məhəmməd','','EMP006','','',1,'2025-10-15 07:58:54.347862',NULL,7,22);
INSERT INTO "accounts_user" VALUES(26,'pbkdf2_sha256$870000$rBiVtLTU4vACOym77tiWuL$tT1KJkMdVc+OdD/zb6CQ1fH1vxzvBWrW9Q9qzr/LT4Y=',0,'farid.ismayilov','Farid','İsmayılov','farid.ismayilov@mincom.gov.az',0,'manager','Şöbə müdiri (Kibertəhlükəsizlik)','Əli','','EMP007','','',1,'2025-10-15 07:58:54.696104',NULL,8,21);
INSERT INTO "accounts_user" VALUES(27,'pbkdf2_sha256$870000$q7pwGJncFeJBYsVDS9IWnW$y8p+Az+P/LY1Uig40v6DOPlK0l1QUtl/S9WeEvIlXGk=',0,'aysel.memmedova','Aysel','Məmmədova','aysel.memmedova@mincom.gov.az',0,'employee','Kibertəhlükəsizlik mütəxəssisi','İlham','','EMP008','','',1,'2025-10-15 07:58:55.070605',NULL,8,26);
INSERT INTO "accounts_user" VALUES(28,'pbkdf2_sha256$870000$59u3AoVZL3ongUMctcFmLi$ScWojOEIp4Y2+ono8ul13rsxfvhlbf8/EuNrxWsGCu0=',0,'kamran.bashirov','Kamran','Bəşirov','kamran.bashirov@mincom.gov.az',1,'admin','İnsan Resursları Direktoru','Rəhim','','EMP009','','',1,'2025-10-15 07:58:55.424328',NULL,9,NULL);
INSERT INTO "accounts_user" VALUES(29,'pbkdf2_sha256$870000$kt4e9nYbXopALipofzjsE1$BFJ9NuYUULpM88qC3BT0Oa1uQLGiZGyGvtGC8xT3Dow=',0,'sevinc.huseynli','Sevinc','Hüseynli','sevinc.huseynli@mincom.gov.az',0,'employee','HR Business Partner','Ağa','','EMP010','','',1,'2025-10-15 07:58:55.744128',NULL,9,28);
INSERT INTO "accounts_user" VALUES(30,'pbkdf2_sha256$870000$8Cw6s97bAWo32dZOK8bc7H$dg4rRgAkWhdtLA/NF/lBpDRszrBBtOUyCVQaJl7sX/Y=',0,'tako','Tariyel','Vəliyev','tako01@gmail.com',0,'employee','Kassir','Aftandil','+994511231212',NULL,'','',1,'2025-10-16 16:35:53.327566','2025-10-16 16:36:09.677024',3,NULL);
INSERT INTO "accounts_user" VALUES(31,'pbkdf2_sha256$870000$t9gVruLliJM1RmOoSUsF4v$XatZyf8H6fqxmMgiX2bT7m4ML7u49pSHNWPju0WG3B8=',0,'test_notification_user','Test','User','test@example.com',0,'employee','','','',NULL,'','',1,'2025-10-17 17:11:47.855244',NULL,NULL,NULL);
INSERT INTO "accounts_user" VALUES(32,'pbkdf2_sha256$870000$I6aSIJxylN03nU8Hr5ooHe$nNumtsNfY0wZGBJicqapwUJsISSGz7cpgWKgebB6wXs=',0,'debug_admin','Admin','User','admin@example.com',1,'admin','','','',NULL,'','',1,'2025-10-17 18:51:01.904370','2025-10-17 18:51:02.694795',11,NULL);
INSERT INTO "accounts_user" VALUES(33,'pbkdf2_sha256$870000$cLbOYUAHmTKmlPF03RlWI8$gQa9cLwz5R20neHnhQRFYVLcnoTiNdATLjYxxdqNf5E=',0,'debug_employee','Emp','Loyee','emp@example.com',0,'employee','','','',NULL,'','',1,'2025-10-17 18:51:02.281796',NULL,11,NULL);
INSERT INTO "accounts_user" VALUES(34,'pbkdf2_sha256$870000$c76It1qLbYL6BQWBA45iZW$d6H9NeQqFKXbR2AIRuaQKg6SijtVUyKDbQfjMzNBapI=',0,'dash_user','','','',1,'admin','','','',NULL,'','',1,'2025-10-17 19:11:19.080363','2025-10-17 19:11:19.948880',12,NULL);
CREATE TABLE "accounts_user_groups" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "accounts_user_groups" VALUES(1,1,1);
INSERT INTO "accounts_user_groups" VALUES(2,20,1);
INSERT INTO "accounts_user_groups" VALUES(3,16,2);
CREATE TABLE "accounts_user_user_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "accounts_user_user_permissions" VALUES(1,1,1);
INSERT INTO "accounts_user_user_permissions" VALUES(2,1,2);
INSERT INTO "accounts_user_user_permissions" VALUES(3,1,3);
INSERT INTO "accounts_user_user_permissions" VALUES(4,1,4);
INSERT INTO "accounts_user_user_permissions" VALUES(5,1,5);
INSERT INTO "accounts_user_user_permissions" VALUES(6,1,6);
INSERT INTO "accounts_user_user_permissions" VALUES(7,1,7);
INSERT INTO "accounts_user_user_permissions" VALUES(8,1,8);
INSERT INTO "accounts_user_user_permissions" VALUES(9,1,9);
INSERT INTO "accounts_user_user_permissions" VALUES(10,1,10);
INSERT INTO "accounts_user_user_permissions" VALUES(11,1,11);
INSERT INTO "accounts_user_user_permissions" VALUES(12,1,12);
INSERT INTO "accounts_user_user_permissions" VALUES(13,1,13);
INSERT INTO "accounts_user_user_permissions" VALUES(14,1,14);
INSERT INTO "accounts_user_user_permissions" VALUES(15,1,15);
INSERT INTO "accounts_user_user_permissions" VALUES(16,1,16);
INSERT INTO "accounts_user_user_permissions" VALUES(17,1,17);
INSERT INTO "accounts_user_user_permissions" VALUES(18,1,18);
INSERT INTO "accounts_user_user_permissions" VALUES(19,1,19);
INSERT INTO "accounts_user_user_permissions" VALUES(20,1,20);
INSERT INTO "accounts_user_user_permissions" VALUES(21,1,21);
INSERT INTO "accounts_user_user_permissions" VALUES(22,1,22);
INSERT INTO "accounts_user_user_permissions" VALUES(23,1,23);
INSERT INTO "accounts_user_user_permissions" VALUES(24,1,24);
INSERT INTO "accounts_user_user_permissions" VALUES(25,1,25);
INSERT INTO "accounts_user_user_permissions" VALUES(26,1,26);
INSERT INTO "accounts_user_user_permissions" VALUES(27,1,27);
INSERT INTO "accounts_user_user_permissions" VALUES(28,1,28);
INSERT INTO "accounts_user_user_permissions" VALUES(29,1,29);
INSERT INTO "accounts_user_user_permissions" VALUES(30,1,30);
INSERT INTO "accounts_user_user_permissions" VALUES(31,1,31);
INSERT INTO "accounts_user_user_permissions" VALUES(32,1,32);
INSERT INTO "accounts_user_user_permissions" VALUES(33,1,33);
INSERT INTO "accounts_user_user_permissions" VALUES(34,1,34);
INSERT INTO "accounts_user_user_permissions" VALUES(35,1,35);
INSERT INTO "accounts_user_user_permissions" VALUES(36,1,36);
INSERT INTO "accounts_user_user_permissions" VALUES(37,1,37);
INSERT INTO "accounts_user_user_permissions" VALUES(38,1,38);
INSERT INTO "accounts_user_user_permissions" VALUES(39,1,39);
INSERT INTO "accounts_user_user_permissions" VALUES(40,1,40);
INSERT INTO "accounts_user_user_permissions" VALUES(41,1,41);
INSERT INTO "accounts_user_user_permissions" VALUES(42,1,42);
INSERT INTO "accounts_user_user_permissions" VALUES(43,1,43);
INSERT INTO "accounts_user_user_permissions" VALUES(44,1,44);
INSERT INTO "accounts_user_user_permissions" VALUES(45,1,45);
INSERT INTO "accounts_user_user_permissions" VALUES(46,1,46);
INSERT INTO "accounts_user_user_permissions" VALUES(47,1,47);
INSERT INTO "accounts_user_user_permissions" VALUES(48,1,48);
INSERT INTO "accounts_user_user_permissions" VALUES(49,1,49);
INSERT INTO "accounts_user_user_permissions" VALUES(50,1,50);
INSERT INTO "accounts_user_user_permissions" VALUES(51,1,51);
INSERT INTO "accounts_user_user_permissions" VALUES(52,1,52);
INSERT INTO "accounts_user_user_permissions" VALUES(53,1,53);
INSERT INTO "accounts_user_user_permissions" VALUES(54,1,54);
INSERT INTO "accounts_user_user_permissions" VALUES(55,1,55);
INSERT INTO "accounts_user_user_permissions" VALUES(56,1,56);
INSERT INTO "accounts_user_user_permissions" VALUES(57,1,57);
INSERT INTO "accounts_user_user_permissions" VALUES(58,1,58);
INSERT INTO "accounts_user_user_permissions" VALUES(59,1,59);
INSERT INTO "accounts_user_user_permissions" VALUES(60,1,60);
INSERT INTO "accounts_user_user_permissions" VALUES(61,1,61);
INSERT INTO "accounts_user_user_permissions" VALUES(62,1,62);
INSERT INTO "accounts_user_user_permissions" VALUES(63,1,63);
INSERT INTO "accounts_user_user_permissions" VALUES(64,1,64);
INSERT INTO "accounts_user_user_permissions" VALUES(65,1,65);
INSERT INTO "accounts_user_user_permissions" VALUES(66,1,66);
INSERT INTO "accounts_user_user_permissions" VALUES(67,1,67);
INSERT INTO "accounts_user_user_permissions" VALUES(68,1,68);
INSERT INTO "accounts_user_user_permissions" VALUES(69,1,69);
INSERT INTO "accounts_user_user_permissions" VALUES(70,1,70);
INSERT INTO "accounts_user_user_permissions" VALUES(71,1,71);
INSERT INTO "accounts_user_user_permissions" VALUES(72,1,72);
INSERT INTO "accounts_user_user_permissions" VALUES(73,1,73);
INSERT INTO "accounts_user_user_permissions" VALUES(74,1,74);
INSERT INTO "accounts_user_user_permissions" VALUES(75,1,75);
INSERT INTO "accounts_user_user_permissions" VALUES(76,1,76);
INSERT INTO "accounts_user_user_permissions" VALUES(77,1,77);
INSERT INTO "accounts_user_user_permissions" VALUES(78,1,78);
INSERT INTO "accounts_user_user_permissions" VALUES(79,1,79);
INSERT INTO "accounts_user_user_permissions" VALUES(80,1,80);
INSERT INTO "accounts_user_user_permissions" VALUES(81,1,81);
INSERT INTO "accounts_user_user_permissions" VALUES(82,1,82);
INSERT INTO "accounts_user_user_permissions" VALUES(83,1,83);
INSERT INTO "accounts_user_user_permissions" VALUES(84,1,84);
INSERT INTO "accounts_user_user_permissions" VALUES(85,1,85);
INSERT INTO "accounts_user_user_permissions" VALUES(86,1,86);
INSERT INTO "accounts_user_user_permissions" VALUES(87,1,87);
INSERT INTO "accounts_user_user_permissions" VALUES(88,1,88);
INSERT INTO "accounts_user_user_permissions" VALUES(89,1,89);
INSERT INTO "accounts_user_user_permissions" VALUES(90,1,90);
INSERT INTO "accounts_user_user_permissions" VALUES(91,1,91);
INSERT INTO "accounts_user_user_permissions" VALUES(92,1,92);
INSERT INTO "accounts_user_user_permissions" VALUES(93,1,93);
INSERT INTO "accounts_user_user_permissions" VALUES(94,1,94);
INSERT INTO "accounts_user_user_permissions" VALUES(95,1,95);
INSERT INTO "accounts_user_user_permissions" VALUES(96,1,96);
INSERT INTO "accounts_user_user_permissions" VALUES(97,1,97);
INSERT INTO "accounts_user_user_permissions" VALUES(98,1,98);
INSERT INTO "accounts_user_user_permissions" VALUES(99,1,99);
INSERT INTO "accounts_user_user_permissions" VALUES(100,1,100);
INSERT INTO "accounts_user_user_permissions" VALUES(101,1,101);
INSERT INTO "accounts_user_user_permissions" VALUES(102,1,102);
INSERT INTO "accounts_user_user_permissions" VALUES(103,1,103);
INSERT INTO "accounts_user_user_permissions" VALUES(104,1,104);
INSERT INTO "accounts_user_user_permissions" VALUES(105,1,105);
INSERT INTO "accounts_user_user_permissions" VALUES(106,1,106);
INSERT INTO "accounts_user_user_permissions" VALUES(107,1,107);
INSERT INTO "accounts_user_user_permissions" VALUES(108,1,108);
INSERT INTO "accounts_user_user_permissions" VALUES(109,1,109);
INSERT INTO "accounts_user_user_permissions" VALUES(110,1,110);
INSERT INTO "accounts_user_user_permissions" VALUES(111,1,111);
INSERT INTO "accounts_user_user_permissions" VALUES(112,1,112);
INSERT INTO "accounts_user_user_permissions" VALUES(113,1,113);
INSERT INTO "accounts_user_user_permissions" VALUES(114,1,114);
INSERT INTO "accounts_user_user_permissions" VALUES(115,1,115);
INSERT INTO "accounts_user_user_permissions" VALUES(116,1,116);
INSERT INTO "accounts_user_user_permissions" VALUES(117,1,117);
INSERT INTO "accounts_user_user_permissions" VALUES(118,1,118);
INSERT INTO "accounts_user_user_permissions" VALUES(119,1,119);
INSERT INTO "accounts_user_user_permissions" VALUES(120,1,120);
INSERT INTO "accounts_user_user_permissions" VALUES(121,1,121);
INSERT INTO "accounts_user_user_permissions" VALUES(122,1,122);
INSERT INTO "accounts_user_user_permissions" VALUES(123,1,123);
INSERT INTO "accounts_user_user_permissions" VALUES(124,1,124);
INSERT INTO "accounts_user_user_permissions" VALUES(125,1,125);
INSERT INTO "accounts_user_user_permissions" VALUES(126,1,126);
INSERT INTO "accounts_user_user_permissions" VALUES(127,1,127);
INSERT INTO "accounts_user_user_permissions" VALUES(128,1,128);
INSERT INTO "accounts_user_user_permissions" VALUES(129,1,129);
INSERT INTO "accounts_user_user_permissions" VALUES(130,1,130);
INSERT INTO "accounts_user_user_permissions" VALUES(131,1,131);
INSERT INTO "accounts_user_user_permissions" VALUES(132,1,132);
INSERT INTO "accounts_user_user_permissions" VALUES(133,1,133);
INSERT INTO "accounts_user_user_permissions" VALUES(134,1,134);
INSERT INTO "accounts_user_user_permissions" VALUES(135,1,135);
INSERT INTO "accounts_user_user_permissions" VALUES(136,1,136);
INSERT INTO "accounts_user_user_permissions" VALUES(137,15,145);
INSERT INTO "accounts_user_user_permissions" VALUES(138,15,146);
INSERT INTO "accounts_user_user_permissions" VALUES(139,15,147);
INSERT INTO "accounts_user_user_permissions" VALUES(140,15,148);
INSERT INTO "accounts_user_user_permissions" VALUES(141,15,149);
INSERT INTO "accounts_user_user_permissions" VALUES(142,15,150);
INSERT INTO "accounts_user_user_permissions" VALUES(143,15,151);
INSERT INTO "accounts_user_user_permissions" VALUES(144,15,152);
INSERT INTO "accounts_user_user_permissions" VALUES(145,1,137);
INSERT INTO "accounts_user_user_permissions" VALUES(146,1,138);
INSERT INTO "accounts_user_user_permissions" VALUES(147,1,139);
INSERT INTO "accounts_user_user_permissions" VALUES(148,1,140);
INSERT INTO "accounts_user_user_permissions" VALUES(149,1,141);
INSERT INTO "accounts_user_user_permissions" VALUES(150,1,142);
INSERT INTO "accounts_user_user_permissions" VALUES(151,1,143);
INSERT INTO "accounts_user_user_permissions" VALUES(152,1,144);
INSERT INTO "accounts_user_user_permissions" VALUES(153,1,145);
INSERT INTO "accounts_user_user_permissions" VALUES(154,1,146);
INSERT INTO "accounts_user_user_permissions" VALUES(155,1,147);
INSERT INTO "accounts_user_user_permissions" VALUES(156,1,148);
INSERT INTO "accounts_user_user_permissions" VALUES(157,1,149);
INSERT INTO "accounts_user_user_permissions" VALUES(158,1,150);
INSERT INTO "accounts_user_user_permissions" VALUES(159,1,151);
INSERT INTO "accounts_user_user_permissions" VALUES(160,1,152);
INSERT INTO "accounts_user_user_permissions" VALUES(161,1,153);
INSERT INTO "accounts_user_user_permissions" VALUES(162,1,154);
INSERT INTO "accounts_user_user_permissions" VALUES(163,1,155);
INSERT INTO "accounts_user_user_permissions" VALUES(164,1,156);
INSERT INTO "accounts_user_user_permissions" VALUES(165,1,157);
INSERT INTO "accounts_user_user_permissions" VALUES(166,1,158);
INSERT INTO "accounts_user_user_permissions" VALUES(167,1,159);
INSERT INTO "accounts_user_user_permissions" VALUES(168,1,160);
INSERT INTO "accounts_user_user_permissions" VALUES(169,1,161);
INSERT INTO "accounts_user_user_permissions" VALUES(170,1,162);
INSERT INTO "accounts_user_user_permissions" VALUES(171,1,163);
INSERT INTO "accounts_user_user_permissions" VALUES(172,1,164);
INSERT INTO "accounts_user_user_permissions" VALUES(173,1,165);
INSERT INTO "accounts_user_user_permissions" VALUES(174,1,166);
INSERT INTO "accounts_user_user_permissions" VALUES(175,1,167);
INSERT INTO "accounts_user_user_permissions" VALUES(176,1,168);
INSERT INTO "accounts_user_user_permissions" VALUES(177,1,169);
INSERT INTO "accounts_user_user_permissions" VALUES(178,1,170);
INSERT INTO "accounts_user_user_permissions" VALUES(179,1,171);
INSERT INTO "accounts_user_user_permissions" VALUES(180,1,172);
INSERT INTO "accounts_user_user_permissions" VALUES(181,1,173);
INSERT INTO "accounts_user_user_permissions" VALUES(182,1,174);
INSERT INTO "accounts_user_user_permissions" VALUES(183,1,175);
INSERT INTO "accounts_user_user_permissions" VALUES(184,1,176);
INSERT INTO "accounts_user_user_permissions" VALUES(185,1,177);
INSERT INTO "accounts_user_user_permissions" VALUES(186,1,178);
INSERT INTO "accounts_user_user_permissions" VALUES(187,1,179);
INSERT INTO "accounts_user_user_permissions" VALUES(188,1,180);
INSERT INTO "accounts_user_user_permissions" VALUES(189,1,181);
INSERT INTO "accounts_user_user_permissions" VALUES(190,1,182);
INSERT INTO "accounts_user_user_permissions" VALUES(191,1,183);
INSERT INTO "accounts_user_user_permissions" VALUES(192,1,184);
INSERT INTO "accounts_user_user_permissions" VALUES(193,1,185);
INSERT INTO "accounts_user_user_permissions" VALUES(194,1,186);
INSERT INTO "accounts_user_user_permissions" VALUES(195,1,187);
INSERT INTO "accounts_user_user_permissions" VALUES(196,1,188);
INSERT INTO "accounts_user_user_permissions" VALUES(197,1,189);
INSERT INTO "accounts_user_user_permissions" VALUES(198,1,190);
INSERT INTO "accounts_user_user_permissions" VALUES(199,1,191);
INSERT INTO "accounts_user_user_permissions" VALUES(200,1,192);
INSERT INTO "accounts_user_user_permissions" VALUES(201,1,193);
INSERT INTO "accounts_user_user_permissions" VALUES(202,1,194);
INSERT INTO "accounts_user_user_permissions" VALUES(203,1,195);
INSERT INTO "accounts_user_user_permissions" VALUES(204,1,196);
INSERT INTO "accounts_user_user_permissions" VALUES(205,1,197);
INSERT INTO "accounts_user_user_permissions" VALUES(206,1,198);
INSERT INTO "accounts_user_user_permissions" VALUES(207,1,199);
INSERT INTO "accounts_user_user_permissions" VALUES(208,1,200);
INSERT INTO "accounts_user_user_permissions" VALUES(209,1,201);
INSERT INTO "accounts_user_user_permissions" VALUES(210,1,202);
INSERT INTO "accounts_user_user_permissions" VALUES(211,1,203);
INSERT INTO "accounts_user_user_permissions" VALUES(212,1,204);
INSERT INTO "accounts_user_user_permissions" VALUES(213,1,205);
INSERT INTO "accounts_user_user_permissions" VALUES(214,1,206);
INSERT INTO "accounts_user_user_permissions" VALUES(215,1,207);
INSERT INTO "accounts_user_user_permissions" VALUES(216,1,208);
INSERT INTO "accounts_user_user_permissions" VALUES(217,1,209);
INSERT INTO "accounts_user_user_permissions" VALUES(218,1,210);
INSERT INTO "accounts_user_user_permissions" VALUES(219,1,211);
INSERT INTO "accounts_user_user_permissions" VALUES(220,1,212);
INSERT INTO "accounts_user_user_permissions" VALUES(221,1,213);
INSERT INTO "accounts_user_user_permissions" VALUES(222,1,214);
INSERT INTO "accounts_user_user_permissions" VALUES(223,1,215);
INSERT INTO "accounts_user_user_permissions" VALUES(224,1,216);
INSERT INTO "accounts_user_user_permissions" VALUES(225,1,217);
INSERT INTO "accounts_user_user_permissions" VALUES(226,1,218);
INSERT INTO "accounts_user_user_permissions" VALUES(227,1,219);
INSERT INTO "accounts_user_user_permissions" VALUES(228,1,220);
INSERT INTO "accounts_user_user_permissions" VALUES(229,1,221);
INSERT INTO "accounts_user_user_permissions" VALUES(230,1,222);
INSERT INTO "accounts_user_user_permissions" VALUES(231,1,223);
INSERT INTO "accounts_user_user_permissions" VALUES(232,1,224);
INSERT INTO "accounts_user_user_permissions" VALUES(233,1,225);
INSERT INTO "accounts_user_user_permissions" VALUES(234,1,226);
INSERT INTO "accounts_user_user_permissions" VALUES(235,1,227);
INSERT INTO "accounts_user_user_permissions" VALUES(236,1,228);
INSERT INTO "accounts_user_user_permissions" VALUES(237,1,229);
INSERT INTO "accounts_user_user_permissions" VALUES(238,1,230);
INSERT INTO "accounts_user_user_permissions" VALUES(239,1,231);
INSERT INTO "accounts_user_user_permissions" VALUES(240,1,232);
INSERT INTO "accounts_user_user_permissions" VALUES(241,1,233);
INSERT INTO "accounts_user_user_permissions" VALUES(242,1,234);
INSERT INTO "accounts_user_user_permissions" VALUES(243,1,235);
INSERT INTO "accounts_user_user_permissions" VALUES(244,1,236);
INSERT INTO "accounts_user_user_permissions" VALUES(245,20,1);
INSERT INTO "accounts_user_user_permissions" VALUES(246,20,2);
INSERT INTO "accounts_user_user_permissions" VALUES(247,20,3);
INSERT INTO "accounts_user_user_permissions" VALUES(248,20,4);
INSERT INTO "accounts_user_user_permissions" VALUES(249,20,5);
INSERT INTO "accounts_user_user_permissions" VALUES(250,20,6);
INSERT INTO "accounts_user_user_permissions" VALUES(251,20,7);
INSERT INTO "accounts_user_user_permissions" VALUES(252,20,8);
INSERT INTO "accounts_user_user_permissions" VALUES(253,20,9);
INSERT INTO "accounts_user_user_permissions" VALUES(254,20,10);
INSERT INTO "accounts_user_user_permissions" VALUES(255,20,11);
INSERT INTO "accounts_user_user_permissions" VALUES(256,20,12);
INSERT INTO "accounts_user_user_permissions" VALUES(257,20,13);
INSERT INTO "accounts_user_user_permissions" VALUES(258,20,14);
INSERT INTO "accounts_user_user_permissions" VALUES(259,20,15);
INSERT INTO "accounts_user_user_permissions" VALUES(260,20,16);
INSERT INTO "accounts_user_user_permissions" VALUES(261,20,17);
INSERT INTO "accounts_user_user_permissions" VALUES(262,20,18);
INSERT INTO "accounts_user_user_permissions" VALUES(263,20,19);
INSERT INTO "accounts_user_user_permissions" VALUES(264,20,20);
INSERT INTO "accounts_user_user_permissions" VALUES(265,20,21);
INSERT INTO "accounts_user_user_permissions" VALUES(266,20,22);
INSERT INTO "accounts_user_user_permissions" VALUES(267,20,23);
INSERT INTO "accounts_user_user_permissions" VALUES(268,20,24);
INSERT INTO "accounts_user_user_permissions" VALUES(269,20,25);
INSERT INTO "accounts_user_user_permissions" VALUES(270,20,26);
INSERT INTO "accounts_user_user_permissions" VALUES(271,20,27);
INSERT INTO "accounts_user_user_permissions" VALUES(272,20,28);
INSERT INTO "accounts_user_user_permissions" VALUES(273,20,29);
INSERT INTO "accounts_user_user_permissions" VALUES(274,20,30);
INSERT INTO "accounts_user_user_permissions" VALUES(275,20,31);
INSERT INTO "accounts_user_user_permissions" VALUES(276,20,32);
INSERT INTO "accounts_user_user_permissions" VALUES(277,20,33);
INSERT INTO "accounts_user_user_permissions" VALUES(278,20,34);
INSERT INTO "accounts_user_user_permissions" VALUES(279,20,35);
INSERT INTO "accounts_user_user_permissions" VALUES(280,20,36);
INSERT INTO "accounts_user_user_permissions" VALUES(281,20,37);
INSERT INTO "accounts_user_user_permissions" VALUES(282,20,38);
INSERT INTO "accounts_user_user_permissions" VALUES(283,20,39);
INSERT INTO "accounts_user_user_permissions" VALUES(284,20,40);
INSERT INTO "accounts_user_user_permissions" VALUES(285,20,41);
INSERT INTO "accounts_user_user_permissions" VALUES(286,20,42);
INSERT INTO "accounts_user_user_permissions" VALUES(287,20,43);
INSERT INTO "accounts_user_user_permissions" VALUES(288,20,44);
INSERT INTO "accounts_user_user_permissions" VALUES(289,20,45);
INSERT INTO "accounts_user_user_permissions" VALUES(290,20,46);
INSERT INTO "accounts_user_user_permissions" VALUES(291,20,47);
INSERT INTO "accounts_user_user_permissions" VALUES(292,20,48);
INSERT INTO "accounts_user_user_permissions" VALUES(293,20,49);
INSERT INTO "accounts_user_user_permissions" VALUES(294,20,50);
INSERT INTO "accounts_user_user_permissions" VALUES(295,20,51);
INSERT INTO "accounts_user_user_permissions" VALUES(296,20,52);
INSERT INTO "accounts_user_user_permissions" VALUES(297,20,53);
INSERT INTO "accounts_user_user_permissions" VALUES(298,20,54);
INSERT INTO "accounts_user_user_permissions" VALUES(299,20,55);
INSERT INTO "accounts_user_user_permissions" VALUES(300,20,56);
INSERT INTO "accounts_user_user_permissions" VALUES(301,20,57);
INSERT INTO "accounts_user_user_permissions" VALUES(302,20,58);
INSERT INTO "accounts_user_user_permissions" VALUES(303,20,59);
INSERT INTO "accounts_user_user_permissions" VALUES(304,20,60);
INSERT INTO "accounts_user_user_permissions" VALUES(305,20,61);
INSERT INTO "accounts_user_user_permissions" VALUES(306,20,62);
INSERT INTO "accounts_user_user_permissions" VALUES(307,20,63);
INSERT INTO "accounts_user_user_permissions" VALUES(308,20,64);
INSERT INTO "accounts_user_user_permissions" VALUES(309,20,65);
INSERT INTO "accounts_user_user_permissions" VALUES(310,20,66);
INSERT INTO "accounts_user_user_permissions" VALUES(311,20,67);
INSERT INTO "accounts_user_user_permissions" VALUES(312,20,68);
INSERT INTO "accounts_user_user_permissions" VALUES(313,20,69);
INSERT INTO "accounts_user_user_permissions" VALUES(314,20,70);
INSERT INTO "accounts_user_user_permissions" VALUES(315,20,71);
INSERT INTO "accounts_user_user_permissions" VALUES(316,20,72);
INSERT INTO "accounts_user_user_permissions" VALUES(317,20,73);
INSERT INTO "accounts_user_user_permissions" VALUES(318,20,74);
INSERT INTO "accounts_user_user_permissions" VALUES(319,20,75);
INSERT INTO "accounts_user_user_permissions" VALUES(320,20,76);
INSERT INTO "accounts_user_user_permissions" VALUES(321,20,77);
INSERT INTO "accounts_user_user_permissions" VALUES(322,20,78);
INSERT INTO "accounts_user_user_permissions" VALUES(323,20,79);
INSERT INTO "accounts_user_user_permissions" VALUES(324,20,80);
INSERT INTO "accounts_user_user_permissions" VALUES(325,20,81);
INSERT INTO "accounts_user_user_permissions" VALUES(326,20,82);
INSERT INTO "accounts_user_user_permissions" VALUES(327,20,83);
INSERT INTO "accounts_user_user_permissions" VALUES(328,20,84);
INSERT INTO "accounts_user_user_permissions" VALUES(329,20,85);
INSERT INTO "accounts_user_user_permissions" VALUES(330,20,86);
INSERT INTO "accounts_user_user_permissions" VALUES(331,20,87);
INSERT INTO "accounts_user_user_permissions" VALUES(332,20,88);
INSERT INTO "accounts_user_user_permissions" VALUES(333,20,89);
INSERT INTO "accounts_user_user_permissions" VALUES(334,20,90);
INSERT INTO "accounts_user_user_permissions" VALUES(335,20,91);
INSERT INTO "accounts_user_user_permissions" VALUES(336,20,92);
INSERT INTO "accounts_user_user_permissions" VALUES(337,20,93);
INSERT INTO "accounts_user_user_permissions" VALUES(338,20,94);
INSERT INTO "accounts_user_user_permissions" VALUES(339,20,95);
INSERT INTO "accounts_user_user_permissions" VALUES(340,20,96);
INSERT INTO "accounts_user_user_permissions" VALUES(341,20,97);
INSERT INTO "accounts_user_user_permissions" VALUES(342,20,98);
INSERT INTO "accounts_user_user_permissions" VALUES(343,20,99);
INSERT INTO "accounts_user_user_permissions" VALUES(344,20,100);
INSERT INTO "accounts_user_user_permissions" VALUES(345,20,101);
INSERT INTO "accounts_user_user_permissions" VALUES(346,20,102);
INSERT INTO "accounts_user_user_permissions" VALUES(347,20,103);
INSERT INTO "accounts_user_user_permissions" VALUES(348,20,104);
INSERT INTO "accounts_user_user_permissions" VALUES(349,20,105);
INSERT INTO "accounts_user_user_permissions" VALUES(350,20,106);
INSERT INTO "accounts_user_user_permissions" VALUES(351,20,107);
INSERT INTO "accounts_user_user_permissions" VALUES(352,20,108);
INSERT INTO "accounts_user_user_permissions" VALUES(353,20,109);
INSERT INTO "accounts_user_user_permissions" VALUES(354,20,110);
INSERT INTO "accounts_user_user_permissions" VALUES(355,20,111);
INSERT INTO "accounts_user_user_permissions" VALUES(356,20,112);
INSERT INTO "accounts_user_user_permissions" VALUES(357,20,113);
INSERT INTO "accounts_user_user_permissions" VALUES(358,20,114);
INSERT INTO "accounts_user_user_permissions" VALUES(359,20,115);
INSERT INTO "accounts_user_user_permissions" VALUES(360,20,116);
INSERT INTO "accounts_user_user_permissions" VALUES(361,20,117);
INSERT INTO "accounts_user_user_permissions" VALUES(362,20,118);
INSERT INTO "accounts_user_user_permissions" VALUES(363,20,119);
INSERT INTO "accounts_user_user_permissions" VALUES(364,20,120);
INSERT INTO "accounts_user_user_permissions" VALUES(365,20,121);
INSERT INTO "accounts_user_user_permissions" VALUES(366,20,122);
INSERT INTO "accounts_user_user_permissions" VALUES(367,20,123);
INSERT INTO "accounts_user_user_permissions" VALUES(368,20,124);
INSERT INTO "accounts_user_user_permissions" VALUES(369,20,125);
INSERT INTO "accounts_user_user_permissions" VALUES(370,20,126);
INSERT INTO "accounts_user_user_permissions" VALUES(371,20,127);
INSERT INTO "accounts_user_user_permissions" VALUES(372,20,128);
INSERT INTO "accounts_user_user_permissions" VALUES(373,20,129);
INSERT INTO "accounts_user_user_permissions" VALUES(374,20,130);
INSERT INTO "accounts_user_user_permissions" VALUES(375,20,131);
INSERT INTO "accounts_user_user_permissions" VALUES(376,20,132);
INSERT INTO "accounts_user_user_permissions" VALUES(377,20,133);
INSERT INTO "accounts_user_user_permissions" VALUES(378,20,134);
INSERT INTO "accounts_user_user_permissions" VALUES(379,20,135);
INSERT INTO "accounts_user_user_permissions" VALUES(380,20,136);
INSERT INTO "accounts_user_user_permissions" VALUES(381,20,137);
INSERT INTO "accounts_user_user_permissions" VALUES(382,20,138);
INSERT INTO "accounts_user_user_permissions" VALUES(383,20,139);
INSERT INTO "accounts_user_user_permissions" VALUES(384,20,140);
INSERT INTO "accounts_user_user_permissions" VALUES(385,20,141);
INSERT INTO "accounts_user_user_permissions" VALUES(386,20,142);
INSERT INTO "accounts_user_user_permissions" VALUES(387,20,143);
INSERT INTO "accounts_user_user_permissions" VALUES(388,20,144);
INSERT INTO "accounts_user_user_permissions" VALUES(389,20,145);
INSERT INTO "accounts_user_user_permissions" VALUES(390,20,146);
INSERT INTO "accounts_user_user_permissions" VALUES(391,20,147);
INSERT INTO "accounts_user_user_permissions" VALUES(392,20,148);
INSERT INTO "accounts_user_user_permissions" VALUES(393,20,149);
INSERT INTO "accounts_user_user_permissions" VALUES(394,20,150);
INSERT INTO "accounts_user_user_permissions" VALUES(395,20,151);
INSERT INTO "accounts_user_user_permissions" VALUES(396,20,152);
INSERT INTO "accounts_user_user_permissions" VALUES(397,20,153);
INSERT INTO "accounts_user_user_permissions" VALUES(398,20,154);
INSERT INTO "accounts_user_user_permissions" VALUES(399,20,155);
INSERT INTO "accounts_user_user_permissions" VALUES(400,20,156);
INSERT INTO "accounts_user_user_permissions" VALUES(401,20,157);
INSERT INTO "accounts_user_user_permissions" VALUES(402,20,158);
INSERT INTO "accounts_user_user_permissions" VALUES(403,20,159);
INSERT INTO "accounts_user_user_permissions" VALUES(404,20,160);
INSERT INTO "accounts_user_user_permissions" VALUES(405,20,161);
INSERT INTO "accounts_user_user_permissions" VALUES(406,20,162);
INSERT INTO "accounts_user_user_permissions" VALUES(407,20,163);
INSERT INTO "accounts_user_user_permissions" VALUES(408,20,164);
INSERT INTO "accounts_user_user_permissions" VALUES(409,20,165);
INSERT INTO "accounts_user_user_permissions" VALUES(410,20,166);
INSERT INTO "accounts_user_user_permissions" VALUES(411,20,167);
INSERT INTO "accounts_user_user_permissions" VALUES(412,20,168);
INSERT INTO "accounts_user_user_permissions" VALUES(413,20,169);
INSERT INTO "accounts_user_user_permissions" VALUES(414,20,170);
INSERT INTO "accounts_user_user_permissions" VALUES(415,20,171);
INSERT INTO "accounts_user_user_permissions" VALUES(416,20,172);
INSERT INTO "accounts_user_user_permissions" VALUES(417,20,173);
INSERT INTO "accounts_user_user_permissions" VALUES(418,20,174);
INSERT INTO "accounts_user_user_permissions" VALUES(419,20,175);
INSERT INTO "accounts_user_user_permissions" VALUES(420,20,176);
INSERT INTO "accounts_user_user_permissions" VALUES(421,20,177);
INSERT INTO "accounts_user_user_permissions" VALUES(422,20,178);
INSERT INTO "accounts_user_user_permissions" VALUES(423,20,179);
INSERT INTO "accounts_user_user_permissions" VALUES(424,20,180);
INSERT INTO "accounts_user_user_permissions" VALUES(425,20,181);
INSERT INTO "accounts_user_user_permissions" VALUES(426,20,182);
INSERT INTO "accounts_user_user_permissions" VALUES(427,20,183);
INSERT INTO "accounts_user_user_permissions" VALUES(428,20,184);
INSERT INTO "accounts_user_user_permissions" VALUES(429,20,185);
INSERT INTO "accounts_user_user_permissions" VALUES(430,20,186);
INSERT INTO "accounts_user_user_permissions" VALUES(431,20,187);
INSERT INTO "accounts_user_user_permissions" VALUES(432,20,188);
INSERT INTO "accounts_user_user_permissions" VALUES(433,20,189);
INSERT INTO "accounts_user_user_permissions" VALUES(434,20,190);
INSERT INTO "accounts_user_user_permissions" VALUES(435,20,191);
INSERT INTO "accounts_user_user_permissions" VALUES(436,20,192);
INSERT INTO "accounts_user_user_permissions" VALUES(437,20,193);
INSERT INTO "accounts_user_user_permissions" VALUES(438,20,194);
INSERT INTO "accounts_user_user_permissions" VALUES(439,20,195);
INSERT INTO "accounts_user_user_permissions" VALUES(440,20,196);
INSERT INTO "accounts_user_user_permissions" VALUES(441,20,197);
INSERT INTO "accounts_user_user_permissions" VALUES(442,20,198);
INSERT INTO "accounts_user_user_permissions" VALUES(443,20,199);
INSERT INTO "accounts_user_user_permissions" VALUES(444,20,200);
INSERT INTO "accounts_user_user_permissions" VALUES(445,20,201);
INSERT INTO "accounts_user_user_permissions" VALUES(446,20,202);
INSERT INTO "accounts_user_user_permissions" VALUES(447,20,203);
INSERT INTO "accounts_user_user_permissions" VALUES(448,20,204);
INSERT INTO "accounts_user_user_permissions" VALUES(449,20,205);
INSERT INTO "accounts_user_user_permissions" VALUES(450,20,206);
INSERT INTO "accounts_user_user_permissions" VALUES(451,20,207);
INSERT INTO "accounts_user_user_permissions" VALUES(452,20,208);
INSERT INTO "accounts_user_user_permissions" VALUES(453,20,209);
INSERT INTO "accounts_user_user_permissions" VALUES(454,20,210);
INSERT INTO "accounts_user_user_permissions" VALUES(455,20,211);
INSERT INTO "accounts_user_user_permissions" VALUES(456,20,212);
INSERT INTO "accounts_user_user_permissions" VALUES(457,20,213);
INSERT INTO "accounts_user_user_permissions" VALUES(458,20,214);
INSERT INTO "accounts_user_user_permissions" VALUES(459,20,215);
INSERT INTO "accounts_user_user_permissions" VALUES(460,20,216);
INSERT INTO "accounts_user_user_permissions" VALUES(461,20,217);
INSERT INTO "accounts_user_user_permissions" VALUES(462,20,218);
INSERT INTO "accounts_user_user_permissions" VALUES(463,20,219);
INSERT INTO "accounts_user_user_permissions" VALUES(464,20,220);
INSERT INTO "accounts_user_user_permissions" VALUES(465,20,221);
INSERT INTO "accounts_user_user_permissions" VALUES(466,20,222);
INSERT INTO "accounts_user_user_permissions" VALUES(467,20,223);
INSERT INTO "accounts_user_user_permissions" VALUES(468,20,224);
INSERT INTO "accounts_user_user_permissions" VALUES(469,20,225);
INSERT INTO "accounts_user_user_permissions" VALUES(470,20,226);
INSERT INTO "accounts_user_user_permissions" VALUES(471,20,227);
INSERT INTO "accounts_user_user_permissions" VALUES(472,20,228);
INSERT INTO "accounts_user_user_permissions" VALUES(473,20,229);
INSERT INTO "accounts_user_user_permissions" VALUES(474,20,230);
INSERT INTO "accounts_user_user_permissions" VALUES(475,20,231);
INSERT INTO "accounts_user_user_permissions" VALUES(476,20,232);
INSERT INTO "accounts_user_user_permissions" VALUES(477,20,233);
INSERT INTO "accounts_user_user_permissions" VALUES(478,20,234);
INSERT INTO "accounts_user_user_permissions" VALUES(479,20,235);
INSERT INTO "accounts_user_user_permissions" VALUES(480,20,236);
INSERT INTO "accounts_user_user_permissions" VALUES(481,16,200);
INSERT INTO "accounts_user_user_permissions" VALUES(482,16,201);
INSERT INTO "accounts_user_user_permissions" VALUES(483,16,205);
INSERT INTO "accounts_user_user_permissions" VALUES(484,16,206);
INSERT INTO "accounts_user_user_permissions" VALUES(485,16,207);
INSERT INTO "accounts_user_user_permissions" VALUES(486,16,208);
INSERT INTO "accounts_user_user_permissions" VALUES(487,32,45);
INSERT INTO "accounts_user_user_permissions" VALUES(488,32,46);
INSERT INTO "accounts_user_user_permissions" VALUES(489,32,47);
INSERT INTO "accounts_user_user_permissions" VALUES(490,32,48);
INSERT INTO "accounts_user_user_permissions" VALUES(491,32,49);
INSERT INTO "accounts_user_user_permissions" VALUES(492,32,50);
INSERT INTO "accounts_user_user_permissions" VALUES(493,32,51);
INSERT INTO "accounts_user_user_permissions" VALUES(494,32,52);
INSERT INTO "accounts_user_user_permissions" VALUES(495,32,53);
INSERT INTO "accounts_user_user_permissions" VALUES(496,32,54);
INSERT INTO "accounts_user_user_permissions" VALUES(497,32,55);
INSERT INTO "accounts_user_user_permissions" VALUES(498,32,56);
INSERT INTO "accounts_user_user_permissions" VALUES(499,32,57);
INSERT INTO "accounts_user_user_permissions" VALUES(500,32,58);
INSERT INTO "accounts_user_user_permissions" VALUES(501,32,59);
INSERT INTO "accounts_user_user_permissions" VALUES(502,32,60);
INSERT INTO "accounts_user_user_permissions" VALUES(503,32,61);
INSERT INTO "accounts_user_user_permissions" VALUES(504,32,62);
INSERT INTO "accounts_user_user_permissions" VALUES(505,32,63);
INSERT INTO "accounts_user_user_permissions" VALUES(506,32,64);
INSERT INTO "accounts_user_user_permissions" VALUES(507,32,65);
INSERT INTO "accounts_user_user_permissions" VALUES(508,32,66);
INSERT INTO "accounts_user_user_permissions" VALUES(509,32,67);
INSERT INTO "accounts_user_user_permissions" VALUES(510,32,68);
INSERT INTO "accounts_user_user_permissions" VALUES(511,32,69);
INSERT INTO "accounts_user_user_permissions" VALUES(512,32,70);
INSERT INTO "accounts_user_user_permissions" VALUES(513,32,71);
INSERT INTO "accounts_user_user_permissions" VALUES(514,32,72);
INSERT INTO "accounts_user_user_permissions" VALUES(515,32,73);
INSERT INTO "accounts_user_user_permissions" VALUES(516,32,74);
INSERT INTO "accounts_user_user_permissions" VALUES(517,32,75);
INSERT INTO "accounts_user_user_permissions" VALUES(518,32,76);
INSERT INTO "accounts_user_user_permissions" VALUES(519,32,77);
INSERT INTO "accounts_user_user_permissions" VALUES(520,32,78);
INSERT INTO "accounts_user_user_permissions" VALUES(521,32,79);
INSERT INTO "accounts_user_user_permissions" VALUES(522,32,80);
INSERT INTO "accounts_user_user_permissions" VALUES(523,32,81);
INSERT INTO "accounts_user_user_permissions" VALUES(524,32,82);
INSERT INTO "accounts_user_user_permissions" VALUES(525,32,83);
INSERT INTO "accounts_user_user_permissions" VALUES(526,32,84);
INSERT INTO "accounts_user_user_permissions" VALUES(527,32,85);
INSERT INTO "accounts_user_user_permissions" VALUES(528,32,86);
INSERT INTO "accounts_user_user_permissions" VALUES(529,32,87);
INSERT INTO "accounts_user_user_permissions" VALUES(530,32,88);
INSERT INTO "accounts_user_user_permissions" VALUES(531,32,89);
INSERT INTO "accounts_user_user_permissions" VALUES(532,32,90);
INSERT INTO "accounts_user_user_permissions" VALUES(533,32,91);
INSERT INTO "accounts_user_user_permissions" VALUES(534,32,92);
INSERT INTO "accounts_user_user_permissions" VALUES(535,32,93);
INSERT INTO "accounts_user_user_permissions" VALUES(536,32,94);
INSERT INTO "accounts_user_user_permissions" VALUES(537,32,95);
INSERT INTO "accounts_user_user_permissions" VALUES(538,32,96);
INSERT INTO "accounts_user_user_permissions" VALUES(539,32,97);
INSERT INTO "accounts_user_user_permissions" VALUES(540,32,98);
INSERT INTO "accounts_user_user_permissions" VALUES(541,32,99);
INSERT INTO "accounts_user_user_permissions" VALUES(542,32,100);
INSERT INTO "accounts_user_user_permissions" VALUES(543,32,101);
INSERT INTO "accounts_user_user_permissions" VALUES(544,32,102);
INSERT INTO "accounts_user_user_permissions" VALUES(545,32,103);
INSERT INTO "accounts_user_user_permissions" VALUES(546,32,104);
INSERT INTO "accounts_user_user_permissions" VALUES(547,32,105);
INSERT INTO "accounts_user_user_permissions" VALUES(548,32,106);
INSERT INTO "accounts_user_user_permissions" VALUES(549,32,107);
INSERT INTO "accounts_user_user_permissions" VALUES(550,32,108);
INSERT INTO "accounts_user_user_permissions" VALUES(551,32,109);
INSERT INTO "accounts_user_user_permissions" VALUES(552,32,110);
INSERT INTO "accounts_user_user_permissions" VALUES(553,32,111);
INSERT INTO "accounts_user_user_permissions" VALUES(554,32,112);
INSERT INTO "accounts_user_user_permissions" VALUES(555,32,113);
INSERT INTO "accounts_user_user_permissions" VALUES(556,32,114);
INSERT INTO "accounts_user_user_permissions" VALUES(557,32,115);
INSERT INTO "accounts_user_user_permissions" VALUES(558,32,116);
INSERT INTO "accounts_user_user_permissions" VALUES(559,32,117);
INSERT INTO "accounts_user_user_permissions" VALUES(560,32,118);
INSERT INTO "accounts_user_user_permissions" VALUES(561,32,119);
INSERT INTO "accounts_user_user_permissions" VALUES(562,32,120);
INSERT INTO "accounts_user_user_permissions" VALUES(563,32,121);
INSERT INTO "accounts_user_user_permissions" VALUES(564,32,122);
INSERT INTO "accounts_user_user_permissions" VALUES(565,32,123);
INSERT INTO "accounts_user_user_permissions" VALUES(566,32,124);
INSERT INTO "accounts_user_user_permissions" VALUES(567,32,125);
INSERT INTO "accounts_user_user_permissions" VALUES(568,32,126);
INSERT INTO "accounts_user_user_permissions" VALUES(569,32,127);
INSERT INTO "accounts_user_user_permissions" VALUES(570,32,128);
INSERT INTO "accounts_user_user_permissions" VALUES(571,32,129);
INSERT INTO "accounts_user_user_permissions" VALUES(572,32,130);
INSERT INTO "accounts_user_user_permissions" VALUES(573,32,131);
INSERT INTO "accounts_user_user_permissions" VALUES(574,32,132);
INSERT INTO "accounts_user_user_permissions" VALUES(575,32,137);
INSERT INTO "accounts_user_user_permissions" VALUES(576,32,138);
INSERT INTO "accounts_user_user_permissions" VALUES(577,32,139);
INSERT INTO "accounts_user_user_permissions" VALUES(578,32,140);
INSERT INTO "accounts_user_user_permissions" VALUES(579,32,141);
INSERT INTO "accounts_user_user_permissions" VALUES(580,32,142);
INSERT INTO "accounts_user_user_permissions" VALUES(581,32,143);
INSERT INTO "accounts_user_user_permissions" VALUES(582,32,144);
INSERT INTO "accounts_user_user_permissions" VALUES(583,32,333);
INSERT INTO "accounts_user_user_permissions" VALUES(584,32,334);
INSERT INTO "accounts_user_user_permissions" VALUES(585,32,335);
INSERT INTO "accounts_user_user_permissions" VALUES(586,32,336);
INSERT INTO "accounts_user_user_permissions" VALUES(587,32,337);
INSERT INTO "accounts_user_user_permissions" VALUES(588,32,338);
INSERT INTO "accounts_user_user_permissions" VALUES(589,32,339);
INSERT INTO "accounts_user_user_permissions" VALUES(590,32,340);
INSERT INTO "accounts_user_user_permissions" VALUES(591,32,341);
INSERT INTO "accounts_user_user_permissions" VALUES(592,32,342);
INSERT INTO "accounts_user_user_permissions" VALUES(593,32,343);
INSERT INTO "accounts_user_user_permissions" VALUES(594,32,344);
INSERT INTO "accounts_user_user_permissions" VALUES(595,32,345);
INSERT INTO "accounts_user_user_permissions" VALUES(596,32,346);
INSERT INTO "accounts_user_user_permissions" VALUES(597,32,347);
INSERT INTO "accounts_user_user_permissions" VALUES(598,32,348);
INSERT INTO "accounts_user_user_permissions" VALUES(599,32,349);
INSERT INTO "accounts_user_user_permissions" VALUES(600,32,350);
INSERT INTO "accounts_user_user_permissions" VALUES(601,32,351);
INSERT INTO "accounts_user_user_permissions" VALUES(602,32,352);
INSERT INTO "accounts_user_user_permissions" VALUES(603,32,353);
INSERT INTO "accounts_user_user_permissions" VALUES(604,32,354);
INSERT INTO "accounts_user_user_permissions" VALUES(605,32,355);
INSERT INTO "accounts_user_user_permissions" VALUES(606,32,356);
INSERT INTO "accounts_user_user_permissions" VALUES(607,32,357);
INSERT INTO "accounts_user_user_permissions" VALUES(608,32,358);
INSERT INTO "accounts_user_user_permissions" VALUES(609,32,359);
INSERT INTO "accounts_user_user_permissions" VALUES(610,32,360);
INSERT INTO "accounts_user_user_permissions" VALUES(611,32,361);
INSERT INTO "accounts_user_user_permissions" VALUES(612,32,362);
INSERT INTO "accounts_user_user_permissions" VALUES(613,32,363);
INSERT INTO "accounts_user_user_permissions" VALUES(614,32,364);
INSERT INTO "accounts_user_user_permissions" VALUES(615,32,413);
INSERT INTO "accounts_user_user_permissions" VALUES(616,32,414);
INSERT INTO "accounts_user_user_permissions" VALUES(617,32,415);
INSERT INTO "accounts_user_user_permissions" VALUES(618,32,416);
INSERT INTO "accounts_user_user_permissions" VALUES(619,32,417);
INSERT INTO "accounts_user_user_permissions" VALUES(620,32,418);
INSERT INTO "accounts_user_user_permissions" VALUES(621,32,419);
INSERT INTO "accounts_user_user_permissions" VALUES(622,32,420);
INSERT INTO "accounts_user_user_permissions" VALUES(623,32,421);
INSERT INTO "accounts_user_user_permissions" VALUES(624,32,422);
INSERT INTO "accounts_user_user_permissions" VALUES(625,32,423);
INSERT INTO "accounts_user_user_permissions" VALUES(626,32,424);
INSERT INTO "accounts_user_user_permissions" VALUES(627,32,425);
INSERT INTO "accounts_user_user_permissions" VALUES(628,32,426);
INSERT INTO "accounts_user_user_permissions" VALUES(629,32,427);
INSERT INTO "accounts_user_user_permissions" VALUES(630,32,428);
INSERT INTO "accounts_user_user_permissions" VALUES(631,32,429);
INSERT INTO "accounts_user_user_permissions" VALUES(632,32,430);
INSERT INTO "accounts_user_user_permissions" VALUES(633,32,431);
INSERT INTO "accounts_user_user_permissions" VALUES(634,32,432);
INSERT INTO "accounts_user_user_permissions" VALUES(635,32,457);
INSERT INTO "accounts_user_user_permissions" VALUES(636,32,458);
INSERT INTO "accounts_user_user_permissions" VALUES(637,32,459);
INSERT INTO "accounts_user_user_permissions" VALUES(638,32,460);
INSERT INTO "accounts_user_user_permissions" VALUES(639,32,461);
INSERT INTO "accounts_user_user_permissions" VALUES(640,32,462);
INSERT INTO "accounts_user_user_permissions" VALUES(641,32,463);
INSERT INTO "accounts_user_user_permissions" VALUES(642,32,464);
INSERT INTO "accounts_user_user_permissions" VALUES(643,32,465);
INSERT INTO "accounts_user_user_permissions" VALUES(644,32,466);
INSERT INTO "accounts_user_user_permissions" VALUES(645,32,467);
INSERT INTO "accounts_user_user_permissions" VALUES(646,32,468);
INSERT INTO "accounts_user_user_permissions" VALUES(647,32,469);
INSERT INTO "accounts_user_user_permissions" VALUES(648,32,470);
INSERT INTO "accounts_user_user_permissions" VALUES(649,32,471);
INSERT INTO "accounts_user_user_permissions" VALUES(650,32,472);
INSERT INTO "accounts_user_user_permissions" VALUES(651,32,473);
INSERT INTO "accounts_user_user_permissions" VALUES(652,32,474);
INSERT INTO "accounts_user_user_permissions" VALUES(653,32,475);
INSERT INTO "accounts_user_user_permissions" VALUES(654,32,476);
INSERT INTO "accounts_user_user_permissions" VALUES(655,32,477);
INSERT INTO "accounts_user_user_permissions" VALUES(656,32,478);
INSERT INTO "accounts_user_user_permissions" VALUES(657,32,479);
INSERT INTO "accounts_user_user_permissions" VALUES(658,32,480);
INSERT INTO "accounts_user_user_permissions" VALUES(659,32,481);
INSERT INTO "accounts_user_user_permissions" VALUES(660,32,482);
INSERT INTO "accounts_user_user_permissions" VALUES(661,32,483);
INSERT INTO "accounts_user_user_permissions" VALUES(662,32,484);
INSERT INTO "accounts_user_user_permissions" VALUES(663,34,45);
INSERT INTO "accounts_user_user_permissions" VALUES(664,34,46);
INSERT INTO "accounts_user_user_permissions" VALUES(665,34,47);
INSERT INTO "accounts_user_user_permissions" VALUES(666,34,48);
INSERT INTO "accounts_user_user_permissions" VALUES(667,34,49);
INSERT INTO "accounts_user_user_permissions" VALUES(668,34,50);
INSERT INTO "accounts_user_user_permissions" VALUES(669,34,51);
INSERT INTO "accounts_user_user_permissions" VALUES(670,34,52);
INSERT INTO "accounts_user_user_permissions" VALUES(671,34,53);
INSERT INTO "accounts_user_user_permissions" VALUES(672,34,54);
INSERT INTO "accounts_user_user_permissions" VALUES(673,34,55);
INSERT INTO "accounts_user_user_permissions" VALUES(674,34,56);
INSERT INTO "accounts_user_user_permissions" VALUES(675,34,57);
INSERT INTO "accounts_user_user_permissions" VALUES(676,34,58);
INSERT INTO "accounts_user_user_permissions" VALUES(677,34,59);
INSERT INTO "accounts_user_user_permissions" VALUES(678,34,60);
INSERT INTO "accounts_user_user_permissions" VALUES(679,34,61);
INSERT INTO "accounts_user_user_permissions" VALUES(680,34,62);
INSERT INTO "accounts_user_user_permissions" VALUES(681,34,63);
INSERT INTO "accounts_user_user_permissions" VALUES(682,34,64);
INSERT INTO "accounts_user_user_permissions" VALUES(683,34,65);
INSERT INTO "accounts_user_user_permissions" VALUES(684,34,66);
INSERT INTO "accounts_user_user_permissions" VALUES(685,34,67);
INSERT INTO "accounts_user_user_permissions" VALUES(686,34,68);
INSERT INTO "accounts_user_user_permissions" VALUES(687,34,69);
INSERT INTO "accounts_user_user_permissions" VALUES(688,34,70);
INSERT INTO "accounts_user_user_permissions" VALUES(689,34,71);
INSERT INTO "accounts_user_user_permissions" VALUES(690,34,72);
INSERT INTO "accounts_user_user_permissions" VALUES(691,34,73);
INSERT INTO "accounts_user_user_permissions" VALUES(692,34,74);
INSERT INTO "accounts_user_user_permissions" VALUES(693,34,75);
INSERT INTO "accounts_user_user_permissions" VALUES(694,34,76);
INSERT INTO "accounts_user_user_permissions" VALUES(695,34,77);
INSERT INTO "accounts_user_user_permissions" VALUES(696,34,78);
INSERT INTO "accounts_user_user_permissions" VALUES(697,34,79);
INSERT INTO "accounts_user_user_permissions" VALUES(698,34,80);
INSERT INTO "accounts_user_user_permissions" VALUES(699,34,81);
INSERT INTO "accounts_user_user_permissions" VALUES(700,34,82);
INSERT INTO "accounts_user_user_permissions" VALUES(701,34,83);
INSERT INTO "accounts_user_user_permissions" VALUES(702,34,84);
INSERT INTO "accounts_user_user_permissions" VALUES(703,34,85);
INSERT INTO "accounts_user_user_permissions" VALUES(704,34,86);
INSERT INTO "accounts_user_user_permissions" VALUES(705,34,87);
INSERT INTO "accounts_user_user_permissions" VALUES(706,34,88);
INSERT INTO "accounts_user_user_permissions" VALUES(707,34,89);
INSERT INTO "accounts_user_user_permissions" VALUES(708,34,90);
INSERT INTO "accounts_user_user_permissions" VALUES(709,34,91);
INSERT INTO "accounts_user_user_permissions" VALUES(710,34,92);
INSERT INTO "accounts_user_user_permissions" VALUES(711,34,93);
INSERT INTO "accounts_user_user_permissions" VALUES(712,34,94);
INSERT INTO "accounts_user_user_permissions" VALUES(713,34,95);
INSERT INTO "accounts_user_user_permissions" VALUES(714,34,96);
INSERT INTO "accounts_user_user_permissions" VALUES(715,34,97);
INSERT INTO "accounts_user_user_permissions" VALUES(716,34,98);
INSERT INTO "accounts_user_user_permissions" VALUES(717,34,99);
INSERT INTO "accounts_user_user_permissions" VALUES(718,34,100);
INSERT INTO "accounts_user_user_permissions" VALUES(719,34,101);
INSERT INTO "accounts_user_user_permissions" VALUES(720,34,102);
INSERT INTO "accounts_user_user_permissions" VALUES(721,34,103);
INSERT INTO "accounts_user_user_permissions" VALUES(722,34,104);
INSERT INTO "accounts_user_user_permissions" VALUES(723,34,105);
INSERT INTO "accounts_user_user_permissions" VALUES(724,34,106);
INSERT INTO "accounts_user_user_permissions" VALUES(725,34,107);
INSERT INTO "accounts_user_user_permissions" VALUES(726,34,108);
INSERT INTO "accounts_user_user_permissions" VALUES(727,34,109);
INSERT INTO "accounts_user_user_permissions" VALUES(728,34,110);
INSERT INTO "accounts_user_user_permissions" VALUES(729,34,111);
INSERT INTO "accounts_user_user_permissions" VALUES(730,34,112);
INSERT INTO "accounts_user_user_permissions" VALUES(731,34,113);
INSERT INTO "accounts_user_user_permissions" VALUES(732,34,114);
INSERT INTO "accounts_user_user_permissions" VALUES(733,34,115);
INSERT INTO "accounts_user_user_permissions" VALUES(734,34,116);
INSERT INTO "accounts_user_user_permissions" VALUES(735,34,117);
INSERT INTO "accounts_user_user_permissions" VALUES(736,34,118);
INSERT INTO "accounts_user_user_permissions" VALUES(737,34,119);
INSERT INTO "accounts_user_user_permissions" VALUES(738,34,120);
INSERT INTO "accounts_user_user_permissions" VALUES(739,34,121);
INSERT INTO "accounts_user_user_permissions" VALUES(740,34,122);
INSERT INTO "accounts_user_user_permissions" VALUES(741,34,123);
INSERT INTO "accounts_user_user_permissions" VALUES(742,34,124);
INSERT INTO "accounts_user_user_permissions" VALUES(743,34,125);
INSERT INTO "accounts_user_user_permissions" VALUES(744,34,126);
INSERT INTO "accounts_user_user_permissions" VALUES(745,34,127);
INSERT INTO "accounts_user_user_permissions" VALUES(746,34,128);
INSERT INTO "accounts_user_user_permissions" VALUES(747,34,129);
INSERT INTO "accounts_user_user_permissions" VALUES(748,34,130);
INSERT INTO "accounts_user_user_permissions" VALUES(749,34,131);
INSERT INTO "accounts_user_user_permissions" VALUES(750,34,132);
INSERT INTO "accounts_user_user_permissions" VALUES(751,34,137);
INSERT INTO "accounts_user_user_permissions" VALUES(752,34,138);
INSERT INTO "accounts_user_user_permissions" VALUES(753,34,139);
INSERT INTO "accounts_user_user_permissions" VALUES(754,34,140);
INSERT INTO "accounts_user_user_permissions" VALUES(755,34,141);
INSERT INTO "accounts_user_user_permissions" VALUES(756,34,142);
INSERT INTO "accounts_user_user_permissions" VALUES(757,34,143);
INSERT INTO "accounts_user_user_permissions" VALUES(758,34,144);
INSERT INTO "accounts_user_user_permissions" VALUES(759,34,333);
INSERT INTO "accounts_user_user_permissions" VALUES(760,34,334);
INSERT INTO "accounts_user_user_permissions" VALUES(761,34,335);
INSERT INTO "accounts_user_user_permissions" VALUES(762,34,336);
INSERT INTO "accounts_user_user_permissions" VALUES(763,34,337);
INSERT INTO "accounts_user_user_permissions" VALUES(764,34,338);
INSERT INTO "accounts_user_user_permissions" VALUES(765,34,339);
INSERT INTO "accounts_user_user_permissions" VALUES(766,34,340);
INSERT INTO "accounts_user_user_permissions" VALUES(767,34,341);
INSERT INTO "accounts_user_user_permissions" VALUES(768,34,342);
INSERT INTO "accounts_user_user_permissions" VALUES(769,34,343);
INSERT INTO "accounts_user_user_permissions" VALUES(770,34,344);
INSERT INTO "accounts_user_user_permissions" VALUES(771,34,345);
INSERT INTO "accounts_user_user_permissions" VALUES(772,34,346);
INSERT INTO "accounts_user_user_permissions" VALUES(773,34,347);
INSERT INTO "accounts_user_user_permissions" VALUES(774,34,348);
INSERT INTO "accounts_user_user_permissions" VALUES(775,34,349);
INSERT INTO "accounts_user_user_permissions" VALUES(776,34,350);
INSERT INTO "accounts_user_user_permissions" VALUES(777,34,351);
INSERT INTO "accounts_user_user_permissions" VALUES(778,34,352);
INSERT INTO "accounts_user_user_permissions" VALUES(779,34,353);
INSERT INTO "accounts_user_user_permissions" VALUES(780,34,354);
INSERT INTO "accounts_user_user_permissions" VALUES(781,34,355);
INSERT INTO "accounts_user_user_permissions" VALUES(782,34,356);
INSERT INTO "accounts_user_user_permissions" VALUES(783,34,357);
INSERT INTO "accounts_user_user_permissions" VALUES(784,34,358);
INSERT INTO "accounts_user_user_permissions" VALUES(785,34,359);
INSERT INTO "accounts_user_user_permissions" VALUES(786,34,360);
INSERT INTO "accounts_user_user_permissions" VALUES(787,34,361);
INSERT INTO "accounts_user_user_permissions" VALUES(788,34,362);
INSERT INTO "accounts_user_user_permissions" VALUES(789,34,363);
INSERT INTO "accounts_user_user_permissions" VALUES(790,34,364);
INSERT INTO "accounts_user_user_permissions" VALUES(791,34,413);
INSERT INTO "accounts_user_user_permissions" VALUES(792,34,414);
INSERT INTO "accounts_user_user_permissions" VALUES(793,34,415);
INSERT INTO "accounts_user_user_permissions" VALUES(794,34,416);
INSERT INTO "accounts_user_user_permissions" VALUES(795,34,417);
INSERT INTO "accounts_user_user_permissions" VALUES(796,34,418);
INSERT INTO "accounts_user_user_permissions" VALUES(797,34,419);
INSERT INTO "accounts_user_user_permissions" VALUES(798,34,420);
INSERT INTO "accounts_user_user_permissions" VALUES(799,34,421);
INSERT INTO "accounts_user_user_permissions" VALUES(800,34,422);
INSERT INTO "accounts_user_user_permissions" VALUES(801,34,423);
INSERT INTO "accounts_user_user_permissions" VALUES(802,34,424);
INSERT INTO "accounts_user_user_permissions" VALUES(803,34,425);
INSERT INTO "accounts_user_user_permissions" VALUES(804,34,426);
INSERT INTO "accounts_user_user_permissions" VALUES(805,34,427);
INSERT INTO "accounts_user_user_permissions" VALUES(806,34,428);
INSERT INTO "accounts_user_user_permissions" VALUES(807,34,429);
INSERT INTO "accounts_user_user_permissions" VALUES(808,34,430);
INSERT INTO "accounts_user_user_permissions" VALUES(809,34,431);
INSERT INTO "accounts_user_user_permissions" VALUES(810,34,432);
INSERT INTO "accounts_user_user_permissions" VALUES(811,34,457);
INSERT INTO "accounts_user_user_permissions" VALUES(812,34,458);
INSERT INTO "accounts_user_user_permissions" VALUES(813,34,459);
INSERT INTO "accounts_user_user_permissions" VALUES(814,34,460);
INSERT INTO "accounts_user_user_permissions" VALUES(815,34,461);
INSERT INTO "accounts_user_user_permissions" VALUES(816,34,462);
INSERT INTO "accounts_user_user_permissions" VALUES(817,34,463);
INSERT INTO "accounts_user_user_permissions" VALUES(818,34,464);
INSERT INTO "accounts_user_user_permissions" VALUES(819,34,465);
INSERT INTO "accounts_user_user_permissions" VALUES(820,34,466);
INSERT INTO "accounts_user_user_permissions" VALUES(821,34,467);
INSERT INTO "accounts_user_user_permissions" VALUES(822,34,468);
INSERT INTO "accounts_user_user_permissions" VALUES(823,34,469);
INSERT INTO "accounts_user_user_permissions" VALUES(824,34,470);
INSERT INTO "accounts_user_user_permissions" VALUES(825,34,471);
INSERT INTO "accounts_user_user_permissions" VALUES(826,34,472);
INSERT INTO "accounts_user_user_permissions" VALUES(827,34,473);
INSERT INTO "accounts_user_user_permissions" VALUES(828,34,474);
INSERT INTO "accounts_user_user_permissions" VALUES(829,34,475);
INSERT INTO "accounts_user_user_permissions" VALUES(830,34,476);
INSERT INTO "accounts_user_user_permissions" VALUES(831,34,477);
INSERT INTO "accounts_user_user_permissions" VALUES(832,34,478);
INSERT INTO "accounts_user_user_permissions" VALUES(833,34,479);
INSERT INTO "accounts_user_user_permissions" VALUES(834,34,480);
INSERT INTO "accounts_user_user_permissions" VALUES(835,34,481);
INSERT INTO "accounts_user_user_permissions" VALUES(836,34,482);
INSERT INTO "accounts_user_user_permissions" VALUES(837,34,483);
INSERT INTO "accounts_user_user_permissions" VALUES(838,34,484);
CREATE TABLE "accounts_workhistory" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "change_type" varchar(50) NOT NULL, "effective_date" date NOT NULL, "old_position" varchar(200) NOT NULL, "new_position" varchar(200) NOT NULL, "reason" text NOT NULL, "notes" text NOT NULL, "created_at" datetime NOT NULL, "approved_by_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "created_by_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "new_department_id" bigint NULL REFERENCES "departments_department" ("id") DEFERRABLE INITIALLY DEFERRED, "old_department_id" bigint NULL REFERENCES "departments_department" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "audit_auditlog" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "action" varchar(20) NOT NULL, "model_name" varchar(100) NOT NULL, "object_id" varchar(50) NOT NULL, "changes" text NOT NULL CHECK ((JSON_VALID("changes") OR "changes" IS NULL)), "ip_address" char(39) NULL, "user_agent" text NOT NULL, "created_at" datetime NOT NULL, "user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "auth_group" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(150) NOT NULL UNIQUE);
INSERT INTO "auth_group" VALUES(1,'q360');
INSERT INTO "auth_group" VALUES(2,'TahmazMuradov');
CREATE TABLE "auth_group_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "auth_group_permissions" VALUES(1,1,1);
INSERT INTO "auth_group_permissions" VALUES(2,1,2);
INSERT INTO "auth_group_permissions" VALUES(3,1,3);
INSERT INTO "auth_group_permissions" VALUES(4,1,4);
INSERT INTO "auth_group_permissions" VALUES(5,1,5);
INSERT INTO "auth_group_permissions" VALUES(6,1,6);
INSERT INTO "auth_group_permissions" VALUES(7,1,7);
INSERT INTO "auth_group_permissions" VALUES(8,1,8);
INSERT INTO "auth_group_permissions" VALUES(9,1,9);
INSERT INTO "auth_group_permissions" VALUES(10,1,10);
INSERT INTO "auth_group_permissions" VALUES(11,1,11);
INSERT INTO "auth_group_permissions" VALUES(12,1,12);
INSERT INTO "auth_group_permissions" VALUES(13,1,13);
INSERT INTO "auth_group_permissions" VALUES(14,1,14);
INSERT INTO "auth_group_permissions" VALUES(15,1,15);
INSERT INTO "auth_group_permissions" VALUES(16,1,16);
INSERT INTO "auth_group_permissions" VALUES(17,1,17);
INSERT INTO "auth_group_permissions" VALUES(18,1,18);
INSERT INTO "auth_group_permissions" VALUES(19,1,19);
INSERT INTO "auth_group_permissions" VALUES(20,1,20);
INSERT INTO "auth_group_permissions" VALUES(21,1,21);
INSERT INTO "auth_group_permissions" VALUES(22,1,22);
INSERT INTO "auth_group_permissions" VALUES(23,1,23);
INSERT INTO "auth_group_permissions" VALUES(24,1,24);
INSERT INTO "auth_group_permissions" VALUES(25,1,25);
INSERT INTO "auth_group_permissions" VALUES(26,1,26);
INSERT INTO "auth_group_permissions" VALUES(27,1,27);
INSERT INTO "auth_group_permissions" VALUES(28,1,28);
INSERT INTO "auth_group_permissions" VALUES(29,1,29);
INSERT INTO "auth_group_permissions" VALUES(30,1,30);
INSERT INTO "auth_group_permissions" VALUES(31,1,31);
INSERT INTO "auth_group_permissions" VALUES(32,1,32);
INSERT INTO "auth_group_permissions" VALUES(33,1,33);
INSERT INTO "auth_group_permissions" VALUES(34,1,34);
INSERT INTO "auth_group_permissions" VALUES(35,1,35);
INSERT INTO "auth_group_permissions" VALUES(36,1,36);
INSERT INTO "auth_group_permissions" VALUES(37,1,37);
INSERT INTO "auth_group_permissions" VALUES(38,1,38);
INSERT INTO "auth_group_permissions" VALUES(39,1,39);
INSERT INTO "auth_group_permissions" VALUES(40,1,40);
INSERT INTO "auth_group_permissions" VALUES(41,1,41);
INSERT INTO "auth_group_permissions" VALUES(42,1,42);
INSERT INTO "auth_group_permissions" VALUES(43,1,43);
INSERT INTO "auth_group_permissions" VALUES(44,1,44);
INSERT INTO "auth_group_permissions" VALUES(45,1,45);
INSERT INTO "auth_group_permissions" VALUES(46,1,46);
INSERT INTO "auth_group_permissions" VALUES(47,1,47);
INSERT INTO "auth_group_permissions" VALUES(48,1,48);
INSERT INTO "auth_group_permissions" VALUES(49,1,49);
INSERT INTO "auth_group_permissions" VALUES(50,1,50);
INSERT INTO "auth_group_permissions" VALUES(51,1,51);
INSERT INTO "auth_group_permissions" VALUES(52,1,52);
INSERT INTO "auth_group_permissions" VALUES(53,1,53);
INSERT INTO "auth_group_permissions" VALUES(54,1,54);
INSERT INTO "auth_group_permissions" VALUES(55,1,55);
INSERT INTO "auth_group_permissions" VALUES(56,1,56);
INSERT INTO "auth_group_permissions" VALUES(57,1,57);
INSERT INTO "auth_group_permissions" VALUES(58,1,58);
INSERT INTO "auth_group_permissions" VALUES(59,1,59);
INSERT INTO "auth_group_permissions" VALUES(60,1,60);
INSERT INTO "auth_group_permissions" VALUES(61,1,61);
INSERT INTO "auth_group_permissions" VALUES(62,1,62);
INSERT INTO "auth_group_permissions" VALUES(63,1,63);
INSERT INTO "auth_group_permissions" VALUES(64,1,64);
INSERT INTO "auth_group_permissions" VALUES(65,1,65);
INSERT INTO "auth_group_permissions" VALUES(66,1,66);
INSERT INTO "auth_group_permissions" VALUES(67,1,67);
INSERT INTO "auth_group_permissions" VALUES(68,1,68);
INSERT INTO "auth_group_permissions" VALUES(69,1,69);
INSERT INTO "auth_group_permissions" VALUES(70,1,70);
INSERT INTO "auth_group_permissions" VALUES(71,1,71);
INSERT INTO "auth_group_permissions" VALUES(72,1,72);
INSERT INTO "auth_group_permissions" VALUES(73,1,73);
INSERT INTO "auth_group_permissions" VALUES(74,1,74);
INSERT INTO "auth_group_permissions" VALUES(75,1,75);
INSERT INTO "auth_group_permissions" VALUES(76,1,76);
INSERT INTO "auth_group_permissions" VALUES(77,1,77);
INSERT INTO "auth_group_permissions" VALUES(78,1,78);
INSERT INTO "auth_group_permissions" VALUES(79,1,79);
INSERT INTO "auth_group_permissions" VALUES(80,1,80);
INSERT INTO "auth_group_permissions" VALUES(81,1,81);
INSERT INTO "auth_group_permissions" VALUES(82,1,82);
INSERT INTO "auth_group_permissions" VALUES(83,1,83);
INSERT INTO "auth_group_permissions" VALUES(84,1,84);
INSERT INTO "auth_group_permissions" VALUES(85,1,85);
INSERT INTO "auth_group_permissions" VALUES(86,1,86);
INSERT INTO "auth_group_permissions" VALUES(87,1,87);
INSERT INTO "auth_group_permissions" VALUES(88,1,88);
INSERT INTO "auth_group_permissions" VALUES(89,1,89);
INSERT INTO "auth_group_permissions" VALUES(90,1,90);
INSERT INTO "auth_group_permissions" VALUES(91,1,91);
INSERT INTO "auth_group_permissions" VALUES(92,1,92);
INSERT INTO "auth_group_permissions" VALUES(93,1,93);
INSERT INTO "auth_group_permissions" VALUES(94,1,94);
INSERT INTO "auth_group_permissions" VALUES(95,1,95);
INSERT INTO "auth_group_permissions" VALUES(96,1,96);
INSERT INTO "auth_group_permissions" VALUES(97,1,97);
INSERT INTO "auth_group_permissions" VALUES(98,1,98);
INSERT INTO "auth_group_permissions" VALUES(99,1,99);
INSERT INTO "auth_group_permissions" VALUES(100,1,100);
INSERT INTO "auth_group_permissions" VALUES(101,1,101);
INSERT INTO "auth_group_permissions" VALUES(102,1,102);
INSERT INTO "auth_group_permissions" VALUES(103,1,103);
INSERT INTO "auth_group_permissions" VALUES(104,1,104);
INSERT INTO "auth_group_permissions" VALUES(105,1,105);
INSERT INTO "auth_group_permissions" VALUES(106,1,106);
INSERT INTO "auth_group_permissions" VALUES(107,1,107);
INSERT INTO "auth_group_permissions" VALUES(108,1,108);
INSERT INTO "auth_group_permissions" VALUES(109,1,109);
INSERT INTO "auth_group_permissions" VALUES(110,1,110);
INSERT INTO "auth_group_permissions" VALUES(111,1,111);
INSERT INTO "auth_group_permissions" VALUES(112,1,112);
INSERT INTO "auth_group_permissions" VALUES(113,1,113);
INSERT INTO "auth_group_permissions" VALUES(114,1,114);
INSERT INTO "auth_group_permissions" VALUES(115,1,115);
INSERT INTO "auth_group_permissions" VALUES(116,1,116);
INSERT INTO "auth_group_permissions" VALUES(117,1,117);
INSERT INTO "auth_group_permissions" VALUES(118,1,118);
INSERT INTO "auth_group_permissions" VALUES(119,1,119);
INSERT INTO "auth_group_permissions" VALUES(120,1,120);
INSERT INTO "auth_group_permissions" VALUES(121,1,121);
INSERT INTO "auth_group_permissions" VALUES(122,1,122);
INSERT INTO "auth_group_permissions" VALUES(123,1,123);
INSERT INTO "auth_group_permissions" VALUES(124,1,124);
INSERT INTO "auth_group_permissions" VALUES(125,1,125);
INSERT INTO "auth_group_permissions" VALUES(126,1,126);
INSERT INTO "auth_group_permissions" VALUES(127,1,127);
INSERT INTO "auth_group_permissions" VALUES(128,1,128);
INSERT INTO "auth_group_permissions" VALUES(129,1,129);
INSERT INTO "auth_group_permissions" VALUES(130,1,130);
INSERT INTO "auth_group_permissions" VALUES(131,1,131);
INSERT INTO "auth_group_permissions" VALUES(132,1,132);
INSERT INTO "auth_group_permissions" VALUES(133,1,133);
INSERT INTO "auth_group_permissions" VALUES(134,1,134);
INSERT INTO "auth_group_permissions" VALUES(135,1,135);
INSERT INTO "auth_group_permissions" VALUES(136,1,136);
INSERT INTO "auth_group_permissions" VALUES(137,2,1);
INSERT INTO "auth_group_permissions" VALUES(138,2,2);
INSERT INTO "auth_group_permissions" VALUES(139,2,3);
INSERT INTO "auth_group_permissions" VALUES(140,2,4);
INSERT INTO "auth_group_permissions" VALUES(141,2,5);
INSERT INTO "auth_group_permissions" VALUES(142,2,6);
INSERT INTO "auth_group_permissions" VALUES(143,2,7);
INSERT INTO "auth_group_permissions" VALUES(144,2,8);
INSERT INTO "auth_group_permissions" VALUES(145,2,9);
INSERT INTO "auth_group_permissions" VALUES(146,2,10);
INSERT INTO "auth_group_permissions" VALUES(147,2,11);
INSERT INTO "auth_group_permissions" VALUES(148,2,12);
INSERT INTO "auth_group_permissions" VALUES(149,2,13);
INSERT INTO "auth_group_permissions" VALUES(150,2,14);
INSERT INTO "auth_group_permissions" VALUES(151,2,15);
INSERT INTO "auth_group_permissions" VALUES(152,2,16);
INSERT INTO "auth_group_permissions" VALUES(153,2,17);
INSERT INTO "auth_group_permissions" VALUES(154,2,18);
INSERT INTO "auth_group_permissions" VALUES(155,2,19);
INSERT INTO "auth_group_permissions" VALUES(156,2,20);
INSERT INTO "auth_group_permissions" VALUES(157,2,21);
INSERT INTO "auth_group_permissions" VALUES(158,2,22);
INSERT INTO "auth_group_permissions" VALUES(159,2,23);
INSERT INTO "auth_group_permissions" VALUES(160,2,24);
INSERT INTO "auth_group_permissions" VALUES(161,2,25);
INSERT INTO "auth_group_permissions" VALUES(162,2,26);
INSERT INTO "auth_group_permissions" VALUES(163,2,27);
INSERT INTO "auth_group_permissions" VALUES(164,2,28);
INSERT INTO "auth_group_permissions" VALUES(165,2,29);
INSERT INTO "auth_group_permissions" VALUES(166,2,30);
INSERT INTO "auth_group_permissions" VALUES(167,2,31);
INSERT INTO "auth_group_permissions" VALUES(168,2,32);
INSERT INTO "auth_group_permissions" VALUES(169,2,33);
INSERT INTO "auth_group_permissions" VALUES(170,2,34);
INSERT INTO "auth_group_permissions" VALUES(171,2,35);
INSERT INTO "auth_group_permissions" VALUES(172,2,36);
INSERT INTO "auth_group_permissions" VALUES(173,2,37);
INSERT INTO "auth_group_permissions" VALUES(174,2,38);
INSERT INTO "auth_group_permissions" VALUES(175,2,39);
INSERT INTO "auth_group_permissions" VALUES(176,2,40);
INSERT INTO "auth_group_permissions" VALUES(177,2,41);
INSERT INTO "auth_group_permissions" VALUES(178,2,42);
INSERT INTO "auth_group_permissions" VALUES(179,2,43);
INSERT INTO "auth_group_permissions" VALUES(180,2,44);
INSERT INTO "auth_group_permissions" VALUES(181,2,45);
INSERT INTO "auth_group_permissions" VALUES(182,2,46);
INSERT INTO "auth_group_permissions" VALUES(183,2,47);
INSERT INTO "auth_group_permissions" VALUES(184,2,48);
INSERT INTO "auth_group_permissions" VALUES(185,2,49);
INSERT INTO "auth_group_permissions" VALUES(186,2,50);
INSERT INTO "auth_group_permissions" VALUES(187,2,51);
INSERT INTO "auth_group_permissions" VALUES(188,2,52);
INSERT INTO "auth_group_permissions" VALUES(189,2,53);
INSERT INTO "auth_group_permissions" VALUES(190,2,54);
INSERT INTO "auth_group_permissions" VALUES(191,2,55);
INSERT INTO "auth_group_permissions" VALUES(192,2,56);
INSERT INTO "auth_group_permissions" VALUES(193,2,57);
INSERT INTO "auth_group_permissions" VALUES(194,2,58);
INSERT INTO "auth_group_permissions" VALUES(195,2,59);
INSERT INTO "auth_group_permissions" VALUES(196,2,60);
INSERT INTO "auth_group_permissions" VALUES(197,2,61);
INSERT INTO "auth_group_permissions" VALUES(198,2,62);
INSERT INTO "auth_group_permissions" VALUES(199,2,63);
INSERT INTO "auth_group_permissions" VALUES(200,2,64);
INSERT INTO "auth_group_permissions" VALUES(201,2,65);
INSERT INTO "auth_group_permissions" VALUES(202,2,66);
INSERT INTO "auth_group_permissions" VALUES(203,2,67);
INSERT INTO "auth_group_permissions" VALUES(204,2,68);
INSERT INTO "auth_group_permissions" VALUES(205,2,69);
INSERT INTO "auth_group_permissions" VALUES(206,2,70);
INSERT INTO "auth_group_permissions" VALUES(207,2,71);
INSERT INTO "auth_group_permissions" VALUES(208,2,72);
INSERT INTO "auth_group_permissions" VALUES(209,2,73);
INSERT INTO "auth_group_permissions" VALUES(210,2,74);
INSERT INTO "auth_group_permissions" VALUES(211,2,75);
INSERT INTO "auth_group_permissions" VALUES(212,2,76);
INSERT INTO "auth_group_permissions" VALUES(213,2,77);
INSERT INTO "auth_group_permissions" VALUES(214,2,78);
INSERT INTO "auth_group_permissions" VALUES(215,2,79);
INSERT INTO "auth_group_permissions" VALUES(216,2,80);
INSERT INTO "auth_group_permissions" VALUES(217,2,81);
INSERT INTO "auth_group_permissions" VALUES(218,2,82);
INSERT INTO "auth_group_permissions" VALUES(219,2,83);
INSERT INTO "auth_group_permissions" VALUES(220,2,84);
INSERT INTO "auth_group_permissions" VALUES(221,2,85);
INSERT INTO "auth_group_permissions" VALUES(222,2,86);
INSERT INTO "auth_group_permissions" VALUES(223,2,87);
INSERT INTO "auth_group_permissions" VALUES(224,2,88);
INSERT INTO "auth_group_permissions" VALUES(225,2,89);
INSERT INTO "auth_group_permissions" VALUES(226,2,90);
INSERT INTO "auth_group_permissions" VALUES(227,2,91);
INSERT INTO "auth_group_permissions" VALUES(228,2,92);
INSERT INTO "auth_group_permissions" VALUES(229,2,93);
INSERT INTO "auth_group_permissions" VALUES(230,2,94);
INSERT INTO "auth_group_permissions" VALUES(231,2,95);
INSERT INTO "auth_group_permissions" VALUES(232,2,96);
INSERT INTO "auth_group_permissions" VALUES(233,2,97);
INSERT INTO "auth_group_permissions" VALUES(234,2,98);
INSERT INTO "auth_group_permissions" VALUES(235,2,99);
INSERT INTO "auth_group_permissions" VALUES(236,2,100);
INSERT INTO "auth_group_permissions" VALUES(237,2,101);
INSERT INTO "auth_group_permissions" VALUES(238,2,102);
INSERT INTO "auth_group_permissions" VALUES(239,2,103);
INSERT INTO "auth_group_permissions" VALUES(240,2,104);
INSERT INTO "auth_group_permissions" VALUES(241,2,105);
INSERT INTO "auth_group_permissions" VALUES(242,2,106);
INSERT INTO "auth_group_permissions" VALUES(243,2,107);
INSERT INTO "auth_group_permissions" VALUES(244,2,108);
INSERT INTO "auth_group_permissions" VALUES(245,2,109);
INSERT INTO "auth_group_permissions" VALUES(246,2,110);
INSERT INTO "auth_group_permissions" VALUES(247,2,111);
INSERT INTO "auth_group_permissions" VALUES(248,2,112);
INSERT INTO "auth_group_permissions" VALUES(249,2,113);
INSERT INTO "auth_group_permissions" VALUES(250,2,114);
INSERT INTO "auth_group_permissions" VALUES(251,2,115);
INSERT INTO "auth_group_permissions" VALUES(252,2,116);
INSERT INTO "auth_group_permissions" VALUES(253,2,117);
INSERT INTO "auth_group_permissions" VALUES(254,2,118);
INSERT INTO "auth_group_permissions" VALUES(255,2,119);
INSERT INTO "auth_group_permissions" VALUES(256,2,120);
INSERT INTO "auth_group_permissions" VALUES(257,2,121);
INSERT INTO "auth_group_permissions" VALUES(258,2,122);
INSERT INTO "auth_group_permissions" VALUES(259,2,123);
INSERT INTO "auth_group_permissions" VALUES(260,2,124);
INSERT INTO "auth_group_permissions" VALUES(261,2,125);
INSERT INTO "auth_group_permissions" VALUES(262,2,126);
INSERT INTO "auth_group_permissions" VALUES(263,2,127);
INSERT INTO "auth_group_permissions" VALUES(264,2,128);
INSERT INTO "auth_group_permissions" VALUES(265,2,129);
INSERT INTO "auth_group_permissions" VALUES(266,2,130);
INSERT INTO "auth_group_permissions" VALUES(267,2,131);
INSERT INTO "auth_group_permissions" VALUES(268,2,132);
INSERT INTO "auth_group_permissions" VALUES(269,2,133);
INSERT INTO "auth_group_permissions" VALUES(270,2,134);
INSERT INTO "auth_group_permissions" VALUES(271,2,135);
INSERT INTO "auth_group_permissions" VALUES(272,2,136);
INSERT INTO "auth_group_permissions" VALUES(273,2,137);
INSERT INTO "auth_group_permissions" VALUES(274,2,138);
INSERT INTO "auth_group_permissions" VALUES(275,2,139);
INSERT INTO "auth_group_permissions" VALUES(276,2,140);
INSERT INTO "auth_group_permissions" VALUES(277,2,141);
INSERT INTO "auth_group_permissions" VALUES(278,2,142);
INSERT INTO "auth_group_permissions" VALUES(279,2,143);
INSERT INTO "auth_group_permissions" VALUES(280,2,144);
INSERT INTO "auth_group_permissions" VALUES(281,2,145);
INSERT INTO "auth_group_permissions" VALUES(282,2,146);
INSERT INTO "auth_group_permissions" VALUES(283,2,147);
INSERT INTO "auth_group_permissions" VALUES(284,2,148);
INSERT INTO "auth_group_permissions" VALUES(285,2,149);
INSERT INTO "auth_group_permissions" VALUES(286,2,150);
INSERT INTO "auth_group_permissions" VALUES(287,2,151);
INSERT INTO "auth_group_permissions" VALUES(288,2,152);
INSERT INTO "auth_group_permissions" VALUES(289,2,153);
INSERT INTO "auth_group_permissions" VALUES(290,2,154);
INSERT INTO "auth_group_permissions" VALUES(291,2,155);
INSERT INTO "auth_group_permissions" VALUES(292,2,156);
INSERT INTO "auth_group_permissions" VALUES(293,2,157);
INSERT INTO "auth_group_permissions" VALUES(294,2,158);
INSERT INTO "auth_group_permissions" VALUES(295,2,159);
INSERT INTO "auth_group_permissions" VALUES(296,2,160);
INSERT INTO "auth_group_permissions" VALUES(297,2,161);
INSERT INTO "auth_group_permissions" VALUES(298,2,162);
INSERT INTO "auth_group_permissions" VALUES(299,2,163);
INSERT INTO "auth_group_permissions" VALUES(300,2,164);
INSERT INTO "auth_group_permissions" VALUES(301,2,165);
INSERT INTO "auth_group_permissions" VALUES(302,2,166);
INSERT INTO "auth_group_permissions" VALUES(303,2,167);
INSERT INTO "auth_group_permissions" VALUES(304,2,168);
INSERT INTO "auth_group_permissions" VALUES(305,2,169);
INSERT INTO "auth_group_permissions" VALUES(306,2,170);
INSERT INTO "auth_group_permissions" VALUES(307,2,171);
INSERT INTO "auth_group_permissions" VALUES(308,2,172);
INSERT INTO "auth_group_permissions" VALUES(309,2,173);
INSERT INTO "auth_group_permissions" VALUES(310,2,174);
INSERT INTO "auth_group_permissions" VALUES(311,2,175);
INSERT INTO "auth_group_permissions" VALUES(312,2,176);
INSERT INTO "auth_group_permissions" VALUES(313,2,177);
INSERT INTO "auth_group_permissions" VALUES(314,2,178);
INSERT INTO "auth_group_permissions" VALUES(315,2,179);
INSERT INTO "auth_group_permissions" VALUES(316,2,180);
INSERT INTO "auth_group_permissions" VALUES(317,2,181);
INSERT INTO "auth_group_permissions" VALUES(318,2,182);
INSERT INTO "auth_group_permissions" VALUES(319,2,183);
INSERT INTO "auth_group_permissions" VALUES(320,2,184);
INSERT INTO "auth_group_permissions" VALUES(321,2,185);
INSERT INTO "auth_group_permissions" VALUES(322,2,186);
INSERT INTO "auth_group_permissions" VALUES(323,2,187);
INSERT INTO "auth_group_permissions" VALUES(324,2,188);
INSERT INTO "auth_group_permissions" VALUES(325,2,189);
INSERT INTO "auth_group_permissions" VALUES(326,2,190);
INSERT INTO "auth_group_permissions" VALUES(327,2,191);
INSERT INTO "auth_group_permissions" VALUES(328,2,192);
INSERT INTO "auth_group_permissions" VALUES(329,2,193);
INSERT INTO "auth_group_permissions" VALUES(330,2,194);
INSERT INTO "auth_group_permissions" VALUES(331,2,195);
INSERT INTO "auth_group_permissions" VALUES(332,2,196);
INSERT INTO "auth_group_permissions" VALUES(333,2,197);
INSERT INTO "auth_group_permissions" VALUES(334,2,198);
INSERT INTO "auth_group_permissions" VALUES(335,2,199);
INSERT INTO "auth_group_permissions" VALUES(336,2,200);
INSERT INTO "auth_group_permissions" VALUES(337,2,201);
INSERT INTO "auth_group_permissions" VALUES(338,2,202);
INSERT INTO "auth_group_permissions" VALUES(339,2,203);
INSERT INTO "auth_group_permissions" VALUES(340,2,204);
INSERT INTO "auth_group_permissions" VALUES(341,2,205);
INSERT INTO "auth_group_permissions" VALUES(342,2,206);
INSERT INTO "auth_group_permissions" VALUES(343,2,207);
INSERT INTO "auth_group_permissions" VALUES(344,2,208);
INSERT INTO "auth_group_permissions" VALUES(345,2,209);
INSERT INTO "auth_group_permissions" VALUES(346,2,210);
INSERT INTO "auth_group_permissions" VALUES(347,2,211);
INSERT INTO "auth_group_permissions" VALUES(348,2,212);
INSERT INTO "auth_group_permissions" VALUES(349,2,213);
INSERT INTO "auth_group_permissions" VALUES(350,2,214);
INSERT INTO "auth_group_permissions" VALUES(351,2,215);
INSERT INTO "auth_group_permissions" VALUES(352,2,216);
INSERT INTO "auth_group_permissions" VALUES(353,2,217);
INSERT INTO "auth_group_permissions" VALUES(354,2,218);
INSERT INTO "auth_group_permissions" VALUES(355,2,219);
INSERT INTO "auth_group_permissions" VALUES(356,2,220);
INSERT INTO "auth_group_permissions" VALUES(357,2,221);
INSERT INTO "auth_group_permissions" VALUES(358,2,222);
INSERT INTO "auth_group_permissions" VALUES(359,2,223);
INSERT INTO "auth_group_permissions" VALUES(360,2,224);
INSERT INTO "auth_group_permissions" VALUES(361,2,225);
INSERT INTO "auth_group_permissions" VALUES(362,2,226);
INSERT INTO "auth_group_permissions" VALUES(363,2,227);
INSERT INTO "auth_group_permissions" VALUES(364,2,228);
INSERT INTO "auth_group_permissions" VALUES(365,2,229);
INSERT INTO "auth_group_permissions" VALUES(366,2,230);
INSERT INTO "auth_group_permissions" VALUES(367,2,231);
INSERT INTO "auth_group_permissions" VALUES(368,2,232);
INSERT INTO "auth_group_permissions" VALUES(369,2,233);
INSERT INTO "auth_group_permissions" VALUES(370,2,234);
INSERT INTO "auth_group_permissions" VALUES(371,2,235);
INSERT INTO "auth_group_permissions" VALUES(372,2,236);
CREATE TABLE "auth_permission" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "codename" varchar(100) NOT NULL, "name" varchar(255) NOT NULL);
INSERT INTO "auth_permission" VALUES(1,1,'add_logentry','Can add log entry');
INSERT INTO "auth_permission" VALUES(2,1,'change_logentry','Can change log entry');
INSERT INTO "auth_permission" VALUES(3,1,'delete_logentry','Can delete log entry');
INSERT INTO "auth_permission" VALUES(4,1,'view_logentry','Can view log entry');
INSERT INTO "auth_permission" VALUES(5,2,'add_permission','Can add permission');
INSERT INTO "auth_permission" VALUES(6,2,'change_permission','Can change permission');
INSERT INTO "auth_permission" VALUES(7,2,'delete_permission','Can delete permission');
INSERT INTO "auth_permission" VALUES(8,2,'view_permission','Can view permission');
INSERT INTO "auth_permission" VALUES(9,3,'add_group','Can add group');
INSERT INTO "auth_permission" VALUES(10,3,'change_group','Can change group');
INSERT INTO "auth_permission" VALUES(11,3,'delete_group','Can delete group');
INSERT INTO "auth_permission" VALUES(12,3,'view_group','Can view group');
INSERT INTO "auth_permission" VALUES(13,4,'add_contenttype','Can add content type');
INSERT INTO "auth_permission" VALUES(14,4,'change_contenttype','Can change content type');
INSERT INTO "auth_permission" VALUES(15,4,'delete_contenttype','Can delete content type');
INSERT INTO "auth_permission" VALUES(16,4,'view_contenttype','Can view content type');
INSERT INTO "auth_permission" VALUES(17,5,'add_session','Can add session');
INSERT INTO "auth_permission" VALUES(18,5,'change_session','Can change session');
INSERT INTO "auth_permission" VALUES(19,5,'delete_session','Can delete session');
INSERT INTO "auth_permission" VALUES(20,5,'view_session','Can view session');
INSERT INTO "auth_permission" VALUES(21,6,'add_user','Can add İstifadəçi');
INSERT INTO "auth_permission" VALUES(22,6,'change_user','Can change İstifadəçi');
INSERT INTO "auth_permission" VALUES(23,6,'delete_user','Can delete İstifadəçi');
INSERT INTO "auth_permission" VALUES(24,6,'view_user','Can view İstifadəçi');
INSERT INTO "auth_permission" VALUES(25,7,'add_historicalprofile','Can add historical Profil');
INSERT INTO "auth_permission" VALUES(26,7,'change_historicalprofile','Can change historical Profil');
INSERT INTO "auth_permission" VALUES(27,7,'delete_historicalprofile','Can delete historical Profil');
INSERT INTO "auth_permission" VALUES(28,7,'view_historicalprofile','Can view historical Profil');
INSERT INTO "auth_permission" VALUES(29,8,'add_historicalrole','Can add historical Rol');
INSERT INTO "auth_permission" VALUES(30,8,'change_historicalrole','Can change historical Rol');
INSERT INTO "auth_permission" VALUES(31,8,'delete_historicalrole','Can delete historical Rol');
INSERT INTO "auth_permission" VALUES(32,8,'view_historicalrole','Can view historical Rol');
INSERT INTO "auth_permission" VALUES(33,9,'add_historicaluser','Can add historical İstifadəçi');
INSERT INTO "auth_permission" VALUES(34,9,'change_historicaluser','Can change historical İstifadəçi');
INSERT INTO "auth_permission" VALUES(35,9,'delete_historicaluser','Can delete historical İstifadəçi');
INSERT INTO "auth_permission" VALUES(36,9,'view_historicaluser','Can view historical İstifadəçi');
INSERT INTO "auth_permission" VALUES(37,10,'add_role','Can add Rol');
INSERT INTO "auth_permission" VALUES(38,10,'change_role','Can change Rol');
INSERT INTO "auth_permission" VALUES(39,10,'delete_role','Can delete Rol');
INSERT INTO "auth_permission" VALUES(40,10,'view_role','Can view Rol');
INSERT INTO "auth_permission" VALUES(41,11,'add_profile','Can add Profil');
INSERT INTO "auth_permission" VALUES(42,11,'change_profile','Can change Profil');
INSERT INTO "auth_permission" VALUES(43,11,'delete_profile','Can delete Profil');
INSERT INTO "auth_permission" VALUES(44,11,'view_profile','Can view Profil');
INSERT INTO "auth_permission" VALUES(45,12,'add_department','Can add Şöbə');
INSERT INTO "auth_permission" VALUES(46,12,'change_department','Can change Şöbə');
INSERT INTO "auth_permission" VALUES(47,12,'delete_department','Can delete Şöbə');
INSERT INTO "auth_permission" VALUES(48,12,'view_department','Can view Şöbə');
INSERT INTO "auth_permission" VALUES(49,13,'add_historicaldepartment','Can add historical Şöbə');
INSERT INTO "auth_permission" VALUES(50,13,'change_historicaldepartment','Can change historical Şöbə');
INSERT INTO "auth_permission" VALUES(51,13,'delete_historicaldepartment','Can delete historical Şöbə');
INSERT INTO "auth_permission" VALUES(52,13,'view_historicaldepartment','Can view historical Şöbə');
INSERT INTO "auth_permission" VALUES(53,14,'add_historicalorganization','Can add historical Təşkilat');
INSERT INTO "auth_permission" VALUES(54,14,'change_historicalorganization','Can change historical Təşkilat');
INSERT INTO "auth_permission" VALUES(55,14,'delete_historicalorganization','Can delete historical Təşkilat');
INSERT INTO "auth_permission" VALUES(56,14,'view_historicalorganization','Can view historical Təşkilat');
INSERT INTO "auth_permission" VALUES(57,15,'add_historicalposition','Can add historical Vəzifə');
INSERT INTO "auth_permission" VALUES(58,15,'change_historicalposition','Can change historical Vəzifə');
INSERT INTO "auth_permission" VALUES(59,15,'delete_historicalposition','Can delete historical Vəzifə');
INSERT INTO "auth_permission" VALUES(60,15,'view_historicalposition','Can view historical Vəzifə');
INSERT INTO "auth_permission" VALUES(61,16,'add_organization','Can add Təşkilat');
INSERT INTO "auth_permission" VALUES(62,16,'change_organization','Can change Təşkilat');
INSERT INTO "auth_permission" VALUES(63,16,'delete_organization','Can delete Təşkilat');
INSERT INTO "auth_permission" VALUES(64,16,'view_organization','Can view Təşkilat');
INSERT INTO "auth_permission" VALUES(65,17,'add_position','Can add Vəzifə');
INSERT INTO "auth_permission" VALUES(66,17,'change_position','Can change Vəzifə');
INSERT INTO "auth_permission" VALUES(67,17,'delete_position','Can delete Vəzifə');
INSERT INTO "auth_permission" VALUES(68,17,'view_position','Can view Vəzifə');
INSERT INTO "auth_permission" VALUES(69,18,'add_evaluationcampaign','Can add Qiymətləndirmə Kampaniyası');
INSERT INTO "auth_permission" VALUES(70,18,'change_evaluationcampaign','Can change Qiymətləndirmə Kampaniyası');
INSERT INTO "auth_permission" VALUES(71,18,'delete_evaluationcampaign','Can delete Qiymətləndirmə Kampaniyası');
INSERT INTO "auth_permission" VALUES(72,18,'view_evaluationcampaign','Can view Qiymətləndirmə Kampaniyası');
INSERT INTO "auth_permission" VALUES(73,19,'add_questioncategory','Can add Sual Kateqoriyası');
INSERT INTO "auth_permission" VALUES(74,19,'change_questioncategory','Can change Sual Kateqoriyası');
INSERT INTO "auth_permission" VALUES(75,19,'delete_questioncategory','Can delete Sual Kateqoriyası');
INSERT INTO "auth_permission" VALUES(76,19,'view_questioncategory','Can view Sual Kateqoriyası');
INSERT INTO "auth_permission" VALUES(77,20,'add_question','Can add Sual');
INSERT INTO "auth_permission" VALUES(78,20,'change_question','Can change Sual');
INSERT INTO "auth_permission" VALUES(79,20,'delete_question','Can delete Sual');
INSERT INTO "auth_permission" VALUES(80,20,'view_question','Can view Sual');
INSERT INTO "auth_permission" VALUES(81,21,'add_historicalquestion','Can add historical Sual');
INSERT INTO "auth_permission" VALUES(82,21,'change_historicalquestion','Can change historical Sual');
INSERT INTO "auth_permission" VALUES(83,21,'delete_historicalquestion','Can delete historical Sual');
INSERT INTO "auth_permission" VALUES(84,21,'view_historicalquestion','Can view historical Sual');
INSERT INTO "auth_permission" VALUES(85,22,'add_historicalevaluationcampaign','Can add historical Qiymətləndirmə Kampaniyası');
INSERT INTO "auth_permission" VALUES(86,22,'change_historicalevaluationcampaign','Can change historical Qiymətləndirmə Kampaniyası');
INSERT INTO "auth_permission" VALUES(87,22,'delete_historicalevaluationcampaign','Can delete historical Qiymətləndirmə Kampaniyası');
INSERT INTO "auth_permission" VALUES(88,22,'view_historicalevaluationcampaign','Can view historical Qiymətləndirmə Kampaniyası');
INSERT INTO "auth_permission" VALUES(89,23,'add_historicalevaluationassignment','Can add historical Qiymətləndirmə Tapşırığı');
INSERT INTO "auth_permission" VALUES(90,23,'change_historicalevaluationassignment','Can change historical Qiymətləndirmə Tapşırığı');
INSERT INTO "auth_permission" VALUES(91,23,'delete_historicalevaluationassignment','Can delete historical Qiymətləndirmə Tapşırığı');
INSERT INTO "auth_permission" VALUES(92,23,'view_historicalevaluationassignment','Can view historical Qiymətləndirmə Tapşırığı');
INSERT INTO "auth_permission" VALUES(93,24,'add_evaluationassignment','Can add Qiymətləndirmə Tapşırığı');
INSERT INTO "auth_permission" VALUES(94,24,'change_evaluationassignment','Can change Qiymətləndirmə Tapşırığı');
INSERT INTO "auth_permission" VALUES(95,24,'delete_evaluationassignment','Can delete Qiymətləndirmə Tapşırığı');
INSERT INTO "auth_permission" VALUES(96,24,'view_evaluationassignment','Can view Qiymətləndirmə Tapşırığı');
INSERT INTO "auth_permission" VALUES(97,25,'add_campaignquestion','Can add Kampaniya Sualı');
INSERT INTO "auth_permission" VALUES(98,25,'change_campaignquestion','Can change Kampaniya Sualı');
INSERT INTO "auth_permission" VALUES(99,25,'delete_campaignquestion','Can delete Kampaniya Sualı');
INSERT INTO "auth_permission" VALUES(100,25,'view_campaignquestion','Can view Kampaniya Sualı');
INSERT INTO "auth_permission" VALUES(101,26,'add_response','Can add Cavab');
INSERT INTO "auth_permission" VALUES(102,26,'change_response','Can change Cavab');
INSERT INTO "auth_permission" VALUES(103,26,'delete_response','Can delete Cavab');
INSERT INTO "auth_permission" VALUES(104,26,'view_response','Can view Cavab');
INSERT INTO "auth_permission" VALUES(105,27,'add_evaluationresult','Can add Qiymətləndirmə Nəticəsi');
INSERT INTO "auth_permission" VALUES(106,27,'change_evaluationresult','Can change Qiymətləndirmə Nəticəsi');
INSERT INTO "auth_permission" VALUES(107,27,'delete_evaluationresult','Can delete Qiymətləndirmə Nəticəsi');
INSERT INTO "auth_permission" VALUES(108,27,'view_evaluationresult','Can view Qiymətləndirmə Nəticəsi');
INSERT INTO "auth_permission" VALUES(109,28,'add_emailtemplate','Can add E-poçt Şablonu');
INSERT INTO "auth_permission" VALUES(110,28,'change_emailtemplate','Can change E-poçt Şablonu');
INSERT INTO "auth_permission" VALUES(111,28,'delete_emailtemplate','Can delete E-poçt Şablonu');
INSERT INTO "auth_permission" VALUES(112,28,'view_emailtemplate','Can view E-poçt Şablonu');
INSERT INTO "auth_permission" VALUES(113,29,'add_notification','Can add Bildiriş');
INSERT INTO "auth_permission" VALUES(114,29,'change_notification','Can change Bildiriş');
INSERT INTO "auth_permission" VALUES(115,29,'delete_notification','Can delete Bildiriş');
INSERT INTO "auth_permission" VALUES(116,29,'view_notification','Can view Bildiriş');
INSERT INTO "auth_permission" VALUES(117,30,'add_report','Can add Hesabat');
INSERT INTO "auth_permission" VALUES(118,30,'change_report','Can change Hesabat');
INSERT INTO "auth_permission" VALUES(119,30,'delete_report','Can delete Hesabat');
INSERT INTO "auth_permission" VALUES(120,30,'view_report','Can view Hesabat');
INSERT INTO "auth_permission" VALUES(121,31,'add_radarchartdata','Can add Radar Qrafik Məlumatı');
INSERT INTO "auth_permission" VALUES(122,31,'change_radarchartdata','Can change Radar Qrafik Məlumatı');
INSERT INTO "auth_permission" VALUES(123,31,'delete_radarchartdata','Can delete Radar Qrafik Məlumatı');
INSERT INTO "auth_permission" VALUES(124,31,'view_radarchartdata','Can view Radar Qrafik Məlumatı');
INSERT INTO "auth_permission" VALUES(125,32,'add_developmentgoal','Can add İnkişaf Məqsədi');
INSERT INTO "auth_permission" VALUES(126,32,'change_developmentgoal','Can change İnkişaf Məqsədi');
INSERT INTO "auth_permission" VALUES(127,32,'delete_developmentgoal','Can delete İnkişaf Məqsədi');
INSERT INTO "auth_permission" VALUES(128,32,'view_developmentgoal','Can view İnkişaf Məqsədi');
INSERT INTO "auth_permission" VALUES(129,33,'add_progresslog','Can add İrəliləyiş Qeydi');
INSERT INTO "auth_permission" VALUES(130,33,'change_progresslog','Can change İrəliləyiş Qeydi');
INSERT INTO "auth_permission" VALUES(131,33,'delete_progresslog','Can delete İrəliləyiş Qeydi');
INSERT INTO "auth_permission" VALUES(132,33,'view_progresslog','Can view İrəliləyiş Qeydi');
INSERT INTO "auth_permission" VALUES(133,34,'add_auditlog','Can add Audit Qeydi');
INSERT INTO "auth_permission" VALUES(134,34,'change_auditlog','Can change Audit Qeydi');
INSERT INTO "auth_permission" VALUES(135,34,'delete_auditlog','Can delete Audit Qeydi');
INSERT INTO "auth_permission" VALUES(136,34,'view_auditlog','Can view Audit Qeydi');
INSERT INTO "auth_permission" VALUES(137,35,'add_emaillog','Can add E-poçt Loqu');
INSERT INTO "auth_permission" VALUES(138,35,'change_emaillog','Can change E-poçt Loqu');
INSERT INTO "auth_permission" VALUES(139,35,'delete_emaillog','Can delete E-poçt Loqu');
INSERT INTO "auth_permission" VALUES(140,35,'view_emaillog','Can view E-poçt Loqu');
INSERT INTO "auth_permission" VALUES(141,36,'add_reportgenerationlog','Can add Hesabat Yaratma Loqu');
INSERT INTO "auth_permission" VALUES(142,36,'change_reportgenerationlog','Can change Hesabat Yaratma Loqu');
INSERT INTO "auth_permission" VALUES(143,36,'delete_reportgenerationlog','Can delete Hesabat Yaratma Loqu');
INSERT INTO "auth_permission" VALUES(144,36,'view_reportgenerationlog','Can view Hesabat Yaratma Loqu');
INSERT INTO "auth_permission" VALUES(145,37,'add_supportticket','Can add Dəstək Sorğusu');
INSERT INTO "auth_permission" VALUES(146,37,'change_supportticket','Can change Dəstək Sorğusu');
INSERT INTO "auth_permission" VALUES(147,37,'delete_supportticket','Can delete Dəstək Sorğusu');
INSERT INTO "auth_permission" VALUES(148,37,'view_supportticket','Can view Dəstək Sorğusu');
INSERT INTO "auth_permission" VALUES(149,38,'add_ticketcomment','Can add Sorğu Şərhi');
INSERT INTO "auth_permission" VALUES(150,38,'change_ticketcomment','Can change Sorğu Şərhi');
INSERT INTO "auth_permission" VALUES(151,38,'delete_ticketcomment','Can delete Sorğu Şərhi');
INSERT INTO "auth_permission" VALUES(152,38,'view_ticketcomment','Can view Sorğu Şərhi');
INSERT INTO "auth_permission" VALUES(153,39,'add_historicalcompetency','Can add historical Kompetensiya');
INSERT INTO "auth_permission" VALUES(154,39,'change_historicalcompetency','Can change historical Kompetensiya');
INSERT INTO "auth_permission" VALUES(155,39,'delete_historicalcompetency','Can delete historical Kompetensiya');
INSERT INTO "auth_permission" VALUES(156,39,'view_historicalcompetency','Can view historical Kompetensiya');
INSERT INTO "auth_permission" VALUES(157,40,'add_competency','Can add Kompetensiya');
INSERT INTO "auth_permission" VALUES(158,40,'change_competency','Can change Kompetensiya');
INSERT INTO "auth_permission" VALUES(159,40,'delete_competency','Can delete Kompetensiya');
INSERT INTO "auth_permission" VALUES(160,40,'view_competency','Can view Kompetensiya');
INSERT INTO "auth_permission" VALUES(161,41,'add_proficiencylevel','Can add Bacarıq Səviyyəsi');
INSERT INTO "auth_permission" VALUES(162,41,'change_proficiencylevel','Can change Bacarıq Səviyyəsi');
INSERT INTO "auth_permission" VALUES(163,41,'delete_proficiencylevel','Can delete Bacarıq Səviyyəsi');
INSERT INTO "auth_permission" VALUES(164,41,'view_proficiencylevel','Can view Bacarıq Səviyyəsi');
INSERT INTO "auth_permission" VALUES(165,42,'add_historicalpositioncompetency','Can add historical Vəzifə Kompetensiyası');
INSERT INTO "auth_permission" VALUES(166,42,'change_historicalpositioncompetency','Can change historical Vəzifə Kompetensiyası');
INSERT INTO "auth_permission" VALUES(167,42,'delete_historicalpositioncompetency','Can delete historical Vəzifə Kompetensiyası');
INSERT INTO "auth_permission" VALUES(168,42,'view_historicalpositioncompetency','Can view historical Vəzifə Kompetensiyası');
INSERT INTO "auth_permission" VALUES(169,43,'add_positioncompetency','Can add Vəzifə Kompetensiyası');
INSERT INTO "auth_permission" VALUES(170,43,'change_positioncompetency','Can change Vəzifə Kompetensiyası');
INSERT INTO "auth_permission" VALUES(171,43,'delete_positioncompetency','Can delete Vəzifə Kompetensiyası');
INSERT INTO "auth_permission" VALUES(172,43,'view_positioncompetency','Can view Vəzifə Kompetensiyası');
INSERT INTO "auth_permission" VALUES(173,44,'add_historicaluserskill','Can add historical İstifadəçi Bacarığı');
INSERT INTO "auth_permission" VALUES(174,44,'change_historicaluserskill','Can change historical İstifadəçi Bacarığı');
INSERT INTO "auth_permission" VALUES(175,44,'delete_historicaluserskill','Can delete historical İstifadəçi Bacarığı');
INSERT INTO "auth_permission" VALUES(176,44,'view_historicaluserskill','Can view historical İstifadəçi Bacarığı');
INSERT INTO "auth_permission" VALUES(177,45,'add_userskill','Can add İstifadəçi Bacarığı');
INSERT INTO "auth_permission" VALUES(178,45,'change_userskill','Can change İstifadəçi Bacarığı');
INSERT INTO "auth_permission" VALUES(179,45,'delete_userskill','Can delete İstifadəçi Bacarığı');
INSERT INTO "auth_permission" VALUES(180,45,'view_userskill','Can view İstifadəçi Bacarığı');
INSERT INTO "auth_permission" VALUES(181,46,'add_historicaltrainingresource','Can add historical Təlim Resursu');
INSERT INTO "auth_permission" VALUES(182,46,'change_historicaltrainingresource','Can change historical Təlim Resursu');
INSERT INTO "auth_permission" VALUES(183,46,'delete_historicaltrainingresource','Can delete historical Təlim Resursu');
INSERT INTO "auth_permission" VALUES(184,46,'view_historicaltrainingresource','Can view historical Təlim Resursu');
INSERT INTO "auth_permission" VALUES(185,47,'add_trainingresource','Can add Təlim Resursu');
INSERT INTO "auth_permission" VALUES(186,47,'change_trainingresource','Can change Təlim Resursu');
INSERT INTO "auth_permission" VALUES(187,47,'delete_trainingresource','Can delete Təlim Resursu');
INSERT INTO "auth_permission" VALUES(188,47,'view_trainingresource','Can view Təlim Resursu');
INSERT INTO "auth_permission" VALUES(189,48,'add_historicalusertraining','Can add historical İstifadəçi Təlimi');
INSERT INTO "auth_permission" VALUES(190,48,'change_historicalusertraining','Can change historical İstifadəçi Təlimi');
INSERT INTO "auth_permission" VALUES(191,48,'delete_historicalusertraining','Can delete historical İstifadəçi Təlimi');
INSERT INTO "auth_permission" VALUES(192,48,'view_historicalusertraining','Can view historical İstifadəçi Təlimi');
INSERT INTO "auth_permission" VALUES(193,49,'add_usertraining','Can add İstifadəçi Təlimi');
INSERT INTO "auth_permission" VALUES(194,49,'change_usertraining','Can change İstifadəçi Təlimi');
INSERT INTO "auth_permission" VALUES(195,49,'delete_usertraining','Can delete İstifadəçi Təlimi');
INSERT INTO "auth_permission" VALUES(196,49,'view_usertraining','Can view İstifadəçi Təlimi');
INSERT INTO "auth_permission" VALUES(197,50,'add_criticalrole','Can add Kritik Rol');
INSERT INTO "auth_permission" VALUES(198,50,'change_criticalrole','Can change Kritik Rol');
INSERT INTO "auth_permission" VALUES(199,50,'delete_criticalrole','Can delete Kritik Rol');
INSERT INTO "auth_permission" VALUES(200,50,'view_criticalrole','Can view Kritik Rol');
INSERT INTO "auth_permission" VALUES(201,51,'add_talentmatrix','Can add İstedad Matrisi Qiymətləndirməsi');
INSERT INTO "auth_permission" VALUES(202,51,'change_talentmatrix','Can change İstedad Matrisi Qiymətləndirməsi');
INSERT INTO "auth_permission" VALUES(203,51,'delete_talentmatrix','Can delete İstedad Matrisi Qiymətləndirməsi');
INSERT INTO "auth_permission" VALUES(204,51,'view_talentmatrix','Can view İstedad Matrisi Qiymətləndirməsi');
INSERT INTO "auth_permission" VALUES(205,52,'add_successioncandidate','Can add Varislik Namizədi');
INSERT INTO "auth_permission" VALUES(206,52,'change_successioncandidate','Can change Varislik Namizədi');
INSERT INTO "auth_permission" VALUES(207,52,'delete_successioncandidate','Can delete Varislik Namizədi');
INSERT INTO "auth_permission" VALUES(208,52,'view_successioncandidate','Can view Varislik Namizədi');
INSERT INTO "auth_permission" VALUES(209,53,'add_competencygap','Can add Kompetensiya Boşluğu');
INSERT INTO "auth_permission" VALUES(210,53,'change_competencygap','Can change Kompetensiya Boşluğu');
INSERT INTO "auth_permission" VALUES(211,53,'delete_competencygap','Can delete Kompetensiya Boşluğu');
INSERT INTO "auth_permission" VALUES(212,53,'view_competencygap','Can view Kompetensiya Boşluğu');
INSERT INTO "auth_permission" VALUES(213,54,'add_feedbacktag','Can add Rəy Etiketi');
INSERT INTO "auth_permission" VALUES(214,54,'change_feedbacktag','Can change Rəy Etiketi');
INSERT INTO "auth_permission" VALUES(215,54,'delete_feedbacktag','Can delete Rəy Etiketi');
INSERT INTO "auth_permission" VALUES(216,54,'view_feedbacktag','Can view Rəy Etiketi');
INSERT INTO "auth_permission" VALUES(217,55,'add_publicrecognition','Can add İctimai Təqdir');
INSERT INTO "auth_permission" VALUES(218,55,'change_publicrecognition','Can change İctimai Təqdir');
INSERT INTO "auth_permission" VALUES(219,55,'delete_publicrecognition','Can delete İctimai Təqdir');
INSERT INTO "auth_permission" VALUES(220,55,'view_publicrecognition','Can view İctimai Təqdir');
INSERT INTO "auth_permission" VALUES(221,56,'add_recognitioncomment','Can add Təqdir Şərhi');
INSERT INTO "auth_permission" VALUES(222,56,'change_recognitioncomment','Can change Təqdir Şərhi');
INSERT INTO "auth_permission" VALUES(223,56,'delete_recognitioncomment','Can delete Təqdir Şərhi');
INSERT INTO "auth_permission" VALUES(224,56,'view_recognitioncomment','Can view Təqdir Şərhi');
INSERT INTO "auth_permission" VALUES(225,57,'add_quickfeedback','Can add Tez Rəy');
INSERT INTO "auth_permission" VALUES(226,57,'change_quickfeedback','Can change Tez Rəy');
INSERT INTO "auth_permission" VALUES(227,57,'delete_quickfeedback','Can delete Tez Rəy');
INSERT INTO "auth_permission" VALUES(228,57,'view_quickfeedback','Can view Tez Rəy');
INSERT INTO "auth_permission" VALUES(229,58,'add_feedbackbank','Can add Rəy Bankı');
INSERT INTO "auth_permission" VALUES(230,58,'change_feedbackbank','Can change Rəy Bankı');
INSERT INTO "auth_permission" VALUES(231,58,'delete_feedbackbank','Can delete Rəy Bankı');
INSERT INTO "auth_permission" VALUES(232,58,'view_feedbackbank','Can view Rəy Bankı');
INSERT INTO "auth_permission" VALUES(233,59,'add_recognitionlike','Can add Təqdir Bəyənməsi');
INSERT INTO "auth_permission" VALUES(234,59,'change_recognitionlike','Can change Təqdir Bəyənməsi');
INSERT INTO "auth_permission" VALUES(235,59,'delete_recognitionlike','Can delete Təqdir Bəyənməsi');
INSERT INTO "auth_permission" VALUES(236,59,'view_recognitionlike','Can view Təqdir Bəyənməsi');
INSERT INTO "auth_permission" VALUES(237,60,'add_historicalworkhistory','Can add historical İş Tarixçəsi');
INSERT INTO "auth_permission" VALUES(238,60,'change_historicalworkhistory','Can change historical İş Tarixçəsi');
INSERT INTO "auth_permission" VALUES(239,60,'delete_historicalworkhistory','Can delete historical İş Tarixçəsi');
INSERT INTO "auth_permission" VALUES(240,60,'view_historicalworkhistory','Can view historical İş Tarixçəsi');
INSERT INTO "auth_permission" VALUES(241,61,'add_historicalemployeedocument','Can add historical İşçi Sənədi');
INSERT INTO "auth_permission" VALUES(242,61,'change_historicalemployeedocument','Can change historical İşçi Sənədi');
INSERT INTO "auth_permission" VALUES(243,61,'delete_historicalemployeedocument','Can delete historical İşçi Sənədi');
INSERT INTO "auth_permission" VALUES(244,61,'view_historicalemployeedocument','Can view historical İşçi Sənədi');
INSERT INTO "auth_permission" VALUES(245,62,'add_workhistory','Can add İş Tarixçəsi');
INSERT INTO "auth_permission" VALUES(246,62,'change_workhistory','Can change İş Tarixçəsi');
INSERT INTO "auth_permission" VALUES(247,62,'delete_workhistory','Can delete İş Tarixçəsi');
INSERT INTO "auth_permission" VALUES(248,62,'view_workhistory','Can view İş Tarixçəsi');
INSERT INTO "auth_permission" VALUES(249,63,'add_employeedocument','Can add İşçi Sənədi');
INSERT INTO "auth_permission" VALUES(250,63,'change_employeedocument','Can change İşçi Sənədi');
INSERT INTO "auth_permission" VALUES(251,63,'delete_employeedocument','Can delete İşçi Sənədi');
INSERT INTO "auth_permission" VALUES(252,63,'view_employeedocument','Can view İşçi Sənədi');
INSERT INTO "auth_permission" VALUES(253,64,'add_compensationhistory','Can add Kompensasiya Tarixçəsi');
INSERT INTO "auth_permission" VALUES(254,64,'change_compensationhistory','Can change Kompensasiya Tarixçəsi');
INSERT INTO "auth_permission" VALUES(255,64,'delete_compensationhistory','Can delete Kompensasiya Tarixçəsi');
INSERT INTO "auth_permission" VALUES(256,64,'view_compensationhistory','Can view Kompensasiya Tarixçəsi');
INSERT INTO "auth_permission" VALUES(257,65,'add_historicalbonus','Can add historical Bonus');
INSERT INTO "auth_permission" VALUES(258,65,'change_historicalbonus','Can change historical Bonus');
INSERT INTO "auth_permission" VALUES(259,65,'delete_historicalbonus','Can delete historical Bonus');
INSERT INTO "auth_permission" VALUES(260,65,'view_historicalbonus','Can view historical Bonus');
INSERT INTO "auth_permission" VALUES(261,66,'add_allowance','Can add Müavinət');
INSERT INTO "auth_permission" VALUES(262,66,'change_allowance','Can change Müavinət');
INSERT INTO "auth_permission" VALUES(263,66,'delete_allowance','Can delete Müavinət');
INSERT INTO "auth_permission" VALUES(264,66,'view_allowance','Can view Müavinət');
INSERT INTO "auth_permission" VALUES(265,67,'add_historicaldeduction','Can add historical Tutma');
INSERT INTO "auth_permission" VALUES(266,67,'change_historicaldeduction','Can change historical Tutma');
INSERT INTO "auth_permission" VALUES(267,67,'delete_historicaldeduction','Can delete historical Tutma');
INSERT INTO "auth_permission" VALUES(268,67,'view_historicaldeduction','Can view historical Tutma');
INSERT INTO "auth_permission" VALUES(269,68,'add_historicalallowance','Can add historical Müavinət');
INSERT INTO "auth_permission" VALUES(270,68,'change_historicalallowance','Can change historical Müavinət');
INSERT INTO "auth_permission" VALUES(271,68,'delete_historicalallowance','Can delete historical Müavinət');
INSERT INTO "auth_permission" VALUES(272,68,'view_historicalallowance','Can view historical Müavinət');
INSERT INTO "auth_permission" VALUES(273,69,'add_historicalcompensationhistory','Can add historical Kompensasiya Tarixçəsi');
INSERT INTO "auth_permission" VALUES(274,69,'change_historicalcompensationhistory','Can change historical Kompensasiya Tarixçəsi');
INSERT INTO "auth_permission" VALUES(275,69,'delete_historicalcompensationhistory','Can delete historical Kompensasiya Tarixçəsi');
INSERT INTO "auth_permission" VALUES(276,69,'view_historicalcompensationhistory','Can view historical Kompensasiya Tarixçəsi');
INSERT INTO "auth_permission" VALUES(277,70,'add_salaryinformation','Can add Maaş Məlumatı');
INSERT INTO "auth_permission" VALUES(278,70,'change_salaryinformation','Can change Maaş Məlumatı');
INSERT INTO "auth_permission" VALUES(279,70,'delete_salaryinformation','Can delete Maaş Məlumatı');
INSERT INTO "auth_permission" VALUES(280,70,'view_salaryinformation','Can view Maaş Məlumatı');
INSERT INTO "auth_permission" VALUES(281,71,'add_deduction','Can add Tutma');
INSERT INTO "auth_permission" VALUES(282,71,'change_deduction','Can change Tutma');
INSERT INTO "auth_permission" VALUES(283,71,'delete_deduction','Can delete Tutma');
INSERT INTO "auth_permission" VALUES(284,71,'view_deduction','Can view Tutma');
INSERT INTO "auth_permission" VALUES(285,72,'add_bonus','Can add Bonus');
INSERT INTO "auth_permission" VALUES(286,72,'change_bonus','Can change Bonus');
INSERT INTO "auth_permission" VALUES(287,72,'delete_bonus','Can delete Bonus');
INSERT INTO "auth_permission" VALUES(288,72,'view_bonus','Can view Bonus');
INSERT INTO "auth_permission" VALUES(289,73,'add_historicalsalaryinformation','Can add historical Maaş Məlumatı');
INSERT INTO "auth_permission" VALUES(290,73,'change_historicalsalaryinformation','Can change historical Maaş Məlumatı');
INSERT INTO "auth_permission" VALUES(291,73,'delete_historicalsalaryinformation','Can delete historical Maaş Məlumatı');
INSERT INTO "auth_permission" VALUES(292,73,'view_historicalsalaryinformation','Can view historical Maaş Məlumatı');
INSERT INTO "auth_permission" VALUES(293,74,'add_leavetype','Can add Məzuniyyət Növü');
INSERT INTO "auth_permission" VALUES(294,74,'change_leavetype','Can change Məzuniyyət Növü');
INSERT INTO "auth_permission" VALUES(295,74,'delete_leavetype','Can delete Məzuniyyət Növü');
INSERT INTO "auth_permission" VALUES(296,74,'view_leavetype','Can view Məzuniyyət Növü');
INSERT INTO "auth_permission" VALUES(297,75,'add_leaverequest','Can add Məzuniyyət Sorğusu');
INSERT INTO "auth_permission" VALUES(298,75,'change_leaverequest','Can change Məzuniyyət Sorğusu');
INSERT INTO "auth_permission" VALUES(299,75,'delete_leaverequest','Can delete Məzuniyyət Sorğusu');
INSERT INTO "auth_permission" VALUES(300,75,'view_leaverequest','Can view Məzuniyyət Sorğusu');
INSERT INTO "auth_permission" VALUES(301,76,'add_leavebalance','Can add Məzuniyyət Qalığı');
INSERT INTO "auth_permission" VALUES(302,76,'change_leavebalance','Can change Məzuniyyət Qalığı');
INSERT INTO "auth_permission" VALUES(303,76,'delete_leavebalance','Can delete Məzuniyyət Qalığı');
INSERT INTO "auth_permission" VALUES(304,76,'view_leavebalance','Can view Məzuniyyət Qalığı');
INSERT INTO "auth_permission" VALUES(305,77,'add_holiday','Can add Bayram');
INSERT INTO "auth_permission" VALUES(306,77,'change_holiday','Can change Bayram');
INSERT INTO "auth_permission" VALUES(307,77,'delete_holiday','Can delete Bayram');
INSERT INTO "auth_permission" VALUES(308,77,'view_holiday','Can view Bayram');
INSERT INTO "auth_permission" VALUES(309,78,'add_historicalleavetype','Can add historical Məzuniyyət Növü');
INSERT INTO "auth_permission" VALUES(310,78,'change_historicalleavetype','Can change historical Məzuniyyət Növü');
INSERT INTO "auth_permission" VALUES(311,78,'delete_historicalleavetype','Can delete historical Məzuniyyət Növü');
INSERT INTO "auth_permission" VALUES(312,78,'view_historicalleavetype','Can view historical Məzuniyyət Növü');
INSERT INTO "auth_permission" VALUES(313,79,'add_historicalleaverequest','Can add historical Məzuniyyət Sorğusu');
INSERT INTO "auth_permission" VALUES(314,79,'change_historicalleaverequest','Can change historical Məzuniyyət Sorğusu');
INSERT INTO "auth_permission" VALUES(315,79,'delete_historicalleaverequest','Can delete historical Məzuniyyət Sorğusu');
INSERT INTO "auth_permission" VALUES(316,79,'view_historicalleaverequest','Can view historical Məzuniyyət Sorğusu');
INSERT INTO "auth_permission" VALUES(317,80,'add_historicalleavebalance','Can add historical Məzuniyyət Qalığı');
INSERT INTO "auth_permission" VALUES(318,80,'change_historicalleavebalance','Can change historical Məzuniyyət Qalığı');
INSERT INTO "auth_permission" VALUES(319,80,'delete_historicalleavebalance','Can delete historical Məzuniyyət Qalığı');
INSERT INTO "auth_permission" VALUES(320,80,'view_historicalleavebalance','Can view historical Məzuniyyət Qalığı');
INSERT INTO "auth_permission" VALUES(321,81,'add_historicalholiday','Can add historical Bayram');
INSERT INTO "auth_permission" VALUES(322,81,'change_historicalholiday','Can change historical Bayram');
INSERT INTO "auth_permission" VALUES(323,81,'delete_historicalholiday','Can delete historical Bayram');
INSERT INTO "auth_permission" VALUES(324,81,'view_historicalholiday','Can view historical Bayram');
INSERT INTO "auth_permission" VALUES(325,82,'add_historicalattendance','Can add historical İştirak Qeydi');
INSERT INTO "auth_permission" VALUES(326,82,'change_historicalattendance','Can change historical İştirak Qeydi');
INSERT INTO "auth_permission" VALUES(327,82,'delete_historicalattendance','Can delete historical İştirak Qeydi');
INSERT INTO "auth_permission" VALUES(328,82,'view_historicalattendance','Can view historical İştirak Qeydi');
INSERT INTO "auth_permission" VALUES(329,83,'add_attendance','Can add İştirak Qeydi');
INSERT INTO "auth_permission" VALUES(330,83,'change_attendance','Can change İştirak Qeydi');
INSERT INTO "auth_permission" VALUES(331,83,'delete_attendance','Can delete İştirak Qeydi');
INSERT INTO "auth_permission" VALUES(332,83,'view_attendance','Can view İştirak Qeydi');
INSERT INTO "auth_permission" VALUES(333,84,'add_kpi','Can add KPI');
INSERT INTO "auth_permission" VALUES(334,84,'change_kpi','Can change KPI');
INSERT INTO "auth_permission" VALUES(335,84,'delete_kpi','Can delete KPI');
INSERT INTO "auth_permission" VALUES(336,84,'view_kpi','Can view KPI');
INSERT INTO "auth_permission" VALUES(337,85,'add_strategicobjective','Can add Strateji Məqsəd');
INSERT INTO "auth_permission" VALUES(338,85,'change_strategicobjective','Can change Strateji Məqsəd');
INSERT INTO "auth_permission" VALUES(339,85,'delete_strategicobjective','Can delete Strateji Məqsəd');
INSERT INTO "auth_permission" VALUES(340,85,'view_strategicobjective','Can view Strateji Məqsəd');
INSERT INTO "auth_permission" VALUES(341,86,'add_kpimeasurement','Can add KPI Ölçməsi');
INSERT INTO "auth_permission" VALUES(342,86,'change_kpimeasurement','Can change KPI Ölçməsi');
INSERT INTO "auth_permission" VALUES(343,86,'delete_kpimeasurement','Can delete KPI Ölçməsi');
INSERT INTO "auth_permission" VALUES(344,86,'view_kpimeasurement','Can view KPI Ölçməsi');
INSERT INTO "auth_permission" VALUES(345,87,'add_keyresult','Can add Açar Nəticə');
INSERT INTO "auth_permission" VALUES(346,87,'change_keyresult','Can change Açar Nəticə');
INSERT INTO "auth_permission" VALUES(347,87,'delete_keyresult','Can delete Açar Nəticə');
INSERT INTO "auth_permission" VALUES(348,87,'view_keyresult','Can view Açar Nəticə');
INSERT INTO "auth_permission" VALUES(349,88,'add_historicalstrategicobjective','Can add historical Strateji Məqsəd');
INSERT INTO "auth_permission" VALUES(350,88,'change_historicalstrategicobjective','Can change historical Strateji Məqsəd');
INSERT INTO "auth_permission" VALUES(351,88,'delete_historicalstrategicobjective','Can delete historical Strateji Məqsəd');
INSERT INTO "auth_permission" VALUES(352,88,'view_historicalstrategicobjective','Can view historical Strateji Məqsəd');
INSERT INTO "auth_permission" VALUES(353,89,'add_historicalkpimeasurement','Can add historical KPI Ölçməsi');
INSERT INTO "auth_permission" VALUES(354,89,'change_historicalkpimeasurement','Can change historical KPI Ölçməsi');
INSERT INTO "auth_permission" VALUES(355,89,'delete_historicalkpimeasurement','Can delete historical KPI Ölçməsi');
INSERT INTO "auth_permission" VALUES(356,89,'view_historicalkpimeasurement','Can view historical KPI Ölçməsi');
INSERT INTO "auth_permission" VALUES(357,90,'add_historicalkpi','Can add historical KPI');
INSERT INTO "auth_permission" VALUES(358,90,'change_historicalkpi','Can change historical KPI');
INSERT INTO "auth_permission" VALUES(359,90,'delete_historicalkpi','Can delete historical KPI');
INSERT INTO "auth_permission" VALUES(360,90,'view_historicalkpi','Can view historical KPI');
INSERT INTO "auth_permission" VALUES(361,91,'add_historicalkeyresult','Can add historical Açar Nəticə');
INSERT INTO "auth_permission" VALUES(362,91,'change_historicalkeyresult','Can change historical Açar Nəticə');
INSERT INTO "auth_permission" VALUES(363,91,'delete_historicalkeyresult','Can delete historical Açar Nəticə');
INSERT INTO "auth_permission" VALUES(364,91,'view_historicalkeyresult','Can view historical Açar Nəticə');
INSERT INTO "auth_permission" VALUES(365,92,'add_application','Can add Müraciət');
INSERT INTO "auth_permission" VALUES(366,92,'change_application','Can change Müraciət');
INSERT INTO "auth_permission" VALUES(367,92,'delete_application','Can delete Müraciət');
INSERT INTO "auth_permission" VALUES(368,92,'view_application','Can view Müraciət');
INSERT INTO "auth_permission" VALUES(369,93,'add_jobposting','Can add Vakansiya');
INSERT INTO "auth_permission" VALUES(370,93,'change_jobposting','Can change Vakansiya');
INSERT INTO "auth_permission" VALUES(371,93,'delete_jobposting','Can delete Vakansiya');
INSERT INTO "auth_permission" VALUES(372,93,'view_jobposting','Can view Vakansiya');
INSERT INTO "auth_permission" VALUES(373,94,'add_interview','Can add Müsahibə');
INSERT INTO "auth_permission" VALUES(374,94,'change_interview','Can change Müsahibə');
INSERT INTO "auth_permission" VALUES(375,94,'delete_interview','Can delete Müsahibə');
INSERT INTO "auth_permission" VALUES(376,94,'view_interview','Can view Müsahibə');
INSERT INTO "auth_permission" VALUES(377,95,'add_historicalonboardingtask','Can add historical İşəbaşlama Tapşırığı');
INSERT INTO "auth_permission" VALUES(378,95,'change_historicalonboardingtask','Can change historical İşəbaşlama Tapşırığı');
INSERT INTO "auth_permission" VALUES(379,95,'delete_historicalonboardingtask','Can delete historical İşəbaşlama Tapşırığı');
INSERT INTO "auth_permission" VALUES(380,95,'view_historicalonboardingtask','Can view historical İşəbaşlama Tapşırığı');
INSERT INTO "auth_permission" VALUES(381,96,'add_historicaloffer','Can add historical Təklif');
INSERT INTO "auth_permission" VALUES(382,96,'change_historicaloffer','Can change historical Təklif');
INSERT INTO "auth_permission" VALUES(383,96,'delete_historicaloffer','Can delete historical Təklif');
INSERT INTO "auth_permission" VALUES(384,96,'view_historicaloffer','Can view historical Təklif');
INSERT INTO "auth_permission" VALUES(385,97,'add_historicaljobposting','Can add historical Vakansiya');
INSERT INTO "auth_permission" VALUES(386,97,'change_historicaljobposting','Can change historical Vakansiya');
INSERT INTO "auth_permission" VALUES(387,97,'delete_historicaljobposting','Can delete historical Vakansiya');
INSERT INTO "auth_permission" VALUES(388,97,'view_historicaljobposting','Can view historical Vakansiya');
INSERT INTO "auth_permission" VALUES(389,98,'add_historicalinterview','Can add historical Müsahibə');
INSERT INTO "auth_permission" VALUES(390,98,'change_historicalinterview','Can change historical Müsahibə');
INSERT INTO "auth_permission" VALUES(391,98,'delete_historicalinterview','Can delete historical Müsahibə');
INSERT INTO "auth_permission" VALUES(392,98,'view_historicalinterview','Can view historical Müsahibə');
INSERT INTO "auth_permission" VALUES(393,99,'add_historicalapplication','Can add historical Müraciət');
INSERT INTO "auth_permission" VALUES(394,99,'change_historicalapplication','Can change historical Müraciət');
INSERT INTO "auth_permission" VALUES(395,99,'delete_historicalapplication','Can delete historical Müraciət');
INSERT INTO "auth_permission" VALUES(396,99,'view_historicalapplication','Can view historical Müraciət');
INSERT INTO "auth_permission" VALUES(397,100,'add_onboardingtask','Can add İşəbaşlama Tapşırığı');
INSERT INTO "auth_permission" VALUES(398,100,'change_onboardingtask','Can change İşəbaşlama Tapşırığı');
INSERT INTO "auth_permission" VALUES(399,100,'delete_onboardingtask','Can delete İşəbaşlama Tapşırığı');
INSERT INTO "auth_permission" VALUES(400,100,'view_onboardingtask','Can view İşəbaşlama Tapşırığı');
INSERT INTO "auth_permission" VALUES(401,101,'add_offer','Can add Təklif');
INSERT INTO "auth_permission" VALUES(402,101,'change_offer','Can change Təklif');
INSERT INTO "auth_permission" VALUES(403,101,'delete_offer','Can delete Təklif');
INSERT INTO "auth_permission" VALUES(404,101,'view_offer','Can view Təklif');
INSERT INTO "auth_permission" VALUES(405,102,'add_historicaldepartmentbudget','Can add historical Departament Büdcəsi');
INSERT INTO "auth_permission" VALUES(406,102,'change_historicaldepartmentbudget','Can change historical Departament Büdcəsi');
INSERT INTO "auth_permission" VALUES(407,102,'delete_historicaldepartmentbudget','Can delete historical Departament Büdcəsi');
INSERT INTO "auth_permission" VALUES(408,102,'view_historicaldepartmentbudget','Can view historical Departament Büdcəsi');
INSERT INTO "auth_permission" VALUES(409,103,'add_departmentbudget','Can add Departament Büdcəsi');
INSERT INTO "auth_permission" VALUES(410,103,'change_departmentbudget','Can change Departament Büdcəsi');
INSERT INTO "auth_permission" VALUES(411,103,'delete_departmentbudget','Can delete Departament Büdcəsi');
INSERT INTO "auth_permission" VALUES(412,103,'view_departmentbudget','Can view Departament Büdcəsi');
INSERT INTO "auth_permission" VALUES(413,104,'add_systemkpi','Can add Sistem KPI');
INSERT INTO "auth_permission" VALUES(414,104,'change_systemkpi','Can change Sistem KPI');
INSERT INTO "auth_permission" VALUES(415,104,'delete_systemkpi','Can delete Sistem KPI');
INSERT INTO "auth_permission" VALUES(416,104,'view_systemkpi','Can view Sistem KPI');
INSERT INTO "auth_permission" VALUES(417,105,'add_objectiveupdate','Can add Məqsəd Yenilənməsi');
INSERT INTO "auth_permission" VALUES(418,105,'change_objectiveupdate','Can change Məqsəd Yenilənməsi');
INSERT INTO "auth_permission" VALUES(419,105,'delete_objectiveupdate','Can delete Məqsəd Yenilənməsi');
INSERT INTO "auth_permission" VALUES(420,105,'view_objectiveupdate','Can view Məqsəd Yenilənməsi');
INSERT INTO "auth_permission" VALUES(421,106,'add_historicalobjectiveupdate','Can add historical Məqsəd Yenilənməsi');
INSERT INTO "auth_permission" VALUES(422,106,'change_historicalobjectiveupdate','Can change historical Məqsəd Yenilənməsi');
INSERT INTO "auth_permission" VALUES(423,106,'delete_historicalobjectiveupdate','Can delete historical Məqsəd Yenilənməsi');
INSERT INTO "auth_permission" VALUES(424,106,'view_historicalobjectiveupdate','Can view historical Məqsəd Yenilənməsi');
INSERT INTO "auth_permission" VALUES(425,107,'add_historicalmilestone','Can add historical Mərhələ');
INSERT INTO "auth_permission" VALUES(426,107,'change_historicalmilestone','Can change historical Mərhələ');
INSERT INTO "auth_permission" VALUES(427,107,'delete_historicalmilestone','Can delete historical Mərhələ');
INSERT INTO "auth_permission" VALUES(428,107,'view_historicalmilestone','Can view historical Mərhələ');
INSERT INTO "auth_permission" VALUES(429,108,'add_milestone','Can add Mərhələ');
INSERT INTO "auth_permission" VALUES(430,108,'change_milestone','Can change Mərhələ');
INSERT INTO "auth_permission" VALUES(431,108,'delete_milestone','Can delete Mərhələ');
INSERT INTO "auth_permission" VALUES(432,108,'view_milestone','Can view Mərhələ');
INSERT INTO "auth_permission" VALUES(433,109,'add_dashboardwidget','Can add Dashboard Widget');
INSERT INTO "auth_permission" VALUES(434,109,'change_dashboardwidget','Can change Dashboard Widget');
INSERT INTO "auth_permission" VALUES(435,109,'delete_dashboardwidget','Can delete Dashboard Widget');
INSERT INTO "auth_permission" VALUES(436,109,'view_dashboardwidget','Can view Dashboard Widget');
INSERT INTO "auth_permission" VALUES(437,110,'add_systemkpi','Can add System KPI');
INSERT INTO "auth_permission" VALUES(438,110,'change_systemkpi','Can change System KPI');
INSERT INTO "auth_permission" VALUES(439,110,'delete_systemkpi','Can delete System KPI');
INSERT INTO "auth_permission" VALUES(440,110,'view_systemkpi','Can view System KPI');
INSERT INTO "auth_permission" VALUES(441,111,'add_trenddata','Can add Trend Data');
INSERT INTO "auth_permission" VALUES(442,111,'change_trenddata','Can change Trend Data');
INSERT INTO "auth_permission" VALUES(443,111,'delete_trenddata','Can delete Trend Data');
INSERT INTO "auth_permission" VALUES(444,111,'view_trenddata','Can view Trend Data');
INSERT INTO "auth_permission" VALUES(445,112,'add_analyticsreport','Can add Analytics Report');
INSERT INTO "auth_permission" VALUES(446,112,'change_analyticsreport','Can change Analytics Report');
INSERT INTO "auth_permission" VALUES(447,112,'delete_analyticsreport','Can delete Analytics Report');
INSERT INTO "auth_permission" VALUES(448,112,'view_analyticsreport','Can view Analytics Report');
INSERT INTO "auth_permission" VALUES(449,113,'add_realtimestat','Can add Real-time Stat');
INSERT INTO "auth_permission" VALUES(450,113,'change_realtimestat','Can change Real-time Stat');
INSERT INTO "auth_permission" VALUES(451,113,'delete_realtimestat','Can delete Real-time Stat');
INSERT INTO "auth_permission" VALUES(452,113,'view_realtimestat','Can view Real-time Stat');
INSERT INTO "auth_permission" VALUES(453,114,'add_forecastdata','Can add Forecast Data');
INSERT INTO "auth_permission" VALUES(454,114,'change_forecastdata','Can change Forecast Data');
INSERT INTO "auth_permission" VALUES(455,114,'delete_forecastdata','Can delete Forecast Data');
INSERT INTO "auth_permission" VALUES(456,114,'view_forecastdata','Can view Forecast Data');
INSERT INTO "auth_permission" VALUES(457,115,'add_notificationmethod','Can add Bildiriş Metodu');
INSERT INTO "auth_permission" VALUES(458,115,'change_notificationmethod','Can change Bildiriş Metodu');
INSERT INTO "auth_permission" VALUES(459,115,'delete_notificationmethod','Can delete Bildiriş Metodu');
INSERT INTO "auth_permission" VALUES(460,115,'view_notificationmethod','Can view Bildiriş Metodu');
INSERT INTO "auth_permission" VALUES(461,116,'add_smsprovider','Can add SMS Təchizatçısı');
INSERT INTO "auth_permission" VALUES(462,116,'change_smsprovider','Can change SMS Təchizatçısı');
INSERT INTO "auth_permission" VALUES(463,116,'delete_smsprovider','Can delete SMS Təchizatçısı');
INSERT INTO "auth_permission" VALUES(464,116,'view_smsprovider','Can view SMS Təchizatçısı');
INSERT INTO "auth_permission" VALUES(465,117,'add_bulknotification','Can add Kütləvi Bildiriş');
INSERT INTO "auth_permission" VALUES(466,117,'change_bulknotification','Can change Kütləvi Bildiriş');
INSERT INTO "auth_permission" VALUES(467,117,'delete_bulknotification','Can delete Kütləvi Bildiriş');
INSERT INTO "auth_permission" VALUES(468,117,'view_bulknotification','Can view Kütləvi Bildiriş');
INSERT INTO "auth_permission" VALUES(469,118,'add_notificationtemplate','Can add Bildiriş Şablonu');
INSERT INTO "auth_permission" VALUES(470,118,'change_notificationtemplate','Can change Bildiriş Şablonu');
INSERT INTO "auth_permission" VALUES(471,118,'delete_notificationtemplate','Can delete Bildiriş Şablonu');
INSERT INTO "auth_permission" VALUES(472,118,'view_notificationtemplate','Can view Bildiriş Şablonu');
INSERT INTO "auth_permission" VALUES(473,119,'add_pushnotification','Can add Push Bildirişi');
INSERT INTO "auth_permission" VALUES(474,119,'change_pushnotification','Can change Push Bildirişi');
INSERT INTO "auth_permission" VALUES(475,119,'delete_pushnotification','Can delete Push Bildirişi');
INSERT INTO "auth_permission" VALUES(476,119,'view_pushnotification','Can view Push Bildirişi');
INSERT INTO "auth_permission" VALUES(477,120,'add_smslog','Can add SMS Loqu');
INSERT INTO "auth_permission" VALUES(478,120,'change_smslog','Can change SMS Loqu');
INSERT INTO "auth_permission" VALUES(479,120,'delete_smslog','Can delete SMS Loqu');
INSERT INTO "auth_permission" VALUES(480,120,'view_smslog','Can view SMS Loqu');
INSERT INTO "auth_permission" VALUES(481,121,'add_usernotificationpreference','Can add İstifadəçi Bildiriş Tənzimləmələri');
INSERT INTO "auth_permission" VALUES(482,121,'change_usernotificationpreference','Can change İstifadəçi Bildiriş Tənzimləmələri');
INSERT INTO "auth_permission" VALUES(483,121,'delete_usernotificationpreference','Can delete İstifadəçi Bildiriş Tənzimləmələri');
INSERT INTO "auth_permission" VALUES(484,121,'view_usernotificationpreference','Can view İstifadəçi Bildiriş Tənzimləmələri');
CREATE TABLE "compensation_allowance" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "allowance_type" varchar(50) NOT NULL, "amount" decimal NOT NULL, "currency" varchar(3) NOT NULL, "payment_frequency" varchar(20) NOT NULL, "start_date" date NOT NULL, "end_date" date NULL, "is_taxable" bool NOT NULL, "description" text NOT NULL, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "approved_by_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "compensation_allowance" VALUES(1,'mobile',500,'AZN','monthly','2025-10-17',NULL,1,'65f',1,'2025-10-16 21:17:47.018762','2025-10-16 21:26:40.378435',30,1);
CREATE TABLE "compensation_bonus" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "bonus_type" varchar(50) NOT NULL, "amount" decimal NOT NULL, "currency" varchar(3) NOT NULL, "status" varchar(20) NOT NULL, "payment_date" date NULL, "fiscal_year" integer NOT NULL, "description" text NOT NULL, "approved_at" datetime NULL, "created_at" datetime NOT NULL, "approved_by_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "created_by_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "compensation_bonus" VALUES(1,'project',50000,'AZN','approved','2025-10-17',10,'45454',NULL,'2025-10-16 21:04:02.833839',1,1,1);
CREATE TABLE "compensation_compensationhistory" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "previous_salary" decimal NULL, "new_salary" decimal NOT NULL, "currency" varchar(3) NOT NULL, "change_percentage" decimal NULL, "change_reason" varchar(50) NOT NULL, "effective_date" date NOT NULL, "notes" text NOT NULL, "created_at" datetime NOT NULL, "approved_by_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "created_by_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "compensation_compensationhistory" VALUES(1,4500,5000,'AZN',11.11,'performance','2025-10-17','aaaaaaaaaaaaaaaaaaaaaaaaaaaa','2025-10-16 21:10:41.395634',1,1,1);
INSERT INTO "compensation_compensationhistory" VALUES(2,5000,6000,'AZN',20,'cost_of_living','2025-10-17','kef','2025-10-16 21:12:05.978328',2,2,20);
INSERT INTO "compensation_compensationhistory" VALUES(3,NULL,5000,'AZN',NULL,'merit_increase','2025-10-17','','2025-10-16 23:18:08.479716',1,1,20);
INSERT INTO "compensation_compensationhistory" VALUES(4,NULL,99999,'EUR',NULL,'retention','2025-10-01','','2025-10-16 23:19:28.098734',1,1,30);
INSERT INTO "compensation_compensationhistory" VALUES(5,3000,3500,'AZN',16.67,'performance','2025-10-17','','2025-10-17 18:51:03.179459',32,32,33);
CREATE TABLE "compensation_deduction" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "deduction_type" varchar(50) NOT NULL, "calculation_method" varchar(20) NOT NULL, "amount" decimal NOT NULL, "currency" varchar(3) NOT NULL, "start_date" date NOT NULL, "end_date" date NULL, "description" text NOT NULL, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "user_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "compensation_deduction" VALUES(1,'income_tax','percentage',1,'AZN','2025-10-17',NULL,'555555555',1,'2025-10-16 21:19:51.300331','2025-10-16 21:19:51.300352',1);
INSERT INTO "compensation_deduction" VALUES(2,'income_tax','percentage',0.24,'AZN','2025-10-17',NULL,'',1,'2025-10-16 21:20:47.408509','2025-10-16 21:20:47.408525',20);
CREATE TABLE "compensation_departmentbudget" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "fiscal_year" integer NOT NULL, "annual_budget" decimal NOT NULL, "currency" varchar(3) NOT NULL, "utilized_amount" decimal NOT NULL, "notes" text NOT NULL, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "created_by_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "department_id" bigint NOT NULL REFERENCES "departments_department" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "compensation_historicalallowance" ("id" bigint NOT NULL, "allowance_type" varchar(50) NOT NULL, "amount" decimal NOT NULL, "currency" varchar(3) NOT NULL, "payment_frequency" varchar(20) NOT NULL, "start_date" date NOT NULL, "end_date" date NULL, "is_taxable" bool NOT NULL, "description" text NOT NULL, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "approved_by_id" bigint NULL, "history_user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NULL);
INSERT INTO "compensation_historicalallowance" VALUES(1,'mobile',500,'AZN','monthly','2025-10-17',NULL,1,'65',1,'2025-10-16 21:17:47.018762','2025-10-16 21:17:47.018785',1,'2025-10-16 21:17:47.023539',NULL,'+',30,1,1);
INSERT INTO "compensation_historicalallowance" VALUES(1,'mobile',500,'AZN','monthly','2025-10-17',NULL,1,'65f',1,'2025-10-16 21:17:47.018762','2025-10-16 21:26:40.378435',2,'2025-10-16 21:26:40.382018',NULL,'~',30,1,1);
CREATE TABLE "compensation_historicalbonus" ("id" bigint NOT NULL, "bonus_type" varchar(50) NOT NULL, "amount" decimal NOT NULL, "currency" varchar(3) NOT NULL, "status" varchar(20) NOT NULL, "payment_date" date NULL, "fiscal_year" integer NOT NULL, "description" text NOT NULL, "approved_at" datetime NULL, "created_at" datetime NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "approved_by_id" bigint NULL, "created_by_id" bigint NULL, "history_user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NULL);
INSERT INTO "compensation_historicalbonus" VALUES(1,'project',50000,'AZN','approved','2025-10-17',4,'45454',NULL,'2025-10-16 21:04:02.833839',1,'2025-10-16 21:04:02.837059',NULL,'+',2,2,1,1);
INSERT INTO "compensation_historicalbonus" VALUES(1,'project',50000,'AZN','approved','2025-10-17',10,'45454',NULL,'2025-10-16 21:04:02.833839',2,'2025-10-16 21:25:17.547417',NULL,'~',1,1,1,1);
CREATE TABLE "compensation_historicalcompensationhistory" ("id" bigint NOT NULL, "previous_salary" decimal NULL, "new_salary" decimal NOT NULL, "currency" varchar(3) NOT NULL, "change_percentage" decimal NULL, "change_reason" varchar(50) NOT NULL, "effective_date" date NOT NULL, "notes" text NOT NULL, "created_at" datetime NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "approved_by_id" bigint NULL, "created_by_id" bigint NULL, "history_user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NULL);
INSERT INTO "compensation_historicalcompensationhistory" VALUES(1,4500,5000,'AZN',11.11,'performance','2025-10-17','','2025-10-16 21:10:41.395634',1,'2025-10-16 21:10:41.399562',NULL,'+',2,2,1,1);
INSERT INTO "compensation_historicalcompensationhistory" VALUES(2,5000,6000,'AZN',20,'cost_of_living','2025-10-17','kef','2025-10-16 21:12:05.978328',2,'2025-10-16 21:12:05.982028',NULL,'+',2,2,1,20);
INSERT INTO "compensation_historicalcompensationhistory" VALUES(1,4500,5000,'AZN',11.11,'performance','2025-10-17','aaaaaaaaaaaaaaaaaaaaaaaaaaaa','2025-10-16 21:10:41.395634',3,'2025-10-16 21:26:01.626183',NULL,'~',1,1,1,1);
INSERT INTO "compensation_historicalcompensationhistory" VALUES(3,NULL,5000,'AZN',NULL,'merit_increase','2025-10-17','','2025-10-16 23:18:08.479716',4,'2025-10-16 23:18:08.489716',NULL,'+',1,1,1,20);
INSERT INTO "compensation_historicalcompensationhistory" VALUES(4,NULL,99999,'EUR',NULL,'retention','2025-10-01','','2025-10-16 23:19:28.098734',5,'2025-10-16 23:19:28.111489',NULL,'+',1,1,1,30);
INSERT INTO "compensation_historicalcompensationhistory" VALUES(5,3000,3500,'AZN',16.67,'performance','2025-10-17','','2025-10-17 18:51:03.179459',6,'2025-10-17 18:51:03.186200',NULL,'+',32,32,32,33);
CREATE TABLE "compensation_historicaldeduction" ("id" bigint NOT NULL, "deduction_type" varchar(50) NOT NULL, "calculation_method" varchar(20) NOT NULL, "amount" decimal NOT NULL, "currency" varchar(3) NOT NULL, "start_date" date NOT NULL, "end_date" date NULL, "description" text NOT NULL, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "history_user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NULL);
INSERT INTO "compensation_historicaldeduction" VALUES(1,'income_tax','percentage',1,'AZN','2025-10-17',NULL,'555555555',1,'2025-10-16 21:19:51.300331','2025-10-16 21:19:51.300352',1,'2025-10-16 21:19:51.304550',NULL,'+',1,1);
INSERT INTO "compensation_historicaldeduction" VALUES(2,'income_tax','percentage',0.24,'AZN','2025-10-17',NULL,'',1,'2025-10-16 21:20:47.408509','2025-10-16 21:20:47.408525',2,'2025-10-16 21:20:47.410974',NULL,'+',1,20);
CREATE TABLE "compensation_historicaldepartmentbudget" ("id" bigint NOT NULL, "fiscal_year" integer NOT NULL, "annual_budget" decimal NOT NULL, "currency" varchar(3) NOT NULL, "utilized_amount" decimal NOT NULL, "notes" text NOT NULL, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "created_by_id" bigint NULL, "department_id" bigint NULL, "history_user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "compensation_historicalsalaryinformation" ("id" bigint NOT NULL, "base_salary" decimal NOT NULL, "currency" varchar(3) NOT NULL, "payment_frequency" varchar(20) NOT NULL, "effective_date" date NOT NULL, "end_date" date NULL, "bank_name" varchar(200) NOT NULL, "bank_account_number" varchar(100) NOT NULL, "swift_code" varchar(50) NOT NULL, "notes" text NOT NULL, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "history_user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "updated_by_id" bigint NULL, "user_id" bigint NULL);
INSERT INTO "compensation_historicalsalaryinformation" VALUES(1,4000,'AZN','monthly','2025-10-17','2026-03-31','kapital','454651213216465451348','316931693169','asasnfjnsdffçnvbdjkf',1,'2025-10-16 21:14:49.738714','2025-10-16 21:14:49.738731',1,'2025-10-16 21:14:49.742263',NULL,'+',1,2,1);
INSERT INTO "compensation_historicalsalaryinformation" VALUES(2,5000,'USD','monthly','2025-10-17','2026-09-30','kapital','454651213216465451348','316931693169','kdjkhfgdsklfglkfn',1,'2025-10-16 21:15:54.538578','2025-10-16 21:15:54.538593',2,'2025-10-16 21:15:54.541934',NULL,'+',1,2,20);
INSERT INTO "compensation_historicalsalaryinformation" VALUES(1,4000,'AZN','monthly','2025-10-17','2025-10-17','kapital','454651213216465451348','316931693169','asasnfjnsdffçnvbdjkf',0,'2025-10-16 21:14:49.738714','2025-10-16 23:07:53.498246',3,'2025-10-16 23:07:53.509153',NULL,'~',1,2,1);
INSERT INTO "compensation_historicalsalaryinformation" VALUES(2,5000,'USD','monthly','2025-10-17','2025-10-17','kapital','454651213216465451348','316931693169','kdjkhfgdsklfglkfn',0,'2025-10-16 21:15:54.538578','2025-10-16 23:15:02.995609',4,'2025-10-16 23:15:03.006281',NULL,'~',1,2,20);
INSERT INTO "compensation_historicalsalaryinformation" VALUES(3,5000,'AZN','monthly','2025-10-17',NULL,'','','','',1,'2025-10-16 23:18:08.456550','2025-10-16 23:18:08.456574',5,'2025-10-16 23:18:08.467385',NULL,'+',1,1,20);
INSERT INTO "compensation_historicalsalaryinformation" VALUES(4,99999,'EUR','biweekly','2025-10-01',NULL,'','','','',1,'2025-10-16 23:19:28.072546','2025-10-16 23:19:28.072563',6,'2025-10-16 23:19:28.085811',NULL,'+',1,1,30);
INSERT INTO "compensation_historicalsalaryinformation" VALUES(5,3000,'AZN','monthly','2024-01-01',NULL,'','','','',1,'2025-10-17 18:51:02.357031','2025-10-17 18:51:02.357045',7,'2025-10-17 18:51:02.364362',NULL,'+',NULL,32,33);
INSERT INTO "compensation_historicalsalaryinformation" VALUES(5,3000,'AZN','monthly','2024-01-01','2025-10-17','','','','',0,'2025-10-17 18:51:02.357031','2025-10-17 18:51:03.151603',8,'2025-10-17 18:51:03.158278',NULL,'~',32,32,33);
INSERT INTO "compensation_historicalsalaryinformation" VALUES(6,3500,'AZN','monthly','2025-10-17',NULL,'','','','',1,'2025-10-17 18:51:03.165591','2025-10-17 18:51:03.165603',9,'2025-10-17 18:51:03.172073',NULL,'+',32,32,33);
CREATE TABLE "compensation_salaryinformation" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "base_salary" decimal NOT NULL, "currency" varchar(3) NOT NULL, "payment_frequency" varchar(20) NOT NULL, "effective_date" date NOT NULL, "end_date" date NULL, "bank_name" varchar(200) NOT NULL, "bank_account_number" varchar(100) NOT NULL, "swift_code" varchar(50) NOT NULL, "notes" text NOT NULL, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "updated_by_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "compensation_salaryinformation" VALUES(1,4000,'AZN','monthly','2025-10-17','2025-10-17','kapital','454651213216465451348','316931693169','asasnfjnsdffçnvbdjkf',0,'2025-10-16 21:14:49.738714','2025-10-16 23:07:53.498246',2,1);
INSERT INTO "compensation_salaryinformation" VALUES(2,5000,'USD','monthly','2025-10-17','2025-10-17','kapital','454651213216465451348','316931693169','kdjkhfgdsklfglkfn',0,'2025-10-16 21:15:54.538578','2025-10-16 23:15:02.995609',2,20);
INSERT INTO "compensation_salaryinformation" VALUES(3,5000,'AZN','monthly','2025-10-17',NULL,'','','','',1,'2025-10-16 23:18:08.456550','2025-10-16 23:18:08.456574',1,20);
INSERT INTO "compensation_salaryinformation" VALUES(4,99999,'EUR','biweekly','2025-10-01',NULL,'','','','',1,'2025-10-16 23:19:28.072546','2025-10-16 23:19:28.072563',1,30);
INSERT INTO "compensation_salaryinformation" VALUES(5,3000,'AZN','monthly','2024-01-01','2025-10-17','','','','',0,'2025-10-17 18:51:02.357031','2025-10-17 18:51:03.151603',32,33);
INSERT INTO "compensation_salaryinformation" VALUES(6,3500,'AZN','monthly','2025-10-17',NULL,'','','','',1,'2025-10-17 18:51:03.165591','2025-10-17 18:51:03.165603',32,33);
CREATE TABLE "competencies_competency" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(200) NOT NULL UNIQUE, "description" text NOT NULL, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL);
INSERT INTO "competencies_competency" VALUES(1,'Liderlik','Komandaya rəhbərlik etmək və istiqamət vermək bacarığı',1,'2025-10-11 07:48:55.767840','2025-10-11 07:48:55.767848');
INSERT INTO "competencies_competency" VALUES(2,'Kommunikasiya','Effektiv şifahi və yazılı ünsiyyət bacarıqları',1,'2025-10-11 07:48:55.768989','2025-10-11 07:48:55.768997');
INSERT INTO "competencies_competency" VALUES(3,'Problemlərin Həlli','Analitik düşüncə və yaradıcı həll yolları tapmaq',1,'2025-10-11 07:48:55.769730','2025-10-11 07:48:55.769738');
INSERT INTO "competencies_competency" VALUES(4,'Komanda İşi','Komanda mühitində effektiv əməkdaşlıq',1,'2025-10-11 07:48:55.770369','2025-10-11 07:48:55.770377');
INSERT INTO "competencies_competency" VALUES(5,'Texniki Bilik','Sahə üzrə texniki bacarıq və biliklərin tətbiqi',1,'2025-10-11 07:48:55.771069','2025-10-11 07:48:55.771076');
INSERT INTO "competencies_competency" VALUES(6,'Müştəri Yönümlülük','Müştəri ehtiyaclarını başa düşmək və cavab vermək',1,'2025-10-11 07:48:55.771731','2025-10-11 07:48:55.771738');
INSERT INTO "competencies_competency" VALUES(7,'Vaxt İdarəetməsi','Vaxtı effektiv planlaşdırmaq və prioritetləri müəyyənləşdirmək',1,'2025-10-11 07:48:55.772386','2025-10-11 07:48:55.772394');
INSERT INTO "competencies_competency" VALUES(8,'İnnovasiya','Yeni ideyalar və yanaşmalar təklif etmək',1,'2025-10-11 07:48:55.773117','2025-10-11 07:48:55.773124');
INSERT INTO "competencies_competency" VALUES(9,'Rəhbərlik və Liderlik','Komandaya rəhbərlik etmək, motivasiya yaratmaq və strateji qərarlar qəbul etmək',1,'2025-10-15 07:47:48.646497','2025-10-15 07:47:48.646516');
INSERT INTO "competencies_competency" VALUES(10,'Komanda İşi və Əməkdaşlıq','Komanda ilə effektiv işləmək, koordinasiya və əməkdaşlıq bacarıqları',1,'2025-10-15 07:47:48.661540','2025-10-15 07:47:48.661560');
INSERT INTO "competencies_competency" VALUES(11,'Texniki Bilik (IT)','İnformasiya texnologiyaları sahəsində texniki bilik və bacarıqlar',1,'2025-10-15 07:47:48.672506','2025-10-15 07:47:48.672521');
CREATE TABLE "competencies_historicalcompetency" ("id" bigint NOT NULL, "name" varchar(200) NOT NULL, "description" text NOT NULL, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "history_user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "competencies_historicalcompetency" VALUES(1,'Liderlik','Komandaya rəhbərlik etmək və istiqamət vermək bacarığı',1,'2025-10-11 07:48:55.767840','2025-10-11 07:48:55.767848',1,'2025-10-11 07:48:55.768106',NULL,'+',NULL);
INSERT INTO "competencies_historicalcompetency" VALUES(2,'Kommunikasiya','Effektiv şifahi və yazılı ünsiyyət bacarıqları',1,'2025-10-11 07:48:55.768989','2025-10-11 07:48:55.768997',2,'2025-10-11 07:48:55.769078',NULL,'+',NULL);
INSERT INTO "competencies_historicalcompetency" VALUES(3,'Problemlərin Həlli','Analitik düşüncə və yaradıcı həll yolları tapmaq',1,'2025-10-11 07:48:55.769730','2025-10-11 07:48:55.769738',3,'2025-10-11 07:48:55.769810',NULL,'+',NULL);
INSERT INTO "competencies_historicalcompetency" VALUES(4,'Komanda İşi','Komanda mühitində effektiv əməkdaşlıq',1,'2025-10-11 07:48:55.770369','2025-10-11 07:48:55.770377',4,'2025-10-11 07:48:55.770491',NULL,'+',NULL);
INSERT INTO "competencies_historicalcompetency" VALUES(5,'Texniki Bilik','Sahə üzrə texniki bacarıq və biliklərin tətbiqi',1,'2025-10-11 07:48:55.771069','2025-10-11 07:48:55.771076',5,'2025-10-11 07:48:55.771149',NULL,'+',NULL);
INSERT INTO "competencies_historicalcompetency" VALUES(6,'Müştəri Yönümlülük','Müştəri ehtiyaclarını başa düşmək və cavab vermək',1,'2025-10-11 07:48:55.771731','2025-10-11 07:48:55.771738',6,'2025-10-11 07:48:55.771811',NULL,'+',NULL);
INSERT INTO "competencies_historicalcompetency" VALUES(7,'Vaxt İdarəetməsi','Vaxtı effektiv planlaşdırmaq və prioritetləri müəyyənləşdirmək',1,'2025-10-11 07:48:55.772386','2025-10-11 07:48:55.772394',7,'2025-10-11 07:48:55.772483',NULL,'+',NULL);
INSERT INTO "competencies_historicalcompetency" VALUES(8,'İnnovasiya','Yeni ideyalar və yanaşmalar təklif etmək',1,'2025-10-11 07:48:55.773117','2025-10-11 07:48:55.773124',8,'2025-10-11 07:48:55.773194',NULL,'+',NULL);
INSERT INTO "competencies_historicalcompetency" VALUES(9,'Rəhbərlik və Liderlik','Komandaya rəhbərlik etmək, motivasiya yaratmaq və strateji qərarlar qəbul etmək',1,'2025-10-15 07:47:48.646497','2025-10-15 07:47:48.646516',9,'2025-10-15 07:47:48.650673',NULL,'+',NULL);
INSERT INTO "competencies_historicalcompetency" VALUES(10,'Komanda İşi və Əməkdaşlıq','Komanda ilə effektiv işləmək, koordinasiya və əməkdaşlıq bacarıqları',1,'2025-10-15 07:47:48.661540','2025-10-15 07:47:48.661560',10,'2025-10-15 07:47:48.663719',NULL,'+',NULL);
INSERT INTO "competencies_historicalcompetency" VALUES(11,'Texniki Bilik (IT)','İnformasiya texnologiyaları sahəsində texniki bilik və bacarıqlar',1,'2025-10-15 07:47:48.672506','2025-10-15 07:47:48.672521',11,'2025-10-15 07:47:48.673612',NULL,'+',NULL);
CREATE TABLE "competencies_historicalpositioncompetency" ("id" bigint NOT NULL, "weight" integer NOT NULL, "is_mandatory" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "competency_id" bigint NULL, "history_user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "position_id" bigint NULL, "required_level_id" bigint NULL);
INSERT INTO "competencies_historicalpositioncompetency" VALUES(1,50,1,'2025-10-14 22:14:33.021896','2025-10-14 22:14:33.021917',1,'2025-10-14 22:14:33.028057',NULL,'+',5,1,6,4);
CREATE TABLE "competencies_historicaluserskill" ("id" bigint NOT NULL, "current_score" decimal NULL, "is_approved" bool NOT NULL, "approval_status" varchar(20) NOT NULL, "approved_at" datetime NULL, "self_assessment_score" decimal NULL, "notes" text NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "approved_by_id" bigint NULL, "competency_id" bigint NULL, "history_user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NULL, "level_id" bigint NULL);
INSERT INTO "competencies_historicaluserskill" VALUES(1,50,1,'approved',NULL,50,'aaaaaaaaaaa','2025-10-14 22:15:31.008420','2025-10-14 22:15:31.008439',1,'2025-10-14 22:15:31.012841',NULL,'+',2,8,1,1,4);
CREATE TABLE "competencies_positioncompetency" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "weight" integer NOT NULL, "is_mandatory" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "competency_id" bigint NOT NULL REFERENCES "competencies_competency" ("id") DEFERRABLE INITIALLY DEFERRED, "position_id" bigint NOT NULL REFERENCES "departments_position" ("id") DEFERRABLE INITIALLY DEFERRED, "required_level_id" bigint NULL REFERENCES "competencies_proficiencylevel" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "competencies_positioncompetency" VALUES(1,50,1,'2025-10-14 22:14:33.021896','2025-10-14 22:14:33.021917',5,6,4);
CREATE TABLE "competencies_proficiencylevel" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(50) NOT NULL UNIQUE, "display_name" varchar(100) NOT NULL, "score_min" decimal NOT NULL, "score_max" decimal NOT NULL, "description" text NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL);
INSERT INTO "competencies_proficiencylevel" VALUES(1,'basic','Əsas',0,40,'Əsas səviyyə - Başlanğıc bilik və bacarıqlar','2025-10-11 07:48:55.764337','2025-10-11 07:48:55.764360');
INSERT INTO "competencies_proficiencylevel" VALUES(2,'intermediate','Orta',40.01,70,'Orta səviyyə - Müstəqil işləmək bacarığı','2025-10-11 07:48:55.766396','2025-10-11 07:48:55.766447');
INSERT INTO "competencies_proficiencylevel" VALUES(3,'advanced','Təkmil',70.01,90,'Təkmil səviyyə - Yüksək səviyyədə mütəxəssislik','2025-10-11 07:48:55.766948','2025-10-11 07:48:55.766957');
INSERT INTO "competencies_proficiencylevel" VALUES(4,'expert','Ekspert',90.01,100,'Ekspert səviyyə - Sahə üzrə lider','2025-10-11 07:48:55.767345','2025-10-11 07:48:55.767352');
CREATE TABLE "competencies_userskill" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "current_score" decimal NULL, "is_approved" bool NOT NULL, "approval_status" varchar(20) NOT NULL, "approved_at" datetime NULL, "self_assessment_score" decimal NULL, "notes" text NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "approved_by_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "competency_id" bigint NOT NULL REFERENCES "competencies_competency" ("id") DEFERRABLE INITIALLY DEFERRED, "level_id" bigint NOT NULL REFERENCES "competencies_proficiencylevel" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "competencies_userskill" VALUES(1,50,1,'approved',NULL,50,'aaaaaaaaaaa','2025-10-14 22:15:31.008420','2025-10-14 22:15:31.008439',2,8,4,1);
CREATE TABLE "continuous_feedback_feedbackbank" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "total_feedbacks_received" integer NOT NULL, "total_recognitions" integer NOT NULL, "total_improvements" integer NOT NULL, "average_rating" decimal NOT NULL, "top_strengths" text NOT NULL CHECK ((JSON_VALID("top_strengths") OR "top_strengths" IS NULL)), "top_improvement_areas" text NOT NULL CHECK ((JSON_VALID("top_improvement_areas") OR "top_improvement_areas" IS NULL)), "positive_sentiment_score" decimal NOT NULL, "last_feedback_date" datetime NULL, "last_updated" datetime NOT NULL, "created_at" datetime NOT NULL, "user_id" bigint NOT NULL UNIQUE REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "continuous_feedback_feedbackbank" VALUES(1,1,1,0,0,'[]','[]',5,'2025-10-16 16:37:21.942503','2025-10-16 21:46:12.029148','2025-10-15 07:14:09.376146',1);
INSERT INTO "continuous_feedback_feedbackbank" VALUES(2,2,2,0,0,'[]','[]',0,'2025-10-16 12:52:02.086748','2025-10-16 12:52:02.114784','2025-10-15 07:19:21.050938',20);
INSERT INTO "continuous_feedback_feedbackbank" VALUES(3,1,0,1,0,'[]','[]',0,'2025-10-15 07:25:03.991344','2025-10-15 07:25:04.020302','2025-10-15 07:25:04.005321',2);
INSERT INTO "continuous_feedback_feedbackbank" VALUES(4,1,1,0,0,'[]','[]',0,'2025-10-16 21:41:42.746524','2025-10-16 21:41:42.788003','2025-10-16 21:41:42.769637',17);
CREATE TABLE "continuous_feedback_feedbacktag" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(50) NOT NULL UNIQUE, "description" text NOT NULL, "icon" varchar(50) NOT NULL, "is_active" bool NOT NULL, "usage_count" integer NOT NULL, "created_at" datetime NOT NULL);
INSERT INTO "continuous_feedback_feedbacktag" VALUES(1,'kitabxana','','',1,0,'2025-10-15 07:26:35.420175');
INSERT INTO "continuous_feedback_feedbacktag" VALUES(2,'test 1','','',1,0,'2025-10-15 07:26:46.537645');
INSERT INTO "continuous_feedback_feedbacktag" VALUES(3,'Komanda İşi','Komanda ilə əməkdaşlıq və birlikdə iş','fa-users',1,0,'2025-10-15 07:49:37.571790');
INSERT INTO "continuous_feedback_feedbacktag" VALUES(4,'test 2','','',1,0,'2025-10-16 21:47:26.391715');
INSERT INTO "continuous_feedback_feedbacktag" VALUES(5,'test 3','','',1,0,'2025-10-16 21:47:31.686889');
INSERT INTO "continuous_feedback_feedbacktag" VALUES(6,'test 4','','',1,0,'2025-10-16 21:47:37.313919');
CREATE TABLE "continuous_feedback_publicrecognition" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "likes_count" integer NOT NULL, "comments_count" integer NOT NULL, "views_count" integer NOT NULL, "is_featured" bool NOT NULL, "featured_until" datetime NULL, "published_at" datetime NOT NULL, "feedback_id" bigint NOT NULL UNIQUE REFERENCES "continuous_feedback_quickfeedback" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "continuous_feedback_publicrecognition" VALUES(1,0,0,0,1,'2025-10-16 12:45:57','2025-10-15 07:19:21.039242',1);
INSERT INTO "continuous_feedback_publicrecognition" VALUES(2,0,0,0,0,NULL,'2025-10-16 12:52:02.097364',3);
INSERT INTO "continuous_feedback_publicrecognition" VALUES(3,0,0,0,1,'2025-10-16 21:52:34','2025-10-16 16:37:21.955227',4);
INSERT INTO "continuous_feedback_publicrecognition" VALUES(4,0,0,0,0,NULL,'2025-10-16 21:41:42.758423',5);
CREATE TABLE "continuous_feedback_quickfeedback" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "feedback_type" varchar(20) NOT NULL, "visibility" varchar(10) NOT NULL, "title" varchar(200) NOT NULL, "message" text NOT NULL, "context" varchar(255) NOT NULL, "rating" integer NULL, "is_anonymous" bool NOT NULL, "is_read" bool NOT NULL, "read_at" datetime NULL, "recipient_response" text NOT NULL, "responded_at" datetime NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "is_flagged" bool NOT NULL, "flagged_reason" text NOT NULL, "recipient_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "related_competency_id" bigint NULL REFERENCES "competencies_competency" ("id") DEFERRABLE INITIALLY DEFERRED, "sender_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "continuous_feedback_quickfeedback" VALUES(1,'recognition','public','əla','super','',NULL,0,0,NULL,'',NULL,'2025-10-15 07:19:21.027181','2025-10-15 07:19:21.027202',0,'',20,NULL,1);
INSERT INTO "continuous_feedback_quickfeedback" VALUES(2,'improvement','team','22222222222222222','2222222222222222222222','',NULL,1,0,NULL,'',NULL,'2025-10-15 07:25:03.991344','2025-10-15 07:25:03.991368',0,'',2,NULL,1);
INSERT INTO "continuous_feedback_quickfeedback" VALUES(3,'recognition','public','1','2','',NULL,1,0,NULL,'',NULL,'2025-10-16 12:52:02.086748','2025-10-16 12:52:02.086768',0,'',20,NULL,1);
INSERT INTO "continuous_feedback_quickfeedback" VALUES(4,'recognition','public','salam','salam','',NULL,0,0,NULL,'',NULL,'2025-10-16 16:37:21.942503','2025-10-16 16:37:21.942525',0,'',1,NULL,30);
INSERT INTO "continuous_feedback_quickfeedback" VALUES(5,'general','public','admin','cd ...	Komut satırı bunu, cd komutundan sonra boşluk olmadan gelen, adı tam olarak "..." (üç nokta) olan bir dizine gitme isteği olarak yorumlar.	Bu isimde bir klasör büyük ihtimalle mevcut değildi.
cd. .	Teknik olarak cd . (geçerli dizin) komutunu çalıştırmayı dener, ancak aradaki fazladan boşluk ve nokta kombinasyonu komut yorumlayıcısını şaşırtır.	İstenen format .. (iki nokta) değil, . . (nokta, boşluk, nokta) idi.
cd....	Komut satırı bunu, adı tam olarak "...." (dört nokta) olan bir dizine gitme isteği olarak yorumlar.	Bu isimde bir klasörün de mevcut olması pek olası değildir.
cd .	Bu, "geçerli dizine git" anlamına gelir. Komut satırında tek bir nokta (.), her zaman içinde bulunduğunuz dizini temsil eder.	Zaten içinde bulunduğunuz dizine gitmek, konumunuzu değiştirmez.cd ...	Komut satırı bunu, cd komutundan sonra boşluk olmadan gelen, adı tam olarak "..." (üç nokta) olan bir dizine gitme isteği olarak yorumlar.	Bu isimde bir klasör büyük ihtimalle mevcut değildi.
cd. .	Teknik olarak cd . (geçerli dizin) komutunu çalıştırmayı dener, ancak aradaki fazladan boşluk ve nokta kombinasyonu komut yorumlayıcısını şaşırtır.	İstenen format .. (iki nokta) değil, . . (nokta, boşluk, nokta) idi.
cd....	Komut satırı bunu, adı tam olarak "...." (dört nokta) olan bir dizine gitme isteği olarak yorumlar.	Bu isimde bir klasörün de mevcut olması pek olası değildir.
cd .	Bu, "geçerli dizine git" anlamına gelir. Komut satırında tek bir nokta (.), her zaman içinde bulunduğunuz dizini temsil eder.	Zaten içinde bulunduğunuz dizine gitmek, konumunuzu değiştirmez.cd ...	Komut satırı bunu, cd komutundan sonra boşluk olmadan gelen, adı tam olarak "..." (üç nokta) olan bir dizine gitme isteği olarak yorumlar.	Bu isimde bir klasör büyük ihtimalle mevcut değildi.
cd. .	Teknik olarak cd . (geçerli dizin) komutunu çalıştırmayı dener, ancak aradaki fazladan boşluk ve nokta kombinasyonu komut yorumlayıcısını şaşırtır.	İstenen format .. (iki nokta) değil, . . (nokta, boşluk, nokta) idi.
cd....	Komut satırı bunu, adı tam olarak "...." (dört nokta) olan bir dizine gitme isteği olarak yorumlar.	Bu isimde bir klasörün de mevcut olması pek olası değildir.
cd .	Bu, "geçerli dizine git" anlamına gelir. Komut satırında tek bir nokta (.), her zaman içinde bulunduğunuz dizini temsil eder.	Zaten içinde bulunduğunuz dizine gitmek, konumunuzu değiştirmez.','dərs',5,0,1,NULL,'sağ olasancd ...	Komut satırı bunu, cd komutundan sonra boşluk olmadan gelen, adı tam olarak "..." (üç nokta) olan bir dizine gitme isteği olarak yorumlar.	Bu isimde bir klasör büyük ihtimalle mevcut değildi.
cd. .	Teknik olarak cd . (geçerli dizin) komutunu çalıştırmayı dener, ancak aradaki fazladan boşluk ve nokta kombinasyonu komut yorumlayıcısını şaşırtır.	İstenen format .. (iki nokta) değil, . . (nokta, boşluk, nokta) idi.
cd....	Komut satırı bunu, adı tam olarak "...." (dört nokta) olan bir dizine gitme isteği olarak yorumlar.	Bu isimde bir klasörün de mevcut olması pek olası değildir.
cd .	Bu, "geçerli dizine git" anlamına gelir. Komut satırında tek bir nokta (.), her zaman içinde bulunduğunuz dizini temsil eder.	Zaten içinde bulunduğunuz dizine gitmek, konumunuzu değiştirmez.',NULL,'2025-10-16 21:41:42.746524','2025-10-16 21:50:58.771909',1,'cd ...	Komut satırı bunu, cd komutundan sonra boşluk olmadan gelen, adı tam olarak "..." (üç nokta) olan bir dizine gitme isteği olarak yorumlar.	Bu isimde bir klasör büyük ihtimalle mevcut değildi.
cd. .	Teknik olarak cd . (geçerli dizin) komutunu çalıştırmayı dener, ancak aradaki fazladan boşluk ve nokta kombinasyonu komut yorumlayıcısını şaşırtır.	İstenen format .. (iki nokta) değil, . . (nokta, boşluk, nokta) idi.
cd....	Komut satırı bunu, adı tam olarak "...." (dört nokta) olan bir dizine gitme isteği olarak yorumlar.	Bu isimde bir klasörün de mevcut olması pek olası değildir.
cd .	Bu, "geçerli dizine git" anlamına gelir. Komut satırında tek bir nokta (.), her zaman içinde bulunduğunuz dizini temsil eder.	Zaten içinde bulunduğunuz dizine gitmek, konumunuzu değiştirmez.',17,11,1);
CREATE TABLE "continuous_feedback_quickfeedback_tags" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "quickfeedback_id" bigint NOT NULL REFERENCES "continuous_feedback_quickfeedback" ("id") DEFERRABLE INITIALLY DEFERRED, "feedbacktag_id" bigint NOT NULL REFERENCES "continuous_feedback_feedbacktag" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "continuous_feedback_quickfeedback_tags" VALUES(1,5,1);
INSERT INTO "continuous_feedback_quickfeedback_tags" VALUES(2,5,2);
INSERT INTO "continuous_feedback_quickfeedback_tags" VALUES(3,5,3);
INSERT INTO "continuous_feedback_quickfeedback_tags" VALUES(4,5,4);
INSERT INTO "continuous_feedback_quickfeedback_tags" VALUES(5,5,5);
INSERT INTO "continuous_feedback_quickfeedback_tags" VALUES(6,5,6);
CREATE TABLE "continuous_feedback_recognitioncomment" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "comment" text NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "recognition_id" bigint NOT NULL REFERENCES "continuous_feedback_publicrecognition" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "continuous_feedback_recognitioncomment" VALUES(1,'11111111111111111111111111111111','2025-10-16 12:45:21.320818','2025-10-16 12:45:21.320874',1,1);
INSERT INTO "continuous_feedback_recognitioncomment" VALUES(2,'000000000000','2025-10-16 12:45:38.779435','2025-10-16 12:45:38.779456',1,20);
CREATE TABLE "continuous_feedback_recognitionlike" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "recognition_id" bigint NOT NULL REFERENCES "continuous_feedback_publicrecognition" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "continuous_feedback_recognitionlike" VALUES(1,'2025-10-16 12:44:41.944436',1,1);
INSERT INTO "continuous_feedback_recognitionlike" VALUES(2,'2025-10-16 12:44:59.029447',1,20);
CREATE TABLE "dashboard_analyticsreport" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(200) NOT NULL, "report_type" varchar(20) NOT NULL, "data" text NOT NULL CHECK ((JSON_VALID("data") OR "data" IS NULL)), "start_date" datetime NOT NULL, "end_date" datetime NOT NULL, "is_published" bool NOT NULL, "file_path" varchar(500) NOT NULL, "created_at" datetime NOT NULL, "generated_by_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "dashboard_dashboardwidget" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(200) NOT NULL, "widget_type" varchar(20) NOT NULL, "title" varchar(200) NOT NULL, "description" text NOT NULL, "order" integer unsigned NOT NULL CHECK ("order" >= 0), "is_active" bool NOT NULL, "config" text NOT NULL CHECK ((JSON_VALID("config") OR "config" IS NULL)), "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL);
CREATE TABLE "dashboard_forecastdata" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "forecast_type" varchar(50) NOT NULL, "forecast_date" date NOT NULL, "predicted_value" decimal NOT NULL, "confidence_level" decimal NOT NULL, "actual_value" decimal NULL, "explanation" text NOT NULL, "created_at" datetime NOT NULL, "department_id" bigint NULL REFERENCES "departments_department" ("id") DEFERRABLE INITIALLY DEFERRED, "organization_id" bigint NULL REFERENCES "departments_organization" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "dashboard_forecastdata" VALUES(1,'staffing','2026-04-17',1.2,95,NULL,'AI tərəfindən əsas trendlərə əsasən proqnozlaşdırılıb: Təşkilatın genişlənməsi və layihələrin artması nəzərə alınaraq 6 ay ərzində işçi sayı artacaq.','2025-10-17 16:31:43.587623',NULL,NULL);
INSERT INTO "dashboard_forecastdata" VALUES(2,'budget','2026-04-17',14000,95,NULL,'AI tərəfindən əmək haqqı trendləri və işə qəbul planlarına əsasən proqnozlaşdırılıb: 6 ay ərzində əmək haqqı fondunun artırılması gözlənilir.','2025-10-17 16:31:43.612588',NULL,NULL);
INSERT INTO "dashboard_forecastdata" VALUES(3,'performance','2026-04-17',0,95,NULL,'AI tərəfindən qiymətləndirmə nəticələrinin trendlərinə əsasən proqnozlaşdırılıb: Təlim və inkişaf tədbirlərinin təsiri nəzərə alınaraq performansın artırılması gözlənilir.','2025-10-17 16:31:43.640570',NULL,NULL);
CREATE TABLE "dashboard_realtimestat" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "stat_type" varchar(30) NOT NULL, "current_value" decimal NOT NULL, "previous_value" decimal NULL, "unit" varchar(20) NOT NULL, "description" varchar(200) NOT NULL, "last_updated" datetime NOT NULL, "organization_id" bigint NULL REFERENCES "departments_organization" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "dashboard_realtimestat" VALUES(1,'active_users',30,NULL,'','Aktiv İstifadəçilər','2025-10-17 16:32:01.424010',NULL);
INSERT INTO "dashboard_realtimestat" VALUES(2,'pending_evaluations',53,NULL,'','Gözləyən Qiymətləndirmələr','2025-10-17 16:32:01.433564',NULL);
INSERT INTO "dashboard_realtimestat" VALUES(3,'new_hires',30,NULL,'','Bu Ay Yeni İşə Qəbul','2025-10-17 16:32:01.440879',NULL);
INSERT INTO "dashboard_realtimestat" VALUES(4,'avg_performance',3.81,NULL,'','Ortalama Performans','2025-10-17 16:32:01.448118',NULL);
INSERT INTO "dashboard_realtimestat" VALUES(5,'budget_utilization',113999,NULL,'₼','Ümumi Maaş Fonduna','2025-10-17 16:32:01.456317',NULL);
INSERT INTO "dashboard_realtimestat" VALUES(6,'leave_requests',0,NULL,'','Gözləyən Məzuniyyət Sorğuları','2025-10-17 16:32:01.464909',NULL);
INSERT INTO "dashboard_realtimestat" VALUES(7,'training_completions',0,NULL,'','Təlim Tamamlamaları','2025-10-17 16:32:01.471785',NULL);
CREATE TABLE "dashboard_systemkpi" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(200) NOT NULL, "kpi_type" varchar(20) NOT NULL, "value" decimal NOT NULL, "target" decimal NULL, "unit" varchar(20) NOT NULL, "period_start" datetime NOT NULL, "period_end" datetime NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL);
INSERT INTO "dashboard_systemkpi" VALUES(1,'Aktiv İstifadəçilər','overall',30,33,'','2025-10-01 00:00:00','2025-10-17 16:31:43.647705','2025-10-17 16:31:43.649422','2025-10-17 16:31:43.649428');
INSERT INTO "dashboard_systemkpi" VALUES(2,'Aktiv İstifadəçilər','overall',30,33,'','2025-10-01 00:00:00','2025-10-17 16:32:01.670070','2025-10-17 16:32:01.671854','2025-10-17 16:32:01.671859');
INSERT INTO "dashboard_systemkpi" VALUES(3,'Qiymətləndirmə İştirakı','overall',3.64,85,'%','2025-10-01 00:00:00','2025-10-17 16:32:01.670070','2025-10-17 16:32:01.680246','2025-10-17 16:32:01.680270');
INSERT INTO "dashboard_systemkpi" VALUES(4,'Ortalama Performans','performance',3.81,4,'/5','2025-10-01 00:00:00','2025-10-17 16:32:01.670070','2025-10-17 16:32:01.688225','2025-10-17 16:32:01.688230');
INSERT INTO "dashboard_systemkpi" VALUES(5,'Maaş Ödənişi Vaxtında','salary',98.5,100,'%','2025-10-01 00:00:00','2025-10-17 16:32:01.670070','2025-10-17 16:32:01.695331','2025-10-17 16:32:01.695340');
CREATE TABLE "dashboard_trenddata" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "data_type" varchar(50) NOT NULL, "period" date NOT NULL, "value" decimal NOT NULL, "created_at" datetime NOT NULL, "department_id" bigint NULL REFERENCES "departments_department" ("id") DEFERRABLE INITIALLY DEFERRED, "organization_id" bigint NULL REFERENCES "departments_organization" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "dashboard_trenddata" VALUES(1,'salary','2025-10-17',28499.75,'2025-10-17 16:29:49.849106',NULL,NULL);
INSERT INTO "dashboard_trenddata" VALUES(2,'performance','2025-10-17',0,'2025-10-17 16:29:49.879196',NULL,NULL);
INSERT INTO "dashboard_trenddata" VALUES(3,'hiring','2025-10-17',0,'2025-10-17 16:29:49.887721',NULL,NULL);
CREATE TABLE "departments_department" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(200) NOT NULL, "code" varchar(20) NOT NULL, "description" text NOT NULL, "phone" varchar(20) NOT NULL, "email" varchar(254) NOT NULL, "location" varchar(200) NOT NULL, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "lft" integer unsigned NOT NULL CHECK ("lft" >= 0), "rght" integer unsigned NOT NULL CHECK ("rght" >= 0), "tree_id" integer unsigned NOT NULL CHECK ("tree_id" >= 0), "level" integer unsigned NOT NULL CHECK ("level" >= 0), "head_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "organization_id" bigint NOT NULL REFERENCES "departments_organization" ("id") DEFERRABLE INITIALLY DEFERRED, "parent_id" bigint NULL REFERENCES "departments_department" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "departments_department" VALUES(1,'İnsan Resursları Şöbəsi','HR','HR department','','','',1,'2025-10-10 15:39:44.216652','2025-10-10 15:39:44.216670',1,2,9,0,NULL,2,NULL);
INSERT INTO "departments_department" VALUES(2,'İnformasiya Texnologiyaları Şöbəsi','IT','IT department','','','',1,'2025-10-10 15:39:44.230156','2025-10-10 15:39:44.230172',1,4,7,0,NULL,2,NULL);
INSERT INTO "departments_department" VALUES(3,'Maliyyə Şöbəsi','FIN','Büdcə və maliyyə idarəetməsi','','','',1,'2025-10-10 15:54:56.494604','2025-10-10 15:54:56.494622',1,2,4,0,NULL,2,NULL);
INSERT INTO "departments_department" VALUES(4,'Hüquq Şöbəsi','LEGAL','Hüquqi məsləhət və sənədləşmə','','','',1,'2025-10-10 15:54:56.505118','2025-10-10 15:54:56.505131',1,2,3,0,NULL,2,NULL);
INSERT INTO "departments_department" VALUES(5,'İctimaiyyətlə Əlaqələr Şöbəsi','PR','PR və kommunikasiya','','','',1,'2025-10-10 15:54:56.515258','2025-10-10 15:54:56.515274',1,2,6,0,NULL,2,NULL);
INSERT INTO "departments_department" VALUES(6,'Rəqəmsal İnkişaf Departamenti','RID','Rəqəmsal transformasiya layihələrinin idarə edilməsi','+994 12 404 50 10','digital@mincom.gov.az','Mərkəzi bina, 3-cü mərtəbə',1,'2025-10-15 07:47:47.294596','2025-10-15 07:47:47.294626',1,6,5,0,NULL,3,NULL);
INSERT INTO "departments_department" VALUES(7,'E-xidmətlər Şöbəsi','EXS','Elektron xidmətlərin hazırlanması və idarə edilməsi','+994 12 404 50 11','eservices@mincom.gov.az','Mərkəzi bina, 3-cü mərtəbə, otaq 310',1,'2025-10-15 07:47:47.315226','2025-10-15 07:47:47.315250',2,3,5,1,NULL,3,6);
INSERT INTO "departments_department" VALUES(8,'Kibertəhlükəsizlik Şöbəsi','KTS','İnformasiya təhlükəsizliyi və kibertəhlükəsizlik','+994 12 404 50 12','cybersec@mincom.gov.az','Mərkəzi bina, 2-ci mərtəbə',1,'2025-10-15 07:47:47.331040','2025-10-15 07:47:47.331063',4,5,5,1,NULL,3,6);
INSERT INTO "departments_department" VALUES(9,'İnsan Resursları və Təlim Mərkəzi','IRTM','Kadr siyasəti və işçilərin inkişafı','+994 12 404 50 20','hr@mincom.gov.az','Mərkəzi bina, 1-ci mərtəbə',1,'2025-10-15 07:47:47.348504','2025-10-15 07:47:47.348549',1,2,8,0,NULL,3,NULL);
INSERT INTO "departments_department" VALUES(10,'helpdes','000012','sssssssssssss','0605536990','muradoffcode@gmail.com','',1,'2025-10-15 11:58:13.051232','2025-10-15 11:58:50.231960',2,3,7,1,20,1,2);
INSERT INTO "departments_department" VALUES(11,'Debug Dept','DEBUG_DEPT','','','','',1,'2025-10-17 18:51:01.576307','2025-10-17 18:51:01.576327',1,2,2,0,NULL,4,NULL);
INSERT INTO "departments_department" VALUES(12,'Dash Dept','DASH_DEPT','','','','',1,'2025-10-17 19:11:18.445517','2025-10-17 19:11:18.445543',1,2,1,0,NULL,5,NULL);
CREATE TABLE "departments_historicaldepartment" ("id" bigint NOT NULL, "name" varchar(200) NOT NULL, "code" varchar(20) NOT NULL, "description" text NOT NULL, "phone" varchar(20) NOT NULL, "email" varchar(254) NOT NULL, "location" varchar(200) NOT NULL, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "head_id" bigint NULL, "history_user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "organization_id" bigint NULL, "parent_id" bigint NULL);
INSERT INTO "departments_historicaldepartment" VALUES(1,'İnsan Resursları Şöbəsi','HR','HR department','','','',1,'2025-10-10 15:39:44.216652','2025-10-10 15:39:44.216670',1,'2025-10-10 15:39:44.219286',NULL,'+',NULL,NULL,2,NULL);
INSERT INTO "departments_historicaldepartment" VALUES(2,'İnformasiya Texnologiyaları Şöbəsi','IT','IT department','','','',1,'2025-10-10 15:39:44.230156','2025-10-10 15:39:44.230172',2,'2025-10-10 15:39:44.230449',NULL,'+',NULL,NULL,2,NULL);
INSERT INTO "departments_historicaldepartment" VALUES(3,'Maliyyə Şöbəsi','FIN','Büdcə və maliyyə idarəetməsi','','','',1,'2025-10-10 15:54:56.494604','2025-10-10 15:54:56.494622',3,'2025-10-10 15:54:56.495055',NULL,'+',NULL,NULL,2,NULL);
INSERT INTO "departments_historicaldepartment" VALUES(4,'Hüquq Şöbəsi','LEGAL','Hüquqi məsləhət və sənədləşmə','','','',1,'2025-10-10 15:54:56.505118','2025-10-10 15:54:56.505131',4,'2025-10-10 15:54:56.505370',NULL,'+',NULL,NULL,2,NULL);
INSERT INTO "departments_historicaldepartment" VALUES(5,'İctimaiyyətlə Əlaqələr Şöbəsi','PR','PR və kommunikasiya','','','',1,'2025-10-10 15:54:56.515258','2025-10-10 15:54:56.515274',5,'2025-10-10 15:54:56.515513',NULL,'+',NULL,NULL,2,NULL);
INSERT INTO "departments_historicaldepartment" VALUES(6,'Rəqəmsal İnkişaf Departamenti','RID','Rəqəmsal transformasiya layihələrinin idarə edilməsi','+994 12 404 50 10','digital@mincom.gov.az','Mərkəzi bina, 3-cü mərtəbə',1,'2025-10-15 07:47:47.294596','2025-10-15 07:47:47.294626',6,'2025-10-15 07:47:47.296558',NULL,'+',NULL,NULL,3,NULL);
INSERT INTO "departments_historicaldepartment" VALUES(7,'E-xidmətlər Şöbəsi','EXS','Elektron xidmətlərin hazırlanması və idarə edilməsi','+994 12 404 50 11','eservices@mincom.gov.az','Mərkəzi bina, 3-cü mərtəbə, otaq 310',1,'2025-10-15 07:47:47.315226','2025-10-15 07:47:47.315250',7,'2025-10-15 07:47:47.315747',NULL,'+',NULL,NULL,3,6);
INSERT INTO "departments_historicaldepartment" VALUES(8,'Kibertəhlükəsizlik Şöbəsi','KTS','İnformasiya təhlükəsizliyi və kibertəhlükəsizlik','+994 12 404 50 12','cybersec@mincom.gov.az','Mərkəzi bina, 2-ci mərtəbə',1,'2025-10-15 07:47:47.331040','2025-10-15 07:47:47.331063',8,'2025-10-15 07:47:47.331570',NULL,'+',NULL,NULL,3,6);
INSERT INTO "departments_historicaldepartment" VALUES(9,'İnsan Resursları və Təlim Mərkəzi','IRTM','Kadr siyasəti və işçilərin inkişafı','+994 12 404 50 20','hr@mincom.gov.az','Mərkəzi bina, 1-ci mərtəbə',1,'2025-10-15 07:47:47.348504','2025-10-15 07:47:47.348549',9,'2025-10-15 07:47:47.349257',NULL,'+',NULL,NULL,3,NULL);
INSERT INTO "departments_historicaldepartment" VALUES(10,'helpdes','000012','sssssssssssss','0605536990','muradoffcode@gmail.com','',1,'2025-10-15 11:58:13.051232','2025-10-15 11:58:13.051257',10,'2025-10-15 11:58:13.051984',NULL,'+',20,1,1,8);
INSERT INTO "departments_historicaldepartment" VALUES(10,'helpdes','000012','sssssssssssss','0605536990','muradoffcode@gmail.com','',1,'2025-10-15 11:58:13.051232','2025-10-15 11:58:50.231960',11,'2025-10-15 11:58:50.233182',NULL,'~',20,1,1,2);
INSERT INTO "departments_historicaldepartment" VALUES(11,'Debug Dept','DEBUG_DEPT','','','','',1,'2025-10-17 18:51:01.576307','2025-10-17 18:51:01.576327',12,'2025-10-17 18:51:01.585170',NULL,'+',NULL,NULL,4,NULL);
INSERT INTO "departments_historicaldepartment" VALUES(12,'Dash Dept','DASH_DEPT','','','','',1,'2025-10-17 19:11:18.445517','2025-10-17 19:11:18.445543',13,'2025-10-17 19:11:18.458907',NULL,'+',NULL,NULL,5,NULL);
CREATE TABLE "departments_historicalorganization" ("id" bigint NOT NULL, "name" varchar(200) NOT NULL, "short_name" varchar(50) NOT NULL, "code" varchar(20) NOT NULL, "description" text NOT NULL, "address" text NOT NULL, "phone" varchar(20) NOT NULL, "email" varchar(254) NOT NULL, "website" varchar(200) NOT NULL, "is_active" bool NOT NULL, "established_date" date NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "history_user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "departments_historicalorganization" VALUES(1,'Mədəniyyət Nazirliyi','Mədəniyyət','0001','nazirlik','Nakhchivan City
Nakhchivan City','0605536990','muradoffcode@gmail.com','http://q360.com',1,'2025-10-09','2025-10-09 07:14:01.118197','2025-10-09 07:14:01.118216',1,'2025-10-09 07:14:01.120037',NULL,'+',1);
INSERT INTO "departments_historicalorganization" VALUES(2,'Dövlət İdarəsi','DI','GOV001','Test təşkilatı','','','info@gov.az','',1,NULL,'2025-10-10 11:26:18.797688','2025-10-10 11:26:18.797706',2,'2025-10-10 11:26:18.804134',NULL,'+',NULL);
INSERT INTO "departments_historicalorganization" VALUES(3,'Azərbaycan Respublikası Rəqəmsal İnkişaf və Nəqliyyat Nazirliyi','RİNN','MINT','Rəqəmsal texnologiyalar, informasiya cəmiyyəti və nəqliyyat','Bakı şəhəri, Yasamal rayonu, Şərifzadə küçəsi 22','+994 12 404 50 00','info@mincom.gov.az','https://mincom.gov.az',1,'2019-07-15','2025-10-15 07:47:47.265718','2025-10-15 07:47:47.265745',3,'2025-10-15 07:47:47.270078',NULL,'+',NULL);
INSERT INTO "departments_historicalorganization" VALUES(4,'Debug Org','DBG','DEBUG_ORG','','','','','',1,NULL,'2025-10-17 18:51:01.550229','2025-10-17 18:51:01.550257',4,'2025-10-17 18:51:01.558261',NULL,'+',NULL);
INSERT INTO "departments_historicalorganization" VALUES(5,'Dash Org','DORG','DASH_TEST','','','','','',1,NULL,'2025-10-17 19:11:18.409199','2025-10-17 19:11:18.409239',5,'2025-10-17 19:11:18.420007',NULL,'+',NULL);
CREATE TABLE "departments_historicalposition" ("id" bigint NOT NULL, "title" varchar(200) NOT NULL, "code" varchar(20) NOT NULL, "description" text NOT NULL, "responsibilities" text NOT NULL, "required_education" varchar(100) NOT NULL, "required_experience" varchar(100) NOT NULL, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "department_id" bigint NULL, "history_user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "organization_id" bigint NULL, "reports_to_id" bigint NULL, "level" integer NOT NULL);
INSERT INTO "departments_historicalposition" VALUES(1,'Direktor','DIR','','','','',1,'2025-10-10 15:54:56.522346','2025-10-10 15:54:56.522360',1,'2025-10-10 15:54:56.523509',NULL,'+',1,NULL,2,NULL,1);
INSERT INTO "departments_historicalposition" VALUES(2,'HR Meneceri','HRMGR','','','','',1,'2025-10-10 15:54:56.531736','2025-10-10 15:54:56.531750',2,'2025-10-10 15:54:56.532834',NULL,'+',1,NULL,2,NULL,2);
INSERT INTO "departments_historicalposition" VALUES(3,'HR Mütəxəssisi','HRSPEC','','','','',1,'2025-10-10 15:54:56.539378','2025-10-10 15:54:56.539391',3,'2025-10-10 15:54:56.540422',NULL,'+',1,NULL,2,NULL,3);
INSERT INTO "departments_historicalposition" VALUES(4,'IT Meneceri','ITMGR','','','','',1,'2025-10-10 15:54:56.548283','2025-10-10 15:54:56.548296',4,'2025-10-10 15:54:56.549370',NULL,'+',2,NULL,2,NULL,2);
INSERT INTO "departments_historicalposition" VALUES(5,'Proqramçı','DEVELOPER','','','','',1,'2025-10-10 15:54:56.555813','2025-10-10 15:54:56.555826',5,'2025-10-10 15:54:56.556855',NULL,'+',2,NULL,2,NULL,3);
INSERT INTO "departments_historicalposition" VALUES(6,'Sistem Administratoru','SYSADMIN','','','','',1,'2025-10-10 15:54:56.563922','2025-10-10 15:54:56.563935',6,'2025-10-10 15:54:56.564910',NULL,'+',2,NULL,2,NULL,3);
INSERT INTO "departments_historicalposition" VALUES(7,'Maliyyə Meneceri','FINMGR','','','','',1,'2025-10-10 15:54:56.572158','2025-10-10 15:54:56.572171',7,'2025-10-10 15:54:56.573118',NULL,'+',3,NULL,2,NULL,2);
INSERT INTO "departments_historicalposition" VALUES(8,'Mühasib','ACCOUNTANT','','','','',1,'2025-10-10 15:54:56.579597','2025-10-10 15:54:56.579610',8,'2025-10-10 15:54:56.580613',NULL,'+',3,NULL,2,NULL,3);
INSERT INTO "departments_historicalposition" VALUES(9,'Hüquqşünas','LAWYER','','','','',1,'2025-10-10 15:54:56.587410','2025-10-10 15:54:56.587422',9,'2025-10-10 15:54:56.588439',NULL,'+',4,NULL,2,NULL,3);
INSERT INTO "departments_historicalposition" VALUES(10,'PR Mütəxəssisi','PRSPEC','','','','',1,'2025-10-10 15:54:56.595430','2025-10-10 15:54:56.595444',10,'2025-10-10 15:54:56.596508',NULL,'+',5,NULL,2,NULL,3);
INSERT INTO "departments_historicalposition" VALUES(1,'Direktor','DIR','aaaaaaaaaa','','a','a',1,'2025-10-10 15:54:56.522346','2025-10-16 21:55:23.957213',11,'2025-10-16 21:55:23.962028',NULL,'~',1,1,2,5,3);
CREATE TABLE "departments_organization" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(200) NOT NULL UNIQUE, "short_name" varchar(50) NOT NULL, "code" varchar(20) NOT NULL UNIQUE, "description" text NOT NULL, "address" text NOT NULL, "phone" varchar(20) NOT NULL, "email" varchar(254) NOT NULL, "website" varchar(200) NOT NULL, "is_active" bool NOT NULL, "established_date" date NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL);
INSERT INTO "departments_organization" VALUES(1,'Mədəniyyət Nazirliyi','Mədəniyyət','0001','nazirlik','Nakhchivan City
Nakhchivan City','0605536990','muradoffcode@gmail.com','http://q360.com',1,'2025-10-09','2025-10-09 07:14:01.118197','2025-10-09 07:14:01.118216');
INSERT INTO "departments_organization" VALUES(2,'Dövlət İdarəsi','DI','GOV001','Test təşkilatı','','','info@gov.az','',1,NULL,'2025-10-10 11:26:18.797688','2025-10-10 11:26:18.797706');
INSERT INTO "departments_organization" VALUES(3,'Azərbaycan Respublikası Rəqəmsal İnkişaf və Nəqliyyat Nazirliyi','RİNN','MINT','Rəqəmsal texnologiyalar, informasiya cəmiyyəti və nəqliyyat','Bakı şəhəri, Yasamal rayonu, Şərifzadə küçəsi 22','+994 12 404 50 00','info@mincom.gov.az','https://mincom.gov.az',1,'2019-07-15','2025-10-15 07:47:47.265718','2025-10-15 07:47:47.265745');
INSERT INTO "departments_organization" VALUES(4,'Debug Org','DBG','DEBUG_ORG','','','','','',1,NULL,'2025-10-17 18:51:01.550229','2025-10-17 18:51:01.550257');
INSERT INTO "departments_organization" VALUES(5,'Dash Org','DORG','DASH_TEST','','','','','',1,NULL,'2025-10-17 19:11:18.409199','2025-10-17 19:11:18.409239');
CREATE TABLE "departments_position" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(200) NOT NULL, "code" varchar(20) NOT NULL, "description" text NOT NULL, "responsibilities" text NOT NULL, "level" integer NOT NULL, "required_education" varchar(100) NOT NULL, "required_experience" varchar(100) NOT NULL, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "department_id" bigint NULL REFERENCES "departments_department" ("id") DEFERRABLE INITIALLY DEFERRED, "organization_id" bigint NOT NULL REFERENCES "departments_organization" ("id") DEFERRABLE INITIALLY DEFERRED, "reports_to_id" bigint NULL REFERENCES "departments_position" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "departments_position" VALUES(1,'Direktor','DIR','aaaaaaaaaa','',3,'a','a',1,'2025-10-10 15:54:56.522346','2025-10-16 21:55:23.957213',1,2,5);
INSERT INTO "departments_position" VALUES(2,'HR Meneceri','HRMGR','','',2,'','',1,'2025-10-10 15:54:56.531736','2025-10-10 15:54:56.531750',1,2,NULL);
INSERT INTO "departments_position" VALUES(3,'HR Mütəxəssisi','HRSPEC','','',3,'','',1,'2025-10-10 15:54:56.539378','2025-10-10 15:54:56.539391',1,2,NULL);
INSERT INTO "departments_position" VALUES(4,'IT Meneceri','ITMGR','','',2,'','',1,'2025-10-10 15:54:56.548283','2025-10-10 15:54:56.548296',2,2,NULL);
INSERT INTO "departments_position" VALUES(5,'Proqramçı','DEVELOPER','','',3,'','',1,'2025-10-10 15:54:56.555813','2025-10-10 15:54:56.555826',2,2,NULL);
INSERT INTO "departments_position" VALUES(6,'Sistem Administratoru','SYSADMIN','','',3,'','',1,'2025-10-10 15:54:56.563922','2025-10-10 15:54:56.563935',2,2,NULL);
INSERT INTO "departments_position" VALUES(7,'Maliyyə Meneceri','FINMGR','','',2,'','',1,'2025-10-10 15:54:56.572158','2025-10-10 15:54:56.572171',3,2,NULL);
INSERT INTO "departments_position" VALUES(8,'Mühasib','ACCOUNTANT','','',3,'','',1,'2025-10-10 15:54:56.579597','2025-10-10 15:54:56.579610',3,2,NULL);
INSERT INTO "departments_position" VALUES(9,'Hüquqşünas','LAWYER','','',3,'','',1,'2025-10-10 15:54:56.587410','2025-10-10 15:54:56.587422',4,2,NULL);
INSERT INTO "departments_position" VALUES(10,'PR Mütəxəssisi','PRSPEC','','',3,'','',1,'2025-10-10 15:54:56.595430','2025-10-10 15:54:56.595444',5,2,NULL);
CREATE TABLE "development_plans_developmentgoal" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(200) NOT NULL, "description" text NOT NULL, "category" varchar(100) NOT NULL, "status" varchar(20) NOT NULL, "target_date" date NOT NULL, "completion_date" date NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "created_by_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "approval_note" text NOT NULL, "approved_at" datetime NULL, "approved_by_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "development_plans_developmentgoal" VALUES(1,'azərbaycan','azərbaycan Respublikası Konstitusiyasının mətnində bu','usersd','completed','2025-10-09','2025-10-09','2025-10-09 07:29:47.555072','2025-10-09 11:25:12.928872',1,1,'',NULL,NULL);
INSERT INTO "development_plans_developmentgoal" VALUES(2,'inkişaf','dövlət sistemlərinin mühafizəsi','Nazirlik','completed','2025-10-09','2025-10-09','2025-10-09 12:08:06.159888','2025-10-10 20:42:15.800493',1,1,'',NULL,NULL);
INSERT INTO "development_plans_developmentgoal" VALUES(3,'Python proqramlaşdırma bacarıqlarını intermediate səviyyəyə çatdırmaq','Django framework-ü öyrənmək və real layihələrdə iştirak etmək','Texniki İnkişaf','active','2024-05-31',NULL,'2025-10-15 07:47:48.731094','2025-10-15 07:47:48.731100',23,23,'','2025-10-15 07:47:48.729851',22);
INSERT INTO "development_plans_developmentgoal" VALUES(4,'Layihənizin əsas xüsusiyyətləri olan 360 Dərəcə Rəy, Performans, Bacarıqlar','Layihənizin əsas xüsusiyyətləri olan 360 Dərəcə Rəy, Performans, Bacarıqlar və Tam İdarəetmə üzərində qurulmuş adlardır.Layihənizin əsas xüsusiyyətləri olan 360 Dərəcə Rəy, Performans, Bacarıqlar və Tam İdarəetmə üzərində qurulmuş adlardır.Layihənizin əsas xüsusiyyətləri olan 360 Dərəcə Rəy, Performans, Bacarıqlar və Tam İdarəetmə üzərində qurulmuş adlardır.Layihənizin əsas xüsusiyyətləri olan 360 Dərəcə Rəy, Performans, Bacarıqlar və Tam İdarəetmə üzərində qurulmuş adlardır.Layihənizin əsas xüsusiyyətləri olan 360 Dərəcə Rəy, Performans, Bacarıqlar və Tam İdarəetmə üzərində qurulmuş adlardır.','Problem Həlli','active','2025-12-31',NULL,'2025-10-16 22:19:53.933196','2025-10-16 22:19:53.933214',1,1,'',NULL,NULL);
CREATE TABLE "development_plans_historicalkeyresult" ("id" bigint NOT NULL, "title" varchar(300) NOT NULL, "description" text NOT NULL, "unit" varchar(20) NOT NULL, "baseline_value" decimal NOT NULL, "target_value" decimal NOT NULL, "current_value" decimal NOT NULL, "weight" decimal NOT NULL, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "history_user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "objective_id" bigint NULL);
INSERT INTO "development_plans_historicalkeyresult" VALUES(1,'aaa','','boolean',0,5,3,100,1,'2025-10-16 21:59:36.200383','2025-10-16 21:59:36.200417',1,'2025-10-16 21:59:36.201919',NULL,'+',1,1);
INSERT INTO "development_plans_historicalkeyresult" VALUES(1,'aaa','','boolean',0,5,5,100,1,'2025-10-16 21:59:36.200383','2025-10-16 22:22:30.806740',2,'2025-10-16 22:22:30.818048',NULL,'~',1,1);
INSERT INTO "development_plans_historicalkeyresult" VALUES(1,'aaa','','boolean',0,5,5,100,1,'2025-10-16 21:59:36.200383','2025-10-16 22:29:02.755330',3,'2025-10-16 22:29:02.765903',NULL,'~',1,1);
INSERT INTO "development_plans_historicalkeyresult" VALUES(1,'aaa','','boolean',0,5,5,100,1,'2025-10-16 21:59:36.200383','2025-10-16 23:06:29.672281',4,'2025-10-16 23:06:29.683892',NULL,'~',1,1);
CREATE TABLE "development_plans_historicalkpi" ("id" bigint NOT NULL, "name" varchar(200) NOT NULL, "description" text NOT NULL, "code" varchar(50) NOT NULL, "unit" varchar(50) NOT NULL, "target_value" decimal NOT NULL, "measurement_frequency" varchar(20) NOT NULL, "red_threshold" decimal NOT NULL, "yellow_threshold" decimal NOT NULL, "green_threshold" decimal NOT NULL, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "department_id" bigint NULL, "history_user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "objective_id" bigint NULL, "owner_id" bigint NULL);
INSERT INTO "development_plans_historicalkpi" VALUES(1,'AzAgroPOS','İstifadəçinin tələb etdiyi 9 məsələ tam həll edildi:

  1. ✅ Modul İnteqrasiyası

  - templates/base/sidebar.html - Bütün yeni modullar və təhlükəsizlik dashboardu əlavə edildi (sətir 432-441)
  - apps/accounts/template_views.py - Dashboard tam HRIS modul datası ilə təchiz edildi (sətir 59-205)
  - Bütün yeni modullar navbar və sidebar-da mövcuddur

  2. ✅ Report Export Funksionallığı

  - PDF export: apps/reports/template_views.py - ReportLab ilə PDF yaradılması (sətir 58-110)
  - Excel export: OpenPyXL ilə XLSX formatı (sətir 112-152)
  - CSV export: apps/reports/utils.py - UTF-8-sig BOM ilə Excel uyğunluğu (sətir 95-117)
  - Multi-format endpoint: /reports/export/<format>/

  3. ✅ Kompensasiya Büdcə Məntiq

  Yeni model əlavə edildi: apps/compensation/models.py (sətir 510-601)
  - DepartmentBudget modeli illik büdcə, istifadə edilmiş məbləğ və qalıq hesablamaları
  - can_afford() metodu ilə büdcə yoxlaması
  - utilization_percentage property

  View-də büdcə validasiyası: apps/compensation/views.py (sətir 118-149)
  if dept_budget:
      if not dept_budget.can_afford(salary_difference):
          return JsonResponse({
              ''success'': False,
              ''message'': f''Büdcə kifayət etmir!...'',
              ''budget_exceeded'': True
          })

  Admin panel: Rəngli utilization percentage və remaining budget göstəricisi

  4. ✅ Kanban Drag-and-Drop

  Sortable.js tam inteqrasiya: templates/recruitment/candidate_pipeline.html (sətir 366-541)

  Əlavə edilən xüsusiyyətlər:
  - ✅ CSRF token düzgün implementasiyası (getCookie funksiyası)
  - ✅ Toast notification sistemi (slideIn/slideOut animation)
  - ✅ Loading state (.updating class)
  - ✅ Auto-revert on error
  - ✅ Real-time stage count update
  - ✅ Visual feedback (ghost class, chosen class)
  - ✅ Smooth animations (cubic-bezier easing)

  5. ✅ Təhlükəsizlik Dashbordu - Təhlükə Analizi

  Brute force detection funksiyası: apps/audit/template_views.py (sətir 12-64)
  def detect_brute_force_attacks(login_failures, time_window=5, threshold=5):
      # 5 dəqiqə ərzində 5+ səhv giriş
      # IP-yə görə qruplama və analiz

  Dashboard-a əlavələr (sətir 129-163):
  - 24 saat ərzində təhlükə axtarışı
  - Severity level (critical/high)
  - Threat table göstərimi (IP, targeted users, time span)

  Template: templates/audit/security_dashboard.html (sətir 216-285)
  - Qırmızı border ilə critical alert
  - Badge ilə threat count
  - Detailed threat table

  6. ✅ Test Coverage

  4 Yeni test modulu yaradıldı:
  1. apps/leave_attendance/tests/test_leave_approval_workflow.py - 11 test
  2. apps/compensation/tests/test_salary_management.py - 12 test
  3. apps/recruitment/tests/test_candidate_pipeline.py - 17 test
  4. apps/evaluations/tests/test_calibration_workflow.py - 20 test

  BaseTestCase pattern - Organization FK problemi həll edildi
  - apps/recruitment/tests/test_base.py
  - apps/compensation/tests/test_base.py

  Ümumi test sayı: 60+ yeni test

  7. ✅ i18n Translation Coverage

  Yoxlanılan template-lər (hamısında {% trans %} mövcuddur):
  - ✅ templates/recruitment/candidate_pipeline.html
  - ✅ templates/evaluations/calibration/dashboard.html
  - ✅ templates/evaluations/calibration/detail.html
  - ✅ templates/notifications/bulk_notification.html
  - ✅ templates/audit/security_dashboard.html

  8. ✅ Əlavə Tamamlanmış İşlər

  360° Kalibrə sistemi:
  - apps/evaluations/views_calibration.py - 5 view (dashboard, detail, adjust, finalize, bulk)
  - 2 tam HTML template (dashboard və detail)
  - Score distribution, statistika, permissions

  Digər modullar:
  - Leave approval workflow (avtomatik balance update)
  - Compensation history tracking
  - Bulk notification system
  - Security dashboard (already complete)

  ---
  📊 Fayl Statistikaları

  - Yeni modellər: DepartmentBudget
  - Yeni migration-lar: 1 (compensation)
  - Yoxlanmış/dəyişdirilmiş fayllar: 15+
  - Yeni test suite-lər: 4
  - Template-lər: Hamısı i18n-ready

  🎉 Nəticə

  Bütün 9 məsələ tam həll edildi:
  1. ✅ Modul İnteqrasiyası
  2. ✅ Export (PDF/Excel/CSV)
  3. ✅ Kompensasiya büdcə məntiq
  4. ✅ Kanban drag-drop
  5. ✅ Təhlükəsizlik threat detection
  6. ✅ Test coverage
  7. ✅ i18n translation','01','1',5,'monthly',5,10,15,1,'2025-10-16 12:42:30.548364','2025-10-16 12:42:30.548384',1,'2025-10-16 12:42:30.550760',NULL,'+',2,1,1,1);
INSERT INTO "development_plans_historicalkpi" VALUES(1,'AzAgroPOS','İstifadəçinin tələb etdiyi 9 məsələ tam həll edildi:

  1. ✅ Modul İnteqrasiyası

  - templates/base/sidebar.html - Bütün yeni modullar və təhlükəsizlik dashboardu əlavə edildi (sətir 432-441)
  - apps/accounts/template_views.py - Dashboard tam HRIS modul datası ilə təchiz edildi (sətir 59-205)
  - Bütün yeni modullar navbar və sidebar-da mövcuddur

  2. ✅ Report Export Funksionallığı

  - PDF export: apps/reports/template_views.py - ReportLab ilə PDF yaradılması (sətir 58-110)
  - Excel export: OpenPyXL ilə XLSX formatı (sətir 112-152)
  - CSV export: apps/reports/utils.py - UTF-8-sig BOM ilə Excel uyğunluğu (sətir 95-117)
  - Multi-format endpoint: /reports/export/<format>/

  3. ✅ Kompensasiya Büdcə Məntiq

  Yeni model əlavə edildi: apps/compensation/models.py (sətir 510-601)
  - DepartmentBudget modeli illik büdcə, istifadə edilmiş məbləğ və qalıq hesablamaları
  - can_afford() metodu ilə büdcə yoxlaması
  - utilization_percentage property

  View-də büdcə validasiyası: apps/compensation/views.py (sətir 118-149)
  if dept_budget:
      if not dept_budget.can_afford(salary_difference):
          return JsonResponse({
              ''success'': False,
              ''message'': f''Büdcə kifayət etmir!...'',
              ''budget_exceeded'': True
          })

  Admin panel: Rəngli utilization percentage və remaining budget göstəricisi

  4. ✅ Kanban Drag-and-Drop

  Sortable.js tam inteqrasiya: templates/recruitment/candidate_pipeline.html (sətir 366-541)

  Əlavə edilən xüsusiyyətlər:
  - ✅ CSRF token düzgün implementasiyası (getCookie funksiyası)
  - ✅ Toast notification sistemi (slideIn/slideOut animation)
  - ✅ Loading state (.updating class)
  - ✅ Auto-revert on error
  - ✅ Real-time stage count update
  - ✅ Visual feedback (ghost class, chosen class)
  - ✅ Smooth animations (cubic-bezier easing)

  5. ✅ Təhlükəsizlik Dashbordu - Təhlükə Analizi

  Brute force detection funksiyası: apps/audit/template_views.py (sətir 12-64)
  def detect_brute_force_attacks(login_failures, time_window=5, threshold=5):
      # 5 dəqiqə ərzində 5+ səhv giriş
      # IP-yə görə qruplama və analiz

  Dashboard-a əlavələr (sətir 129-163):
  - 24 saat ərzində təhlükə axtarışı
  - Severity level (critical/high)
  - Threat table göstərimi (IP, targeted users, time span)

  Template: templates/audit/security_dashboard.html (sətir 216-285)
  - Qırmızı border ilə critical alert
  - Badge ilə threat count
  - Detailed threat table

  6. ✅ Test Coverage

  4 Yeni test modulu yaradıldı:
  1. apps/leave_attendance/tests/test_leave_approval_workflow.py - 11 test
  2. apps/compensation/tests/test_salary_management.py - 12 test
  3. apps/recruitment/tests/test_candidate_pipeline.py - 17 test
  4. apps/evaluations/tests/test_calibration_workflow.py - 20 test

  BaseTestCase pattern - Organization FK problemi həll edildi
  - apps/recruitment/tests/test_base.py
  - apps/compensation/tests/test_base.py

  Ümumi test sayı: 60+ yeni test

  7. ✅ i18n Translation Coverage

  Yoxlanılan template-lər (hamısında {% trans %} mövcuddur):
  - ✅ templates/recruitment/candidate_pipeline.html
  - ✅ templates/evaluations/calibration/dashboard.html
  - ✅ templates/evaluations/calibration/detail.html
  - ✅ templates/notifications/bulk_notification.html
  - ✅ templates/audit/security_dashboard.html

  8. ✅ Əlavə Tamamlanmış İşlər

  360° Kalibrə sistemi:
  - apps/evaluations/views_calibration.py - 5 view (dashboard, detail, adjust, finalize, bulk)
  - 2 tam HTML template (dashboard və detail)
  - Score distribution, statistika, permissions

  Digər modullar:
  - Leave approval workflow (avtomatik balance update)
  - Compensation history tracking
  - Bulk notification system
  - Security dashboard (already complete)

  ---
  📊 Fayl Statistikaları

  - Yeni modellər: DepartmentBudget
  - Yeni migration-lar: 1 (compensation)
  - Yoxlanmış/dəyişdirilmiş fayllar: 15+
  - Yeni test suite-lər: 4
  - Template-lər: Hamısı i18n-ready

  🎉 Nəticə

  Bütün 9 məsələ tam həll edildi:
  1. ✅ Modul İnteqrasiyası
  2. ✅ Export (PDF/Excel/CSV)
  3. ✅ Kompensasiya büdcə məntiq
  4. ✅ Kanban drag-drop
  5. ✅ Təhlükəsizlik threat detection
  6. ✅ Test coverage
  7. ✅ i18n translation','01','1',5,'monthly',5,10,15,1,'2025-10-16 12:42:30.548364','2025-10-16 21:58:25.455594',2,'2025-10-16 21:58:25.459710',NULL,'~',2,1,1,1);
CREATE TABLE "development_plans_historicalkpimeasurement" ("id" bigint NOT NULL, "measurement_date" date NOT NULL, "actual_value" decimal NOT NULL, "trend" varchar(10) NULL, "notes" text NOT NULL, "created_at" datetime NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "history_user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "kpi_id" bigint NULL, "measured_by_id" bigint NULL);
INSERT INTO "development_plans_historicalkpimeasurement" VALUES(1,'2025-10-17',45,'down','454','2025-10-16 21:56:40.443606',1,'2025-10-16 21:56:40.446815',NULL,'+',1,1,1);
CREATE TABLE "development_plans_historicalmilestone" ("id" bigint NOT NULL, "title" varchar(200) NOT NULL, "description" text NOT NULL, "due_date" date NOT NULL, "is_completed" bool NOT NULL, "completed_at" datetime NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "created_by_id" bigint NULL, "history_user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "objective_id" bigint NULL);
CREATE TABLE "development_plans_historicalobjectiveupdate" ("id" bigint NOT NULL, "content" text NOT NULL, "progress_value" decimal NULL, "created_at" datetime NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "created_by_id" bigint NULL, "history_user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "objective_id" bigint NULL);
CREATE TABLE "development_plans_historicalstrategicobjective" ("id" bigint NOT NULL, "title" varchar(300) NOT NULL, "description" text NOT NULL, "level" varchar(20) NOT NULL, "status" varchar(20) NOT NULL, "fiscal_year" integer NOT NULL, "quarter" varchar(10) NOT NULL, "start_date" date NOT NULL, "end_date" date NOT NULL, "progress_percentage" decimal NOT NULL, "weight" decimal NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "created_by_id" bigint NULL, "department_id" bigint NULL, "history_user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "owner_id" bigint NULL, "parent_objective_id" bigint NULL);
INSERT INTO "development_plans_historicalstrategicobjective" VALUES(1,'aaaaaaaaaaaa','aaaaaaaaaaaaaaaaaİstifadəçinin tələb etdiyi 9 məsələ tam həll edildi:

  1. ✅ Modul İnteqrasiyası

  - templates/base/sidebar.html - Bütün yeni modullar və təhlükəsizlik dashboardu əlavə edildi (sətir 432-441)
  - apps/accounts/template_views.py - Dashboard tam HRIS modul datası ilə təchiz edildi (sətir 59-205)
  - Bütün yeni modullar navbar və sidebar-da mövcuddur

  2. ✅ Report Export Funksionallığı

  - PDF export: apps/reports/template_views.py - ReportLab ilə PDF yaradılması (sətir 58-110)
  - Excel export: OpenPyXL ilə XLSX formatı (sətir 112-152)
  - CSV export: apps/reports/utils.py - UTF-8-sig BOM ilə Excel uyğunluğu (sətir 95-117)
  - Multi-format endpoint: /reports/export/<format>/

  3. ✅ Kompensasiya Büdcə Məntiq

  Yeni model əlavə edildi: apps/compensation/models.py (sətir 510-601)
  - DepartmentBudget modeli illik büdcə, istifadə edilmiş məbləğ və qalıq hesablamaları
  - can_afford() metodu ilə büdcə yoxlaması
  - utilization_percentage property

  View-də büdcə validasiyası: apps/compensation/views.py (sətir 118-149)
  if dept_budget:
      if not dept_budget.can_afford(salary_difference):
          return JsonResponse({
              ''success'': False,
              ''message'': f''Büdcə kifayət etmir!...'',
              ''budget_exceeded'': True
          })

  Admin panel: Rəngli utilization percentage və remaining budget göstəricisi

  4. ✅ Kanban Drag-and-Drop

  Sortable.js tam inteqrasiya: templates/recruitment/candidate_pipeline.html (sətir 366-541)

  Əlavə edilən xüsusiyyətlər:
  - ✅ CSRF token düzgün implementasiyası (getCookie funksiyası)
  - ✅ Toast notification sistemi (slideIn/slideOut animation)
  - ✅ Loading state (.updating class)
  - ✅ Auto-revert on error
  - ✅ Real-time stage count update
  - ✅ Visual feedback (ghost class, chosen class)
  - ✅ Smooth animations (cubic-bezier easing)

  5. ✅ Təhlükəsizlik Dashbordu - Təhlükə Analizi

  Brute force detection funksiyası: apps/audit/template_views.py (sətir 12-64)
  def detect_brute_force_attacks(login_failures, time_window=5, threshold=5):
      # 5 dəqiqə ərzində 5+ səhv giriş
      # IP-yə görə qruplama və analiz

  Dashboard-a əlavələr (sətir 129-163):
  - 24 saat ərzində təhlükə axtarışı
  - Severity level (critical/high)
  - Threat table göstərimi (IP, targeted users, time span)

  Template: templates/audit/security_dashboard.html (sətir 216-285)
  - Qırmızı border ilə critical alert
  - Badge ilə threat count
  - Detailed threat table

  6. ✅ Test Coverage

  4 Yeni test modulu yaradıldı:
  1. apps/leave_attendance/tests/test_leave_approval_workflow.py - 11 test
  2. apps/compensation/tests/test_salary_management.py - 12 test
  3. apps/recruitment/tests/test_candidate_pipeline.py - 17 test
  4. apps/evaluations/tests/test_calibration_workflow.py - 20 test

  BaseTestCase pattern - Organization FK problemi həll edildi
  - apps/recruitment/tests/test_base.py
  - apps/compensation/tests/test_base.py

  Ümumi test sayı: 60+ yeni test

  7. ✅ i18n Translation Coverage

  Yoxlanılan template-lər (hamısında {% trans %} mövcuddur):
  - ✅ templates/recruitment/candidate_pipeline.html
  - ✅ templates/evaluations/calibration/dashboard.html
  - ✅ templates/evaluations/calibration/detail.html
  - ✅ templates/notifications/bulk_notification.html
  - ✅ templates/audit/security_dashboard.html

  8. ✅ Əlavə Tamamlanmış İşlər

  360° Kalibrə sistemi:
  - apps/evaluations/views_calibration.py - 5 view (dashboard, detail, adjust, finalize, bulk)
  - 2 tam HTML template (dashboard və detail)
  - Score distribution, statistika, permissions

  Digər modullar:
  - Leave approval workflow (avtomatik balance update)
  - Compensation history tracking
  - Bulk notification system
  - Security dashboard (already complete)

  ---
  📊 Fayl Statistikaları

  - Yeni modellər: DepartmentBudget
  - Yeni migration-lar: 1 (compensation)
  - Yoxlanmış/dəyişdirilmiş fayllar: 15+
  - Yeni test suite-lər: 4
  - Template-lər: Hamısı i18n-ready

  🎉 Nəticə

  Bütün 9 məsələ tam həll edildi:
  1. ✅ Modul İnteqrasiyası
  2. ✅ Export (PDF/Excel/CSV)
  3. ✅ Kompensasiya büdcə məntiq
  4. ✅ Kanban drag-drop
  5. ✅ Təhlükəsizlik threat detection
  6. ✅ Test coverage
  7. ✅ i18n translation','organization','active',2025,'annual','2025-10-16','2025-10-31',0,100,'2025-10-16 12:41:33.115606','2025-10-16 12:41:33.115624',1,'2025-10-16 12:41:33.118912',NULL,'+',2,2,1,1,NULL);
INSERT INTO "development_plans_historicalstrategicobjective" VALUES(1,'test','aaaaaaaaaaaaaaaaaİstifadəçinin tələb etdiyi 9 məsələ tam həll edildi:

  1. ✅ Modul İnteqrasiyası

  - templates/base/sidebar.html - Bütün yeni modullar və təhlükəsizlik dashboardu əlavə edildi (sətir 432-441)
  - apps/accounts/template_views.py - Dashboard tam HRIS modul datası ilə təchiz edildi (sətir 59-205)
  - Bütün yeni modullar navbar və sidebar-da mövcuddur

  2. ✅ Report Export Funksionallığı

  - PDF export: apps/reports/template_views.py - ReportLab ilə PDF yaradılması (sətir 58-110)
  - Excel export: OpenPyXL ilə XLSX formatı (sətir 112-152)
  - CSV export: apps/reports/utils.py - UTF-8-sig BOM ilə Excel uyğunluğu (sətir 95-117)
  - Multi-format endpoint: /reports/export/<format>/

  3. ✅ Kompensasiya Büdcə Məntiq

  Yeni model əlavə edildi: apps/compensation/models.py (sətir 510-601)
  - DepartmentBudget modeli illik büdcə, istifadə edilmiş məbləğ və qalıq hesablamaları
  - can_afford() metodu ilə büdcə yoxlaması
  - utilization_percentage property

  View-də büdcə validasiyası: apps/compensation/views.py (sətir 118-149)
  if dept_budget:
      if not dept_budget.can_afford(salary_difference):
          return JsonResponse({
              ''success'': False,
              ''message'': f''Büdcə kifayət etmir!...'',
              ''budget_exceeded'': True
          })

  Admin panel: Rəngli utilization percentage və remaining budget göstəricisi

  4. ✅ Kanban Drag-and-Drop

  Sortable.js tam inteqrasiya: templates/recruitment/candidate_pipeline.html (sətir 366-541)

  Əlavə edilən xüsusiyyətlər:
  - ✅ CSRF token düzgün implementasiyası (getCookie funksiyası)
  - ✅ Toast notification sistemi (slideIn/slideOut animation)
  - ✅ Loading state (.updating class)
  - ✅ Auto-revert on error
  - ✅ Real-time stage count update
  - ✅ Visual feedback (ghost class, chosen class)
  - ✅ Smooth animations (cubic-bezier easing)

  5. ✅ Təhlükəsizlik Dashbordu - Təhlükə Analizi

  Brute force detection funksiyası: apps/audit/template_views.py (sətir 12-64)
  def detect_brute_force_attacks(login_failures, time_window=5, threshold=5):
      # 5 dəqiqə ərzində 5+ səhv giriş
      # IP-yə görə qruplama və analiz

  Dashboard-a əlavələr (sətir 129-163):
  - 24 saat ərzində təhlükə axtarışı
  - Severity level (critical/high)
  - Threat table göstərimi (IP, targeted users, time span)

  Template: templates/audit/security_dashboard.html (sətir 216-285)
  - Qırmızı border ilə critical alert
  - Badge ilə threat count
  - Detailed threat table

  6. ✅ Test Coverage

  4 Yeni test modulu yaradıldı:
  1. apps/leave_attendance/tests/test_leave_approval_workflow.py - 11 test
  2. apps/compensation/tests/test_salary_management.py - 12 test
  3. apps/recruitment/tests/test_candidate_pipeline.py - 17 test
  4. apps/evaluations/tests/test_calibration_workflow.py - 20 test

  BaseTestCase pattern - Organization FK problemi həll edildi
  - apps/recruitment/tests/test_base.py
  - apps/compensation/tests/test_base.py

  Ümumi test sayı: 60+ yeni test

  7. ✅ i18n Translation Coverage

  Yoxlanılan template-lər (hamısında {% trans %} mövcuddur):
  - ✅ templates/recruitment/candidate_pipeline.html
  - ✅ templates/evaluations/calibration/dashboard.html
  - ✅ templates/evaluations/calibration/detail.html
  - ✅ templates/notifications/bulk_notification.html
  - ✅ templates/audit/security_dashboard.html

  8. ✅ Əlavə Tamamlanmış İşlər

  360° Kalibrə sistemi:
  - apps/evaluations/views_calibration.py - 5 view (dashboard, detail, adjust, finalize, bulk)
  - 2 tam HTML template (dashboard və detail)
  - Score distribution, statistika, permissions

  Digər modullar:
  - Leave approval workflow (avtomatik balance update)
  - Compensation history tracking
  - Bulk notification system
  - Security dashboard (already complete)

  ---
  📊 Fayl Statistikaları

  - Yeni modellər: DepartmentBudget
  - Yeni migration-lar: 1 (compensation)
  - Yoxlanmış/dəyişdirilmiş fayllar: 15+
  - Yeni test suite-lər: 4
  - Template-lər: Hamısı i18n-ready

  🎉 Nəticə

  Bütün 9 məsələ tam həll edildi:
  1. ✅ Modul İnteqrasiyası
  2. ✅ Export (PDF/Excel/CSV)
  3. ✅ Kompensasiya büdcə məntiq
  4. ✅ Kanban drag-drop
  5. ✅ Təhlükəsizlik threat detection
  6. ✅ Test coverage
  7. ✅ i18n translation','organization','active',2025,'annual','2025-10-16','2025-10-31',0,100,'2025-10-16 12:41:33.115606','2025-10-16 21:58:54.467223',2,'2025-10-16 21:58:54.473074',NULL,'~',2,2,1,1,NULL);
INSERT INTO "development_plans_historicalstrategicobjective" VALUES(1,'test','aaaaaaaaaaaaaaaaaİstifadəçinin tələb etdiyi 9 məsələ tam həll edildi:

  1. ✅ Modul İnteqrasiyası

  - templates/base/sidebar.html - Bütün yeni modullar və təhlükəsizlik dashboardu əlavə edildi (sətir 432-441)
  - apps/accounts/template_views.py - Dashboard tam HRIS modul datası ilə təchiz edildi (sətir 59-205)
  - Bütün yeni modullar navbar və sidebar-da mövcuddur

  2. ✅ Report Export Funksionallığı

  - PDF export: apps/reports/template_views.py - ReportLab ilə PDF yaradılması (sətir 58-110)
  - Excel export: OpenPyXL ilə XLSX formatı (sətir 112-152)
  - CSV export: apps/reports/utils.py - UTF-8-sig BOM ilə Excel uyğunluğu (sətir 95-117)
  - Multi-format endpoint: /reports/export/<format>/

  3. ✅ Kompensasiya Büdcə Məntiq

  Yeni model əlavə edildi: apps/compensation/models.py (sətir 510-601)
  - DepartmentBudget modeli illik büdcə, istifadə edilmiş məbləğ və qalıq hesablamaları
  - can_afford() metodu ilə büdcə yoxlaması
  - utilization_percentage property

  View-də büdcə validasiyası: apps/compensation/views.py (sətir 118-149)
  if dept_budget:
      if not dept_budget.can_afford(salary_difference):
          return JsonResponse({
              ''success'': False,
              ''message'': f''Büdcə kifayət etmir!...'',
              ''budget_exceeded'': True
          })

  Admin panel: Rəngli utilization percentage və remaining budget göstəricisi

  4. ✅ Kanban Drag-and-Drop

  Sortable.js tam inteqrasiya: templates/recruitment/candidate_pipeline.html (sətir 366-541)

  Əlavə edilən xüsusiyyətlər:
  - ✅ CSRF token düzgün implementasiyası (getCookie funksiyası)
  - ✅ Toast notification sistemi (slideIn/slideOut animation)
  - ✅ Loading state (.updating class)
  - ✅ Auto-revert on error
  - ✅ Real-time stage count update
  - ✅ Visual feedback (ghost class, chosen class)
  - ✅ Smooth animations (cubic-bezier easing)

  5. ✅ Təhlükəsizlik Dashbordu - Təhlükə Analizi

  Brute force detection funksiyası: apps/audit/template_views.py (sətir 12-64)
  def detect_brute_force_attacks(login_failures, time_window=5, threshold=5):
      # 5 dəqiqə ərzində 5+ səhv giriş
      # IP-yə görə qruplama və analiz

  Dashboard-a əlavələr (sətir 129-163):
  - 24 saat ərzində təhlükə axtarışı
  - Severity level (critical/high)
  - Threat table göstərimi (IP, targeted users, time span)

  Template: templates/audit/security_dashboard.html (sətir 216-285)
  - Qırmızı border ilə critical alert
  - Badge ilə threat count
  - Detailed threat table

  6. ✅ Test Coverage

  4 Yeni test modulu yaradıldı:
  1. apps/leave_attendance/tests/test_leave_approval_workflow.py - 11 test
  2. apps/compensation/tests/test_salary_management.py - 12 test
  3. apps/recruitment/tests/test_candidate_pipeline.py - 17 test
  4. apps/evaluations/tests/test_calibration_workflow.py - 20 test

  BaseTestCase pattern - Organization FK problemi həll edildi
  - apps/recruitment/tests/test_base.py
  - apps/compensation/tests/test_base.py

  Ümumi test sayı: 60+ yeni test

  7. ✅ i18n Translation Coverage

  Yoxlanılan template-lər (hamısında {% trans %} mövcuddur):
  - ✅ templates/recruitment/candidate_pipeline.html
  - ✅ templates/evaluations/calibration/dashboard.html
  - ✅ templates/evaluations/calibration/detail.html
  - ✅ templates/notifications/bulk_notification.html
  - ✅ templates/audit/security_dashboard.html

  8. ✅ Əlavə Tamamlanmış İşlər

  360° Kalibrə sistemi:
  - apps/evaluations/views_calibration.py - 5 view (dashboard, detail, adjust, finalize, bulk)
  - 2 tam HTML template (dashboard və detail)
  - Score distribution, statistika, permissions

  Digər modullar:
  - Leave approval workflow (avtomatik balance update)
  - Compensation history tracking
  - Bulk notification system
  - Security dashboard (already complete)

  ---
  📊 Fayl Statistikaları

  - Yeni modellər: DepartmentBudget
  - Yeni migration-lar: 1 (compensation)
  - Yoxlanmış/dəyişdirilmiş fayllar: 15+
  - Yeni test suite-lər: 4
  - Template-lər: Hamısı i18n-ready

  🎉 Nəticə

  Bütün 9 məsələ tam həll edildi:
  1. ✅ Modul İnteqrasiyası
  2. ✅ Export (PDF/Excel/CSV)
  3. ✅ Kompensasiya büdcə məntiq
  4. ✅ Kanban drag-drop
  5. ✅ Təhlükəsizlik threat detection
  6. ✅ Test coverage
  7. ✅ i18n translation','organization','active',2025,'annual','2025-10-16','2025-10-31',0,100,'2025-10-16 12:41:33.115606','2025-10-16 21:59:36.194280',3,'2025-10-16 21:59:36.197661',NULL,'~',2,2,1,1,NULL);
INSERT INTO "development_plans_historicalstrategicobjective" VALUES(1,'test','aaaaaaaaaaaaaaaaaİstifadəçinin tələb etdiyi 9 məsələ tam həll edildi:

  1. ✅ Modul İnteqrasiyası

  - templates/base/sidebar.html - Bütün yeni modullar və təhlükəsizlik dashboardu əlavə edildi (sətir 432-441)
  - apps/accounts/template_views.py - Dashboard tam HRIS modul datası ilə təchiz edildi (sətir 59-205)
  - Bütün yeni modullar navbar və sidebar-da mövcuddur

  2. ✅ Report Export Funksionallığı

  - PDF export: apps/reports/template_views.py - ReportLab ilə PDF yaradılması (sətir 58-110)
  - Excel export: OpenPyXL ilə XLSX formatı (sətir 112-152)
  - CSV export: apps/reports/utils.py - UTF-8-sig BOM ilə Excel uyğunluğu (sətir 95-117)
  - Multi-format endpoint: /reports/export/<format>/

  3. ✅ Kompensasiya Büdcə Məntiq

  Yeni model əlavə edildi: apps/compensation/models.py (sətir 510-601)
  - DepartmentBudget modeli illik büdcə, istifadə edilmiş məbləğ və qalıq hesablamaları
  - can_afford() metodu ilə büdcə yoxlaması
  - utilization_percentage property

  View-də büdcə validasiyası: apps/compensation/views.py (sətir 118-149)
  if dept_budget:
      if not dept_budget.can_afford(salary_difference):
          return JsonResponse({
              ''success'': False,
              ''message'': f''Büdcə kifayət etmir!...'',
              ''budget_exceeded'': True
          })

  Admin panel: Rəngli utilization percentage və remaining budget göstəricisi

  4. ✅ Kanban Drag-and-Drop

  Sortable.js tam inteqrasiya: templates/recruitment/candidate_pipeline.html (sətir 366-541)

  Əlavə edilən xüsusiyyətlər:
  - ✅ CSRF token düzgün implementasiyası (getCookie funksiyası)
  - ✅ Toast notification sistemi (slideIn/slideOut animation)
  - ✅ Loading state (.updating class)
  - ✅ Auto-revert on error
  - ✅ Real-time stage count update
  - ✅ Visual feedback (ghost class, chosen class)
  - ✅ Smooth animations (cubic-bezier easing)

  5. ✅ Təhlükəsizlik Dashbordu - Təhlükə Analizi

  Brute force detection funksiyası: apps/audit/template_views.py (sətir 12-64)
  def detect_brute_force_attacks(login_failures, time_window=5, threshold=5):
      # 5 dəqiqə ərzində 5+ səhv giriş
      # IP-yə görə qruplama və analiz

  Dashboard-a əlavələr (sətir 129-163):
  - 24 saat ərzində təhlükə axtarışı
  - Severity level (critical/high)
  - Threat table göstərimi (IP, targeted users, time span)

  Template: templates/audit/security_dashboard.html (sətir 216-285)
  - Qırmızı border ilə critical alert
  - Badge ilə threat count
  - Detailed threat table

  6. ✅ Test Coverage

  4 Yeni test modulu yaradıldı:
  1. apps/leave_attendance/tests/test_leave_approval_workflow.py - 11 test
  2. apps/compensation/tests/test_salary_management.py - 12 test
  3. apps/recruitment/tests/test_candidate_pipeline.py - 17 test
  4. apps/evaluations/tests/test_calibration_workflow.py - 20 test

  BaseTestCase pattern - Organization FK problemi həll edildi
  - apps/recruitment/tests/test_base.py
  - apps/compensation/tests/test_base.py

  Ümumi test sayı: 60+ yeni test

  7. ✅ i18n Translation Coverage

  Yoxlanılan template-lər (hamısında {% trans %} mövcuddur):
  - ✅ templates/recruitment/candidate_pipeline.html
  - ✅ templates/evaluations/calibration/dashboard.html
  - ✅ templates/evaluations/calibration/detail.html
  - ✅ templates/notifications/bulk_notification.html
  - ✅ templates/audit/security_dashboard.html

  8. ✅ Əlavə Tamamlanmış İşlər

  360° Kalibrə sistemi:
  - apps/evaluations/views_calibration.py - 5 view (dashboard, detail, adjust, finalize, bulk)
  - 2 tam HTML template (dashboard və detail)
  - Score distribution, statistika, permissions

  Digər modullar:
  - Leave approval workflow (avtomatik balance update)
  - Compensation history tracking
  - Bulk notification system
  - Security dashboard (already complete)

  ---
  📊 Fayl Statistikaları

  - Yeni modellər: DepartmentBudget
  - Yeni migration-lar: 1 (compensation)
  - Yoxlanmış/dəyişdirilmiş fayllar: 15+
  - Yeni test suite-lər: 4
  - Template-lər: Hamısı i18n-ready

  🎉 Nəticə

  Bütün 9 məsələ tam həll edildi:
  1. ✅ Modul İnteqrasiyası
  2. ✅ Export (PDF/Excel/CSV)
  3. ✅ Kompensasiya büdcə məntiq
  4. ✅ Kanban drag-drop
  5. ✅ Təhlükəsizlik threat detection
  6. ✅ Test coverage
  7. ✅ i18n translation','organization','active',2025,'annual','2025-10-16','2025-10-31',60,100,'2025-10-16 12:41:33.115606','2025-10-16 21:59:36.206222',4,'2025-10-16 21:59:36.206951',NULL,'~',2,2,1,1,NULL);
INSERT INTO "development_plans_historicalstrategicobjective" VALUES(1,'admin test','stifadəçinin tələb etdiyi 9 məsələ tam həll edildi:

  1. ✅ Modul İnteqrasiyası

  - templates/base/sidebar.html - Bütün yeni modullar və təhlükəsizlik dashboardu əlavə edildi (sətir 432-441)
  - apps/accounts/template_views.py - Dashboard tam HRIS modul datası ilə təchiz edildi (sətir 59-205)
  - Bütün yeni modullar navbar və sidebar-da mövcuddur

  2. ✅ Report Export Funksionallığı

  - PDF export: apps/reports/template_views.py - ReportLab ilə PDF yaradılması (sətir 58-110)
  - Excel export: OpenPyXL ilə XLSX formatı (sətir 112-152)
  - CSV export: apps/reports/utils.py - UTF-8-sig BOM ilə Excel uyğunluğu (sətir 95-117)
  - Multi-format endpoint: /reports/export/<format>/

  3. ✅ Kompensasiya Büdcə Məntiq

  Yeni model əlavə edildi: apps/compensation/models.py (sətir 510-601)
  - DepartmentBudget modeli illik büdcə, istifadə edilmiş məbləğ və qalıq hesablamaları
  - can_afford() metodu ilə büdcə yoxlaması
  - utilization_percentage property

  View-də büdcə validasiyası: apps/compensation/views.py (sətir 118-149)
  if dept_budget:
      if not dept_budget.can_afford(salary_difference):
          return JsonResponse({
              ''success'': False,
              ''message'': f''Büdcə kifayət etmir!...'',
              ''budget_exceeded'': True
          })

  Admin panel: Rəngli utilization percentage və remaining budget göstəricisi

  4. ✅ Kanban Drag-and-Drop

  Sortable.js tam inteqrasiya: templates/recruitment/candidate_pipeline.html (sətir 366-541)

  Əlavə edilən xüsusiyyətlər:
  - ✅ CSRF token düzgün implementasiyası (getCookie funksiyası)
  - ✅ Toast notification sistemi (slideIn/slideOut animation)
  - ✅ Loading state (.updating class)
  - ✅ Auto-revert on error
  - ✅ Real-time stage count update
  - ✅ Visual feedback (ghost class, chosen class)
  - ✅ Smooth animations (cubic-bezier easing)

  5. ✅ Təhlükəsizlik Dashbordu - Təhlükə Analizi

  Brute force detection funksiyası: apps/audit/template_views.py (sətir 12-64)
  def detect_brute_force_attacks(login_failures, time_window=5, threshold=5):
      # 5 dəqiqə ərzində 5+ səhv giriş
      # IP-yə görə qruplama və analiz

  Dashboard-a əlavələr (sətir 129-163):
  - 24 saat ərzində təhlükə axtarışı
  - Severity level (critical/high)
  - Threat table göstərimi (IP, targeted users, time span)

  Template: templates/audit/security_dashboard.html (sətir 216-285)
  - Qırmızı border ilə critical alert
  - Badge ilə threat count
  - Detailed threat table

  6. ✅ Test Coverage

  4 Yeni test modulu yaradıldı:
  1. apps/leave_attendance/tests/test_leave_approval_workflow.py - 11 test
  2. apps/compensation/tests/test_salary_management.py - 12 test
  3. apps/recruitment/tests/test_candidate_pipeline.py - 17 test
  4. apps/evaluations/tests/test_calibration_workflow.py - 20 test

  BaseTestCase pattern - Organization FK problemi həll edildi
  - apps/recruitment/tests/test_base.py
  - apps/compensation/tests/test_base.py

  Ümumi test sayı: 60+ yeni test

  7. ✅ i18n Translation Coverage

  Yoxlanılan template-lər (hamısında {% trans %} mövcuddur):
  - ✅ templates/recruitment/candidate_pipeline.html
  - ✅ templates/evaluations/calibration/dashboard.html
  - ✅ templates/evaluations/calibration/detail.html
  - ✅ templates/notifications/bulk_notification.html
  - ✅ templates/audit/security_dashboard.html

  8. ✅ Əlavə Tamamlanmış İşlər

  360° Kalibrə sistemi:
  - apps/evaluations/views_calibration.py - 5 view (dashboard, detail, adjust, finalize, bulk)
  - 2 tam HTML template (dashboard və detail)
  - Score distribution, statistika, permissions

  Digər modullar:
  - Leave approval workflow (avtomatik balance update)
  - Compensation history tracking
  - Bulk notification system
  - Security dashboard (already complete)

  ---
  📊 Fayl Statistikaları

  - Yeni modellər: DepartmentBudget
  - Yeni migration-lar: 1 (compensation)
  - Yoxlanmış/dəyişdirilmiş fayllar: 15+
  - Yeni test suite-lər: 4
  - Template-lər: Hamısı i18n-ready

  🎉 Nəticə

  Bütün 9 məsələ tam həll edildi:
  1. ✅ Modul İnteqrasiyası
  2. ✅ Export (PDF/Excel/CSV)
  3. ✅ Kompensasiya büdcə məntiq
  4. ✅ Kanban drag-drop
  5. ✅ Təhlükəsizlik threat detection
  6. ✅ Test coverage
  7. ✅ i18n translation','organization','active',2025,'annual','2025-10-16','2025-10-31',60,100,'2025-10-16 12:41:33.115606','2025-10-16 22:22:12.656796',5,'2025-10-16 22:22:12.667453',NULL,'~',2,2,1,1,NULL);
INSERT INTO "development_plans_historicalstrategicobjective" VALUES(1,'admin test','stifadəçinin tələb etdiyi 9 məsələ tam həll edildi:

  1. ✅ Modul İnteqrasiyası

  - templates/base/sidebar.html - Bütün yeni modullar və təhlükəsizlik dashboardu əlavə edildi (sətir 432-441)
  - apps/accounts/template_views.py - Dashboard tam HRIS modul datası ilə təchiz edildi (sətir 59-205)
  - Bütün yeni modullar navbar və sidebar-da mövcuddur

  2. ✅ Report Export Funksionallığı

  - PDF export: apps/reports/template_views.py - ReportLab ilə PDF yaradılması (sətir 58-110)
  - Excel export: OpenPyXL ilə XLSX formatı (sətir 112-152)
  - CSV export: apps/reports/utils.py - UTF-8-sig BOM ilə Excel uyğunluğu (sətir 95-117)
  - Multi-format endpoint: /reports/export/<format>/

  3. ✅ Kompensasiya Büdcə Məntiq

  Yeni model əlavə edildi: apps/compensation/models.py (sətir 510-601)
  - DepartmentBudget modeli illik büdcə, istifadə edilmiş məbləğ və qalıq hesablamaları
  - can_afford() metodu ilə büdcə yoxlaması
  - utilization_percentage property

  View-də büdcə validasiyası: apps/compensation/views.py (sətir 118-149)
  if dept_budget:
      if not dept_budget.can_afford(salary_difference):
          return JsonResponse({
              ''success'': False,
              ''message'': f''Büdcə kifayət etmir!...'',
              ''budget_exceeded'': True
          })

  Admin panel: Rəngli utilization percentage və remaining budget göstəricisi

  4. ✅ Kanban Drag-and-Drop

  Sortable.js tam inteqrasiya: templates/recruitment/candidate_pipeline.html (sətir 366-541)

  Əlavə edilən xüsusiyyətlər:
  - ✅ CSRF token düzgün implementasiyası (getCookie funksiyası)
  - ✅ Toast notification sistemi (slideIn/slideOut animation)
  - ✅ Loading state (.updating class)
  - ✅ Auto-revert on error
  - ✅ Real-time stage count update
  - ✅ Visual feedback (ghost class, chosen class)
  - ✅ Smooth animations (cubic-bezier easing)

  5. ✅ Təhlükəsizlik Dashbordu - Təhlükə Analizi

  Brute force detection funksiyası: apps/audit/template_views.py (sətir 12-64)
  def detect_brute_force_attacks(login_failures, time_window=5, threshold=5):
      # 5 dəqiqə ərzində 5+ səhv giriş
      # IP-yə görə qruplama və analiz

  Dashboard-a əlavələr (sətir 129-163):
  - 24 saat ərzində təhlükə axtarışı
  - Severity level (critical/high)
  - Threat table göstərimi (IP, targeted users, time span)

  Template: templates/audit/security_dashboard.html (sətir 216-285)
  - Qırmızı border ilə critical alert
  - Badge ilə threat count
  - Detailed threat table

  6. ✅ Test Coverage

  4 Yeni test modulu yaradıldı:
  1. apps/leave_attendance/tests/test_leave_approval_workflow.py - 11 test
  2. apps/compensation/tests/test_salary_management.py - 12 test
  3. apps/recruitment/tests/test_candidate_pipeline.py - 17 test
  4. apps/evaluations/tests/test_calibration_workflow.py - 20 test

  BaseTestCase pattern - Organization FK problemi həll edildi
  - apps/recruitment/tests/test_base.py
  - apps/compensation/tests/test_base.py

  Ümumi test sayı: 60+ yeni test

  7. ✅ i18n Translation Coverage

  Yoxlanılan template-lər (hamısında {% trans %} mövcuddur):
  - ✅ templates/recruitment/candidate_pipeline.html
  - ✅ templates/evaluations/calibration/dashboard.html
  - ✅ templates/evaluations/calibration/detail.html
  - ✅ templates/notifications/bulk_notification.html
  - ✅ templates/audit/security_dashboard.html

  8. ✅ Əlavə Tamamlanmış İşlər

  360° Kalibrə sistemi:
  - apps/evaluations/views_calibration.py - 5 view (dashboard, detail, adjust, finalize, bulk)
  - 2 tam HTML template (dashboard və detail)
  - Score distribution, statistika, permissions

  Digər modullar:
  - Leave approval workflow (avtomatik balance update)
  - Compensation history tracking
  - Bulk notification system
  - Security dashboard (already complete)

  ---
  📊 Fayl Statistikaları

  - Yeni modellər: DepartmentBudget
  - Yeni migration-lar: 1 (compensation)
  - Yoxlanmış/dəyişdirilmiş fayllar: 15+
  - Yeni test suite-lər: 4
  - Template-lər: Hamısı i18n-ready

  🎉 Nəticə

  Bütün 9 məsələ tam həll edildi:
  1. ✅ Modul İnteqrasiyası
  2. ✅ Export (PDF/Excel/CSV)
  3. ✅ Kompensasiya büdcə məntiq
  4. ✅ Kanban drag-drop
  5. ✅ Təhlükəsizlik threat detection
  6. ✅ Test coverage
  7. ✅ i18n translation','organization','active',2025,'annual','2025-10-16','2025-10-31',100,100,'2025-10-16 12:41:33.115606','2025-10-16 22:22:30.834145',6,'2025-10-16 22:22:30.842775',NULL,'~',2,2,1,1,NULL);
INSERT INTO "development_plans_historicalstrategicobjective" VALUES(1,'admin test','stifadəçinin tələb etdiyi 9 məsələ tam həll edildi:

  1. ✅ Modul İnteqrasiyası

  - templates/base/sidebar.html - Bütün yeni modullar və təhlükəsizlik dashboardu əlavə edildi (sətir 432-441)
  - apps/accounts/template_views.py - Dashboard tam HRIS modul datası ilə təchiz edildi (sətir 59-205)
  - Bütün yeni modullar navbar və sidebar-da mövcuddur

  2. ✅ Report Export Funksionallığı

  - PDF export: apps/reports/template_views.py - ReportLab ilə PDF yaradılması (sətir 58-110)
  - Excel export: OpenPyXL ilə XLSX formatı (sətir 112-152)
  - CSV export: apps/reports/utils.py - UTF-8-sig BOM ilə Excel uyğunluğu (sətir 95-117)
  - Multi-format endpoint: /reports/export/<format>/

  3. ✅ Kompensasiya Büdcə Məntiq

  Yeni model əlavə edildi: apps/compensation/models.py (sətir 510-601)
  - DepartmentBudget modeli illik büdcə, istifadə edilmiş məbləğ və qalıq hesablamaları
  - can_afford() metodu ilə büdcə yoxlaması
  - utilization_percentage property

  View-də büdcə validasiyası: apps/compensation/views.py (sətir 118-149)
  if dept_budget:
      if not dept_budget.can_afford(salary_difference):
          return JsonResponse({
              ''success'': False,
              ''message'': f''Büdcə kifayət etmir!...'',
              ''budget_exceeded'': True
          })

  Admin panel: Rəngli utilization percentage və remaining budget göstəricisi

  4. ✅ Kanban Drag-and-Drop

  Sortable.js tam inteqrasiya: templates/recruitment/candidate_pipeline.html (sətir 366-541)

  Əlavə edilən xüsusiyyətlər:
  - ✅ CSRF token düzgün implementasiyası (getCookie funksiyası)
  - ✅ Toast notification sistemi (slideIn/slideOut animation)
  - ✅ Loading state (.updating class)
  - ✅ Auto-revert on error
  - ✅ Real-time stage count update
  - ✅ Visual feedback (ghost class, chosen class)
  - ✅ Smooth animations (cubic-bezier easing)

  5. ✅ Təhlükəsizlik Dashbordu - Təhlükə Analizi

  Brute force detection funksiyası: apps/audit/template_views.py (sətir 12-64)
  def detect_brute_force_attacks(login_failures, time_window=5, threshold=5):
      # 5 dəqiqə ərzində 5+ səhv giriş
      # IP-yə görə qruplama və analiz

  Dashboard-a əlavələr (sətir 129-163):
  - 24 saat ərzində təhlükə axtarışı
  - Severity level (critical/high)
  - Threat table göstərimi (IP, targeted users, time span)

  Template: templates/audit/security_dashboard.html (sətir 216-285)
  - Qırmızı border ilə critical alert
  - Badge ilə threat count
  - Detailed threat table

  6. ✅ Test Coverage

  4 Yeni test modulu yaradıldı:
  1. apps/leave_attendance/tests/test_leave_approval_workflow.py - 11 test
  2. apps/compensation/tests/test_salary_management.py - 12 test
  3. apps/recruitment/tests/test_candidate_pipeline.py - 17 test
  4. apps/evaluations/tests/test_calibration_workflow.py - 20 test

  BaseTestCase pattern - Organization FK problemi həll edildi
  - apps/recruitment/tests/test_base.py
  - apps/compensation/tests/test_base.py

  Ümumi test sayı: 60+ yeni test

  7. ✅ i18n Translation Coverage

  Yoxlanılan template-lər (hamısında {% trans %} mövcuddur):
  - ✅ templates/recruitment/candidate_pipeline.html
  - ✅ templates/evaluations/calibration/dashboard.html
  - ✅ templates/evaluations/calibration/detail.html
  - ✅ templates/notifications/bulk_notification.html
  - ✅ templates/audit/security_dashboard.html

  8. ✅ Əlavə Tamamlanmış İşlər

  360° Kalibrə sistemi:
  - apps/evaluations/views_calibration.py - 5 view (dashboard, detail, adjust, finalize, bulk)
  - 2 tam HTML template (dashboard və detail)
  - Score distribution, statistika, permissions

  Digər modullar:
  - Leave approval workflow (avtomatik balance update)
  - Compensation history tracking
  - Bulk notification system
  - Security dashboard (already complete)

  ---
  📊 Fayl Statistikaları

  - Yeni modellər: DepartmentBudget
  - Yeni migration-lar: 1 (compensation)
  - Yoxlanmış/dəyişdirilmiş fayllar: 15+
  - Yeni test suite-lər: 4
  - Template-lər: Hamısı i18n-ready

  🎉 Nəticə

  Bütün 9 məsələ tam həll edildi:
  1. ✅ Modul İnteqrasiyası
  2. ✅ Export (PDF/Excel/CSV)
  3. ✅ Kompensasiya büdcə məntiq
  4. ✅ Kanban drag-drop
  5. ✅ Təhlükəsizlik threat detection
  6. ✅ Test coverage
  7. ✅ i18n translation','organization','active',2025,'annual','2025-10-16','2025-10-31',100,100,'2025-10-16 12:41:33.115606','2025-10-16 22:29:02.783792',7,'2025-10-16 22:29:02.793796',NULL,'~',2,2,1,1,NULL);
INSERT INTO "development_plans_historicalstrategicobjective" VALUES(1,'admin test','stifadəçinin tələb etdiyi 9 məsələ tam həll edildi:

  1. ✅ Modul İnteqrasiyası

  - templates/base/sidebar.html - Bütün yeni modullar və təhlükəsizlik dashboardu əlavə edildi (sətir 432-441)
  - apps/accounts/template_views.py - Dashboard tam HRIS modul datası ilə təchiz edildi (sətir 59-205)
  - Bütün yeni modullar navbar və sidebar-da mövcuddur

  2. ✅ Report Export Funksionallığı

  - PDF export: apps/reports/template_views.py - ReportLab ilə PDF yaradılması (sətir 58-110)
  - Excel export: OpenPyXL ilə XLSX formatı (sətir 112-152)
  - CSV export: apps/reports/utils.py - UTF-8-sig BOM ilə Excel uyğunluğu (sətir 95-117)
  - Multi-format endpoint: /reports/export/<format>/

  3. ✅ Kompensasiya Büdcə Məntiq

  Yeni model əlavə edildi: apps/compensation/models.py (sətir 510-601)
  - DepartmentBudget modeli illik büdcə, istifadə edilmiş məbləğ və qalıq hesablamaları
  - can_afford() metodu ilə büdcə yoxlaması
  - utilization_percentage property

  View-də büdcə validasiyası: apps/compensation/views.py (sətir 118-149)
  if dept_budget:
      if not dept_budget.can_afford(salary_difference):
          return JsonResponse({
              ''success'': False,
              ''message'': f''Büdcə kifayət etmir!...'',
              ''budget_exceeded'': True
          })

  Admin panel: Rəngli utilization percentage və remaining budget göstəricisi

  4. ✅ Kanban Drag-and-Drop

  Sortable.js tam inteqrasiya: templates/recruitment/candidate_pipeline.html (sətir 366-541)

  Əlavə edilən xüsusiyyətlər:
  - ✅ CSRF token düzgün implementasiyası (getCookie funksiyası)
  - ✅ Toast notification sistemi (slideIn/slideOut animation)
  - ✅ Loading state (.updating class)
  - ✅ Auto-revert on error
  - ✅ Real-time stage count update
  - ✅ Visual feedback (ghost class, chosen class)
  - ✅ Smooth animations (cubic-bezier easing)

  5. ✅ Təhlükəsizlik Dashbordu - Təhlükə Analizi

  Brute force detection funksiyası: apps/audit/template_views.py (sətir 12-64)
  def detect_brute_force_attacks(login_failures, time_window=5, threshold=5):
      # 5 dəqiqə ərzində 5+ səhv giriş
      # IP-yə görə qruplama və analiz

  Dashboard-a əlavələr (sətir 129-163):
  - 24 saat ərzində təhlükə axtarışı
  - Severity level (critical/high)
  - Threat table göstərimi (IP, targeted users, time span)

  Template: templates/audit/security_dashboard.html (sətir 216-285)
  - Qırmızı border ilə critical alert
  - Badge ilə threat count
  - Detailed threat table

  6. ✅ Test Coverage

  4 Yeni test modulu yaradıldı:
  1. apps/leave_attendance/tests/test_leave_approval_workflow.py - 11 test
  2. apps/compensation/tests/test_salary_management.py - 12 test
  3. apps/recruitment/tests/test_candidate_pipeline.py - 17 test
  4. apps/evaluations/tests/test_calibration_workflow.py - 20 test

  BaseTestCase pattern - Organization FK problemi həll edildi
  - apps/recruitment/tests/test_base.py
  - apps/compensation/tests/test_base.py

  Ümumi test sayı: 60+ yeni test

  7. ✅ i18n Translation Coverage

  Yoxlanılan template-lər (hamısında {% trans %} mövcuddur):
  - ✅ templates/recruitment/candidate_pipeline.html
  - ✅ templates/evaluations/calibration/dashboard.html
  - ✅ templates/evaluations/calibration/detail.html
  - ✅ templates/notifications/bulk_notification.html
  - ✅ templates/audit/security_dashboard.html

  8. ✅ Əlavə Tamamlanmış İşlər

  360° Kalibrə sistemi:
  - apps/evaluations/views_calibration.py - 5 view (dashboard, detail, adjust, finalize, bulk)
  - 2 tam HTML template (dashboard və detail)
  - Score distribution, statistika, permissions

  Digər modullar:
  - Leave approval workflow (avtomatik balance update)
  - Compensation history tracking
  - Bulk notification system
  - Security dashboard (already complete)

  ---
  📊 Fayl Statistikaları

  - Yeni modellər: DepartmentBudget
  - Yeni migration-lar: 1 (compensation)
  - Yoxlanmış/dəyişdirilmiş fayllar: 15+
  - Yeni test suite-lər: 4
  - Template-lər: Hamısı i18n-ready

  🎉 Nəticə

  Bütün 9 məsələ tam həll edildi:
  1. ✅ Modul İnteqrasiyası
  2. ✅ Export (PDF/Excel/CSV)
  3. ✅ Kompensasiya büdcə məntiq
  4. ✅ Kanban drag-drop
  5. ✅ Təhlükəsizlik threat detection
  6. ✅ Test coverage
  7. ✅ i18n translation','organization','active',2025,'annual','2025-10-16','2025-10-31',100,100,'2025-10-16 12:41:33.115606','2025-10-16 23:06:29.699384',8,'2025-10-16 23:06:29.708774',NULL,'~',2,2,1,1,NULL);
CREATE TABLE "development_plans_keyresult" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(300) NOT NULL, "description" text NOT NULL, "unit" varchar(20) NOT NULL, "baseline_value" decimal NOT NULL, "target_value" decimal NOT NULL, "current_value" decimal NOT NULL, "weight" decimal NOT NULL, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "objective_id" bigint NOT NULL REFERENCES "development_plans_strategicobjective" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "development_plans_keyresult" VALUES(1,'aaa','','boolean',0,5,5,100,1,'2025-10-16 21:59:36.200383','2025-10-16 23:06:29.672281',1);
CREATE TABLE "development_plans_kpi" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(200) NOT NULL, "description" text NOT NULL, "code" varchar(50) NOT NULL UNIQUE, "unit" varchar(50) NOT NULL, "target_value" decimal NOT NULL, "measurement_frequency" varchar(20) NOT NULL, "red_threshold" decimal NOT NULL, "yellow_threshold" decimal NOT NULL, "green_threshold" decimal NOT NULL, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "department_id" bigint NULL REFERENCES "departments_department" ("id") DEFERRABLE INITIALLY DEFERRED, "objective_id" bigint NULL REFERENCES "development_plans_strategicobjective" ("id") DEFERRABLE INITIALLY DEFERRED, "owner_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "development_plans_kpi" VALUES(1,'AzAgroPOS','İstifadəçinin tələb etdiyi 9 məsələ tam həll edildi:

  1. ✅ Modul İnteqrasiyası

  - templates/base/sidebar.html - Bütün yeni modullar və təhlükəsizlik dashboardu əlavə edildi (sətir 432-441)
  - apps/accounts/template_views.py - Dashboard tam HRIS modul datası ilə təchiz edildi (sətir 59-205)
  - Bütün yeni modullar navbar və sidebar-da mövcuddur

  2. ✅ Report Export Funksionallığı

  - PDF export: apps/reports/template_views.py - ReportLab ilə PDF yaradılması (sətir 58-110)
  - Excel export: OpenPyXL ilə XLSX formatı (sətir 112-152)
  - CSV export: apps/reports/utils.py - UTF-8-sig BOM ilə Excel uyğunluğu (sətir 95-117)
  - Multi-format endpoint: /reports/export/<format>/

  3. ✅ Kompensasiya Büdcə Məntiq

  Yeni model əlavə edildi: apps/compensation/models.py (sətir 510-601)
  - DepartmentBudget modeli illik büdcə, istifadə edilmiş məbləğ və qalıq hesablamaları
  - can_afford() metodu ilə büdcə yoxlaması
  - utilization_percentage property

  View-də büdcə validasiyası: apps/compensation/views.py (sətir 118-149)
  if dept_budget:
      if not dept_budget.can_afford(salary_difference):
          return JsonResponse({
              ''success'': False,
              ''message'': f''Büdcə kifayət etmir!...'',
              ''budget_exceeded'': True
          })

  Admin panel: Rəngli utilization percentage və remaining budget göstəricisi

  4. ✅ Kanban Drag-and-Drop

  Sortable.js tam inteqrasiya: templates/recruitment/candidate_pipeline.html (sətir 366-541)

  Əlavə edilən xüsusiyyətlər:
  - ✅ CSRF token düzgün implementasiyası (getCookie funksiyası)
  - ✅ Toast notification sistemi (slideIn/slideOut animation)
  - ✅ Loading state (.updating class)
  - ✅ Auto-revert on error
  - ✅ Real-time stage count update
  - ✅ Visual feedback (ghost class, chosen class)
  - ✅ Smooth animations (cubic-bezier easing)

  5. ✅ Təhlükəsizlik Dashbordu - Təhlükə Analizi

  Brute force detection funksiyası: apps/audit/template_views.py (sətir 12-64)
  def detect_brute_force_attacks(login_failures, time_window=5, threshold=5):
      # 5 dəqiqə ərzində 5+ səhv giriş
      # IP-yə görə qruplama və analiz

  Dashboard-a əlavələr (sətir 129-163):
  - 24 saat ərzində təhlükə axtarışı
  - Severity level (critical/high)
  - Threat table göstərimi (IP, targeted users, time span)

  Template: templates/audit/security_dashboard.html (sətir 216-285)
  - Qırmızı border ilə critical alert
  - Badge ilə threat count
  - Detailed threat table

  6. ✅ Test Coverage

  4 Yeni test modulu yaradıldı:
  1. apps/leave_attendance/tests/test_leave_approval_workflow.py - 11 test
  2. apps/compensation/tests/test_salary_management.py - 12 test
  3. apps/recruitment/tests/test_candidate_pipeline.py - 17 test
  4. apps/evaluations/tests/test_calibration_workflow.py - 20 test

  BaseTestCase pattern - Organization FK problemi həll edildi
  - apps/recruitment/tests/test_base.py
  - apps/compensation/tests/test_base.py

  Ümumi test sayı: 60+ yeni test

  7. ✅ i18n Translation Coverage

  Yoxlanılan template-lər (hamısında {% trans %} mövcuddur):
  - ✅ templates/recruitment/candidate_pipeline.html
  - ✅ templates/evaluations/calibration/dashboard.html
  - ✅ templates/evaluations/calibration/detail.html
  - ✅ templates/notifications/bulk_notification.html
  - ✅ templates/audit/security_dashboard.html

  8. ✅ Əlavə Tamamlanmış İşlər

  360° Kalibrə sistemi:
  - apps/evaluations/views_calibration.py - 5 view (dashboard, detail, adjust, finalize, bulk)
  - 2 tam HTML template (dashboard və detail)
  - Score distribution, statistika, permissions

  Digər modullar:
  - Leave approval workflow (avtomatik balance update)
  - Compensation history tracking
  - Bulk notification system
  - Security dashboard (already complete)

  ---
  📊 Fayl Statistikaları

  - Yeni modellər: DepartmentBudget
  - Yeni migration-lar: 1 (compensation)
  - Yoxlanmış/dəyişdirilmiş fayllar: 15+
  - Yeni test suite-lər: 4
  - Template-lər: Hamısı i18n-ready

  🎉 Nəticə

  Bütün 9 məsələ tam həll edildi:
  1. ✅ Modul İnteqrasiyası
  2. ✅ Export (PDF/Excel/CSV)
  3. ✅ Kompensasiya büdcə məntiq
  4. ✅ Kanban drag-drop
  5. ✅ Təhlükəsizlik threat detection
  6. ✅ Test coverage
  7. ✅ i18n translation','01','1',5,'monthly',5,10,15,1,'2025-10-16 12:42:30.548364','2025-10-16 21:58:25.455594',2,1,1);
CREATE TABLE "development_plans_kpimeasurement" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "measurement_date" date NOT NULL, "actual_value" decimal NOT NULL, "trend" varchar(10) NULL, "notes" text NOT NULL, "created_at" datetime NOT NULL, "kpi_id" bigint NOT NULL REFERENCES "development_plans_kpi" ("id") DEFERRABLE INITIALLY DEFERRED, "measured_by_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "development_plans_kpimeasurement" VALUES(1,'2025-10-17',45,'down','454','2025-10-16 21:56:40.443606',1,1);
CREATE TABLE "development_plans_milestone" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(200) NOT NULL, "description" text NOT NULL, "due_date" date NOT NULL, "is_completed" bool NOT NULL, "completed_at" datetime NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "created_by_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "objective_id" bigint NOT NULL REFERENCES "development_plans_strategicobjective" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "development_plans_objectiveupdate" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "content" text NOT NULL, "progress_value" decimal NULL, "created_at" datetime NOT NULL, "created_by_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "objective_id" bigint NOT NULL REFERENCES "development_plans_strategicobjective" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "development_plans_progresslog" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "note" text NOT NULL, "progress_percentage" integer NOT NULL, "created_at" datetime NOT NULL, "goal_id" bigint NOT NULL REFERENCES "development_plans_developmentgoal" ("id") DEFERRABLE INITIALLY DEFERRED, "logged_by_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "is_draft" bool NOT NULL, "updated_at" datetime NOT NULL);
INSERT INTO "development_plans_progresslog" VALUES(1,'aaaaaaaaaaaaaa',3,'2025-10-09 07:30:00.992617',1,1,0,'2025-10-09 22:29:32.962249');
INSERT INTO "development_plans_progresslog" VALUES(2,'Məqsəd tamamlandı',100,'2025-10-09 11:25:12.949164',1,1,0,'2025-10-09 22:29:32.962249');
INSERT INTO "development_plans_progresslog" VALUES(3,'İlk mərhələ tamamlandı',100,'2025-10-09 22:18:06.698408',2,1,0,'2025-10-09 22:29:32.962249');
INSERT INTO "development_plans_progresslog" VALUES(4,'Məqsəd tamamlandı',100,'2025-10-09 22:44:36.065034',2,1,0,'2025-10-09 22:44:36.065084');
CREATE TABLE "development_plans_strategicobjective" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(300) NOT NULL, "description" text NOT NULL, "level" varchar(20) NOT NULL, "status" varchar(20) NOT NULL, "fiscal_year" integer NOT NULL, "quarter" varchar(10) NOT NULL, "start_date" date NOT NULL, "end_date" date NOT NULL, "progress_percentage" decimal NOT NULL, "weight" decimal NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "created_by_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "department_id" bigint NULL REFERENCES "departments_department" ("id") DEFERRABLE INITIALLY DEFERRED, "owner_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "parent_objective_id" bigint NULL REFERENCES "development_plans_strategicobjective" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "development_plans_strategicobjective" VALUES(1,'admin test','stifadəçinin tələb etdiyi 9 məsələ tam həll edildi:

  1. ✅ Modul İnteqrasiyası

  - templates/base/sidebar.html - Bütün yeni modullar və təhlükəsizlik dashboardu əlavə edildi (sətir 432-441)
  - apps/accounts/template_views.py - Dashboard tam HRIS modul datası ilə təchiz edildi (sətir 59-205)
  - Bütün yeni modullar navbar və sidebar-da mövcuddur

  2. ✅ Report Export Funksionallığı

  - PDF export: apps/reports/template_views.py - ReportLab ilə PDF yaradılması (sətir 58-110)
  - Excel export: OpenPyXL ilə XLSX formatı (sətir 112-152)
  - CSV export: apps/reports/utils.py - UTF-8-sig BOM ilə Excel uyğunluğu (sətir 95-117)
  - Multi-format endpoint: /reports/export/<format>/

  3. ✅ Kompensasiya Büdcə Məntiq

  Yeni model əlavə edildi: apps/compensation/models.py (sətir 510-601)
  - DepartmentBudget modeli illik büdcə, istifadə edilmiş məbləğ və qalıq hesablamaları
  - can_afford() metodu ilə büdcə yoxlaması
  - utilization_percentage property

  View-də büdcə validasiyası: apps/compensation/views.py (sətir 118-149)
  if dept_budget:
      if not dept_budget.can_afford(salary_difference):
          return JsonResponse({
              ''success'': False,
              ''message'': f''Büdcə kifayət etmir!...'',
              ''budget_exceeded'': True
          })

  Admin panel: Rəngli utilization percentage və remaining budget göstəricisi

  4. ✅ Kanban Drag-and-Drop

  Sortable.js tam inteqrasiya: templates/recruitment/candidate_pipeline.html (sətir 366-541)

  Əlavə edilən xüsusiyyətlər:
  - ✅ CSRF token düzgün implementasiyası (getCookie funksiyası)
  - ✅ Toast notification sistemi (slideIn/slideOut animation)
  - ✅ Loading state (.updating class)
  - ✅ Auto-revert on error
  - ✅ Real-time stage count update
  - ✅ Visual feedback (ghost class, chosen class)
  - ✅ Smooth animations (cubic-bezier easing)

  5. ✅ Təhlükəsizlik Dashbordu - Təhlükə Analizi

  Brute force detection funksiyası: apps/audit/template_views.py (sətir 12-64)
  def detect_brute_force_attacks(login_failures, time_window=5, threshold=5):
      # 5 dəqiqə ərzində 5+ səhv giriş
      # IP-yə görə qruplama və analiz

  Dashboard-a əlavələr (sətir 129-163):
  - 24 saat ərzində təhlükə axtarışı
  - Severity level (critical/high)
  - Threat table göstərimi (IP, targeted users, time span)

  Template: templates/audit/security_dashboard.html (sətir 216-285)
  - Qırmızı border ilə critical alert
  - Badge ilə threat count
  - Detailed threat table

  6. ✅ Test Coverage

  4 Yeni test modulu yaradıldı:
  1. apps/leave_attendance/tests/test_leave_approval_workflow.py - 11 test
  2. apps/compensation/tests/test_salary_management.py - 12 test
  3. apps/recruitment/tests/test_candidate_pipeline.py - 17 test
  4. apps/evaluations/tests/test_calibration_workflow.py - 20 test

  BaseTestCase pattern - Organization FK problemi həll edildi
  - apps/recruitment/tests/test_base.py
  - apps/compensation/tests/test_base.py

  Ümumi test sayı: 60+ yeni test

  7. ✅ i18n Translation Coverage

  Yoxlanılan template-lər (hamısında {% trans %} mövcuddur):
  - ✅ templates/recruitment/candidate_pipeline.html
  - ✅ templates/evaluations/calibration/dashboard.html
  - ✅ templates/evaluations/calibration/detail.html
  - ✅ templates/notifications/bulk_notification.html
  - ✅ templates/audit/security_dashboard.html

  8. ✅ Əlavə Tamamlanmış İşlər

  360° Kalibrə sistemi:
  - apps/evaluations/views_calibration.py - 5 view (dashboard, detail, adjust, finalize, bulk)
  - 2 tam HTML template (dashboard və detail)
  - Score distribution, statistika, permissions

  Digər modullar:
  - Leave approval workflow (avtomatik balance update)
  - Compensation history tracking
  - Bulk notification system
  - Security dashboard (already complete)

  ---
  📊 Fayl Statistikaları

  - Yeni modellər: DepartmentBudget
  - Yeni migration-lar: 1 (compensation)
  - Yoxlanmış/dəyişdirilmiş fayllar: 15+
  - Yeni test suite-lər: 4
  - Template-lər: Hamısı i18n-ready

  🎉 Nəticə

  Bütün 9 məsələ tam həll edildi:
  1. ✅ Modul İnteqrasiyası
  2. ✅ Export (PDF/Excel/CSV)
  3. ✅ Kompensasiya büdcə məntiq
  4. ✅ Kanban drag-drop
  5. ✅ Təhlükəsizlik threat detection
  6. ✅ Test coverage
  7. ✅ i18n translation','organization','active',2025,'annual','2025-10-16','2025-10-31',100,100,'2025-10-16 12:41:33.115606','2025-10-16 23:06:29.699384',2,2,1,NULL);
CREATE TABLE "django_admin_log" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "object_id" text NULL, "object_repr" varchar(200) NOT NULL, "action_flag" smallint unsigned NOT NULL CHECK ("action_flag" >= 0), "change_message" text NOT NULL, "content_type_id" integer NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "action_time" datetime NOT NULL);
INSERT INTO "django_admin_log" VALUES(1,'1','Admin User - Profil',2,'[{"changed": {"fields": ["\u0130\u015f\u0259 Q\u0259bul Tarixi"]}}]',11,1,'2025-10-09 06:45:59.994217');
INSERT INTO "django_admin_log" VALUES(2,'1','baş admin',1,'[{"added": {}}]',10,1,'2025-10-09 06:46:54.256145');
INSERT INTO "django_admin_log" VALUES(3,'1','nazirlik',1,'[{"added": {}}]',19,1,'2025-10-09 06:49:07.775994');
INSERT INTO "django_admin_log" VALUES(4,'1','nazirlik: nazirlik...',1,'[{"added": {}}]',20,1,'2025-10-09 06:50:32.016855');
INSERT INTO "django_admin_log" VALUES(5,'1','Mədəniyyət',1,'[{"added": {}}]',16,1,'2025-10-09 07:14:01.122111');
INSERT INTO "django_admin_log" VALUES(6,'1','q360',1,'[{"added": {}}]',3,1,'2025-10-09 07:16:50.869672');
INSERT INTO "django_admin_log" VALUES(7,'1','Admin User',2,'[{"changed": {"fields": ["Telefon", "Rol", "V\u0259zif\u0259", "\u0130\u015f\u00e7i ID", "R\u0259hb\u0259r", "Haqq\u0131nda", "Groups", "User permissions"]}}]',6,1,'2025-10-09 07:20:04.097127');
INSERT INTO "django_admin_log" VALUES(8,'1','admin - azərbaycan',1,'[{"added": {}}]',32,1,'2025-10-09 07:29:47.557236');
INSERT INTO "django_admin_log" VALUES(9,'1','azərbaycan - 3%',1,'[{"added": {}}]',33,1,'2025-10-09 07:30:00.995885');
INSERT INTO "django_admin_log" VALUES(10,'1','admin - azərbaycan',2,'[{"changed": {"fields": ["Completion date"]}}]',32,1,'2025-10-09 07:30:37.167883');
INSERT INTO "django_admin_log" VALUES(11,'1','Admin User',2,'[{"changed": {"fields": ["Username"]}}]',6,1,'2025-10-09 10:57:25.511134');
INSERT INTO "django_admin_log" VALUES(12,'1','Tahmaz Seyran Muradov',2,'[{"changed": {"fields": ["First name", "Ata ad\u0131", "Last name"]}}]',6,1,'2025-10-09 10:57:59.648082');
INSERT INTO "django_admin_log" VALUES(13,'1','2025 İllik Qiymətləndirmə - nazirlik',1,'[{"added": {}}]',25,1,'2025-10-09 11:37:31.785759');
INSERT INTO "django_admin_log" VALUES(14,'1','Tahmaz Seyran Muradov - 2025 İllik Qiymətləndirmə',1,'[{"added": {}}]',27,1,'2025-10-09 11:38:32.616906');
INSERT INTO "django_admin_log" VALUES(15,'1','Tahmaz Seyran Muradov → Tahmaz Seyran Muradov',1,'[{"added": {}}]',24,1,'2025-10-09 11:41:24.274811');
INSERT INTO "django_admin_log" VALUES(16,'1','Tahmaz - aaaaaaaaa',1,'[{"added": {}}]',29,1,'2025-10-09 11:48:22.698259');
INSERT INTO "django_admin_log" VALUES(17,'1','AzAgroPOS',1,'[{"added": {}}]',28,1,'2025-10-09 12:05:19.811846');
INSERT INTO "django_admin_log" VALUES(18,'1','Tahmaz - usersd',1,'[{"added": {}}]',31,1,'2025-10-09 12:06:20.039466');
INSERT INTO "django_admin_log" VALUES(19,'2','Tahmaz - inkişaf',1,'[{"added": {}}]',32,1,'2025-10-09 12:08:06.162410');
INSERT INTO "django_admin_log" VALUES(20,'1','Tahmaz Seyran Muradov - Profil',2,'[{"changed": {"fields": ["T\u0259hsil S\u0259viyy\u0259si", "\u0130xtisas"]}}]',11,1,'2025-10-09 12:08:46.379278');
INSERT INTO "django_admin_log" VALUES(21,'1','Tahmaz Seyran Muradov - Profil',2,'[{"changed": {"fields": ["\u0130\u015f E-po\u00e7tu", "\u0130\u015f Telefonu", "\u00dcnvan"]}}]',11,1,'2025-10-09 12:09:02.265492');
INSERT INTO "django_admin_log" VALUES(22,'1','muradoffcode@gmail.com - aaaaaaaaaaaaaaaa',1,'[{"added": {}}]',35,1,'2025-10-09 23:28:19.456837');
INSERT INTO "django_admin_log" VALUES(23,'2','2024 - İllik Performans Qiymətləndirməsi - Komanda üzvlərini motivasiya e',2,'[{"changed": {"fields": ["S\u0131ra"]}}]',25,1,'2025-10-10 20:36:25.250961');
INSERT INTO "django_admin_log" VALUES(24,'19','Murad Süleymanov',2,'[{"changed": {"fields": ["\u0130\u015f\u00e7i ID"]}}]',6,1,'2025-10-10 20:40:15.830196');
INSERT INTO "django_admin_log" VALUES(25,'2','Tahmaz - inkişaf',2,'[]',32,1,'2025-10-10 20:42:15.802400');
INSERT INTO "django_admin_log" VALUES(26,'1','Tahmaz Seyran Muradov',2,'[{"changed": {"fields": ["Profil \u015e\u0259kli"]}}]',6,1,'2025-10-10 20:43:12.019273');
INSERT INTO "django_admin_log" VALUES(27,'1','Tahmaz Seyran Muradov',2,'[]',6,1,'2025-10-10 20:44:02.574288');
INSERT INTO "django_admin_log" VALUES(28,'1','Tahmaz Seyran Muradov',2,'[{"changed": {"fields": ["\u015e\u00f6b\u0259"]}}]',6,1,'2025-10-10 20:44:22.169867');
INSERT INTO "django_admin_log" VALUES(29,'1','AzAgroPOS',2,'[]',28,1,'2025-10-10 20:44:34.355281');
INSERT INTO "django_admin_log" VALUES(30,'1','AzAgroPOS',2,'[]',28,1,'2025-10-10 20:44:47.374465');
INSERT INTO "django_admin_log" VALUES(31,'2','aaaaaaaaaaaaaaaaa',1,'[{"added": {}}]',28,1,'2025-10-10 20:45:00.671434');
INSERT INTO "django_admin_log" VALUES(32,'6','Problemlərin Həlli',2,'[{"changed": {"fields": ["S\u0131ra"]}}]',19,1,'2025-10-10 20:46:14.422144');
INSERT INTO "django_admin_log" VALUES(33,'1','baş admin',2,'[{"changed": {"fields": ["\u0130caz\u0259l\u0259r"]}}]',10,1,'2025-10-10 20:48:20.508451');
INSERT INTO "django_admin_log" VALUES(34,'1','Tahmaz Seyran Muradov',2,'[]',6,1,'2025-10-10 20:55:10.461314');
INSERT INTO "django_admin_log" VALUES(35,'2','İşçi',1,'[{"added": {}}]',10,1,'2025-10-10 21:06:01.874854');
INSERT INTO "django_admin_log" VALUES(36,'3','Admin',1,'[{"added": {}}]',10,1,'2025-10-10 21:06:28.216680');
INSERT INTO "django_admin_log" VALUES(37,'4','Rəhbər',1,'[{"added": {}}]',10,1,'2025-10-10 21:07:06.005493');
INSERT INTO "django_admin_log" VALUES(38,'15','Farid Abdullayev',2,'[{"changed": {"fields": ["password"]}}]',6,1,'2025-10-10 21:07:55.741296');
INSERT INTO "django_admin_log" VALUES(39,'15','Farid Abdullayev',2,'[{"changed": {"fields": ["Profil \u015e\u0259kli"]}}]',6,1,'2025-10-10 21:08:34.599318');
INSERT INTO "django_admin_log" VALUES(40,'15','Farid Abdullayev',2,'[{"changed": {"fields": ["User permissions"]}}]',6,1,'2025-10-10 21:09:20.118306');
INSERT INTO "django_admin_log" VALUES(41,'1','Liderlik Əsasları (Kurs)',2,'[{"changed": {"fields": ["M\u0259cburi"]}}]',47,1,'2025-10-11 08:09:57.212853');
INSERT INTO "django_admin_log" VALUES(42,'1','Tahmaz Seyran Muradov - Liderlik Əsasları (Davam Edir)',1,'[{"added": {}}]',49,1,'2025-10-11 08:11:25.211527');
INSERT INTO "django_admin_log" VALUES(43,'1','1 - Açıq',1,'[{"added": {}}]',37,1,'2025-10-11 18:00:21.676366');
INSERT INTO "django_admin_log" VALUES(44,'1','1 - Şərh',1,'[{"added": {}}]',38,1,'2025-10-11 18:01:00.404664');
INSERT INTO "django_admin_log" VALUES(45,'1','Tahmaz Seyran Muradov - Texniki Bilik (Boşluq: 4)',1,'[{"added": {}}]',53,1,'2025-10-14 22:10:31.296973');
INSERT INTO "django_admin_log" VALUES(46,'1','Sistem Administratoru (Orta)',1,'[{"added": {}}]',50,1,'2025-10-14 22:11:28.104048');
INSERT INTO "django_admin_log" VALUES(47,'1','Admin İstifadəçi → Sistem Administratoru',1,'[{"added": {}}]',52,1,'2025-10-14 22:12:09.871464');
INSERT INTO "django_admin_log" VALUES(48,'1','Tahmaz Seyran Muradov - 9. Qutu - Üstün İstedad (2025 q2)',1,'[{"added": {}}]',51,1,'2025-10-14 22:13:13.991501');
INSERT INTO "django_admin_log" VALUES(49,'1','Sistem Administratoru - Texniki Bilik (50%)',1,'[{"added": {}}]',43,1,'2025-10-14 22:14:33.029469');
INSERT INTO "django_admin_log" VALUES(50,'1','Tahmaz Seyran Muradov - İnnovasiya (Ekspert)',1,'[{"added": {}}]',45,1,'2025-10-14 22:15:31.980814');
INSERT INTO "django_admin_log" VALUES(51,'1','Tahmaz Seyran Muradov',2,'[{"changed": {"fields": ["User permissions"]}}]',6,1,'2025-10-14 22:16:27.495660');
INSERT INTO "django_admin_log" VALUES(52,'1','Tahmaz Seyran Muradov',2,'[{"changed": {"fields": ["\u015e\u00f6b\u0259"]}}]',6,1,'2025-10-14 22:16:47.816562');
INSERT INTO "django_admin_log" VALUES(53,'20','Tahmaz Seyran Muradov',2,'[{"changed": {"fields": ["First name", "Ata ad\u0131", "Last name", "Telefon", "Rol", "\u015e\u00f6b\u0259", "V\u0259zif\u0259", "\u0130\u015f\u00e7i ID", "R\u0259hb\u0259r", "Groups", "User permissions"]}}]',6,1,'2025-10-14 22:17:55.686208');
INSERT INTO "django_admin_log" VALUES(54,'1','kitabxana',1,'[{"added": {}}]',54,1,'2025-10-15 07:26:35.422922');
INSERT INTO "django_admin_log" VALUES(55,'2','22222222',1,'[{"added": {}}]',54,1,'2025-10-15 07:26:46.540840');
INSERT INTO "django_admin_log" VALUES(56,'15','Farid Abdullayev',2,'[{"changed": {"fields": ["\u015e\u00f6b\u0259"]}}]',6,1,'2025-10-15 11:43:22.050288');
INSERT INTO "django_admin_log" VALUES(57,'4','Müştəri Xidməti Mükəmməlliyi (Vebinar)',2,'[{"changed": {"fields": ["\u018flaq\u0259li Kompetensiyalar"]}}]',47,1,'2025-10-15 11:52:50.773185');
INSERT INTO "django_admin_log" VALUES(58,'2','Effektiv Kommunikasiya Bacarıqları (Vebinar)',2,'[{"changed": {"fields": ["T\u0259lim N\u00f6v\u00fc", "\u00c7\u0259tinlik S\u0259viyy\u0259si", "Onlayn", "\u00c7atd\u0131r\u0131lma Metodu", "\u018flaq\u0259li Kompetensiyalar", "Maksimum \u0130\u015ftirak\u00e7\u0131", "M\u0259cburi"]}}]',47,1,'2025-10-15 11:53:40.064582');
INSERT INTO "django_admin_log" VALUES(59,'10','Mədəniyyət - helpdes',1,'[{"added": {}}]',12,1,'2025-10-15 11:58:13.053680');
INSERT INTO "django_admin_log" VALUES(60,'10','Mədəniyyət - helpdes',2,'[{"changed": {"fields": ["\u00dcst \u015e\u00f6b\u0259"]}}]',12,1,'2025-10-15 11:58:50.234749');
INSERT INTO "django_admin_log" VALUES(61,'2','TahmazMuradov',1,'[{"added": {}}]',3,1,'2025-10-15 13:55:41.660154');
INSERT INTO "django_admin_log" VALUES(62,'1','PDF Hesabat - Tahmaz (İşlənir)',1,'[{"added": {}}]',36,1,'2025-10-15 21:30:08.837331');
INSERT INTO "django_admin_log" VALUES(63,'16','Sevinc Qasımova',2,'[{"changed": {"fields": ["Groups", "User permissions"]}}]',6,1,'2025-10-16 00:52:15.939289');
INSERT INTO "django_admin_log" VALUES(64,'1','test - 2025-10-16',1,'[{"added": {}}]',77,1,'2025-10-16 07:39:50.207035');
INSERT INTO "django_admin_log" VALUES(65,'1','əmək',1,'[{"added": {}}]',74,1,'2025-10-16 08:20:11.271067');
INSERT INTO "django_admin_log" VALUES(66,'1','əmək',2,'[{"changed": {"fields": ["N\u00f6vb\u0259ti \u0130l\u0259 Ke\u00e7ir", "Maksimum Ke\u00e7id G\u00fcn Say\u0131"]}}]',74,1,'2025-10-16 08:20:37.498237');
INSERT INTO "django_admin_log" VALUES(67,'2','sosial',1,'[{"added": {}}]',74,1,'2025-10-16 08:21:48.429790');
INSERT INTO "django_admin_log" VALUES(68,'1','Tahmaz Seyran Muradov - əmək (2025)',1,'[{"added": {}}]',76,1,'2025-10-16 08:22:58.396588');
INSERT INTO "django_admin_log" VALUES(69,'1','Tahmaz Seyran Muradov - sosial (2025-10-16 - 2025-10-20)',1,'[{"added": {}}]',75,1,'2025-10-16 08:24:52.806892');
INSERT INTO "django_admin_log" VALUES(70,'1','aaaaaaaaaaaa (2025 - annual)',1,'[{"added": {}}]',85,1,'2025-10-16 12:41:33.120851');
INSERT INTO "django_admin_log" VALUES(71,'1','01 - AzAgroPOS',1,'[{"added": {}}]',84,1,'2025-10-16 12:42:30.552715');
INSERT INTO "django_admin_log" VALUES(72,'1','Tahmaz Seyran Muradov bəyəndi',1,'[{"added": {}}]',59,1,'2025-10-16 12:44:41.947780');
INSERT INTO "django_admin_log" VALUES(73,'2','Tahmaz Seyran Muradov bəyəndi',1,'[{"added": {}}]',59,1,'2025-10-16 12:44:59.033545');
INSERT INTO "django_admin_log" VALUES(74,'1','Tahmaz Seyran Muradov: 11111111111111111111111111111111',1,'[{"added": {}}]',56,1,'2025-10-16 12:45:21.324307');
INSERT INTO "django_admin_log" VALUES(75,'2','Tahmaz Seyran Muradov: 000000000000',1,'[{"added": {}}]',56,1,'2025-10-16 12:45:38.783152');
INSERT INTO "django_admin_log" VALUES(76,'1','İctimai Təqdir: əla',2,'[{"changed": {"fields": ["Se\u00e7ilm\u0259 M\u00fcdd\u0259ti"]}}]',55,1,'2025-10-16 12:46:02.684496');
INSERT INTO "django_admin_log" VALUES(77,'1','İctimai Təqdir: əla',2,'[{"changed": {"fields": ["X\u00fcsusi Se\u00e7ilmi\u015f"]}}]',55,1,'2025-10-16 12:46:11.708209');
INSERT INTO "django_admin_log" VALUES(78,'1','01 - it',1,'[{"added": {}}]',93,1,'2025-10-16 12:54:32.932240');
INSERT INTO "django_admin_log" VALUES(79,'1','Tahmaz Muradov - it',1,'[{"added": {}}]',92,1,'2025-10-16 12:56:10.176031');
INSERT INTO "django_admin_log" VALUES(80,'1','Tahmaz Muradov - aaaaaaaaaa - 5000 AZN',1,'[{"added": {}}]',101,1,'2025-10-16 12:57:26.066346');
INSERT INTO "django_admin_log" VALUES(81,'1','Tahmaz Seyran Muradov - Layihə Bonusu - 50000 AZN',1,'[{"added": {}}]',72,1,'2025-10-16 21:04:02.840190');
INSERT INTO "django_admin_log" VALUES(82,'1','Tahmaz Seyran Muradov - 5000 AZN (2025-10-17)',1,'[{"added": {}}]',64,1,'2025-10-16 21:10:41.402566');
INSERT INTO "django_admin_log" VALUES(83,'2','Tahmaz Seyran Muradov - 6000 AZN (2025-10-17)',1,'[{"added": {}}]',64,1,'2025-10-16 21:12:05.983746');
INSERT INTO "django_admin_log" VALUES(84,'1','Tahmaz Seyran Muradov - 4000 AZN',1,'[{"added": {}}]',70,1,'2025-10-16 21:14:49.748136');
INSERT INTO "django_admin_log" VALUES(85,'2','Tahmaz Seyran Muradov - 5000 USD',1,'[{"added": {}}]',70,1,'2025-10-16 21:15:54.543746');
INSERT INTO "django_admin_log" VALUES(86,'1','Tahmaz Seyran Muradov - Mobil Telefon Müavinəti - 500 AZN',1,'[{"added": {}}]',66,1,'2025-10-16 21:17:47.026437');
INSERT INTO "django_admin_log" VALUES(87,'1','Tahmaz Seyran Muradov - Gəlir Vergisi',1,'[{"added": {}}]',71,1,'2025-10-16 21:19:51.307264');
INSERT INTO "django_admin_log" VALUES(88,'2','Tahmaz Seyran Muradov - Gəlir Vergisi',1,'[{"added": {}}]',71,1,'2025-10-16 21:20:47.412659');
INSERT INTO "django_admin_log" VALUES(89,'1','Tahmaz Muradov',2,'[{"changed": {"fields": ["Ata ad\u0131"]}}, {"changed": {"name": "Profil", "object": "Tahmaz Muradov - Profil", "fields": ["T\u0259hsil S\u0259viyy\u0259si"]}}]',6,1,'2025-10-16 21:21:23.154992');
INSERT INTO "django_admin_log" VALUES(90,'1','Tahmaz Muradov - Layihə Bonusu - 50000.00 AZN',2,'[{"changed": {"fields": ["Maliyy\u0259 \u0130li", "T\u0259sdiql\u0259y\u0259n", "Yaradan"]}}]',72,1,'2025-10-16 21:25:17.549351');
INSERT INTO "django_admin_log" VALUES(91,'1','Tahmaz Muradov - 5000.00 AZN (2025-10-17)',2,'[{"changed": {"fields": ["T\u0259sdiql\u0259y\u0259n", "Qeydl\u0259r", "Yaradan"]}}]',64,1,'2025-10-16 21:26:01.627952');
INSERT INTO "django_admin_log" VALUES(92,'1','Tahmaz Muradov - Mobil Telefon Müavinəti - 500.00 AZN',2,'[{"changed": {"fields": ["T\u0259svir"]}}]',66,1,'2025-10-16 21:26:40.383591');
INSERT INTO "django_admin_log" VALUES(93,'2','tecili - Açıq',1,'[{"added": {}}, {"added": {"name": "Sor\u011fu \u015e\u0259rhi", "object": "tecili - \u015e\u0259rh"}}, {"added": {"name": "Sor\u011fu \u015e\u0259rhi", "object": "tecili - \u015e\u0259rh"}}, {"added": {"name": "Sor\u011fu \u015e\u0259rhi", "object": "tecili - \u015e\u0259rh"}}, {"added": {"name": "Sor\u011fu \u015e\u0259rhi", "object": "tecili - \u015e\u0259rh"}}]',37,1,'2025-10-16 21:28:33.318821');
INSERT INTO "django_admin_log" VALUES(94,'1','1 - Açıq',2,'[{"changed": {"fields": ["T\u0259yin Edildi"]}}, {"added": {"name": "Sor\u011fu \u015e\u0259rhi", "object": "1 - \u015e\u0259rh"}}]',37,1,'2025-10-16 21:29:44.876831');
INSERT INTO "django_admin_log" VALUES(95,'2','muradofftehmez01@gmail.com - aaaaaaaaaaaaaaaa',1,'[{"added": {}}]',35,1,'2025-10-16 21:33:00.998978');
INSERT INTO "django_admin_log" VALUES(96,'1','muradoffcode@gmail.com - aaaaaaaaaaaaaaaa',2,'[{"changed": {"fields": ["Status"]}}]',35,1,'2025-10-16 21:33:14.412453');
INSERT INTO "django_admin_log" VALUES(97,'1566','aynur - salam ',3,'',29,1,'2025-10-16 21:34:30.403575');
INSERT INTO "django_admin_log" VALUES(98,'1565','employee1 - salam ',3,'',29,1,'2025-10-16 21:34:30.403621');
INSERT INTO "django_admin_log" VALUES(99,'1564','murad.aliyev - salam ',3,'',29,1,'2025-10-16 21:34:30.403651');
INSERT INTO "django_admin_log" VALUES(100,'1563','kamran - salam ',3,'',29,1,'2025-10-16 21:34:30.403678');
INSERT INTO "django_admin_log" VALUES(101,'1562','admin - salam ',3,'',29,1,'2025-10-16 21:34:30.403703');
INSERT INTO "django_admin_log" VALUES(102,'1561','gunel - salam ',3,'',29,1,'2025-10-16 21:34:30.403728');
INSERT INTO "django_admin_log" VALUES(103,'1560','employee3 - salam ',3,'',29,1,'2025-10-16 21:34:30.403752');
INSERT INTO "django_admin_log" VALUES(104,'1559','farid.ismayilov - salam ',3,'',29,1,'2025-10-16 21:34:30.403775');
INSERT INTO "django_admin_log" VALUES(105,'1558','murad - salam ',3,'',29,1,'2025-10-16 21:34:30.403798');
INSERT INTO "django_admin_log" VALUES(106,'1557','aysel - salam ',3,'',29,1,'2025-10-16 21:34:30.403834');
INSERT INTO "django_admin_log" VALUES(107,'1556','elvin.quliyev - salam ',3,'',29,1,'2025-10-16 21:34:30.403857');
INSERT INTO "django_admin_log" VALUES(108,'1555','elvin - salam ',3,'',29,1,'2025-10-16 21:34:30.403879');
INSERT INTO "django_admin_log" VALUES(109,'1554','sevinc - salam ',3,'',29,1,'2025-10-16 21:34:30.403901');
INSERT INTO "django_admin_log" VALUES(110,'1553','nigar - salam ',3,'',29,1,'2025-10-16 21:34:30.403924');
INSERT INTO "django_admin_log" VALUES(111,'1552','aysel.memmedova - salam ',3,'',29,1,'2025-10-16 21:34:30.403946');
INSERT INTO "django_admin_log" VALUES(112,'1551','rashad.mammadov - salam ',3,'',29,1,'2025-10-16 21:34:30.403967');
INSERT INTO "django_admin_log" VALUES(113,'1550','rashad - salam ',3,'',29,1,'2025-10-16 21:34:30.403997');
INSERT INTO "django_admin_log" VALUES(114,'1549','manager - salam ',3,'',29,1,'2025-10-16 21:34:30.404018');
INSERT INTO "django_admin_log" VALUES(115,'1548','tahmaz - salam ',3,'',29,1,'2025-10-16 21:34:30.404040');
INSERT INTO "django_admin_log" VALUES(116,'1546','nigar.hasanova - salam ',3,'',29,1,'2025-10-16 21:34:30.404061');
INSERT INTO "django_admin_log" VALUES(117,'1545','leyla - salam ',3,'',29,1,'2025-10-16 21:34:30.404082');
INSERT INTO "django_admin_log" VALUES(118,'1544','elchin - salam ',3,'',29,1,'2025-10-16 21:34:30.404103');
INSERT INTO "django_admin_log" VALUES(119,'1543','employee2 - salam ',3,'',29,1,'2025-10-16 21:34:30.404124');
INSERT INTO "django_admin_log" VALUES(120,'1542','leyla.huseynova - salam ',3,'',29,1,'2025-10-16 21:34:30.404146');
INSERT INTO "django_admin_log" VALUES(121,'1541','sevinc.huseynli - salam ',3,'',29,1,'2025-10-16 21:34:30.404167');
INSERT INTO "django_admin_log" VALUES(122,'1540','tural - salam ',3,'',29,1,'2025-10-16 21:34:30.404188');
INSERT INTO "django_admin_log" VALUES(123,'1539','kamran.bashirov - salam ',3,'',29,1,'2025-10-16 21:34:30.404210');
INSERT INTO "django_admin_log" VALUES(124,'1538','farid - salam ',3,'',29,1,'2025-10-16 21:34:30.404231');
INSERT INTO "django_admin_log" VALUES(125,'1537','aynur - 1111111',3,'',29,1,'2025-10-16 21:34:30.404251');
INSERT INTO "django_admin_log" VALUES(126,'1536','employee1 - 1111111',3,'',29,1,'2025-10-16 21:34:30.404285');
INSERT INTO "django_admin_log" VALUES(127,'1535','murad.aliyev - 1111111',3,'',29,1,'2025-10-16 21:34:30.404307');
INSERT INTO "django_admin_log" VALUES(128,'1534','kamran - 1111111',3,'',29,1,'2025-10-16 21:34:30.404327');
INSERT INTO "django_admin_log" VALUES(129,'1533','admin - 1111111',3,'',29,1,'2025-10-16 21:34:30.404348');
INSERT INTO "django_admin_log" VALUES(130,'1532','gunel - 1111111',3,'',29,1,'2025-10-16 21:34:30.404369');
INSERT INTO "django_admin_log" VALUES(131,'1531','employee3 - 1111111',3,'',29,1,'2025-10-16 21:34:30.404390');
INSERT INTO "django_admin_log" VALUES(132,'1530','farid.ismayilov - 1111111',3,'',29,1,'2025-10-16 21:34:30.404411');
INSERT INTO "django_admin_log" VALUES(133,'1529','murad - 1111111',3,'',29,1,'2025-10-16 21:34:30.404432');
INSERT INTO "django_admin_log" VALUES(134,'1528','aysel - 1111111',3,'',29,1,'2025-10-16 21:34:30.404452');
INSERT INTO "django_admin_log" VALUES(135,'1527','elvin.quliyev - 1111111',3,'',29,1,'2025-10-16 21:34:30.404473');
INSERT INTO "django_admin_log" VALUES(136,'1526','elvin - 1111111',3,'',29,1,'2025-10-16 21:34:30.404506');
INSERT INTO "django_admin_log" VALUES(137,'1525','sevinc - 1111111',3,'',29,1,'2025-10-16 21:34:30.404527');
INSERT INTO "django_admin_log" VALUES(138,'1524','nigar - 1111111',3,'',29,1,'2025-10-16 21:34:30.404549');
INSERT INTO "django_admin_log" VALUES(139,'1523','aysel.memmedova - 1111111',3,'',29,1,'2025-10-16 21:34:30.404570');
INSERT INTO "django_admin_log" VALUES(140,'1522','rashad.mammadov - 1111111',3,'',29,1,'2025-10-16 21:34:30.404591');
INSERT INTO "django_admin_log" VALUES(141,'1521','rashad - 1111111',3,'',29,1,'2025-10-16 21:34:30.404612');
INSERT INTO "django_admin_log" VALUES(142,'1520','manager - 1111111',3,'',29,1,'2025-10-16 21:34:30.404633');
INSERT INTO "django_admin_log" VALUES(143,'1519','tahmaz - 1111111',3,'',29,1,'2025-10-16 21:34:30.404654');
INSERT INTO "django_admin_log" VALUES(144,'1517','nigar.hasanova - 1111111',3,'',29,1,'2025-10-16 21:34:30.404675');
INSERT INTO "django_admin_log" VALUES(145,'1516','leyla - 1111111',3,'',29,1,'2025-10-16 21:34:30.404695');
INSERT INTO "django_admin_log" VALUES(146,'1515','elchin - 1111111',3,'',29,1,'2025-10-16 21:34:30.404716');
INSERT INTO "django_admin_log" VALUES(147,'1514','employee2 - 1111111',3,'',29,1,'2025-10-16 21:34:30.404745');
INSERT INTO "django_admin_log" VALUES(148,'1513','leyla.huseynova - 1111111',3,'',29,1,'2025-10-16 21:34:30.404769');
INSERT INTO "django_admin_log" VALUES(149,'1512','sevinc.huseynli - 1111111',3,'',29,1,'2025-10-16 21:34:30.404790');
INSERT INTO "django_admin_log" VALUES(150,'1511','tural - 1111111',3,'',29,1,'2025-10-16 21:34:30.404811');
INSERT INTO "django_admin_log" VALUES(151,'1510','kamran.bashirov - 1111111',3,'',29,1,'2025-10-16 21:34:30.404832');
INSERT INTO "django_admin_log" VALUES(152,'1509','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.404855');
INSERT INTO "django_admin_log" VALUES(153,'1508','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.404876');
INSERT INTO "django_admin_log" VALUES(154,'1507','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.404897');
INSERT INTO "django_admin_log" VALUES(155,'1506','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.404917');
INSERT INTO "django_admin_log" VALUES(156,'1505','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.404938');
INSERT INTO "django_admin_log" VALUES(157,'1504','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.404959');
INSERT INTO "django_admin_log" VALUES(158,'1503','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.404979');
INSERT INTO "django_admin_log" VALUES(159,'1502','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.405000');
INSERT INTO "django_admin_log" VALUES(160,'1501','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.405021');
INSERT INTO "django_admin_log" VALUES(161,'1500','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.405041');
INSERT INTO "django_admin_log" VALUES(162,'1499','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.405064');
INSERT INTO "django_admin_log" VALUES(163,'1498','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.405085');
INSERT INTO "django_admin_log" VALUES(164,'1497','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.405106');
INSERT INTO "django_admin_log" VALUES(165,'1496','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.405127');
INSERT INTO "django_admin_log" VALUES(166,'1495','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.405147');
INSERT INTO "django_admin_log" VALUES(167,'1494','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.405168');
INSERT INTO "django_admin_log" VALUES(168,'1493','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.405197');
INSERT INTO "django_admin_log" VALUES(169,'1492','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.405220');
INSERT INTO "django_admin_log" VALUES(170,'1491','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.405242');
INSERT INTO "django_admin_log" VALUES(171,'1490','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.405262');
INSERT INTO "django_admin_log" VALUES(172,'1489','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.405283');
INSERT INTO "django_admin_log" VALUES(173,'1488','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.405304');
INSERT INTO "django_admin_log" VALUES(174,'1487','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.405329');
INSERT INTO "django_admin_log" VALUES(175,'1486','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.405350');
INSERT INTO "django_admin_log" VALUES(176,'1485','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.405371');
INSERT INTO "django_admin_log" VALUES(177,'1484','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.405393');
INSERT INTO "django_admin_log" VALUES(178,'1483','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.405414');
INSERT INTO "django_admin_log" VALUES(179,'1482','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.405434');
INSERT INTO "django_admin_log" VALUES(180,'1481','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.405455');
INSERT INTO "django_admin_log" VALUES(181,'1480','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.405475');
INSERT INTO "django_admin_log" VALUES(182,'1479','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.405496');
INSERT INTO "django_admin_log" VALUES(183,'1478','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.405516');
INSERT INTO "django_admin_log" VALUES(184,'1477','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.405537');
INSERT INTO "django_admin_log" VALUES(185,'1476','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.405558');
INSERT INTO "django_admin_log" VALUES(186,'1475','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.405578');
INSERT INTO "django_admin_log" VALUES(187,'1474','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.405599');
INSERT INTO "django_admin_log" VALUES(188,'1473','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.405620');
INSERT INTO "django_admin_log" VALUES(189,'1472','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.405649');
INSERT INTO "django_admin_log" VALUES(190,'1471','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.405671');
INSERT INTO "django_admin_log" VALUES(191,'1470','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.405692');
INSERT INTO "django_admin_log" VALUES(192,'1469','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.405714');
INSERT INTO "django_admin_log" VALUES(193,'1468','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.405735');
INSERT INTO "django_admin_log" VALUES(194,'1467','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.405756');
INSERT INTO "django_admin_log" VALUES(195,'1466','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.405779');
INSERT INTO "django_admin_log" VALUES(196,'1465','farid - 1111111',3,'',29,1,'2025-10-16 21:34:30.405800');
INSERT INTO "django_admin_log" VALUES(197,'1264','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.427922');
INSERT INTO "django_admin_log" VALUES(198,'1263','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.427974');
INSERT INTO "django_admin_log" VALUES(199,'1262','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428004');
INSERT INTO "django_admin_log" VALUES(200,'1261','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428032');
INSERT INTO "django_admin_log" VALUES(201,'1260','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428058');
INSERT INTO "django_admin_log" VALUES(202,'1259','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428083');
INSERT INTO "django_admin_log" VALUES(203,'1258','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428107');
INSERT INTO "django_admin_log" VALUES(204,'1257','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428131');
INSERT INTO "django_admin_log" VALUES(205,'1256','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428167');
INSERT INTO "django_admin_log" VALUES(206,'1255','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428191');
INSERT INTO "django_admin_log" VALUES(207,'1254','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428213');
INSERT INTO "django_admin_log" VALUES(208,'1253','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428236');
INSERT INTO "django_admin_log" VALUES(209,'1252','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428258');
INSERT INTO "django_admin_log" VALUES(210,'1251','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428280');
INSERT INTO "django_admin_log" VALUES(211,'1250','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428302');
INSERT INTO "django_admin_log" VALUES(212,'1249','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428324');
INSERT INTO "django_admin_log" VALUES(213,'1248','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428346');
INSERT INTO "django_admin_log" VALUES(214,'1247','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428368');
INSERT INTO "django_admin_log" VALUES(215,'1246','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428390');
INSERT INTO "django_admin_log" VALUES(216,'1245','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428411');
INSERT INTO "django_admin_log" VALUES(217,'1244','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428433');
INSERT INTO "django_admin_log" VALUES(218,'1243','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428455');
INSERT INTO "django_admin_log" VALUES(219,'1242','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428477');
INSERT INTO "django_admin_log" VALUES(220,'1241','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428499');
INSERT INTO "django_admin_log" VALUES(221,'1240','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428521');
INSERT INTO "django_admin_log" VALUES(222,'1239','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428545');
INSERT INTO "django_admin_log" VALUES(223,'1238','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428567');
INSERT INTO "django_admin_log" VALUES(224,'1237','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428598');
INSERT INTO "django_admin_log" VALUES(225,'1236','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428621');
INSERT INTO "django_admin_log" VALUES(226,'1235','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428643');
INSERT INTO "django_admin_log" VALUES(227,'1234','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428664');
INSERT INTO "django_admin_log" VALUES(228,'1233','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428686');
INSERT INTO "django_admin_log" VALUES(229,'1232','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428707');
INSERT INTO "django_admin_log" VALUES(230,'1231','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428729');
INSERT INTO "django_admin_log" VALUES(231,'1230','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428751');
INSERT INTO "django_admin_log" VALUES(232,'1229','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428772');
INSERT INTO "django_admin_log" VALUES(233,'1228','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428793');
INSERT INTO "django_admin_log" VALUES(234,'1227','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428815');
INSERT INTO "django_admin_log" VALUES(235,'1226','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428836');
INSERT INTO "django_admin_log" VALUES(236,'1225','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428858');
INSERT INTO "django_admin_log" VALUES(237,'1224','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428880');
INSERT INTO "django_admin_log" VALUES(238,'1223','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428902');
INSERT INTO "django_admin_log" VALUES(239,'1222','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428924');
INSERT INTO "django_admin_log" VALUES(240,'1221','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428945');
INSERT INTO "django_admin_log" VALUES(241,'1220','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428967');
INSERT INTO "django_admin_log" VALUES(242,'1219','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.428989');
INSERT INTO "django_admin_log" VALUES(243,'1218','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429011');
INSERT INTO "django_admin_log" VALUES(244,'1217','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429032');
INSERT INTO "django_admin_log" VALUES(245,'1216','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429064');
INSERT INTO "django_admin_log" VALUES(246,'1215','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429085');
INSERT INTO "django_admin_log" VALUES(247,'1214','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429106');
INSERT INTO "django_admin_log" VALUES(248,'1213','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429127');
INSERT INTO "django_admin_log" VALUES(249,'1212','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429148');
INSERT INTO "django_admin_log" VALUES(250,'1211','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429170');
INSERT INTO "django_admin_log" VALUES(251,'1210','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429191');
INSERT INTO "django_admin_log" VALUES(252,'1209','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429214');
INSERT INTO "django_admin_log" VALUES(253,'1208','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429236');
INSERT INTO "django_admin_log" VALUES(254,'1207','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429270');
INSERT INTO "django_admin_log" VALUES(255,'1206','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429292');
INSERT INTO "django_admin_log" VALUES(256,'1205','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429313');
INSERT INTO "django_admin_log" VALUES(257,'1204','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429335');
INSERT INTO "django_admin_log" VALUES(258,'1203','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429356');
INSERT INTO "django_admin_log" VALUES(259,'1202','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429376');
INSERT INTO "django_admin_log" VALUES(260,'1201','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429398');
INSERT INTO "django_admin_log" VALUES(261,'1200','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429419');
INSERT INTO "django_admin_log" VALUES(262,'1199','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429441');
INSERT INTO "django_admin_log" VALUES(263,'1198','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429462');
INSERT INTO "django_admin_log" VALUES(264,'1197','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429483');
INSERT INTO "django_admin_log" VALUES(265,'1196','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429517');
INSERT INTO "django_admin_log" VALUES(266,'1195','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429539');
INSERT INTO "django_admin_log" VALUES(267,'1194','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429560');
INSERT INTO "django_admin_log" VALUES(268,'1193','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429582');
INSERT INTO "django_admin_log" VALUES(269,'1192','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429605');
INSERT INTO "django_admin_log" VALUES(270,'1191','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429627');
INSERT INTO "django_admin_log" VALUES(271,'1190','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429649');
INSERT INTO "django_admin_log" VALUES(272,'1189','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429671');
INSERT INTO "django_admin_log" VALUES(273,'1188','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429692');
INSERT INTO "django_admin_log" VALUES(274,'1187','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429716');
INSERT INTO "django_admin_log" VALUES(275,'1186','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429739');
INSERT INTO "django_admin_log" VALUES(276,'1185','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429760');
INSERT INTO "django_admin_log" VALUES(277,'1184','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429781');
INSERT INTO "django_admin_log" VALUES(278,'1183','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429803');
INSERT INTO "django_admin_log" VALUES(279,'1182','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429824');
INSERT INTO "django_admin_log" VALUES(280,'1181','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429844');
INSERT INTO "django_admin_log" VALUES(281,'1180','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429866');
INSERT INTO "django_admin_log" VALUES(282,'1179','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429887');
INSERT INTO "django_admin_log" VALUES(283,'1178','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429908');
INSERT INTO "django_admin_log" VALUES(284,'1177','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429929');
INSERT INTO "django_admin_log" VALUES(285,'1176','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429958');
INSERT INTO "django_admin_log" VALUES(286,'1175','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.429981');
INSERT INTO "django_admin_log" VALUES(287,'1174','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.430002');
INSERT INTO "django_admin_log" VALUES(288,'1173','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.430024');
INSERT INTO "django_admin_log" VALUES(289,'1172','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.430045');
INSERT INTO "django_admin_log" VALUES(290,'1171','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.430067');
INSERT INTO "django_admin_log" VALUES(291,'1170','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.430088');
INSERT INTO "django_admin_log" VALUES(292,'1169','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.430110');
INSERT INTO "django_admin_log" VALUES(293,'1168','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.430130');
INSERT INTO "django_admin_log" VALUES(294,'1167','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.430151');
INSERT INTO "django_admin_log" VALUES(295,'1166','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.430172');
INSERT INTO "django_admin_log" VALUES(296,'1165','farid - 1111111',3,'',29,1,'2025-10-16 21:35:07.430194');
INSERT INTO "django_admin_log" VALUES(297,'1164','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.050243');
INSERT INTO "django_admin_log" VALUES(298,'1163','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.050297');
INSERT INTO "django_admin_log" VALUES(299,'1162','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.050328');
INSERT INTO "django_admin_log" VALUES(300,'1161','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.050356');
INSERT INTO "django_admin_log" VALUES(301,'1160','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.050381');
INSERT INTO "django_admin_log" VALUES(302,'1159','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.050407');
INSERT INTO "django_admin_log" VALUES(303,'1158','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.050431');
INSERT INTO "django_admin_log" VALUES(304,'1157','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.050454');
INSERT INTO "django_admin_log" VALUES(305,'1156','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.050477');
INSERT INTO "django_admin_log" VALUES(306,'1155','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.050501');
INSERT INTO "django_admin_log" VALUES(307,'1154','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.050577');
INSERT INTO "django_admin_log" VALUES(308,'1153','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.050618');
INSERT INTO "django_admin_log" VALUES(309,'1152','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.050644');
INSERT INTO "django_admin_log" VALUES(310,'1151','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.050668');
INSERT INTO "django_admin_log" VALUES(311,'1150','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.050693');
INSERT INTO "django_admin_log" VALUES(312,'1149','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.050717');
INSERT INTO "django_admin_log" VALUES(313,'1148','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.050742');
INSERT INTO "django_admin_log" VALUES(314,'1147','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.050764');
INSERT INTO "django_admin_log" VALUES(315,'1146','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.050789');
INSERT INTO "django_admin_log" VALUES(316,'1145','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.050811');
INSERT INTO "django_admin_log" VALUES(317,'1144','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.050834');
INSERT INTO "django_admin_log" VALUES(318,'1143','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.050857');
INSERT INTO "django_admin_log" VALUES(319,'1142','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.050880');
INSERT INTO "django_admin_log" VALUES(320,'1141','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.050904');
INSERT INTO "django_admin_log" VALUES(321,'1140','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.050927');
INSERT INTO "django_admin_log" VALUES(322,'1139','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.050950');
INSERT INTO "django_admin_log" VALUES(323,'1138','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.050973');
INSERT INTO "django_admin_log" VALUES(324,'1137','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.050996');
INSERT INTO "django_admin_log" VALUES(325,'1136','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051019');
INSERT INTO "django_admin_log" VALUES(326,'1135','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051042');
INSERT INTO "django_admin_log" VALUES(327,'1134','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051064');
INSERT INTO "django_admin_log" VALUES(328,'1133','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051088');
INSERT INTO "django_admin_log" VALUES(329,'1132','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051112');
INSERT INTO "django_admin_log" VALUES(330,'1131','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051135');
INSERT INTO "django_admin_log" VALUES(331,'1130','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051156');
INSERT INTO "django_admin_log" VALUES(332,'1129','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051178');
INSERT INTO "django_admin_log" VALUES(333,'1128','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051202');
INSERT INTO "django_admin_log" VALUES(334,'1127','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051225');
INSERT INTO "django_admin_log" VALUES(335,'1126','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051247');
INSERT INTO "django_admin_log" VALUES(336,'1125','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051269');
INSERT INTO "django_admin_log" VALUES(337,'1124','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051293');
INSERT INTO "django_admin_log" VALUES(338,'1123','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051316');
INSERT INTO "django_admin_log" VALUES(339,'1122','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051341');
INSERT INTO "django_admin_log" VALUES(340,'1121','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051364');
INSERT INTO "django_admin_log" VALUES(341,'1120','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051387');
INSERT INTO "django_admin_log" VALUES(342,'1119','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051426');
INSERT INTO "django_admin_log" VALUES(343,'1118','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051449');
INSERT INTO "django_admin_log" VALUES(344,'1117','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051472');
INSERT INTO "django_admin_log" VALUES(345,'1116','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051495');
INSERT INTO "django_admin_log" VALUES(346,'1115','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051519');
INSERT INTO "django_admin_log" VALUES(347,'1114','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051541');
INSERT INTO "django_admin_log" VALUES(348,'1113','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051564');
INSERT INTO "django_admin_log" VALUES(349,'1112','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051587');
INSERT INTO "django_admin_log" VALUES(350,'1111','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051611');
INSERT INTO "django_admin_log" VALUES(351,'1110','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051634');
INSERT INTO "django_admin_log" VALUES(352,'1109','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051658');
INSERT INTO "django_admin_log" VALUES(353,'1108','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051681');
INSERT INTO "django_admin_log" VALUES(354,'1107','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051704');
INSERT INTO "django_admin_log" VALUES(355,'1106','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051728');
INSERT INTO "django_admin_log" VALUES(356,'1105','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051750');
INSERT INTO "django_admin_log" VALUES(357,'1104','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051772');
INSERT INTO "django_admin_log" VALUES(358,'1103','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051794');
INSERT INTO "django_admin_log" VALUES(359,'1102','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051817');
INSERT INTO "django_admin_log" VALUES(360,'1101','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051838');
INSERT INTO "django_admin_log" VALUES(361,'1100','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051874');
INSERT INTO "django_admin_log" VALUES(362,'1099','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051899');
INSERT INTO "django_admin_log" VALUES(363,'1098','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051922');
INSERT INTO "django_admin_log" VALUES(364,'1097','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051944');
INSERT INTO "django_admin_log" VALUES(365,'1096','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051966');
INSERT INTO "django_admin_log" VALUES(366,'1095','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.051988');
INSERT INTO "django_admin_log" VALUES(367,'1094','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.052010');
INSERT INTO "django_admin_log" VALUES(368,'1093','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.052033');
INSERT INTO "django_admin_log" VALUES(369,'1092','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.052055');
INSERT INTO "django_admin_log" VALUES(370,'1091','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.052076');
INSERT INTO "django_admin_log" VALUES(371,'1090','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.052098');
INSERT INTO "django_admin_log" VALUES(372,'1089','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.052121');
INSERT INTO "django_admin_log" VALUES(373,'1088','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.052144');
INSERT INTO "django_admin_log" VALUES(374,'1087','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.052168');
INSERT INTO "django_admin_log" VALUES(375,'1086','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.052189');
INSERT INTO "django_admin_log" VALUES(376,'1085','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.052211');
INSERT INTO "django_admin_log" VALUES(377,'1084','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.052233');
INSERT INTO "django_admin_log" VALUES(378,'1083','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.052257');
INSERT INTO "django_admin_log" VALUES(379,'1082','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.052280');
INSERT INTO "django_admin_log" VALUES(380,'1081','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.052302');
INSERT INTO "django_admin_log" VALUES(381,'1080','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.052335');
INSERT INTO "django_admin_log" VALUES(382,'1079','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.052358');
INSERT INTO "django_admin_log" VALUES(383,'1078','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.052379');
INSERT INTO "django_admin_log" VALUES(384,'1077','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.052401');
INSERT INTO "django_admin_log" VALUES(385,'1076','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.052422');
INSERT INTO "django_admin_log" VALUES(386,'1075','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.052445');
INSERT INTO "django_admin_log" VALUES(387,'1074','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.052469');
INSERT INTO "django_admin_log" VALUES(388,'1073','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.052491');
INSERT INTO "django_admin_log" VALUES(389,'1072','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.052514');
INSERT INTO "django_admin_log" VALUES(390,'1071','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.052622');
INSERT INTO "django_admin_log" VALUES(391,'1070','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.052659');
INSERT INTO "django_admin_log" VALUES(392,'1069','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.052684');
INSERT INTO "django_admin_log" VALUES(393,'1068','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.052709');
INSERT INTO "django_admin_log" VALUES(394,'1067','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.052734');
INSERT INTO "django_admin_log" VALUES(395,'1066','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.052758');
INSERT INTO "django_admin_log" VALUES(396,'1065','farid - 1111111',3,'',29,1,'2025-10-16 21:35:18.052782');
INSERT INTO "django_admin_log" VALUES(397,'1064','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.722964');
INSERT INTO "django_admin_log" VALUES(398,'1063','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723007');
INSERT INTO "django_admin_log" VALUES(399,'1062','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723036');
INSERT INTO "django_admin_log" VALUES(400,'1061','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723062');
INSERT INTO "django_admin_log" VALUES(401,'1060','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723087');
INSERT INTO "django_admin_log" VALUES(402,'1059','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723111');
INSERT INTO "django_admin_log" VALUES(403,'1058','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723134');
INSERT INTO "django_admin_log" VALUES(404,'1057','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723156');
INSERT INTO "django_admin_log" VALUES(405,'1056','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723178');
INSERT INTO "django_admin_log" VALUES(406,'1055','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723200');
INSERT INTO "django_admin_log" VALUES(407,'1054','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723221');
INSERT INTO "django_admin_log" VALUES(408,'1053','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723243');
INSERT INTO "django_admin_log" VALUES(409,'1052','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723264');
INSERT INTO "django_admin_log" VALUES(410,'1051','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723285');
INSERT INTO "django_admin_log" VALUES(411,'1050','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723316');
INSERT INTO "django_admin_log" VALUES(412,'1049','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723338');
INSERT INTO "django_admin_log" VALUES(413,'1048','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723359');
INSERT INTO "django_admin_log" VALUES(414,'1047','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723389');
INSERT INTO "django_admin_log" VALUES(415,'1046','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723411');
INSERT INTO "django_admin_log" VALUES(416,'1045','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723432');
INSERT INTO "django_admin_log" VALUES(417,'1044','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723453');
INSERT INTO "django_admin_log" VALUES(418,'1043','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723474');
INSERT INTO "django_admin_log" VALUES(419,'1042','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723495');
INSERT INTO "django_admin_log" VALUES(420,'1041','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723516');
INSERT INTO "django_admin_log" VALUES(421,'1040','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723537');
INSERT INTO "django_admin_log" VALUES(422,'1039','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723558');
INSERT INTO "django_admin_log" VALUES(423,'1038','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723579');
INSERT INTO "django_admin_log" VALUES(424,'1037','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723600');
INSERT INTO "django_admin_log" VALUES(425,'1036','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723621');
INSERT INTO "django_admin_log" VALUES(426,'1035','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723642');
INSERT INTO "django_admin_log" VALUES(427,'1034','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723663');
INSERT INTO "django_admin_log" VALUES(428,'1033','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723684');
INSERT INTO "django_admin_log" VALUES(429,'1032','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723705');
INSERT INTO "django_admin_log" VALUES(430,'1031','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723726');
INSERT INTO "django_admin_log" VALUES(431,'1030','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723747');
INSERT INTO "django_admin_log" VALUES(432,'1029','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723776');
INSERT INTO "django_admin_log" VALUES(433,'1028','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723797');
INSERT INTO "django_admin_log" VALUES(434,'1027','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723819');
INSERT INTO "django_admin_log" VALUES(435,'1026','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723839');
INSERT INTO "django_admin_log" VALUES(436,'1025','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723861');
INSERT INTO "django_admin_log" VALUES(437,'1024','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723882');
INSERT INTO "django_admin_log" VALUES(438,'1023','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723904');
INSERT INTO "django_admin_log" VALUES(439,'1022','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723926');
INSERT INTO "django_admin_log" VALUES(440,'1021','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723947');
INSERT INTO "django_admin_log" VALUES(441,'1020','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723969');
INSERT INTO "django_admin_log" VALUES(442,'1019','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.723990');
INSERT INTO "django_admin_log" VALUES(443,'1018','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724011');
INSERT INTO "django_admin_log" VALUES(444,'1017','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724032');
INSERT INTO "django_admin_log" VALUES(445,'1016','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724053');
INSERT INTO "django_admin_log" VALUES(446,'1015','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724074');
INSERT INTO "django_admin_log" VALUES(447,'1014','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724095');
INSERT INTO "django_admin_log" VALUES(448,'1013','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724117');
INSERT INTO "django_admin_log" VALUES(449,'1012','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724139');
INSERT INTO "django_admin_log" VALUES(450,'1011','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724161');
INSERT INTO "django_admin_log" VALUES(451,'1010','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724182');
INSERT INTO "django_admin_log" VALUES(452,'1009','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724203');
INSERT INTO "django_admin_log" VALUES(453,'1008','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724233');
INSERT INTO "django_admin_log" VALUES(454,'1007','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724254');
INSERT INTO "django_admin_log" VALUES(455,'1006','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724275');
INSERT INTO "django_admin_log" VALUES(456,'1005','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724296');
INSERT INTO "django_admin_log" VALUES(457,'1004','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724317');
INSERT INTO "django_admin_log" VALUES(458,'1003','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724339');
INSERT INTO "django_admin_log" VALUES(459,'1002','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724360');
INSERT INTO "django_admin_log" VALUES(460,'1001','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724381');
INSERT INTO "django_admin_log" VALUES(461,'1000','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724403');
INSERT INTO "django_admin_log" VALUES(462,'999','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724424');
INSERT INTO "django_admin_log" VALUES(463,'998','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724446');
INSERT INTO "django_admin_log" VALUES(464,'997','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724466');
INSERT INTO "django_admin_log" VALUES(465,'996','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724487');
INSERT INTO "django_admin_log" VALUES(466,'995','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724508');
INSERT INTO "django_admin_log" VALUES(467,'994','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724529');
INSERT INTO "django_admin_log" VALUES(468,'993','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724550');
INSERT INTO "django_admin_log" VALUES(469,'992','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724571');
INSERT INTO "django_admin_log" VALUES(470,'991','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724592');
INSERT INTO "django_admin_log" VALUES(471,'990','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724613');
INSERT INTO "django_admin_log" VALUES(472,'989','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724634');
INSERT INTO "django_admin_log" VALUES(473,'988','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724662');
INSERT INTO "django_admin_log" VALUES(474,'987','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724684');
INSERT INTO "django_admin_log" VALUES(475,'986','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724706');
INSERT INTO "django_admin_log" VALUES(476,'985','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724728');
INSERT INTO "django_admin_log" VALUES(477,'984','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724750');
INSERT INTO "django_admin_log" VALUES(478,'983','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724771');
INSERT INTO "django_admin_log" VALUES(479,'982','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724792');
INSERT INTO "django_admin_log" VALUES(480,'981','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724813');
INSERT INTO "django_admin_log" VALUES(481,'980','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724834');
INSERT INTO "django_admin_log" VALUES(482,'979','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724855');
INSERT INTO "django_admin_log" VALUES(483,'978','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724876');
INSERT INTO "django_admin_log" VALUES(484,'977','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724896');
INSERT INTO "django_admin_log" VALUES(485,'976','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724917');
INSERT INTO "django_admin_log" VALUES(486,'975','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724938');
INSERT INTO "django_admin_log" VALUES(487,'974','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724959');
INSERT INTO "django_admin_log" VALUES(488,'973','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.724980');
INSERT INTO "django_admin_log" VALUES(489,'972','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.725001');
INSERT INTO "django_admin_log" VALUES(490,'971','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.725023');
INSERT INTO "django_admin_log" VALUES(491,'970','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.725043');
INSERT INTO "django_admin_log" VALUES(492,'969','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.725064');
INSERT INTO "django_admin_log" VALUES(493,'968','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.725085');
INSERT INTO "django_admin_log" VALUES(494,'967','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.725113');
INSERT INTO "django_admin_log" VALUES(495,'966','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.725135');
INSERT INTO "django_admin_log" VALUES(496,'965','farid - 1111111',3,'',29,1,'2025-10-16 21:35:26.725156');
INSERT INTO "django_admin_log" VALUES(497,'964','farid - 1111111',3,'',29,1,'2025-10-16 21:36:13.833351');
INSERT INTO "django_admin_log" VALUES(498,'963','farid - 1111111',3,'',29,1,'2025-10-16 21:36:13.833394');
INSERT INTO "django_admin_log" VALUES(499,'962','farid - 1111111',3,'',29,1,'2025-10-16 21:36:13.833422');
INSERT INTO "django_admin_log" VALUES(500,'961','farid - 1111111',3,'',29,1,'2025-10-16 21:36:13.833448');
INSERT INTO "django_admin_log" VALUES(501,'960','farid - 1111111',3,'',29,1,'2025-10-16 21:36:13.833473');
INSERT INTO "django_admin_log" VALUES(502,'959','farid - 1111111',3,'',29,1,'2025-10-16 21:36:13.833497');
INSERT INTO "django_admin_log" VALUES(503,'958','farid - 1111111',3,'',29,1,'2025-10-16 21:36:13.833520');
INSERT INTO "django_admin_log" VALUES(504,'957','farid - 1111111',3,'',29,1,'2025-10-16 21:36:13.833542');
INSERT INTO "django_admin_log" VALUES(505,'956','farid - 1111111',3,'',29,1,'2025-10-16 21:36:13.833564');
INSERT INTO "django_admin_log" VALUES(506,'955','farid - 1111111',3,'',29,1,'2025-10-16 21:36:13.833586');
INSERT INTO "django_admin_log" VALUES(507,'954','farid - 1111111',3,'',29,1,'2025-10-16 21:36:13.833618');
INSERT INTO "django_admin_log" VALUES(508,'953','farid - 1111111',3,'',29,1,'2025-10-16 21:36:13.833640');
INSERT INTO "django_admin_log" VALUES(509,'952','farid - 1111111',3,'',29,1,'2025-10-16 21:36:13.833661');
INSERT INTO "django_admin_log" VALUES(510,'951','farid - 1111111',3,'',29,1,'2025-10-16 21:36:13.833682');
INSERT INTO "django_admin_log" VALUES(511,'950','farid - 1111111',3,'',29,1,'2025-10-16 21:36:13.833704');
INSERT INTO "django_admin_log" VALUES(512,'949','farid - 1111111',3,'',29,1,'2025-10-16 21:36:13.833726');
INSERT INTO "django_admin_log" VALUES(513,'948','farid - 1111111',3,'',29,1,'2025-10-16 21:36:13.833747');
INSERT INTO "django_admin_log" VALUES(514,'947','farid - 1111111',3,'',29,1,'2025-10-16 21:36:13.833768');
INSERT INTO "django_admin_log" VALUES(515,'946','farid - 1111111',3,'',29,1,'2025-10-16 21:36:13.833790');
INSERT INTO "django_admin_log" VALUES(516,'945','farid - 1111111',3,'',29,1,'2025-10-16 21:36:13.833811');
INSERT INTO "django_admin_log" VALUES(517,'944','farid - 1111111',3,'',29,1,'2025-10-16 21:36:13.833831');
INSERT INTO "django_admin_log" VALUES(518,'943','farid - 1111111',3,'',29,1,'2025-10-16 21:36:13.833852');
INSERT INTO "django_admin_log" VALUES(519,'942','farid - 1111111',3,'',29,1,'2025-10-16 21:36:13.833873');
INSERT INTO "django_admin_log" VALUES(520,'941','farid - 1111111',3,'',29,1,'2025-10-16 21:36:13.833894');
INSERT INTO "django_admin_log" VALUES(521,'940','farid - 1111111',3,'',29,1,'2025-10-16 21:36:13.833914');
INSERT INTO "django_admin_log" VALUES(522,'939','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.833936');
INSERT INTO "django_admin_log" VALUES(523,'938','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.833957');
INSERT INTO "django_admin_log" VALUES(524,'937','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.833977');
INSERT INTO "django_admin_log" VALUES(525,'936','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.833998');
INSERT INTO "django_admin_log" VALUES(526,'935','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834019');
INSERT INTO "django_admin_log" VALUES(527,'934','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834040');
INSERT INTO "django_admin_log" VALUES(528,'933','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834068');
INSERT INTO "django_admin_log" VALUES(529,'932','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834090');
INSERT INTO "django_admin_log" VALUES(530,'931','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834112');
INSERT INTO "django_admin_log" VALUES(531,'930','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834133');
INSERT INTO "django_admin_log" VALUES(532,'929','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834154');
INSERT INTO "django_admin_log" VALUES(533,'928','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834175');
INSERT INTO "django_admin_log" VALUES(534,'927','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834196');
INSERT INTO "django_admin_log" VALUES(535,'926','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834217');
INSERT INTO "django_admin_log" VALUES(536,'925','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834237');
INSERT INTO "django_admin_log" VALUES(537,'924','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834259');
INSERT INTO "django_admin_log" VALUES(538,'923','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834280');
INSERT INTO "django_admin_log" VALUES(539,'922','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834301');
INSERT INTO "django_admin_log" VALUES(540,'921','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834323');
INSERT INTO "django_admin_log" VALUES(541,'920','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834344');
INSERT INTO "django_admin_log" VALUES(542,'919','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834365');
INSERT INTO "django_admin_log" VALUES(543,'918','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834386');
INSERT INTO "django_admin_log" VALUES(544,'917','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834408');
INSERT INTO "django_admin_log" VALUES(545,'916','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834429');
INSERT INTO "django_admin_log" VALUES(546,'915','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834450');
INSERT INTO "django_admin_log" VALUES(547,'914','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834470');
INSERT INTO "django_admin_log" VALUES(548,'913','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834492');
INSERT INTO "django_admin_log" VALUES(549,'912','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834521');
INSERT INTO "django_admin_log" VALUES(550,'911','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834543');
INSERT INTO "django_admin_log" VALUES(551,'910','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834564');
INSERT INTO "django_admin_log" VALUES(552,'909','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834585');
INSERT INTO "django_admin_log" VALUES(553,'908','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834606');
INSERT INTO "django_admin_log" VALUES(554,'907','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834627');
INSERT INTO "django_admin_log" VALUES(555,'906','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834648');
INSERT INTO "django_admin_log" VALUES(556,'905','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834669');
INSERT INTO "django_admin_log" VALUES(557,'904','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834690');
INSERT INTO "django_admin_log" VALUES(558,'903','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834710');
INSERT INTO "django_admin_log" VALUES(559,'902','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834731');
INSERT INTO "django_admin_log" VALUES(560,'901','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834752');
INSERT INTO "django_admin_log" VALUES(561,'900','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834772');
INSERT INTO "django_admin_log" VALUES(562,'899','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834794');
INSERT INTO "django_admin_log" VALUES(563,'898','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834815');
INSERT INTO "django_admin_log" VALUES(564,'897','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834835');
INSERT INTO "django_admin_log" VALUES(565,'896','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834856');
INSERT INTO "django_admin_log" VALUES(566,'895','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834877');
INSERT INTO "django_admin_log" VALUES(567,'894','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834898');
INSERT INTO "django_admin_log" VALUES(568,'893','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834919');
INSERT INTO "django_admin_log" VALUES(569,'892','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834940');
INSERT INTO "django_admin_log" VALUES(570,'891','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834969');
INSERT INTO "django_admin_log" VALUES(571,'890','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.834990');
INSERT INTO "django_admin_log" VALUES(572,'889','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.835011');
INSERT INTO "django_admin_log" VALUES(573,'888','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.835032');
INSERT INTO "django_admin_log" VALUES(574,'887','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.835062');
INSERT INTO "django_admin_log" VALUES(575,'886','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.835084');
INSERT INTO "django_admin_log" VALUES(576,'885','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.835104');
INSERT INTO "django_admin_log" VALUES(577,'884','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.835125');
INSERT INTO "django_admin_log" VALUES(578,'883','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.835146');
INSERT INTO "django_admin_log" VALUES(579,'882','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.835166');
INSERT INTO "django_admin_log" VALUES(580,'881','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.835188');
INSERT INTO "django_admin_log" VALUES(581,'880','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.835208');
INSERT INTO "django_admin_log" VALUES(582,'879','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.835229');
INSERT INTO "django_admin_log" VALUES(583,'878','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.835250');
INSERT INTO "django_admin_log" VALUES(584,'877','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.835271');
INSERT INTO "django_admin_log" VALUES(585,'876','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.835293');
INSERT INTO "django_admin_log" VALUES(586,'875','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.835314');
INSERT INTO "django_admin_log" VALUES(587,'874','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.835335');
INSERT INTO "django_admin_log" VALUES(588,'873','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.835355');
INSERT INTO "django_admin_log" VALUES(589,'872','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.835388');
INSERT INTO "django_admin_log" VALUES(590,'871','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.835418');
INSERT INTO "django_admin_log" VALUES(591,'870','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.835440');
INSERT INTO "django_admin_log" VALUES(592,'869','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.835466');
INSERT INTO "django_admin_log" VALUES(593,'868','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.835488');
INSERT INTO "django_admin_log" VALUES(594,'867','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.835509');
INSERT INTO "django_admin_log" VALUES(595,'866','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.835530');
INSERT INTO "django_admin_log" VALUES(596,'865','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:36:13.835553');
INSERT INTO "django_admin_log" VALUES(597,'764','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:37:08.440732');
INSERT INTO "django_admin_log" VALUES(598,'763','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:37:08.440777');
INSERT INTO "django_admin_log" VALUES(599,'762','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:37:08.440803');
INSERT INTO "django_admin_log" VALUES(600,'761','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:37:08.440826');
INSERT INTO "django_admin_log" VALUES(601,'760','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:37:08.440847');
INSERT INTO "django_admin_log" VALUES(602,'759','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:37:08.440870');
INSERT INTO "django_admin_log" VALUES(603,'758','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:37:08.440892');
INSERT INTO "django_admin_log" VALUES(604,'757','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:37:08.440913');
INSERT INTO "django_admin_log" VALUES(605,'756','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:37:08.440934');
INSERT INTO "django_admin_log" VALUES(606,'755','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:37:08.440955');
INSERT INTO "django_admin_log" VALUES(607,'754','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:37:08.440976');
INSERT INTO "django_admin_log" VALUES(608,'753','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:37:08.440997');
INSERT INTO "django_admin_log" VALUES(609,'752','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:37:08.441018');
INSERT INTO "django_admin_log" VALUES(610,'751','farid - azərbaycan ',3,'',29,1,'2025-10-16 21:37:08.441039');
INSERT INTO "django_admin_log" VALUES(611,'750','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441060');
INSERT INTO "django_admin_log" VALUES(612,'749','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441081');
INSERT INTO "django_admin_log" VALUES(613,'748','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441102');
INSERT INTO "django_admin_log" VALUES(614,'747','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441123');
INSERT INTO "django_admin_log" VALUES(615,'746','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441144');
INSERT INTO "django_admin_log" VALUES(616,'745','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441166');
INSERT INTO "django_admin_log" VALUES(617,'744','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441187');
INSERT INTO "django_admin_log" VALUES(618,'743','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441207');
INSERT INTO "django_admin_log" VALUES(619,'742','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441228');
INSERT INTO "django_admin_log" VALUES(620,'741','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441250');
INSERT INTO "django_admin_log" VALUES(621,'740','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441270');
INSERT INTO "django_admin_log" VALUES(622,'739','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441291');
INSERT INTO "django_admin_log" VALUES(623,'738','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441311');
INSERT INTO "django_admin_log" VALUES(624,'737','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441332');
INSERT INTO "django_admin_log" VALUES(625,'736','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441352');
INSERT INTO "django_admin_log" VALUES(626,'735','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441373');
INSERT INTO "django_admin_log" VALUES(627,'734','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441393');
INSERT INTO "django_admin_log" VALUES(628,'733','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441414');
INSERT INTO "django_admin_log" VALUES(629,'732','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441434');
INSERT INTO "django_admin_log" VALUES(630,'731','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441454');
INSERT INTO "django_admin_log" VALUES(631,'730','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441475');
INSERT INTO "django_admin_log" VALUES(632,'729','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441495');
INSERT INTO "django_admin_log" VALUES(633,'728','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441516');
INSERT INTO "django_admin_log" VALUES(634,'727','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441536');
INSERT INTO "django_admin_log" VALUES(635,'726','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441557');
INSERT INTO "django_admin_log" VALUES(636,'725','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441578');
INSERT INTO "django_admin_log" VALUES(637,'724','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441599');
INSERT INTO "django_admin_log" VALUES(638,'723','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441620');
INSERT INTO "django_admin_log" VALUES(639,'722','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441641');
INSERT INTO "django_admin_log" VALUES(640,'721','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441662');
INSERT INTO "django_admin_log" VALUES(641,'720','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441683');
INSERT INTO "django_admin_log" VALUES(642,'719','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441704');
INSERT INTO "django_admin_log" VALUES(643,'718','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441724');
INSERT INTO "django_admin_log" VALUES(644,'717','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441745');
INSERT INTO "django_admin_log" VALUES(645,'716','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441765');
INSERT INTO "django_admin_log" VALUES(646,'715','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441785');
INSERT INTO "django_admin_log" VALUES(647,'714','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441805');
INSERT INTO "django_admin_log" VALUES(648,'713','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441825');
INSERT INTO "django_admin_log" VALUES(649,'712','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441846');
INSERT INTO "django_admin_log" VALUES(650,'711','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441867');
INSERT INTO "django_admin_log" VALUES(651,'710','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441887');
INSERT INTO "django_admin_log" VALUES(652,'709','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441908');
INSERT INTO "django_admin_log" VALUES(653,'708','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441929');
INSERT INTO "django_admin_log" VALUES(654,'707','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.441949');
INSERT INTO "django_admin_log" VALUES(655,'706','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.442580');
INSERT INTO "django_admin_log" VALUES(656,'705','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.442614');
INSERT INTO "django_admin_log" VALUES(657,'704','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.442637');
INSERT INTO "django_admin_log" VALUES(658,'703','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.442659');
INSERT INTO "django_admin_log" VALUES(659,'702','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.442681');
INSERT INTO "django_admin_log" VALUES(660,'701','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.442703');
INSERT INTO "django_admin_log" VALUES(661,'700','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.442724');
INSERT INTO "django_admin_log" VALUES(662,'699','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.442746');
INSERT INTO "django_admin_log" VALUES(663,'698','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.442767');
INSERT INTO "django_admin_log" VALUES(664,'697','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.442787');
INSERT INTO "django_admin_log" VALUES(665,'696','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.442808');
INSERT INTO "django_admin_log" VALUES(666,'695','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.442828');
INSERT INTO "django_admin_log" VALUES(667,'694','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.442849');
INSERT INTO "django_admin_log" VALUES(668,'693','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.442870');
INSERT INTO "django_admin_log" VALUES(669,'692','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.442890');
INSERT INTO "django_admin_log" VALUES(670,'691','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.442911');
INSERT INTO "django_admin_log" VALUES(671,'690','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.442932');
INSERT INTO "django_admin_log" VALUES(672,'689','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.442953');
INSERT INTO "django_admin_log" VALUES(673,'688','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.442973');
INSERT INTO "django_admin_log" VALUES(674,'687','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.442996');
INSERT INTO "django_admin_log" VALUES(675,'686','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.443016');
INSERT INTO "django_admin_log" VALUES(676,'685','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.443037');
INSERT INTO "django_admin_log" VALUES(677,'684','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.443058');
INSERT INTO "django_admin_log" VALUES(678,'683','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.443078');
INSERT INTO "django_admin_log" VALUES(679,'682','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.443098');
INSERT INTO "django_admin_log" VALUES(680,'681','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.443119');
INSERT INTO "django_admin_log" VALUES(681,'680','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.443139');
INSERT INTO "django_admin_log" VALUES(682,'679','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.443159');
INSERT INTO "django_admin_log" VALUES(683,'678','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.443180');
INSERT INTO "django_admin_log" VALUES(684,'677','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.443200');
INSERT INTO "django_admin_log" VALUES(685,'676','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.443220');
INSERT INTO "django_admin_log" VALUES(686,'675','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.443240');
INSERT INTO "django_admin_log" VALUES(687,'674','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.443261');
INSERT INTO "django_admin_log" VALUES(688,'673','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.443281');
INSERT INTO "django_admin_log" VALUES(689,'672','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.443301');
INSERT INTO "django_admin_log" VALUES(690,'671','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.443322');
INSERT INTO "django_admin_log" VALUES(691,'670','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.443342');
INSERT INTO "django_admin_log" VALUES(692,'669','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.443362');
INSERT INTO "django_admin_log" VALUES(693,'668','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.443383');
INSERT INTO "django_admin_log" VALUES(694,'667','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.443403');
INSERT INTO "django_admin_log" VALUES(695,'666','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.443423');
INSERT INTO "django_admin_log" VALUES(696,'665','farid - 55555555',3,'',29,1,'2025-10-16 21:37:08.443443');
INSERT INTO "django_admin_log" VALUES(697,'664','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.526886');
INSERT INTO "django_admin_log" VALUES(698,'663','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.526935');
INSERT INTO "django_admin_log" VALUES(699,'662','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.526963');
INSERT INTO "django_admin_log" VALUES(700,'661','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.526989');
INSERT INTO "django_admin_log" VALUES(701,'660','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527013');
INSERT INTO "django_admin_log" VALUES(702,'659','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527045');
INSERT INTO "django_admin_log" VALUES(703,'658','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527069');
INSERT INTO "django_admin_log" VALUES(704,'657','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527091');
INSERT INTO "django_admin_log" VALUES(705,'656','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527113');
INSERT INTO "django_admin_log" VALUES(706,'655','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527136');
INSERT INTO "django_admin_log" VALUES(707,'654','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527158');
INSERT INTO "django_admin_log" VALUES(708,'653','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527187');
INSERT INTO "django_admin_log" VALUES(709,'652','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527211');
INSERT INTO "django_admin_log" VALUES(710,'651','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527233');
INSERT INTO "django_admin_log" VALUES(711,'650','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527255');
INSERT INTO "django_admin_log" VALUES(712,'649','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527277');
INSERT INTO "django_admin_log" VALUES(713,'648','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527298');
INSERT INTO "django_admin_log" VALUES(714,'647','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527321');
INSERT INTO "django_admin_log" VALUES(715,'646','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527342');
INSERT INTO "django_admin_log" VALUES(716,'645','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527364');
INSERT INTO "django_admin_log" VALUES(717,'644','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527386');
INSERT INTO "django_admin_log" VALUES(718,'643','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527407');
INSERT INTO "django_admin_log" VALUES(719,'642','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527429');
INSERT INTO "django_admin_log" VALUES(720,'641','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527450');
INSERT INTO "django_admin_log" VALUES(721,'640','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527471');
INSERT INTO "django_admin_log" VALUES(722,'639','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527493');
INSERT INTO "django_admin_log" VALUES(723,'638','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527514');
INSERT INTO "django_admin_log" VALUES(724,'637','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527535');
INSERT INTO "django_admin_log" VALUES(725,'636','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527557');
INSERT INTO "django_admin_log" VALUES(726,'635','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527578');
INSERT INTO "django_admin_log" VALUES(727,'634','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527599');
INSERT INTO "django_admin_log" VALUES(728,'633','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527620');
INSERT INTO "django_admin_log" VALUES(729,'632','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527649');
INSERT INTO "django_admin_log" VALUES(730,'631','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527671');
INSERT INTO "django_admin_log" VALUES(731,'630','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527693');
INSERT INTO "django_admin_log" VALUES(732,'629','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527714');
INSERT INTO "django_admin_log" VALUES(733,'628','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527736');
INSERT INTO "django_admin_log" VALUES(734,'627','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527757');
INSERT INTO "django_admin_log" VALUES(735,'626','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527778');
INSERT INTO "django_admin_log" VALUES(736,'625','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527799');
INSERT INTO "django_admin_log" VALUES(737,'624','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527821');
INSERT INTO "django_admin_log" VALUES(738,'623','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527843');
INSERT INTO "django_admin_log" VALUES(739,'622','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527864');
INSERT INTO "django_admin_log" VALUES(740,'621','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527885');
INSERT INTO "django_admin_log" VALUES(741,'620','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527907');
INSERT INTO "django_admin_log" VALUES(742,'619','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527928');
INSERT INTO "django_admin_log" VALUES(743,'618','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527949');
INSERT INTO "django_admin_log" VALUES(744,'617','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527970');
INSERT INTO "django_admin_log" VALUES(745,'616','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.527991');
INSERT INTO "django_admin_log" VALUES(746,'615','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528013');
INSERT INTO "django_admin_log" VALUES(747,'614','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528034');
INSERT INTO "django_admin_log" VALUES(748,'613','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528055');
INSERT INTO "django_admin_log" VALUES(749,'612','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528077');
INSERT INTO "django_admin_log" VALUES(750,'611','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528106');
INSERT INTO "django_admin_log" VALUES(751,'610','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528127');
INSERT INTO "django_admin_log" VALUES(752,'609','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528149');
INSERT INTO "django_admin_log" VALUES(753,'608','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528174');
INSERT INTO "django_admin_log" VALUES(754,'607','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528195');
INSERT INTO "django_admin_log" VALUES(755,'606','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528216');
INSERT INTO "django_admin_log" VALUES(756,'605','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528237');
INSERT INTO "django_admin_log" VALUES(757,'604','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528258');
INSERT INTO "django_admin_log" VALUES(758,'603','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528279');
INSERT INTO "django_admin_log" VALUES(759,'602','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528300');
INSERT INTO "django_admin_log" VALUES(760,'601','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528321');
INSERT INTO "django_admin_log" VALUES(761,'600','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528341');
INSERT INTO "django_admin_log" VALUES(762,'599','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528363');
INSERT INTO "django_admin_log" VALUES(763,'598','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528384');
INSERT INTO "django_admin_log" VALUES(764,'597','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528405');
INSERT INTO "django_admin_log" VALUES(765,'596','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528426');
INSERT INTO "django_admin_log" VALUES(766,'595','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528447');
INSERT INTO "django_admin_log" VALUES(767,'594','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528468');
INSERT INTO "django_admin_log" VALUES(768,'593','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528489');
INSERT INTO "django_admin_log" VALUES(769,'592','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528509');
INSERT INTO "django_admin_log" VALUES(770,'591','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528538');
INSERT INTO "django_admin_log" VALUES(771,'590','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528559');
INSERT INTO "django_admin_log" VALUES(772,'589','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528580');
INSERT INTO "django_admin_log" VALUES(773,'588','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528600');
INSERT INTO "django_admin_log" VALUES(774,'587','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528622');
INSERT INTO "django_admin_log" VALUES(775,'586','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528643');
INSERT INTO "django_admin_log" VALUES(776,'585','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528664');
INSERT INTO "django_admin_log" VALUES(777,'584','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528685');
INSERT INTO "django_admin_log" VALUES(778,'583','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528706');
INSERT INTO "django_admin_log" VALUES(779,'582','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528727');
INSERT INTO "django_admin_log" VALUES(780,'581','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528747');
INSERT INTO "django_admin_log" VALUES(781,'580','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528768');
INSERT INTO "django_admin_log" VALUES(782,'579','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528789');
INSERT INTO "django_admin_log" VALUES(783,'578','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528809');
INSERT INTO "django_admin_log" VALUES(784,'577','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528830');
INSERT INTO "django_admin_log" VALUES(785,'576','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528851');
INSERT INTO "django_admin_log" VALUES(786,'575','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528872');
INSERT INTO "django_admin_log" VALUES(787,'574','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528892');
INSERT INTO "django_admin_log" VALUES(788,'573','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528914');
INSERT INTO "django_admin_log" VALUES(789,'572','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528935');
INSERT INTO "django_admin_log" VALUES(790,'571','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528957');
INSERT INTO "django_admin_log" VALUES(791,'570','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.528985');
INSERT INTO "django_admin_log" VALUES(792,'569','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529009');
INSERT INTO "django_admin_log" VALUES(793,'568','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529037');
INSERT INTO "django_admin_log" VALUES(794,'567','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529060');
INSERT INTO "django_admin_log" VALUES(795,'566','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529081');
INSERT INTO "django_admin_log" VALUES(796,'565','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529102');
INSERT INTO "django_admin_log" VALUES(797,'564','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529123');
INSERT INTO "django_admin_log" VALUES(798,'563','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529144');
INSERT INTO "django_admin_log" VALUES(799,'562','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529164');
INSERT INTO "django_admin_log" VALUES(800,'561','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529185');
INSERT INTO "django_admin_log" VALUES(801,'560','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529206');
INSERT INTO "django_admin_log" VALUES(802,'559','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529227');
INSERT INTO "django_admin_log" VALUES(803,'558','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529248');
INSERT INTO "django_admin_log" VALUES(804,'557','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529269');
INSERT INTO "django_admin_log" VALUES(805,'556','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529290');
INSERT INTO "django_admin_log" VALUES(806,'555','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529311');
INSERT INTO "django_admin_log" VALUES(807,'554','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529332');
INSERT INTO "django_admin_log" VALUES(808,'553','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529353');
INSERT INTO "django_admin_log" VALUES(809,'552','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529373');
INSERT INTO "django_admin_log" VALUES(810,'551','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529394');
INSERT INTO "django_admin_log" VALUES(811,'550','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529415');
INSERT INTO "django_admin_log" VALUES(812,'549','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529443');
INSERT INTO "django_admin_log" VALUES(813,'548','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529465');
INSERT INTO "django_admin_log" VALUES(814,'547','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529485');
INSERT INTO "django_admin_log" VALUES(815,'546','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529506');
INSERT INTO "django_admin_log" VALUES(816,'545','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529527');
INSERT INTO "django_admin_log" VALUES(817,'544','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529548');
INSERT INTO "django_admin_log" VALUES(818,'543','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529569');
INSERT INTO "django_admin_log" VALUES(819,'542','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529589');
INSERT INTO "django_admin_log" VALUES(820,'541','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529610');
INSERT INTO "django_admin_log" VALUES(821,'540','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529630');
INSERT INTO "django_admin_log" VALUES(822,'539','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529651');
INSERT INTO "django_admin_log" VALUES(823,'538','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529672');
INSERT INTO "django_admin_log" VALUES(824,'537','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529693');
INSERT INTO "django_admin_log" VALUES(825,'536','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529713');
INSERT INTO "django_admin_log" VALUES(826,'535','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529735');
INSERT INTO "django_admin_log" VALUES(827,'534','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529756');
INSERT INTO "django_admin_log" VALUES(828,'533','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529777');
INSERT INTO "django_admin_log" VALUES(829,'532','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529797');
INSERT INTO "django_admin_log" VALUES(830,'531','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529818');
INSERT INTO "django_admin_log" VALUES(831,'530','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529839');
INSERT INTO "django_admin_log" VALUES(832,'529','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529860');
INSERT INTO "django_admin_log" VALUES(833,'528','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529889');
INSERT INTO "django_admin_log" VALUES(834,'527','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529911');
INSERT INTO "django_admin_log" VALUES(835,'526','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529932');
INSERT INTO "django_admin_log" VALUES(836,'525','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529953');
INSERT INTO "django_admin_log" VALUES(837,'524','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529974');
INSERT INTO "django_admin_log" VALUES(838,'523','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.529995');
INSERT INTO "django_admin_log" VALUES(839,'522','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530016');
INSERT INTO "django_admin_log" VALUES(840,'521','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530037');
INSERT INTO "django_admin_log" VALUES(841,'520','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530058');
INSERT INTO "django_admin_log" VALUES(842,'519','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530079');
INSERT INTO "django_admin_log" VALUES(843,'518','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530099');
INSERT INTO "django_admin_log" VALUES(844,'517','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530120');
INSERT INTO "django_admin_log" VALUES(845,'516','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530141');
INSERT INTO "django_admin_log" VALUES(846,'515','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530162');
INSERT INTO "django_admin_log" VALUES(847,'514','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530183');
INSERT INTO "django_admin_log" VALUES(848,'513','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530204');
INSERT INTO "django_admin_log" VALUES(849,'512','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530224');
INSERT INTO "django_admin_log" VALUES(850,'511','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530245');
INSERT INTO "django_admin_log" VALUES(851,'510','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530266');
INSERT INTO "django_admin_log" VALUES(852,'509','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530287');
INSERT INTO "django_admin_log" VALUES(853,'508','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530307');
INSERT INTO "django_admin_log" VALUES(854,'507','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530335');
INSERT INTO "django_admin_log" VALUES(855,'506','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530356');
INSERT INTO "django_admin_log" VALUES(856,'505','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530377');
INSERT INTO "django_admin_log" VALUES(857,'504','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530398');
INSERT INTO "django_admin_log" VALUES(858,'503','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530419');
INSERT INTO "django_admin_log" VALUES(859,'502','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530439');
INSERT INTO "django_admin_log" VALUES(860,'501','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530460');
INSERT INTO "django_admin_log" VALUES(861,'500','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530480');
INSERT INTO "django_admin_log" VALUES(862,'499','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530501');
INSERT INTO "django_admin_log" VALUES(863,'498','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530521');
INSERT INTO "django_admin_log" VALUES(864,'497','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530542');
INSERT INTO "django_admin_log" VALUES(865,'496','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530562');
INSERT INTO "django_admin_log" VALUES(866,'495','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530583');
INSERT INTO "django_admin_log" VALUES(867,'494','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530604');
INSERT INTO "django_admin_log" VALUES(868,'493','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530624');
INSERT INTO "django_admin_log" VALUES(869,'492','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530645');
INSERT INTO "django_admin_log" VALUES(870,'491','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530666');
INSERT INTO "django_admin_log" VALUES(871,'490','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530687');
INSERT INTO "django_admin_log" VALUES(872,'489','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530707');
INSERT INTO "django_admin_log" VALUES(873,'488','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530728');
INSERT INTO "django_admin_log" VALUES(874,'487','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530749');
INSERT INTO "django_admin_log" VALUES(875,'486','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530769');
INSERT INTO "django_admin_log" VALUES(876,'485','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530798');
INSERT INTO "django_admin_log" VALUES(877,'484','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530819');
INSERT INTO "django_admin_log" VALUES(878,'483','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530839');
INSERT INTO "django_admin_log" VALUES(879,'482','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530860');
INSERT INTO "django_admin_log" VALUES(880,'481','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530881');
INSERT INTO "django_admin_log" VALUES(881,'480','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530901');
INSERT INTO "django_admin_log" VALUES(882,'479','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530922');
INSERT INTO "django_admin_log" VALUES(883,'478','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530942');
INSERT INTO "django_admin_log" VALUES(884,'477','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530963');
INSERT INTO "django_admin_log" VALUES(885,'476','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.530983');
INSERT INTO "django_admin_log" VALUES(886,'475','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.531004');
INSERT INTO "django_admin_log" VALUES(887,'474','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.531024');
INSERT INTO "django_admin_log" VALUES(888,'473','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.531053');
INSERT INTO "django_admin_log" VALUES(889,'472','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.531074');
INSERT INTO "django_admin_log" VALUES(890,'471','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.531094');
INSERT INTO "django_admin_log" VALUES(891,'470','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.531115');
INSERT INTO "django_admin_log" VALUES(892,'469','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.531136');
INSERT INTO "django_admin_log" VALUES(893,'468','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.531156');
INSERT INTO "django_admin_log" VALUES(894,'467','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.531177');
INSERT INTO "django_admin_log" VALUES(895,'466','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.531198');
INSERT INTO "django_admin_log" VALUES(896,'465','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.531219');
INSERT INTO "django_admin_log" VALUES(897,'464','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.531247');
INSERT INTO "django_admin_log" VALUES(898,'463','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.531269');
INSERT INTO "django_admin_log" VALUES(899,'462','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.531290');
INSERT INTO "django_admin_log" VALUES(900,'461','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.531311');
INSERT INTO "django_admin_log" VALUES(901,'460','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.531331');
INSERT INTO "django_admin_log" VALUES(902,'459','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.531352');
INSERT INTO "django_admin_log" VALUES(903,'458','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.531373');
INSERT INTO "django_admin_log" VALUES(904,'457','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.531395');
INSERT INTO "django_admin_log" VALUES(905,'456','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.531416');
INSERT INTO "django_admin_log" VALUES(906,'455','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.531437');
INSERT INTO "django_admin_log" VALUES(907,'454','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.531457');
INSERT INTO "django_admin_log" VALUES(908,'453','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.531478');
INSERT INTO "django_admin_log" VALUES(909,'452','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.531499');
INSERT INTO "django_admin_log" VALUES(910,'451','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.531519');
INSERT INTO "django_admin_log" VALUES(911,'450','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.531540');
INSERT INTO "django_admin_log" VALUES(912,'449','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.531560');
INSERT INTO "django_admin_log" VALUES(913,'448','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.531581');
INSERT INTO "django_admin_log" VALUES(914,'447','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.531601');
INSERT INTO "django_admin_log" VALUES(915,'446','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.531623');
INSERT INTO "django_admin_log" VALUES(916,'445','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.531643');
INSERT INTO "django_admin_log" VALUES(917,'444','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.531664');
INSERT INTO "django_admin_log" VALUES(918,'443','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.531693');
INSERT INTO "django_admin_log" VALUES(919,'442','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.531714');
INSERT INTO "django_admin_log" VALUES(920,'441','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.531735');
INSERT INTO "django_admin_log" VALUES(921,'440','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.531757');
INSERT INTO "django_admin_log" VALUES(922,'439','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.531778');
INSERT INTO "django_admin_log" VALUES(923,'438','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.531801');
INSERT INTO "django_admin_log" VALUES(924,'437','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.531974');
INSERT INTO "django_admin_log" VALUES(925,'436','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.531995');
INSERT INTO "django_admin_log" VALUES(926,'435','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532016');
INSERT INTO "django_admin_log" VALUES(927,'434','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532037');
INSERT INTO "django_admin_log" VALUES(928,'433','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532057');
INSERT INTO "django_admin_log" VALUES(929,'432','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532078');
INSERT INTO "django_admin_log" VALUES(930,'431','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532099');
INSERT INTO "django_admin_log" VALUES(931,'430','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532120');
INSERT INTO "django_admin_log" VALUES(932,'429','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532150');
INSERT INTO "django_admin_log" VALUES(933,'428','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532171');
INSERT INTO "django_admin_log" VALUES(934,'427','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532191');
INSERT INTO "django_admin_log" VALUES(935,'426','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532212');
INSERT INTO "django_admin_log" VALUES(936,'425','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532232');
INSERT INTO "django_admin_log" VALUES(937,'424','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532253');
INSERT INTO "django_admin_log" VALUES(938,'423','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532273');
INSERT INTO "django_admin_log" VALUES(939,'422','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532294');
INSERT INTO "django_admin_log" VALUES(940,'421','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532314');
INSERT INTO "django_admin_log" VALUES(941,'420','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532335');
INSERT INTO "django_admin_log" VALUES(942,'419','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532355');
INSERT INTO "django_admin_log" VALUES(943,'418','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532376');
INSERT INTO "django_admin_log" VALUES(944,'417','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532396');
INSERT INTO "django_admin_log" VALUES(945,'416','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532417');
INSERT INTO "django_admin_log" VALUES(946,'415','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532437');
INSERT INTO "django_admin_log" VALUES(947,'414','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532458');
INSERT INTO "django_admin_log" VALUES(948,'413','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532479');
INSERT INTO "django_admin_log" VALUES(949,'412','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532499');
INSERT INTO "django_admin_log" VALUES(950,'411','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532520');
INSERT INTO "django_admin_log" VALUES(951,'410','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532540');
INSERT INTO "django_admin_log" VALUES(952,'409','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532561');
INSERT INTO "django_admin_log" VALUES(953,'408','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532591');
INSERT INTO "django_admin_log" VALUES(954,'407','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532612');
INSERT INTO "django_admin_log" VALUES(955,'406','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532632');
INSERT INTO "django_admin_log" VALUES(956,'405','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532653');
INSERT INTO "django_admin_log" VALUES(957,'404','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532674');
INSERT INTO "django_admin_log" VALUES(958,'403','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532694');
INSERT INTO "django_admin_log" VALUES(959,'402','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532715');
INSERT INTO "django_admin_log" VALUES(960,'401','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532736');
INSERT INTO "django_admin_log" VALUES(961,'400','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532757');
INSERT INTO "django_admin_log" VALUES(962,'399','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532777');
INSERT INTO "django_admin_log" VALUES(963,'398','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532798');
INSERT INTO "django_admin_log" VALUES(964,'397','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532819');
INSERT INTO "django_admin_log" VALUES(965,'396','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532840');
INSERT INTO "django_admin_log" VALUES(966,'395','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532861');
INSERT INTO "django_admin_log" VALUES(967,'394','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532882');
INSERT INTO "django_admin_log" VALUES(968,'393','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532902');
INSERT INTO "django_admin_log" VALUES(969,'392','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532923');
INSERT INTO "django_admin_log" VALUES(970,'391','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532943');
INSERT INTO "django_admin_log" VALUES(971,'390','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532964');
INSERT INTO "django_admin_log" VALUES(972,'389','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.532984');
INSERT INTO "django_admin_log" VALUES(973,'388','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.533006');
INSERT INTO "django_admin_log" VALUES(974,'387','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.533040');
INSERT INTO "django_admin_log" VALUES(975,'386','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.533062');
INSERT INTO "django_admin_log" VALUES(976,'385','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.533083');
INSERT INTO "django_admin_log" VALUES(977,'384','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.533104');
INSERT INTO "django_admin_log" VALUES(978,'383','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.533125');
INSERT INTO "django_admin_log" VALUES(979,'382','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.533145');
INSERT INTO "django_admin_log" VALUES(980,'381','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.533166');
INSERT INTO "django_admin_log" VALUES(981,'380','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.533187');
INSERT INTO "django_admin_log" VALUES(982,'379','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.533208');
INSERT INTO "django_admin_log" VALUES(983,'378','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.533229');
INSERT INTO "django_admin_log" VALUES(984,'377','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.533249');
INSERT INTO "django_admin_log" VALUES(985,'376','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.533270');
INSERT INTO "django_admin_log" VALUES(986,'375','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.533291');
INSERT INTO "django_admin_log" VALUES(987,'374','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.533311');
INSERT INTO "django_admin_log" VALUES(988,'373','farid - 55555555',3,'',29,1,'2025-10-16 21:37:25.533332');
INSERT INTO "django_admin_log" VALUES(989,'1567','Tahmaz - test salam',1,'[{"added": {}}]',29,1,'2025-10-16 21:38:51.123920');
INSERT INTO "django_admin_log" VALUES(990,'1568','Tahmaz - a',1,'[{"added": {}}]',29,1,'2025-10-16 21:40:18.894570');
INSERT INTO "django_admin_log" VALUES(991,'1','Rəy Bankı: Tahmaz Muradov (1 rəy)',2,'[{"changed": {"fields": ["M\u00fcsb\u0259t Sentiment Bal\u0131"]}}]',58,1,'2025-10-16 21:46:12.032876');
INSERT INTO "django_admin_log" VALUES(992,'2','test 1',2,'[{"changed": {"fields": ["Ad"]}}]',54,1,'2025-10-16 21:47:20.921814');
INSERT INTO "django_admin_log" VALUES(993,'4','test 2',1,'[{"added": {}}]',54,1,'2025-10-16 21:47:26.393957');
INSERT INTO "django_admin_log" VALUES(994,'5','test 3',1,'[{"added": {}}]',54,1,'2025-10-16 21:47:31.689622');
INSERT INTO "django_admin_log" VALUES(995,'6','test 4',1,'[{"added": {}}]',54,1,'2025-10-16 21:47:37.316505');
INSERT INTO "django_admin_log" VALUES(996,'5','Tahmaz Muradov → Tural Cəfərov: a',2,'[{"changed": {"fields": ["\u018flaq\u0259li Kompetensiya", "Kontekst", "Qiym\u0259t (1-5)", "Oxundu", "Alan\u0131n Cavab\u0131", "Etiketl\u0259r"]}}]',57,1,'2025-10-16 21:48:31.177047');
INSERT INTO "django_admin_log" VALUES(997,'5','Tahmaz Muradov → Tural Cəfərov: admin',2,'[{"changed": {"fields": ["R\u0259y Tipi", "Ba\u015fl\u0131q", "Mesaj", "\u018flaq\u0259li Kompetensiya", "Kontekst", "Alan\u0131n Cavab\u0131", "Bildirildi", "Bildirm\u0259 S\u0259b\u0259bi"]}}]',57,1,'2025-10-16 21:50:58.775753');
INSERT INTO "django_admin_log" VALUES(998,'3','İctimai Təqdir: salam',2,'[{"changed": {"fields": ["X\u00fcsusi Se\u00e7ilmi\u015f", "Se\u00e7ilm\u0259 M\u00fcdd\u0259ti"]}}]',55,1,'2025-10-16 21:52:42.740388');
INSERT INTO "django_admin_log" VALUES(999,'1','Direktor (DIR)',2,'[{"changed": {"fields": ["T\u0259svir", "S\u0259viyy\u0259", "Hesabat Verir", "T\u0259l\u0259b Olunan T\u0259hsil", "T\u0259l\u0259b Olunan T\u0259cr\u00fcb\u0259"]}}]',17,1,'2025-10-16 21:55:23.965229');
INSERT INTO "django_admin_log" VALUES(1000,'1','01 - 2025-10-17: 45',1,'[{"added": {}}]',86,1,'2025-10-16 21:56:40.449383');
INSERT INTO "django_admin_log" VALUES(1001,'1','01 - AzAgroPOS',2,'[]',84,1,'2025-10-16 21:58:25.463775');
INSERT INTO "django_admin_log" VALUES(1002,'1','test (2025 - annual)',2,'[{"changed": {"fields": ["M\u0259qs\u0259d"]}}]',85,1,'2025-10-16 21:58:54.476557');
INSERT INTO "django_admin_log" VALUES(1003,'1','test (2025 - annual)',2,'[{"added": {"name": "A\u00e7ar N\u0259tic\u0259", "object": "test - aaa"}}]',85,1,'2025-10-16 21:59:36.208585');
CREATE TABLE "django_content_type" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app_label" varchar(100) NOT NULL, "model" varchar(100) NOT NULL);
INSERT INTO "django_content_type" VALUES(1,'admin','logentry');
INSERT INTO "django_content_type" VALUES(2,'auth','permission');
INSERT INTO "django_content_type" VALUES(3,'auth','group');
INSERT INTO "django_content_type" VALUES(4,'contenttypes','contenttype');
INSERT INTO "django_content_type" VALUES(5,'sessions','session');
INSERT INTO "django_content_type" VALUES(6,'accounts','user');
INSERT INTO "django_content_type" VALUES(7,'accounts','historicalprofile');
INSERT INTO "django_content_type" VALUES(8,'accounts','historicalrole');
INSERT INTO "django_content_type" VALUES(9,'accounts','historicaluser');
INSERT INTO "django_content_type" VALUES(10,'accounts','role');
INSERT INTO "django_content_type" VALUES(11,'accounts','profile');
INSERT INTO "django_content_type" VALUES(12,'departments','department');
INSERT INTO "django_content_type" VALUES(13,'departments','historicaldepartment');
INSERT INTO "django_content_type" VALUES(14,'departments','historicalorganization');
INSERT INTO "django_content_type" VALUES(15,'departments','historicalposition');
INSERT INTO "django_content_type" VALUES(16,'departments','organization');
INSERT INTO "django_content_type" VALUES(17,'departments','position');
INSERT INTO "django_content_type" VALUES(18,'evaluations','evaluationcampaign');
INSERT INTO "django_content_type" VALUES(19,'evaluations','questioncategory');
INSERT INTO "django_content_type" VALUES(20,'evaluations','question');
INSERT INTO "django_content_type" VALUES(21,'evaluations','historicalquestion');
INSERT INTO "django_content_type" VALUES(22,'evaluations','historicalevaluationcampaign');
INSERT INTO "django_content_type" VALUES(23,'evaluations','historicalevaluationassignment');
INSERT INTO "django_content_type" VALUES(24,'evaluations','evaluationassignment');
INSERT INTO "django_content_type" VALUES(25,'evaluations','campaignquestion');
INSERT INTO "django_content_type" VALUES(26,'evaluations','response');
INSERT INTO "django_content_type" VALUES(27,'evaluations','evaluationresult');
INSERT INTO "django_content_type" VALUES(28,'notifications','emailtemplate');
INSERT INTO "django_content_type" VALUES(29,'notifications','notification');
INSERT INTO "django_content_type" VALUES(30,'reports','report');
INSERT INTO "django_content_type" VALUES(31,'reports','radarchartdata');
INSERT INTO "django_content_type" VALUES(32,'development_plans','developmentgoal');
INSERT INTO "django_content_type" VALUES(33,'development_plans','progresslog');
INSERT INTO "django_content_type" VALUES(34,'audit','auditlog');
INSERT INTO "django_content_type" VALUES(35,'notifications','emaillog');
INSERT INTO "django_content_type" VALUES(36,'reports','reportgenerationlog');
INSERT INTO "django_content_type" VALUES(37,'support','supportticket');
INSERT INTO "django_content_type" VALUES(38,'support','ticketcomment');
INSERT INTO "django_content_type" VALUES(39,'competencies','historicalcompetency');
INSERT INTO "django_content_type" VALUES(40,'competencies','competency');
INSERT INTO "django_content_type" VALUES(41,'competencies','proficiencylevel');
INSERT INTO "django_content_type" VALUES(42,'competencies','historicalpositioncompetency');
INSERT INTO "django_content_type" VALUES(43,'competencies','positioncompetency');
INSERT INTO "django_content_type" VALUES(44,'competencies','historicaluserskill');
INSERT INTO "django_content_type" VALUES(45,'competencies','userskill');
INSERT INTO "django_content_type" VALUES(46,'training','historicaltrainingresource');
INSERT INTO "django_content_type" VALUES(47,'training','trainingresource');
INSERT INTO "django_content_type" VALUES(48,'training','historicalusertraining');
INSERT INTO "django_content_type" VALUES(49,'training','usertraining');
INSERT INTO "django_content_type" VALUES(50,'workforce_planning','criticalrole');
INSERT INTO "django_content_type" VALUES(51,'workforce_planning','talentmatrix');
INSERT INTO "django_content_type" VALUES(52,'workforce_planning','successioncandidate');
INSERT INTO "django_content_type" VALUES(53,'workforce_planning','competencygap');
INSERT INTO "django_content_type" VALUES(54,'continuous_feedback','feedbacktag');
INSERT INTO "django_content_type" VALUES(55,'continuous_feedback','publicrecognition');
INSERT INTO "django_content_type" VALUES(56,'continuous_feedback','recognitioncomment');
INSERT INTO "django_content_type" VALUES(57,'continuous_feedback','quickfeedback');
INSERT INTO "django_content_type" VALUES(58,'continuous_feedback','feedbackbank');
INSERT INTO "django_content_type" VALUES(59,'continuous_feedback','recognitionlike');
INSERT INTO "django_content_type" VALUES(60,'accounts','historicalworkhistory');
INSERT INTO "django_content_type" VALUES(61,'accounts','historicalemployeedocument');
INSERT INTO "django_content_type" VALUES(62,'accounts','workhistory');
INSERT INTO "django_content_type" VALUES(63,'accounts','employeedocument');
INSERT INTO "django_content_type" VALUES(64,'compensation','compensationhistory');
INSERT INTO "django_content_type" VALUES(65,'compensation','historicalbonus');
INSERT INTO "django_content_type" VALUES(66,'compensation','allowance');
INSERT INTO "django_content_type" VALUES(67,'compensation','historicaldeduction');
INSERT INTO "django_content_type" VALUES(68,'compensation','historicalallowance');
INSERT INTO "django_content_type" VALUES(69,'compensation','historicalcompensationhistory');
INSERT INTO "django_content_type" VALUES(70,'compensation','salaryinformation');
INSERT INTO "django_content_type" VALUES(71,'compensation','deduction');
INSERT INTO "django_content_type" VALUES(72,'compensation','bonus');
INSERT INTO "django_content_type" VALUES(73,'compensation','historicalsalaryinformation');
INSERT INTO "django_content_type" VALUES(74,'leave_attendance','leavetype');
INSERT INTO "django_content_type" VALUES(75,'leave_attendance','leaverequest');
INSERT INTO "django_content_type" VALUES(76,'leave_attendance','leavebalance');
INSERT INTO "django_content_type" VALUES(77,'leave_attendance','holiday');
INSERT INTO "django_content_type" VALUES(78,'leave_attendance','historicalleavetype');
INSERT INTO "django_content_type" VALUES(79,'leave_attendance','historicalleaverequest');
INSERT INTO "django_content_type" VALUES(80,'leave_attendance','historicalleavebalance');
INSERT INTO "django_content_type" VALUES(81,'leave_attendance','historicalholiday');
INSERT INTO "django_content_type" VALUES(82,'leave_attendance','historicalattendance');
INSERT INTO "django_content_type" VALUES(83,'leave_attendance','attendance');
INSERT INTO "django_content_type" VALUES(84,'development_plans','kpi');
INSERT INTO "django_content_type" VALUES(85,'development_plans','strategicobjective');
INSERT INTO "django_content_type" VALUES(86,'development_plans','kpimeasurement');
INSERT INTO "django_content_type" VALUES(87,'development_plans','keyresult');
INSERT INTO "django_content_type" VALUES(88,'development_plans','historicalstrategicobjective');
INSERT INTO "django_content_type" VALUES(89,'development_plans','historicalkpimeasurement');
INSERT INTO "django_content_type" VALUES(90,'development_plans','historicalkpi');
INSERT INTO "django_content_type" VALUES(91,'development_plans','historicalkeyresult');
INSERT INTO "django_content_type" VALUES(92,'recruitment','application');
INSERT INTO "django_content_type" VALUES(93,'recruitment','jobposting');
INSERT INTO "django_content_type" VALUES(94,'recruitment','interview');
INSERT INTO "django_content_type" VALUES(95,'recruitment','historicalonboardingtask');
INSERT INTO "django_content_type" VALUES(96,'recruitment','historicaloffer');
INSERT INTO "django_content_type" VALUES(97,'recruitment','historicaljobposting');
INSERT INTO "django_content_type" VALUES(98,'recruitment','historicalinterview');
INSERT INTO "django_content_type" VALUES(99,'recruitment','historicalapplication');
INSERT INTO "django_content_type" VALUES(100,'recruitment','onboardingtask');
INSERT INTO "django_content_type" VALUES(101,'recruitment','offer');
INSERT INTO "django_content_type" VALUES(102,'compensation','historicaldepartmentbudget');
INSERT INTO "django_content_type" VALUES(103,'compensation','departmentbudget');
INSERT INTO "django_content_type" VALUES(104,'reports','systemkpi');
INSERT INTO "django_content_type" VALUES(105,'development_plans','objectiveupdate');
INSERT INTO "django_content_type" VALUES(106,'development_plans','historicalobjectiveupdate');
INSERT INTO "django_content_type" VALUES(107,'development_plans','historicalmilestone');
INSERT INTO "django_content_type" VALUES(108,'development_plans','milestone');
INSERT INTO "django_content_type" VALUES(109,'dashboard','dashboardwidget');
INSERT INTO "django_content_type" VALUES(110,'dashboard','systemkpi');
INSERT INTO "django_content_type" VALUES(111,'dashboard','trenddata');
INSERT INTO "django_content_type" VALUES(112,'dashboard','analyticsreport');
INSERT INTO "django_content_type" VALUES(113,'dashboard','realtimestat');
INSERT INTO "django_content_type" VALUES(114,'dashboard','forecastdata');
INSERT INTO "django_content_type" VALUES(115,'notifications','notificationmethod');
INSERT INTO "django_content_type" VALUES(116,'notifications','smsprovider');
INSERT INTO "django_content_type" VALUES(117,'notifications','bulknotification');
INSERT INTO "django_content_type" VALUES(118,'notifications','notificationtemplate');
INSERT INTO "django_content_type" VALUES(119,'notifications','pushnotification');
INSERT INTO "django_content_type" VALUES(120,'notifications','smslog');
INSERT INTO "django_content_type" VALUES(121,'notifications','usernotificationpreference');
CREATE TABLE "django_migrations" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app" varchar(255) NOT NULL, "name" varchar(255) NOT NULL, "applied" datetime NOT NULL);
INSERT INTO "django_migrations" VALUES(1,'contenttypes','0001_initial','2025-10-09 06:28:57.995389');
INSERT INTO "django_migrations" VALUES(2,'contenttypes','0002_remove_content_type_name','2025-10-09 06:28:58.004715');
INSERT INTO "django_migrations" VALUES(3,'auth','0001_initial','2025-10-09 06:28:58.021365');
INSERT INTO "django_migrations" VALUES(4,'auth','0002_alter_permission_name_max_length','2025-10-09 06:28:58.031606');
INSERT INTO "django_migrations" VALUES(5,'auth','0003_alter_user_email_max_length','2025-10-09 06:28:58.039769');
INSERT INTO "django_migrations" VALUES(6,'auth','0004_alter_user_username_opts','2025-10-09 06:28:58.048839');
INSERT INTO "django_migrations" VALUES(7,'auth','0005_alter_user_last_login_null','2025-10-09 06:28:58.056728');
INSERT INTO "django_migrations" VALUES(8,'auth','0006_require_contenttypes_0002','2025-10-09 06:28:58.063342');
INSERT INTO "django_migrations" VALUES(9,'auth','0007_alter_validators_add_error_messages','2025-10-09 06:28:58.071929');
INSERT INTO "django_migrations" VALUES(10,'auth','0008_alter_user_username_max_length','2025-10-09 06:28:58.081167');
INSERT INTO "django_migrations" VALUES(11,'auth','0009_alter_user_last_name_max_length','2025-10-09 06:28:58.089625');
INSERT INTO "django_migrations" VALUES(12,'auth','0010_alter_group_name_max_length','2025-10-09 06:28:58.100444');
INSERT INTO "django_migrations" VALUES(13,'auth','0011_update_proxy_permissions','2025-10-09 06:28:58.109101');
INSERT INTO "django_migrations" VALUES(14,'auth','0012_alter_user_first_name_max_length','2025-10-09 06:28:58.117567');
INSERT INTO "django_migrations" VALUES(15,'accounts','0001_initial','2025-10-09 06:28:58.140660');
INSERT INTO "django_migrations" VALUES(16,'departments','0001_initial','2025-10-09 06:28:58.279569');
INSERT INTO "django_migrations" VALUES(17,'accounts','0002_initial','2025-10-09 06:28:58.403874');
INSERT INTO "django_migrations" VALUES(18,'admin','0001_initial','2025-10-09 06:28:58.428661');
INSERT INTO "django_migrations" VALUES(19,'admin','0002_logentry_remove_auto_add','2025-10-09 06:28:58.447244');
INSERT INTO "django_migrations" VALUES(20,'admin','0003_logentry_add_action_flag_choices','2025-10-09 06:28:58.461765');
INSERT INTO "django_migrations" VALUES(21,'audit','0001_initial','2025-10-09 06:28:58.488213');
INSERT INTO "django_migrations" VALUES(22,'development_plans','0001_initial','2025-10-09 06:28:58.567167');
INSERT INTO "django_migrations" VALUES(23,'evaluations','0001_initial','2025-10-09 06:28:58.837628');
INSERT INTO "django_migrations" VALUES(24,'notifications','0001_initial','2025-10-09 06:28:58.878254');
INSERT INTO "django_migrations" VALUES(25,'reports','0001_initial','2025-10-09 06:28:58.929321');
INSERT INTO "django_migrations" VALUES(26,'sessions','0001_initial','2025-10-09 06:28:58.948002');
INSERT INTO "django_migrations" VALUES(27,'development_plans','0002_developmentgoal_approval_note_and_more','2025-10-09 22:12:54.646397');
INSERT INTO "django_migrations" VALUES(28,'development_plans','0003_progresslog_is_draft_progresslog_updated_at','2025-10-09 22:29:32.965682');
INSERT INTO "django_migrations" VALUES(29,'notifications','0002_emaillog','2025-10-09 22:39:25.594212');
INSERT INTO "django_migrations" VALUES(30,'development_plans','0004_developmentgoal_is_approved','2025-10-10 07:30:27.691423');
INSERT INTO "django_migrations" VALUES(31,'development_plans','0005_remove_is_approved_field','2025-10-10 08:47:03.852037');
INSERT INTO "django_migrations" VALUES(32,'evaluations','0002_update_score_validators_to_5','2025-10-10 08:47:03.885382');
INSERT INTO "django_migrations" VALUES(33,'reports','0002_add_report_generation_log','2025-10-10 08:47:03.921902');
INSERT INTO "django_migrations" VALUES(34,'departments','0002_remove_department_departments_department_tref4ab','2025-10-10 09:29:33.912707');
INSERT INTO "django_migrations" VALUES(35,'departments','0003_remove_historicalposition_level','2025-10-10 11:33:51.423240');
INSERT INTO "django_migrations" VALUES(36,'departments','0004_historicalposition_level','2025-10-10 15:34:25.745691');
INSERT INTO "django_migrations" VALUES(37,'evaluations','0003_response_sentiment_category_response_sentiment_score','2025-10-10 15:34:25.777753');
INSERT INTO "django_migrations" VALUES(38,'support','0001_initial','2025-10-10 20:49:59.824974');
INSERT INTO "django_migrations" VALUES(39,'audit','0002_alter_auditlog_action','2025-10-10 22:49:57.360219');
INSERT INTO "django_migrations" VALUES(40,'competencies','0001_initial','2025-10-11 07:46:57.244394');
INSERT INTO "django_migrations" VALUES(41,'training','0001_initial','2025-10-11 07:46:57.641642');
INSERT INTO "django_migrations" VALUES(42,'competencies','0002_competency_competencie_name_eac81b_idx_and_more','2025-10-11 10:32:53.632096');
INSERT INTO "django_migrations" VALUES(43,'evaluations','0004_evaluationcampaign_evaluations_status_540c61_idx_and_more','2025-10-11 10:32:53.845792');
INSERT INTO "django_migrations" VALUES(44,'training','0002_trainingresource_training_tr_provide_516d62_idx_and_more','2025-10-11 10:32:53.990367');
INSERT INTO "django_migrations" VALUES(45,'continuous_feedback','0001_initial','2025-10-14 22:02:20.406457');
INSERT INTO "django_migrations" VALUES(46,'departments','0005_department_departments_department_tref4ab','2025-10-14 22:02:20.471141');
INSERT INTO "django_migrations" VALUES(47,'workforce_planning','0001_initial','2025-10-14 22:02:20.678490');
INSERT INTO "django_migrations" VALUES(48,'departments','0006_remove_department_departments_department_tref4ab','2025-10-14 22:02:45.131355');
INSERT INTO "django_migrations" VALUES(49,'departments','0007_department_departments_department_tref4ab','2025-10-15 07:45:34.608983');
INSERT INTO "django_migrations" VALUES(50,'departments','0008_remove_department_departments_department_tref4ab','2025-10-15 11:48:58.775785');
INSERT INTO "django_migrations" VALUES(52,'departments','0009_department_departments_department_tref4ab','2025-10-15 16:24:31.566612');
INSERT INTO "django_migrations" VALUES(53,'evaluations','0005_evaluationcampaign_weight_peer_and_more','2025-10-15 16:28:32.507238');
INSERT INTO "django_migrations" VALUES(54,'departments','0010_remove_department_departments_department_tref4ab','2025-10-15 17:21:42.864258');
INSERT INTO "django_migrations" VALUES(55,'departments','0011_department_departments_department_tref4ab','2025-10-16 07:24:17.812892');
INSERT INTO "django_migrations" VALUES(56,'accounts','0003_historicalprofile_city_and_more','2025-10-16 07:24:20.540595');
INSERT INTO "django_migrations" VALUES(57,'compensation','0001_initial','2025-10-16 07:30:26.738731');
INSERT INTO "django_migrations" VALUES(58,'leave_attendance','0001_initial','2025-10-16 07:32:57.924890');
INSERT INTO "django_migrations" VALUES(59,'development_plans','0006_kpi_strategicobjective_kpimeasurement_kpi_objective_and_more','2025-10-16 07:36:57.928148');
INSERT INTO "django_migrations" VALUES(60,'recruitment','0001_initial','2025-10-16 07:40:58.682342');
INSERT INTO "django_migrations" VALUES(61,'compensation','0002_historicaldepartmentbudget_departmentbudget','2025-10-16 12:36:39.211403');
INSERT INTO "django_migrations" VALUES(62,'departments','0012_remove_department_departments_department_tref4ab','2025-10-16 12:36:39.294972');
INSERT INTO "django_migrations" VALUES(63,'reports','0003_systemkpi','2025-10-16 17:05:17.287863');
INSERT INTO "django_migrations" VALUES(64,'development_plans','0007_historicalmilestone_historicalobjectiveupdate_and_more','2025-10-16 22:42:13.736880');
INSERT INTO "django_migrations" VALUES(65,'compensation','0003_alter_salaryinformation_user','2025-10-16 23:17:06.266638');
INSERT INTO "django_migrations" VALUES(66,'dashboard','0001_initial','2025-10-17 16:27:59.331702');
INSERT INTO "django_migrations" VALUES(67,'notifications','0003_notificationmethod_smsprovider_notification_channel_and_more','2025-10-17 17:10:52.156500');
INSERT INTO "django_migrations" VALUES(68,'accounts','0004_alter_user_managers','2025-10-17 18:53:18.184671');
CREATE TABLE "django_session" ("session_key" varchar(40) NOT NULL PRIMARY KEY, "session_data" text NOT NULL, "expire_date" datetime NOT NULL);
INSERT INTO "django_session" VALUES('a7ck3118qrr5sf724l6pmy7ibsmxiln3','.eJxVjMEOwiAQRP-FsyEuCHQ9eu83kIUFqRpISnsy_rtt0oPeJvPezFt4Wpfi155mP7G4ChCn3y5QfKa6A35QvTcZW13mKchdkQftcmycXrfD_Tso1Mu21o7RKhODzpltgsFaA9EphRB00FoZRrQWAZA5g3MKzECo4nkLmS7i8wXDLzbA:1v6yt0:b9IYbN0zajva0l4jOl9iedlt2Zc0RymKfOIEADbfFP0','2025-10-23 22:13:22.954266');
INSERT INTO "django_session" VALUES('ct0crrx2uictww7knzj9f9bnenrc57zf','.eJxVjDsOwyAQRO9CHSG-xqRM7zOghV2CkwgkY1dR7h5bcpGUM-_NvFmAbS1h67SEGdmVSXb57SKkJ9UD4APqvfHU6rrMkR8KP2nnU0N63U7376BAL_t6TDRojSRIRsTReEiKEkhjndIWDWRS0idNRiibY44iO5XjsGcppHfs8wUC4DhP:1v7LtD:bkf0ejF97C-qMjMWpJz2JcEJtKZtKNWxKFHelp30Nqo','2025-10-24 22:47:07.502328');
INSERT INTO "django_session" VALUES('la7mnbp2j0ogcjimchi9jkmk0b2rw0xm','.eJxVjDsOwyAQRO9CHSG-xqRM7zOghV2CkwgkY1dR7h5bcpGUM-_NvFmAbS1h67SEGdmVSXb57SKkJ9UD4APqvfHU6rrMkR8KP2nnU0N63U7376BAL_t6TDRojSRIRsTReEiKEkhjndIWDWRS0idNRiibY44iO5XjsGcppHfs8wUC4DhP:1v9T59:KC1WcLLg5z-8-O3OK2NTK-bLzYRtj5ACvgakEV2VEmA','2025-10-30 18:52:11.469614');
INSERT INTO "django_session" VALUES('fcs2iwhwdpllgvfy30d1pkfwapz16l3b','.eJxVjLsOwjAMAP8lM4oaJ00dRvZ-Q-XYLimgVOpjQvw7qtQB1rvTvc1A-1aGfdVlmMRcjQdz-YWZ-Kn1MPKgep8tz3VbpmyPxJ52tf0s-rqd7d-g0FqOr3dhzKnF6AmSA5TMnetglNSgDxFJGVHbJjiGDKouQiRmCSOLj8l8vuv2N9w:1v9pXa:7RfC_S-_dF-DepqORJAAsgGtVRcppxs9qU6xxcyHFew','2025-10-31 18:51:02.724096');
INSERT INTO "django_session" VALUES('qodxv69mqxuwnfrkqgxx7fnojz7adyhp','.eJxVjEEOwiAQAP_C2RBwQVmP3n0D2WVBqoYmpT0Z_25IetDrzGTeKtK21rj1vMRJ1EWBU4dfyJSeuQ0jD2r3Wae5rcvEeiR6t13fZsmv697-DSr1Or6CjASIxok1YhOc_DmRdwUKEYoN4AxDsYQuBzhCYnbBem-xsJeiPl8BnDgD:1v9prE:jgyUpxN0LbbEUGTjSTeJeGoIkZraKbqDok9rAh33PPg','2025-10-31 19:11:20.008708');
CREATE TABLE "evaluations_campaignquestion" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "order" integer NOT NULL, "campaign_id" bigint NOT NULL REFERENCES "evaluations_evaluationcampaign" ("id") DEFERRABLE INITIALLY DEFERRED, "question_id" bigint NOT NULL REFERENCES "evaluations_question" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "evaluations_campaignquestion" VALUES(1,1,1,1);
INSERT INTO "evaluations_campaignquestion" VALUES(2,2,3,47);
INSERT INTO "evaluations_campaignquestion" VALUES(3,1,3,48);
INSERT INTO "evaluations_campaignquestion" VALUES(4,2,3,49);
INSERT INTO "evaluations_campaignquestion" VALUES(5,3,3,50);
INSERT INTO "evaluations_campaignquestion" VALUES(6,4,3,51);
INSERT INTO "evaluations_campaignquestion" VALUES(7,5,3,52);
INSERT INTO "evaluations_campaignquestion" VALUES(8,6,3,53);
INSERT INTO "evaluations_campaignquestion" VALUES(9,7,3,54);
INSERT INTO "evaluations_campaignquestion" VALUES(10,8,3,55);
INSERT INTO "evaluations_campaignquestion" VALUES(11,9,3,56);
INSERT INTO "evaluations_campaignquestion" VALUES(12,10,3,57);
INSERT INTO "evaluations_campaignquestion" VALUES(13,11,3,58);
INSERT INTO "evaluations_campaignquestion" VALUES(14,12,3,59);
INSERT INTO "evaluations_campaignquestion" VALUES(15,13,3,60);
INSERT INTO "evaluations_campaignquestion" VALUES(16,14,3,61);
INSERT INTO "evaluations_campaignquestion" VALUES(17,0,4,47);
INSERT INTO "evaluations_campaignquestion" VALUES(18,1,4,48);
INSERT INTO "evaluations_campaignquestion" VALUES(19,2,4,49);
INSERT INTO "evaluations_campaignquestion" VALUES(20,3,4,50);
INSERT INTO "evaluations_campaignquestion" VALUES(21,4,4,51);
INSERT INTO "evaluations_campaignquestion" VALUES(22,5,4,52);
INSERT INTO "evaluations_campaignquestion" VALUES(23,6,4,53);
INSERT INTO "evaluations_campaignquestion" VALUES(24,7,4,54);
INSERT INTO "evaluations_campaignquestion" VALUES(25,8,4,55);
INSERT INTO "evaluations_campaignquestion" VALUES(26,9,4,56);
INSERT INTO "evaluations_campaignquestion" VALUES(27,10,4,57);
INSERT INTO "evaluations_campaignquestion" VALUES(28,11,4,58);
INSERT INTO "evaluations_campaignquestion" VALUES(29,12,4,59);
INSERT INTO "evaluations_campaignquestion" VALUES(30,13,4,60);
INSERT INTO "evaluations_campaignquestion" VALUES(31,14,4,61);
CREATE TABLE "evaluations_evaluationassignment" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "relationship" varchar(20) NOT NULL, "status" varchar(20) NOT NULL, "started_at" datetime NULL, "completed_at" datetime NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "campaign_id" bigint NOT NULL REFERENCES "evaluations_evaluationcampaign" ("id") DEFERRABLE INITIALLY DEFERRED, "evaluatee_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "evaluator_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "evaluations_evaluationassignment" VALUES(1,'self','in_progress','2025-10-09 11:41:09','2025-10-09 11:42:19.905649','2025-10-09 11:41:24.270744','2025-10-10 20:55:50.278297',1,1,1);
INSERT INTO "evaluations_evaluationassignment" VALUES(2,'self','pending',NULL,NULL,'2025-10-10 15:55:01.730680','2025-10-10 15:55:01.730695',3,2,2);
INSERT INTO "evaluations_evaluationassignment" VALUES(3,'peer','pending',NULL,NULL,'2025-10-10 15:55:01.740667','2025-10-10 15:55:01.740681',3,2,7);
INSERT INTO "evaluations_evaluationassignment" VALUES(4,'peer','pending',NULL,NULL,'2025-10-10 15:55:01.748757','2025-10-10 15:55:01.748772',3,2,10);
INSERT INTO "evaluations_evaluationassignment" VALUES(5,'peer','pending',NULL,NULL,'2025-10-10 15:55:01.756781','2025-10-10 15:55:01.756794',3,2,11);
INSERT INTO "evaluations_evaluationassignment" VALUES(6,'self','pending',NULL,NULL,'2025-10-10 15:55:01.766557','2025-10-10 15:55:01.766572',3,7,7);
INSERT INTO "evaluations_evaluationassignment" VALUES(7,'supervisor','pending',NULL,NULL,'2025-10-10 15:55:01.775017','2025-10-10 15:55:01.775032',3,7,2);
INSERT INTO "evaluations_evaluationassignment" VALUES(8,'peer','pending',NULL,NULL,'2025-10-10 15:55:01.784339','2025-10-10 15:55:01.784352',3,7,10);
INSERT INTO "evaluations_evaluationassignment" VALUES(9,'peer','pending',NULL,NULL,'2025-10-10 15:55:01.794017','2025-10-10 15:55:01.794032',3,7,11);
INSERT INTO "evaluations_evaluationassignment" VALUES(10,'self','pending',NULL,NULL,'2025-10-10 15:55:01.802981','2025-10-10 15:55:01.802994',3,8,8);
INSERT INTO "evaluations_evaluationassignment" VALUES(11,'supervisor','pending',NULL,NULL,'2025-10-10 15:55:01.811040','2025-10-10 15:55:01.811052',3,8,2);
INSERT INTO "evaluations_evaluationassignment" VALUES(12,'peer','pending',NULL,NULL,'2025-10-10 15:55:01.820369','2025-10-10 15:55:01.820383',3,8,12);
INSERT INTO "evaluations_evaluationassignment" VALUES(13,'peer','pending',NULL,NULL,'2025-10-10 15:55:01.828537','2025-10-10 15:55:01.828549',3,8,13);
INSERT INTO "evaluations_evaluationassignment" VALUES(14,'peer','pending',NULL,NULL,'2025-10-10 15:55:01.837486','2025-10-10 15:55:01.837500',3,8,14);
INSERT INTO "evaluations_evaluationassignment" VALUES(15,'self','pending',NULL,NULL,'2025-10-10 15:55:01.846225','2025-10-10 15:55:01.846240',3,9,9);
INSERT INTO "evaluations_evaluationassignment" VALUES(16,'supervisor','pending',NULL,NULL,'2025-10-10 15:55:01.854236','2025-10-10 15:55:01.854250',3,9,2);
INSERT INTO "evaluations_evaluationassignment" VALUES(17,'peer','in_progress','2025-10-10 21:10:47.023115',NULL,'2025-10-10 15:55:01.862315','2025-10-10 21:12:02.837007',3,9,15);
INSERT INTO "evaluations_evaluationassignment" VALUES(18,'peer','pending',NULL,NULL,'2025-10-10 15:55:01.870409','2025-10-10 15:55:01.870423',3,9,16);
INSERT INTO "evaluations_evaluationassignment" VALUES(19,'self','pending',NULL,NULL,'2025-10-10 15:55:01.878004','2025-10-10 15:55:01.878016',3,10,10);
INSERT INTO "evaluations_evaluationassignment" VALUES(20,'supervisor','pending',NULL,NULL,'2025-10-10 15:55:01.892084','2025-10-10 15:55:01.892097',3,10,7);
INSERT INTO "evaluations_evaluationassignment" VALUES(21,'peer','pending',NULL,NULL,'2025-10-10 15:55:01.900216','2025-10-10 15:55:01.900230',3,10,2);
INSERT INTO "evaluations_evaluationassignment" VALUES(22,'peer','pending',NULL,NULL,'2025-10-10 15:55:01.908562','2025-10-10 15:55:01.908574',3,10,11);
INSERT INTO "evaluations_evaluationassignment" VALUES(23,'self','pending',NULL,NULL,'2025-10-10 15:55:01.916270','2025-10-10 15:55:01.916282',3,11,11);
INSERT INTO "evaluations_evaluationassignment" VALUES(24,'supervisor','pending',NULL,NULL,'2025-10-10 15:55:01.923932','2025-10-10 15:55:01.923945',3,11,7);
INSERT INTO "evaluations_evaluationassignment" VALUES(25,'peer','pending',NULL,NULL,'2025-10-10 15:55:01.931723','2025-10-10 15:55:01.931736',3,11,2);
INSERT INTO "evaluations_evaluationassignment" VALUES(26,'peer','pending',NULL,NULL,'2025-10-10 15:55:01.940307','2025-10-10 15:55:01.940319',3,11,10);
INSERT INTO "evaluations_evaluationassignment" VALUES(27,'self','pending',NULL,NULL,'2025-10-10 15:55:01.948339','2025-10-10 15:55:01.948356',3,12,12);
INSERT INTO "evaluations_evaluationassignment" VALUES(28,'supervisor','pending',NULL,NULL,'2025-10-10 15:55:01.956460','2025-10-10 15:55:01.956473',3,12,8);
INSERT INTO "evaluations_evaluationassignment" VALUES(29,'peer','pending',NULL,NULL,'2025-10-10 15:55:01.964962','2025-10-10 15:55:01.964974',3,12,13);
INSERT INTO "evaluations_evaluationassignment" VALUES(30,'peer','pending',NULL,NULL,'2025-10-10 15:55:01.972805','2025-10-10 15:55:01.972817',3,12,14);
INSERT INTO "evaluations_evaluationassignment" VALUES(31,'self','pending',NULL,NULL,'2025-10-10 15:55:01.980607','2025-10-10 15:55:01.980619',3,13,13);
INSERT INTO "evaluations_evaluationassignment" VALUES(32,'supervisor','pending',NULL,NULL,'2025-10-10 15:55:01.988498','2025-10-10 15:55:01.988511',3,13,8);
INSERT INTO "evaluations_evaluationassignment" VALUES(33,'peer','pending',NULL,NULL,'2025-10-10 15:55:01.996753','2025-10-10 15:55:01.996763',3,13,12);
INSERT INTO "evaluations_evaluationassignment" VALUES(34,'peer','pending',NULL,NULL,'2025-10-10 15:55:02.005399','2025-10-10 15:55:02.005412',3,13,14);
INSERT INTO "evaluations_evaluationassignment" VALUES(35,'self','pending',NULL,NULL,'2025-10-10 15:55:02.013074','2025-10-10 15:55:02.013087',3,14,14);
INSERT INTO "evaluations_evaluationassignment" VALUES(36,'supervisor','pending',NULL,NULL,'2025-10-10 15:55:02.020810','2025-10-10 15:55:02.020823',3,14,8);
INSERT INTO "evaluations_evaluationassignment" VALUES(37,'peer','pending',NULL,NULL,'2025-10-10 15:55:02.029035','2025-10-10 15:55:02.029046',3,14,12);
INSERT INTO "evaluations_evaluationassignment" VALUES(38,'peer','pending',NULL,NULL,'2025-10-10 15:55:02.037095','2025-10-10 15:55:02.037108',3,14,13);
INSERT INTO "evaluations_evaluationassignment" VALUES(39,'self','in_progress','2025-10-10 21:13:13.103261',NULL,'2025-10-10 15:55:02.044624','2025-10-10 21:13:29.909042',3,15,15);
INSERT INTO "evaluations_evaluationassignment" VALUES(40,'supervisor','pending',NULL,NULL,'2025-10-10 15:55:02.052221','2025-10-10 15:55:02.052233',3,15,9);
INSERT INTO "evaluations_evaluationassignment" VALUES(41,'peer','pending',NULL,NULL,'2025-10-10 15:55:02.060389','2025-10-10 15:55:02.060399',3,15,16);
INSERT INTO "evaluations_evaluationassignment" VALUES(42,'self','pending',NULL,NULL,'2025-10-10 15:55:02.067710','2025-10-10 15:55:02.067722',3,16,16);
INSERT INTO "evaluations_evaluationassignment" VALUES(43,'supervisor','pending',NULL,NULL,'2025-10-10 15:55:02.075537','2025-10-10 15:55:02.075550',3,16,9);
INSERT INTO "evaluations_evaluationassignment" VALUES(44,'peer','pending',NULL,NULL,'2025-10-10 15:55:02.084069','2025-10-10 15:55:02.084081',3,16,15);
INSERT INTO "evaluations_evaluationassignment" VALUES(45,'self','pending',NULL,NULL,'2025-10-10 15:55:02.091869','2025-10-10 15:55:02.091882',3,17,17);
INSERT INTO "evaluations_evaluationassignment" VALUES(46,'supervisor','pending',NULL,NULL,'2025-10-10 15:55:02.099710','2025-10-10 15:55:02.099721',3,17,2);
INSERT INTO "evaluations_evaluationassignment" VALUES(47,'self','pending',NULL,NULL,'2025-10-10 15:55:02.107751','2025-10-10 15:55:02.107763',3,18,18);
INSERT INTO "evaluations_evaluationassignment" VALUES(48,'supervisor','pending',NULL,NULL,'2025-10-10 15:55:02.115318','2025-10-10 15:55:02.115330',3,18,2);
INSERT INTO "evaluations_evaluationassignment" VALUES(49,'peer','pending',NULL,NULL,'2025-10-10 15:55:02.123017','2025-10-10 15:55:02.123029',3,18,19);
INSERT INTO "evaluations_evaluationassignment" VALUES(50,'self','pending',NULL,NULL,'2025-10-10 15:55:02.130597','2025-10-10 15:55:02.130609',3,19,19);
INSERT INTO "evaluations_evaluationassignment" VALUES(51,'supervisor','completed',NULL,'2025-10-12 13:40:18.010587','2025-10-10 15:55:02.138433','2025-10-16 13:40:18.010778',3,19,2);
INSERT INTO "evaluations_evaluationassignment" VALUES(52,'peer','pending',NULL,NULL,'2025-10-10 15:55:02.146039','2025-10-10 15:55:02.146052',3,19,18);
INSERT INTO "evaluations_evaluationassignment" VALUES(53,'supervisor','pending',NULL,NULL,'2025-10-16 13:24:17.058644','2025-10-16 13:24:17.058658',3,15,2);
INSERT INTO "evaluations_evaluationassignment" VALUES(54,'peer','pending',NULL,NULL,'2025-10-16 13:24:17.069887','2025-10-16 13:24:17.069901',3,15,17);
INSERT INTO "evaluations_evaluationassignment" VALUES(55,'peer','completed',NULL,'2025-10-15 13:40:17.178556','2025-10-16 13:24:17.082045','2025-10-16 13:40:17.178677',3,17,15);
CREATE TABLE "evaluations_evaluationcampaign" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(200) NOT NULL, "description" text NOT NULL, "start_date" date NOT NULL, "end_date" date NOT NULL, "status" varchar(20) NOT NULL, "is_anonymous" bool NOT NULL, "allow_self_evaluation" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "created_by_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "weight_peer" decimal NOT NULL, "weight_self" decimal NOT NULL, "weight_subordinate" decimal NOT NULL, "weight_supervisor" decimal NOT NULL);
INSERT INTO "evaluations_evaluationcampaign" VALUES(1,'2025 İllik Qiymətləndirmə','2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə','2025-10-09','2025-10-16','draft',0,0,'2025-10-09 11:23:13.773067','2025-10-09 11:23:13.773085',1,20,20,10,50);
INSERT INTO "evaluations_evaluationcampaign" VALUES(2,'Q1 Performance Review','Q1 Performance ReviewQ1 Performance ReviewQ1 Performance ReviewQ1 Performance ReviewQ1 Performance Review','2025-10-13','2025-10-19','draft',0,0,'2025-10-09 23:16:13.391632','2025-10-16 10:58:26.940142',1,20,20,10,50);
INSERT INTO "evaluations_evaluationcampaign" VALUES(3,'2024 - İllik Performans Qiymətləndirməsi','2024-cü il illik performans qiymətləndirmə kampaniyası','2025-08-11','2025-11-09','active',1,1,'2025-10-10 15:55:01.480795','2025-10-10 15:55:01.480808',2,20,20,10,50);
INSERT INTO "evaluations_evaluationcampaign" VALUES(4,'2024 - Rüblük Qiymətləndirmə (Q3)','3-cü rüb üzrə qiymətləndirmə 1','2025-10-15','2025-10-19','completed',0,0,'2025-10-10 15:55:01.491491','2025-10-15 11:54:39.517000',2,20,20,10,50);
CREATE TABLE "evaluations_evaluationcampaign_target_departments" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "evaluationcampaign_id" bigint NOT NULL REFERENCES "evaluations_evaluationcampaign" ("id") DEFERRABLE INITIALLY DEFERRED, "department_id" bigint NOT NULL REFERENCES "departments_department" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "evaluations_evaluationcampaign_target_users" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "evaluationcampaign_id" bigint NOT NULL REFERENCES "evaluations_evaluationcampaign" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "evaluations_evaluationresult" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "overall_score" decimal NULL, "self_score" decimal NULL, "supervisor_score" decimal NULL, "peer_score" decimal NULL, "subordinate_score" decimal NULL, "total_evaluators" integer NOT NULL, "completion_rate" decimal NOT NULL, "is_finalized" bool NOT NULL, "finalized_at" datetime NULL, "calculated_at" datetime NOT NULL, "created_at" datetime NOT NULL, "campaign_id" bigint NOT NULL REFERENCES "evaluations_evaluationcampaign" ("id") DEFERRABLE INITIALLY DEFERRED, "evaluatee_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "evaluations_evaluationresult" VALUES(1,NULL,NULL,50,40,45,1,100,1,'2025-10-09 11:38:30','2025-10-09 11:42:19.930523','2025-10-09 11:38:32.614266',1,1);
INSERT INTO "evaluations_evaluationresult" VALUES(2,4.67,NULL,NULL,4.67,NULL,1,33.33,0,NULL,'2025-10-16 13:40:17.229062','2025-10-16 13:40:17.214644',3,17);
INSERT INTO "evaluations_evaluationresult" VALUES(3,NULL,NULL,NULL,NULL,NULL,0,0,0,NULL,'2025-10-16 13:40:18.038993','2025-10-16 13:40:18.039016',3,19);
CREATE TABLE "evaluations_historicalevaluationassignment" ("id" bigint NOT NULL, "relationship" varchar(20) NOT NULL, "status" varchar(20) NOT NULL, "started_at" datetime NULL, "completed_at" datetime NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "campaign_id" bigint NULL, "evaluatee_id" bigint NULL, "evaluator_id" bigint NULL, "history_user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(1,'self','in_progress','2025-10-09 11:41:09','2025-10-09 14:00:00','2025-10-09 11:41:24.270744','2025-10-09 11:41:24.270755',1,'2025-10-09 11:41:24.272923',NULL,'+',1,1,1,1);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(1,'self','in_progress','2025-10-09 11:41:09','2025-10-09 14:00:00','2025-10-09 11:41:24.270744','2025-10-09 11:42:16.419490',2,'2025-10-09 11:42:16.428626',NULL,'~',1,1,1,1);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(1,'self','completed','2025-10-09 11:41:09','2025-10-09 11:42:19.905649','2025-10-09 11:41:24.270744','2025-10-09 11:42:19.905794',3,'2025-10-09 11:42:19.914426',NULL,'~',1,1,1,1);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(1,'self','in_progress','2025-10-09 11:41:09','2025-10-09 11:42:19.905649','2025-10-09 11:41:24.270744','2025-10-10 15:48:10.702936',4,'2025-10-10 15:48:10.720070',NULL,'~',1,1,1,1);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(1,'self','in_progress','2025-10-09 11:41:09','2025-10-09 11:42:19.905649','2025-10-09 11:41:24.270744','2025-10-10 15:48:19.267383',5,'2025-10-10 15:48:19.281180',NULL,'~',1,1,1,1);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(2,'self','pending',NULL,NULL,'2025-10-10 15:55:01.730680','2025-10-10 15:55:01.730695',6,'2025-10-10 15:55:01.732031',NULL,'+',3,2,2,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(3,'peer','pending',NULL,NULL,'2025-10-10 15:55:01.740667','2025-10-10 15:55:01.740681',7,'2025-10-10 15:55:01.741796',NULL,'+',3,2,7,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(4,'peer','pending',NULL,NULL,'2025-10-10 15:55:01.748757','2025-10-10 15:55:01.748772',8,'2025-10-10 15:55:01.749863',NULL,'+',3,2,10,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(5,'peer','pending',NULL,NULL,'2025-10-10 15:55:01.756781','2025-10-10 15:55:01.756794',9,'2025-10-10 15:55:01.757826',NULL,'+',3,2,11,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(6,'self','pending',NULL,NULL,'2025-10-10 15:55:01.766557','2025-10-10 15:55:01.766572',10,'2025-10-10 15:55:01.767697',NULL,'+',3,7,7,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(7,'supervisor','pending',NULL,NULL,'2025-10-10 15:55:01.775017','2025-10-10 15:55:01.775032',11,'2025-10-10 15:55:01.776115',NULL,'+',3,7,2,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(8,'peer','pending',NULL,NULL,'2025-10-10 15:55:01.784339','2025-10-10 15:55:01.784352',12,'2025-10-10 15:55:01.785819',NULL,'+',3,7,10,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(9,'peer','pending',NULL,NULL,'2025-10-10 15:55:01.794017','2025-10-10 15:55:01.794032',13,'2025-10-10 15:55:01.795304',NULL,'+',3,7,11,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(10,'self','pending',NULL,NULL,'2025-10-10 15:55:01.802981','2025-10-10 15:55:01.802994',14,'2025-10-10 15:55:01.804000',NULL,'+',3,8,8,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(11,'supervisor','pending',NULL,NULL,'2025-10-10 15:55:01.811040','2025-10-10 15:55:01.811052',15,'2025-10-10 15:55:01.812022',NULL,'+',3,8,2,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(12,'peer','pending',NULL,NULL,'2025-10-10 15:55:01.820369','2025-10-10 15:55:01.820383',16,'2025-10-10 15:55:01.821516',NULL,'+',3,8,12,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(13,'peer','pending',NULL,NULL,'2025-10-10 15:55:01.828537','2025-10-10 15:55:01.828549',17,'2025-10-10 15:55:01.829779',NULL,'+',3,8,13,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(14,'peer','pending',NULL,NULL,'2025-10-10 15:55:01.837486','2025-10-10 15:55:01.837500',18,'2025-10-10 15:55:01.838763',NULL,'+',3,8,14,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(15,'self','pending',NULL,NULL,'2025-10-10 15:55:01.846225','2025-10-10 15:55:01.846240',19,'2025-10-10 15:55:01.847335',NULL,'+',3,9,9,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(16,'supervisor','pending',NULL,NULL,'2025-10-10 15:55:01.854236','2025-10-10 15:55:01.854250',20,'2025-10-10 15:55:01.855329',NULL,'+',3,9,2,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(17,'peer','pending',NULL,NULL,'2025-10-10 15:55:01.862315','2025-10-10 15:55:01.862327',21,'2025-10-10 15:55:01.863388',NULL,'+',3,9,15,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(18,'peer','pending',NULL,NULL,'2025-10-10 15:55:01.870409','2025-10-10 15:55:01.870423',22,'2025-10-10 15:55:01.871516',NULL,'+',3,9,16,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(19,'self','pending',NULL,NULL,'2025-10-10 15:55:01.878004','2025-10-10 15:55:01.878016',23,'2025-10-10 15:55:01.879209',NULL,'+',3,10,10,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(20,'supervisor','pending',NULL,NULL,'2025-10-10 15:55:01.892084','2025-10-10 15:55:01.892097',24,'2025-10-10 15:55:01.893196',NULL,'+',3,10,7,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(21,'peer','pending',NULL,NULL,'2025-10-10 15:55:01.900216','2025-10-10 15:55:01.900230',25,'2025-10-10 15:55:01.901272',NULL,'+',3,10,2,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(22,'peer','pending',NULL,NULL,'2025-10-10 15:55:01.908562','2025-10-10 15:55:01.908574',26,'2025-10-10 15:55:01.909544',NULL,'+',3,10,11,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(23,'self','pending',NULL,NULL,'2025-10-10 15:55:01.916270','2025-10-10 15:55:01.916282',27,'2025-10-10 15:55:01.917314',NULL,'+',3,11,11,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(24,'supervisor','pending',NULL,NULL,'2025-10-10 15:55:01.923932','2025-10-10 15:55:01.923945',28,'2025-10-10 15:55:01.924988',NULL,'+',3,11,7,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(25,'peer','pending',NULL,NULL,'2025-10-10 15:55:01.931723','2025-10-10 15:55:01.931736',29,'2025-10-10 15:55:01.932923',NULL,'+',3,11,2,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(26,'peer','pending',NULL,NULL,'2025-10-10 15:55:01.940307','2025-10-10 15:55:01.940319',30,'2025-10-10 15:55:01.941292',NULL,'+',3,11,10,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(27,'self','pending',NULL,NULL,'2025-10-10 15:55:01.948339','2025-10-10 15:55:01.948356',31,'2025-10-10 15:55:01.949364',NULL,'+',3,12,12,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(28,'supervisor','pending',NULL,NULL,'2025-10-10 15:55:01.956460','2025-10-10 15:55:01.956473',32,'2025-10-10 15:55:01.957503',NULL,'+',3,12,8,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(29,'peer','pending',NULL,NULL,'2025-10-10 15:55:01.964962','2025-10-10 15:55:01.964974',33,'2025-10-10 15:55:01.966002',NULL,'+',3,12,13,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(30,'peer','pending',NULL,NULL,'2025-10-10 15:55:01.972805','2025-10-10 15:55:01.972817',34,'2025-10-10 15:55:01.973817',NULL,'+',3,12,14,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(31,'self','pending',NULL,NULL,'2025-10-10 15:55:01.980607','2025-10-10 15:55:01.980619',35,'2025-10-10 15:55:01.981566',NULL,'+',3,13,13,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(32,'supervisor','pending',NULL,NULL,'2025-10-10 15:55:01.988498','2025-10-10 15:55:01.988511',36,'2025-10-10 15:55:01.989481',NULL,'+',3,13,8,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(33,'peer','pending',NULL,NULL,'2025-10-10 15:55:01.996753','2025-10-10 15:55:01.996763',37,'2025-10-10 15:55:01.998403',NULL,'+',3,13,12,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(34,'peer','pending',NULL,NULL,'2025-10-10 15:55:02.005399','2025-10-10 15:55:02.005412',38,'2025-10-10 15:55:02.006532',NULL,'+',3,13,14,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(35,'self','pending',NULL,NULL,'2025-10-10 15:55:02.013074','2025-10-10 15:55:02.013087',39,'2025-10-10 15:55:02.014112',NULL,'+',3,14,14,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(36,'supervisor','pending',NULL,NULL,'2025-10-10 15:55:02.020810','2025-10-10 15:55:02.020823',40,'2025-10-10 15:55:02.021913',NULL,'+',3,14,8,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(37,'peer','pending',NULL,NULL,'2025-10-10 15:55:02.029035','2025-10-10 15:55:02.029046',41,'2025-10-10 15:55:02.030075',NULL,'+',3,14,12,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(38,'peer','pending',NULL,NULL,'2025-10-10 15:55:02.037095','2025-10-10 15:55:02.037108',42,'2025-10-10 15:55:02.038090',NULL,'+',3,14,13,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(39,'self','pending',NULL,NULL,'2025-10-10 15:55:02.044624','2025-10-10 15:55:02.044637',43,'2025-10-10 15:55:02.045654',NULL,'+',3,15,15,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(40,'supervisor','pending',NULL,NULL,'2025-10-10 15:55:02.052221','2025-10-10 15:55:02.052233',44,'2025-10-10 15:55:02.053252',NULL,'+',3,15,9,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(41,'peer','pending',NULL,NULL,'2025-10-10 15:55:02.060389','2025-10-10 15:55:02.060399',45,'2025-10-10 15:55:02.061392',NULL,'+',3,15,16,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(42,'self','pending',NULL,NULL,'2025-10-10 15:55:02.067710','2025-10-10 15:55:02.067722',46,'2025-10-10 15:55:02.068748',NULL,'+',3,16,16,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(43,'supervisor','pending',NULL,NULL,'2025-10-10 15:55:02.075537','2025-10-10 15:55:02.075550',47,'2025-10-10 15:55:02.076691',NULL,'+',3,16,9,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(44,'peer','pending',NULL,NULL,'2025-10-10 15:55:02.084069','2025-10-10 15:55:02.084081',48,'2025-10-10 15:55:02.085130',NULL,'+',3,16,15,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(45,'self','pending',NULL,NULL,'2025-10-10 15:55:02.091869','2025-10-10 15:55:02.091882',49,'2025-10-10 15:55:02.093082',NULL,'+',3,17,17,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(46,'supervisor','pending',NULL,NULL,'2025-10-10 15:55:02.099710','2025-10-10 15:55:02.099721',50,'2025-10-10 15:55:02.100796',NULL,'+',3,17,2,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(47,'self','pending',NULL,NULL,'2025-10-10 15:55:02.107751','2025-10-10 15:55:02.107763',51,'2025-10-10 15:55:02.108812',NULL,'+',3,18,18,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(48,'supervisor','pending',NULL,NULL,'2025-10-10 15:55:02.115318','2025-10-10 15:55:02.115330',52,'2025-10-10 15:55:02.116312',NULL,'+',3,18,2,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(49,'peer','pending',NULL,NULL,'2025-10-10 15:55:02.123017','2025-10-10 15:55:02.123029',53,'2025-10-10 15:55:02.124077',NULL,'+',3,18,19,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(50,'self','pending',NULL,NULL,'2025-10-10 15:55:02.130597','2025-10-10 15:55:02.130609',54,'2025-10-10 15:55:02.131631',NULL,'+',3,19,19,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(51,'supervisor','pending',NULL,NULL,'2025-10-10 15:55:02.138433','2025-10-10 15:55:02.138444',55,'2025-10-10 15:55:02.139442',NULL,'+',3,19,2,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(52,'peer','pending',NULL,NULL,'2025-10-10 15:55:02.146039','2025-10-10 15:55:02.146052',56,'2025-10-10 15:55:02.147108',NULL,'+',3,19,18,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(1,'self','in_progress','2025-10-09 11:41:09','2025-10-09 11:42:19.905649','2025-10-09 11:41:24.270744','2025-10-10 20:55:50.278297',57,'2025-10-10 20:55:50.287982',NULL,'~',1,1,1,1);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(17,'peer','in_progress','2025-10-10 21:10:47.023115',NULL,'2025-10-10 15:55:01.862315','2025-10-10 21:10:47.023199',58,'2025-10-10 21:10:47.035439',NULL,'~',3,9,15,15);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(17,'peer','in_progress','2025-10-10 21:10:47.023115',NULL,'2025-10-10 15:55:01.862315','2025-10-10 21:10:58.359888',59,'2025-10-10 21:10:58.372535',NULL,'~',3,9,15,15);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(17,'peer','in_progress','2025-10-10 21:10:47.023115',NULL,'2025-10-10 15:55:01.862315','2025-10-10 21:11:03.786749',60,'2025-10-10 21:11:03.798782',NULL,'~',3,9,15,15);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(17,'peer','in_progress','2025-10-10 21:10:47.023115',NULL,'2025-10-10 15:55:01.862315','2025-10-10 21:11:10.052443',61,'2025-10-10 21:11:10.064000',NULL,'~',3,9,15,15);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(17,'peer','in_progress','2025-10-10 21:10:47.023115',NULL,'2025-10-10 15:55:01.862315','2025-10-10 21:11:14.423888',62,'2025-10-10 21:11:14.435462',NULL,'~',3,9,15,15);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(17,'peer','in_progress','2025-10-10 21:10:47.023115',NULL,'2025-10-10 15:55:01.862315','2025-10-10 21:11:34.772058',63,'2025-10-10 21:11:34.781225',NULL,'~',3,9,15,15);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(17,'peer','in_progress','2025-10-10 21:10:47.023115',NULL,'2025-10-10 15:55:01.862315','2025-10-10 21:11:38.996268',64,'2025-10-10 21:11:39.007470',NULL,'~',3,9,15,15);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(17,'peer','in_progress','2025-10-10 21:10:47.023115',NULL,'2025-10-10 15:55:01.862315','2025-10-10 21:11:49.524225',65,'2025-10-10 21:11:49.534866',NULL,'~',3,9,15,15);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(17,'peer','in_progress','2025-10-10 21:10:47.023115',NULL,'2025-10-10 15:55:01.862315','2025-10-10 21:11:53.416520',66,'2025-10-10 21:11:53.425778',NULL,'~',3,9,15,15);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(17,'peer','in_progress','2025-10-10 21:10:47.023115',NULL,'2025-10-10 15:55:01.862315','2025-10-10 21:11:58.893787',67,'2025-10-10 21:11:58.904085',NULL,'~',3,9,15,15);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(17,'peer','in_progress','2025-10-10 21:10:47.023115',NULL,'2025-10-10 15:55:01.862315','2025-10-10 21:12:02.837007',68,'2025-10-10 21:12:02.848121',NULL,'~',3,9,15,15);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(39,'self','in_progress','2025-10-10 21:13:13.103261',NULL,'2025-10-10 15:55:02.044624','2025-10-10 21:13:13.103323',69,'2025-10-10 21:13:13.115240',NULL,'~',3,15,15,15);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(39,'self','in_progress','2025-10-10 21:13:13.103261',NULL,'2025-10-10 15:55:02.044624','2025-10-10 21:13:27.782234',70,'2025-10-10 21:13:27.791432',NULL,'~',3,15,15,15);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(39,'self','in_progress','2025-10-10 21:13:13.103261',NULL,'2025-10-10 15:55:02.044624','2025-10-10 21:13:29.909042',71,'2025-10-10 21:13:29.919225',NULL,'~',3,15,15,15);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(53,'supervisor','pending',NULL,NULL,'2025-10-16 13:24:17.058644','2025-10-16 13:24:17.058658',72,'2025-10-16 13:24:17.061431',NULL,'+',3,15,2,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(54,'peer','pending',NULL,NULL,'2025-10-16 13:24:17.069887','2025-10-16 13:24:17.069901',73,'2025-10-16 13:24:17.071316',NULL,'+',3,15,17,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(55,'peer','pending',NULL,NULL,'2025-10-16 13:24:17.082045','2025-10-16 13:24:17.082057',74,'2025-10-16 13:24:17.083175',NULL,'+',3,17,15,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(55,'peer','completed',NULL,'2025-10-15 13:40:17.178556','2025-10-16 13:24:17.082045','2025-10-16 13:40:17.178677',75,'2025-10-16 13:40:17.204675',NULL,'~',3,17,15,NULL);
INSERT INTO "evaluations_historicalevaluationassignment" VALUES(51,'supervisor','completed',NULL,'2025-10-12 13:40:18.010587','2025-10-10 15:55:02.138433','2025-10-16 13:40:18.010778',76,'2025-10-16 13:40:18.024282',NULL,'~',3,19,2,NULL);
CREATE TABLE "evaluations_historicalevaluationcampaign" ("id" bigint NOT NULL, "title" varchar(200) NOT NULL, "description" text NOT NULL, "start_date" date NOT NULL, "end_date" date NOT NULL, "status" varchar(20) NOT NULL, "is_anonymous" bool NOT NULL, "allow_self_evaluation" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "created_by_id" bigint NULL, "history_user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "weight_peer" decimal NOT NULL, "weight_self" decimal NOT NULL, "weight_subordinate" decimal NOT NULL, "weight_supervisor" decimal NOT NULL);
INSERT INTO "evaluations_historicalevaluationcampaign" VALUES(1,'2025 İllik Qiymətləndirmə','2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə2024 İllik Qiymətləndirmə','2025-10-09','2025-10-16','draft',0,0,'2025-10-09 11:23:13.773067','2025-10-09 11:23:13.773085',1,'2025-10-09 11:23:13.784123',NULL,'+',1,1,20,20,10,50);
INSERT INTO "evaluations_historicalevaluationcampaign" VALUES(2,'Q1 Performance Review','Q1 Performance ReviewQ1 Performance ReviewQ1 Performance ReviewQ1 Performance ReviewQ1 Performance Review','2025-10-10','2025-10-11','draft',0,0,'2025-10-09 23:16:13.391632','2025-10-09 23:16:13.391661',2,'2025-10-09 23:16:13.402748',NULL,'+',1,1,20,20,10,50);
INSERT INTO "evaluations_historicalevaluationcampaign" VALUES(3,'2024 - İllik Performans Qiymətləndirməsi','2024-cü il illik performans qiymətləndirmə kampaniyası','2025-08-11','2025-11-09','active',1,1,'2025-10-10 15:55:01.480795','2025-10-10 15:55:01.480808',3,'2025-10-10 15:55:01.482197',NULL,'+',2,NULL,20,20,10,50);
INSERT INTO "evaluations_historicalevaluationcampaign" VALUES(4,'2024 - Rüblük Qiymətləndirmə (Q3)','3-cü rüb üzrə qiymətləndirmə','2025-06-12','2025-09-10','completed',1,1,'2025-10-10 15:55:01.491491','2025-10-10 15:55:01.491502',4,'2025-10-10 15:55:01.492544',NULL,'+',2,NULL,20,20,10,50);
INSERT INTO "evaluations_historicalevaluationcampaign" VALUES(4,'2024 - Rüblük Qiymətləndirmə (Q3)','3-cü rüb üzrə qiymətləndirmə 1','2025-10-15','2025-10-19','completed',0,0,'2025-10-10 15:55:01.491491','2025-10-15 11:54:39.517000',5,'2025-10-15 11:54:39.529813',NULL,'~',2,1,20,20,10,50);
INSERT INTO "evaluations_historicalevaluationcampaign" VALUES(2,'Q1 Performance Review','Q1 Performance ReviewQ1 Performance ReviewQ1 Performance ReviewQ1 Performance ReviewQ1 Performance Review','2025-10-13','2025-10-19','draft',0,0,'2025-10-09 23:16:13.391632','2025-10-16 10:58:26.940142',6,'2025-10-16 10:58:26.950658',NULL,'~',1,1,20,20,10,50);
CREATE TABLE "evaluations_historicalquestion" ("id" bigint NOT NULL, "text" text NOT NULL, "question_type" varchar(20) NOT NULL, "max_score" integer unsigned NOT NULL CHECK ("max_score" >= 0), "is_required" bool NOT NULL, "order" integer NOT NULL, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "category_id" bigint NULL, "history_user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "evaluations_historicalquestion" VALUES(1,'nazirlik','boolean',5,1,1,1,'2025-10-09 06:50:32.011459','2025-10-09 06:50:32.011479',1,'2025-10-09 06:50:32.015475',NULL,'+',1,1);
INSERT INTO "evaluations_historicalquestion" VALUES(2,'Komandaya aydın istiqamət və vizyon verir','scale',5,1,1,1,'2025-10-10 11:26:56.082003','2025-10-10 11:26:56.082020',2,'2025-10-10 11:26:56.083515',NULL,'+',2,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(3,'Qərarlar qəbul edərkən effektiv və vaxtında hərəkət edir','scale',5,1,2,1,'2025-10-10 11:26:56.092060','2025-10-10 11:26:56.092075',3,'2025-10-10 11:26:56.093125',NULL,'+',2,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(4,'Komanda üzvlərinə güvənir və səlahiyyət verir','scale',5,1,3,1,'2025-10-10 11:26:56.101978','2025-10-10 11:26:56.102003',4,'2025-10-10 11:26:56.103923',NULL,'+',2,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(5,'Dəyişikliklərə uyğunlaşma qabiliyyəti yüksəkdir','scale',5,1,4,1,'2025-10-10 11:26:56.112125','2025-10-10 11:26:56.112141',5,'2025-10-10 11:26:56.113258',NULL,'+',2,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(6,'Strateji düşüncə qabiliyyətinə sahibdir','scale',5,1,5,1,'2025-10-10 11:26:56.120429','2025-10-10 11:26:56.120446',6,'2025-10-10 11:26:56.121794',NULL,'+',2,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(7,'Məlumatları aydın və anlaşılan şəkildə çatdırır','scale',5,1,1,1,'2025-10-10 11:26:56.138833','2025-10-10 11:26:56.138853',7,'2025-10-10 11:26:56.139998',NULL,'+',3,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(8,'Aktiv dinləyici olaraq başqalarının fikirlərinə hörmət edir','scale',5,1,2,1,'2025-10-10 11:26:56.147294','2025-10-10 11:26:56.147309',8,'2025-10-10 11:26:56.148402',NULL,'+',3,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(9,'Yazılı kommunikasiya bacarıqları yüksəkdir','scale',5,1,3,1,'2025-10-10 11:26:56.155787','2025-10-10 11:26:56.155802',9,'2025-10-10 11:26:56.156934',NULL,'+',3,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(10,'Konflikt situasiyalarında effektiv ünsiyyət qurur','scale',5,1,4,1,'2025-10-10 11:26:56.164477','2025-10-10 11:26:56.164493',10,'2025-10-10 11:26:56.165563',NULL,'+',3,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(11,'Prezentasiya bacarıqları peşəkardır','scale',5,1,5,1,'2025-10-10 11:26:56.173419','2025-10-10 11:26:56.173434',11,'2025-10-10 11:26:56.174513',NULL,'+',3,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(12,'İşi üçün lazım olan texniki bilikləri tam əhatə edir','scale',5,1,1,1,'2025-10-10 11:26:56.192164','2025-10-10 11:26:56.192181',12,'2025-10-10 11:26:56.193374',NULL,'+',4,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(13,'Yeni texnologiyaları öyrənməyə açıqdır','scale',5,1,2,1,'2025-10-10 11:26:56.200455','2025-10-10 11:26:56.200471',13,'2025-10-10 11:26:56.201456',NULL,'+',4,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(14,'Problemləri texniki yanaşma ilə həll edir','scale',5,1,3,1,'2025-10-10 11:26:56.209415','2025-10-10 11:26:56.209432',14,'2025-10-10 11:26:56.210437',NULL,'+',4,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(15,'İşində keyfiyyət standartlarına riayət edir','scale',5,1,4,1,'2025-10-10 11:26:56.217514','2025-10-10 11:26:56.217530',15,'2025-10-10 11:26:56.218676',NULL,'+',4,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(16,'Texniki yenilikləri işə tətbiq edir','scale',5,1,5,1,'2025-10-10 11:26:56.227029','2025-10-10 11:26:56.227046',16,'2025-10-10 11:26:56.228313',NULL,'+',4,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(17,'Komanda üzvləri ilə əməkdaşlıq edir','scale',5,1,1,1,'2025-10-10 11:26:56.244369','2025-10-10 11:26:56.244385',17,'2025-10-10 11:26:56.245575',NULL,'+',5,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(18,'Digər şöbələrlə səmərəli iş qurur','scale',5,1,2,1,'2025-10-10 11:26:56.271185','2025-10-10 11:26:56.271205',18,'2025-10-10 11:26:56.272698',NULL,'+',5,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(19,'Komanda məqsədlərinə töhfə verir','scale',5,1,3,1,'2025-10-10 11:26:56.297920','2025-10-10 11:26:56.297935',19,'2025-10-10 11:26:56.299060',NULL,'+',5,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(20,'Komanda ruhunu dəstəkləyir','scale',5,1,4,1,'2025-10-10 11:26:56.312266','2025-10-10 11:26:56.312281',20,'2025-10-10 11:26:56.313258',NULL,'+',5,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(21,'Paylaşma və kömək mədəniyyətini dəstəkləyir','scale',5,1,5,1,'2025-10-10 11:26:56.320644','2025-10-10 11:26:56.320660',21,'2025-10-10 11:26:56.321694',NULL,'+',5,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(22,'Problemləri tez müəyyən edir','scale',5,1,1,1,'2025-10-10 11:26:56.336327','2025-10-10 11:26:56.336342',22,'2025-10-10 11:26:56.337454',NULL,'+',6,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(23,'Yaradıcı həll yolları tapır','scale',5,1,2,1,'2025-10-10 11:26:56.345381','2025-10-10 11:26:56.345400',23,'2025-10-10 11:26:56.346456',NULL,'+',6,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(24,'Analitik düşüncə qabiliyyəti güclüdür','scale',5,1,3,1,'2025-10-10 11:26:56.353413','2025-10-10 11:26:56.353429',24,'2025-10-10 11:26:56.354581',NULL,'+',6,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(25,'Qərar qəbul etmədə məntiqli yanaşır','scale',5,1,4,1,'2025-10-10 11:26:56.362012','2025-10-10 11:26:56.362028',25,'2025-10-10 11:26:56.363030',NULL,'+',6,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(26,'Nəticəyönümlü həllər təklif edir','scale',5,1,5,1,'2025-10-10 11:26:56.369903','2025-10-10 11:26:56.369920',26,'2025-10-10 11:26:56.371006',NULL,'+',6,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(27,'İşləri vaxtında tamamlayır','scale',5,1,1,1,'2025-10-10 11:26:56.387905','2025-10-10 11:26:56.387920',27,'2025-10-10 11:26:56.388913',NULL,'+',7,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(28,'Prioritetləri düzgün müəyyən edir','scale',5,1,2,1,'2025-10-10 11:26:56.396306','2025-10-10 11:26:56.396320',28,'2025-10-10 11:26:56.397342',NULL,'+',7,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(29,'Çoxsaylı tapşırıqları eyni vaxtda idarə edə bilir','scale',5,1,3,1,'2025-10-10 11:26:56.404733','2025-10-10 11:26:56.404748',29,'2025-10-10 11:26:56.405787',NULL,'+',7,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(30,'Son tarixlərə riayət edir','scale',5,1,4,1,'2025-10-10 11:26:56.413566','2025-10-10 11:26:56.413584',30,'2025-10-10 11:26:56.415021',NULL,'+',7,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(31,'İş yükünü effektiv planlaşdırır','scale',5,1,5,1,'2025-10-10 11:26:56.422382','2025-10-10 11:26:56.422397',31,'2025-10-10 11:26:56.423488',NULL,'+',7,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(32,'Yenilikçi ideya və təkliflər verir','scale',5,1,1,1,'2025-10-10 11:26:56.438855','2025-10-10 11:26:56.438871',32,'2025-10-10 11:26:56.440051',NULL,'+',8,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(33,'Mövcud prosesləri təkmilləşdirmək üçün çalışır','scale',5,1,2,1,'2025-10-10 11:26:56.447235','2025-10-10 11:26:56.447250',33,'2025-10-10 11:26:56.448292',NULL,'+',8,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(34,'Dəyişikliklərə açıqdır və dəstək verir','scale',5,1,3,1,'2025-10-10 11:26:56.455785','2025-10-10 11:26:56.455801',34,'2025-10-10 11:26:56.457495',NULL,'+',8,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(35,'Yaradıcı yanaşmalar təklif edir','scale',5,1,4,1,'2025-10-10 11:26:56.464716','2025-10-10 11:26:56.464731',35,'2025-10-10 11:26:56.465905',NULL,'+',8,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(36,'Risk götürməkdən çəkinmir','scale',5,1,5,1,'2025-10-10 11:26:56.473715','2025-10-10 11:26:56.473731',36,'2025-10-10 11:26:56.474835',NULL,'+',8,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(37,'İş etikasına riayət edir','scale',5,1,1,1,'2025-10-10 11:26:56.489863','2025-10-10 11:26:56.489879',37,'2025-10-10 11:26:56.491016',NULL,'+',9,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(38,'Məsuliyyətli və etibarlıdır','scale',5,1,2,1,'2025-10-10 11:26:56.498746','2025-10-10 11:26:56.498761',38,'2025-10-10 11:26:56.499849',NULL,'+',9,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(39,'Müştəri və ya daxili tərəfdaşlara xidmətdə keyfiyyətlidir','scale',5,1,3,1,'2025-10-10 11:26:56.507420','2025-10-10 11:26:56.507435',39,'2025-10-10 11:26:56.508423',NULL,'+',9,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(40,'Peşəkar davranış nümayiş etdirir','scale',5,1,4,1,'2025-10-10 11:26:56.515820','2025-10-10 11:26:56.515836',40,'2025-10-10 11:26:56.516981',NULL,'+',9,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(41,'Öz inkişafına diqqət yetirir','scale',5,1,5,1,'2025-10-10 11:26:56.524272','2025-10-10 11:26:56.524286',41,'2025-10-10 11:26:56.525368',NULL,'+',9,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(42,'Bu şəxsi iş yoldaşınız kimi tövsiyə edərdiniz?','boolean',5,1,0,1,'2025-10-10 11:26:56.542059','2025-10-10 11:26:56.542074',42,'2025-10-10 11:26:56.543124',NULL,'+',10,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(43,'Bu şəxs komandaya dəyərli töhfələr verir?','boolean',5,1,0,1,'2025-10-10 11:26:56.550219','2025-10-10 11:26:56.550234',43,'2025-10-10 11:26:56.551189',NULL,'+',10,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(44,'Bu şəxsin əsas güclü tərəfləri nələrdir?','text',5,0,0,1,'2025-10-10 11:26:56.558255','2025-10-10 11:26:56.558270',44,'2025-10-10 11:26:56.559386',NULL,'+',10,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(45,'İnkişaf etməli olduğu sahələr hansılardır?','text',5,0,0,1,'2025-10-10 11:26:56.571037','2025-10-10 11:26:56.571053',45,'2025-10-10 11:26:56.572019',NULL,'+',10,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(46,'Əlavə şərh və ya tövsiyələriniz:','text',5,0,0,1,'2025-10-10 11:26:56.581334','2025-10-10 11:26:56.581349',46,'2025-10-10 11:26:56.582615',NULL,'+',10,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(47,'Komanda üzvlərini motivasiya etmək və rəhbərlik etmək bacarığı','scale',5,1,0,1,'2025-10-10 15:55:01.350397','2025-10-10 15:55:01.350413',47,'2025-10-10 15:55:01.351725',NULL,'+',11,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(48,'Strateji düşüncə və qərar qəbul etmə bacarığı','scale',5,1,1,1,'2025-10-10 15:55:01.359020','2025-10-10 15:55:01.359034',48,'2025-10-10 15:55:01.360100',NULL,'+',11,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(49,'Aydın və effektiv ünsiyyət qurma bacarığı','scale',5,1,2,1,'2025-10-10 15:55:01.368804','2025-10-10 15:55:01.368821',49,'2025-10-10 15:55:01.369994',NULL,'+',3,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(50,'Komanda ilə əməkdaşlıq və koordinasiya','scale',5,1,3,1,'2025-10-10 15:55:01.379172','2025-10-10 15:55:01.379189',50,'2025-10-10 15:55:01.380562',NULL,'+',3,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(51,'Dinləmə və başqalarının fikirlərini qəbul etmə bacarığı','scale',5,1,4,1,'2025-10-10 15:55:01.387873','2025-10-10 15:55:01.387887',51,'2025-10-10 15:55:01.388841',NULL,'+',3,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(52,'Peşəkar bilik və bacarıqların səviyyəsi','scale',5,1,5,1,'2025-10-10 15:55:01.396355','2025-10-10 15:55:01.396370',52,'2025-10-10 15:55:01.397318',NULL,'+',9,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(53,'İşə məsuliyyətli və ciddi yanaşma','scale',5,1,6,1,'2025-10-10 15:55:01.403909','2025-10-10 15:55:01.403922',53,'2025-10-10 15:55:01.404844',NULL,'+',9,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(54,'Davamlı öyrənmə və inkişaf istəyi','scale',5,1,7,1,'2025-10-10 15:55:01.412268','2025-10-10 15:55:01.412321',54,'2025-10-10 15:55:01.414376',NULL,'+',9,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(55,'Problemləri təhlil edib həll yolları tapmaq bacarığı','scale',5,1,8,1,'2025-10-10 15:55:01.422055','2025-10-10 15:55:01.422070',55,'2025-10-10 15:55:01.423266',NULL,'+',12,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(56,'Yaradıcı və innovativ yanaşma','scale',5,1,9,1,'2025-10-10 15:55:01.430718','2025-10-10 15:55:01.430733',56,'2025-10-10 15:55:01.431723',NULL,'+',12,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(57,'Tapşırıqların vaxtında və keyfiyyətli yerinə yetirilməsi','scale',5,1,10,1,'2025-10-10 15:55:01.439123','2025-10-10 15:55:01.439138',57,'2025-10-10 15:55:01.440162',NULL,'+',13,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(58,'Məhsuldarlıq və effektivlik','scale',5,1,11,1,'2025-10-10 15:55:01.447840','2025-10-10 15:55:01.447855',58,'2025-10-10 15:55:01.448871',NULL,'+',13,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(59,'Bu şəxsin ən güclü tərəfləri hansılardır?','text',5,1,12,1,'2025-10-10 15:55:01.456307','2025-10-10 15:55:01.456323',59,'2025-10-10 15:55:01.457361',NULL,'+',11,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(60,'Hansı sahələrdə inkişaf etməlidir?','text',5,1,13,1,'2025-10-10 15:55:01.464232','2025-10-10 15:55:01.464247',60,'2025-10-10 15:55:01.465388',NULL,'+',11,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(61,'Əlavə rəy və təkliflər','text',5,0,14,1,'2025-10-10 15:55:01.472477','2025-10-10 15:55:01.472493',61,'2025-10-10 15:55:01.473424',NULL,'+',13,NULL);
INSERT INTO "evaluations_historicalquestion" VALUES(62,'İşçi komandaya effektiv rəhbərlik edir və komanda üzvlərini motivasiya edir','scale',5,1,1,1,'2025-10-15 07:47:48.693107','2025-10-15 07:47:48.693121',62,'2025-10-15 07:47:48.694959',NULL,'+',14,NULL);
CREATE TABLE "evaluations_question" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "text" text NOT NULL, "question_type" varchar(20) NOT NULL, "max_score" integer unsigned NOT NULL CHECK ("max_score" >= 0), "is_required" bool NOT NULL, "order" integer NOT NULL, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "category_id" bigint NOT NULL REFERENCES "evaluations_questioncategory" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "evaluations_question" VALUES(1,'nazirlik','boolean',5,1,1,1,'2025-10-09 06:50:32.011459','2025-10-09 06:50:32.011479',1);
INSERT INTO "evaluations_question" VALUES(2,'Komandaya aydın istiqamət və vizyon verir','scale',5,1,1,1,'2025-10-10 11:26:56.082003','2025-10-10 11:26:56.082020',2);
INSERT INTO "evaluations_question" VALUES(3,'Qərarlar qəbul edərkən effektiv və vaxtında hərəkət edir','scale',5,1,2,1,'2025-10-10 11:26:56.092060','2025-10-10 11:26:56.092075',2);
INSERT INTO "evaluations_question" VALUES(4,'Komanda üzvlərinə güvənir və səlahiyyət verir','scale',5,1,3,1,'2025-10-10 11:26:56.101978','2025-10-10 11:26:56.102003',2);
INSERT INTO "evaluations_question" VALUES(5,'Dəyişikliklərə uyğunlaşma qabiliyyəti yüksəkdir','scale',5,1,4,1,'2025-10-10 11:26:56.112125','2025-10-10 11:26:56.112141',2);
INSERT INTO "evaluations_question" VALUES(6,'Strateji düşüncə qabiliyyətinə sahibdir','scale',5,1,5,1,'2025-10-10 11:26:56.120429','2025-10-10 11:26:56.120446',2);
INSERT INTO "evaluations_question" VALUES(7,'Məlumatları aydın və anlaşılan şəkildə çatdırır','scale',5,1,1,1,'2025-10-10 11:26:56.138833','2025-10-10 11:26:56.138853',3);
INSERT INTO "evaluations_question" VALUES(8,'Aktiv dinləyici olaraq başqalarının fikirlərinə hörmət edir','scale',5,1,2,1,'2025-10-10 11:26:56.147294','2025-10-10 11:26:56.147309',3);
INSERT INTO "evaluations_question" VALUES(9,'Yazılı kommunikasiya bacarıqları yüksəkdir','scale',5,1,3,1,'2025-10-10 11:26:56.155787','2025-10-10 11:26:56.155802',3);
INSERT INTO "evaluations_question" VALUES(10,'Konflikt situasiyalarında effektiv ünsiyyət qurur','scale',5,1,4,1,'2025-10-10 11:26:56.164477','2025-10-10 11:26:56.164493',3);
INSERT INTO "evaluations_question" VALUES(11,'Prezentasiya bacarıqları peşəkardır','scale',5,1,5,1,'2025-10-10 11:26:56.173419','2025-10-10 11:26:56.173434',3);
INSERT INTO "evaluations_question" VALUES(12,'İşi üçün lazım olan texniki bilikləri tam əhatə edir','scale',5,1,1,1,'2025-10-10 11:26:56.192164','2025-10-10 11:26:56.192181',4);
INSERT INTO "evaluations_question" VALUES(13,'Yeni texnologiyaları öyrənməyə açıqdır','scale',5,1,2,1,'2025-10-10 11:26:56.200455','2025-10-10 11:26:56.200471',4);
INSERT INTO "evaluations_question" VALUES(14,'Problemləri texniki yanaşma ilə həll edir','scale',5,1,3,1,'2025-10-10 11:26:56.209415','2025-10-10 11:26:56.209432',4);
INSERT INTO "evaluations_question" VALUES(15,'İşində keyfiyyət standartlarına riayət edir','scale',5,1,4,1,'2025-10-10 11:26:56.217514','2025-10-10 11:26:56.217530',4);
INSERT INTO "evaluations_question" VALUES(16,'Texniki yenilikləri işə tətbiq edir','scale',5,1,5,1,'2025-10-10 11:26:56.227029','2025-10-10 11:26:56.227046',4);
INSERT INTO "evaluations_question" VALUES(17,'Komanda üzvləri ilə əməkdaşlıq edir','scale',5,1,1,1,'2025-10-10 11:26:56.244369','2025-10-10 11:26:56.244385',5);
INSERT INTO "evaluations_question" VALUES(18,'Digər şöbələrlə səmərəli iş qurur','scale',5,1,2,1,'2025-10-10 11:26:56.271185','2025-10-10 11:26:56.271205',5);
INSERT INTO "evaluations_question" VALUES(19,'Komanda məqsədlərinə töhfə verir','scale',5,1,3,1,'2025-10-10 11:26:56.297920','2025-10-10 11:26:56.297935',5);
INSERT INTO "evaluations_question" VALUES(20,'Komanda ruhunu dəstəkləyir','scale',5,1,4,1,'2025-10-10 11:26:56.312266','2025-10-10 11:26:56.312281',5);
INSERT INTO "evaluations_question" VALUES(21,'Paylaşma və kömək mədəniyyətini dəstəkləyir','scale',5,1,5,1,'2025-10-10 11:26:56.320644','2025-10-10 11:26:56.320660',5);
INSERT INTO "evaluations_question" VALUES(22,'Problemləri tez müəyyən edir','scale',5,1,1,1,'2025-10-10 11:26:56.336327','2025-10-10 11:26:56.336342',6);
INSERT INTO "evaluations_question" VALUES(23,'Yaradıcı həll yolları tapır','scale',5,1,2,1,'2025-10-10 11:26:56.345381','2025-10-10 11:26:56.345400',6);
INSERT INTO "evaluations_question" VALUES(24,'Analitik düşüncə qabiliyyəti güclüdür','scale',5,1,3,1,'2025-10-10 11:26:56.353413','2025-10-10 11:26:56.353429',6);
INSERT INTO "evaluations_question" VALUES(25,'Qərar qəbul etmədə məntiqli yanaşır','scale',5,1,4,1,'2025-10-10 11:26:56.362012','2025-10-10 11:26:56.362028',6);
INSERT INTO "evaluations_question" VALUES(26,'Nəticəyönümlü həllər təklif edir','scale',5,1,5,1,'2025-10-10 11:26:56.369903','2025-10-10 11:26:56.369920',6);
INSERT INTO "evaluations_question" VALUES(27,'İşləri vaxtında tamamlayır','scale',5,1,1,1,'2025-10-10 11:26:56.387905','2025-10-10 11:26:56.387920',7);
INSERT INTO "evaluations_question" VALUES(28,'Prioritetləri düzgün müəyyən edir','scale',5,1,2,1,'2025-10-10 11:26:56.396306','2025-10-10 11:26:56.396320',7);
INSERT INTO "evaluations_question" VALUES(29,'Çoxsaylı tapşırıqları eyni vaxtda idarə edə bilir','scale',5,1,3,1,'2025-10-10 11:26:56.404733','2025-10-10 11:26:56.404748',7);
INSERT INTO "evaluations_question" VALUES(30,'Son tarixlərə riayət edir','scale',5,1,4,1,'2025-10-10 11:26:56.413566','2025-10-10 11:26:56.413584',7);
INSERT INTO "evaluations_question" VALUES(31,'İş yükünü effektiv planlaşdırır','scale',5,1,5,1,'2025-10-10 11:26:56.422382','2025-10-10 11:26:56.422397',7);
INSERT INTO "evaluations_question" VALUES(32,'Yenilikçi ideya və təkliflər verir','scale',5,1,1,1,'2025-10-10 11:26:56.438855','2025-10-10 11:26:56.438871',8);
INSERT INTO "evaluations_question" VALUES(33,'Mövcud prosesləri təkmilləşdirmək üçün çalışır','scale',5,1,2,1,'2025-10-10 11:26:56.447235','2025-10-10 11:26:56.447250',8);
INSERT INTO "evaluations_question" VALUES(34,'Dəyişikliklərə açıqdır və dəstək verir','scale',5,1,3,1,'2025-10-10 11:26:56.455785','2025-10-10 11:26:56.455801',8);
INSERT INTO "evaluations_question" VALUES(35,'Yaradıcı yanaşmalar təklif edir','scale',5,1,4,1,'2025-10-10 11:26:56.464716','2025-10-10 11:26:56.464731',8);
INSERT INTO "evaluations_question" VALUES(36,'Risk götürməkdən çəkinmir','scale',5,1,5,1,'2025-10-10 11:26:56.473715','2025-10-10 11:26:56.473731',8);
INSERT INTO "evaluations_question" VALUES(37,'İş etikasına riayət edir','scale',5,1,1,1,'2025-10-10 11:26:56.489863','2025-10-10 11:26:56.489879',9);
INSERT INTO "evaluations_question" VALUES(38,'Məsuliyyətli və etibarlıdır','scale',5,1,2,1,'2025-10-10 11:26:56.498746','2025-10-10 11:26:56.498761',9);
INSERT INTO "evaluations_question" VALUES(39,'Müştəri və ya daxili tərəfdaşlara xidmətdə keyfiyyətlidir','scale',5,1,3,1,'2025-10-10 11:26:56.507420','2025-10-10 11:26:56.507435',9);
INSERT INTO "evaluations_question" VALUES(40,'Peşəkar davranış nümayiş etdirir','scale',5,1,4,1,'2025-10-10 11:26:56.515820','2025-10-10 11:26:56.515836',9);
INSERT INTO "evaluations_question" VALUES(41,'Öz inkişafına diqqət yetirir','scale',5,1,5,1,'2025-10-10 11:26:56.524272','2025-10-10 11:26:56.524286',9);
INSERT INTO "evaluations_question" VALUES(42,'Bu şəxsi iş yoldaşınız kimi tövsiyə edərdiniz?','boolean',5,1,0,1,'2025-10-10 11:26:56.542059','2025-10-10 11:26:56.542074',10);
INSERT INTO "evaluations_question" VALUES(43,'Bu şəxs komandaya dəyərli töhfələr verir?','boolean',5,1,0,1,'2025-10-10 11:26:56.550219','2025-10-10 11:26:56.550234',10);
INSERT INTO "evaluations_question" VALUES(44,'Bu şəxsin əsas güclü tərəfləri nələrdir?','text',5,0,0,1,'2025-10-10 11:26:56.558255','2025-10-10 11:26:56.558270',10);
INSERT INTO "evaluations_question" VALUES(45,'İnkişaf etməli olduğu sahələr hansılardır?','text',5,0,0,1,'2025-10-10 11:26:56.571037','2025-10-10 11:26:56.571053',10);
INSERT INTO "evaluations_question" VALUES(46,'Əlavə şərh və ya tövsiyələriniz:','text',5,0,0,1,'2025-10-10 11:26:56.581334','2025-10-10 11:26:56.581349',10);
INSERT INTO "evaluations_question" VALUES(47,'Komanda üzvlərini motivasiya etmək və rəhbərlik etmək bacarığı','scale',5,1,0,1,'2025-10-10 15:55:01.350397','2025-10-10 15:55:01.350413',11);
INSERT INTO "evaluations_question" VALUES(48,'Strateji düşüncə və qərar qəbul etmə bacarığı','scale',5,1,1,1,'2025-10-10 15:55:01.359020','2025-10-10 15:55:01.359034',11);
INSERT INTO "evaluations_question" VALUES(49,'Aydın və effektiv ünsiyyət qurma bacarığı','scale',5,1,2,1,'2025-10-10 15:55:01.368804','2025-10-10 15:55:01.368821',3);
INSERT INTO "evaluations_question" VALUES(50,'Komanda ilə əməkdaşlıq və koordinasiya','scale',5,1,3,1,'2025-10-10 15:55:01.379172','2025-10-10 15:55:01.379189',3);
INSERT INTO "evaluations_question" VALUES(51,'Dinləmə və başqalarının fikirlərini qəbul etmə bacarığı','scale',5,1,4,1,'2025-10-10 15:55:01.387873','2025-10-10 15:55:01.387887',3);
INSERT INTO "evaluations_question" VALUES(52,'Peşəkar bilik və bacarıqların səviyyəsi','scale',5,1,5,1,'2025-10-10 15:55:01.396355','2025-10-10 15:55:01.396370',9);
INSERT INTO "evaluations_question" VALUES(53,'İşə məsuliyyətli və ciddi yanaşma','scale',5,1,6,1,'2025-10-10 15:55:01.403909','2025-10-10 15:55:01.403922',9);
INSERT INTO "evaluations_question" VALUES(54,'Davamlı öyrənmə və inkişaf istəyi','scale',5,1,7,1,'2025-10-10 15:55:01.412268','2025-10-10 15:55:01.412321',9);
INSERT INTO "evaluations_question" VALUES(55,'Problemləri təhlil edib həll yolları tapmaq bacarığı','scale',5,1,8,1,'2025-10-10 15:55:01.422055','2025-10-10 15:55:01.422070',12);
INSERT INTO "evaluations_question" VALUES(56,'Yaradıcı və innovativ yanaşma','scale',5,1,9,1,'2025-10-10 15:55:01.430718','2025-10-10 15:55:01.430733',12);
INSERT INTO "evaluations_question" VALUES(57,'Tapşırıqların vaxtında və keyfiyyətli yerinə yetirilməsi','scale',5,1,10,1,'2025-10-10 15:55:01.439123','2025-10-10 15:55:01.439138',13);
INSERT INTO "evaluations_question" VALUES(58,'Məhsuldarlıq və effektivlik','scale',5,1,11,1,'2025-10-10 15:55:01.447840','2025-10-10 15:55:01.447855',13);
INSERT INTO "evaluations_question" VALUES(59,'Bu şəxsin ən güclü tərəfləri hansılardır?','text',5,1,12,1,'2025-10-10 15:55:01.456307','2025-10-10 15:55:01.456323',11);
INSERT INTO "evaluations_question" VALUES(60,'Hansı sahələrdə inkişaf etməlidir?','text',5,1,13,1,'2025-10-10 15:55:01.464232','2025-10-10 15:55:01.464247',11);
INSERT INTO "evaluations_question" VALUES(61,'Əlavə rəy və təkliflər','text',5,0,14,1,'2025-10-10 15:55:01.472477','2025-10-10 15:55:01.472493',13);
INSERT INTO "evaluations_question" VALUES(62,'İşçi komandaya effektiv rəhbərlik edir və komanda üzvlərini motivasiya edir','scale',5,1,1,1,'2025-10-15 07:47:48.693107','2025-10-15 07:47:48.693121',14);
CREATE TABLE "evaluations_questioncategory" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL UNIQUE, "description" text NOT NULL, "order" integer NOT NULL, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL);
INSERT INTO "evaluations_questioncategory" VALUES(1,'nazirlik','nazirliyə aid sullar',1,1,'2025-10-09 06:49:07.773755','2025-10-09 06:49:07.773778');
INSERT INTO "evaluations_questioncategory" VALUES(2,'Rəhbərlik','Rəhbərlik ilə bağlı qiymətləndirmə meyarları',0,1,'2025-10-10 11:26:56.072138','2025-10-10 11:26:56.072159');
INSERT INTO "evaluations_questioncategory" VALUES(3,'Kommunikasiya','Kommunikasiya ilə bağlı qiymətləndirmə meyarları',0,1,'2025-10-10 11:26:56.129399','2025-10-10 11:26:56.129416');
INSERT INTO "evaluations_questioncategory" VALUES(4,'Texniki Bacarıqlar','Texniki Bacarıqlar ilə bağlı qiymətləndirmə meyarları',0,1,'2025-10-10 11:26:56.182166','2025-10-10 11:26:56.182182');
INSERT INTO "evaluations_questioncategory" VALUES(5,'Komanda İşi','Komanda İşi ilə bağlı qiymətləndirmə meyarları',0,1,'2025-10-10 11:26:56.235897','2025-10-10 11:26:56.235913');
INSERT INTO "evaluations_questioncategory" VALUES(6,'Problemlərin Həlli','Problemlərin Həlli ilə bağlı qiymətləndirmə meyarları',8,1,'2025-10-10 11:26:56.328685','2025-10-10 20:46:14.420956');
INSERT INTO "evaluations_questioncategory" VALUES(7,'Vaxt İdarəetməsi','Vaxt İdarəetməsi ilə bağlı qiymətləndirmə meyarları',0,1,'2025-10-10 11:26:56.378361','2025-10-10 11:26:56.378376');
INSERT INTO "evaluations_questioncategory" VALUES(8,'İnnovasiya','İnnovasiya ilə bağlı qiymətləndirmə meyarları',0,1,'2025-10-10 11:26:56.430939','2025-10-10 11:26:56.430954');
INSERT INTO "evaluations_questioncategory" VALUES(9,'Peşəkarlıq','Peşəkarlıq ilə bağlı qiymətləndirmə meyarları',0,1,'2025-10-10 11:26:56.482163','2025-10-10 11:26:56.482179');
INSERT INTO "evaluations_questioncategory" VALUES(10,'Ümumi Qiymətləndirmə','Ümumi suallar',0,1,'2025-10-10 11:26:56.532745','2025-10-10 11:26:56.532760');
INSERT INTO "evaluations_questioncategory" VALUES(11,'Liderlik','Liderlik və komanda idarəetməsi bacarıqları',1,1,'2025-10-10 15:55:01.324737','2025-10-10 15:55:01.324754');
INSERT INTO "evaluations_questioncategory" VALUES(12,'Problem Həlli','Analitik düşüncə və problem həlli',4,1,'2025-10-10 15:55:01.334180','2025-10-10 15:55:01.334195');
INSERT INTO "evaluations_questioncategory" VALUES(13,'İş Nəticələri','Tapşırıqların yerinə yetirilməsi və nəticə',5,1,'2025-10-10 15:55:01.342459','2025-10-10 15:55:01.342475');
INSERT INTO "evaluations_questioncategory" VALUES(14,'Rəhbərlik və İdarəetmə','Rəhbərlik, liderlik və komanda idarəetməsi bacarıqları',1,1,'2025-10-15 07:47:48.683036','2025-10-15 07:47:48.683051');
CREATE TABLE "evaluations_response" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "score" integer NULL, "boolean_answer" bool NULL, "text_answer" text NOT NULL, "comment" text NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "assignment_id" bigint NOT NULL REFERENCES "evaluations_evaluationassignment" ("id") DEFERRABLE INITIALLY DEFERRED, "question_id" bigint NOT NULL REFERENCES "evaluations_question" ("id") DEFERRABLE INITIALLY DEFERRED, "sentiment_category" varchar(20) NOT NULL, "sentiment_score" real NOT NULL);
INSERT INTO "evaluations_response" VALUES(1,NULL,1,'','salam','2025-10-09 11:42:19.889225','2025-10-10 20:55:49.257682',1,1,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(2,3,NULL,'','','2025-10-10 15:55:02.157242','2025-10-10 15:55:02.157255',52,47,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(3,4,NULL,'','','2025-10-10 15:55:02.166066','2025-10-10 15:55:02.166079',52,48,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(4,4,NULL,'','','2025-10-10 15:55:02.173580','2025-10-10 15:55:02.173594',52,49,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(5,3,NULL,'','','2025-10-10 15:55:02.181577','2025-10-10 15:55:02.181590',52,50,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(6,5,NULL,'','','2025-10-10 15:55:02.189263','2025-10-10 15:55:02.189277',52,51,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(7,3,NULL,'','','2025-10-10 15:55:02.197180','2025-10-10 15:55:02.197193',52,52,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(8,3,NULL,'','','2025-10-10 15:55:02.204935','2025-10-10 15:55:02.204948',52,53,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(9,5,NULL,'','','2025-10-10 15:55:02.212645','2025-10-10 15:55:02.212657',52,54,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(10,3,NULL,'','','2025-10-10 15:55:02.220325','2025-10-10 15:55:02.220337',52,55,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(11,4,NULL,'','','2025-10-10 15:55:02.227949','2025-10-10 15:55:02.227962',52,56,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(12,4,NULL,'','','2025-10-10 15:55:02.235701','2025-10-10 15:55:02.235712',52,57,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(13,4,NULL,'','','2025-10-10 15:55:02.243677','2025-10-10 15:55:02.243689',52,58,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(14,2,NULL,'','a','2025-10-10 21:12:00.674674','2025-10-10 21:12:16.631349',17,48,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(15,5,NULL,'','','2025-10-10 21:13:28.118414','2025-10-10 21:13:30.158610',39,48,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(16,5,NULL,'','','2025-10-10 21:13:28.130313','2025-10-10 21:13:30.170800',39,47,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(17,5,NULL,'','','2025-10-10 21:13:28.140323','2025-10-10 21:13:30.182163',39,49,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(18,5,NULL,'','','2025-10-10 21:13:28.150361','2025-10-10 21:13:30.191122',39,50,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(19,5,NULL,'','','2025-10-10 21:13:28.163183','2025-10-10 21:13:30.201169',39,51,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(20,5,NULL,'','','2025-10-10 21:13:28.172538','2025-10-10 21:13:30.210651',39,52,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(21,5,NULL,'','','2025-10-10 21:13:28.179454','2025-10-10 21:13:30.220896',39,53,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(22,5,NULL,'','','2025-10-10 21:13:28.186474','2025-10-10 21:13:30.230084',39,54,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(23,5,NULL,'','','2025-10-10 21:13:28.196207','2025-10-10 21:13:30.240168',39,55,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(24,5,NULL,'','','2025-10-10 21:13:28.202860','2025-10-10 21:13:30.249673',39,56,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(25,5,NULL,'','','2025-10-10 21:13:28.210147','2025-10-10 21:13:30.258621',39,57,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(26,5,NULL,'','','2025-10-10 21:13:28.216817','2025-10-10 21:13:30.267698',39,58,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(27,NULL,NULL,'əla','əla','2025-10-10 21:13:28.223443','2025-10-10 21:13:30.277672',39,59,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(28,4,NULL,'','','2025-10-16 13:24:17.101357','2025-10-16 13:24:17.101374',55,48,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(29,5,NULL,'','','2025-10-16 13:24:17.113796','2025-10-16 13:24:17.113812',55,47,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(30,5,NULL,'','','2025-10-16 13:24:17.124693','2025-10-16 13:24:17.124707',55,49,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(31,5,NULL,'','','2025-10-16 13:24:17.134594','2025-10-16 13:24:17.134609',55,50,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(32,4,NULL,'','','2025-10-16 13:24:17.144467','2025-10-16 13:24:17.144483',55,51,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(33,5,NULL,'','','2025-10-16 13:24:17.154264','2025-10-16 13:24:17.154277',55,52,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(34,5,NULL,'','','2025-10-16 13:24:17.163782','2025-10-16 13:24:17.163798',55,53,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(35,4,NULL,'','','2025-10-16 13:24:17.172342','2025-10-16 13:24:17.172356',55,54,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(36,5,NULL,'','','2025-10-16 13:24:17.181437','2025-10-16 13:24:17.181452',55,55,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(37,5,NULL,'','','2025-10-16 13:24:17.189696','2025-10-16 13:24:17.189711',55,56,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(38,4,NULL,'','','2025-10-16 13:24:17.198715','2025-10-16 13:24:17.198730',55,57,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(39,5,NULL,'','','2025-10-16 13:24:17.207781','2025-10-16 13:24:17.207795',55,58,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(40,NULL,NULL,'Məhsuldarlıq, effektivlik, dəqiqlik','','2025-10-16 13:40:16.967296','2025-10-16 13:43:36.823333',55,59,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(41,NULL,NULL,'Stres idarəetməsi üzərində işləməlidir.','','2025-10-16 13:40:17.153319','2025-10-16 13:43:36.599467',55,60,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(42,NULL,NULL,'İşə ciddi yanaşır, tapşırıqları vaxtında və keyfiyyətli yerinə yetirir.','','2025-10-16 13:40:17.167743','2025-10-16 13:43:35.357628',55,61,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(43,2,NULL,'','','2025-10-16 13:40:17.240024','2025-10-16 13:40:17.240038',54,48,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(44,2,NULL,'','','2025-10-16 13:40:17.250659','2025-10-16 13:40:17.250673',54,47,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(45,2,NULL,'','','2025-10-16 13:40:17.259749','2025-10-16 13:40:17.259763',54,49,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(46,2,NULL,'','','2025-10-16 13:40:17.269952','2025-10-16 13:40:17.269967',54,50,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(47,3,NULL,'','','2025-10-16 13:40:17.279508','2025-10-16 13:40:17.279524',54,51,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(48,2,NULL,'','','2025-10-16 13:40:17.288741','2025-10-16 13:40:17.288756',54,52,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(49,3,NULL,'','','2025-10-16 13:40:17.299410','2025-10-16 13:40:17.299427',54,53,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(50,3,NULL,'','','2025-10-16 13:40:17.322786','2025-10-16 13:40:17.322804',54,54,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(55,NULL,NULL,'Liderlik, komanda idarəetməsi, strateji düşüncə','','2025-10-16 13:40:17.370769','2025-10-16 13:43:37.077737',54,59,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(56,NULL,NULL,'Bəzi hallarda daha çox təşəbbüskarlıq göstərə bilər.','','2025-10-16 13:40:17.408624','2025-10-16 13:43:36.366453',54,60,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(57,NULL,NULL,'Komanda ilə əla əməkdaşlıq edir, həmişə köməyə hazırdır.','','2025-10-16 13:40:17.419553','2025-10-16 13:43:37.176363',54,61,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(58,4,NULL,'','','2025-10-16 13:40:17.432655','2025-10-16 13:40:17.432672',53,48,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(59,4,NULL,'','','2025-10-16 13:40:17.457995','2025-10-16 13:40:17.458012',53,47,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(60,5,NULL,'','','2025-10-16 13:40:17.467969','2025-10-16 13:40:17.467985',53,49,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(61,5,NULL,'','','2025-10-16 13:40:17.477152','2025-10-16 13:40:17.477166',53,50,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(62,5,NULL,'','','2025-10-16 13:40:17.486744','2025-10-16 13:40:17.486760',53,51,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(63,4,NULL,'','','2025-10-16 13:40:17.497044','2025-10-16 13:40:17.497059',53,52,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(64,4,NULL,'','','2025-10-16 13:40:17.508837','2025-10-16 13:40:17.508854',53,53,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(65,4,NULL,'','','2025-10-16 13:40:17.537791','2025-10-16 13:40:17.537807',53,54,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(66,4,NULL,'','','2025-10-16 13:40:17.548259','2025-10-16 13:40:17.548273',53,55,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(67,4,NULL,'','','2025-10-16 13:40:17.564586','2025-10-16 13:40:17.564603',53,56,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(68,5,NULL,'','','2025-10-16 13:40:17.574950','2025-10-16 13:40:17.574967',53,57,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(69,4,NULL,'','','2025-10-16 13:40:17.584459','2025-10-16 13:40:17.584474',53,58,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(70,NULL,NULL,'Məhsuldarlıq, effektivlik, dəqiqlik','','2025-10-16 13:40:17.595992','2025-10-16 13:43:36.284751',53,59,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(71,NULL,NULL,'Vaxt idarəetməsini təkmilləşdirmək lazımdır.','','2025-10-16 13:40:17.622795','2025-10-16 13:43:35.555856',53,60,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(72,NULL,NULL,'Liderlik keyfiyyətləri çox güclüdür, komandanı yaxşı motivasiya edir.','','2025-10-16 13:40:17.637816','2025-10-16 13:43:32.632600',53,61,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(73,NULL,NULL,'Məhsuldarlıq, effektivlik, dəqiqlik','','2025-10-16 13:40:17.733967','2025-10-16 13:43:36.394185',52,59,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(74,NULL,NULL,'Vaxt idarəetməsini təkmilləşdirmək lazımdır.','','2025-10-16 13:40:17.746247','2025-10-16 13:43:30.751021',52,60,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(75,NULL,NULL,'Kommunikasiya bacarıqları əladır, hamı ilə rahat ünsiyyət qurur.','','2025-10-16 13:40:17.760644','2025-10-16 13:43:33.559584',52,61,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(76,3,NULL,'','','2025-10-16 13:40:17.793262','2025-10-16 13:40:17.793281',51,48,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(77,2,NULL,'','','2025-10-16 13:40:17.812127','2025-10-16 13:40:17.812144',51,47,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(78,3,NULL,'','','2025-10-16 13:40:17.823970','2025-10-16 13:40:17.823987',51,49,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(79,2,NULL,'','','2025-10-16 13:40:17.836321','2025-10-16 13:40:17.836338',51,50,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(80,2,NULL,'','','2025-10-16 13:40:17.849799','2025-10-16 13:40:17.849823',51,51,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(81,2,NULL,'','','2025-10-16 13:40:17.865627','2025-10-16 13:40:17.865656',51,52,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(82,2,NULL,'','','2025-10-16 13:40:17.893556','2025-10-16 13:40:17.893575',51,53,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(83,3,NULL,'','','2025-10-16 13:40:17.904052','2025-10-16 13:40:17.904066',51,54,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(84,3,NULL,'','','2025-10-16 13:40:17.919200','2025-10-16 13:40:17.919218',51,55,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(85,2,NULL,'','','2025-10-16 13:40:17.932270','2025-10-16 13:40:17.932288',51,56,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(86,3,NULL,'','','2025-10-16 13:40:17.944628','2025-10-16 13:40:17.944644',51,57,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(87,2,NULL,'','','2025-10-16 13:40:17.958040','2025-10-16 13:40:17.958059',51,58,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(88,NULL,NULL,'Liderlik, komanda idarəetməsi, strateji düşüncə','','2025-10-16 13:40:17.969080','2025-10-16 13:43:34.556898',51,59,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(89,NULL,NULL,'Vaxt idarəetməsini təkmilləşdirmək lazımdır.','','2025-10-16 13:40:17.982365','2025-10-16 13:43:31.807898',51,60,'neutral',0.0);
INSERT INTO "evaluations_response" VALUES(90,NULL,NULL,'Innovativ fikirləri və yaradıcı yanaşması ilə seçilir.','','2025-10-16 13:40:17.997517','2025-10-16 13:43:36.711949',51,61,'neutral',0.0);
CREATE TABLE "leave_attendance_attendance" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "date" date NOT NULL, "status" varchar(20) NOT NULL, "check_in" time NULL, "check_out" time NULL, "work_hours" decimal NULL, "late_minutes" integer NOT NULL, "early_leave_minutes" integer NOT NULL, "notes" text NOT NULL, "verified_at" datetime NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "leave_request_id" bigint NULL REFERENCES "leave_attendance_leaverequest" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "verified_by_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "leave_attendance_historicalattendance" ("id" bigint NOT NULL, "date" date NOT NULL, "status" varchar(20) NOT NULL, "check_in" time NULL, "check_out" time NULL, "work_hours" decimal NULL, "late_minutes" integer NOT NULL, "early_leave_minutes" integer NOT NULL, "notes" text NOT NULL, "verified_at" datetime NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "history_user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "leave_request_id" bigint NULL, "user_id" bigint NULL, "verified_by_id" bigint NULL);
CREATE TABLE "leave_attendance_historicalholiday" ("id" bigint NOT NULL, "name" varchar(200) NOT NULL, "date" date NOT NULL, "holiday_type" varchar(20) NOT NULL, "is_recurring" bool NOT NULL, "description" text NOT NULL, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "history_user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "leave_attendance_historicalholiday" VALUES(1,'test','2025-10-16','public',1,'11111111111',1,'2025-10-16 07:39:50.202346','2025-10-16 07:39:50.202370',1,'2025-10-16 07:39:50.205478',NULL,'+',1);
CREATE TABLE "leave_attendance_historicalleavebalance" ("id" bigint NOT NULL, "year" integer NOT NULL, "entitled_days" decimal NOT NULL, "used_days" decimal NOT NULL, "pending_days" decimal NOT NULL, "carried_forward_days" decimal NOT NULL, "notes" text NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "history_user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "leave_type_id" bigint NULL, "user_id" bigint NULL);
INSERT INTO "leave_attendance_historicalleavebalance" VALUES(1,2025,42,15,10,5,'gghghjg','2025-10-16 08:22:58.391672','2025-10-16 08:22:58.391693',1,'2025-10-16 08:22:58.395026',NULL,'+',1,1,20);
CREATE TABLE "leave_attendance_historicalleaverequest" ("id" bigint NOT NULL, "start_date" date NOT NULL, "end_date" date NOT NULL, "number_of_days" decimal NOT NULL, "reason" text NOT NULL, "status" varchar(20) NOT NULL, "attachment" text NULL, "approved_at" datetime NULL, "rejection_reason" text NOT NULL, "is_half_day_start" bool NOT NULL, "is_half_day_end" bool NOT NULL, "emergency" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "approved_by_id" bigint NULL, "history_user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "leave_type_id" bigint NULL, "user_id" bigint NULL);
INSERT INTO "leave_attendance_historicalleaverequest" VALUES(1,'2025-10-16','2025-10-20',4,'keyfim bilir lan','pending','',NULL,'451232659878',1,1,0,'2025-10-16 08:24:52.801165','2025-10-16 08:24:52.801182',1,'2025-10-16 08:24:52.805046',NULL,'+',2,1,2,20);
INSERT INTO "leave_attendance_historicalleaverequest" VALUES(1,'2025-10-16','2025-10-20',4,'keyfim bilir lan','approved','','2025-10-15 20:00:00','451232659878',1,1,0,'2025-10-16 08:24:52.801165','2025-10-16 11:29:56.655515',2,'2025-10-16 11:29:56.684285',NULL,'~',1,1,2,20);
CREATE TABLE "leave_attendance_historicalleavetype" ("id" bigint NOT NULL, "name" varchar(100) NOT NULL, "code" varchar(20) NOT NULL, "description" text NOT NULL, "days_per_year" decimal NOT NULL, "max_consecutive_days" integer NULL, "is_paid" bool NOT NULL, "requires_approval" bool NOT NULL, "requires_document" bool NOT NULL, "carry_forward" bool NOT NULL, "max_carry_forward_days" integer NULL, "notice_days" integer NOT NULL, "color_code" varchar(7) NOT NULL, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "history_user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "leave_attendance_historicalleavetype" VALUES(1,'əmək','01','1111111111111115555555555555',42,5,1,1,1,0,NULL,5,'#3B82F6',1,'2025-10-16 08:20:11.265973','2025-10-16 08:20:11.265997',1,'2025-10-16 08:20:11.269019',NULL,'+',1);
INSERT INTO "leave_attendance_historicalleavetype" VALUES(1,'əmək','01','1111111111111115555555555555',42,5,1,1,1,1,5,5,'#3B82F6',1,'2025-10-16 08:20:11.265973','2025-10-16 08:20:37.493061',2,'2025-10-16 08:20:37.496771',NULL,'~',1);
INSERT INTO "leave_attendance_historicalleavetype" VALUES(2,'sosial','02','əmək məzuniyyəti',14,3,1,1,1,1,3,3,'#3B82F6',1,'2025-10-16 08:21:48.425446','2025-10-16 08:21:48.425469',3,'2025-10-16 08:21:48.428219',NULL,'+',1);
CREATE TABLE "leave_attendance_holiday" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(200) NOT NULL, "date" date NOT NULL, "holiday_type" varchar(20) NOT NULL, "is_recurring" bool NOT NULL, "description" text NOT NULL, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL);
INSERT INTO "leave_attendance_holiday" VALUES(1,'test','2025-10-16','public',1,'11111111111',1,'2025-10-16 07:39:50.202346','2025-10-16 07:39:50.202370');
CREATE TABLE "leave_attendance_leavebalance" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "year" integer NOT NULL, "entitled_days" decimal NOT NULL, "used_days" decimal NOT NULL, "pending_days" decimal NOT NULL, "carried_forward_days" decimal NOT NULL, "notes" text NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "leave_type_id" bigint NOT NULL REFERENCES "leave_attendance_leavetype" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "leave_attendance_leavebalance" VALUES(1,2025,42,15,10,5,'gghghjg','2025-10-16 08:22:58.391672','2025-10-16 08:22:58.391693',1,20);
CREATE TABLE "leave_attendance_leaverequest" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "start_date" date NOT NULL, "end_date" date NOT NULL, "number_of_days" decimal NOT NULL, "reason" text NOT NULL, "status" varchar(20) NOT NULL, "attachment" varchar(100) NULL, "approved_at" datetime NULL, "rejection_reason" text NOT NULL, "is_half_day_start" bool NOT NULL, "is_half_day_end" bool NOT NULL, "emergency" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "approved_by_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "leave_type_id" bigint NOT NULL REFERENCES "leave_attendance_leavetype" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "leave_attendance_leaverequest" VALUES(1,'2025-10-16','2025-10-20',4,'keyfim bilir lan','approved','','2025-10-15 20:00:00','451232659878',1,1,0,'2025-10-16 08:24:52.801165','2025-10-16 11:29:56.655515',1,2,20);
CREATE TABLE "leave_attendance_leavetype" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL UNIQUE, "code" varchar(20) NOT NULL UNIQUE, "description" text NOT NULL, "days_per_year" decimal NOT NULL, "max_consecutive_days" integer NULL, "is_paid" bool NOT NULL, "requires_approval" bool NOT NULL, "requires_document" bool NOT NULL, "carry_forward" bool NOT NULL, "max_carry_forward_days" integer NULL, "notice_days" integer NOT NULL, "color_code" varchar(7) NOT NULL, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL);
INSERT INTO "leave_attendance_leavetype" VALUES(1,'əmək','01','1111111111111115555555555555',42,5,1,1,1,1,5,5,'#3B82F6',1,'2025-10-16 08:20:11.265973','2025-10-16 08:20:37.493061');
INSERT INTO "leave_attendance_leavetype" VALUES(2,'sosial','02','əmək məzuniyyəti',14,3,1,1,1,1,3,3,'#3B82F6',1,'2025-10-16 08:21:48.425446','2025-10-16 08:21:48.425469');
CREATE TABLE "notifications_bulknotification" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(200) NOT NULL, "message" text NOT NULL, "recipients_count" integer NOT NULL, "filter_criteria" text NOT NULL CHECK ((JSON_VALID("filter_criteria") OR "filter_criteria" IS NULL)), "status" varchar(20) NOT NULL, "channels" text NOT NULL CHECK ((JSON_VALID("channels") OR "channels" IS NULL)), "sent_count" integer NOT NULL, "failed_count" integer NOT NULL, "created_at" datetime NOT NULL, "completed_at" datetime NULL, "initiated_by_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "notifications_emaillog" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "recipient_email" varchar(254) NOT NULL, "subject" varchar(200) NOT NULL, "status" varchar(20) NOT NULL, "error_message" text NOT NULL, "sent_at" datetime NULL, "opened_at" datetime NULL, "clicked_at" datetime NULL, "created_at" datetime NOT NULL, "recipient_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "template_id" bigint NULL REFERENCES "notifications_emailtemplate" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "notifications_emaillog" VALUES(1,'muradoffcode@gmail.com','aaaaaaaaaaaaaaaa','sent','aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',NULL,NULL,NULL,'2025-10-09 23:28:19.454416',1,1);
INSERT INTO "notifications_emaillog" VALUES(2,'muradofftehmez01@gmail.com','aaaaaaaaaaaaaaaa','sent','aaaaaaaaaaaaaaaaaaa',NULL,NULL,NULL,'2025-10-16 21:33:00.995912',1,1);
CREATE TABLE "notifications_emailtemplate" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL UNIQUE, "subject" varchar(200) NOT NULL, "html_content" text NOT NULL, "text_content" text NOT NULL, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL);
INSERT INTO "notifications_emailtemplate" VALUES(1,'AzAgroPOS','aaaaaaaaaaaaaaaa','aaaaaaaaa','aaaaaaaaa',1,'2025-10-09 12:05:19.808200','2025-10-10 20:44:47.373228');
INSERT INTO "notifications_emailtemplate" VALUES(2,'aaaaaaaaaaaaaaaaa','aaaaaaaaaaaaaaaaaaaaaaaaaaa','aaaaaaaaaaaaaaaaaaaaz','zzzzzzzzzzzzzzzzzz',1,'2025-10-10 20:45:00.669990','2025-10-10 20:45:00.670006');
CREATE TABLE "notifications_notification" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(200) NOT NULL, "message" text NOT NULL, "notification_type" varchar(20) NOT NULL, "is_read" bool NOT NULL, "link" varchar(500) NOT NULL, "created_at" datetime NOT NULL, "read_at" datetime NULL, "user_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "channel" varchar(20) NOT NULL, "content_type_id" integer NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "object_id" integer unsigned NULL CHECK ("object_id" >= 0), "priority" varchar(20) NOT NULL, "scheduled_time" datetime NULL, "sent_at" datetime NULL);
INSERT INTO "notifications_notification" VALUES(1569,'Test Bildirişi','Bu tətbiqin artırılmış bildiriş funksiyasını test etmək üçün bir test bildirişidir.','info',0,'/dashboard/','2025-10-17 17:13:37.250426',NULL,31,'in_app',NULL,NULL,'normal',NULL,NULL);
INSERT INTO "notifications_notification" VALUES(1570,'Kanal Testi','Bu bildiriş bütün mövcud kanallar üzrə test üçün göndərilir.','announcement',0,'','2025-10-17 17:14:46.945852',NULL,31,'push',NULL,NULL,'normal',NULL,NULL);
INSERT INTO "notifications_notification" VALUES(1571,'Kütləvi Test','Bu kütləvi bildiriş testidir.','info',0,'','2025-10-17 17:15:55.964619',NULL,31,'in_app',NULL,NULL,'normal',NULL,NULL);
CREATE TABLE "notifications_notificationmethod" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(50) NOT NULL UNIQUE, "method_type" varchar(20) NOT NULL, "is_active" bool NOT NULL, "configuration" text NOT NULL CHECK ((JSON_VALID("configuration") OR "configuration" IS NULL)), "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL);
CREATE TABLE "notifications_notificationtemplate" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL UNIQUE, "trigger" varchar(50) NOT NULL, "subject" varchar(200) NOT NULL, "email_content" text NOT NULL, "sms_content" varchar(160) NOT NULL, "push_content" varchar(200) NOT NULL, "inapp_content" text NOT NULL, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL);
INSERT INTO "notifications_notificationtemplate" VALUES(1,'Test Template','general_announcement','Yeni Bildiriş: {{ title }}','<p>Salam {{ user_name }},</p><p>{{ message }}</p>','Yeni bildiriş: {{ message }}','Yeni bildiriş: {{ title }}','Yeni bildiriş: {{ message }}',1,'2025-10-17 17:11:48.243396','2025-10-17 17:11:48.243412');
CREATE TABLE "notifications_notificationtemplate_methods" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "notificationtemplate_id" bigint NOT NULL REFERENCES "notifications_notificationtemplate" ("id") DEFERRABLE INITIALLY DEFERRED, "notificationmethod_id" bigint NOT NULL REFERENCES "notifications_notificationmethod" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "notifications_pushnotification" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(200) NOT NULL, "message" text NOT NULL, "data" text NOT NULL CHECK ((JSON_VALID("data") OR "data" IS NULL)), "status" varchar(20) NOT NULL, "error_message" text NOT NULL, "sent_at" datetime NULL, "created_at" datetime NOT NULL, "user_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "notifications_smslog" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "recipient_phone" varchar(20) NOT NULL, "message" text NOT NULL, "status" varchar(20) NOT NULL, "external_id" varchar(100) NOT NULL, "error_message" text NOT NULL, "sent_at" datetime NULL, "delivered_at" datetime NULL, "created_at" datetime NOT NULL, "recipient_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "provider_id" bigint NULL REFERENCES "notifications_smsprovider" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "notifications_smsprovider" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL UNIQUE, "provider" varchar(20) NOT NULL, "is_active" bool NOT NULL, "configuration" text NOT NULL CHECK ((JSON_VALID("configuration") OR "configuration" IS NULL)), "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL);
INSERT INTO "notifications_smsprovider" VALUES(1,'Test Provider','twilio',1,'{"account_sid": "test_sid", "auth_token": "test_token", "from_number": "+1234567890"}','2025-10-17 17:11:48.253059','2025-10-17 17:11:48.253077');
CREATE TABLE "notifications_usernotificationpreference" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "email_notifications" bool NOT NULL, "email_assignment" bool NOT NULL, "email_reminder" bool NOT NULL, "email_announcement" bool NOT NULL, "email_security" bool NOT NULL, "sms_notifications" bool NOT NULL, "sms_important_only" bool NOT NULL, "sms_assignment" bool NOT NULL, "sms_reminder" bool NOT NULL, "sms_security" bool NOT NULL, "push_notifications" bool NOT NULL, "push_assignment" bool NOT NULL, "push_reminder" bool NOT NULL, "push_announcement" bool NOT NULL, "dnd_start_time" time NULL, "dnd_end_time" time NULL, "weekend_notifications" bool NOT NULL, "weekday_start" time NOT NULL, "weekday_end" time NOT NULL, "user_id" bigint NOT NULL UNIQUE REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "notifications_usernotificationpreference" VALUES(1,1,1,1,1,1,0,1,0,0,1,1,1,1,1,NULL,NULL,1,'08:00:00','18:00:00',31);
INSERT INTO "notifications_usernotificationpreference" VALUES(2,1,1,1,1,1,0,1,0,0,1,1,1,1,1,NULL,NULL,1,'08:00:00','18:00:00',1);
CREATE TABLE "recruitment_application" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "first_name" varchar(100) NOT NULL, "last_name" varchar(100) NOT NULL, "email" varchar(254) NOT NULL, "phone" varchar(20) NOT NULL, "resume" varchar(100) NOT NULL, "cover_letter" text NOT NULL, "portfolio_url" varchar(200) NOT NULL, "status" varchar(20) NOT NULL, "source" varchar(20) NOT NULL, "current_position" varchar(200) NOT NULL, "years_of_experience" decimal NULL, "expected_salary" decimal NULL, "notice_period_days" integer NULL, "rating" integer NULL, "notes" text NOT NULL, "applied_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "assigned_to_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "job_posting_id" bigint NOT NULL REFERENCES "recruitment_jobposting" ("id") DEFERRABLE INITIALLY DEFERRED, "referrer_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "recruitment_application" VALUES(1,'Tahmaz','Muradov','muradoffcode@gmail.com','0605536990','resumes/2025/10/Sertifikat_.pdf','ssssssssssssssssssssss','','offer','agency','it',5,450,15,3,'aaaaaaaaaaaaaaa','2025-10-16 12:56:10.169834','2025-10-16 23:04:21.472802',24,1,29);
CREATE TABLE "recruitment_historicalapplication" ("id" bigint NOT NULL, "first_name" varchar(100) NOT NULL, "last_name" varchar(100) NOT NULL, "email" varchar(254) NOT NULL, "phone" varchar(20) NOT NULL, "resume" text NOT NULL, "cover_letter" text NOT NULL, "portfolio_url" varchar(200) NOT NULL, "status" varchar(20) NOT NULL, "source" varchar(20) NOT NULL, "current_position" varchar(200) NOT NULL, "years_of_experience" decimal NULL, "expected_salary" decimal NULL, "notice_period_days" integer NULL, "rating" integer NULL, "notes" text NOT NULL, "applied_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "assigned_to_id" bigint NULL, "history_user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "job_posting_id" bigint NULL, "referrer_id" bigint NULL);
INSERT INTO "recruitment_historicalapplication" VALUES(1,'Tahmaz','Muradov','muradoffcode@gmail.com','0605536990','resumes/2025/10/Sertifikat_.pdf','ssssssssssssssssssssss','','assessment','agency','it',5,450,15,3,'aaaaaaaaaaaaaaa','2025-10-16 12:56:10.169834','2025-10-16 12:56:10.169851',1,'2025-10-16 12:56:10.171711',NULL,'+',24,1,1,29);
INSERT INTO "recruitment_historicalapplication" VALUES(1,'Tahmaz','Muradov','muradoffcode@gmail.com','0605536990','resumes/2025/10/Sertifikat_.pdf','ssssssssssssssssssssss','','offer','agency','it',5,450,15,3,'aaaaaaaaaaaaaaa','2025-10-16 12:56:10.169834','2025-10-16 23:04:21.472802',2,'2025-10-16 23:04:21.486423',NULL,'~',24,1,1,29);
CREATE TABLE "recruitment_historicalinterview" ("id" bigint NOT NULL, "interview_type" varchar(20) NOT NULL, "scheduled_date" datetime NOT NULL, "duration_minutes" integer NOT NULL, "location" varchar(200) NOT NULL, "meeting_link" varchar(200) NOT NULL, "status" varchar(20) NOT NULL, "feedback" text NOT NULL, "rating" integer NULL, "recommendation" varchar(20) NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "application_id" bigint NULL, "created_by_id" bigint NULL, "history_user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "recruitment_historicaljobposting" ("id" bigint NOT NULL, "title" varchar(200) NOT NULL, "code" varchar(50) NOT NULL, "description" text NOT NULL, "responsibilities" text NOT NULL, "requirements" text NOT NULL, "qualifications" text NOT NULL, "employment_type" varchar(20) NOT NULL, "experience_level" varchar(20) NOT NULL, "number_of_positions" integer NOT NULL, "salary_min" decimal NULL, "salary_max" decimal NULL, "salary_currency" varchar(3) NOT NULL, "show_salary" bool NOT NULL, "location" varchar(200) NOT NULL, "remote_allowed" bool NOT NULL, "status" varchar(20) NOT NULL, "posted_date" date NULL, "closing_date" date NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "created_by_id" bigint NULL, "department_id" bigint NULL, "hiring_manager_id" bigint NULL, "history_user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "recruitment_historicaljobposting" VALUES(1,'it','01','gəl','aaaaaaaaaaaaaaaaaa','aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','full_time','mid',5,500,600,'AZN',1,'naxçıvan',1,'open','2025-10-16','2025-10-31','2025-10-16 12:54:32.925304','2025-10-16 12:54:32.925321',1,'2025-10-16 12:54:32.927606',NULL,'+',20,2,20,1);
INSERT INTO "recruitment_historicaljobposting" VALUES(1,'it','01','gəl','trtrtrt','aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','full_time','mid',5,500,600,'AZN',1,'naxçıvan',1,'open','2025-10-16','2025-10-31','2025-10-16 12:54:32.925304','2025-10-16 22:24:41.208488',2,'2025-10-16 22:24:41.220080',NULL,'~',20,2,20,1);
CREATE TABLE "recruitment_historicaloffer" ("id" bigint NOT NULL, "position_title" varchar(200) NOT NULL, "salary" decimal NOT NULL, "currency" varchar(3) NOT NULL, "bonus_potential" decimal NULL, "benefits" text NOT NULL, "start_date" date NULL, "status" varchar(20) NOT NULL, "sent_date" date NULL, "expiry_date" date NULL, "response_date" date NULL, "offer_letter" text NULL, "notes" text NOT NULL, "approved_at" datetime NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "application_id" bigint NULL, "approved_by_id" bigint NULL, "created_by_id" bigint NULL, "history_user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "recruitment_historicaloffer" VALUES(1,'aaaaaaaaaa',5000,'AZN',45,'aaaaaaaaaaaaa','2025-10-16','negotiating','2025-10-16','2025-10-19','2025-10-16','','aaaaaaaaaaaaa','2025-10-16 12:57:17','2025-10-16 12:57:26.061524','2025-10-16 12:57:26.061536',1,'2025-10-16 12:57:26.064242',NULL,'+',1,11,2,1);
CREATE TABLE "recruitment_historicalonboardingtask" ("id" bigint NOT NULL, "title" varchar(200) NOT NULL, "description" text NOT NULL, "category" varchar(100) NOT NULL, "status" varchar(20) NOT NULL, "due_date" date NULL, "completed_date" date NULL, "notes" text NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "application_id" bigint NULL, "assigned_to_id" bigint NULL, "history_user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "new_hire_id" bigint NULL);
CREATE TABLE "recruitment_interview" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "interview_type" varchar(20) NOT NULL, "scheduled_date" datetime NOT NULL, "duration_minutes" integer NOT NULL, "location" varchar(200) NOT NULL, "meeting_link" varchar(200) NOT NULL, "status" varchar(20) NOT NULL, "feedback" text NOT NULL, "rating" integer NULL, "recommendation" varchar(20) NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "application_id" bigint NOT NULL REFERENCES "recruitment_application" ("id") DEFERRABLE INITIALLY DEFERRED, "created_by_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "recruitment_interview_interviewers" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "interview_id" bigint NOT NULL REFERENCES "recruitment_interview" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "recruitment_jobposting" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(200) NOT NULL, "code" varchar(50) NOT NULL UNIQUE, "description" text NOT NULL, "responsibilities" text NOT NULL, "requirements" text NOT NULL, "qualifications" text NOT NULL, "employment_type" varchar(20) NOT NULL, "experience_level" varchar(20) NOT NULL, "number_of_positions" integer NOT NULL, "salary_min" decimal NULL, "salary_max" decimal NULL, "salary_currency" varchar(3) NOT NULL, "show_salary" bool NOT NULL, "location" varchar(200) NOT NULL, "remote_allowed" bool NOT NULL, "status" varchar(20) NOT NULL, "posted_date" date NULL, "closing_date" date NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "created_by_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "department_id" bigint NOT NULL REFERENCES "departments_department" ("id") DEFERRABLE INITIALLY DEFERRED, "hiring_manager_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "recruitment_jobposting" VALUES(1,'it','01','gəl','trtrtrt','aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','full_time','mid',5,500,600,'AZN',1,'naxçıvan',1,'open','2025-10-16','2025-10-31','2025-10-16 12:54:32.925304','2025-10-16 22:24:41.208488',20,2,20);
CREATE TABLE "recruitment_jobposting_recruiters" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "jobposting_id" bigint NOT NULL REFERENCES "recruitment_jobposting" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "recruitment_jobposting_recruiters" VALUES(1,1,1);
INSERT INTO "recruitment_jobposting_recruiters" VALUES(2,1,2);
INSERT INTO "recruitment_jobposting_recruiters" VALUES(3,1,3);
INSERT INTO "recruitment_jobposting_recruiters" VALUES(4,1,4);
INSERT INTO "recruitment_jobposting_recruiters" VALUES(5,1,5);
INSERT INTO "recruitment_jobposting_recruiters" VALUES(6,1,6);
INSERT INTO "recruitment_jobposting_recruiters" VALUES(7,1,7);
INSERT INTO "recruitment_jobposting_recruiters" VALUES(8,1,8);
INSERT INTO "recruitment_jobposting_recruiters" VALUES(9,1,9);
INSERT INTO "recruitment_jobposting_recruiters" VALUES(10,1,10);
INSERT INTO "recruitment_jobposting_recruiters" VALUES(11,1,11);
INSERT INTO "recruitment_jobposting_recruiters" VALUES(12,1,12);
INSERT INTO "recruitment_jobposting_recruiters" VALUES(13,1,13);
INSERT INTO "recruitment_jobposting_recruiters" VALUES(14,1,14);
INSERT INTO "recruitment_jobposting_recruiters" VALUES(15,1,15);
INSERT INTO "recruitment_jobposting_recruiters" VALUES(16,1,16);
INSERT INTO "recruitment_jobposting_recruiters" VALUES(17,1,17);
INSERT INTO "recruitment_jobposting_recruiters" VALUES(18,1,18);
INSERT INTO "recruitment_jobposting_recruiters" VALUES(19,1,19);
INSERT INTO "recruitment_jobposting_recruiters" VALUES(20,1,20);
INSERT INTO "recruitment_jobposting_recruiters" VALUES(21,1,21);
INSERT INTO "recruitment_jobposting_recruiters" VALUES(22,1,22);
INSERT INTO "recruitment_jobposting_recruiters" VALUES(23,1,23);
INSERT INTO "recruitment_jobposting_recruiters" VALUES(24,1,24);
INSERT INTO "recruitment_jobposting_recruiters" VALUES(25,1,25);
INSERT INTO "recruitment_jobposting_recruiters" VALUES(26,1,26);
INSERT INTO "recruitment_jobposting_recruiters" VALUES(27,1,27);
INSERT INTO "recruitment_jobposting_recruiters" VALUES(28,1,28);
INSERT INTO "recruitment_jobposting_recruiters" VALUES(29,1,29);
CREATE TABLE "recruitment_offer" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "position_title" varchar(200) NOT NULL, "salary" decimal NOT NULL, "currency" varchar(3) NOT NULL, "bonus_potential" decimal NULL, "benefits" text NOT NULL, "start_date" date NULL, "status" varchar(20) NOT NULL, "sent_date" date NULL, "expiry_date" date NULL, "response_date" date NULL, "offer_letter" varchar(100) NULL, "notes" text NOT NULL, "approved_at" datetime NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "application_id" bigint NOT NULL REFERENCES "recruitment_application" ("id") DEFERRABLE INITIALLY DEFERRED, "approved_by_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "created_by_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "recruitment_offer" VALUES(1,'aaaaaaaaaa',5000,'AZN',45,'aaaaaaaaaaaaa','2025-10-16','negotiating','2025-10-16','2025-10-19','2025-10-16','','aaaaaaaaaaaaa','2025-10-16 12:57:17','2025-10-16 12:57:26.061524','2025-10-16 12:57:26.061536',1,11,2);
CREATE TABLE "recruitment_onboardingtask" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(200) NOT NULL, "description" text NOT NULL, "category" varchar(100) NOT NULL, "status" varchar(20) NOT NULL, "due_date" date NULL, "completed_date" date NULL, "notes" text NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "application_id" bigint NOT NULL REFERENCES "recruitment_application" ("id") DEFERRABLE INITIALLY DEFERRED, "assigned_to_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "new_hire_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "reports_radarchartdata" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "category" varchar(100) NOT NULL, "self_score" decimal NULL, "others_score" decimal NULL, "created_at" datetime NOT NULL, "campaign_id" bigint NOT NULL REFERENCES "evaluations_evaluationcampaign" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "reports_radarchartdata" VALUES(1,'usersd',0.01,0.01,'2025-10-09 12:06:20.036108',1,1);
CREATE TABLE "reports_report" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "report_type" varchar(20) NOT NULL, "title" varchar(200) NOT NULL, "file_path" varchar(100) NOT NULL, "data" text NOT NULL CHECK ((JSON_VALID("data") OR "data" IS NULL)), "created_at" datetime NOT NULL, "campaign_id" bigint NOT NULL REFERENCES "evaluations_evaluationcampaign" ("id") DEFERRABLE INITIALLY DEFERRED, "generated_by_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "generated_for_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "reports_reportgenerationlog" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "report_type" varchar(20) NOT NULL, "status" varchar(20) NOT NULL, "file" varchar(100) NULL, "metadata" text NOT NULL CHECK ((JSON_VALID("metadata") OR "metadata" IS NULL)), "error_message" text NOT NULL, "created_at" datetime NOT NULL, "completed_at" datetime NULL, "requested_by_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "reports_reportgenerationlog" VALUES(1,'pdf','processing','','{}','','2025-10-15 21:30:08.832403',NULL,1);
CREATE TABLE "reports_systemkpi" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "date" date NOT NULL UNIQUE, "total_users" integer NOT NULL, "active_users" integer NOT NULL, "new_users_today" integer NOT NULL, "users_logged_in_today" integer NOT NULL, "total_campaigns" integer NOT NULL, "active_campaigns" integer NOT NULL, "total_evaluations" integer NOT NULL, "completed_evaluations" integer NOT NULL, "evaluations_completed_today" integer NOT NULL, "completion_rate" decimal NOT NULL, "total_departments" integer NOT NULL, "total_trainings" integer NOT NULL, "active_trainings" integer NOT NULL, "login_attempts_today" integer NOT NULL, "failed_login_attempts_today" integer NOT NULL, "security_threats_detected" integer NOT NULL, "average_response_time" decimal NOT NULL, "database_size_mb" decimal NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL);
INSERT INTO "reports_systemkpi" VALUES(1,'2025-10-16',30,30,1,0,4,1,55,2,0,3.64,10,7,1,0,0,0,0,0,'2025-10-16 17:50:23.132533','2025-10-16 17:50:23.132556');
INSERT INTO "reports_systemkpi" VALUES(2,'2025-10-17',30,30,0,0,4,1,55,2,0,3.64,10,7,1,0,0,0,0,0,'2025-10-16 21:21:58.369088','2025-10-16 21:21:58.369107');
CREATE TABLE "support_supportticket" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(200) NOT NULL, "description" text NOT NULL, "status" varchar(20) NOT NULL, "priority" varchar(20) NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "resolved_at" datetime NULL, "assigned_to_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "created_by_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "support_supportticket" VALUES(1,'1','11','open','urgent','2025-10-11 18:00:21.672106','2025-10-16 21:29:44.864506',NULL,1,2);
INSERT INTO "support_supportticket" VALUES(2,'tecili','aaaaaaaaaaaaa','open','high','2025-10-16 21:28:33.312027','2025-10-16 21:28:33.312047',NULL,1,1);
CREATE TABLE "support_ticketcomment" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "comment" text NOT NULL, "is_internal" bool NOT NULL, "created_at" datetime NOT NULL, "created_by_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "ticket_id" bigint NOT NULL REFERENCES "support_supportticket" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "support_ticketcomment" VALUES(1,'4444444444444444444444444',1,'2025-10-11 18:01:00.400738',1,1);
INSERT INTO "support_ticketcomment" VALUES(2,'zzzzzzzzzzzzzzzzzzzz',1,'2025-10-16 21:28:33.316088',15,2);
INSERT INTO "support_ticketcomment" VALUES(3,'zzzzzzzzzzzzzzzzzzz',1,'2025-10-16 21:28:33.317467',29,2);
INSERT INTO "support_ticketcomment" VALUES(4,'zzzzzzzzzzzzzzaaaaaaaaaaaaaaa',1,'2025-10-16 21:28:33.317825',6,2);
INSERT INTO "support_ticketcomment" VALUES(5,'xsxs',1,'2025-10-16 21:28:33.318212',16,2);
INSERT INTO "support_ticketcomment" VALUES(6,'süsüsü',1,'2025-10-16 21:29:44.875875',1,1);
CREATE TABLE "training_historicaltrainingresource" ("id" bigint NOT NULL, "title" varchar(300) NOT NULL, "description" text NOT NULL, "type" varchar(20) NOT NULL, "is_online" bool NOT NULL, "delivery_method" varchar(20) NOT NULL, "link" varchar(200) NOT NULL, "difficulty_level" varchar(20) NOT NULL, "duration_hours" decimal NULL, "language" varchar(50) NOT NULL, "provider" varchar(200) NOT NULL, "instructor" varchar(200) NOT NULL, "cost" decimal NULL, "max_participants" integer NULL, "is_active" bool NOT NULL, "is_mandatory" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "history_user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "training_historicaltrainingresource" VALUES(1,'Liderlik Əsasları','Effektiv liderlik prinsipləri və komanda idarəetməsi üzrə təlim','course',1,'online','https://example.com/leadership','intermediate',16,'Azərbaycan','Q360 Academy','Dr. Əli Məmmədov',250,NULL,1,0,'2025-10-11 07:49:07.262343','2025-10-11 07:49:07.262374',1,'2025-10-11 07:49:07.264954',NULL,'+',NULL);
INSERT INTO "training_historicaltrainingresource" VALUES(2,'Effektiv Kommunikasiya Bacarıqları','Şifahi və yazılı ünsiyyət bacarıqlarının inkişafı','workshop',0,'offline','','beginner',8,'Azərbaycan','BizSkills Training Center','Nigar Həsənova',150,NULL,1,0,'2025-10-11 07:49:07.270008','2025-10-11 07:49:07.270025',2,'2025-10-11 07:49:07.270206',NULL,'+',NULL);
INSERT INTO "training_historicaltrainingresource" VALUES(3,'Problem Həlli və Kritik Düşüncə','Analitik düşüncə və yaradıcı problem həlli texnikaları','course',1,'hybrid','https://example.com/problem-solving','advanced',24,'Azərbaycan','Q360 Academy','Prof. Rəşid Quliyev',350,NULL,1,0,'2025-10-11 07:49:07.271886','2025-10-11 07:49:07.271905',3,'2025-10-11 07:49:07.272047',NULL,'+',NULL);
INSERT INTO "training_historicaltrainingresource" VALUES(4,'Müştəri Xidməti Mükəmməlliyi','Müştəri məmnuniyyəti və xidmət keyfiyyətinin artırılması','webinar',1,'online','https://example.com/customer-service','intermediate',4,'Azərbaycan','Service Excellence Institute','Aynur Əliyeva',75,NULL,1,0,'2025-10-11 07:49:07.274443','2025-10-11 07:49:07.274462',4,'2025-10-11 07:49:07.274587',NULL,'+',NULL);
INSERT INTO "training_historicaltrainingresource" VALUES(5,'Vaxt İdarəetməsi və Məhsuldarlıq','Effektiv vaxt planlaması və prioritet müəyyənləşdirmə','self_study',1,'online','https://example.com/time-management','beginner',6,'Azərbaycan','Productivity Pro','Kamran Məmmədov',0,NULL,1,1,'2025-10-11 07:49:07.277084','2025-10-11 07:49:07.277095',5,'2025-10-11 07:49:07.277207',NULL,'+',NULL);
INSERT INTO "training_historicaltrainingresource" VALUES(6,'Texniki Bacarıqların İnkişafı','Sahə üzrə texniki bilik və praktiki tətbiq','certification',1,'online','https://example.com/technical-skills','expert',40,'İngilis','Tech Academy','International Experts',500,NULL,1,0,'2025-10-11 07:49:07.278365','2025-10-11 07:49:07.278375',6,'2025-10-11 07:49:07.278482',NULL,'+',NULL);
INSERT INTO "training_historicaltrainingresource" VALUES(1,'Liderlik Əsasları','Effektiv liderlik prinsipləri və komanda idarəetməsi üzrə təlim','course',1,'online','https://example.com/leadership','intermediate',16,'Azərbaycan','Q360 Academy','Dr. Əli Məmmədov',250,NULL,1,1,'2025-10-11 07:49:07.262343','2025-10-11 08:09:57.207662',7,'2025-10-11 08:09:57.211006',NULL,'~',1);
INSERT INTO "training_historicaltrainingresource" VALUES(7,'Python ilə Proqramlaşdırma - Əsaslar','Python proqramlaşdırma dilinin əsasları','course',1,'online','https://www.udemy.com/course/python-programming/','beginner',40,'İngilis','Udemy','',150,NULL,1,0,'2025-10-15 07:47:48.705638','2025-10-15 07:47:48.705651',8,'2025-10-15 07:47:48.707301',NULL,'+',NULL);
INSERT INTO "training_historicaltrainingresource" VALUES(4,'Müştəri Xidməti Mükəmməlliyi','Müştəri məmnuniyyəti və xidmət keyfiyyətinin artırılması','webinar',1,'online','https://example.com/customer-service','intermediate',4,'Azərbaycan','Service Excellence Institute','Aynur Əliyeva',75,NULL,1,0,'2025-10-11 07:49:07.274443','2025-10-15 11:52:50.764734',9,'2025-10-15 11:52:50.769969',NULL,'~',1);
INSERT INTO "training_historicaltrainingresource" VALUES(2,'Effektiv Kommunikasiya Bacarıqları','Şifahi və yazılı ünsiyyət bacarıqlarının inkişafı','webinar',1,'hybrid','','intermediate',8,'Azərbaycan','BizSkills Training Center','Nigar Həsənova',150,100,1,1,'2025-10-11 07:49:07.270008','2025-10-15 11:53:40.057972',10,'2025-10-15 11:53:40.061545',NULL,'~',1);
CREATE TABLE "training_historicalusertraining" ("id" bigint NOT NULL, "assignment_type" varchar(30) NOT NULL, "start_date" date NULL, "due_date" date NULL, "completed_date" date NULL, "status" varchar(20) NOT NULL, "progress_percentage" integer NOT NULL, "completion_note" text NOT NULL, "user_feedback" text NOT NULL, "rating" integer NULL, "certificate_url" varchar(200) NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "assigned_by_id" bigint NULL, "history_user_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "related_goal_id" bigint NULL, "user_id" bigint NULL, "resource_id" bigint NULL);
INSERT INTO "training_historicalusertraining" VALUES(1,'manager_assigned','2025-10-11','2025-10-30',NULL,'in_progress',11,'əla','əla',2,'','2025-10-11 08:11:25.205695','2025-10-11 08:11:25.205715',1,'2025-10-11 08:11:25.208036',NULL,'+',2,1,1,1,1);
INSERT INTO "training_historicalusertraining" VALUES(2,'system_recommended','2025-10-14',NULL,NULL,'pending',0,'','',NULL,'','2025-10-14 22:15:31.016315','2025-10-14 22:15:31.016329',2,'2025-10-14 22:15:31.016984',NULL,'+',NULL,1,NULL,1,3);
INSERT INTO "training_historicalusertraining" VALUES(3,'system_recommended','2025-10-14',NULL,NULL,'pending',0,'','',NULL,'','2025-10-14 22:15:31.513678','2025-10-14 22:15:31.513695',3,'2025-10-14 22:15:31.514068',NULL,'+',NULL,1,NULL,1,6);
CREATE TABLE "training_trainingresource" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(300) NOT NULL, "description" text NOT NULL, "type" varchar(20) NOT NULL, "is_online" bool NOT NULL, "delivery_method" varchar(20) NOT NULL, "link" varchar(200) NOT NULL, "difficulty_level" varchar(20) NOT NULL, "duration_hours" decimal NULL, "language" varchar(50) NOT NULL, "provider" varchar(200) NOT NULL, "instructor" varchar(200) NOT NULL, "cost" decimal NULL, "max_participants" integer NULL, "is_active" bool NOT NULL, "is_mandatory" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL);
INSERT INTO "training_trainingresource" VALUES(1,'Liderlik Əsasları','Effektiv liderlik prinsipləri və komanda idarəetməsi üzrə təlim','course',1,'online','https://example.com/leadership','intermediate',16,'Azərbaycan','Q360 Academy','Dr. Əli Məmmədov',250,NULL,1,1,'2025-10-11 07:49:07.262343','2025-10-11 08:09:57.207662');
INSERT INTO "training_trainingresource" VALUES(2,'Effektiv Kommunikasiya Bacarıqları','Şifahi və yazılı ünsiyyət bacarıqlarının inkişafı','webinar',1,'hybrid','','intermediate',8,'Azərbaycan','BizSkills Training Center','Nigar Həsənova',150,100,1,1,'2025-10-11 07:49:07.270008','2025-10-15 11:53:40.057972');
INSERT INTO "training_trainingresource" VALUES(3,'Problem Həlli və Kritik Düşüncə','Analitik düşüncə və yaradıcı problem həlli texnikaları','course',1,'hybrid','https://example.com/problem-solving','advanced',24,'Azərbaycan','Q360 Academy','Prof. Rəşid Quliyev',350,NULL,1,0,'2025-10-11 07:49:07.271886','2025-10-11 07:49:07.271905');
INSERT INTO "training_trainingresource" VALUES(4,'Müştəri Xidməti Mükəmməlliyi','Müştəri məmnuniyyəti və xidmət keyfiyyətinin artırılması','webinar',1,'online','https://example.com/customer-service','intermediate',4,'Azərbaycan','Service Excellence Institute','Aynur Əliyeva',75,NULL,1,0,'2025-10-11 07:49:07.274443','2025-10-15 11:52:50.764734');
INSERT INTO "training_trainingresource" VALUES(5,'Vaxt İdarəetməsi və Məhsuldarlıq','Effektiv vaxt planlaması və prioritet müəyyənləşdirmə','self_study',1,'online','https://example.com/time-management','beginner',6,'Azərbaycan','Productivity Pro','Kamran Məmmədov',0,NULL,1,1,'2025-10-11 07:49:07.277084','2025-10-11 07:49:07.277095');
INSERT INTO "training_trainingresource" VALUES(6,'Texniki Bacarıqların İnkişafı','Sahə üzrə texniki bilik və praktiki tətbiq','certification',1,'online','https://example.com/technical-skills','expert',40,'İngilis','Tech Academy','International Experts',500,NULL,1,0,'2025-10-11 07:49:07.278365','2025-10-11 07:49:07.278375');
INSERT INTO "training_trainingresource" VALUES(7,'Python ilə Proqramlaşdırma - Əsaslar','Python proqramlaşdırma dilinin əsasları','course',1,'online','https://www.udemy.com/course/python-programming/','beginner',40,'İngilis','Udemy','',150,NULL,1,0,'2025-10-15 07:47:48.705638','2025-10-15 07:47:48.705651');
CREATE TABLE "training_trainingresource_required_competencies" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "trainingresource_id" bigint NOT NULL REFERENCES "training_trainingresource" ("id") DEFERRABLE INITIALLY DEFERRED, "competency_id" bigint NOT NULL REFERENCES "competencies_competency" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "training_trainingresource_required_competencies" VALUES(1,1,1);
INSERT INTO "training_trainingresource_required_competencies" VALUES(2,1,4);
INSERT INTO "training_trainingresource_required_competencies" VALUES(3,2,2);
INSERT INTO "training_trainingresource_required_competencies" VALUES(4,3,3);
INSERT INTO "training_trainingresource_required_competencies" VALUES(5,3,8);
INSERT INTO "training_trainingresource_required_competencies" VALUES(6,4,6);
INSERT INTO "training_trainingresource_required_competencies" VALUES(7,4,2);
INSERT INTO "training_trainingresource_required_competencies" VALUES(8,5,7);
INSERT INTO "training_trainingresource_required_competencies" VALUES(9,6,5);
INSERT INTO "training_trainingresource_required_competencies" VALUES(10,6,8);
INSERT INTO "training_trainingresource_required_competencies" VALUES(11,7,11);
INSERT INTO "training_trainingresource_required_competencies" VALUES(13,4,1);
INSERT INTO "training_trainingresource_required_competencies" VALUES(14,4,3);
INSERT INTO "training_trainingresource_required_competencies" VALUES(15,4,4);
INSERT INTO "training_trainingresource_required_competencies" VALUES(16,4,5);
INSERT INTO "training_trainingresource_required_competencies" VALUES(17,4,7);
INSERT INTO "training_trainingresource_required_competencies" VALUES(18,4,8);
INSERT INTO "training_trainingresource_required_competencies" VALUES(19,4,9);
INSERT INTO "training_trainingresource_required_competencies" VALUES(20,4,10);
INSERT INTO "training_trainingresource_required_competencies" VALUES(21,4,11);
INSERT INTO "training_trainingresource_required_competencies" VALUES(22,2,1);
INSERT INTO "training_trainingresource_required_competencies" VALUES(23,2,3);
INSERT INTO "training_trainingresource_required_competencies" VALUES(24,2,4);
INSERT INTO "training_trainingresource_required_competencies" VALUES(25,2,5);
INSERT INTO "training_trainingresource_required_competencies" VALUES(26,2,6);
INSERT INTO "training_trainingresource_required_competencies" VALUES(27,2,7);
INSERT INTO "training_trainingresource_required_competencies" VALUES(28,2,8);
INSERT INTO "training_trainingresource_required_competencies" VALUES(29,2,9);
INSERT INTO "training_trainingresource_required_competencies" VALUES(30,2,10);
INSERT INTO "training_trainingresource_required_competencies" VALUES(31,2,11);
CREATE TABLE "training_usertraining" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "assignment_type" varchar(30) NOT NULL, "start_date" date NULL, "due_date" date NULL, "completed_date" date NULL, "status" varchar(20) NOT NULL, "progress_percentage" integer NOT NULL, "completion_note" text NOT NULL, "user_feedback" text NOT NULL, "rating" integer NULL, "certificate_url" varchar(200) NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "assigned_by_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "related_goal_id" bigint NULL REFERENCES "development_plans_developmentgoal" ("id") DEFERRABLE INITIALLY DEFERRED, "resource_id" bigint NOT NULL REFERENCES "training_trainingresource" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "training_usertraining" VALUES(1,'manager_assigned','2025-10-11','2025-10-30',NULL,'in_progress',11,'əla','əla',2,'','2025-10-11 08:11:25.205695','2025-10-11 08:11:25.205715',2,1,1,1);
INSERT INTO "training_usertraining" VALUES(2,'system_recommended','2025-10-14',NULL,NULL,'pending',0,'','',NULL,'','2025-10-14 22:15:31.016315','2025-10-14 22:15:31.016329',NULL,NULL,3,1);
INSERT INTO "training_usertraining" VALUES(3,'system_recommended','2025-10-14',NULL,NULL,'pending',0,'','',NULL,'','2025-10-14 22:15:31.513678','2025-10-14 22:15:31.513695',NULL,NULL,6,1);
CREATE TABLE "workforce_planning_competencygap" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "current_score" decimal NOT NULL, "target_score" decimal NOT NULL, "gap_score" decimal NOT NULL, "gap_status" varchar(20) NOT NULL, "recommended_actions" text NOT NULL, "priority" varchar(10) NOT NULL, "identified_date" date NOT NULL, "target_close_date" date NULL, "is_closed" bool NOT NULL, "closed_date" date NULL, "closure_notes" text NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "competency_id" bigint NOT NULL REFERENCES "competencies_competency" ("id") DEFERRABLE INITIALLY DEFERRED, "current_level_id" bigint NULL REFERENCES "competencies_proficiencylevel" ("id") DEFERRABLE INITIALLY DEFERRED, "target_level_id" bigint NOT NULL REFERENCES "competencies_proficiencylevel" ("id") DEFERRABLE INITIALLY DEFERRED, "target_position_id" bigint NULL REFERENCES "departments_position" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "workforce_planning_competencygap" VALUES(1,1,5,4,'minor_gap','aaaaaaaaaaaa','medium','2025-10-15','2025-10-15',0,NULL,'','2025-10-14 22:10:31.291580','2025-10-14 22:10:31.291599',5,1,1,1,1);
CREATE TABLE "workforce_planning_competencygap_recommended_trainings" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "competencygap_id" bigint NOT NULL REFERENCES "workforce_planning_competencygap" ("id") DEFERRABLE INITIALLY DEFERRED, "trainingresource_id" bigint NOT NULL REFERENCES "training_trainingresource" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "workforce_planning_competencygap_recommended_trainings" VALUES(1,1,1);
INSERT INTO "workforce_planning_competencygap_recommended_trainings" VALUES(2,1,2);
INSERT INTO "workforce_planning_competencygap_recommended_trainings" VALUES(3,1,3);
INSERT INTO "workforce_planning_competencygap_recommended_trainings" VALUES(4,1,4);
INSERT INTO "workforce_planning_competencygap_recommended_trainings" VALUES(5,1,5);
INSERT INTO "workforce_planning_competencygap_recommended_trainings" VALUES(6,1,6);
CREATE TABLE "workforce_planning_criticalrole" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "criticality_level" varchar(10) NOT NULL, "business_impact" text NOT NULL, "required_experience_years" integer NOT NULL, "succession_readiness" varchar(20) NOT NULL, "is_active" bool NOT NULL, "designated_date" date NOT NULL, "notes" text NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "current_holder_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "position_id" bigint NOT NULL REFERENCES "departments_position" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "workforce_planning_criticalrole" VALUES(1,'medium','aaaaaaaaaaaaaaaaaaaaaaaaaaaa',5,'ready_now',1,'2025-10-15','aaaaaaaaaaaaa','2025-10-14 22:11:28.098545','2025-10-14 22:11:28.098563',1,6);
CREATE TABLE "workforce_planning_criticalrole_required_competencies" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "criticalrole_id" bigint NOT NULL REFERENCES "workforce_planning_criticalrole" ("id") DEFERRABLE INITIALLY DEFERRED, "competency_id" bigint NOT NULL REFERENCES "competencies_competency" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "workforce_planning_criticalrole_required_competencies" VALUES(1,1,1);
INSERT INTO "workforce_planning_criticalrole_required_competencies" VALUES(2,1,2);
INSERT INTO "workforce_planning_criticalrole_required_competencies" VALUES(3,1,3);
INSERT INTO "workforce_planning_criticalrole_required_competencies" VALUES(4,1,4);
INSERT INTO "workforce_planning_criticalrole_required_competencies" VALUES(5,1,5);
INSERT INTO "workforce_planning_criticalrole_required_competencies" VALUES(6,1,6);
INSERT INTO "workforce_planning_criticalrole_required_competencies" VALUES(7,1,7);
INSERT INTO "workforce_planning_criticalrole_required_competencies" VALUES(8,1,8);
CREATE TABLE "workforce_planning_successioncandidate" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "readiness_level" varchar(20) NOT NULL, "readiness_score" decimal NOT NULL, "strengths" text NOT NULL, "development_needs" text NOT NULL, "development_plan" text NOT NULL, "nomination_date" date NOT NULL, "is_active" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "candidate_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "critical_role_id" bigint NOT NULL REFERENCES "workforce_planning_criticalrole" ("id") DEFERRABLE INITIALLY DEFERRED, "nominated_by_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "workforce_planning_successioncandidate" VALUES(1,'ready_1_2_years',4,'aaaaaaaaaaaaaaaaa','aaaaaaaaaaaaaaaaaaaaaa','aaaaaaaaaaaaaaaaaaaaaaa','2025-10-15',1,'2025-10-14 22:12:09.867750','2025-10-14 22:12:09.867771',2,1,1);
CREATE TABLE "workforce_planning_talentmatrix" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "performance_level" varchar(10) NOT NULL, "potential_level" varchar(10) NOT NULL, "box_category" varchar(10) NOT NULL, "performance_score" decimal NOT NULL, "potential_score" decimal NOT NULL, "assessment_date" date NOT NULL, "assessment_period" varchar(50) NOT NULL, "notes" text NOT NULL, "development_actions" text NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "assessed_by_id" bigint NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "workforce_planning_talentmatrix" VALUES(1,'high','high','box9',10,10,'2025-10-15','2025 q2','aaaaaaaaaaaaaa','aaaaaaaaaaaaaaa','2025-10-14 22:13:13.988448','2025-10-14 22:13:13.988472',2,1);
CREATE UNIQUE INDEX "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" ("app_label", "model");
CREATE UNIQUE INDEX "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" ("group_id", "permission_id");
CREATE INDEX "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" ("group_id");
CREATE INDEX "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" ("permission_id");
CREATE UNIQUE INDEX "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" ("content_type_id", "codename");
CREATE INDEX "auth_permission_content_type_id_2f476e4b" ON "auth_permission" ("content_type_id");
CREATE INDEX "accounts_historicalrole_id_d74f1604" ON "accounts_historicalrole" ("id");
CREATE INDEX "accounts_historicalrole_name_0e74a4a1" ON "accounts_historicalrole" ("name");
CREATE INDEX "accounts_historicalrole_history_date_b5ed4377" ON "accounts_historicalrole" ("history_date");
CREATE INDEX "accounts_historicaluser_id_d7601895" ON "accounts_historicaluser" ("id");
CREATE INDEX "accounts_historicaluser_username_e37d9ea8" ON "accounts_historicaluser" ("username");
CREATE INDEX "accounts_historicaluser_employee_id_d739e18e" ON "accounts_historicaluser" ("employee_id");
CREATE INDEX "accounts_historicaluser_history_date_94c91976" ON "accounts_historicaluser" ("history_date");
CREATE UNIQUE INDEX "accounts_role_permissions_role_id_permission_id_032c715e_uniq" ON "accounts_role_permissions" ("role_id", "permission_id");
CREATE INDEX "accounts_role_permissions_role_id_54f107a6" ON "accounts_role_permissions" ("role_id");
CREATE INDEX "accounts_role_permissions_permission_id_76fe677d" ON "accounts_role_permissions" ("permission_id");
CREATE INDEX "departments_code_7a7a1f_idx" ON "departments_organization" ("code");
CREATE INDEX "departments_is_acti_5ac9f2_idx" ON "departments_organization" ("is_active");
CREATE INDEX "departments_historicaldepartment_id_7c4d87f4" ON "departments_historicaldepartment" ("id");
CREATE INDEX "departments_historicaldepartment_history_date_c0ad87eb" ON "departments_historicaldepartment" ("history_date");
CREATE INDEX "departments_historicalorganization_id_9be989c5" ON "departments_historicalorganization" ("id");
CREATE INDEX "departments_historicalorganization_name_a9e430f8" ON "departments_historicalorganization" ("name");
CREATE INDEX "departments_historicalorganization_code_6fa08a1f" ON "departments_historicalorganization" ("code");
CREATE INDEX "departments_historicalorganization_history_date_055cbda6" ON "departments_historicalorganization" ("history_date");
CREATE INDEX "departments_position_department_id_8b23d744" ON "departments_position" ("department_id");
CREATE INDEX "departments_position_organization_id_0075f57e" ON "departments_position" ("organization_id");
CREATE INDEX "departments_position_reports_to_id_f4a71763" ON "departments_position" ("reports_to_id");
CREATE INDEX "departments_historicalorganization_history_user_id_98c30490" ON "departments_historicalorganization" ("history_user_id");
CREATE INDEX "departments_historicaldepartment_head_id_1adbc720" ON "departments_historicaldepartment" ("head_id");
CREATE INDEX "departments_historicaldepartment_history_user_id_83883ee1" ON "departments_historicaldepartment" ("history_user_id");
CREATE INDEX "departments_historicaldepartment_organization_id_f35e850e" ON "departments_historicaldepartment" ("organization_id");
CREATE INDEX "departments_historicaldepartment_parent_id_391a5ac5" ON "departments_historicaldepartment" ("parent_id");
CREATE INDEX "departments_department_tree_id_28cdc253" ON "departments_department" ("tree_id");
CREATE INDEX "departments_department_head_id_3a991eda" ON "departments_department" ("head_id");
CREATE INDEX "departments_department_organization_id_b2b8ccdf" ON "departments_department" ("organization_id");
CREATE INDEX "departments_code_659216_idx" ON "departments_position" ("code");
CREATE INDEX "departments_level_dc8ed0_idx" ON "departments_position" ("level");
CREATE UNIQUE INDEX "departments_position_organization_id_code_571f0711_uniq" ON "departments_position" ("organization_id", "code");
CREATE INDEX "departments_code_35a421_idx" ON "departments_department" ("code");
CREATE INDEX "departments_is_acti_51d68f_idx" ON "departments_department" ("is_active");
CREATE UNIQUE INDEX "departments_department_organization_id_code_77d333b6_uniq" ON "departments_department" ("organization_id", "code");
CREATE INDEX "departments_department_parent_id_cc8b848e" ON "departments_department" ("parent_id");
CREATE INDEX "accounts_us_employe_0cbd94_idx" ON "accounts_user" ("employee_id");
CREATE INDEX "accounts_us_role_1fa9a5_idx" ON "accounts_user" ("role");
CREATE INDEX "accounts_us_departm_444702_idx" ON "accounts_user" ("department_id");
CREATE INDEX "accounts_historicaluser_department_id_5ba4994e" ON "accounts_historicaluser" ("department_id");
CREATE INDEX "accounts_historicaluser_history_user_id_db1b2c5f" ON "accounts_historicaluser" ("history_user_id");
CREATE INDEX "accounts_historicaluser_supervisor_id_0fcdd57a" ON "accounts_historicaluser" ("supervisor_id");
CREATE INDEX "accounts_historicalrole_history_user_id_81a0a8b1" ON "accounts_historicalrole" ("history_user_id");
CREATE INDEX "accounts_user_department_id_8dc06840" ON "accounts_user" ("department_id");
CREATE UNIQUE INDEX "accounts_user_groups_user_id_group_id_59c0b32f_uniq" ON "accounts_user_groups" ("user_id", "group_id");
CREATE INDEX "accounts_user_groups_user_id_52b62117" ON "accounts_user_groups" ("user_id");
CREATE INDEX "accounts_user_groups_group_id_bd11a704" ON "accounts_user_groups" ("group_id");
CREATE INDEX "accounts_user_supervisor_id_f571ce05" ON "accounts_user" ("supervisor_id");
CREATE UNIQUE INDEX "accounts_user_user_permissions_user_id_permission_id_2ab516c2_uniq" ON "accounts_user_user_permissions" ("user_id", "permission_id");
CREATE INDEX "accounts_user_user_permissions_user_id_e4f0a161" ON "accounts_user_user_permissions" ("user_id");
CREATE INDEX "accounts_user_user_permissions_permission_id_113bb443" ON "accounts_user_user_permissions" ("permission_id");
CREATE INDEX "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" ("content_type_id");
CREATE INDEX "django_admin_log_user_id_c564eba6" ON "django_admin_log" ("user_id");
CREATE INDEX "audit_auditlog_user_id_c1cca96c" ON "audit_auditlog" ("user_id");
CREATE INDEX "audit_audit_user_id_a3c2bc_idx" ON "audit_auditlog" ("user_id", "created_at");
CREATE INDEX "audit_audit_action_3e3f78_idx" ON "audit_auditlog" ("action", "model_name");
CREATE INDEX "evaluations_evaluat_b86b4a_idx" ON "evaluations_evaluationassignment" ("evaluator_id", "status");
CREATE INDEX "evaluations_evaluat_0b4546_idx" ON "evaluations_evaluationassignment" ("evaluatee_id", "campaign_id");
CREATE UNIQUE INDEX "evaluations_evaluationassignment_campaign_id_evaluator_id_evaluatee_id_2bc68ea1_uniq" ON "evaluations_evaluationassignment" ("campaign_id", "evaluator_id", "evaluatee_id");
CREATE UNIQUE INDEX "evaluations_campaignquestion_campaign_id_question_id_20c04a5e_uniq" ON "evaluations_campaignquestion" ("campaign_id", "question_id");
CREATE UNIQUE INDEX "evaluations_evaluationcampaign_target_departments_evaluationcampaign_id_department_id_b6967967_uniq" ON "evaluations_evaluationcampaign_target_departments" ("evaluationcampaign_id", "department_id");
CREATE INDEX "evaluations_evaluationcampaign_target_departments_evaluationcampaign_id_b1f1cd16" ON "evaluations_evaluationcampaign_target_departments" ("evaluationcampaign_id");
CREATE INDEX "evaluations_evaluationcampaign_target_departments_department_id_4a971c38" ON "evaluations_evaluationcampaign_target_departments" ("department_id");
CREATE UNIQUE INDEX "evaluations_evaluationcampaign_target_users_evaluationcampaign_id_user_id_8aea5194_uniq" ON "evaluations_evaluationcampaign_target_users" ("evaluationcampaign_id", "user_id");
CREATE INDEX "evaluations_evaluationcampaign_target_users_evaluationcampaign_id_9fc20965" ON "evaluations_evaluationcampaign_target_users" ("evaluationcampaign_id");
CREATE INDEX "evaluations_evaluationcampaign_target_users_user_id_4791dc35" ON "evaluations_evaluationcampaign_target_users" ("user_id");
CREATE INDEX "evaluations_question_category_id_6ef989ae" ON "evaluations_question" ("category_id");
CREATE INDEX "evaluations_historicalquestion_id_07207bc7" ON "evaluations_historicalquestion" ("id");
CREATE INDEX "evaluations_historicalquestion_history_date_93856b35" ON "evaluations_historicalquestion" ("history_date");
CREATE INDEX "evaluations_historicalquestion_category_id_bf2205bb" ON "evaluations_historicalquestion" ("category_id");
CREATE INDEX "evaluations_historicalquestion_history_user_id_e8ccc42f" ON "evaluations_historicalquestion" ("history_user_id");
CREATE INDEX "evaluations_historicalevaluationassignment_id_85eb9c1c" ON "evaluations_historicalevaluationassignment" ("id");
CREATE INDEX "evaluations_historicalevaluationassignment_history_date_9d44d712" ON "evaluations_historicalevaluationassignment" ("history_date");
CREATE INDEX "evaluations_historicalevaluationassignment_campaign_id_66ca37de" ON "evaluations_historicalevaluationassignment" ("campaign_id");
CREATE INDEX "evaluations_historicalevaluationassignment_evaluatee_id_fffed19f" ON "evaluations_historicalevaluationassignment" ("evaluatee_id");
CREATE INDEX "evaluations_historicalevaluationassignment_evaluator_id_4e206d07" ON "evaluations_historicalevaluationassignment" ("evaluator_id");
CREATE INDEX "evaluations_historicalevaluationassignment_history_user_id_b87e8c23" ON "evaluations_historicalevaluationassignment" ("history_user_id");
CREATE INDEX "evaluations_evaluationassignment_campaign_id_2ce28274" ON "evaluations_evaluationassignment" ("campaign_id");
CREATE INDEX "evaluations_evaluationassignment_evaluatee_id_e730c182" ON "evaluations_evaluationassignment" ("evaluatee_id");
CREATE INDEX "evaluations_evaluationassignment_evaluator_id_9f647a97" ON "evaluations_evaluationassignment" ("evaluator_id");
CREATE INDEX "evaluations_campaignquestion_campaign_id_fe32827e" ON "evaluations_campaignquestion" ("campaign_id");
CREATE INDEX "evaluations_campaignquestion_question_id_e5335b30" ON "evaluations_campaignquestion" ("question_id");
CREATE UNIQUE INDEX "evaluations_evaluationresult_campaign_id_evaluatee_id_2f9b8489_uniq" ON "evaluations_evaluationresult" ("campaign_id", "evaluatee_id");
CREATE INDEX "evaluations_evaluationresult_campaign_id_16936ca6" ON "evaluations_evaluationresult" ("campaign_id");
CREATE INDEX "evaluations_evaluationresult_evaluatee_id_61f8e409" ON "evaluations_evaluationresult" ("evaluatee_id");
CREATE INDEX "reports_report_campaign_id_a635c94c" ON "reports_report" ("campaign_id");
CREATE INDEX "reports_report_generated_by_id_17b52253" ON "reports_report" ("generated_by_id");
CREATE INDEX "reports_report_generated_for_id_6dbc2ee3" ON "reports_report" ("generated_for_id");
CREATE UNIQUE INDEX "reports_radarchartdata_user_id_campaign_id_category_85752120_uniq" ON "reports_radarchartdata" ("user_id", "campaign_id", "category");
CREATE INDEX "reports_radarchartdata_campaign_id_ea62cce3" ON "reports_radarchartdata" ("campaign_id");
CREATE INDEX "reports_radarchartdata_user_id_ed249755" ON "reports_radarchartdata" ("user_id");
CREATE INDEX "django_session_expire_date_a5c62663" ON "django_session" ("expire_date");
CREATE INDEX "development_plans_progresslog_goal_id_cd9b0a8f" ON "development_plans_progresslog" ("goal_id");
CREATE INDEX "development_plans_progresslog_logged_by_id_c86c97d2" ON "development_plans_progresslog" ("logged_by_id");
CREATE INDEX "notifications_emaillog_recipient_id_2b216ffc" ON "notifications_emaillog" ("recipient_id");
CREATE INDEX "notifications_emaillog_template_id_276b6a99" ON "notifications_emaillog" ("template_id");
CREATE INDEX "development_plans_developmentgoal_created_by_id_ae87fad9" ON "development_plans_developmentgoal" ("created_by_id");
CREATE INDEX "development_plans_developmentgoal_user_id_226b191f" ON "development_plans_developmentgoal" ("user_id");
CREATE INDEX "development_plans_developmentgoal_approved_by_id_3d8ea48a" ON "development_plans_developmentgoal" ("approved_by_id");
CREATE INDEX "reports_reportgenerationlog_requested_by_id_7b19aa7e" ON "reports_reportgenerationlog" ("requested_by_id");
CREATE INDEX "reports_rep_request_510537_idx" ON "reports_reportgenerationlog" ("requested_by_id", "status");
CREATE INDEX "reports_rep_created_3cb1bc_idx" ON "reports_reportgenerationlog" ("created_at");
CREATE INDEX "departments_historicalposition_id_9bf9e9b4" ON "departments_historicalposition" ("id");
CREATE INDEX "departments_historicalposition_history_date_3cc21fa9" ON "departments_historicalposition" ("history_date");
CREATE INDEX "departments_historicalposition_department_id_0c724233" ON "departments_historicalposition" ("department_id");
CREATE INDEX "departments_historicalposition_history_user_id_dc3caf8c" ON "departments_historicalposition" ("history_user_id");
CREATE INDEX "departments_historicalposition_organization_id_a98cd77f" ON "departments_historicalposition" ("organization_id");
CREATE INDEX "departments_historicalposition_reports_to_id_44ce417f" ON "departments_historicalposition" ("reports_to_id");
CREATE UNIQUE INDEX "evaluations_response_assignment_id_question_id_b332c035_uniq" ON "evaluations_response" ("assignment_id", "question_id");
CREATE INDEX "evaluations_response_assignment_id_534a8fd3" ON "evaluations_response" ("assignment_id");
CREATE INDEX "evaluations_response_question_id_48a570e1" ON "evaluations_response" ("question_id");
CREATE INDEX "support_supportticket_assigned_to_id_1b1ae160" ON "support_supportticket" ("assigned_to_id");
CREATE INDEX "support_supportticket_created_by_id_fa84ce40" ON "support_supportticket" ("created_by_id");
CREATE INDEX "support_ticketcomment_created_by_id_4f0c0788" ON "support_ticketcomment" ("created_by_id");
CREATE INDEX "support_ticketcomment_ticket_id_ff028e93" ON "support_ticketcomment" ("ticket_id");
CREATE INDEX "competencie_name_23d94b_idx" ON "competencies_competency" ("name");
CREATE INDEX "competencie_is_acti_0b88da_idx" ON "competencies_competency" ("is_active");
CREATE INDEX "competencies_historicalcompetency_id_baf36769" ON "competencies_historicalcompetency" ("id");
CREATE INDEX "competencies_historicalcompetency_name_06b51462" ON "competencies_historicalcompetency" ("name");
CREATE INDEX "competencies_historicalcompetency_history_date_2df7adf7" ON "competencies_historicalcompetency" ("history_date");
CREATE INDEX "competencies_historicalcompetency_history_user_id_626c1c78" ON "competencies_historicalcompetency" ("history_user_id");
CREATE INDEX "competencie_name_43a725_idx" ON "competencies_proficiencylevel" ("name");
CREATE INDEX "competencies_historicaluserskill_id_29c65e36" ON "competencies_historicaluserskill" ("id");
CREATE INDEX "competencies_historicaluserskill_history_date_8b3dceb6" ON "competencies_historicaluserskill" ("history_date");
CREATE INDEX "competencies_historicaluserskill_approved_by_id_e787dec6" ON "competencies_historicaluserskill" ("approved_by_id");
CREATE INDEX "competencies_historicaluserskill_competency_id_a034c787" ON "competencies_historicaluserskill" ("competency_id");
CREATE INDEX "competencies_historicaluserskill_history_user_id_d0a2807a" ON "competencies_historicaluserskill" ("history_user_id");
CREATE INDEX "competencies_historicaluserskill_user_id_08e53119" ON "competencies_historicaluserskill" ("user_id");
CREATE INDEX "competencies_historicaluserskill_level_id_cfb5e7dc" ON "competencies_historicaluserskill" ("level_id");
CREATE INDEX "competencies_historicalpositioncompetency_id_7385ddb8" ON "competencies_historicalpositioncompetency" ("id");
CREATE INDEX "competencies_historicalpositioncompetency_history_date_fe59239e" ON "competencies_historicalpositioncompetency" ("history_date");
CREATE INDEX "competencies_historicalpositioncompetency_competency_id_13d11809" ON "competencies_historicalpositioncompetency" ("competency_id");
CREATE INDEX "competencies_historicalpositioncompetency_history_user_id_48f6e969" ON "competencies_historicalpositioncompetency" ("history_user_id");
CREATE INDEX "competencies_historicalpositioncompetency_position_id_d2276e62" ON "competencies_historicalpositioncompetency" ("position_id");
CREATE INDEX "competencies_historicalpositioncompetency_required_level_id_fc61044c" ON "competencies_historicalpositioncompetency" ("required_level_id");
CREATE UNIQUE INDEX "competencies_positioncompetency_position_id_competency_id_32f31151_uniq" ON "competencies_positioncompetency" ("position_id", "competency_id");
CREATE INDEX "competencies_positioncompetency_competency_id_cf74e4fd" ON "competencies_positioncompetency" ("competency_id");
CREATE INDEX "competencies_positioncompetency_position_id_9ebb3564" ON "competencies_positioncompetency" ("position_id");
CREATE INDEX "competencies_positioncompetency_required_level_id_9b579f19" ON "competencies_positioncompetency" ("required_level_id");
CREATE INDEX "competencie_positio_275513_idx" ON "competencies_positioncompetency" ("position_id", "weight");
CREATE INDEX "competencie_compete_b197dc_idx" ON "competencies_positioncompetency" ("competency_id");
CREATE UNIQUE INDEX "competencies_userskill_user_id_competency_id_f97b2914_uniq" ON "competencies_userskill" ("user_id", "competency_id");
CREATE INDEX "competencies_userskill_approved_by_id_b5ead7db" ON "competencies_userskill" ("approved_by_id");
CREATE INDEX "competencies_userskill_competency_id_ccb80b3d" ON "competencies_userskill" ("competency_id");
CREATE INDEX "competencies_userskill_level_id_cdbedef3" ON "competencies_userskill" ("level_id");
CREATE INDEX "competencies_userskill_user_id_14631c18" ON "competencies_userskill" ("user_id");
CREATE INDEX "competencie_user_id_b83df4_idx" ON "competencies_userskill" ("user_id", "is_approved");
CREATE INDEX "competencie_compete_ebce9f_idx" ON "competencies_userskill" ("competency_id", "level_id");
CREATE INDEX "competencie_approva_acd8f4_idx" ON "competencies_userskill" ("approval_status");
CREATE INDEX "training_tr_type_38fb0e_idx" ON "training_trainingresource" ("type", "is_active");
CREATE INDEX "training_tr_difficu_3024b8_idx" ON "training_trainingresource" ("difficulty_level");
CREATE INDEX "training_tr_is_mand_e6b83e_idx" ON "training_trainingresource" ("is_mandatory");
CREATE INDEX "training_us_user_id_4bff29_idx" ON "training_usertraining" ("user_id", "status");
CREATE INDEX "training_us_resourc_c03d3c_idx" ON "training_usertraining" ("resource_id", "status");
CREATE INDEX "training_us_due_dat_898bb2_idx" ON "training_usertraining" ("due_date");
CREATE INDEX "training_us_assignm_b6e785_idx" ON "training_usertraining" ("assignment_type");
CREATE UNIQUE INDEX "training_usertraining_user_id_resource_id_4a8339ac_uniq" ON "training_usertraining" ("user_id", "resource_id");
CREATE INDEX "training_historicaltrainingresource_id_c43df152" ON "training_historicaltrainingresource" ("id");
CREATE INDEX "training_historicaltrainingresource_history_date_91781925" ON "training_historicaltrainingresource" ("history_date");
CREATE INDEX "training_historicaltrainingresource_history_user_id_bb812cb6" ON "training_historicaltrainingresource" ("history_user_id");
CREATE UNIQUE INDEX "training_trainingresource_required_competencies_trainingresource_id_competency_id_a7bc08d0_uniq" ON "training_trainingresource_required_competencies" ("trainingresource_id", "competency_id");
CREATE INDEX "training_trainingresource_required_competencies_trainingresource_id_21c9dccf" ON "training_trainingresource_required_competencies" ("trainingresource_id");
CREATE INDEX "training_trainingresource_required_competencies_competency_id_75460a7c" ON "training_trainingresource_required_competencies" ("competency_id");
CREATE INDEX "training_historicalusertraining_id_75f3222c" ON "training_historicalusertraining" ("id");
CREATE INDEX "training_historicalusertraining_history_date_b01401ae" ON "training_historicalusertraining" ("history_date");
CREATE INDEX "training_historicalusertraining_assigned_by_id_fdea0018" ON "training_historicalusertraining" ("assigned_by_id");
CREATE INDEX "training_historicalusertraining_history_user_id_5e7cf72e" ON "training_historicalusertraining" ("history_user_id");
CREATE INDEX "training_historicalusertraining_related_goal_id_1b29e205" ON "training_historicalusertraining" ("related_goal_id");
CREATE INDEX "training_historicalusertraining_user_id_2a8352bb" ON "training_historicalusertraining" ("user_id");
CREATE INDEX "training_historicalusertraining_resource_id_9a1b278f" ON "training_historicalusertraining" ("resource_id");
CREATE INDEX "training_usertraining_assigned_by_id_01ec1c98" ON "training_usertraining" ("assigned_by_id");
CREATE INDEX "training_usertraining_related_goal_id_158f3526" ON "training_usertraining" ("related_goal_id");
CREATE INDEX "training_usertraining_resource_id_ac7b7ec1" ON "training_usertraining" ("resource_id");
CREATE INDEX "training_usertraining_user_id_39d4161d" ON "training_usertraining" ("user_id");
CREATE INDEX "competencie_name_eac81b_idx" ON "competencies_competency" ("name", "is_active");
CREATE INDEX "competencie_score_m_96389c_idx" ON "competencies_proficiencylevel" ("score_min", "score_max");
CREATE INDEX "competencie_user_id_dc22be_idx" ON "competencies_userskill" ("user_id", "competency_id", "is_approved");
CREATE INDEX "competencie_current_a60b10_idx" ON "competencies_userskill" ("current_score");
CREATE INDEX "evaluations_campaig_8f9381_idx" ON "evaluations_evaluationresult" ("campaign_id", "evaluatee_id");
CREATE INDEX "evaluations_evaluat_9c92c8_idx" ON "evaluations_evaluationresult" ("evaluatee_id");
CREATE INDEX "evaluations_overall_3cb2fe_idx" ON "evaluations_evaluationresult" ("overall_score");
CREATE INDEX "evaluations_is_fina_aa3421_idx" ON "evaluations_evaluationresult" ("is_finalized");
CREATE INDEX "evaluations_categor_12d1ec_idx" ON "evaluations_question" ("category_id", "is_active");
CREATE INDEX "evaluations_questio_fd93e3_idx" ON "evaluations_question" ("question_type");
CREATE INDEX "evaluations_is_acti_c4763a_idx" ON "evaluations_question" ("is_active");
CREATE INDEX "evaluations_assignm_343623_idx" ON "evaluations_response" ("assignment_id", "question_id");
CREATE INDEX "evaluations_assignm_f87987_idx" ON "evaluations_response" ("assignment_id");
CREATE INDEX "evaluations_questio_35127c_idx" ON "evaluations_response" ("question_id");
CREATE INDEX "evaluations_sentime_2bf585_idx" ON "evaluations_response" ("sentiment_category");
CREATE INDEX "training_tr_provide_516d62_idx" ON "training_trainingresource" ("provider");
CREATE INDEX "training_tr_title_f512b5_idx" ON "training_trainingresource" ("title", "type");
CREATE INDEX "training_us_user_id_4c1bef_idx" ON "training_usertraining" ("user_id", "resource_id", "status");
CREATE INDEX "training_us_progres_290244_idx" ON "training_usertraining" ("progress_percentage");
CREATE INDEX "training_us_rating_17dd9d_idx" ON "training_usertraining" ("rating");
CREATE INDEX "continuous_feedback_recognitioncomment_recognition_id_23cbe925" ON "continuous_feedback_recognitioncomment" ("recognition_id");
CREATE INDEX "continuous_feedback_recognitioncomment_user_id_bdcc823d" ON "continuous_feedback_recognitioncomment" ("user_id");
CREATE INDEX "continuous_feedback_quickfeedback_recipient_id_b40c473f" ON "continuous_feedback_quickfeedback" ("recipient_id");
CREATE INDEX "continuous_feedback_quickfeedback_related_competency_id_d071f12a" ON "continuous_feedback_quickfeedback" ("related_competency_id");
CREATE INDEX "continuous_feedback_quickfeedback_sender_id_6106bbbc" ON "continuous_feedback_quickfeedback" ("sender_id");
CREATE UNIQUE INDEX "continuous_feedback_quickfeedback_tags_quickfeedback_id_feedbacktag_id_619d2945_uniq" ON "continuous_feedback_quickfeedback_tags" ("quickfeedback_id", "feedbacktag_id");
CREATE INDEX "continuous_feedback_quickfeedback_tags_quickfeedback_id_6d6f2e58" ON "continuous_feedback_quickfeedback_tags" ("quickfeedback_id");
CREATE INDEX "continuous_feedback_quickfeedback_tags_feedbacktag_id_753398d0" ON "continuous_feedback_quickfeedback_tags" ("feedbacktag_id");
CREATE INDEX "continuous__recipie_10005f_idx" ON "continuous_feedback_quickfeedback" ("recipient_id", "created_at" DESC);
CREATE INDEX "continuous__sender__34e568_idx" ON "continuous_feedback_quickfeedback" ("sender_id", "created_at" DESC);
CREATE INDEX "continuous__feedbac_8a10f0_idx" ON "continuous_feedback_quickfeedback" ("feedback_type", "visibility");
CREATE INDEX "continuous__publish_0dec65_idx" ON "continuous_feedback_publicrecognition" ("published_at" DESC);
CREATE INDEX "continuous__is_feat_f64722_idx" ON "continuous_feedback_publicrecognition" ("is_featured", "published_at" DESC);
CREATE UNIQUE INDEX "continuous_feedback_recognitionlike_recognition_id_user_id_6ada4d76_uniq" ON "continuous_feedback_recognitionlike" ("recognition_id", "user_id");
CREATE INDEX "continuous_feedback_recognitionlike_recognition_id_9ad394a4" ON "continuous_feedback_recognitionlike" ("recognition_id");
CREATE INDEX "continuous_feedback_recognitionlike_user_id_7111e097" ON "continuous_feedback_recognitionlike" ("user_id");
CREATE INDEX "workforce_planning_criticalrole_current_holder_id_12a730a1" ON "workforce_planning_criticalrole" ("current_holder_id");
CREATE INDEX "workforce_planning_criticalrole_position_id_18d22936" ON "workforce_planning_criticalrole" ("position_id");
CREATE UNIQUE INDEX "workforce_planning_criticalrole_required_competencies_criticalrole_id_competency_id_b4a649ad_uniq" ON "workforce_planning_criticalrole_required_competencies" ("criticalrole_id", "competency_id");
CREATE INDEX "workforce_planning_criticalrole_required_competencies_criticalrole_id_6e115b4e" ON "workforce_planning_criticalrole_required_competencies" ("criticalrole_id");
CREATE INDEX "workforce_planning_criticalrole_required_competencies_competency_id_171dc2d5" ON "workforce_planning_criticalrole_required_competencies" ("competency_id");
CREATE INDEX "workforce_planning_talentmatrix_assessed_by_id_76773f31" ON "workforce_planning_talentmatrix" ("assessed_by_id");
CREATE INDEX "workforce_planning_talentmatrix_user_id_4753c3d3" ON "workforce_planning_talentmatrix" ("user_id");
CREATE INDEX "workforce_p_user_id_fc86de_idx" ON "workforce_planning_talentmatrix" ("user_id", "assessment_date" DESC);
CREATE INDEX "workforce_p_box_cat_f086ba_idx" ON "workforce_planning_talentmatrix" ("box_category");
CREATE UNIQUE INDEX "workforce_planning_successioncandidate_critical_role_id_candidate_id_0062bbcf_uniq" ON "workforce_planning_successioncandidate" ("critical_role_id", "candidate_id");
CREATE INDEX "workforce_planning_successioncandidate_candidate_id_bbf93356" ON "workforce_planning_successioncandidate" ("candidate_id");
CREATE INDEX "workforce_planning_successioncandidate_critical_role_id_7ebe323c" ON "workforce_planning_successioncandidate" ("critical_role_id");
CREATE INDEX "workforce_planning_successioncandidate_nominated_by_id_42a502e9" ON "workforce_planning_successioncandidate" ("nominated_by_id");
CREATE INDEX "workforce_planning_competencygap_competency_id_6989d40b" ON "workforce_planning_competencygap" ("competency_id");
CREATE INDEX "workforce_planning_competencygap_current_level_id_ba3f4bf3" ON "workforce_planning_competencygap" ("current_level_id");
CREATE INDEX "workforce_planning_competencygap_target_level_id_065d342f" ON "workforce_planning_competencygap" ("target_level_id");
CREATE INDEX "workforce_planning_competencygap_target_position_id_90a7580b" ON "workforce_planning_competencygap" ("target_position_id");
CREATE INDEX "workforce_planning_competencygap_user_id_31aca51f" ON "workforce_planning_competencygap" ("user_id");
CREATE INDEX "workforce_p_user_id_dd7dcf_idx" ON "workforce_planning_competencygap" ("user_id", "gap_score" DESC);
CREATE INDEX "workforce_p_priorit_1f8413_idx" ON "workforce_planning_competencygap" ("priority", "identified_date" DESC);
CREATE UNIQUE INDEX "workforce_planning_competencygap_recommended_trainings_competencygap_id_trainingresource_id_4fcd908f_uniq" ON "workforce_planning_competencygap_recommended_trainings" ("competencygap_id", "trainingresource_id");
CREATE INDEX "workforce_planning_competencygap_recommended_trainings_competencygap_id_ed14be17" ON "workforce_planning_competencygap_recommended_trainings" ("competencygap_id");
CREATE INDEX "workforce_planning_competencygap_recommended_trainings_trainingresource_id_ea800cc1" ON "workforce_planning_competencygap_recommended_trainings" ("trainingresource_id");
CREATE INDEX "evaluations_evaluationcampaign_created_by_id_ce7beda5" ON "evaluations_evaluationcampaign" ("created_by_id");
CREATE INDEX "evaluations_status_2985ee_idx" ON "evaluations_evaluationcampaign" ("status", "start_date");
CREATE INDEX "evaluations_end_dat_1d8a09_idx" ON "evaluations_evaluationcampaign" ("end_date");
CREATE INDEX "evaluations_status_540c61_idx" ON "evaluations_evaluationcampaign" ("status");
CREATE INDEX "evaluations_created_4c6f18_idx" ON "evaluations_evaluationcampaign" ("created_by_id");
CREATE INDEX "evaluations_historicalevaluationcampaign_id_c834903c" ON "evaluations_historicalevaluationcampaign" ("id");
CREATE INDEX "evaluations_historicalevaluationcampaign_history_date_4ff4020a" ON "evaluations_historicalevaluationcampaign" ("history_date");
CREATE INDEX "evaluations_historicalevaluationcampaign_created_by_id_318fabf6" ON "evaluations_historicalevaluationcampaign" ("created_by_id");
CREATE INDEX "evaluations_historicalevaluationcampaign_history_user_id_67d6384a" ON "evaluations_historicalevaluationcampaign" ("history_user_id");
CREATE INDEX "accounts_historicalprofile_id_dc0b5a08" ON "accounts_historicalprofile" ("id");
CREATE INDEX "accounts_historicalprofile_history_date_25a1ea7d" ON "accounts_historicalprofile" ("history_date");
CREATE INDEX "accounts_historicalprofile_history_user_id_200e06b5" ON "accounts_historicalprofile" ("history_user_id");
CREATE INDEX "accounts_historicalprofile_user_id_000fa6bf" ON "accounts_historicalprofile" ("user_id");
CREATE INDEX "accounts_historicalworkhistory_id_e45b828b" ON "accounts_historicalworkhistory" ("id");
CREATE INDEX "accounts_historicalworkhistory_history_date_bb0e7f84" ON "accounts_historicalworkhistory" ("history_date");
CREATE INDEX "accounts_historicalworkhistory_approved_by_id_4fb3a951" ON "accounts_historicalworkhistory" ("approved_by_id");
CREATE INDEX "accounts_historicalworkhistory_created_by_id_02c6dc16" ON "accounts_historicalworkhistory" ("created_by_id");
CREATE INDEX "accounts_historicalworkhistory_history_user_id_630aa6c6" ON "accounts_historicalworkhistory" ("history_user_id");
CREATE INDEX "accounts_historicalworkhistory_new_department_id_e0fcf849" ON "accounts_historicalworkhistory" ("new_department_id");
CREATE INDEX "accounts_historicalworkhistory_old_department_id_6367d98b" ON "accounts_historicalworkhistory" ("old_department_id");
CREATE INDEX "accounts_historicalworkhistory_user_id_098c9429" ON "accounts_historicalworkhistory" ("user_id");
CREATE INDEX "accounts_historicalemployeedocument_id_1a35cdc3" ON "accounts_historicalemployeedocument" ("id");
CREATE INDEX "accounts_historicalemployeedocument_history_date_27001013" ON "accounts_historicalemployeedocument" ("history_date");
CREATE INDEX "accounts_historicalemployeedocument_history_user_id_65992d75" ON "accounts_historicalemployeedocument" ("history_user_id");
CREATE INDEX "accounts_historicalemployeedocument_uploaded_by_id_370326c1" ON "accounts_historicalemployeedocument" ("uploaded_by_id");
CREATE INDEX "accounts_historicalemployeedocument_user_id_be68e252" ON "accounts_historicalemployeedocument" ("user_id");
CREATE INDEX "accounts_workhistory_approved_by_id_c87114b5" ON "accounts_workhistory" ("approved_by_id");
CREATE INDEX "accounts_workhistory_created_by_id_4209cf4c" ON "accounts_workhistory" ("created_by_id");
CREATE INDEX "accounts_workhistory_new_department_id_6160a14a" ON "accounts_workhistory" ("new_department_id");
CREATE INDEX "accounts_workhistory_old_department_id_6d8df846" ON "accounts_workhistory" ("old_department_id");
CREATE INDEX "accounts_workhistory_user_id_c7c322a9" ON "accounts_workhistory" ("user_id");
CREATE INDEX "accounts_wo_user_id_1de8f0_idx" ON "accounts_workhistory" ("user_id", "effective_date");
CREATE INDEX "accounts_wo_change__ba220f_idx" ON "accounts_workhistory" ("change_type");
CREATE INDEX "accounts_employeedocument_uploaded_by_id_56b5affa" ON "accounts_employeedocument" ("uploaded_by_id");
CREATE INDEX "accounts_employeedocument_user_id_118b2377" ON "accounts_employeedocument" ("user_id");
CREATE INDEX "accounts_em_user_id_92a11b_idx" ON "accounts_employeedocument" ("user_id", "document_type");
CREATE INDEX "accounts_em_expiry__df6ac5_idx" ON "accounts_employeedocument" ("expiry_date");
CREATE INDEX "compensation_historicalsalaryinformation_id_0c61c6d1" ON "compensation_historicalsalaryinformation" ("id");
CREATE INDEX "compensation_historicalsalaryinformation_history_date_7b500f4f" ON "compensation_historicalsalaryinformation" ("history_date");
CREATE INDEX "compensation_historicalsalaryinformation_history_user_id_d346ef07" ON "compensation_historicalsalaryinformation" ("history_user_id");
CREATE INDEX "compensation_historicalsalaryinformation_updated_by_id_ac05268e" ON "compensation_historicalsalaryinformation" ("updated_by_id");
CREATE INDEX "compensation_historicalsalaryinformation_user_id_e8d21d99" ON "compensation_historicalsalaryinformation" ("user_id");
CREATE INDEX "compensation_historicaldeduction_id_11ccfdaf" ON "compensation_historicaldeduction" ("id");
CREATE INDEX "compensation_historicaldeduction_history_date_6e569359" ON "compensation_historicaldeduction" ("history_date");
CREATE INDEX "compensation_historicaldeduction_history_user_id_b5ae928f" ON "compensation_historicaldeduction" ("history_user_id");
CREATE INDEX "compensation_historicaldeduction_user_id_5e17a56a" ON "compensation_historicaldeduction" ("user_id");
CREATE INDEX "compensation_historicalcompensationhistory_id_fb0a6a1f" ON "compensation_historicalcompensationhistory" ("id");
CREATE INDEX "compensation_historicalcompensationhistory_history_date_fd85506a" ON "compensation_historicalcompensationhistory" ("history_date");
CREATE INDEX "compensation_historicalcompensationhistory_approved_by_id_8bb8a99e" ON "compensation_historicalcompensationhistory" ("approved_by_id");
CREATE INDEX "compensation_historicalcompensationhistory_created_by_id_691a71cb" ON "compensation_historicalcompensationhistory" ("created_by_id");
CREATE INDEX "compensation_historicalcompensationhistory_history_user_id_c25e3e5a" ON "compensation_historicalcompensationhistory" ("history_user_id");
CREATE INDEX "compensation_historicalcompensationhistory_user_id_b69ef269" ON "compensation_historicalcompensationhistory" ("user_id");
CREATE INDEX "compensation_historicalbonus_id_9ee3d29d" ON "compensation_historicalbonus" ("id");
CREATE INDEX "compensation_historicalbonus_history_date_547119de" ON "compensation_historicalbonus" ("history_date");
CREATE INDEX "compensation_historicalbonus_approved_by_id_a719a7a8" ON "compensation_historicalbonus" ("approved_by_id");
CREATE INDEX "compensation_historicalbonus_created_by_id_375f0edb" ON "compensation_historicalbonus" ("created_by_id");
CREATE INDEX "compensation_historicalbonus_history_user_id_fea8e446" ON "compensation_historicalbonus" ("history_user_id");
CREATE INDEX "compensation_historicalbonus_user_id_a8ab7251" ON "compensation_historicalbonus" ("user_id");
CREATE INDEX "compensation_historicalallowance_id_7e5c1b54" ON "compensation_historicalallowance" ("id");
CREATE INDEX "compensation_historicalallowance_history_date_c3643fd6" ON "compensation_historicalallowance" ("history_date");
CREATE INDEX "compensation_historicalallowance_approved_by_id_ac4a5c43" ON "compensation_historicalallowance" ("approved_by_id");
CREATE INDEX "compensation_historicalallowance_history_user_id_442e72d1" ON "compensation_historicalallowance" ("history_user_id");
CREATE INDEX "compensation_historicalallowance_user_id_5ff968a8" ON "compensation_historicalallowance" ("user_id");
CREATE INDEX "compensation_compensationhistory_approved_by_id_74206349" ON "compensation_compensationhistory" ("approved_by_id");
CREATE INDEX "compensation_compensationhistory_created_by_id_152e7542" ON "compensation_compensationhistory" ("created_by_id");
CREATE INDEX "compensation_compensationhistory_user_id_a0d17f60" ON "compensation_compensationhistory" ("user_id");
CREATE INDEX "compensation_deduction_user_id_cfc6c0a6" ON "compensation_deduction" ("user_id");
CREATE INDEX "compensatio_user_id_687bc8_idx" ON "compensation_deduction" ("user_id", "deduction_type");
CREATE INDEX "compensatio_is_acti_e718a2_idx" ON "compensation_deduction" ("is_active");
CREATE INDEX "compensation_bonus_approved_by_id_133dca86" ON "compensation_bonus" ("approved_by_id");
CREATE INDEX "compensation_bonus_created_by_id_5b7099c3" ON "compensation_bonus" ("created_by_id");
CREATE INDEX "compensation_bonus_user_id_7363104b" ON "compensation_bonus" ("user_id");
CREATE INDEX "compensatio_user_id_c49a3d_idx" ON "compensation_bonus" ("user_id", "fiscal_year");
CREATE INDEX "compensatio_status_272ed9_idx" ON "compensation_bonus" ("status");
CREATE INDEX "compensation_allowance_approved_by_id_e26343b1" ON "compensation_allowance" ("approved_by_id");
CREATE INDEX "compensation_allowance_user_id_53f09711" ON "compensation_allowance" ("user_id");
CREATE INDEX "compensatio_user_id_53d151_idx" ON "compensation_allowance" ("user_id", "allowance_type");
CREATE INDEX "compensatio_is_acti_9d29db_idx" ON "compensation_allowance" ("is_active");
CREATE INDEX "leave_atten_user_id_dd947d_idx" ON "leave_attendance_leaverequest" ("user_id", "status");
CREATE INDEX "leave_atten_start_d_cc6953_idx" ON "leave_attendance_leaverequest" ("start_date", "end_date");
CREATE INDEX "leave_atten_status_26f77b_idx" ON "leave_attendance_leaverequest" ("status");
CREATE INDEX "leave_atten_user_id_23dbb5_idx" ON "leave_attendance_leavebalance" ("user_id", "year");
CREATE INDEX "leave_atten_leave_t_24ef17_idx" ON "leave_attendance_leavebalance" ("leave_type_id", "year");
CREATE UNIQUE INDEX "leave_attendance_leavebalance_user_id_leave_type_id_year_e97eb48a_uniq" ON "leave_attendance_leavebalance" ("user_id", "leave_type_id", "year");
CREATE INDEX "leave_atten_user_id_5ca70b_idx" ON "leave_attendance_attendance" ("user_id", "date");
CREATE INDEX "leave_atten_date_b017ba_idx" ON "leave_attendance_attendance" ("date", "status");
CREATE UNIQUE INDEX "leave_attendance_attendance_user_id_date_b5e1876d_uniq" ON "leave_attendance_attendance" ("user_id", "date");
CREATE INDEX "leave_attendance_leaverequest_approved_by_id_2b474289" ON "leave_attendance_leaverequest" ("approved_by_id");
CREATE INDEX "leave_attendance_leaverequest_leave_type_id_c380d140" ON "leave_attendance_leaverequest" ("leave_type_id");
CREATE INDEX "leave_attendance_leaverequest_user_id_04899ba1" ON "leave_attendance_leaverequest" ("user_id");
CREATE INDEX "leave_attendance_leavebalance_leave_type_id_012985d8" ON "leave_attendance_leavebalance" ("leave_type_id");
CREATE INDEX "leave_attendance_leavebalance_user_id_5b7ede58" ON "leave_attendance_leavebalance" ("user_id");
CREATE INDEX "leave_atten_date_282b20_idx" ON "leave_attendance_holiday" ("date");
CREATE INDEX "leave_atten_is_acti_a31c49_idx" ON "leave_attendance_holiday" ("is_active");
CREATE INDEX "leave_attendance_historicalleavetype_id_ebcd15f4" ON "leave_attendance_historicalleavetype" ("id");
CREATE INDEX "leave_attendance_historicalleavetype_name_c4ea0db6" ON "leave_attendance_historicalleavetype" ("name");
CREATE INDEX "leave_attendance_historicalleavetype_code_e19febb1" ON "leave_attendance_historicalleavetype" ("code");
CREATE INDEX "leave_attendance_historicalleavetype_history_date_af45263c" ON "leave_attendance_historicalleavetype" ("history_date");
CREATE INDEX "leave_attendance_historicalleavetype_history_user_id_eb203a1c" ON "leave_attendance_historicalleavetype" ("history_user_id");
CREATE INDEX "leave_attendance_historicalleaverequest_id_3575f701" ON "leave_attendance_historicalleaverequest" ("id");
CREATE INDEX "leave_attendance_historicalleaverequest_history_date_fc1531a0" ON "leave_attendance_historicalleaverequest" ("history_date");
CREATE INDEX "leave_attendance_historicalleaverequest_approved_by_id_f0187b2a" ON "leave_attendance_historicalleaverequest" ("approved_by_id");
CREATE INDEX "leave_attendance_historicalleaverequest_history_user_id_7e46326e" ON "leave_attendance_historicalleaverequest" ("history_user_id");
CREATE INDEX "leave_attendance_historicalleaverequest_leave_type_id_a0ccf84d" ON "leave_attendance_historicalleaverequest" ("leave_type_id");
CREATE INDEX "leave_attendance_historicalleaverequest_user_id_4a239457" ON "leave_attendance_historicalleaverequest" ("user_id");
CREATE INDEX "leave_attendance_historicalleavebalance_id_747bccb9" ON "leave_attendance_historicalleavebalance" ("id");
CREATE INDEX "leave_attendance_historicalleavebalance_history_date_2b6b2799" ON "leave_attendance_historicalleavebalance" ("history_date");
CREATE INDEX "leave_attendance_historicalleavebalance_history_user_id_1ab613ae" ON "leave_attendance_historicalleavebalance" ("history_user_id");
CREATE INDEX "leave_attendance_historicalleavebalance_leave_type_id_b04dbc83" ON "leave_attendance_historicalleavebalance" ("leave_type_id");
CREATE INDEX "leave_attendance_historicalleavebalance_user_id_a20b0fdb" ON "leave_attendance_historicalleavebalance" ("user_id");
CREATE INDEX "leave_attendance_historicalholiday_id_7f08bc7d" ON "leave_attendance_historicalholiday" ("id");
CREATE INDEX "leave_attendance_historicalholiday_history_date_49fd8cc5" ON "leave_attendance_historicalholiday" ("history_date");
CREATE INDEX "leave_attendance_historicalholiday_history_user_id_28a3e198" ON "leave_attendance_historicalholiday" ("history_user_id");
CREATE INDEX "leave_attendance_historicalattendance_id_cd94755e" ON "leave_attendance_historicalattendance" ("id");
CREATE INDEX "leave_attendance_historicalattendance_history_date_dadb6aa0" ON "leave_attendance_historicalattendance" ("history_date");
CREATE INDEX "leave_attendance_historicalattendance_history_user_id_bc5100b7" ON "leave_attendance_historicalattendance" ("history_user_id");
CREATE INDEX "leave_attendance_historicalattendance_leave_request_id_04d996d5" ON "leave_attendance_historicalattendance" ("leave_request_id");
CREATE INDEX "leave_attendance_historicalattendance_user_id_c07db692" ON "leave_attendance_historicalattendance" ("user_id");
CREATE INDEX "leave_attendance_historicalattendance_verified_by_id_bde339dd" ON "leave_attendance_historicalattendance" ("verified_by_id");
CREATE INDEX "leave_attendance_attendance_leave_request_id_5273861a" ON "leave_attendance_attendance" ("leave_request_id");
CREATE INDEX "leave_attendance_attendance_user_id_f15ffa53" ON "leave_attendance_attendance" ("user_id");
CREATE INDEX "leave_attendance_attendance_verified_by_id_12916579" ON "leave_attendance_attendance" ("verified_by_id");
CREATE INDEX "development_level_651246_idx" ON "development_plans_strategicobjective" ("level", "status");
CREATE INDEX "development_fiscal__3ad16b_idx" ON "development_plans_strategicobjective" ("fiscal_year", "quarter");
CREATE INDEX "development_owner_i_0128fd_idx" ON "development_plans_strategicobjective" ("owner_id");
CREATE INDEX "development_departm_0a7ede_idx" ON "development_plans_strategicobjective" ("department_id");
CREATE INDEX "development_kpi_id_3ecf3c_idx" ON "development_plans_kpimeasurement" ("kpi_id", "measurement_date");
CREATE UNIQUE INDEX "development_plans_kpimeasurement_kpi_id_measurement_date_57af7fde_uniq" ON "development_plans_kpimeasurement" ("kpi_id", "measurement_date");
CREATE INDEX "development_owner_i_9bb0f9_idx" ON "development_plans_kpi" ("owner_id");
CREATE INDEX "development_departm_fe7211_idx" ON "development_plans_kpi" ("department_id");
CREATE INDEX "development_is_acti_e2fc1a_idx" ON "development_plans_kpi" ("is_active");
CREATE INDEX "development_objecti_812853_idx" ON "development_plans_keyresult" ("objective_id");
CREATE INDEX "development_is_acti_acdb1e_idx" ON "development_plans_keyresult" ("is_active");
CREATE INDEX "development_plans_kpi_department_id_fbd38010" ON "development_plans_kpi" ("department_id");
CREATE INDEX "development_plans_strategicobjective_created_by_id_c66825be" ON "development_plans_strategicobjective" ("created_by_id");
CREATE INDEX "development_plans_strategicobjective_department_id_0ab9ac1f" ON "development_plans_strategicobjective" ("department_id");
CREATE INDEX "development_plans_strategicobjective_owner_id_bdfe8357" ON "development_plans_strategicobjective" ("owner_id");
CREATE INDEX "development_plans_strategicobjective_parent_objective_id_ef9fc73a" ON "development_plans_strategicobjective" ("parent_objective_id");
CREATE INDEX "development_plans_kpimeasurement_kpi_id_3b5ee098" ON "development_plans_kpimeasurement" ("kpi_id");
CREATE INDEX "development_plans_kpimeasurement_measured_by_id_316bd52b" ON "development_plans_kpimeasurement" ("measured_by_id");
CREATE INDEX "development_plans_kpi_objective_id_922831e1" ON "development_plans_kpi" ("objective_id");
CREATE INDEX "development_plans_kpi_owner_id_daa04cd4" ON "development_plans_kpi" ("owner_id");
CREATE INDEX "development_plans_keyresult_objective_id_78504122" ON "development_plans_keyresult" ("objective_id");
CREATE INDEX "development_plans_historicalstrategicobjective_id_3461efca" ON "development_plans_historicalstrategicobjective" ("id");
CREATE INDEX "development_plans_historicalstrategicobjective_history_date_526746d7" ON "development_plans_historicalstrategicobjective" ("history_date");
CREATE INDEX "development_plans_historicalstrategicobjective_created_by_id_9c5fd456" ON "development_plans_historicalstrategicobjective" ("created_by_id");
CREATE INDEX "development_plans_historicalstrategicobjective_department_id_916c5e8e" ON "development_plans_historicalstrategicobjective" ("department_id");
CREATE INDEX "development_plans_historicalstrategicobjective_history_user_id_ab921880" ON "development_plans_historicalstrategicobjective" ("history_user_id");
CREATE INDEX "development_plans_historicalstrategicobjective_owner_id_b5f9c54f" ON "development_plans_historicalstrategicobjective" ("owner_id");
CREATE INDEX "development_plans_historicalstrategicobjective_parent_objective_id_f1cedfc8" ON "development_plans_historicalstrategicobjective" ("parent_objective_id");
CREATE INDEX "development_plans_historicalkpimeasurement_id_ee64f750" ON "development_plans_historicalkpimeasurement" ("id");
CREATE INDEX "development_plans_historicalkpimeasurement_history_date_5492297a" ON "development_plans_historicalkpimeasurement" ("history_date");
CREATE INDEX "development_plans_historicalkpimeasurement_history_user_id_3622338e" ON "development_plans_historicalkpimeasurement" ("history_user_id");
CREATE INDEX "development_plans_historicalkpimeasurement_kpi_id_26192dcb" ON "development_plans_historicalkpimeasurement" ("kpi_id");
CREATE INDEX "development_plans_historicalkpimeasurement_measured_by_id_8ac41baa" ON "development_plans_historicalkpimeasurement" ("measured_by_id");
CREATE INDEX "development_plans_historicalkpi_id_521ed373" ON "development_plans_historicalkpi" ("id");
CREATE INDEX "development_plans_historicalkpi_code_4415c281" ON "development_plans_historicalkpi" ("code");
CREATE INDEX "development_plans_historicalkpi_history_date_3973a626" ON "development_plans_historicalkpi" ("history_date");
CREATE INDEX "development_plans_historicalkpi_department_id_26cf1035" ON "development_plans_historicalkpi" ("department_id");
CREATE INDEX "development_plans_historicalkpi_history_user_id_17c13ce4" ON "development_plans_historicalkpi" ("history_user_id");
CREATE INDEX "development_plans_historicalkpi_objective_id_b2fac617" ON "development_plans_historicalkpi" ("objective_id");
CREATE INDEX "development_plans_historicalkpi_owner_id_f21020a9" ON "development_plans_historicalkpi" ("owner_id");
CREATE INDEX "development_plans_historicalkeyresult_id_7f7d6dc6" ON "development_plans_historicalkeyresult" ("id");
CREATE INDEX "development_plans_historicalkeyresult_history_date_2ad5c459" ON "development_plans_historicalkeyresult" ("history_date");
CREATE INDEX "development_plans_historicalkeyresult_history_user_id_64000299" ON "development_plans_historicalkeyresult" ("history_user_id");
CREATE INDEX "development_plans_historicalkeyresult_objective_id_b00acad0" ON "development_plans_historicalkeyresult" ("objective_id");
CREATE INDEX "recruitment_jobposting_created_by_id_c7887cb3" ON "recruitment_jobposting" ("created_by_id");
CREATE INDEX "recruitment_jobposting_department_id_8a5c16c4" ON "recruitment_jobposting" ("department_id");
CREATE INDEX "recruitment_jobposting_hiring_manager_id_018423f8" ON "recruitment_jobposting" ("hiring_manager_id");
CREATE UNIQUE INDEX "recruitment_jobposting_recruiters_jobposting_id_user_id_d65ded87_uniq" ON "recruitment_jobposting_recruiters" ("jobposting_id", "user_id");
CREATE INDEX "recruitment_jobposting_recruiters_jobposting_id_0850d769" ON "recruitment_jobposting_recruiters" ("jobposting_id");
CREATE INDEX "recruitment_jobposting_recruiters_user_id_0f4fdd21" ON "recruitment_jobposting_recruiters" ("user_id");
CREATE INDEX "recruitment_interview_application_id_6ea4352e" ON "recruitment_interview" ("application_id");
CREATE INDEX "recruitment_interview_created_by_id_2545bdfa" ON "recruitment_interview" ("created_by_id");
CREATE UNIQUE INDEX "recruitment_interview_interviewers_interview_id_user_id_52f415a5_uniq" ON "recruitment_interview_interviewers" ("interview_id", "user_id");
CREATE INDEX "recruitment_interview_interviewers_interview_id_6f9e4ea5" ON "recruitment_interview_interviewers" ("interview_id");
CREATE INDEX "recruitment_interview_interviewers_user_id_321f0481" ON "recruitment_interview_interviewers" ("user_id");
CREATE INDEX "recruitment_historicalonboardingtask_id_e5698e1c" ON "recruitment_historicalonboardingtask" ("id");
CREATE INDEX "recruitment_historicalonboardingtask_history_date_80ab6f33" ON "recruitment_historicalonboardingtask" ("history_date");
CREATE INDEX "recruitment_historicalonboardingtask_application_id_675f2f1b" ON "recruitment_historicalonboardingtask" ("application_id");
CREATE INDEX "recruitment_historicalonboardingtask_assigned_to_id_83014de6" ON "recruitment_historicalonboardingtask" ("assigned_to_id");
CREATE INDEX "recruitment_historicalonboardingtask_history_user_id_7c77010c" ON "recruitment_historicalonboardingtask" ("history_user_id");
CREATE INDEX "recruitment_historicalonboardingtask_new_hire_id_5f918dc1" ON "recruitment_historicalonboardingtask" ("new_hire_id");
CREATE INDEX "recruitment_historicaloffer_id_05e59ac3" ON "recruitment_historicaloffer" ("id");
CREATE INDEX "recruitment_historicaloffer_history_date_96086083" ON "recruitment_historicaloffer" ("history_date");
CREATE INDEX "recruitment_historicaloffer_application_id_cdc244fd" ON "recruitment_historicaloffer" ("application_id");
CREATE INDEX "recruitment_historicaloffer_approved_by_id_88383cf3" ON "recruitment_historicaloffer" ("approved_by_id");
CREATE INDEX "recruitment_historicaloffer_created_by_id_988da250" ON "recruitment_historicaloffer" ("created_by_id");
CREATE INDEX "recruitment_historicaloffer_history_user_id_99afe340" ON "recruitment_historicaloffer" ("history_user_id");
CREATE INDEX "recruitment_historicaljobposting_id_77e217ea" ON "recruitment_historicaljobposting" ("id");
CREATE INDEX "recruitment_historicaljobposting_code_7d64f304" ON "recruitment_historicaljobposting" ("code");
CREATE INDEX "recruitment_historicaljobposting_history_date_9df40852" ON "recruitment_historicaljobposting" ("history_date");
CREATE INDEX "recruitment_historicaljobposting_created_by_id_c26648c2" ON "recruitment_historicaljobposting" ("created_by_id");
CREATE INDEX "recruitment_historicaljobposting_department_id_d615dbf4" ON "recruitment_historicaljobposting" ("department_id");
CREATE INDEX "recruitment_historicaljobposting_hiring_manager_id_9959f0a3" ON "recruitment_historicaljobposting" ("hiring_manager_id");
CREATE INDEX "recruitment_historicaljobposting_history_user_id_1c4920a5" ON "recruitment_historicaljobposting" ("history_user_id");
CREATE INDEX "recruitment_historicalinterview_id_907cdc6e" ON "recruitment_historicalinterview" ("id");
CREATE INDEX "recruitment_historicalinterview_history_date_0278ba29" ON "recruitment_historicalinterview" ("history_date");
CREATE INDEX "recruitment_historicalinterview_application_id_dff2d967" ON "recruitment_historicalinterview" ("application_id");
CREATE INDEX "recruitment_historicalinterview_created_by_id_1152763a" ON "recruitment_historicalinterview" ("created_by_id");
CREATE INDEX "recruitment_historicalinterview_history_user_id_9b740fe9" ON "recruitment_historicalinterview" ("history_user_id");
CREATE INDEX "recruitment_historicalapplication_id_c350d697" ON "recruitment_historicalapplication" ("id");
CREATE INDEX "recruitment_historicalapplication_history_date_d151d266" ON "recruitment_historicalapplication" ("history_date");
CREATE INDEX "recruitment_historicalapplication_assigned_to_id_3099bc5c" ON "recruitment_historicalapplication" ("assigned_to_id");
CREATE INDEX "recruitment_historicalapplication_history_user_id_bb7dc5a0" ON "recruitment_historicalapplication" ("history_user_id");
CREATE INDEX "recruitment_historicalapplication_job_posting_id_e61f4f28" ON "recruitment_historicalapplication" ("job_posting_id");
CREATE INDEX "recruitment_historicalapplication_referrer_id_90a168d0" ON "recruitment_historicalapplication" ("referrer_id");
CREATE INDEX "recruitment_application_assigned_to_id_af966e93" ON "recruitment_application" ("assigned_to_id");
CREATE INDEX "recruitment_application_job_posting_id_9dcfa4fe" ON "recruitment_application" ("job_posting_id");
CREATE INDEX "recruitment_status_84e609_idx" ON "recruitment_jobposting" ("status", "posted_date");
CREATE INDEX "recruitment_departm_94a2e0_idx" ON "recruitment_jobposting" ("department_id");
CREATE INDEX "recruitment_employm_87e973_idx" ON "recruitment_jobposting" ("employment_type");
CREATE INDEX "recruitment_applica_d3ac81_idx" ON "recruitment_interview" ("application_id", "status");
CREATE INDEX "recruitment_schedul_9f7e08_idx" ON "recruitment_interview" ("scheduled_date");
CREATE INDEX "recruitment_job_pos_99b759_idx" ON "recruitment_application" ("job_posting_id", "status");
CREATE INDEX "recruitment_email_9308cd_idx" ON "recruitment_application" ("email");
CREATE INDEX "recruitment_status_d5b0c5_idx" ON "recruitment_application" ("status");
CREATE INDEX "recruitment_application_referrer_id_cad00dc4" ON "recruitment_application" ("referrer_id");
CREATE INDEX "recruitment_onboardingtask_application_id_a28fe532" ON "recruitment_onboardingtask" ("application_id");
CREATE INDEX "recruitment_onboardingtask_assigned_to_id_3cceb986" ON "recruitment_onboardingtask" ("assigned_to_id");
CREATE INDEX "recruitment_onboardingtask_new_hire_id_23e84ae0" ON "recruitment_onboardingtask" ("new_hire_id");
CREATE INDEX "recruitment_applica_0df70b_idx" ON "recruitment_onboardingtask" ("application_id", "status");
CREATE INDEX "recruitment_new_hir_e2a548_idx" ON "recruitment_onboardingtask" ("new_hire_id", "status");
CREATE INDEX "recruitment_assigne_0396c4_idx" ON "recruitment_onboardingtask" ("assigned_to_id", "status");
CREATE INDEX "recruitment_offer_application_id_b6ae646b" ON "recruitment_offer" ("application_id");
CREATE INDEX "recruitment_offer_approved_by_id_ac1a6408" ON "recruitment_offer" ("approved_by_id");
CREATE INDEX "recruitment_offer_created_by_id_a199fdbc" ON "recruitment_offer" ("created_by_id");
CREATE INDEX "recruitment_applica_f9f2e4_idx" ON "recruitment_offer" ("application_id", "status");
CREATE INDEX "recruitment_status_c9d751_idx" ON "recruitment_offer" ("status");
CREATE INDEX "compensation_historicaldepartmentbudget_id_6530c28c" ON "compensation_historicaldepartmentbudget" ("id");
CREATE INDEX "compensation_historicaldepartmentbudget_history_date_70e9db17" ON "compensation_historicaldepartmentbudget" ("history_date");
CREATE INDEX "compensation_historicaldepartmentbudget_created_by_id_0b8dbdac" ON "compensation_historicaldepartmentbudget" ("created_by_id");
CREATE INDEX "compensation_historicaldepartmentbudget_department_id_5034796d" ON "compensation_historicaldepartmentbudget" ("department_id");
CREATE INDEX "compensation_historicaldepartmentbudget_history_user_id_59d3c1c3" ON "compensation_historicaldepartmentbudget" ("history_user_id");
CREATE UNIQUE INDEX "compensation_departmentbudget_department_id_fiscal_year_b187df3a_uniq" ON "compensation_departmentbudget" ("department_id", "fiscal_year");
CREATE INDEX "compensation_departmentbudget_created_by_id_a121784e" ON "compensation_departmentbudget" ("created_by_id");
CREATE INDEX "compensation_departmentbudget_department_id_9802aa9f" ON "compensation_departmentbudget" ("department_id");
CREATE INDEX "compensatio_departm_8dd155_idx" ON "compensation_departmentbudget" ("department_id", "fiscal_year");
CREATE INDEX "reports_sys_date_1b58ea_idx" ON "reports_systemkpi" ("date" DESC);
CREATE INDEX "development_plans_historicalmilestone_id_5eb992be" ON "development_plans_historicalmilestone" ("id");
CREATE INDEX "development_plans_historicalmilestone_history_date_80fc8836" ON "development_plans_historicalmilestone" ("history_date");
CREATE INDEX "development_plans_historicalmilestone_created_by_id_1f7838e4" ON "development_plans_historicalmilestone" ("created_by_id");
CREATE INDEX "development_plans_historicalmilestone_history_user_id_71f6358c" ON "development_plans_historicalmilestone" ("history_user_id");
CREATE INDEX "development_plans_historicalmilestone_objective_id_5364da1e" ON "development_plans_historicalmilestone" ("objective_id");
CREATE INDEX "development_plans_historicalobjectiveupdate_id_0aed1a81" ON "development_plans_historicalobjectiveupdate" ("id");
CREATE INDEX "development_plans_historicalobjectiveupdate_history_date_8df9019e" ON "development_plans_historicalobjectiveupdate" ("history_date");
CREATE INDEX "development_plans_historicalobjectiveupdate_created_by_id_e5090280" ON "development_plans_historicalobjectiveupdate" ("created_by_id");
CREATE INDEX "development_plans_historicalobjectiveupdate_history_user_id_e89f67f7" ON "development_plans_historicalobjectiveupdate" ("history_user_id");
CREATE INDEX "development_plans_historicalobjectiveupdate_objective_id_b50fc0a8" ON "development_plans_historicalobjectiveupdate" ("objective_id");
CREATE INDEX "development_plans_milestone_created_by_id_76898851" ON "development_plans_milestone" ("created_by_id");
CREATE INDEX "development_plans_milestone_objective_id_bc2dcb8f" ON "development_plans_milestone" ("objective_id");
CREATE INDEX "development_objecti_08015a_idx" ON "development_plans_milestone" ("objective_id");
CREATE INDEX "development_is_comp_885f68_idx" ON "development_plans_milestone" ("is_completed");
CREATE INDEX "development_plans_objectiveupdate_created_by_id_fcf6cba4" ON "development_plans_objectiveupdate" ("created_by_id");
CREATE INDEX "development_plans_objectiveupdate_objective_id_90158dd2" ON "development_plans_objectiveupdate" ("objective_id");
CREATE INDEX "development_objecti_28a4ef_idx" ON "development_plans_objectiveupdate" ("objective_id");
CREATE INDEX "development_created_a2784d_idx" ON "development_plans_objectiveupdate" ("created_at");
CREATE INDEX "compensation_salaryinformation_updated_by_id_4394b41e" ON "compensation_salaryinformation" ("updated_by_id");
CREATE INDEX "compensation_salaryinformation_user_id_b59ff26b" ON "compensation_salaryinformation" ("user_id");
CREATE INDEX "dashboard_analyticsreport_generated_by_id_a7ba283b" ON "dashboard_analyticsreport" ("generated_by_id");
CREATE INDEX "dashboard_realtimestat_organization_id_9e843a39" ON "dashboard_realtimestat" ("organization_id");
CREATE UNIQUE INDEX "dashboard_forecastdata_forecast_type_forecast_date_department_id_organization_id_183bc01d_uniq" ON "dashboard_forecastdata" ("forecast_type", "forecast_date", "department_id", "organization_id");
CREATE INDEX "dashboard_forecastdata_department_id_fde42774" ON "dashboard_forecastdata" ("department_id");
CREATE INDEX "dashboard_forecastdata_organization_id_95ee3f85" ON "dashboard_forecastdata" ("organization_id");
CREATE UNIQUE INDEX "dashboard_trenddata_data_type_period_department_id_organization_id_efe813ff_uniq" ON "dashboard_trenddata" ("data_type", "period", "department_id", "organization_id");
CREATE INDEX "dashboard_trenddata_department_id_321c52fa" ON "dashboard_trenddata" ("department_id");
CREATE INDEX "dashboard_trenddata_organization_id_db02d078" ON "dashboard_trenddata" ("organization_id");
CREATE INDEX "notifications_notification_user_id_b5e8c0ff" ON "notifications_notification" ("user_id");
CREATE INDEX "notifications_notification_content_type_id_74ab3a2c" ON "notifications_notification" ("content_type_id");
CREATE INDEX "notifications_bulknotification_initiated_by_id_c9ccfc76" ON "notifications_bulknotification" ("initiated_by_id");
CREATE UNIQUE INDEX "notifications_notificationtemplate_methods_notificationtemplate_id_notificationmethod_id_b89ee7e9_uniq" ON "notifications_notificationtemplate_methods" ("notificationtemplate_id", "notificationmethod_id");
CREATE INDEX "notifications_notificationtemplate_methods_notificationtemplate_id_e3b77acf" ON "notifications_notificationtemplate_methods" ("notificationtemplate_id");
CREATE INDEX "notifications_notificationtemplate_methods_notificationmethod_id_574e9ac5" ON "notifications_notificationtemplate_methods" ("notificationmethod_id");
CREATE INDEX "notifications_pushnotification_user_id_0f5b6387" ON "notifications_pushnotification" ("user_id");
CREATE INDEX "notifications_smslog_recipient_id_2ffded95" ON "notifications_smslog" ("recipient_id");
CREATE INDEX "notifications_smslog_provider_id_b3fbe8e2" ON "notifications_smslog" ("provider_id");
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('django_migrations',68);
INSERT INTO "sqlite_sequence" VALUES('django_content_type',121);
INSERT INTO "sqlite_sequence" VALUES('auth_permission',484);
INSERT INTO "sqlite_sequence" VALUES('auth_group',2);
INSERT INTO "sqlite_sequence" VALUES('departments_department',12);
INSERT INTO "sqlite_sequence" VALUES('django_admin_log',1003);
INSERT INTO "sqlite_sequence" VALUES('accounts_user',34);
INSERT INTO "sqlite_sequence" VALUES('accounts_historicaluser',130);
INSERT INTO "sqlite_sequence" VALUES('accounts_role',4);
INSERT INTO "sqlite_sequence" VALUES('accounts_historicalrole',5);
INSERT INTO "sqlite_sequence" VALUES('accounts_role_permissions',327);
INSERT INTO "sqlite_sequence" VALUES('evaluations_questioncategory',14);
INSERT INTO "sqlite_sequence" VALUES('evaluations_question',62);
INSERT INTO "sqlite_sequence" VALUES('evaluations_historicalquestion',62);
INSERT INTO "sqlite_sequence" VALUES('departments_organization',5);
INSERT INTO "sqlite_sequence" VALUES('departments_historicalorganization',5);
INSERT INTO "sqlite_sequence" VALUES('auth_group_permissions',372);
INSERT INTO "sqlite_sequence" VALUES('accounts_user_groups',3);
INSERT INTO "sqlite_sequence" VALUES('accounts_user_user_permissions',838);
INSERT INTO "sqlite_sequence" VALUES('evaluations_campaignquestion',31);
INSERT INTO "sqlite_sequence" VALUES('evaluations_evaluationresult',3);
INSERT INTO "sqlite_sequence" VALUES('evaluations_evaluationassignment',55);
INSERT INTO "sqlite_sequence" VALUES('evaluations_historicalevaluationassignment',76);
INSERT INTO "sqlite_sequence" VALUES('notifications_emailtemplate',2);
INSERT INTO "sqlite_sequence" VALUES('reports_radarchartdata',1);
INSERT INTO "sqlite_sequence" VALUES('development_plans_progresslog',4);
INSERT INTO "sqlite_sequence" VALUES('notifications_emaillog',2);
INSERT INTO "sqlite_sequence" VALUES('development_plans_developmentgoal',4);
INSERT INTO "sqlite_sequence" VALUES('departments_historicalposition',11);
INSERT INTO "sqlite_sequence" VALUES('evaluations_response',90);
INSERT INTO "sqlite_sequence" VALUES('departments_historicaldepartment',13);
INSERT INTO "sqlite_sequence" VALUES('departments_position',10);
INSERT INTO "sqlite_sequence" VALUES('competencies_proficiencylevel',4);
INSERT INTO "sqlite_sequence" VALUES('competencies_competency',11);
INSERT INTO "sqlite_sequence" VALUES('competencies_historicalcompetency',11);
INSERT INTO "sqlite_sequence" VALUES('training_trainingresource',7);
INSERT INTO "sqlite_sequence" VALUES('training_historicaltrainingresource',10);
INSERT INTO "sqlite_sequence" VALUES('training_trainingresource_required_competencies',32);
INSERT INTO "sqlite_sequence" VALUES('training_usertraining',3);
INSERT INTO "sqlite_sequence" VALUES('training_historicalusertraining',3);
INSERT INTO "sqlite_sequence" VALUES('support_supportticket',2);
INSERT INTO "sqlite_sequence" VALUES('support_ticketcomment',6);
INSERT INTO "sqlite_sequence" VALUES('continuous_feedback_publicrecognition',4);
INSERT INTO "sqlite_sequence" VALUES('workforce_planning_competencygap',1);
INSERT INTO "sqlite_sequence" VALUES('workforce_planning_competencygap_recommended_trainings',6);
INSERT INTO "sqlite_sequence" VALUES('workforce_planning_criticalrole',1);
INSERT INTO "sqlite_sequence" VALUES('workforce_planning_criticalrole_required_competencies',8);
INSERT INTO "sqlite_sequence" VALUES('workforce_planning_successioncandidate',1);
INSERT INTO "sqlite_sequence" VALUES('workforce_planning_talentmatrix',1);
INSERT INTO "sqlite_sequence" VALUES('competencies_positioncompetency',1);
INSERT INTO "sqlite_sequence" VALUES('competencies_historicalpositioncompetency',1);
INSERT INTO "sqlite_sequence" VALUES('competencies_userskill',1);
INSERT INTO "sqlite_sequence" VALUES('competencies_historicaluserskill',1);
INSERT INTO "sqlite_sequence" VALUES('continuous_feedback_feedbackbank',4);
INSERT INTO "sqlite_sequence" VALUES('continuous_feedback_quickfeedback',5);
INSERT INTO "sqlite_sequence" VALUES('continuous_feedback_feedbacktag',6);
INSERT INTO "sqlite_sequence" VALUES('evaluations_evaluationcampaign',4);
INSERT INTO "sqlite_sequence" VALUES('evaluations_historicalevaluationcampaign',6);
INSERT INTO "sqlite_sequence" VALUES('reports_reportgenerationlog',1);
INSERT INTO "sqlite_sequence" VALUES('accounts_historicalprofile',169);
INSERT INTO "sqlite_sequence" VALUES('accounts_profile',34);
INSERT INTO "sqlite_sequence" VALUES('leave_attendance_holiday',1);
INSERT INTO "sqlite_sequence" VALUES('leave_attendance_historicalholiday',1);
INSERT INTO "sqlite_sequence" VALUES('recruitment_application',1);
INSERT INTO "sqlite_sequence" VALUES('leave_attendance_leavetype',2);
INSERT INTO "sqlite_sequence" VALUES('leave_attendance_historicalleavetype',3);
INSERT INTO "sqlite_sequence" VALUES('leave_attendance_leavebalance',1);
INSERT INTO "sqlite_sequence" VALUES('leave_attendance_historicalleavebalance',1);
INSERT INTO "sqlite_sequence" VALUES('leave_attendance_leaverequest',1);
INSERT INTO "sqlite_sequence" VALUES('leave_attendance_historicalleaverequest',2);
INSERT INTO "sqlite_sequence" VALUES('development_plans_strategicobjective',1);
INSERT INTO "sqlite_sequence" VALUES('development_plans_historicalstrategicobjective',8);
INSERT INTO "sqlite_sequence" VALUES('development_plans_kpi',1);
INSERT INTO "sqlite_sequence" VALUES('development_plans_historicalkpi',2);
INSERT INTO "sqlite_sequence" VALUES('continuous_feedback_recognitionlike',2);
INSERT INTO "sqlite_sequence" VALUES('continuous_feedback_recognitioncomment',2);
INSERT INTO "sqlite_sequence" VALUES('recruitment_jobposting',1);
INSERT INTO "sqlite_sequence" VALUES('recruitment_historicaljobposting',2);
INSERT INTO "sqlite_sequence" VALUES('recruitment_jobposting_recruiters',29);
INSERT INTO "sqlite_sequence" VALUES('recruitment_historicalapplication',2);
INSERT INTO "sqlite_sequence" VALUES('recruitment_offer',1);
INSERT INTO "sqlite_sequence" VALUES('recruitment_historicaloffer',1);
INSERT INTO "sqlite_sequence" VALUES('reports_systemkpi',2);
INSERT INTO "sqlite_sequence" VALUES('compensation_bonus',1);
INSERT INTO "sqlite_sequence" VALUES('compensation_historicalbonus',2);
INSERT INTO "sqlite_sequence" VALUES('compensation_compensationhistory',5);
INSERT INTO "sqlite_sequence" VALUES('compensation_historicalcompensationhistory',6);
INSERT INTO "sqlite_sequence" VALUES('compensation_historicalsalaryinformation',9);
INSERT INTO "sqlite_sequence" VALUES('compensation_allowance',1);
INSERT INTO "sqlite_sequence" VALUES('compensation_historicalallowance',2);
INSERT INTO "sqlite_sequence" VALUES('compensation_deduction',2);
INSERT INTO "sqlite_sequence" VALUES('compensation_historicaldeduction',2);
INSERT INTO "sqlite_sequence" VALUES('continuous_feedback_quickfeedback_tags',6);
INSERT INTO "sqlite_sequence" VALUES('development_plans_kpimeasurement',1);
INSERT INTO "sqlite_sequence" VALUES('development_plans_historicalkpimeasurement',1);
INSERT INTO "sqlite_sequence" VALUES('development_plans_keyresult',1);
INSERT INTO "sqlite_sequence" VALUES('development_plans_historicalkeyresult',4);
INSERT INTO "sqlite_sequence" VALUES('compensation_salaryinformation',6);
INSERT INTO "sqlite_sequence" VALUES('dashboard_realtimestat',7);
INSERT INTO "sqlite_sequence" VALUES('dashboard_trenddata',3);
INSERT INTO "sqlite_sequence" VALUES('dashboard_forecastdata',3);
INSERT INTO "sqlite_sequence" VALUES('dashboard_systemkpi',5);
INSERT INTO "sqlite_sequence" VALUES('notifications_notification',1572);
INSERT INTO "sqlite_sequence" VALUES('notifications_usernotificationpreference',2);
INSERT INTO "sqlite_sequence" VALUES('notifications_notificationtemplate',1);
INSERT INTO "sqlite_sequence" VALUES('notifications_smsprovider',1);
COMMIT;
