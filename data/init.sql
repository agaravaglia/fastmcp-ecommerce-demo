-- Create the users table
CREATE TABLE users (
    user_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(255),
    shipping_address TEXT
);

-- Create the products table
CREATE TABLE products (
    product_id VARCHAR(255) PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    description TEXT,
    price NUMERIC(12, 2) NOT NULL,
    stock_quantity INTEGER NOT NULL,
    category VARCHAR(255)
);

-- Create the orders table
CREATE TABLE orders (
    order_id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) REFERENCES users(user_id),
    product_id VARCHAR(255) REFERENCES products(product_id),
    quantity INTEGER NOT NULL,
    purchase_date DATE NOT NULL,
    delivery_date DATE,
    status VARCHAR(50) NOT NULL CHECK (status IN ('in_progress', 'submitted', 'delivered'))
);

-- Populate the users table
INSERT INTO users (user_id, name, email, phone_number, shipping_address) VALUES
('usr_001', 'John Doe', 'john.doe@email.com', '555-0101', '123 Maple Street, Anytown, USA 12345'),
('usr_002', 'Jane Smith', 'jane.smith@email.com', '555-0102', '456 Oak Avenue, Sometown, USA 67890'),
('usr_003', 'Marc Unknown', 'marc.unknown@email.com', '555-0103', '789 Pine Lane, Otherville, USA 11223'),
('usr_004', 'Alice Wonder', 'alice.wonder@email.com', '555-0104', '101 Wonderland Road, Teatown, USA 33445'),
('usr_005', 'Robert Builder', 'bob.builder@email.com', '555-0105', '212 Build It Ave, Construct, USA 55667'),
('usr_006', 'Clara Oswald', 'clara.oswald@email.com', '555-0106', '321 Tardis Way, Gallifrey, UK 99887'),
('usr_007', 'Peter Parker', 'p.parker@email.com', '555-0107', '20 Ingram Street, Forest Hills, USA 10001'),
('usr_008', 'Tony Stark', 'tony.stark@email.com', '555-0108', '10880 Malibu Point, Malibu, USA 90265'),
('usr_009', 'Bruce Wayne', 'bruce.wayne@email.com', '555-0109', '1007 Mountain Drive, Gotham, USA 50001'),
('usr_010', 'Diana Prince', 'diana.prince@email.com', '555-0110', 'Gateway City, Themyscira, USA 40001');

-- Populate the products table
INSERT INTO products (product_id, product_name, description, price, stock_quantity, category) VALUES
('car_001', 'Aether R1', 'A supercar that defies gravity.', 450000.00, 5, 'Supercar'),
('car_002', 'Vortex GT', 'Experience the whirlwind of speed.', 320000.00, 8, 'Supercar'),
('car_003', 'Nebula Roadster', 'Cruise the cosmos in style.', 780000.00, 3, 'Hypercar'),
('car_004', 'FakeCar3000', 'A reliable and fast sports car for daily driving.', 85000.00, 15, 'Sports Car'),
('car_005', 'Solaris F1', 'Harness the power of the sun. Track-focused.', 1200000.00, 2, 'Hypercar'),
('car_006', 'Quasar Coupe', 'A bright star in the world of grand tourers.', 210000.00, 12, 'Grand Tourer'),
('car_007', 'Pulsar 900X', 'Electric hypercar with instant torque.', 950000.00, 6, 'Hypercar'),
('car_008', 'Comet R-Spec', 'Leaves a trail of fire and awe.', 375000.00, 7, 'Supercar'),
('car_009', 'Galaxy Tourer', 'Ultimate comfort for interstellar journeys.', 280000.00, 10, 'Grand Tourer'),
('car_010', 'Meteor S', 'A compact and explosive sports car.', 110000.00, 20, 'Sports Car'),
('car_011', 'Stardust Spyder', 'Open-top cruising under the stars.', 480000.00, 4, 'Supercar'),
('car_012', 'Blade Runner', 'Futuristic design meets raw power.', 650000.00, 5, 'Hypercar'),
('car_013', 'Velocity V12', 'The pinnacle of internal combustion engines.', 550000.00, 6, 'Supercar'),
('car_014', 'Stealth Bomber', 'So quiet, they won''t hear you coming.', 1500000.00, 1, 'Hypercar'),
('car_015', 'Apex Predator', 'Rule the track with unmatched performance.', 420000.00, 9, 'Supercar'),
('car_016', 'Juggernaut GT', 'An unstoppable force on the road.', 250000.00, 11, 'Grand Tourer'),
('car_017', 'Serpent GTS', 'Sleek, venomous, and incredibly fast.', 130000.00, 18, 'Sports Car'),
('car_018', 'Titan E-GT', 'A titan of electric grand touring.', 310000.00, 7, 'Grand Tourer'),
('car_019', 'Phoenix Fury', 'Rises from the ashes of its competitors.', 390000.00, 8, 'Supercar'),
('car_020', 'Wraith Shadow', 'A ghostly presence on the streets.', 880000.00, 3, 'Hypercar');

-- Populate the orders table
INSERT INTO orders (order_id, product_id, quantity, purchase_date, delivery_date, user_id, status) VALUES
('ord_001', 'car_001', 1, '2025-01-15', '2025-04-15', 'usr_008', 'delivered'),
('ord_002', 'car_004', 1, '2025-02-20', '2025-03-20', 'usr_001', 'delivered'),
('ord_003', 'car_010', 1, '2025-03-01', '2025-04-01', 'usr_002', 'delivered'),
('ord_004', 'car_003', 1, '2025-03-10', '2025-09-10', 'usr_009', 'submitted'),
('ord_005', 'car_007', 1, '2025-04-05', '2025-10-05', 'usr_008', 'submitted'),
('ord_006', 'car_017', 1, '2025-04-12', '2025-05-12', 'usr_007', 'delivered'),
('ord_007', 'car_009', 1, '2025-04-20', '2025-06-20', 'usr_005', 'delivered'),
('ord_008', 'car_012', 1, '2025-05-01', '2025-11-01', 'usr_010', 'submitted'),
('ord_009', 'car_015', 1, '2025-05-15', '2025-08-15', 'usr_003', 'delivered'),
('ord_010', 'car_002', 1, '2025-05-25', '2025-08-25', 'usr_004', 'delivered'),
('ord_011', 'car_005', 1, '2025-06-02', '2026-01-02', 'usr_009', 'in_progress'),
('ord_012', 'car_019', 1, '2025-06-10', '2025-09-10', 'usr_006', 'submitted'),
('ord_013', 'car_020', 1, '2025-06-18', '2026-02-18', 'usr_009', 'in_progress'),
('ord_014', 'car_008', 1, '2025-06-22', '2025-09-22', 'usr_001', 'submitted'),
('ord_015', 'car_011', 1, '2025-07-01', '2025-10-01', 'usr_002', 'submitted'),
('ord_016', 'car_014', 1, '2025-07-05', '2026-07-05', 'usr_008', 'in_progress'),
('ord_017', 'car_006', 1, '2025-07-11', '2025-09-11', 'usr_003', 'submitted'),
('ord_018', 'car_013', 1, '2025-07-15', '2025-11-15', 'usr_004', 'in_progress'),
('ord_019', 'car_018', 1, '2025-07-20', '2025-10-20', 'usr_005', 'submitted'),
('ord_020', 'car_016', 1, '2025-07-28', '2025-10-28', 'usr_006', 'in_progress'),
('ord_021', 'car_004', 1, '2025-08-01', '2025-09-01', 'usr_007', 'in_progress'),
('ord_022', 'car_010', 1, '2025-08-05', '2025-09-05', 'usr_010', 'submitted'),
('ord_023', 'car_001', 1, '2024-11-10', '2025-02-10', 'usr_009', 'delivered'),
('ord_024', 'car_002', 1, '2024-12-01', '2025-03-01', 'usr_008', 'delivered'),
('ord_025', 'car_017', 1, '2025-01-05', '2025-02-05', 'usr_001', 'delivered'),
('ord_026', 'car_004', 1, '2025-08-10', '2025-09-10', 'usr_002', 'in_progress'),
('ord_027', 'car_009', 1, '2025-08-12', '2025-10-12', 'usr_003', 'submitted'),
('ord_028', 'car_015', 1, '2025-08-13', '2025-11-13', 'usr_005', 'in_progress'),
('ord_029', 'car_007', 1, '2024-10-01', '2025-04-01', 'usr_010', 'delivered'),
('ord_030', 'car_003', 1, '2025-08-01', '2026-02-01', 'usr_008', 'in_progress');