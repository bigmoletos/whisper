# Glossaire Technique - Guide d'amélioration de la transcription

## Comment améliorer la reconnaissance des mots techniques

### Solution 1 : Prompt Initial (Le plus simple ✅)

Le fichier `config.json` contient maintenant un champ `initial_prompt` que vous pouvez personnaliser.

#### Exemple actuel :
```json
"initial_prompt": "Voici une transcription technique incluant des termes comme Ollama, Whisper, Docker, Kubernetes..."
```

#### Comment personnaliser :
1. Ouvrez `projects/voice-to-text-basic/config.json`
2. Modifiez le champ `initial_prompt` pour inclure **VOS** mots techniques
3. Relancez l'application

#### Exemples par domaine :

**Java / Microservices (ACTUELLEMENT CONFIGURÉ) :**
```
Transcription technique Java microservices : Spring Boot, Spring Cloud, Kubernetes, Docker, Maven, Gradle, JUnit, Mockito, Hibernate, JPA, PostgreSQL, MongoDB, Redis, Kafka, RabbitMQ, REST API, GraphQL, OAuth2, JWT, Microservice, Service Mesh, Istio, Prometheus, Grafana, ELK, Elasticsearch, Logstash, Kibana, Jenkins, GitLab CI, ArgoCD, Helm, Terraform, Ansible, AWS, Azure, GCP, Lambda, S3, EC2, RDS, DynamoDB, API Gateway, Load Balancer, Nginx, Apache, Tomcat, Netty, Reactive, WebFlux, Actuator, Eureka, Consul, Zipkin, Jaeger, Resilience4j, Circuit Breaker, Feign Client, OpenFeign, Config Server, Vault, Secrets Manager
```

**Termes Java supplémentaires :**
```
Java Enterprise : JavaEE, Jakarta EE, JAX-RS, JAX-WS, JSF, Servlet, Filter, Interceptor, Bean Validation, CDI, EJB, Quarkus, Micronaut, Vert.x, Helidon, Dropwizard, Play Framework, Spark Java, Ratpack, Javalin
```

**Frameworks Java :**
```
Spring Ecosystem : Spring MVC, Spring Data, Spring Security, Spring Batch, Spring Integration, Spring HATEOAS, Spring Session, Spring WebSocket, Spring Cache, Spring Retry, Spring Cloud Gateway, Spring Cloud Config, Spring Cloud Netflix, Spring Cloud Sleuth, Spring Cloud Stream
```

**Tests & Qualité Java :**
```
Testing : JUnit 5, TestNG, Mockito, MockMvc, RestAssured, WireMock, Testcontainers, Cucumber, ArchUnit, JaCoCo, Sonar, SpotBugs, Checkstyle, PMD, JMH, Gatling, JMeter
```

**DevOps / Infrastructure :**
```
Transcription technique : Docker, Kubernetes, Terraform, Ansible, Jenkins, GitLab CI, Prometheus, Grafana, Helm, ArgoCD, Tekton, Argo Workflows
```

**Développement Python :**
```
Transcription Python : FastAPI, Django, Flask, PyTorch, TensorFlow, NumPy, Pandas, Scikit-learn, pytest, asyncio
```

**Cloud / AWS :**
```
Transcription cloud : AWS, EC2, S3, Lambda, ECS, CloudFormation, Azure, GCP, Kubernetes, Terraform
```

**Data Science / IA :**
```
Transcription data science : LLM, GPT, BERT, transformer, embedding, fine-tuning, dataset, preprocessing, inference
```

---

## Comment réduire les fautes d'orthographe ✅

### Améliorations appliquées automatiquement :

Le code a été modifié pour utiliser les **meilleurs paramètres de qualité** :

1. **Temperature = 0** : Plus déterministe, moins de variations aléatoires
2. **Beam Search activé** : Explore plusieurs possibilités pour choisir la meilleure
3. **Context-aware** : Utilise le contexte précédent pour cohérence
4. **Filtres de qualité** : Rejette les transcriptions de faible qualité

Ces paramètres améliorent **significativement** l'orthographe et la cohérence.

### Si vous avez encore des fautes :

**1. Utilisez un modèle plus gros** (medium → large-v3) :
```json
"model": "large-v3"
```

**2. Parlez plus lentement et distinctement** :
- Articulation claire
- Pause entre les phrases
- Prononciation soignée des mots complexes

**3. Améliorez la qualité audio** :
- Micro de qualité (ou casque-micro)
- Silence dans la pièce
- Distance micro : 15-30cm de la bouche

**4. Reformulez si mal reconnu** :
- Répétez la phrase différemment
- Décomposez les phrases longues
- Épeler les noms propres difficiles

---

## Solution 2 : Utiliser un modèle plus gros

Plus le modèle est gros, meilleure est la précision :

| Modèle | Précision | Vitesse | Recommandation |
|--------|-----------|---------|----------------|
| base | ⭐⭐ | ⚡⚡⚡ | Trop faible |
| **medium** | ⭐⭐⭐⭐ | ⚡⚡ | **Actuellement utilisé** |
| large-v3 | ⭐⭐⭐⭐⭐ | ⚡ | Meilleur pour français |

Pour passer à `large-v3` :
```json
"model": "large-v3"
```

---

## Solution 3 : Post-processing avec corrections

Créez un fichier de corrections automatiques pour vos termes métiers.

Exemple : `corrections.json`
```json
{
  "olama": "Ollama",
  "whisperr": "Whisper",
  "docker": "Docker",
  "kubernetesse": "Kubernetes"
}
```

---

## Solution 4 : Combiner plusieurs techniques

**Configuration optimale pour vocabulaire technique Java/microservices :**
```json
{
  "whisper": {
    "engine": "whisper",
    "model": "large-v3",
    "language": "fr",
    "device": "cpu",
    "initial_prompt": "Transcription Java microservices : Spring Boot, Spring Cloud, Kubernetes, Docker, Maven, Gradle, Hibernate, JPA, PostgreSQL, MongoDB, Redis, Kafka, REST API, GraphQL, OAuth2, JWT, Microservice, Prometheus, Grafana, Jenkins, AWS"
  }
}
```

**Note :** La configuration actuelle utilise déjà un prompt Java/microservices très complet ! Les paramètres de qualité ont aussi été optimisés automatiquement.

---

## Astuces supplémentaires

### 1. **Articuler clairement les termes techniques**
- Faites une pause avant/après les mots techniques
- Prononcez distinctement : "O-lla-ma" plutôt que "olama"

### 2. **Qualité audio**
- Microphone proche (15-30 cm)
- Environnement silencieux
- Éviter les bruits de fond

### 3. **Utiliser Voice-to-Text TURBO**
- Option [2] dans le menu
- Plus rapide, permet d'utiliser `large-v3` sans ralentissement

---

## Tester vos modifications

1. Modifiez `config.json` avec votre prompt personnalisé
2. Relancez `start.bat`
3. Testez avec une phrase contenant vos mots techniques
4. Ajustez le prompt si nécessaire

**Exemple de test :**
> "Je vais installer Ollama avec Docker et configurer Kubernetes pour déployer mon application FastAPI."

Si les mots sont mal reconnus, ajoutez-les au `initial_prompt` !
