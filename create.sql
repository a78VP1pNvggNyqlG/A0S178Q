Create table goods
( id char(8) primary key,
  brandName char(30) Not null,
  category char(30),
  originalPrice float,
  priceOnsale float,
  size1Amount int,
  size2Amount int,
  size3Amount int,
  size4Amount int,
  size5Amount int,
  size6Amount int,
  size7Amount int,
  size8Amount int,
  size9Amount int,
  size10Amount int,
  description char(200),
  fit char(20),
  tissue char(10));

Create table Localisation
( genre char(20) primary key,
Eng  char(30) ,
Chi char(30),
Fra char(30),
Ita char(30));

