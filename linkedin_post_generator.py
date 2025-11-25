import requests
import json
import random
from datetime import datetime
import os

class LinkedInPostGenerator:
    def __init__(self, api_key=None):
        """
        Inicializa el generador de posts.
        API gratuita recomendada: Groq (https://console.groq.com)
        Alternativamente: Hugging Face
        """
        self.api_key = api_key or os.getenv('GROQ_API_KEY')
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        
        # Temas disponibles con variaciones
        self.temas = {
            "empleo": [
                "consejos para entrevistas de trabajo",
                "desarrollo de carrera profesional",
                "networking efectivo",
                "búsqueda de empleo en tech",
                "habilidades blandas más demandadas",
                "negociación salarial",
                "trabajo remoto y productividad"
            ],
            "java_spring": [
                "microservicios con Spring Boot",
                "mejores prácticas en Spring Security",
                "optimización de aplicaciones Spring",
                "Spring Boot vs frameworks tradicionales",
                "arquitectura hexagonal con Spring",
                "testing en Spring Boot",
                "deployment de aplicaciones Spring"
            ],
            "idiomas": [
                "aprender inglés para desarrolladores",
                "importancia del inglés en tech",
                "recursos para estudiar portugués",
                "diferencias entre español y portugués",
                "inglés técnico para programadores",
                "certificaciones de idiomas más valoradas",
                "comunicación multicultural en equipos remotos"
            ]
        }
    
    def generar_prompt(self, categoria, tema):
        """Genera un prompt optimizado para crear posts de LinkedIn"""
        prompts = {
            "empleo": f"""Crea un post profesional para LinkedIn sobre "{tema}". 
            El post debe:
            - Tener entre 150-200 palabras
            - Ser inspirador y práctico
            - Incluir 2-3 consejos concretos
            - Terminar con una pregunta para generar engagement
            - Usar un tono profesional pero cercano
            - NO incluir hashtags (los agregaré después)
            - Escribir en primera persona cuando sea apropiado""",
            
            "java_spring": f"""Crea un post técnico para LinkedIn sobre "{tema}".
            El post debe:
            - Tener entre 150-200 palabras
            - Compartir conocimiento técnico de forma accesible
            - Incluir un ejemplo práctico o caso de uso
            - Mencionar beneficios concretos
            - Terminar con una pregunta o invitación a comentar
            - Usar un tono profesional pero no demasiado académico
            - NO incluir hashtags ni código extenso""",
            
            "idiomas": f"""Crea un post motivacional para LinkedIn sobre "{tema}".
            El post debe:
            - Tener entre 150-200 palabras
            - Ser motivador e inspirador
            - Compartir beneficios de aprender idiomas en el ámbito profesional
            - Incluir consejos prácticos
            - Terminar con una pregunta para fomentar la conversación
            - Usar un tono amigable y cercano
            - NO incluir hashtags"""
        }
        return prompts[categoria]
    
    def generar_post_con_ia(self, categoria, tema):
        """Llama a la API de Groq para generar el contenido del post"""
        if not self.api_key:
            return self.generar_post_fallback(categoria, tema)
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            prompt = self.generar_prompt(categoria, tema)
            
            data = {
                "model": "llama-3.3-70b-versatile",  # Modelo gratuito de Groq
                "messages": [
                    {
                        "role": "system",
                        "content": "Eres un experto en crear contenido profesional para LinkedIn. Creas posts engaging, profesionales y valiosos."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.8,
                "max_tokens": 500
            }
            
            response = requests.post(self.api_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            contenido = result['choices'][0]['message']['content'].strip()
            
            return contenido
            
        except Exception as e:
            print(f"Error al llamar a la API: {e}")
    
    def agregar_hashtags(self, categoria):
        """Agrega hashtags relevantes según la categoría"""
        hashtags_map = {
            "empleo": ["#Empleo", "#DesarrolloCarrera", "#LinkedIn", "#TrabajoTech", "#Networking"],
            "java_spring": ["#Java", "#SpringBoot", "#Desarrollo", "#Programming", "#Backend"],
            "idiomas": ["#Idiomas", "#AprendizajeIdiomas", "#Inglés", "#DesarrolloProfesional", "#Multilingüe"]
        }
        tags = hashtags_map.get(categoria, [])
        random.shuffle(tags)
        return " ".join(tags[:4])  # Usar 4 hashtags aleatorios
    
    def generar_posts(self, cantidad=5):
        """Genera múltiples posts y los guarda"""
        posts_generados = []
        
        print(f"Generando {cantidad} posts para LinkedIn...\n")
        
        for i in range(cantidad):
            # Seleccionar categoría y tema aleatorios
            categoria = random.choice(list(self.temas.keys()))
            tema = random.choice(self.temas[categoria])
            
            print(f"Generando post {i+1}/{cantidad}: {categoria} - {tema}")
            
            # Generar contenido con IA
            contenido = self.generar_post_con_ia(categoria, tema)
            
            # Agregar hashtags
            hashtags = self.agregar_hashtags(categoria)
            post_completo = f"{contenido}\n\n{hashtags}"
            
            # Crear objeto del post
            post = {
                "id": i + 1,
                "categoria": categoria,
                "tema": tema,
                "contenido": contenido,
                "hashtags": hashtags,
                "post_completo": post_completo,
                "fecha_generacion": datetime.now().isoformat(),
                "publicado": False
            }
            
            posts_generados.append(post)
            print(f"Post generado exitosamente\n")
        
        return posts_generados
    
    def guardar_posts(self, posts, formato="json"):
        """Guarda los posts en un archivo"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if formato == "json":
            filename = f"linkedin_posts_{timestamp}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(posts, f, ensure_ascii=False, indent=2)
            print(f"Posts guardados en: {filename}")
        
        elif formato == "txt":
            filename = f"linkedin_posts_{timestamp}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                for post in posts:
                    f.write(f"{'='*60}\n")
                    f.write(f"POST #{post['id']} - {post['categoria'].upper()}\n")
                    f.write(f"Tema: {post['tema']}\n")
                    f.write(f"{'='*60}\n\n")
                    f.write(post['post_completo'])
                    f.write(f"\n\n{'='*60}\n\n")
            print(f"Posts guardados en: {filename}")
        
        return filename
    
    def mostrar_preview(self, posts, cantidad=2):
        """Muestra un preview de algunos posts"""
        print(f"\n{'='*60}")
        print("PREVIEW DE POSTS GENERADOS")
        print(f"{'='*60}\n")
        
        for post in posts[:cantidad]:
            print(f"POST #{post['id']} - {post['categoria'].upper()}")
            print(f"Tema: {post['tema']}")
            print("-" * 60)
            print(post['post_completo'])
            print(f"\n{'='*60}\n")


def main():
    """Función principal"""
    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║   GENERADOR DE POSTS DE LINKEDIN CON IA              ║
    ║   Para obtener API key gratuita: console.groq.com    ║
    ╚═══════════════════════════════════════════════════════╝
    """)
    
    # Configuración
    api_key = input("Ingresa tu API key de Groq (o presiona Enter para usar modo fallback): ").strip()
    #api_key =
    if not api_key:
        print("\n⚠️  Usando modo fallback (sin IA). Los posts serán más básicos.")
        api_key = None
    
    cantidad = int(input("¿Cuántos posts deseas generar? (recomendado: 5-10): ") or "5")
    
    # Crear generador
    generador = LinkedInPostGenerator(api_key=api_key)
    
    # Generar posts
    posts = generador.generar_posts(cantidad=cantidad)
    
    # Mostrar preview
    generador.mostrar_preview(posts, cantidad=2)
    
    # Guardar posts
    print("\nGuardando posts...")
    archivo_json = generador.guardar_posts(posts, formato="json")
    archivo_txt = generador.guardar_posts(posts, formato="txt")
    
    print(f"""
    ¡Proceso completado exitosamente!
    
    Archivos generados:
        - {archivo_json} (formato estructurado)
        - {archivo_txt} (formato legible)
    
    Próximos pasos:
        1. Revisa los posts generados
        2. Edita o personaliza según necesites
        3. Copia y pega en LinkedIn para publicar
        4. ¡Monitorea el engagement!
    
    Tip: Publica en horarios de mayor actividad (8-10am, 12-1pm, 5-6pm)
    """)


if __name__ == "__main__":
    main()