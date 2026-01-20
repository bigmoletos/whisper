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

**Git & Gestion de versions :**
```
Plateformes : GitHub, GitLab, Bitbucket, Azure DevOps, Gitea, Gogs
Commandes : commit, push, pull, fetch, merge, rebase, cherry-pick, stash, branch, checkout, clone, fork, tag, release, squash, reset, revert
Concepts : pull request, merge request, code review, conflict, diff, patch, blame, log, status, remote, origin, upstream
Workflows : GitFlow, GitHub Flow, trunk-based development, feature branch, hotfix, release branch
```

**Tests & Qualité (tous langages) :**
```
Tests frontend : Playwright, Selenium, Cypress, Puppeteer, TestCafe, WebDriverIO
Tests backend : JUnit, TestNG, Mockito, RestAssured, WireMock, Postman, Insomnia
Tests E2E : Cucumber, SpecFlow, Behave, Robot Framework
Qualité code : SonarQube, SonarCloud, Checkmarx, Veracode, Snyk, CodeQL, Fortify
Linters : ESLint, Prettier, Checkstyle, PMD, SpotBugs, Pylint, Flake8, RuboCop
Coverage : JaCoCo, Istanbul, Coverage.py, SimpleCov
Performance : JMeter, Gatling, Locust, K6, Artillery
```

**DevOps / Infrastructure :**
```
Transcription technique : Docker, Kubernetes, Terraform, Ansible, Jenkins, GitLab CI, Prometheus, Grafana, Helm, ArgoCD, Tekton, Argo Workflows
CI/CD : Jenkins, GitLab CI, GitHub Actions, CircleCI, Travis CI, Azure Pipelines, Bamboo, TeamCity
Conteneurs : Docker, Podman, Buildah, Containerd, CRI-O, Docker Compose, Docker Swarm
Orchestration : Kubernetes, OpenShift, Rancher, Nomad, Docker Swarm, ECS, AKS, GKE, EKS
```

**Formats de fichiers techniques :**
```
Configuration : point JSON, point YAML, point YML, point TOML, point INI, point CONF, point PROPERTIES, point ENV, point DOTENV
Code : point JAVA, point PY, point JS, point TS, point GO, point RS, point C, point CPP, point H, point CS
Scripts : point SH, point BASH, point BAT, point CMD, point PS1, point PSQL
Web : point HTML, point CSS, point SCSS, point SASS, point LESS, point JSX, point TSX, point VUE
Données : point CSV, point XML, point SQL, point PARQUET, point AVRO, point PROTO
Documentation : point MD, point MARKDOWN, point RST, point ADOC, point TXT, point PDF
Logs : point LOG, point OUT, point ERR, point TRACE
Build : point GRADLE, point POM, point XML, point LOCK, point SUM
Infrastructure : point TF, point HCL, point TFVARS, point YML pour Ansible et Docker Compose
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

## 📄 Guide spécial : Extensions de fichiers

### Comment dicter les extensions de fichiers

Whisper peut confondre les extensions avec des mots normaux. Voici comment les dicter :

**❌ Ne dites PAS :**
- "fichier point j s o n" → risque : "fichier . Jason"
- "script dot bat" → risque : "script dot bât"

**✅ Dites plutôt :**

#### Méthode 1 : "point + extension" (RECOMMANDÉ)
```
"le fichier point JSON"        → ✅ le fichier .json
"un script point BAT"          → ✅ un script .bat
"le document point MD"         → ✅ le document .md
"configuration point YAML"     → ✅ configuration .yaml
```

#### Méthode 2 : Épeler pour les extensions ambiguës
```
"fichier P-O-M point X-M-L"    → pom.xml
"script point S-H"             → script.sh
"config point E-N-V"           → config.env
```

### Extensions courantes et leur prononciation

| Extension | Comment dicter | Éviter |
|-----------|---------------|---------|
| .md | "point MD" ou "point markdown" | "point M D" |
| .json | "point JSON" | "point Jason" |
| .yaml / .yml | "point YAML" | "point yamel" |
| .csv | "point CSV" | "point C S V" |
| .xml | "point XML" | "point x m l" |
| .bat | "point BAT" | "point batte" |
| .sh | "point SH" ou "point shell" | "point S H" |
| .ps1 | "point PS1" ou "point PowerShell" | "point P S 1" |
| .py | "point PY" ou "point Python" | "point P Y" |
| .java | "point JAVA" | "point java" |
| .js | "point JS" ou "point JavaScript" | "point J S" |
| .ts | "point TS" ou "point TypeScript" | "point T S" |
| .html | "point HTML" | "point H T M L" |
| .css | "point CSS" | "point C S S" |
| .sql | "point SQL" | "point S Q L" |
| .txt | "point TXT" ou "point texte" | "point T X T" |
| .log | "point LOG" | "point logue" |
| .env | "point ENV" | "point N V" |
| .properties | "point PROPERTIES" | "point propriété" |
| .conf | "point CONF" ou "point config" | "point confe" |
| .ini | "point INI" | "point I N I" |
| .toml | "point TOML" | "point tomle" |

### Exemples de phrases complètes

```
✅ "J'ouvre le fichier configuration point JSON"
✅ "Le script de déploiement point SH doit être modifié"
✅ "Les données sont dans le fichier point CSV"
✅ "La documentation est dans le README point MD"
✅ "Le batch Windows point BAT lance l'application"
✅ "Le script PowerShell point PS1 automatise le processus"
✅ "Les tests sont dans point JAVA et point XML"
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
