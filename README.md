# Generador de Posts de LinkedIn con IA

Genera posts profesionales para LinkedIn usando IA de forma automática.

## Requisitos

- Docker y Docker Compose
- API Key de Groq (gratuita) - [Obtener aquí](https://console.groq.com)

## Instalación y Ejecución

### 1. Clonar o descargar el proyecto

```bash
git clone <tu-repositorio>
cd linkedin-post-generator
```

### 2. Configurar API Key

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar y agregar tu API key
nano .env  # o usa tu editor favorito
```

Tu archivo `.env` debe verse así:
```
GROQ_API_KEY=gsk_tu_api_key_aqui
```

### 3. Crear directorio de salida

```bash
mkdir output
```

### 4. Ejecutar con Docker

```bash
# Opción 1: Ejecutar directamente (recomendado)
docker-compose run --rm linkedin-generator

# Opción 2: Construir primero
docker-compose build
docker-compose run --rm linkedin-generator
```

### 5. Seguir las instrucciones

El programa te pedirá:
- API key (o presiona Enter si ya está en `.env`)
- Cantidad de posts a generar

## Estructura del Proyecto

```
linkedin-post-generator/
├── Dockerfile              # Configuración de Docker
├── docker-compose.yml      # Orquestación de servicios
├── requirements.txt        # Dependencias de Python
├── linkedin_post_generator.py  # Script principal
├── .env                    # Tu API key (no compartir)
├── .env.example           # Plantilla de configuración
└── output/                # Posts generados (JSON y TXT)
```

## Resultado

Los posts se generarán en la carpeta `output/` con dos formatos:
- `linkedin_posts_XXXXXX.json` - Formato estructurado
- `linkedin_posts_XXXXXX.txt` - Formato legible para copiar/pegar

## Comandos Útiles

```bash
# Ver posts generados
ls output/
cat output/linkedin_posts_*.txt

# Limpiar contenedores
docker-compose down

# Reconstruir imagen
docker-compose build --no-cache

# Ver logs
docker-compose logs
```

## Uso sin Docker (Opcional)

Si prefieres ejecutar sin Docker:

```bash
# Instalar Python 3.11+
pip install -r requirements.txt

# Configurar API key
export GROQ_API_KEY=tu_api_key_aqui

# Ejecutar
python linkedin_post_generator.py
```

## Categorías de Posts

El generador crea posts sobre:
- **Empleo**: Consejos de carrera, networking, entrevistas
- **Java/Spring**: Tips técnicos, mejores prácticas, arquitectura
- **Idiomas**: Aprendizaje de inglés/portugués para profesionales

## Personalizar los Posts

Puedes personalizar el generador editando `linkedin_post_generator.py`:

### 1. Agregar Nuevas Categorías

Edita el diccionario `self.temas` (línea ~15):

```python
self.temas = {
    "empleo": [...],
    "java_spring": [...],
    "idiomas": [...],
    # Agregar tu nueva categoría
    "inteligencia_artificial": [
        "ChatGPT y productividad",
        "IA generativa en desarrollo",
        "Machine Learning para principiantes",
        "Ética en IA"
    ]
}
```

### 2. Modificar el Estilo de los Posts

Edita los prompts en `generar_prompt()` (línea ~40):

```python
"tu_categoria": f"""Crea un post para LinkedIn sobre "{tema}".
El post debe:
- Tener entre 150-200 palabras  # Cambia el tamaño
- Ser inspirador y técnico      # Define el tono
- Incluir estadísticas          # Agrega requisitos
- Usar emojis moderadamente     # Personaliza formato
- Terminar con call-to-action
- NO incluir hashtags
- Escribir en tercera persona   # Cambia perspectiva
"""
```

### 3. Personalizar Hashtags

Modifica `agregar_hashtags()` (línea ~100):

```python
hashtags_map = {
    "empleo": ["#Empleo", "#Carrera", "#TuHashtag"],
    "tu_categoria": ["#IA", "#Tech", "#Innovation", "#TuMarca"]
}
# Cambia cantidad de hashtags
return " ".join(tags[:3])  # Usa 3 en lugar de 4
```

### 4. Cambiar el Modelo de IA

Edita la llamada a la API (línea ~70):

```python
data = {
    "model": "llama-3.3-70b-versatile",  # Cambiar modelo
    "temperature": 0.8,    # 0.1-1.0: creatividad (más alto = más creativo)
    "max_tokens": 500      # Longitud máxima del post
}
```

**Modelos disponibles en Groq:**
- `llama-3.3-70b-versatile` - Equilibrado (recomendado)
- `llama-3.1-8b-instant` - Más rápido, posts más simples
- `mixtral-8x7b-32768` - Más creativo y detallado

### 5. Ajustar Longitud de Posts

En los prompts, modifica:

```python
- Tener entre 150-200 palabras    # Cambiar a: 100-150 o 200-300
```

### 6. Cambiar Idioma de Generación

Edita el `system` prompt (línea ~60):

```python
"content": "Eres un experto en crear contenido profesional para LinkedIn en español/inglés/portugués."
```

Y en cada prompt específico:

```python
f"""Crea un post profesional EN INGLÉS para LinkedIn sobre "{tema}"."""
```

### 7. Aplicar Cambios con Docker

Después de editar el archivo:

```bash
# Los cambios se aplican automáticamente gracias al volumen montado
docker-compose run --rm linkedin-generator

# O si necesitas reconstruir:
docker-compose build --no-cache
docker-compose run --rm linkedin-generator
```

## Licencia

MIT License - Libre para uso personal y comercial