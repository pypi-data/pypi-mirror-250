"""
Módulo departamentos del Perú.

Incluye las clases:
- Departamento
"""
from unidecode import unidecode

departaments_peru = {
    "Amazonas": {
        "ubigeo": "01",
        "poblacion": 426806,
        "superficie_km2": 39249.17,
        "capital": "Chachapoyas",
        "provincias": 7,
        "provincias_lista": ["Bagua", "Bongará", "Chachapoyas", "Condorcanqui", "Luya", "Rodríguez de Mendoza", "Utcubamba"]
    },
    "Áncash": {
        "ubigeo": "02",
        "poblacion": 1143073,
        "superficie_km2": 35978.29,
        "capital": "Huaraz",
        "provincias": 20,
        "provincias_lista": ["Aija", "Antonio Raimondi", "Asunción", "Bolognesi", "Carhuaz", "Carlos Fermín Fitzcarrald", "Casma", "Corongo", "Huari", "Huarmey", "Huaylas", "Mariscal Luzuriaga", "Ocros", "Pallasca", "Pomabamba", "Recuay", "Santa", "Sihuas", "Yungay", "Independencia"]
    },
    "Apurímac": {
        "ubigeo": "03",
        "poblacion": 405759,
        "superficie_km2": 21187.15,
        "capital": "Abancay",
        "provincias": 7,
        "provincias_lista": ["Abancay", "Andahuaylas", "Antabamba", "Aymaraes", "Cotabambas", "Grau", "Chincheros"]
    },
    "Arequipa": {
        "ubigeo": "04",
        "poblacion": 1382730,
        "superficie_km2": 63247.22,
        "capital": "Arequipa",
        "provincias": 8,
        "provincias_lista": ["Arequipa", "Camaná", "Caravelí", "Castilla", "Caylloma", "Condesuyos", "Islay", "La Unión"]
    },
    "Ayacucho": {
        "ubigeo": "05",
        "poblacion": 616176,
        "superficie_km2": 43116.05,
        "capital": "Ayacucho",
        "provincias": 11,
        "provincias_lista": ["Huamanga", "Cangallo", "Huanca Sancos", "Huanta", "La Mar", "Lucanas", "Parinacochas", "Páucar del Sara Sara", "Sucre", "Víctor Fajardo", "Vilcas Huamán"]
    },
    "Cajamarca": {
        "ubigeo": "06",
        "poblacion": 1473586,
        "superficie_km2": 33324.87,
        "capital": "Cajamarca",
        "provincias": 13,
        "provincias_lista": ["Cajamarca", "Cajabamba", "Celendín", "Chota", "Contumazá", "Cutervo", "Hualgayoc", "Jaén", "San Ignacio", "San Marcos", "San Miguel", "San Pablo", "Santa Cruz"]
    },
    "Callao": {
        "ubigeo": "07",
        "poblacion": 994494,
        "superficie_km2": 147.98,
        "capital": "Callao",
        "provincias": 1,
        "provincias_lista": ["Callao"]
    },
    "Cusco": {
        "ubigeo": "08",
        "poblacion": 1408815,
        "superficie_km2": 71844.11,
        "capital": "Cusco",
        "provincias": 13,
        "provincias_lista": ["Cusco", "Acomayo", "Anta", "Calca", "Canas", "Canchis", "Chumbivilcas", "Espinar", "La Convención", "Paruro", "Paucartambo", "Quispicanchi", "Urubamba"]
    },
    "Huancavelica": {
        "ubigeo": "09",
        "poblacion": 454797,
        "superficie_km2": 22239.38,
        "capital": "Huancavelica",
        "provincias": 7,
        "provincias_lista": ["Huancavelica", "Acobamba", "Angaraes", "Castrovirreyna", "Churcampa", "Huaytará", "Tayacaja"]
    },
    "Huánuco": {
        "ubigeo": "10",
        "poblacion": 811779,
        "superficie_km2": 36895.98,
        "capital": "Huánuco",
        "provincias": 11,
        "provincias_lista": ["Huánuco", "Ambo", "Dos de Mayo", "Huacaybamba", "Huamalíes", "Leoncio Prado", "Marañón", "Pachitea", "Puerto Inca", "Lauricocha", "Yarowilca"]
    },
    "Ica": {
        "ubigeo": "11",
        "poblacion": 843547,
        "superficie_km2": 21385.94,
        "capital": "Ica",
        "provincias": 5,
        "provincias_lista": ["Ica", "Chincha", "Nasca", "Palpa", "Pisco"]
    },
    "Junín": {
        "ubigeo": "12",
        "poblacion": 1436419,
        "superficie_km2": 44581.21,
        "capital": "Huancayo",
        "provincias": 9,
        "provincias_lista": ["Huancayo", "Concepción", "Chanchamayo", "Jauja", "Junín", "Satipo", "Tarma", "Yauli", "Chupaca"]
    },
    "La Libertad": {
        "ubigeo": "13",
        "poblacion": 1880538,
        "superficie_km2": 25392.25,
        "capital": "Trujillo",
        "provincias": 12,
        "provincias_lista": ["Trujillo", "Ascope", "Bolívar", "Chepén", "Julcán", "Otuzco", "Pacasmayo", "Pataz", "Sánchez Carrión", "Santiago de Chuco", "Gran Chimú", "Virú"]
    },
    "Lambayeque": {
        "ubigeo": "14",
        "poblacion": 1229196,
        "superficie_km2": 14149.37,
        "capital": "Chiclayo",
        "provincias": 3,
        "provincias_lista": ["Chiclayo", "Ferreñafe", "Lambayeque"]
    },
    "Lima": {
        "ubigeo": "15",
        "poblacion": 11128658,
        "superficie_km2": 32888.02,
        "capital": "Lima",
        "provincias": 10,
        "provincias_lista": ["Lima", "Barranca", "Cajatambo", "Canta", "Cañete", "Huaral", "Huarochirí", "Huaura", "Oyón", "Yauyos"]
    },
    "Loreto": {
        "ubigeo": "16",
        "poblacion": 1083279,
        "superficie_km2": 368852.26,
        "capital": "Iquitos",
        "provincias": 8,
        "provincias_lista": ["Maynas", "Alto Amazonas", "Loreto", "Mariscal Ramón Castilla", "Requena", "Ucayali", "Datem del Marañón", "Putumayo"]
    },
    "Madre de Dios": {
        "ubigeo": "17",
        "poblacion": 157257,
        "superficie_km2": 85164.05,
        "capital": "Puerto Maldonado",
        "provincias": 3,
        "provincias_lista": ["Tambopata", "Manu", "Tahuamanu"]
    },
    "Moquegua": {
        "ubigeo": "18",
        "poblacion": 191559,
        "superficie_km2": 15884.17,
        "capital": "Moquegua",
        "provincias": 3,
        "provincias_lista": ["Mariscal Nieto", "General Sánchez Cerro", "Ilo"]
    },
    "Pasco": {
        "ubigeo": "19",
        "poblacion": 280691,
        "superficie_km2": 25418.78,
        "capital": "Cerro de Pasco",
        "provincias": 3,
        "provincias_lista": ["Pasco", "Daniel Alcídes Carrión", "Oxapampa"]
    },
    "Piura": {
        "ubigeo": "20",
        "poblacion": 2053479,
        "superficie_km2": 35693.47,
        "capital": "Piura",
        "provincias": 8,
        "provincias_lista": ["Piura", "Ayabaca", "Huancabamba", "Morropón", "Paita", "Sullana", "Talara", "Sechura"]
    },
    "Puno": {
        "ubigeo": "21",
        "poblacion": 1314857,
        "superficie_km2": 67924.85,
        "capital": "Puno",
        "provincias": 13,
        "provincias_lista": ["Puno", "Azángaro", "Carabaya", "Chucuito", "El Collao", "Huancané", "Lampa", "Melgar", "Moho", "San Antonio de Putina", "San Román", "Sandia", "Yunguyo"]
    },
    "San Martín": {
        "ubigeo": "22",
        "poblacion": 877588,
        "superficie_km2": 51289.18,
        "capital": "Moyobamba",
        "provincias": 10,
        "provincias_lista": ["Moyobamba", "Bellavista", "El Dorado", "Huallaga", "Lamas", "Mariscal Cáceres", "Picota", "Rioja", "San Martín", "Tocache"]
    },
    "Tacna": {
        "ubigeo": "23",
        "poblacion": 365317,
        "superficie_km2": 16076.32,
        "capital": "Tacna",
        "provincias": 4,
        "provincias_lista": ["Tacna", "Candarave", "Jorge Basadre", "Tarata"]
    },
    "Tumbes": {
        "ubigeo": "24",
        "poblacion": 251521,
        "superficie_km2": 4662.75,
        "capital": "Tumbes",
        "provincias": 3,
        "provincias_lista": ["Tumbes", "Contralmirante Villar", "Zarumilla"]
    },
    "Ucayali": {
        "ubigeo": "25",
        "poblacion": 589110,
        "superficie_km2": 102410.09,
        "capital": "Pucallpa",
        "provincias": 4,
        "provincias_lista": ["Coronel Portillo", "Atalaya", "Padre Abad", "Purús"]
    }
}


class Departamento:
    """
    Methods: 
    - search(name)
    """

    def search(self, name):
        """
        search("[name]")

        - name: argument of name departament's

        - Results: Departamento, Ubigeo, Población, Superficie (km²),
        Capital, Número de provincias, Provincias

        - Example:
        search("Lima")

        """
        departament = unidecode("".join(name))  # Convertir a ASCII
        for dept, details in departaments_peru.items():
            if departament.lower() == unidecode(dept).lower():
                print("Departamento:", dept)
                print("Ubigeo:", details["ubigeo"])
                print("Población:", details["poblacion"])
                print("Superficie (km²):", details["superficie_km2"])
                print("Capital:", details["capital"])
                print("Número de provincias:", details["provincias"])
                print("Provincias:", ", ".join(details["provincias_lista"]))
                return
        print(f"No existe el departamento '{departament}'")