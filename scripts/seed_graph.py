import os
import sys
import django
from pathlib import Path

# Setup Django Environment
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rattlesnake.settings')
django.setup()

from app.graph.cognodb import CognoDBManager

CYPHER_SCRIPT = """
CREATE (s1:Student {id: 'S101', name: 'Alice Smith', email: 'alice@example.com', gpa: 3.8});
CREATE (s2:Student {id: 'S102', name: 'Bob Jones', email: 'bob@example.com', gpa: 3.5});
CREATE (c1:Course {code: 'CS101', title: 'Intro to Computer Science', credits: 4});
CREATE (c2:Course {code: 'CS202', title: 'Data Structures & Algorithms', credits: 4});
CREATE (d1:Department {name: 'Computer Science', code: 'CS'});

MATCH (s1:Student {id: 'S101'}), (c1:Course {code: 'CS101'}) CREATE (s1)-[:ENROLLED_IN]->(c1);
MATCH (s1:Student {id: 'S101'}), (c2:Course {code: 'CS202'}) CREATE (s1)-[:ENROLLED_IN]->(c2);
MATCH (s2:Student {id: 'S102'}), (c1:Course {code: 'CS101'}) CREATE (s2)-[:ENROLLED_IN]->(c1);
MATCH (c1:Course {code: 'CS101'}), (d1:Department {code: 'CS'}) CREATE (c1)-[:BELONGS_TO]->(d1);
MATCH (c2:Course {code: 'CS202'}), (d1:Department {code: 'CS'}) CREATE (c2)-[:BELONGS_TO]->(d1);
"""

def seed():
    driver = CognoDBManager.get_driver()
    if not driver:
        print("Could not get database driver.")
        return

    statements = [stmt.strip() for stmt in CYPHER_SCRIPT.split(';') if stmt.strip()]

    with driver.session() as session:
        # Clear existing hotel data first
        session.execute_write(lambda tx: tx.run("MATCH (n) DETACH DELETE n"))
        
        # Seed student graph data
        for statement in statements:
            session.execute_write(lambda tx: tx.run(statement))
            
    print("Student graph database seeded successfully!")

if __name__ == '__main__':
    seed()