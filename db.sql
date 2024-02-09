CREATE TABLE `Categories` (
  `Id` Integer UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(500) UNIQUE NOT NULL,
  `Description` TEXT NOT NULL,
  `CreatedAt` Timestamp NOT NULL,
  `UpdatedAt` Timestamp
);

CREATE TABLE `Products` (
  `Id` Integer UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(500) NOT NULL,
  `Description` TEXT,
  `Stock` Integer NOT NULL,
  `Quantity` Integer NOT NULL,
  `Size` VARCHAR(500),
  `Weight` Double,
  `Color` VARCHAR(500),
  `Cover` TEXT,
  `Price` Double NOT NULL,
  `Status` VARCHAR(500) NOT NULL,
  `Available` Bit NOT NULL,
  `Display` Bit NOT NULL,
  `VariantOf` Integer,
  `CreatedAt` Timestamp NOT NULL,
  `UpdatedAt` Timestamp
);

CREATE TABLE `ProductCategories` (
  `Id` Integer UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `ProductId` Integer NOT NULL,
  `CategoryId` Integer NOT NULL,
  `CreatedAt` Timestamp NOT NULL,
  `UpdatedAt` Timestamp
);

CREATE TABLE `Discounts` (
  `Id` Integer UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `ProductId` Integer NOT NULL,
  `Percent` Double NOT NULL,
  `Units` Integer NOT NULL,
  `ActiveFrom` Timestamp NOT NULL,
  `ActiveTo` Timestamp,
  `CreatedAt` Timestamp NOT NULL,
  `UpdatedAt` Timestamp
);

CREATE TABLE `PrecingHistory` (
  `Id` Integer UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `ProductId` Integer NOT NULL,
  `Price` Double NOT NULL,
  `ActiveFrom` Timestamp NOT NULL,
  `ActiveTo` Timestamp,
  `CreatedAt` Timestamp NOT NULL,
  `UpdatedAt` Timestamp
);

CREATE TABLE `VariatingHistory` (
  `Id` Integer UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `ProductId` Integer NOT NULL,
  `VariantId` Integer NOT NULL,
  `ActiveFrom` Timestamp NOT NULL,
  `ActiveTo` Timestamp,
  `CreatedAt` Timestamp NOT NULL,
  `UpdatedAt` Timestamp
);

CREATE TABLE `ProductMedia` (
  `Id` Integer UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `ProductId` Integer NOT NULL,
  `Url` TEXT NOT NULL,
  `Type` VARCHAR(255) NOT NULL,
  `CreatedAt` Timestamp NOT NULL,
  `UpdatedAt` Timestamp
);

ALTER TABLE `ProductCategories` ADD FOREIGN KEY (`ProductId`) REFERENCES `Products` (`Id`);

ALTER TABLE `ProductCategories` ADD FOREIGN KEY (`CategoryId`) REFERENCES `Categories` (`Id`);

ALTER TABLE `PrecingHistory` ADD FOREIGN KEY (`ProductId`) REFERENCES `Products` (`Id`);

ALTER TABLE `Discounts` ADD FOREIGN KEY (`ProductId`) REFERENCES `Products` (`Id`);

ALTER TABLE `VariatingHistory` ADD FOREIGN KEY (`ProductId`) REFERENCES `Products` (`Id`);

ALTER TABLE `VariatingHistory` ADD FOREIGN KEY (`VariantId`) REFERENCES `Products` (`Id`);

ALTER TABLE `Products` ADD FOREIGN KEY (`VariantOf`) REFERENCES `Products` (`Id`);

ALTER TABLE `ProductMedia` ADD FOREIGN KEY (`ProductId`) REFERENCES `Products` (`Id`);