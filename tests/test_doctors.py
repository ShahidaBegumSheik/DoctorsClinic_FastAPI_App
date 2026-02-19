
def test_doctors_requires_auth(client):
    res = client.get("/doctors")
    assert res.status_code in (401, 403)

def test_create_and_list_doctors(admin_headers, client):
    d1 = {
        "name": "Dr Alice",
        "specialization": "Cardiology",
        "emailid": "alice.doc@example.com",
        "password": "Password123!",
    }
    d2 = {
        "name": "Dr Bob",
        "specialization": "Dermatology",
        "emailid": "bob.doc@example.com",
        "password": "Password123!",
    }

    r1 = client.post("/doctors", json=d1, headers=admin_headers)
    assert r1.status_code == 200, r1.text
    r2 = client.post("/doctors", json=d2, headers=admin_headers)
    assert r2.status_code == 200, r2.text

    id1 = r1.json()["id"]
    id2 = r2.json()["id"]

    res = client.get("/doctors?page=1&size=100", headers=admin_headers)
    assert res.status_code == 200
    body = res.json()

    assert body["meta"]["page"] == 1
    assert body["meta"]["size"] == 100
    assert body["meta"]["total"] >= 2

    ids = {d["id"] for d in body["items"]}
    assert id1 in ids
    assert id2 in ids

def test_list_doctors_filters_by_search_and_active(admin_headers, client):
    d1 = client.post(
        "/doctors",
        json={
            "name": "Dr Cathy",
            "specialization": "Neurology",
            "emailid": "cathy.doc@example.com",
            "password": "Password123!",
        },
        headers=admin_headers,
    ).json()

    d2 = client.post(
        "/doctors",
        json={
            "name": "Dr Dan",
            "specialization": "Orthopedics",
            "emailid": "dan.doc@example.com",
            "password": "Password123!",
        },
        headers=admin_headers,
    ).json()

    upd = client.put(f"/doctors/{d2['id']}", json={"is_active": False}, headers=admin_headers)
    assert upd.status_code == 200
    assert upd.json()["is_active"] is False

    res = client.get("/doctors?q=Neuro&size=100", headers=admin_headers)
    assert res.status_code == 200
    ids = {d["id"] for d in res.json()["items"]}
    assert d1["id"] in ids

    res = client.get("/doctors?is_active=false&size=100", headers=admin_headers)
    assert res.status_code == 200
    ids = {d["id"] for d in res.json()["items"]}
    assert d2["id"] in ids

def test_get_update_delete_doctor(admin_headers, client):
    created = client.post(
        "/doctors",
        json={
            "name": "Dr Eve",
            "specialization": "ENT",
            "emailid": "eve.doc@example.com",
            "password": "Password123!",
        },
        headers=admin_headers,
    ).json()

    res = client.get(f"/doctors/{created['id']}", headers=admin_headers)
    assert res.status_code == 200
    assert res.json()["emailid"] == "eve.doc@example.com"

    res = client.put(
        f"/doctors/{created['id']}",
        json={"name": "Dr Eve Updated", "specialization": "ENT", "is_active": True},
        headers=admin_headers,
    )
    assert res.status_code == 200
    assert res.json()["name"] == "Dr Eve Updated"

    res = client.delete(f"/doctors/{created['id']}", headers=admin_headers)
    assert res.status_code == 200
    assert res.json()["is_active"] is False

def test_get_missing_doctor_returns_404(admin_headers, client):
    res = client.get("/doctors/9999", headers=admin_headers)
    assert res.status_code == 404
    assert res.json()["detail"] == "Doctor not found"
