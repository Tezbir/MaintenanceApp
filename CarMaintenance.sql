create table users(
user_id bigint auto_increment primary key,
user_name varchar(30),
user_email varchar(100) not null unique,
user_password varchar(18) not null,
user_creation_date timestamp default current_timestamp
);

CREATE TABLE vee (
  vee_id bigint unsigned auto_increment primary key,
  user_id bigint unsigned not null,     
  vee_name varchar(100),
  vee_year smallint unsigned,        
  vee_make varchar(100),              
  vee_model varchar(100),
  vee_vin varchar(17),              
  vee_mileage int unsigned not null default 0,
  vee_stamped timestamp default current_timestamp,

 CONSTRAINT fk_vee_user
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    ON DELETE CASCADE,
  CONSTRAINT uq_user_vin
    UNIQUE (user_id, vee_vin)
    
) ENGINE=InnoDB;

CREATE INDEX idx_vee_user_id ON vee(user_id);

create table service_type(
service_type_id bigint auto_increment primary key,
service_type_name varchar(100) unique,
service_type_default_interval_miles INT UNSIGNED NULL,
service_type_default_interval_days INT UNSIGNED NULL,
service_type_created_at timestamp NOT NULL default current_timestamp
);

CREATE TABLE service_record (
  service_record_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  vee_id BIGINT UNSIGNED NOT NULL,
  service_type_id BIGINT UNSIGNED NOT NULL,
  service_record_date DATE NOT NULL,
  service_record_mileage INT UNSIGNED NOT NULL,
  
  service_record_cost DECIMAL(10,2) NULL,
  service_record_notes TEXT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_record_vee
    FOREIGN KEY (vee_id) REFERENCES vee(vee_id)
    ON DELETE CASCADE,
  CONSTRAINT fk_record_type
    FOREIGN KEY (service_type_id) REFERENCES service_type(service_type_id)
    ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE INDEX idx_record_vee_date ON service_record(vee_id, service_record_date DESC);
CREATE INDEX idx_record_vee_type ON service_record(vee_id, service_type_id, service_record_mileage DESC);
show tables;
