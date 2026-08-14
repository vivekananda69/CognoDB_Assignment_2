

```markdown
# Student Graph Explorer (CognoDB)

A Django-based web application backed by a **CognoDB** graph database layer to explore students, course enrollments, and academic departments.

---

## 1. Use Case & "Why a Graph Database?"

### Use Case
This application models an academic ecosystem where students enroll in courses and courses belong to academic departments. The goal is to easily trace academic relationships, student course loads, and department affiliations.

### Why a Graph Database Over Relational SQL?
* **Elimination of Join Tables:** In traditional relational databases (SQL), querying student enrollments across departments requires querying junction tables (`Student` -> `Enrollment` -> `Course` -> `Department`).
* **Fast Multi-Hop Traversal:** Graph databases store relationships natively as edges. Traversing from a `Student` node to a `Department` node (2+ hops) is a direct pointer lookup rather than an expensive multi-table `JOIN`.
* **Flexible Schema:** Adding new relationship types (e.g., `PREREQUISITE_FOR` between courses or `ADVISED_BY` between students and faculty) does not require complex SQL schema migrations.

---

## 2. Data Model Diagram


```

(:Student) -[:ENROLLED_IN]-> (:Course) -[:BELONGS_TO]-> (:Department)

```

* **Nodes:**
  * `Student` (`id`, `name`, `email`, `gpa`)
  * `Course` (`code`, `title`, `credits`)
  * `Department` (`name`, `code`)
* **Relationships:**
  * `(:Student)-[:ENROLLED_IN]->(:Course)`
  * `(:Course)-[:BELONGS_TO]->(:Department)`

---

## 3. Key Cypher Queries

### Multi-Hop Traversal (Student to Department)
Fetch students and their enrolled courses under a specific department code:

```cypher
MATCH (s:Student)-[:ENROLLED_IN]->(c:Course)-[:BELONGS_TO]->(d:Department)
WHERE d.code = $dept_code
RETURN s.name AS student_name, c.title AS course_title, d.name AS department_name

```

### Student Enrollment Overview

Fetch all students along with an aggregated list of their enrolled courses:

```cypher
MATCH (s:Student)-[:ENROLLED_IN]->(c:Course)
RETURN s.id AS student_id, 
       s.name AS student_name, 
       s.gpa AS gpa, 
       collect(c.title) AS courses

```

---

## 4. CognoDB Setup & Local Installation

### Prerequisites

* Python 3.10+
* A free instance on [CognoDB Cloud](https://www.google.com/search?q=https://console.cognodb.com/)

### Step 1: Clone Repository & Virtual Environment

```bash
git clone <YOUR_REPOSITORY_URL>
cd django-crud-sqlite

# Create and activate virtual environment
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On macOS/Linux:
source venv/bin/activate

```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt

```

### Step 3: Environment Configuration

Create a `.env` file in the root directory (alongside `manage.py`):

```env
COGNODB_URI=bolt+s://<your-instance-id>.databases.cognodb.cloud:7687
COGNODB_USERNAME=cognodb
COGNODB_PASSWORD=<your-generated-password>

```

### Step 4: Seed Graph Data & Run Migrations

```bash
# Seed student graph data into CognoDB
python scripts/seed_graph.py

# Apply local SQLite migrations
python manage.py migrate

# Start the Django development server
python manage.py runserver

```

---

## 5. Usage

1. Open your browser and navigate to `http://127.0.0.1:8000/graph/` to launch the **Student Graph Explorer**.
2. Navigate to `http://127.0.0.1:8000/` to access the core application routes.

```

```
