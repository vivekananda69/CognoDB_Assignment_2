from django.shortcuts import render
from .cognodb import CognoDBManager

def student_graph_explorer(request):
    students = []
    error = None
    
    try:
        driver = CognoDBManager.get_driver()
        if driver:
            with driver.session() as session:
                # Query Students and their Enrolled Courses
                query = """
                MATCH (s:Student)-[:ENROLLED_IN]->(c:Course)
                RETURN s.id AS student_id, s.name AS student_name, s.gpa AS gpa, collect(c.title) AS courses
                """
                results = session.run(query)
                for record in results:
                    students.append({
                        'id': record['student_id'],
                        'name': record['student_name'],
                        'gpa': record['gpa'],
                        'courses': record['courses']
                    })
        else:
            error = "Could not connect to CognoDB driver."
    except Exception as e:
        error = f"Error fetching graph data: {str(e)}"

    return render(request, 'graph/explorer.html', {
        'students_list': students,
        'error_message': error
    })