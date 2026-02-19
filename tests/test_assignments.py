
def _login(client, email: str, password: str) -> str:
    res = client.post(
        "/auth/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert res.status_code == 200, res.text
    return res.json()["access_token"]


def test_admin_can_assign_and_list_doctor_patients(admin_headers, client):
    doctor = client.post(
        "/doctors",
        json={
            "name": "Dr Assign",
            "specialization": "General",
            "emailid": "assign.doc@example.com",
            "password": "Password123!",
        },
        headers=admin_headers,
    ).json()

    patient = client.post(
        "/patients",
        json={"name": "Assigned Patient", "age": 40, "phone": "1234567890"},
        headers=admin_headers,
    ).json()

    res = client.post(
        f"/doctors/{doctor['id']}/patients/{patient['id']}",
        headers=admin_headers,
    )
    assert res.status_code == 200
    assert res.json()["message"] == "Patient assigned"

    res = client.post(
        f"/doctors/{doctor['id']}/patients/{patient['id']}",
        headers=admin_headers,
    )
    assert res.status_code == 200

    res = client.get(f"/doctors/{doctor['id']}/patients", headers=admin_headers)
    assert res.status_code == 200
    items = res.json()
    assert len(items) == 1
    assert items[0]["id"] == patient["id"]


def test_assign_to_inactive_doctor_returns_400(admin_headers, client):
    doctor = client.post(
        "/doctors",
        json={
            "name": "Dr Inactive",
            "specialization": "General",
            "emailid": "inactive.doc@example.com",
            "password": "Password123!",
        },
        headers=admin_headers,
    ).json()

    # deactivate
    client.put(f"/doctors/{doctor['id']}", json={"is_active": False}, headers=admin_headers)

    patient = client.post(
        "/patients",
        json={"name": "Patient", "age": 22, "phone": "1234567891"},
        headers=admin_headers,
    ).json()

    res = client.post(
        f"/doctors/{doctor['id']}/patients/{patient['id']}",
        headers=admin_headers,
    )
    assert res.status_code == 400
    assert res.json()["detail"] == "Doctor is inactive"


def test_doctor_can_only_view_own_patients(admin_headers, client):
    # Create two doctors
    doc1_payload = {
        "name": "Dr One",
        "specialization": "General",
        "emailid": "doc1@example.com",
        "password": "Password123!",
    }
    doc2_payload = {
        "name": "Dr Two",
        "specialization": "General",
        "emailid": "doc2@example.com",
        "password": "Password123!",
    }

    doc1 = client.post("/doctors", json=doc1_payload, headers=admin_headers).json()
    doc2 = client.post("/doctors", json=doc2_payload, headers=admin_headers).json()

    patient = client.post(
        "/patients",
        json={"name": "Patient X", "age": 33, "phone": "1234567892"},
        headers=admin_headers,
    ).json()

    client.post(f"/doctors/{doc1['id']}/patients/{patient['id']}", headers=admin_headers)

    token = _login(client, doc1_payload["emailid"], doc1_payload["password"])
    doc1_headers = {"Authorization": f"Bearer {token}"}

    res = client.get(f"/doctors/{doc1['id']}/patients", headers=doc1_headers)
    assert res.status_code == 200
    assert len(res.json()) == 1

    res = client.get(f"/doctors/{doc2['id']}/patients", headers=doc1_headers)
    assert res.status_code == 403
    assert res.json()["detail"] == "Doctors can only view their own patients"
