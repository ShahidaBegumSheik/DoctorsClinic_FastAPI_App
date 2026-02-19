
def test_create_patient_requires_admin(admin_headers, client):
    # no auth
    res = client.post("/patients", json={"name": "Pat", "age": 25, "phone": "1234567890"})
    assert res.status_code in (401, 403)

    # with admin
    res = client.post("/patients", json={"name": "Pat", "age": 25, "phone": "1234567890"}, headers=admin_headers)
    assert res.status_code == 200
    assert res.json()["name"] == "Pat"


def test_create_patient_phone_validation_422(admin_headers, client):
    res = client.post(
        "/patients",
        json={"name": "Bad Phone", "age": 30, "phone": "123-ABC-999"},
        headers=admin_headers,
    )
    assert res.status_code == 422


def test_list_patients_pagination_and_search(admin_headers, client):
    prefix = "Pytest Batch A"

    for i in range(15):
        client.post(
            "/patients",
            json={
                "name": f"{prefix} {i}",
                "age": 20 + i,
                "phone": f"555000{str(i).zfill(4)}",
            },
            headers=admin_headers,
        )

    res = client.get(f"/patients?q={prefix}&page=1&size=100", headers=admin_headers)
    assert res.status_code == 200
    body = res.json()
    assert body["meta"]["total"] == 15
    assert len(body["items"]) == 15

    res = client.get("/patients?q=0005&size=100", headers=admin_headers)
    assert res.status_code == 200
    assert res.json()["meta"]["total"] >= 1


def test_get_missing_patient_returns_404(admin_headers, client):
    res = client.get("/patients/9999", headers=admin_headers)
    assert res.status_code == 404
    assert res.json()["detail"] == "Patient not found"
