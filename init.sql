create table if not exists public.subscribers(
uuid varchar not null unique,
name varchar not null,
balance integer not null,
hold integer not null,
status integer not null);
insert into subscribers (uuid,name,balance, hold, status ) values ('26c940a1-7228-4ea2-a3bc-e6460b172040', 'Петров Иван Сергеевич', '1700', '300', '1');
insert into subscribers (uuid,name,balance, hold, status ) values ('7badc8f8-65bc-449a-8cde-855234ac63e1', 'Kazitsky Jason', '200', '200', '1');
insert into subscribers (uuid,name,balance, hold, status ) values ('5597cc3d-c948-48a0-b711-393edf20d9c0', 'Пархоменко Антон Александрович', '10', '300', '1');
insert into subscribers (uuid,name,balance, hold, status ) values ('867f0924-a917-4711-939b-90b179a96392', 'Петечкин Петр Измаилович', '1000000', '1', '0');