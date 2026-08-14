from .cognodb import CognoDBManager

def execute_read_query(query, parameters=None):
    driver = CognoDBManager.get_driver()
    if not driver:
        return None, "Unable to connect to the graph database. Please try again."

    try:
        with driver.session() as session:
            result = session.execute_read(lambda tx: list(tx.run(query, parameters or {})))
            return result, None
    except Exception:
        return None, "Unable to connect to the graph database. Please try again."

def get_all_hotels():
    query = "MATCH (h:Hotel) RETURN h.id AS id, h.name AS name ORDER BY h.name ASC"
    records, error = execute_read_query(query)
    if error or records is None:
        return [], error
    return [{"id": r["id"], "name": r["name"]} for r in records], None

def get_hotel_details_and_related(hotel_id):
    # Selected Hotel Query
    sel_query = """
    MATCH (h:Hotel {id: $hotel_id})
    OPTIONAL MATCH (h)-[:LOCATED_IN]->(l:Location)
    OPTIONAL MATCH (h)-[:HAS_AMENITY]->(a:Amenity)
    RETURN h.id AS id, h.name AS name, h.rating AS rating,
           l.city AS city, l.country AS country, collect(a.name) AS amenities
    """

    # Multi-Hop Traversal Query (Hotel -> Amenity <- Other Hotel -> Location)
    rel_query = """
    MATCH (h:Hotel)-[:HAS_AMENITY]->(a:Amenity)<-[:HAS_AMENITY]-(other:Hotel)
    MATCH (other)-[:LOCATED_IN]->(location:Location)
    WHERE h.id = $hotel_id AND h <> other
    RETURN other.id AS id, other.name AS name, other.rating AS rating,
           location.city AS city, collect(a.name) AS shared_amenities,
           count(a) AS similarity
    ORDER BY similarity DESC LIMIT 5
    """

    params = {"hotel_id": hotel_id}
    sel_records, err1 = execute_read_query(sel_query, params)
    if err1: return None, [], err1
    if not sel_records: return None, [], None

    s = sel_records[0]
    selected_hotel = {
        "id": s["id"], "name": s["name"], "rating": s["rating"],
        "city": s["city"] or "Unknown", "country": s["country"] or "",
        "amenities": s["amenities"] or []
    }

    rel_records, err2 = execute_read_query(rel_query, params)
    if err2: return selected_hotel, [], err2

    related_hotels = [{
        "id": r["id"], "name": r["name"], "rating": r["rating"],
        "city": r["city"], "shared_amenities": r["shared_amenities"],
        "similarity": r["similarity"]
    } for r in rel_records]

    return selected_hotel, related_hotels, None