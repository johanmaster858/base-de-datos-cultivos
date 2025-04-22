-- Creación de la estructura de la base de datos para el sistema de recomendación de cultivos

-- Tabla CULTIVOS
CREATE TABLE cultivos (
    id_cultivo INTEGER PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    nombre_cientifico VARCHAR(100),
    descripcion TEXT,
    tipo VARCHAR(50),
    ciclo_dias INTEGER,
    densidad_siembra VARCHAR(100),
    imagen VARCHAR(255)
);

-- Tabla CONDICIONES
CREATE TABLE condiciones (
    id_condicion INTEGER PRIMARY KEY,
    id_cultivo INTEGER,
    temp_min DECIMAL(5,2),
    temp_max DECIMAL(5,2),
    precipitacion_min INTEGER,
    precipitacion_max INTEGER,
    tipo_suelo VARCHAR(100),
    ph_min DECIMAL(3,1),
    ph_max DECIMAL(3,1),
    altitud_min INTEGER,
    altitud_max INTEGER,
    FOREIGN KEY (id_cultivo) REFERENCES cultivos(id_cultivo)
);

-- Tabla ZONAS
CREATE TABLE zonas (
    id_zona INTEGER PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    departamento VARCHAR(50),
    altitud_min INTEGER,
    altitud_max INTEGER,
    temp_promedio DECIMAL(5,2),
    precipitacion INTEGER
);

-- Tabla CULTIVO_ZONA
CREATE TABLE cultivo_zona (
    id_cultivo INTEGER,
    id_zona INTEGER,
    rendimiento DECIMAL(10,2),
    rentabilidad VARCHAR(20),
    popularidad INTEGER,
    PRIMARY KEY (id_cultivo, id_zona),
    FOREIGN KEY (id_cultivo) REFERENCES cultivos(id_cultivo),
    FOREIGN KEY (id_zona) REFERENCES zonas(id_zona)
);

-- Tabla COSTOS
CREATE TABLE costos (
    id_costo INTEGER PRIMARY KEY,
    id_cultivo INTEGER,
    inversion_min DECIMAL(15,2),
    inversion_max DECIMAL(15,2),
    costo_operativo DECIMAL(15,2),
    precio_interno DECIMAL(15,2),
    precio_export DECIMAL(15,2),
    rentabilidad DECIMAL(5,2),
    fecha_actualizacion DATE,
    FOREIGN KEY (id_cultivo) REFERENCES cultivos(id_cultivo)
);

-- Tabla PLAGAS_ENFERMEDADES
CREATE TABLE plagas_enfermedades (
    id_plaga INTEGER PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    nombre_cientifico VARCHAR(100),
    tipo VARCHAR(50),
    descripcion TEXT,
    control TEXT,
    imagen VARCHAR(255)
);

-- Tabla CULTIVO_PLAGA
CREATE TABLE cultivo_plaga (
    id_cultivo INTEGER,
    id_plaga INTEGER,
    severidad VARCHAR(20),
    frecuencia VARCHAR(20),
    PRIMARY KEY (id_cultivo, id_plaga),
    FOREIGN KEY (id_cultivo) REFERENCES cultivos(id_cultivo),
    FOREIGN KEY (id_plaga) REFERENCES plagas_enfermedades(id_plaga)
);

-- Tabla INSUMOS
CREATE TABLE insumos (
    id_insumo INTEGER PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(50),
    descripcion TEXT,
    unidad_medida VARCHAR(20),
    precio_promedio DECIMAL(15,2),
    fecha_actualizacion DATE
);

-- Tabla INSUMO_CULTIVO
CREATE TABLE insumo_cultivo (
    id_insumo INTEGER,
    id_cultivo INTEGER,
    cantidad_por_ha DECIMAL(10,2),
    etapa_aplicacion VARCHAR(50),
    frecuencia VARCHAR(50),
    PRIMARY KEY (id_insumo, id_cultivo),
    FOREIGN KEY (id_insumo) REFERENCES insumos(id_insumo),
    FOREIGN KEY (id_cultivo) REFERENCES cultivos(id_cultivo)
);

-- Tabla PROVEEDORES
CREATE TABLE proveedores (
    id_proveedor INTEGER PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo VARCHAR(50),
    contacto VARCHAR(100),
    ubicacion VARCHAR(255),
    sitio_web VARCHAR(255),
    telefono VARCHAR(20)
);

-- Tabla PROVEEDOR_INSUMO
CREATE TABLE proveedor_insumo (
    id_proveedor INTEGER,
    id_insumo INTEGER,
    precio DECIMAL(15,2),
    disponibilidad VARCHAR(50),
    PRIMARY KEY (id_proveedor, id_insumo),
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor),
    FOREIGN KEY (id_insumo) REFERENCES insumos(id_insumo)
);

-- Tabla TECNICAS
CREATE TABLE tecnicas (
    id_tecnica INTEGER PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(50),
    descripcion TEXT,
    dificultad VARCHAR(20),
    beneficios TEXT
);

-- Tabla TECNICA_CULTIVO
CREATE TABLE tecnica_cultivo (
    id_tecnica INTEGER,
    id_cultivo INTEGER,
    importancia VARCHAR(20),
    etapa_aplicacion VARCHAR(50),
    PRIMARY KEY (id_tecnica, id_cultivo),
    FOREIGN KEY (id_tecnica) REFERENCES tecnicas(id_tecnica),
    FOREIGN KEY (id_cultivo) REFERENCES cultivos(id_cultivo)
);

-- Tabla CERTIFICACIONES
CREATE TABLE certificaciones (
    id_certificacion INTEGER PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    entidad VARCHAR(100),
    requisitos TEXT,
    beneficios TEXT,
    duracion VARCHAR(50)
);

-- Tabla CULTIVO_CERTIFICACION
CREATE TABLE cultivo_certificacion (
    id_cultivo INTEGER,
    id_certificacion INTEGER,
    mercado_objetivo VARCHAR(100),
    premium_precio DECIMAL(5,2),
    PRIMARY KEY (id_cultivo, id_certificacion),
    FOREIGN KEY (id_cultivo) REFERENCES cultivos(id_cultivo),
    FOREIGN KEY (id_certificacion) REFERENCES certificaciones(id_certificacion)
);

-- Creación de índices para optimizar consultas
CREATE INDEX idx_cultivos_tipo ON cultivos(tipo);
CREATE INDEX idx_condiciones_cultivo ON condiciones(id_cultivo);
CREATE INDEX idx_zonas_departamento ON zonas(departamento);
CREATE INDEX idx_costos_cultivo ON costos(id_cultivo);
CREATE INDEX idx_plagas_tipo ON plagas_enfermedades(tipo);
CREATE INDEX idx_insumos_categoria ON insumos(categoria);
CREATE INDEX idx_proveedores_tipo ON proveedores(tipo);
CREATE INDEX idx_tecnicas_categoria ON tecnicas(categoria);
